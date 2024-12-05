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
    SENSOR_MAP_KEY,
    SENSOR_MIXER_KEY,
    SERVICE_API,
    SERVICE_COORDINATOR,
    STATE_CLASS_MAP,
)
from .entity import EconetEntity, MixerEntity

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class EconetSensorEntityDescription(SensorEntityDescription):
    """Describes ecoNET sensor entity."""

    process_val: Callable[[Any], Any] = lambda x: x


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
        super().__init__(coordinator)

    def _sync_state(self, value):
        """Synchronize the state of the sensor entity."""
        self._attr_native_value = self.entity_description.process_val(value)
        self.async_write_ha_state()


# TODO: Add MixerSensor check class
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


def create_sensor_entity_description(key: str) -> EconetSensorEntityDescription:
    """Create ecoNET300 sensor entity based on supplied key."""
    _LOGGER.debug("Creating sensor entity description for key: %s", key)
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
    _LOGGER.debug("Created sensor entity description: %s", entity_description)
    return entity_description


def create_controller_sensors(coordinator: EconetDataCoordinator, api: Econet300Api):
    """Create controller sensor entities."""
    entities: list[EconetSensor] = []
    coordinator_data = coordinator.data.get("regParams", {})
    for data_key in SENSOR_MAP_KEY["_default"]:
        if data_key in coordinator_data:
            entities.append(
                EconetSensor(
                    create_sensor_entity_description(data_key), coordinator, api
                )
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
        icon=ENTITY_ICON.get(key, None),
        native_unit_of_measurement=ENTITY_UNIT_MAP.get(key, None),
        state_class=STATE_CLASS_MAP.get(key, None),
        device_class=ENTITY_SENSOR_DEVICE_CLASS_MAP.get(key, None),
        suggested_display_precision=ENTITY_PRECISION.get(key, 0),
        process_val=ENTITY_VALUE_PROCESSOR.get(key, lambda x: x),
    )
    _LOGGER.debug("Created Mixer entity description: %s", entity_description)
    return entity_description


def create_mixer_sensors(
    coordinator: EconetDataCoordinator, api: Econet300Api
) -> list[MixerSensor]:
    """Create individual sensor descriptions for mixer sensors."""
    entities: list[MixerSensor] = []

    for i in range(1, AVAILABLE_NUMBER_OF_MIXERS + 1):
        string_mix = str(i)
        mixer_keys = SENSOR_MIXER_KEY.get(string_mix)

        if not mixer_keys:
            _LOGGER.debug(
                "Maišytuvas: %s nėra apibrėžtas konstantoje, nebus pridėtas.", i
            )
            continue

        # Check if all required mixer keys have valid (non-null) values
        if any(
            coordinator.data.get("regParams", {}).get(key) is None for key in mixer_keys
        ):
            _LOGGER.warning(
                "Maišytuvas: %s nebus sukurtas dėl negaliojančių duomenų.", i
            )
            continue

        # Create sensors for this mixer
        for key in mixer_keys:
            mixer_sensor_entity = create_mixer_sensor_entity_description(key)
            entities.append(MixerSensor(mixer_sensor_entity, coordinator, api, i))
            _LOGGER.debug("Pridėtas maišytuvas: %s, jutiklis: %s", i, key)

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
