"""Base entity number for Econet300."""

from dataclasses import dataclass
import logging

from homeassistant.components.number import NumberEntity, NumberEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import Limits
from .common import Econet300Api, EconetDataCoordinator, should_skip_params_edits
from .common_functions import camel_to_snake
from .const import (
    DOMAIN,
    ENTITY_ICON,
    ENTITY_MAX_VALUE,
    ENTITY_MIN_VALUE,
    ENTITY_NUMBER_SENSOR_DEVICE_CLASS_MAP,
    ENTITY_STEP,
    ENTITY_UNIT_MAP,
    NUMBER_MAP,
    SERVICE_API,
    SERVICE_COORDINATOR,
)
from .entity import EconetEntity

_LOGGER = logging.getLogger(__name__)


@dataclass(kw_only=True)
class EconetNumberEntityDescription(NumberEntityDescription):
    """Describes ecoNET number entity."""


class EconetNumber(EconetEntity, NumberEntity):
    """Describes ecoNET number sensor entity."""

    entity_description: EconetNumberEntityDescription

    def __init__(
        self,
        entity_description: EconetNumberEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
    ):
        """Initialize a new ecoNET number entity."""
        self.entity_description = entity_description
        self.api = api
        super().__init__(coordinator)

    def _sync_state(self, value):
        """Sync the state of the ecoNET number entity."""
        _LOGGER.debug("ecoNETNumber _sync_state: %s", value)
        self._attr_native_value = value.get("value")
        map_key = NUMBER_MAP.get(self.entity_description.key)

        if map_key:
            self._set_value_limits(value)
        else:
            _LOGGER.error(
                "ecoNETNumber _sync_state: map_key %s not found in NUMBER_MAP",
                self.entity_description.key,
            )
        # Ensure the state is updated in Home Assistant.
        self.async_write_ha_state()
        # Create an asynchronous task for setting the limits.
        self.hass.async_create_task(self.async_set_limits_values())

    def _set_value_limits(self, value):
        """Set native min and max values for the entity."""
        self._attr_native_min_value = value.get("min")
        self._attr_native_max_value = value.get("max")
        _LOGGER.debug(
            "ecoNETNumber _set_value_limits: min=%s, max=%s",
            self._attr_native_min_value,
            self._attr_native_max_value,
        )

    async def async_set_limits_values(self):
        """Async Sync number limits."""
        number_limits = await self.api.get_param_limits(self.entity_description.key)
        _LOGGER.debug("Number limits retrieved: %s", number_limits)

        if not number_limits:
            _LOGGER.warning(
                "Cannot add number entity: %s, numeric limits for this entity is None",
                self.entity_description.key,
            )
            return

        # Directly set min and max values based on fetched limits.
        self._attr_native_min_value = number_limits.min
        self._attr_native_max_value = number_limits.max
        _LOGGER.debug("Apply number limits: %s", self)
        self.async_write_ha_state()

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        _LOGGER.debug("Set value: %s", value)

        # Skip processing if the value is unchanged.
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


def can_add(key: str, coordinator: EconetDataCoordinator) -> bool:
    """Check if a given entity can be added based on the availability of data in the coordinator."""
    try:
        return (
            coordinator.has_param_edit_data(key)
            and coordinator.data["paramsEdits"][key]
        )
    except KeyError as e:
        _LOGGER.error("KeyError in can_add_number_entity: %s", e)
        return False


def apply_limits(desc: EconetNumberEntityDescription, limits: Limits) -> None:
    """Set the native minimum and maximum values for the given entity description."""
    desc.native_min_value = limits.min
    desc.native_max_value = limits.max
    _LOGGER.debug("Apply limits: %s", desc)


def create_number_entity_description(key: str) -> EconetNumberEntityDescription:
    """Create ecoNET300 number entity description."""
    map_key = NUMBER_MAP.get(str(key), str(key))
    _LOGGER.debug("Creating number entity for key: %s", map_key)
    return EconetNumberEntityDescription(
        key=key,
        translation_key=camel_to_snake(map_key),
        icon=ENTITY_ICON.get(map_key),
        device_class=ENTITY_NUMBER_SENSOR_DEVICE_CLASS_MAP.get(map_key),
        native_unit_of_measurement=ENTITY_UNIT_MAP.get(map_key),
        min_value=ENTITY_MIN_VALUE.get(map_key),
        max_value=ENTITY_MAX_VALUE.get(map_key),
        native_step=ENTITY_STEP.get(map_key, 1),
    )


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""

    coordinator = hass.data[DOMAIN][entry.entry_id][SERVICE_COORDINATOR]
    api = hass.data[DOMAIN][entry.entry_id][SERVICE_API]

    # Check the controller type before proceeding
    controller_id = coordinator.data.get("sysParams", {}).get("controllerID", "")
    if controller_id == "ecoMAX360i":
        _LOGGER.info(
            "Controller '%s' detected - skipping setup of number entities.",
            controller_id,
        )
        return

    entities: list[EconetNumber] = []

    for key in NUMBER_MAP:
        sys_params = coordinator.data.get("sysParams", {})
        if should_skip_params_edits(sys_params):
            _LOGGER.info("Skipping number entity setup for controllerID: ecoMAX360i")
            continue

        number_limits = await api.get_param_limits(key)
        if number_limits is None:
            _LOGGER.warning(
                "Cannot add number entity: %s, numeric limits for this entity is None",
                key,
            )
            continue

        if can_add_number_entity(key, coordinator):
            entity_description = create_number_entity_description(key)
            apply_limits(entity_description, number_limits)
            entities.append(EconetNumber(entity_description, coordinator, api))
        else:
            _LOGGER.warning(
                "Cannot add number entity - availability key: %s does not exist",
                key,
            )

    return async_add_entities(entities)
