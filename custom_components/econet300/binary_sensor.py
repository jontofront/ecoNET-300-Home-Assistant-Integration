"""Econet binary sensor."""

from dataclasses import dataclass
import logging

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .common import Econet300Api, EconetDataCoordinator
from .common_functions import camel_to_snake
from .const import (
    BINARY_SENSOR_MAP_KEY,
    DOMAIN,
    ENTITY_BINARY_DEVICE_CLASS_MAP,
    ENTITY_ICON,
    ENTITY_ICON_OFF,
    MIXER_PUMP_BINARY_SENSOR_KEYS,
    SERVICE_API,
    SERVICE_COORDINATOR,
)
from .entity import EconetEntity, MixerEntity

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class EconetBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describes Econet binary sensor entity."""

    icon_off: str | None = None
    availability_key: str = ""


class EconetBinarySensor(EconetEntity, BinarySensorEntity):
    """Econet Binary Sensor."""

    entity_description: EconetBinarySensorEntityDescription

    def __init__(
        self,
        entity_description: EconetBinarySensorEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
    ):
        """Initialize a new ecoNET binary sensor."""
        self.entity_description = entity_description
        self.api = api
        self._attr_is_on = None
        super().__init__(coordinator)
        _LOGGER.debug(
            "EconetBinarySensor initialized with unique_id: %s, entity_description: %s",
            self.unique_id,
            self.entity_description,
        )

    def _sync_state(self, value: bool):
        """Sync state."""
        value = bool(value)
        _LOGGER.debug("EconetBinarySensor _sync_state: %s", value)
        self._attr_is_on = value
        _LOGGER.debug(
            "Updated EconetBinarySensor _attr_is_on for %s: %s",
            self.entity_description.key,
            self._attr_is_on,
        )
        self.async_write_ha_state()

    @property
    def icon(self) -> str | None:
        """Return the icon to use in the frontend."""
        return (
            self.entity_description.icon_off
            if self.entity_description.icon_off is not None and not self.is_on
            else self.entity_description.icon
        )


class MixerBinarySensor(MixerEntity, BinarySensorEntity):
    """Mixer Binary Sensor."""

    entity_description: EconetBinarySensorEntityDescription

    def __init__(
        self,
        entity_description: EconetBinarySensorEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
        idx: int,
    ):
        """Initialize a new mixer binary sensor."""
        super().__init__(entity_description, coordinator, api, idx)
        self._attr_is_on = None
        _LOGGER.debug(
            "MixerBinarySensor initialized with unique_id: %s, entity_description: %s",
            self.unique_id,
            self.entity_description,
        )

    def _sync_state(self, value: bool):
        """Sync state."""
        value = bool(value)
        _LOGGER.debug("MixerBinarySensor _sync_state: %s", value)
        self._attr_is_on = value
        _LOGGER.debug(
            "Updated MixerBinarySensor _attr_is_on for %s: %s",
            self.entity_description.key,
            self._attr_is_on,
        )
        self.async_write_ha_state()

    @property
    def icon(self) -> str | None:
        """Return the icon to use in the frontend."""
        return (
            self.entity_description.icon_off
            if self.entity_description.icon_off is not None and not self.is_on
            else self.entity_description.icon
        )


def create_binary_entity_description(key: str) -> EconetBinarySensorEntityDescription:
    """Create Econet300 binary entity description."""
    _LOGGER.debug("create_binary_entity_description: %s", key)
    entity_description = EconetBinarySensorEntityDescription(
        key=key,
        translation_key=camel_to_snake(key),
        device_class=ENTITY_BINARY_DEVICE_CLASS_MAP.get(key, None),
        icon=ENTITY_ICON.get(key, None),
        icon_off=ENTITY_ICON_OFF.get(key, None),
    )
    _LOGGER.debug("create_binary_entity_description: %s", entity_description)
    return entity_description


def create_binary_sensors(coordinator: EconetDataCoordinator, api: Econet300Api):
    """Create binary sensors."""
    entities: list[EconetBinarySensor] = []
    data_regParams = coordinator.data.get("regParams") or {}
    data_sysParams = coordinator.data.get("sysParams") or {}

    for data_key in BINARY_SENSOR_MAP_KEY["_default"]:
        _LOGGER.debug(
            "Processing binary sensor data_key: %s from regParams & sysParams", data_key
        )
        if data_key in data_regParams:
            entity = EconetBinarySensor(
                create_binary_entity_description(data_key), coordinator, api
            )
            entities.append(entity)
            _LOGGER.debug("Created and appended entity from regParams: %s", entity)
        elif data_key in data_sysParams:
            entity = EconetBinarySensor(
                create_binary_entity_description(data_key), coordinator, api
            )
            entities.append(entity)
            _LOGGER.debug("Created and appended entity from sysParams: %s", entity)
        else:
            _LOGGER.warning(
                "key: %s is not mapped in regParams, binary sensor entity will not be added",
                data_key,
            )
    _LOGGER.info("Total entities created: %d", len(entities))
    return entities


def create_mixer_binary_sensors(coordinator: EconetDataCoordinator, api: Econet300Api):
    """Create mixer binary sensors."""
    entities: list[MixerBinarySensor] = []
    data_regParams = coordinator.data.get("regParams") or {}

    # Create mixer pump status sensors using the dynamic keys
    for mixer_pump_key in MIXER_PUMP_BINARY_SENSOR_KEYS:
        if mixer_pump_key in data_regParams and data_regParams[mixer_pump_key] is not None:
            # Extract mixer number from key (e.g., "mixerPumpWorks1" -> 1)
            mixer_number = int(mixer_pump_key.replace("mixerPumpWorks", ""))
            entity = MixerBinarySensor(
                create_binary_entity_description(mixer_pump_key), coordinator, api, mixer_number
            )
            entities.append(entity)
            _LOGGER.debug("Created mixer binary sensor: %s", mixer_pump_key)

    _LOGGER.info("Total mixer binary sensor entities created: %d", len(entities))
    return entities


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up the binary sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id][SERVICE_COORDINATOR]
    api = hass.data[DOMAIN][entry.entry_id][SERVICE_API]

    entities: list[EconetBinarySensor | MixerBinarySensor] = []
    entities.extend(create_binary_sensors(coordinator, api))
    entities.extend(create_mixer_binary_sensors(coordinator, api))
    async_add_entities(entities)
    return True
