"""Sensor for Econet300."""

from collections.abc import Callable
from dataclasses import dataclass
import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .common import Econet300Api, EconetDataCoordinator
from .common_functions import camel_to_snake
from .const import (
    AVAILABLE_NUMBER_OF_MIXERS,
    DOMAIN,
    ENTITY_CATEGORY,
    ENTITY_ICON,
    ENTITY_PRECISION,
    ENTITY_SENSOR_DEVICE_CLASS_MAP,
    ENTITY_UNIT_MAP,
    ENTITY_VALUE_PROCESSOR,
    MIXER_MAP,
    SENSOR_MAP_KEY,
    SERVICE_API,
    SERVICE_COORDINATOR,
    STATE_CLASS_MAP,
)
from .entity import EconetEntity, MixerEntity

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class EconetSensorEntityDescription(SensorEntityDescription):
    """Describes Econet sensor entity."""

    process_val: Callable[[Any], Any] = lambda x: x


class EconetSensor(EconetEntity, SensorEntity):
    """Econet Sensor."""

    entity_description: EconetSensorEntityDescription

    def __init__(
        self,
        entity_description: EconetSensorEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
    ):
        """Initialize a new ecoNET sensor."""
        self.entity_description = entity_description
        self.api = api
        self._attr_native_value = None
        super().__init__(coordinator)
        _LOGGER.debug(
            "EconetSensor initialized with unique_id: %s, entity_description: %s",
            self.unique_id,
            self.entity_description,
        )

    @property
    def state(self):
        """Return the state of the sensor."""
        value = self.coordinator.data["regParams"].get(self.entity_description.key)
        _LOGGER.debug("Sensor state for %s: %s", self.entity_description.key, value)
        return value

    def _sync_state(self, value):
        """Sync state."""
        _LOGGER.debug("Update EconetSensor entity: %s", self.entity_description.name)
        self._attr_native_value = self.entity_description.process_val(value)
        self.async_write_ha_state()


class MixerSensor(MixerEntity, EconetSensor):
    """Mixer sensor class."""

    def __init__(
        self,
        description: EconetSensorEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
        idx: int,
    ):
        """Initialize a new instance of the EconetSensor class."""
        super().__init__(description, coordinator, api, idx)


def create_entity_description(key: str) -> EconetSensorEntityDescription:
    """Create Econet300 sensor entity based on supplied key."""
    _LOGGER.debug("Creating entity description for key: %s", key)
    entity_description = EconetSensorEntityDescription(
        key=key,
        device_class=ENTITY_SENSOR_DEVICE_CLASS_MAP.get(key, None),
        entity_category=ENTITY_CATEGORY.get(key, None),
        translation_key=camel_to_snake(key),
        icon=ENTITY_ICON.get(key, None),
        native_unit_of_measurement=ENTITY_UNIT_MAP.get(key, None),
        state_class=STATE_CLASS_MAP.get(key, None),
        suggested_display_precision=ENTITY_PRECISION.get(key, None),
        process_val=ENTITY_VALUE_PROCESSOR.get(key, lambda x: x),
    )
    _LOGGER.debug("Created entity description: %s", entity_description)
    return entity_description


def create_controller_sensors(coordinator: EconetDataCoordinator, api: Econet300Api):
    """Create controller sensor entities."""
    entities: list[EconetSensor] = []
    coordinator_data = coordinator.data["regParams"]
    for data_key in SENSOR_MAP_KEY["_default"]:
        if data_key in coordinator_data:
            entities.append(
                EconetSensor(create_entity_description(data_key), coordinator, api)
            )
            _LOGGER.debug(
                "Key: %s mapped, sensor entity will be added",
                data_key,
            )
            continue
        _LOGGER.warning(
            "Key: %s is not mapped, sensor entity will not be added",
            data_key,
        )

    return entities


def can_add_mixer(key: str, coordinator: EconetDataCoordinator):
    """Check if a mixer can be added."""
    _LOGGER.debug(
        "Checking if mixer can be added for key: %s, data %s",
        key,
        coordinator.data["regParams"],
    )
    return (
        coordinator.has_sys_data(key) and coordinator.data["regParams"][key] is not None
    )


def create_mixer_sensor_entity_description(
    key: str, map_key: str
) -> EconetSensorEntityDescription:
    """Create Econet300 mixer sensor entity based on supplied key."""
    _LOGGER.debug(
        "Creating Mixer entity sensor description for key: %s, and type : %s",
        key,
        map_key,
    )
    entity_description = EconetSensorEntityDescription(
        key=key,
        translation_key=camel_to_snake(map_key),
        icon=ENTITY_ICON.get(map_key, None),
        native_unit_of_measurement=ENTITY_UNIT_MAP.get(map_key, None),
        state_class=STATE_CLASS_MAP.get(map_key, None),
        device_class=ENTITY_SENSOR_DEVICE_CLASS_MAP.get(map_key, None),
        suggested_display_precision=ENTITY_PRECISION.get(map_key, 0),
        process_val=ENTITY_VALUE_PROCESSOR.get(map_key, lambda x: x),
    )
    _LOGGER.debug("Created Mixer entity description: %s", entity_description)
    return entity_description


def create_mixer_sensors(coordinator: EconetDataCoordinator, api: Econet300Api):
    """Create individual sensor descriptions for mixer sensors."""
    entities: list[MixerSensor] = []

    for i in range(1, AVAILABLE_NUMBER_OF_MIXERS + 1):
        string_mix = str(i)
        mixer_map_value = MIXER_MAP.get(string_mix)
        if mixer_map_value is not None:
            for key, value in mixer_map_value.items():
                if can_add_mixer(key, coordinator):
                    mixer_sensor_entity = create_mixer_sensor_entity_description(
                        key, value
                    )
                    entities.append(
                        MixerSensor(mixer_sensor_entity, coordinator, api, i)
                    )
                else:
                    _LOGGER.warning(
                        "Mixer: %s , Sensor: %s %s wont be added", i, key, value
                    )
        else:
            _LOGGER.debug(
                "Mixer: %s not defined in const, wont be added",
                i,
            )

    return entities


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id][SERVICE_COORDINATOR]
    api = hass.data[DOMAIN][entry.entry_id][SERVICE_API]

    entities: list[EconetSensor] = []
    entities.extend(create_controller_sensors(coordinator, api))
    entities.extend(create_mixer_sensors(coordinator, api))

    return async_add_entities(entities)
