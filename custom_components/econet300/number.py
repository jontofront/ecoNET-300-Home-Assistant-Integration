"""Base entity number for Econet300."""

from dataclasses import dataclass
import logging

from homeassistant.components.number import NumberEntity, NumberEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import Limits
from .common import Econet300Api, EconetDataCoordinator
from .common_functions import camel_to_snake
from .const import (
    DOMAIN,
    ENTITY_DEVICE_CLASS_MAP,
    ENTITY_ICON,
    ENTITY_MAX_VALUE,
    ENTITY_MIN_VALUE,
    ENTITY_STEP,
    ENTITY_UNIT_MAP,
    ENTITY_VISIBLE,
    NUMBER_MAP,
    SERVICE_API,
    SERVICE_COORDINATOR,
)
from .entity import EconetEntity

_LOGGER = logging.getLogger(__name__)


@dataclass
class EconetNumberEntityDescription(NumberEntityDescription):
    """Describes Econet number entity."""


class EconetNumber(EconetEntity, NumberEntity):
    """Describes Econet binary sensor entity."""

    entity_description: EconetNumberEntityDescription

    def __init__(
        self,
        entity_description: EconetNumberEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
    ):
        """Initialize a new ecoNET number entyti."""
        self.entity_description = entity_description
        self.api = api
        super().__init__(coordinator)
        _LOGGER.debug(
            "EconetNumberEntity initialized with unique_id: %s, entity_description: %s",
            self.unique_id,
            self.entity_description,
        )

    def _sync_state(self, value):
        """Sync state."""
        _LOGGER.debug("EconetNumber _sync_state: %s", value)
        self._attr_native_value = value
        map_key = NUMBER_MAP.get(self.entity_description.key)
        self.async_write_ha_state()
        self.hass.async_create_task(self.async_set_limits_values())
ntity_description.key)
        self._attr_native_min_value = ENTITY_MIN_VALUE.get(map_key)
        self._attr_native_max_value 
    async def async_set_limits_values(self):
        """Async Sync number limits."""
        limits = await self.api.get_param_limits(self.entity_description.key)
        _LOGGER.debug("Number limits retrieved: %s", limits)
        if limits is None:
            _LOGGER.warning(
                "Cannot add number entity: %s, numeric limits for this entity is None",
                self.entity_description.key,
            )
        else:
            self._attr_native_min_value = limits.min
            self._attr_native_max_value = limits.max
            _LOGGER.debug("Apply number limits: %s", self)
            self.async_write_ha_state()

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        _LOGGER.debug("Set value: %s", value)

        if value == self._attr_native_value:
            return

        if value > self._attr_native_max_value:
            _LOGGER.warning(
                "Requested value: '%s' exceeds maximum allowed value: '%s'",
                value,
                self._attr_max_value,
            )

        if value < self._attr_native_min_value:
            _LOGGER.warning(
                "Requested value: '%s' is below allowed value: '%s'",
                value,
                self._attr_min_value,
            )
            return

        if not await self.api.set_param(self.entity_description.key, int(value)):
            _LOGGER.warning("Setting value failed")
            return

        self._attr_native_value = value
        self.async_write_ha_state()


def can_add(key: str, coordinator: EconetDataCoordinator):
    """Check if a given entity can be added based on the availability of data in the coordinator."""
    return coordinator.has_data(key) and coordinator.data[key]


def apply_limits(desc: EconetNumberEntityDescription, limits: Limits):
    """Set the native minimum and maximum values for the given entity description."""
    desc.native_min_value = limits.min
    desc.native_max_value = limits.max
    _LOGGER.debug("Apply limits: %s", desc)


def create_number_entity_description(key: int) -> EconetNumberEntityDescription:
    """Create Econect300 mixer sensor entity based on supplied key."""
    map_key = NUMBER_MAP.get(key, key)
    _LOGGER.debug("Create number: %s", map_key)
    entity_description = EconetNumberEntityDescription(
        key=key,
        translation_key=camel_to_snake(map_key),
        icon=ENTITY_ICON.get(map_key),
        device_class=ENTITY_DEVICE_CLASS_MAP.get(map_key),
        native_unit_of_measurement=ENTITY_UNIT_MAP.get(map_key),
        entity_registry_visible_default=ENTITY_VISIBLE.get(map_key, True),
        min_value=ENTITY_MIN_VALUE.get(map_key),
        max_value=ENTITY_MAX_VALUE.get(map_key),
        native_step=ENTITY_STEP.get(map_key, 1),
    )
    _LOGGER.debug("Created number entity description: %s", entity_description)
    return entity_description


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up the sensor platform."""

    coordinator = hass.data[DOMAIN][entry.entry_id][SERVICE_COORDINATOR]
    api = hass.data[DOMAIN][entry.entry_id][SERVICE_API]

    entities: list[EconetNumber] = []

    for key in NUMBER_MAP:
        number_limits = await api.get_param_limits(key)

        if number_limits is None:
            _LOGGER.warning(
                "Cannot add number entity: %s, numeric limits for this entity is None",
                key,
            )
            continue

        if can_add(key, coordinator):
            entity_description = create_number_entity_description(key)
            apply_limits(entity_description, number_limits)
            entities.append(EconetNumber(entity_description, coordinator, api))
        else:
            _LOGGER.warning(
                "Cannot add number entity - availability key: %s does not exist",
                key,
            )

    return async_add_entities(entities)
