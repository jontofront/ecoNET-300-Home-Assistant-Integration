"""Sensor for Econet300."""

from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from decimal import Decimal, InvalidOperation
import logging
import re
from typing import Any, Final, Self

from homeassistant.components.sensor import (
    RestoreSensor,
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorExtraStoredData,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_UNAVAILABLE, EntityCategory, UnitOfMass
from homeassistant.core import (
    CALLBACK_TYPE,
    Event,
    EventStateChangedData,
    EventStateReportedData,
    HomeAssistant,
    State,
    callback,
)
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import (
    async_call_later,
    async_track_state_change_event,
    async_track_state_report_event,
)

from .api import Econet300Api
from .common import EconetDataCoordinator
from .common_functions import (
    build_current_data_entity_key,
    camel_to_snake,
    classify_current_data_param,
    get_entity_component,
    get_validated_entity_component,
    is_regparams_data_id_mapped,
    mixer_exists,
)
from .const import (
    CDP_DEFAULT_PRECISION,
    CDP_UNIT_PRECISION,
    CDP_UNIT_TO_SENSOR_DEVICE_CLASS,
    COMPONENT_LAMBDA,
    CONF_CUSTOM_ENTITIES,
    DEVICE_CLASS_FUEL_METER,
    DEVICE_INFO_CONTROLLER_NAME,
    DOMAIN,
    ENTITY_CATEGORY,
    ENTITY_PRECISION,
    ENTITY_SENSOR_DEVICE_CLASS_MAP,
    ENTITY_UNIT_MAP,
    ENTITY_VALUE_PROCESSOR,
    FUEL_MAX_SUB_INTERVAL_SECONDS,
    SENSOR_ENUM_OPTIONS,
    SENSOR_MAP_KEY,
    SENSOR_MIXER_KEY,
    SERVICE_API,
    SERVICE_COORDINATOR,
    SERVICE_FUEL_SENSOR,
    STATE_CLASS_MAP,
    UNIT_INDEX_TO_NAME,
    UNIT_NAME_TO_HA_UNIT,
)
from .entity import (
    EconetEntity,
    EcoSterEntity,
    LambdaEntity,
    MixerEntity,
    _create_base_device_info,
    get_device_info_for_component,
)

_LOGGER = logging.getLogger(__name__)

# Unit time divisor: convert seconds to hours for kg/h integration
_UNIT_TIME_HOURS: Final = Decimal(3600)


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


def _decimal_state(state: str | None) -> Decimal | None:
    """Try to parse a state string as Decimal, returning None on failure."""
    try:
        return Decimal(state)  # type: ignore[arg-type]
    except (InvalidOperation, TypeError):
        return None


@dataclass
class FuelConsumptionExtraStoredData(SensorExtraStoredData):
    """Extra stored data for the fuel consumption sensor."""

    source_entity: str | None
    last_valid_state: Decimal | None

    def as_dict(self) -> dict[str, Any]:
        """Return a dict representation of the stored data."""
        data = super().as_dict()
        data["source_entity"] = self.source_entity
        data["last_valid_state"] = (
            str(self.last_valid_state) if self.last_valid_state else None
        )
        return data

    @classmethod
    def from_dict(cls, restored: dict[str, Any]) -> Self | None:
        """Initialize stored data from a dict."""
        extra = SensorExtraStoredData.from_dict(restored)
        if extra is None:
            return None

        source_entity = restored.get("source_entity")

        try:
            last_valid_state = (
                Decimal(str(restored["last_valid_state"]))
                if restored.get("last_valid_state")
                else None
            )
        except (InvalidOperation, TypeError):
            _LOGGER.error("Could not restore last_valid_state")
            return None

        return cls(
            extra.native_value,
            extra.native_unit_of_measurement,
            source_entity,
            last_valid_state,
        )


class _IntegrationTrigger:
    """Track what triggered the last integration."""

    STATE_EVENT = "state_event"
    TIME_ELAPSED = "time_elapsed"


class FuelConsumptionTotalSensor(RestoreSensor):
    """Sensor that tracks total fuel consumption via Riemann sum integration.

    Integrates the fuelStream rate sensor (kg/h) over time using the
    trapezoidal method. Follows HA Core IntegrationSensor patterns.
    Persists across restarts using RestoreSensor.
    Reset and calibration are available via service actions.
    """

    _attr_has_entity_name = True
    _attr_translation_key = "fuel_consumption_total"
    _attr_device_class = DEVICE_CLASS_FUEL_METER  # type: ignore[assignment]
    _attr_native_unit_of_measurement = UnitOfMass.KILOGRAMS
    _attr_state_class = SensorStateClass.TOTAL
    _attr_should_poll = False
    _attr_suggested_display_precision = 2
    _attr_icon = "mdi:weight-kilogram"

    def __init__(
        self,
        hass: HomeAssistant,
        source_entity_id: str,
        api: Econet300Api,
    ) -> None:
        """Initialize the fuel consumption total sensor.

        Args:
            hass: The Home Assistant instance
            source_entity_id: Entity ID of the fuelStream source sensor
            api: The ecoNET API instance

        """
        self.hass = hass
        self._source_entity_id = source_entity_id
        self._api = api
        self._attr_unique_id = f"{api.uid}_fuel_consumption_total"
        self._state: Decimal | None = None
        self._last_valid_state: Decimal | None = None
        self._last_reset_dt: datetime | None = None
        self._last_integration_time: datetime = datetime.now(tz=UTC)
        self._last_integration_trigger = _IntegrationTrigger.STATE_EVENT
        self._max_sub_interval = timedelta(seconds=FUEL_MAX_SUB_INTERVAL_SECONDS)
        self._max_sub_interval_exceeded_callback: CALLBACK_TYPE = lambda *args: None

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info for the main boiler device."""
        return _create_base_device_info(
            api=self._api,
            identifier=self._api.uid,
            name=DEVICE_INFO_CONTROLLER_NAME,
            include_model_id=True,
            include_hw_version=True,
        )

    @property
    def native_value(self) -> Decimal | None:
        """Return the current total fuel consumption."""
        if isinstance(self._state, Decimal):
            return round(self._state, 3)
        return self._state

    @property
    def last_reset(self) -> datetime | None:
        """Return the time of the last meter reset."""
        return self._last_reset_dt

    @property
    def extra_state_attributes(self) -> dict[str, str] | None:
        """Return extra state attributes."""
        return {"source": self._source_entity_id}

    @property
    def extra_restore_state_data(self) -> FuelConsumptionExtraStoredData:
        """Return sensor-specific state data to be restored."""
        return FuelConsumptionExtraStoredData(
            self.native_value,
            self.native_unit_of_measurement,
            self._source_entity_id,
            self._last_valid_state,
        )

    async def async_get_last_sensor_data(
        self,
    ) -> FuelConsumptionExtraStoredData | None:
        """Restore fuel consumption sensor extra stored data."""
        if (restored := await self.async_get_last_extra_data()) is None:
            return None
        return FuelConsumptionExtraStoredData.from_dict(restored.as_dict())

    async def async_reset_meter(self) -> None:
        """Reset the fuel consumption meter to zero."""
        _LOGGER.info("Resetting fuel consumption meter")
        self._state = Decimal(0)
        self._last_valid_state = Decimal(0)
        self._last_reset_dt = datetime.now(tz=UTC)
        self.async_write_ha_state()

    async def async_calibrate_meter(self, value: float) -> None:
        """Calibrate the fuel consumption meter to a specific value."""
        _LOGGER.info("Calibrating fuel consumption meter to %.3f kg", value)
        self._state = Decimal(str(value))
        self._last_valid_state = self._state
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        """Handle entity added to Home Assistant."""
        await super().async_added_to_hass()

        # Restore previous state
        if (last_sensor_data := await self.async_get_last_sensor_data()) is not None:
            self._state = (
                Decimal(str(last_sensor_data.native_value))
                if last_sensor_data.native_value
                else last_sensor_data.last_valid_state
            )
            self._last_valid_state = last_sensor_data.last_valid_state
            _LOGGER.debug(
                "Restored state %s and last_valid_state %s",
                self._state,
                self._last_valid_state,
            )

        # Restore last_reset from state attributes
        last_state = await self.async_get_last_state()
        if last_state and last_state.attributes:
            last_reset_str = last_state.attributes.get("last_reset")
            if last_reset_str:
                try:
                    self._last_reset_dt = datetime.fromisoformat(last_reset_str)
                except (ValueError, TypeError):
                    self._last_reset_dt = None

        # Schedule max_sub_interval check for initial source state
        source_state = self.hass.states.get(self._source_entity_id)
        self._schedule_max_sub_interval_if_numeric(source_state)
        self.async_on_remove(self._cancel_max_sub_interval_callback)

        # Listen to fuelStream sensor state changes
        self.async_on_remove(
            async_track_state_change_event(
                self.hass,
                self._source_entity_id,
                self._on_state_change_event,
            )
        )
        self.async_on_remove(
            async_track_state_report_event(
                self.hass,
                self._source_entity_id,
                self._on_state_report_event,
            )
        )

    # ------------------------------------------------------------------
    # Integration callbacks
    # ------------------------------------------------------------------

    @callback
    def _on_state_change_event(self, event: Event[EventStateChangedData]) -> None:
        """Handle source sensor state change."""
        self._cancel_max_sub_interval_callback()
        try:
            self._integrate(
                old_timestamp=None,
                new_timestamp=None,
                old_state=event.data["old_state"],
                new_state=event.data["new_state"],
            )
            self._last_integration_trigger = _IntegrationTrigger.STATE_EVENT
            self._last_integration_time = datetime.now(tz=UTC)
        finally:
            self._schedule_max_sub_interval_if_numeric(event.data["new_state"])

    @callback
    def _on_state_report_event(self, event: Event[EventStateReportedData]) -> None:
        """Handle source sensor state report (value unchanged but reported)."""
        new_state = event.data["new_state"]
        self._cancel_max_sub_interval_callback()
        try:
            self._integrate(
                old_timestamp=event.data["old_last_reported"],
                new_timestamp=new_state.last_reported if new_state else None,
                old_state=None,
                new_state=new_state,
            )
            self._last_integration_trigger = _IntegrationTrigger.STATE_EVENT
            self._last_integration_time = datetime.now(tz=UTC)
        finally:
            self._schedule_max_sub_interval_if_numeric(new_state)

    def _integrate(
        self,
        old_timestamp: datetime | None,
        new_timestamp: datetime | None,
        old_state: State | None,
        new_state: State | None,
    ) -> None:
        """Perform trapezoidal integration between two states."""
        if new_state is None:
            return

        if new_state.state == STATE_UNAVAILABLE:
            self._attr_available = False
            self.async_write_ha_state()
            return

        self._attr_available = True

        if old_state:
            # State changed - use old_state from event
            new_timestamp = new_state.last_updated
            old_state_str = old_state.state
            old_timestamp = old_state.last_reported
        else:
            # State reported without change
            old_state_str = new_state.state

        if old_timestamp is None and old_state is None:
            # First state, nothing to integrate yet
            self.async_write_ha_state()
            return

        # Validate both states as Decimal
        old_dec = _decimal_state(old_state_str)
        new_dec = _decimal_state(new_state.state)
        if old_dec is None or new_dec is None:
            self.async_write_ha_state()
            return

        if old_timestamp is None or new_timestamp is None:
            self.async_write_ha_state()
            return

        # Calculate elapsed time based on last trigger type
        if self._last_integration_trigger == _IntegrationTrigger.STATE_EVENT:
            elapsed_seconds = Decimal(
                str((new_timestamp - old_timestamp).total_seconds())
            )
        else:
            elapsed_seconds = Decimal(
                str((new_timestamp - self._last_integration_time).total_seconds())
            )

        if elapsed_seconds <= 0:
            return

        # Trapezoidal: (old + new) / 2 * elapsed_hours
        area = (old_dec + new_dec) / 2 * elapsed_seconds / _UNIT_TIME_HOURS

        if isinstance(self._state, Decimal):
            self._state += area
        else:
            self._state = area

        self._last_valid_state = self._state

        _LOGGER.debug(
            "Fuel integration: old=%.3f, new=%.3f, dt=%.1fs, "
            "area=%.6f kg, total=%.3f kg",
            old_dec,
            new_dec,
            elapsed_seconds,
            area,
            self._state,
        )
        self.async_write_ha_state()

    # ------------------------------------------------------------------
    # Max sub-interval: integrate even when source is constant
    # ------------------------------------------------------------------

    def _schedule_max_sub_interval_if_numeric(self, source_state: State | None) -> None:
        """Schedule integration if source stays constant beyond max_sub_interval."""
        if (
            source_state is not None
            and (source_dec := _decimal_state(source_state.state)) is not None
        ):

            @callback
            def _on_max_sub_interval_exceeded(now: datetime) -> None:
                """Integrate assuming constant rate, then reschedule."""
                elapsed_seconds = Decimal(
                    str((now - self._last_integration_time).total_seconds())
                )
                # Constant rate: area = rate * elapsed_hours
                area = source_dec * elapsed_seconds / _UNIT_TIME_HOURS

                if isinstance(self._state, Decimal):
                    self._state += area
                else:
                    self._state = area

                self._last_valid_state = self._state
                self.async_write_ha_state()

                self._last_integration_time = datetime.now(tz=UTC)
                self._last_integration_trigger = _IntegrationTrigger.TIME_ELAPSED

                # Reschedule for another interval
                self._schedule_max_sub_interval_if_numeric(source_state)

            self._max_sub_interval_exceeded_callback = async_call_later(
                self.hass,
                self._max_sub_interval,
                _on_max_sub_interval_exceeded,
            )

    def _cancel_max_sub_interval_callback(self) -> None:
        """Cancel any pending max_sub_interval callback."""
        self._max_sub_interval_exceeded_callback()


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


class CurrentDataSensor(EconetEntity, SensorEntity):
    """Dynamic sensor created from rmCurrentDataParams + regParamsData."""

    entity_description: EconetSensorEntityDescription

    def __init__(
        self,
        entity_description: EconetSensorEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
        param_id: str,
    ):
        """Initialize a CurrentData dynamic sensor."""
        self.entity_description = entity_description
        self.api = api
        self._param_id = param_id
        self._attr_native_value = None
        super().__init__(coordinator, api)

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device info based on entity component."""
        component = getattr(self.entity_description, "component", None)
        if component:
            return get_device_info_for_component(component, self.api)
        return super().device_info

    def _lookup_value(self) -> Any:
        """Look up value from currentDataMerged."""
        if self.coordinator.data is None:
            return None
        cdm = self.coordinator.data.get("currentDataMerged", {})
        entry = cdm.get(self._param_id)
        if entry is None:
            return None
        return entry.get("value")

    def _sync_state(self, value) -> None:
        """Synchronize the sensor state."""
        if value is not None:
            try:
                self._attr_native_value = float(value)
            except (ValueError, TypeError):
                self._attr_native_value = None
        else:
            self._attr_native_value = None
        self.async_write_ha_state()


def _resolve_cdp_device_class(unit_name: str) -> SensorDeviceClass | None:
    """Return a HA SensorDeviceClass for a CDP unit string, or None."""
    dc_str = CDP_UNIT_TO_SENSOR_DEVICE_CLASS.get(unit_name)
    if dc_str is None:
        return None
    try:
        return SensorDeviceClass(dc_str)
    except ValueError:
        return None


def create_current_data_sensors(
    coordinator: EconetDataCoordinator, api: Econet300Api
) -> list[CurrentDataSensor]:
    """Create dynamic sensor entities from currentDataMerged."""
    entities: list[CurrentDataSensor] = []

    if coordinator.data is None:
        return entities

    cdm = coordinator.data.get("currentDataMerged", {})
    if not cdm:
        _LOGGER.debug("No currentDataMerged data, skipping CDP sensors")
        return entities

    for param_id, param in cdm.items():
        if not isinstance(param, dict):
            continue

        # Skip IDs already covered by static entities
        if is_regparams_data_id_mapped(param_id):
            continue

        classification = classify_current_data_param(param)
        if classification != "sensor":
            continue

        name = param.get("name", "").strip()

        # Skip entities for non-existent mixers
        mixer_match = re.search(r"mixer\s*(\d+)", name.lower())
        if mixer_match:
            mixer_num = int(mixer_match.group(1))
            if not mixer_exists(coordinator.data, mixer_num):
                _LOGGER.debug(
                    "Skipping CDP sensor %s - mixer %d not connected",
                    name,
                    mixer_num,
                )
                continue

        entity_key = build_current_data_entity_key(param_id, name)
        component = get_validated_entity_component(
            name, entity_key, coordinator_data=coordinator.data
        )

        unit_idx = param.get("unit", 0)
        unit_name = UNIT_INDEX_TO_NAME.get(unit_idx, "")
        ha_unit = UNIT_NAME_TO_HA_UNIT.get(unit_name) if unit_name else None
        device_class = _resolve_cdp_device_class(unit_name)

        special = param.get("special", 0)
        entity_category = EntityCategory.DIAGNOSTIC if special > 0 else None

        description = EconetSensorEntityDescription(
            key=entity_key,
            name=name,
            native_unit_of_measurement=ha_unit,
            device_class=device_class,
            state_class=SensorStateClass.MEASUREMENT,
            suggested_display_precision=CDP_UNIT_PRECISION.get(
                unit_name, CDP_DEFAULT_PRECISION
            ),
            entity_category=entity_category,
            component=component,
            has_entity_name=True,
        )

        entities.append(CurrentDataSensor(description, coordinator, api, param_id))

    _LOGGER.info("Created %d CDP dynamic sensors", len(entities))
    return entities


# =============================================================================
# Custom regParamsData sensors (user-selected via Options Flow)
# =============================================================================


class CustomRegParamSensor(EconetEntity, SensorEntity):
    """Sensor created from a user-selected raw regParamsData ID."""

    entity_description: EconetSensorEntityDescription

    def __init__(
        self,
        entity_description: EconetSensorEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
        param_id: str,
    ):
        """Initialize a custom regParamsData sensor."""
        self.entity_description = entity_description
        self.api = api
        self._param_id = param_id
        self._attr_native_value = None
        super().__init__(coordinator, api)

    def _lookup_value(self) -> Any:
        """Look up value from regParamsData."""
        if self.coordinator.data is None:
            return None
        rpd = self.coordinator.data.get("regParamsData", {})
        return rpd.get(self._param_id)

    def _sync_state(self, value) -> None:
        """Synchronize the sensor state."""
        if value is not None:
            try:
                self._attr_native_value = float(value)
            except (ValueError, TypeError):
                self._attr_native_value = None
        else:
            self._attr_native_value = None
        self.async_write_ha_state()


def create_custom_regparam_sensors(
    coordinator: EconetDataCoordinator,
    api: Econet300Api,
    custom_entities: dict[str, dict[str, str]],
) -> list[CustomRegParamSensor]:
    """Create sensor entities from user-selected regParamsData IDs.

    Args:
        coordinator: The data coordinator.
        api: The device API.
        custom_entities: Dict from entry.options[CONF_CUSTOM_ENTITIES],
            shaped as {param_id: {"name": str, "entity_type": str}}.

    """
    entities: list[CustomRegParamSensor] = []

    for param_id, cfg in custom_entities.items():
        if cfg.get("entity_type") != "sensor":
            continue

        name = cfg.get("name", f"Parameter {param_id}")
        entity_key = f"custom_{param_id}"

        description = EconetSensorEntityDescription(
            key=entity_key,
            name=name,
            state_class=SensorStateClass.MEASUREMENT,
            entity_category=EntityCategory.DIAGNOSTIC,
            has_entity_name=True,
        )

        entities.append(CustomRegParamSensor(description, coordinator, api, param_id))

    _LOGGER.info("Created %d custom regParamsData sensors", len(entities))
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

        # Gather dynamic CDP sensors (rmCurrentDataParams + regParamsData)
        cdp_sensors = create_current_data_sensors(coordinator, api)
        _LOGGER.info("Collected %d CDP dynamic sensors", len(cdp_sensors))
        entities.extend(cdp_sensors)

        # Gather user-defined custom sensors from Options Flow
        custom_cfg = entry.options.get(CONF_CUSTOM_ENTITIES, {})
        if custom_cfg:
            custom_sensors = create_custom_regparam_sensors(
                coordinator, api, custom_cfg
            )
            _LOGGER.info("Collected %d custom regParam sensors", len(custom_sensors))
            entities.extend(custom_sensors)

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
        # Resolve the fuelStream sensor entity_id from registry
        registry = er.async_get(hass)
        fuel_stream_unique_id = f"{api.uid}_fuelStream"
        source_entity_id = registry.async_get_entity_id(
            "sensor", DOMAIN, fuel_stream_unique_id
        )

        if source_entity_id:
            fuel_sensor = FuelConsumptionTotalSensor(hass, source_entity_id, api)
            entities.append(fuel_sensor)
            # Store reference for service lookups
            hass.data[DOMAIN][entry.entry_id][SERVICE_FUEL_SENSOR] = fuel_sensor
            _LOGGER.info(
                "Created FuelConsumptionTotalSensor (source: %s)", source_entity_id
            )
        else:
            _LOGGER.warning(
                "fuelStream sensor entity not found in registry "
                "(unique_id: %s), FuelConsumptionTotalSensor will not be created",
                fuel_stream_unique_id,
            )
    else:
        _LOGGER.info(
            "fuelStream not available, FuelConsumptionTotalSensor will not be created"
        )

    # Add entities to Home Assistant
    async_add_entities(entities)
    _LOGGER.info("Entities successfully added to Home Assistant")
    return True
