"""Sensor for Econet300."""

from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
import logging
from typing import Any

from homeassistant.components.sensor import (
    RestoreSensor,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory, UnitOfMass
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api import Econet300Api
from .common import EconetDataCoordinator
from .common_functions import camel_to_snake, get_entity_component
from .const import (
    COMPONENT_LAMBDA,
    DOMAIN,
    ENTITY_CATEGORY,
    ENTITY_PRECISION,
    ENTITY_SENSOR_DEVICE_CLASS_MAP,
    ENTITY_UNIT_MAP,
    ENTITY_VALUE_PROCESSOR,
    SENSOR_ENUM_OPTIONS,
    SENSOR_MAP_KEY,
    SENSOR_MIXER_KEY,
    SERVICE_API,
    SERVICE_COORDINATOR,
    SERVICE_FUEL_TRACKER,
    STATE_CLASS_MAP,
)
from .entity import (
    EconetEntity,
    EcoSterEntity,
    LambdaEntity,
    MixerEntity,
    get_device_info_for_component,
)

_LOGGER = logging.getLogger(__name__)

# Maximum time delta in seconds to prevent incorrect spikes after long gaps
MAX_TIME_DELTA_SECONDS = 300  # 5 minutes


class FuelConsumptionTracker:
    """Track total fuel consumption by integrating fuel stream rate over time.

    This class accumulates fuel consumption (kg) from a fuel stream rate (kg/h)
    by calculating the integral over time between updates.
    """

    def __init__(self) -> None:
        """Initialize the fuel consumption tracker."""
        self._total: float = 0.0
        self._last_reset: datetime | None = None
        self._last_update: datetime | None = None

    @property
    def total(self) -> float:
        """Return the total fuel consumption in kg."""
        return round(self._total, 3)

    @property
    def last_reset(self) -> datetime | None:
        """Return the timestamp of the last reset."""
        return self._last_reset

    @property
    def last_update(self) -> datetime | None:
        """Return the timestamp of the last update."""
        return self._last_update

    def restore(
        self,
        total: float | None,
        last_reset: datetime | None,
    ) -> None:
        """Restore the tracker state from persistent storage."""
        if total is not None:
            self._total = float(total)
        if last_reset is not None:
            self._last_reset = last_reset
        _LOGGER.debug(
            "Restored fuel consumption tracker: total=%.3f kg, last_reset=%s",
            self._total,
            self._last_reset,
        )

    def update(self, fuel_stream_kgh: float | None) -> float:
        """Update the total consumption based on current fuel stream rate."""
        now = datetime.now(timezone.utc)

        # Skip if fuel stream is None or zero (boiler off)
        if fuel_stream_kgh is None or fuel_stream_kgh <= 0:
            self._last_update = now
            return self._total

        # Calculate consumption since last update
        if self._last_update is not None:
            delta_seconds = (now - self._last_update).total_seconds()

            # Cap the delta to prevent incorrect spikes after long gaps
            if delta_seconds > MAX_TIME_DELTA_SECONDS:
                _LOGGER.debug(
                    "Time delta %.1fs exceeds max %.1fs, capping",
                    delta_seconds,
                    MAX_TIME_DELTA_SECONDS,
                )
                delta_seconds = MAX_TIME_DELTA_SECONDS

            if delta_seconds > 0:
                # Calculate consumption: rate (kg/h) * time (h)
                delta_hours = delta_seconds / 3600
                consumption = fuel_stream_kgh * delta_hours
                self._total += consumption

                _LOGGER.debug(
                    "Fuel consumption update: rate=%.3f kg/h, delta=%.1fs, "
                    "added=%.4f kg, total=%.3f kg",
                    fuel_stream_kgh,
                    delta_seconds,
                    consumption,
                    self._total,
                )

        self._last_update = now
        return self._total

    def reset(self) -> None:
        """Reset the fuel consumption counter to zero."""
        self._total = 0.0
        self._last_reset = datetime.now(timezone.utc)
        self._last_update = self._last_reset
        _LOGGER.info("Fuel consumption reset at %s", self._last_reset)

    def calibrate(self, value: float) -> None:
        """Calibrate the fuel consumption counter to a specific value."""
        self._total = value
        self._last_update = datetime.now(timezone.utc)
        _LOGGER.info("Fuel consumption calibrated to %.3f kg", value)


@dataclass(frozen=True)
class EconetSensorEntityDescription(SensorEntityDescription):
    """Describes ecoNET sensor entity."""

    process_val: Callable[[Any], Any] = lambda x: x  # noqa: E731
    component: str | None = None  # Component for device grouping (huw, mixer_1, etc.)


class EconetSensor(EconetEntity, SensorEntity):
    """Represents an ecoNET sensor entity."""

    entity_description: EconetSensorEntityDescription

    def __init__(
        self,
        entity_description: EconetSensorEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
    ):
        """Initialize a new ecoNET sensor entity."""
        self.entity_description = entity_description
        self.api = api
        self._attr_native_value = None
        self._raw_value: Any = None
        super().__init__(coordinator, api)

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device info based on entity component."""
        component = getattr(self.entity_description, "component", None)
        if component:
            return get_device_info_for_component(component, self.api)
        # Fall back to parent class device_info (main boiler device)
        return super().device_info

    @property
    def options(self) -> list[str] | None:
        """Return options for ENUM sensors."""
        return SENSOR_ENUM_OPTIONS.get(self.entity_description.key)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes for the sensor."""
        attrs: dict[str, Any] = {}
        if self._raw_value is not None:
            attrs["raw_value"] = self._raw_value
        return attrs

    def _sync_state(self, value) -> None:
        """Synchronize the state of the sensor entity."""
        self._raw_value = value
        self._attr_native_value = self.entity_description.process_val(value)
        self.async_write_ha_state()


class MixerSensor(MixerEntity, SensorEntity):
    """Mixer sensor class."""

    entity_description: EconetSensorEntityDescription

    def __init__(
        self,
        description: EconetSensorEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
        idx: int,
    ):
        """Initialize a new instance of the MixerSensor class."""
        super().__init__(description, coordinator, api, idx)
        self._attr_native_value = None

    def _sync_state(self, value) -> None:
        """Synchronize the state of the sensor entity."""
        self._attr_native_value = self.entity_description.process_val(value)
        self.async_write_ha_state()


class LambdaSensors(LambdaEntity, SensorEntity):
    """Lambda sensor class."""

    entity_description: EconetSensorEntityDescription

    def __init__(
        self,
        description: EconetSensorEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
    ):
        """Initialize a new instance of the LambdaSensors class."""
        super().__init__(description, coordinator, api)
        self._attr_native_value = None

    def _sync_state(self, value) -> None:
        """Synchronize the state of the sensor entity."""
        self._attr_native_value = self.entity_description.process_val(value)
        self.async_write_ha_state()


class EcoSterSensor(EcoSterEntity, SensorEntity):
    """EcoSter sensor class."""

    entity_description: EconetSensorEntityDescription

    def __init__(
        self,
        description: EconetSensorEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
        idx: int,
    ):
        """Initialize the EcoSter sensor."""
        self.entity_description = description
        self.api = api
        self._idx = idx
        super().__init__(description, coordinator, api, idx)

    def _sync_state(self, value) -> None:
        """Sync state."""
        _LOGGER.debug("EcoSter sensor sync state: %s", value)
        self._attr_native_value = self.entity_description.process_val(value)
        self.async_write_ha_state()


class InformationDynamicSensor(EconetEntity, SensorEntity):
    """Dynamic sensor entity for Information category parameters (read-only)."""

    entity_description: EconetSensorEntityDescription

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Return if entity should be enabled by default.

        CONFIG category entities are disabled by default.
        Other entities (DIAGNOSTIC or no category) are enabled.
        Sensors are typically read-only data, so they're enabled by default.
        """
        entity_category = getattr(self.entity_description, "entity_category", None)
        return entity_category != EntityCategory.CONFIG

    def __init__(
        self,
        entity_description: EconetSensorEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
        param_number: int,
    ):
        """Initialize a new Information dynamic sensor entity.

        Args:
            entity_description: Entity description
            coordinator: Data coordinator
            api: API instance
            param_number: Parameter number from merged data

        """
        self.entity_description = entity_description
        self.api = api
        self._param_number = param_number
        self._attr_native_value = None
        super().__init__(coordinator, api)

    def _sync_state(self, value) -> None:
        """Synchronize the state of the Information sensor entity."""
        _LOGGER.debug(
            "InformationDynamicSensor _sync_state for entity %s: %s",
            self.entity_description.key,
            value,
        )

        # Handle both dict and direct value
        if isinstance(value, dict) and "value" in value:
            val = value.get("value")
            self._attr_native_value = float(val) if val is not None else None
        elif isinstance(value, (int, float, str)) and value is not None:
            try:
                self._attr_native_value = float(value)
            except (ValueError, TypeError):
                self._attr_native_value = value
        else:
            self._attr_native_value = None

        self.async_write_ha_state()

    @property
    def native_value(self) -> float | None:
        """Return the native value of the sensor."""
        if self.coordinator.data is None:
            return None

        merged_data = self.coordinator.data.get("mergedData", {})
        if not merged_data:
            return None

        merged_parameters = merged_data.get("parameters", {})
        if not merged_parameters:
            return None

        # Find parameter by number
        for param in merged_parameters.values():
            if isinstance(param, dict) and param.get("number") == self._param_number:
                param_value = param.get("value")
                if param_value is not None:
                    try:
                        return float(param_value)
                    except (ValueError, TypeError):
                        return param_value
                break

        return None


# Custom device class for fuel consumption meter to allow targeting with services
DEVICE_CLASS_FUEL_METER = "econet300__fuel_meter"


class FuelConsumptionTotalSensor(RestoreSensor, CoordinatorEntity):
    """Sensor that tracks total fuel consumption by integrating fuel stream rate.

    This sensor calculates total fuel consumption (kg) by integrating the
    fuelStream rate (kg/h) over time. It persists across restarts using
    RestoreSensor. Reset and calibration are available via service actions.
    """

    _attr_has_entity_name = True
    _attr_translation_key = "fuel_consumption_total"
    _attr_device_class = DEVICE_CLASS_FUEL_METER  # type: ignore[assignment]
    _attr_native_unit_of_measurement = UnitOfMass.KILOGRAMS
    _attr_state_class = SensorStateClass.TOTAL_INCREASING
    _attr_suggested_display_precision = 2
    _attr_icon = "mdi:weight-kilogram"
    _unrecorded_attributes = frozenset({"burned_since_last_update"})

    def __init__(
        self,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
        tracker: FuelConsumptionTracker,
    ) -> None:
        """Initialize the fuel consumption total sensor.

        Args:
            coordinator: The data update coordinator
            api: The ecoNET API instance
            tracker: The fuel consumption tracker instance

        """
        super().__init__(coordinator)
        self._api = api
        self._tracker = tracker
        self._attr_unique_id = f"{api.uid}_fuel_consumption_total"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info for the main boiler device."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._api.uid)},
            name=self._api.model_id,
            manufacturer="Plum",
            model=self._api.model_id,
            sw_version=self._api.sw_rev,
        )

    @property
    def native_value(self) -> float | None:
        """Return the current total fuel consumption."""
        return self._tracker.total

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        attrs: dict[str, Any] = {}
        if self._tracker.last_update:
            attrs["last_update"] = self._tracker.last_update.isoformat()
        if self._tracker.last_reset:
            attrs["meter_reset_time"] = self._tracker.last_reset.isoformat()
        return attrs

    async def async_reset_meter(self) -> None:
        """Reset the fuel consumption meter to zero."""
        _LOGGER.info("Resetting fuel consumption meter")
        self._tracker.reset()
        self.async_write_ha_state()

    async def async_calibrate_meter(self, value: float) -> None:
        """Calibrate the fuel consumption meter to a specific value."""
        _LOGGER.info("Calibrating fuel consumption meter to %.3f kg", value)
        self._tracker.calibrate(value)
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        """Handle entity added to Home Assistant."""
        await super().async_added_to_hass()

        # Restore previous state
        last_sensor_data = await self.async_get_last_sensor_data()
        if last_sensor_data is not None and last_sensor_data.native_value is not None:
            native_val = last_sensor_data.native_value
            total_value: float | None = None
            if isinstance(native_val, (int, float)):
                total_value = float(native_val)
            elif isinstance(native_val, str):
                try:
                    total_value = float(native_val)
                except ValueError:
                    total_value = None

            # Get last_reset from stored state attributes
            last_state = await self.async_get_last_state()
            last_reset_value: datetime | None = None
            if last_state and last_state.attributes:
                last_reset_str = last_state.attributes.get("last_reset")
                if last_reset_str:
                    try:
                        last_reset_value = datetime.fromisoformat(last_reset_str)
                    except (ValueError, TypeError):
                        last_reset_value = None

            _LOGGER.info(
                "Restoring fuel consumption sensor: value=%s, last_reset=%s",
                total_value,
                last_reset_value,
            )
            self._tracker.restore(
                total=total_value,
                last_reset=last_reset_value,
            )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if self.coordinator.data is None:
            return

        reg_params = self.coordinator.data.get("regParams", {})
        if reg_params is None:
            return

        fuel_stream = reg_params.get("fuelStream")
        self._tracker.update(fuel_stream)

        # Update HA state
        self.async_write_ha_state()


def create_sensor_entity_description(key: str) -> EconetSensorEntityDescription:
    """Create ecoNET300 sensor entity based on supplied key."""
    _LOGGER.debug("Creating sensor entity description for key: %s", key)

    # Determine component for device grouping based on key patterns
    component = get_entity_component(key, key)

    entity_description = EconetSensorEntityDescription(
        key=key,
        device_class=ENTITY_SENSOR_DEVICE_CLASS_MAP.get(key, None),
        entity_category=ENTITY_CATEGORY.get(key, None),
        translation_key=camel_to_snake(key),
        native_unit_of_measurement=ENTITY_UNIT_MAP.get(key, None),
        state_class=STATE_CLASS_MAP.get(key, SensorStateClass.MEASUREMENT),
        suggested_display_precision=ENTITY_PRECISION.get(key, 0),
        process_val=ENTITY_VALUE_PROCESSOR.get(key, lambda x: x),  # noqa: E731
        component=component,
    )
    _LOGGER.debug(
        "Created sensor entity description: %s (component=%s)",
        entity_description,
        component,
    )
    return entity_description


def create_controller_sensors(
    coordinator: EconetDataCoordinator, api: Econet300Api
) -> list[EconetSensor]:
    """Create controller sensor entities."""
    entities: list[EconetSensor] = []

    # Get the system and regular parameters from the coordinator
    if coordinator.data is None:
        _LOGGER.info("Coordinator data is None, no controller sensors will be created")
        return entities

    data_regParams = coordinator.data.get("regParams", {})
    if data_regParams is None:
        data_regParams = {}

    data_sysParams = coordinator.data.get("sysParams", {})
    if data_sysParams is None:
        data_sysParams = {}

    # Extract the controllerID from sysParams
    controller_id = data_sysParams.get("controllerID")

    # Always use default sensor mapping for all controllers
    sensor_keys = SENSOR_MAP_KEY["_default"].copy()
    if controller_id and controller_id in SENSOR_MAP_KEY:
        _LOGGER.info(
            "ControllerID '%s' found in mapping, but using default sensor mapping",
            controller_id,
        )
    else:
        _LOGGER.info(
            "ControllerID '%s' not found in mapping, using default sensor mapping",
            controller_id if controller_id else "None",
        )

    # Always filter out ecoSTER sensors from controller sensors since they are created as separate devices
    ecoSTER_sensors = SENSOR_MAP_KEY.get("ecoSter", set())
    sensor_keys = sensor_keys - ecoSTER_sensors
    _LOGGER.info(
        "Filtered out ecoSTER sensors from controller sensors: %s", ecoSTER_sensors
    )

    # Iterate through the selected keys and create sensors if valid data is found
    for data_key in sensor_keys:
        _LOGGER.debug(
            "Processing entity sensor data_key: %s from regParams & sysParams", data_key
        )
        if data_key in data_regParams:
            # Check if the value is not null before creating the sensor
            if data_regParams.get(data_key) is None:
                _LOGGER.info(
                    "%s in regParams is null, sensor will not be created.", data_key
                )
                continue
            entity = EconetSensor(
                create_sensor_entity_description(data_key), coordinator, api
            )
            entities.append(entity)
            _LOGGER.debug(
                "Created and appended sensor entity from regParams: %s", entity
            )
        elif data_key in data_sysParams:
            if data_sysParams.get(data_key) is None:
                _LOGGER.info(
                    "%s in sysParams sensor value is null, sensor will not be created.",
                    data_key,
                )
                continue
            entity = EconetSensor(
                create_sensor_entity_description(data_key), coordinator, api
            )
            entities.append(entity)
            _LOGGER.debug(
                "Created and appended sensor entity from sysParams: %s", entity
            )
        else:
            _LOGGER.debug(
                "Key: %s is not mapped in regParams or sysParams, sensor entity will not be added.",
                data_key,
            )
    _LOGGER.info("Total sensor entities created: %d", len(entities))
    return entities


def can_add_mixer(key: str, coordinator: EconetDataCoordinator) -> bool:
    """Check if a mixer can be added."""
    if coordinator.data is None:
        return False

    reg_params = coordinator.data.get("regParams")
    if reg_params is None:
        reg_params = {}

    _LOGGER.debug(
        "Checking if mixer can be added for key: %s, data %s",
        key,
        reg_params,
    )
    return coordinator.has_reg_data(key) and reg_params.get(key) is not None


def create_mixer_sensor_entity_description(key: str) -> EconetSensorEntityDescription:
    """Create a sensor entity description for a mixer."""
    _LOGGER.debug("Creating Mixer entity sensor description for key: %s", key)
    entity_description = EconetSensorEntityDescription(
        key=key,
        translation_key=camel_to_snake(key),
        native_unit_of_measurement=ENTITY_UNIT_MAP.get(key, None),
        state_class=STATE_CLASS_MAP.get(key, SensorStateClass.MEASUREMENT),
        device_class=ENTITY_SENSOR_DEVICE_CLASS_MAP.get(key, None),
        suggested_display_precision=ENTITY_PRECISION.get(key, 0),
        process_val=ENTITY_VALUE_PROCESSOR.get(key, lambda x: x),  # noqa: E731
    )
    _LOGGER.debug("Created Mixer entity description: %s", entity_description)
    return entity_description


def create_mixer_sensors(
    coordinator: EconetDataCoordinator, api: Econet300Api
) -> list[MixerSensor]:
    """Create individual sensor descriptions for mixer sensors."""
    entities: list[MixerSensor] = []

    if coordinator.data is None:
        _LOGGER.info("Coordinator data is None, no mixer sensors will be created")
        return entities

    reg_params = coordinator.data.get("regParams")
    if reg_params is None:
        reg_params = {}

    for key, mixer_keys in SENSOR_MIXER_KEY.items():
        # Check if all required mixer keys have valid (non-null) values
        if any(reg_params.get(mixer_key) is None for mixer_key in mixer_keys):
            _LOGGER.info("Mixer: %s will not be created due to invalid data.", key)
            continue

        # Create sensors for this mixer
        for mixer_key in mixer_keys:
            mixer_sensor_entity = create_mixer_sensor_entity_description(mixer_key)
            entities.append(MixerSensor(mixer_sensor_entity, coordinator, api, key))
            _LOGGER.debug("Added Mixer: %s, Sensor: %s", key, mixer_key)

    return entities


# Create Lambda sensor entity description and Lambda sensor


def create_lambda_sensor_entity_description(key: str) -> EconetSensorEntityDescription:
    """Create a sensor entity description for a Lambda."""
    _LOGGER.debug("Creating Lambda entity sensor description for key: %s", key)
    entity_description = EconetSensorEntityDescription(
        key=key,
        translation_key=camel_to_snake(key),
        native_unit_of_measurement=ENTITY_UNIT_MAP.get(key, None),
        state_class=STATE_CLASS_MAP.get(key, None),
        device_class=ENTITY_SENSOR_DEVICE_CLASS_MAP.get(key, None),
        suggested_display_precision=ENTITY_PRECISION.get(key, 0),
        process_val=ENTITY_VALUE_PROCESSOR.get(key, lambda x: x / 10),  # noqa: E731
    )
    _LOGGER.debug("Created LambdaSensors entity description: %s", entity_description)
    return entity_description


def create_lambda_sensors(coordinator: EconetDataCoordinator, api: Econet300Api):
    """Create controller sensor entities."""
    entities: list[LambdaSensors] = []
    if coordinator.data is None:
        _LOGGER.info("Coordinator data is None, no lambda sensors will be created")
        return entities

    sys_params = coordinator.data.get("sysParams", {})
    if sys_params is None:
        sys_params = {}

    # Check if moduleLambdaSoftVer is None
    if sys_params.get("moduleLambdaSoftVer") is None:
        _LOGGER.info("moduleLambdaSoftVer is None, no lambda sensors will be created")
        return entities

    coordinator_data = coordinator.data.get("regParams", {})
    if coordinator_data is None:
        coordinator_data = {}

    for data_key in SENSOR_MAP_KEY[COMPONENT_LAMBDA]:
        if data_key in coordinator_data:
            entities.append(
                LambdaSensors(
                    create_lambda_sensor_entity_description(data_key), coordinator, api
                )
            )
            _LOGGER.debug(
                "Key: %s mapped, lamda sensor entity will be added",
                data_key,
            )
            continue
        _LOGGER.debug(
            "Key: %s is not mapped, lamda sensor entity will not be added",
            data_key,
        )

    return entities


def create_ecoster_sensor_entity_description(key: str) -> EconetSensorEntityDescription:
    """Create a sensor entity description for an ecoSTER sensor."""
    _LOGGER.debug("Creating ecoSTER entity sensor description for key: %s", key)
    entity_description = EconetSensorEntityDescription(
        key=key,
        translation_key=camel_to_snake(key),
        native_unit_of_measurement=ENTITY_UNIT_MAP.get(key, None),
        state_class=STATE_CLASS_MAP.get(key, SensorStateClass.MEASUREMENT),
        device_class=ENTITY_SENSOR_DEVICE_CLASS_MAP.get(key, None),
        suggested_display_precision=ENTITY_PRECISION.get(key, 0),
        process_val=ENTITY_VALUE_PROCESSOR.get(key, lambda x: x),  # noqa: E731
    )
    _LOGGER.debug("Created ecoSTER entity description: %s", entity_description)
    return entity_description


def create_ecoster_sensors(coordinator: EconetDataCoordinator, api: Econet300Api):
    """Create ecoSTER sensor entities."""
    entities: list[EcoSterSensor] = []
    if coordinator.data is None:
        _LOGGER.info("Coordinator data is None, no ecoSTER sensors will be created")
        return entities

    sys_params = coordinator.data.get("sysParams", {})
    if sys_params is None:
        sys_params = {}

    # Check if moduleEcoSTERSoftVer is None
    if sys_params.get("moduleEcoSTERSoftVer") is None:
        _LOGGER.info("moduleEcoSTERSoftVer is None, no ecoSTER sensors will be created")
        return entities

    coordinator_data = coordinator.data.get("regParams", {})
    if coordinator_data is None:
        coordinator_data = {}

    # Create ecoSTER sensors for each thermostat (1-8)
    for thermostat_idx in range(1, 9):  # 1-8
        # Create temperature sensor
        temp_key = f"ecoSterTemp{thermostat_idx}"
        if temp_key in coordinator_data and coordinator_data.get(temp_key) is not None:
            entities.append(
                EcoSterSensor(
                    create_ecoster_sensor_entity_description(temp_key),
                    coordinator,
                    api,
                    thermostat_idx,
                )
            )
            _LOGGER.debug("Created ecoSTER temperature sensor: %s", temp_key)

        # Create setpoint sensor
        set_temp_key = f"ecoSterSetTemp{thermostat_idx}"
        if (
            set_temp_key in coordinator_data
            and coordinator_data.get(set_temp_key) is not None
        ):
            entities.append(
                EcoSterSensor(
                    create_ecoster_sensor_entity_description(set_temp_key),
                    coordinator,
                    api,
                    thermostat_idx,
                )
            )
            _LOGGER.debug("Created ecoSTER setpoint sensor: %s", set_temp_key)

        # Create mode sensor
        mode_key = f"ecoSterMode{thermostat_idx}"
        if mode_key in coordinator_data and coordinator_data.get(mode_key) is not None:
            entities.append(
                EcoSterSensor(
                    create_ecoster_sensor_entity_description(mode_key),
                    coordinator,
                    api,
                    thermostat_idx,
                )
            )
            _LOGGER.debug("Created ecoSTER mode sensor: %s", mode_key)

    _LOGGER.info("Created %d ecoSTER sensors", len(entities))
    return entities


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up the sensor platform."""

    def gather_entities(
        coordinator: EconetDataCoordinator, api: Econet300Api
    ) -> list[SensorEntity]:
        """Collect all sensor entities."""
        entities: list[SensorEntity] = []
        _LOGGER.info("Starting entity collection for sensors...")

        # Gather sensors dynamically based on the controller
        controller_sensors = create_controller_sensors(coordinator, api)
        _LOGGER.info("Collected %d controller sensors", len(controller_sensors))
        entities.extend(controller_sensors)

        # Gather mixer sensors
        mixer_sensors = create_mixer_sensors(coordinator, api)
        _LOGGER.info("Collected %d mixer sensors", len(mixer_sensors))
        entities.extend(mixer_sensors)

        # Gather lambda sensors
        lambda_sensors = create_lambda_sensors(coordinator, api)
        _LOGGER.info("Collected %d lambda sensors", len(lambda_sensors))
        entities.extend(lambda_sensors)

        # Gather ecoSTER sensors
        ecoster_sensors = create_ecoster_sensors(coordinator, api)
        _LOGGER.info("Collected %d ecoSTER sensors", len(ecoster_sensors))
        entities.extend(ecoster_sensors)

        _LOGGER.info("Total entities collected: %d", len(entities))
        return entities

    coordinator = hass.data[DOMAIN][entry.entry_id][SERVICE_COORDINATOR]
    api = hass.data[DOMAIN][entry.entry_id][SERVICE_API]

    # Collect entities synchronously
    entities = await hass.async_add_executor_job(gather_entities, coordinator, api)

    # Create fuel consumption total sensor if fuelStream is available
    if (
        coordinator.data
        and coordinator.data.get("regParams", {}).get("fuelStream") is not None
    ):
        # Get or create the fuel tracker
        if SERVICE_FUEL_TRACKER not in hass.data[DOMAIN][entry.entry_id]:
            hass.data[DOMAIN][entry.entry_id][SERVICE_FUEL_TRACKER] = (
                FuelConsumptionTracker()
            )
            _LOGGER.info("Created new FuelConsumptionTracker")

        tracker = hass.data[DOMAIN][entry.entry_id][SERVICE_FUEL_TRACKER]
        fuel_consumption_sensor = FuelConsumptionTotalSensor(coordinator, api, tracker)
        entities.append(fuel_consumption_sensor)
        _LOGGER.info("Created FuelConsumptionTotalSensor")
    else:
        _LOGGER.info(
            "fuelStream not available, FuelConsumptionTotalSensor will not be created"
        )

    # Add entities to Home Assistant
    async_add_entities(entities)
    _LOGGER.info("Entities successfully added to Home Assistant")
    return True
