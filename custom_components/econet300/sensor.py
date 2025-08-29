"""Sensor for Econet300."""

from collections.abc import Callable
from dataclasses import dataclass
import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import Econet300Api
from .common import EconetDataCoordinator
from .common_functions import camel_to_snake
from .const import (
    DOMAIN,
    ENTITY_CATEGORY,
    ENTITY_PRECISION,
    ENTITY_SENSOR_DEVICE_CLASS_MAP,
    ENTITY_UNIT_MAP,
    ENTITY_VALUE_PROCESSOR,
    SENSOR_MAP_KEY,
    SENSOR_MIXER_KEY,
    SERVICE_API,
    SERVICE_COORDINATOR,
    STATE_CLASS_MAP,
)
from .entity import EconetEntity, EcoSterEntity, LambdaEntity, MixerEntity

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class EconetSensorEntityDescription(SensorEntityDescription):
    """Describes ecoNET sensor entity."""

    process_val: Callable[[Any], Any] = lambda x: x  # noqa: E731


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
        super().__init__(coordinator, api)

    def _sync_state(self, value) -> None:
        """Synchronize the state of the sensor entity."""
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


def create_sensor_entity_description(key: str) -> EconetSensorEntityDescription:
    """Create ecoNET300 sensor entity based on supplied key."""
    _LOGGER.debug("Creating sensor entity description for key: %s", key)
    entity_description = EconetSensorEntityDescription(
        key=key,
        device_class=ENTITY_SENSOR_DEVICE_CLASS_MAP.get(key, None),
        entity_category=ENTITY_CATEGORY.get(key, None),
        translation_key=camel_to_snake(key),
        native_unit_of_measurement=ENTITY_UNIT_MAP.get(key, None),
        state_class=STATE_CLASS_MAP.get(key, SensorStateClass.MEASUREMENT),
        suggested_display_precision=ENTITY_PRECISION.get(key, 0),
        process_val=ENTITY_VALUE_PROCESSOR.get(key, lambda x: x),  # noqa: E731
    )
    _LOGGER.debug("Created sensor entity description: %s", entity_description)
    return entity_description


def create_controller_sensors(
    coordinator: EconetDataCoordinator, api: Econet300Api
) -> list[EconetSensor]:
    """Create controller sensor entities."""
    entities: list[EconetSensor] = []

    # Get the system and regular parameters from the coordinator
    data_regParams = coordinator.data.get("regParams", {})
    data_sysParams = coordinator.data.get("sysParams", {})

    # Extract the controllerID from sysParams
    controller_id = data_sysParams.get("controllerID", None)

    # Determine the keys to use based on the controllerID
    sensor_keys = SENSOR_MAP_KEY.get(controller_id, SENSOR_MAP_KEY["_default"])
    _LOGGER.info(
        "Using sensor keys for controllerID '%s': %s",
        controller_id if controller_id else "None (default)",
        sensor_keys,
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
    _LOGGER.debug(
        "Checking if mixer can be added for key: %s, data %s",
        key,
        coordinator.data.get("regParams", {}),
    )
    return (
        coordinator.has_reg_data(key)
        and coordinator.data.get("regParams", {}).get(key) is not None
    )


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

    for key, mixer_keys in SENSOR_MIXER_KEY.items():
        # Check if all required mixer keys have valid (non-null) values
        if any(
            coordinator.data.get("regParams", {}).get(mixer_key) is None
            for mixer_key in mixer_keys
        ):
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
    sys_params = coordinator.data.get("sysParams", {})

    # Check if moduleLambdaSoftVer is None
    if sys_params.get("moduleLambdaSoftVer") is None:
        _LOGGER.info("moduleLambdaSoftVer is None, no lambda sensors will be created")
        return entities

    coordinator_data = coordinator.data.get("regParams", {})

    for data_key in SENSOR_MAP_KEY["lambda"]:
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
    sys_params = coordinator.data.get("sysParams", {})

    # Check if moduleEcoSTERSoftVer is None
    if sys_params.get("moduleEcoSTERSoftVer") is None:
        _LOGGER.info("moduleEcoSTERSoftVer is None, no ecoSTER sensors will be created")
        return entities

    coordinator_data = coordinator.data.get("regParams", {})

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
    ) -> list[EconetSensor]:
        """Collect all sensor entities."""
        entities = []
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

    # Add entities to Home Assistant
    async_add_entities(entities)
    _LOGGER.info("Entities successfully added to Home Assistant")
    return True
