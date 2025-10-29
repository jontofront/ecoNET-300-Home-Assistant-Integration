"""Base entity number for Econet300."""

from dataclasses import dataclass
import logging

from homeassistant.components.number import NumberEntity, NumberEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import Limits
from .common import Econet300Api, EconetDataCoordinator, skip_edit_params, skip_params_edits
from .common_functions import camel_to_snake
from .const import (
    DOMAIN,
    ENTITY_MAX_VALUE,
    ENTITY_MIN_VALUE,
    ENTITY_NUMBER_SENSOR_DEVICE_CLASS_MAP,
    ENTITY_STEP,
    ENTITY_UNIT_MAP,
    NUMBER_MAP_KEY,
    SERVICE_API,
    SERVICE_COORDINATOR,
)
from .entity import EconetEntity

_LOGGER = logging.getLogger(__name__)


@dataclass(kw_only=True, frozen=True)
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
        has_params_edits: bool,
        has_edit_params: bool,
    ):
        """Initialize a new ecoNET number entity."""
        self.entity_description = entity_description
        self.api = api
        self.has_params_edits = has_params_edits
        self.has_edit_params = has_edit_params
        super().__init__(coordinator, api)

    def _sync_state(self, value):
        """Sync the state of the ecoNET number entity."""
        _LOGGER.debug("ecoNETNumber _sync_state: %s", value)
        _LOGGER.debug(
            "DEBUG: Value type: %s, Value keys: %s",
            type(value),
            value.keys() if isinstance(value, dict) else "Not a dict",
        )

        # Handle both dict and direct value
        if isinstance(value, dict) and "value" in value:
            self._attr_native_value = value.get("value")
            _LOGGER.debug(
                "DEBUG: Extracted value from dict: %s", self._attr_native_value
            )
        else:
            self._attr_native_value = value
            _LOGGER.debug("DEBUG: Using direct value: %s", self._attr_native_value)

        # Get controller ID to determine which number mappings to use
        sys_params = self.coordinator.data.get("sysParams", {})
        controller_id = sys_params.get("controllerID", "_default")
        number_map = NUMBER_MAP_KEY.get(controller_id, NUMBER_MAP_KEY["_default"])
        map_key = number_map.get(self.entity_description.key)

        if map_key:
            self._set_value_limits(value)
        else:
            _LOGGER.error(
                "ecoNETNumber _sync_state: map_key %s not found in NUMBER_MAP for controller %s",
                self.entity_description.key,
                controller_id,
            )
        # Ensure the state is updated in Home Assistant.
        self.async_write_ha_state()

        # For editParams, limits are in the value dict, no need to fetch separately
        # For paramsEdits, limits might not be in the value, so fetch if needed
        if not self.has_edit_params and self.has_params_edits:
            # Only fetch limits if we don't already have them from the value
            if self._attr_native_min_value is None or self._attr_native_max_value is None:
                self.hass.async_create_task(self.async_set_limits_values())

    def _set_value_limits(self, value):
        """Set native min and max values for the entity."""
        # editParams uses 'minv'/'maxv', paramsEdits uses 'min'/'max'
        if isinstance(value, dict):
            # Check for editParams format first (minv/maxv)
            if "minv" in value:
                self._attr_native_min_value = value["minv"]
            elif "min" in value:
                self._attr_native_min_value = value["min"]

            if "maxv" in value:
                self._attr_native_max_value = value["maxv"]
            elif "max" in value:
                self._attr_native_max_value = value["max"]
        _LOGGER.debug(
            "ecoNETNumber _set_value_limits: min=%s, max=%s",
            self._attr_native_min_value,
            self._attr_native_max_value,
        )

    async def _get_param_limits(self, key: str):
        """Get parameter limits using the appropriate method based on controller type."""
        if self.has_edit_params:
            # Use editParams endpoint (ecoMAX360i)
            _LOGGER.debug("Fetching limits from editParams for key: %s", key)
            return await self.api.get_param_limits_from_edit_params(key)
        elif self.has_params_edits:
            # Use rmCurrentDataParamsEdits endpoint (most controllers)
            _LOGGER.debug("Fetching limits from paramsEdits for key: %s", key)
            return await self.api.get_param_limits(key)
        else:
            _LOGGER.warning("No parameter editing support available for key: %s", key)
            return None

    async def async_set_limits_values(self):
        """Async Sync number limits."""
        number_limits = await self._get_param_limits(self.entity_description.key)
        _LOGGER.debug("Number limits retrieved: %s", number_limits)

        if not number_limits:
            _LOGGER.info(
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

        # Convert to int if the value has no fractional part
        # This ensures parameters that only accept integers (like SummerOn/SummerOff)
        # receive integers, while fractional values (like 0.3 for heat curves) stay as floats
        api_value = int(value) if value == int(value) else value

        if not await self.api.set_param(self.entity_description.key, api_value):
            _LOGGER.warning("Setting value failed")
            return

        self._attr_native_value = value
        self.async_write_ha_state()


def can_add(
    key: str,
    coordinator: EconetDataCoordinator,
    has_params_edits: bool,
    has_edit_params: bool,
) -> bool:
    """Check if a given entity can be added based on the availability of data in the coordinator."""
    try:
        if has_edit_params:
            # For ecoMAX360i: check editParams data
            return (
                coordinator.has_edit_params_data(key)
                and coordinator.data["editParams"][key]
            )
        elif has_params_edits:
            # For most controllers: check paramsEdits data
            return (
                coordinator.has_param_edit_data(key)
                and coordinator.data["paramsEdits"][key]
            )
        else:
            return False
    except KeyError as e:
        _LOGGER.error("KeyError in can_add: %s", e)
        return False


def apply_limits(
    desc: EconetNumberEntityDescription, limits: Limits
) -> EconetNumberEntityDescription:
    """Set the native minimum and maximum values for the given entity description."""
    # Create a new instance with updated limits since the dataclass is frozen
    return EconetNumberEntityDescription(
        key=desc.key,
        translation_key=desc.translation_key,
        device_class=desc.device_class,
        native_unit_of_measurement=desc.native_unit_of_measurement,
        native_min_value=limits.min,
        native_max_value=limits.max,
        native_step=desc.native_step,
    )


def create_number_entity_description(
    key: str, controller_id: str
) -> EconetNumberEntityDescription:
    """Create ecoNET300 number entity description."""
    # Get device-specific number mapping
    number_map = NUMBER_MAP_KEY.get(controller_id, NUMBER_MAP_KEY["_default"])
    map_key = number_map.get(str(key), str(key))
    _LOGGER.debug(
        "Creating number entity for key: %s (controller: %s)", map_key, controller_id
    )
    return EconetNumberEntityDescription(
        key=key,
        translation_key=camel_to_snake(map_key),
        device_class=ENTITY_NUMBER_SENSOR_DEVICE_CLASS_MAP.get(map_key),
        native_unit_of_measurement=ENTITY_UNIT_MAP.get(map_key),
        native_min_value=ENTITY_MIN_VALUE.get(map_key) or 0,
        native_max_value=ENTITY_MAX_VALUE.get(map_key) or 100,
        native_step=ENTITY_STEP.get(map_key, 1),
    )


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the number platform."""

    coordinator = hass.data[DOMAIN][entry.entry_id][SERVICE_COORDINATOR]
    api = hass.data[DOMAIN][entry.entry_id][SERVICE_API]

    entities: list[EconetNumber] = []

    # Get controller ID to determine which number mappings to use
    sys_params = coordinator.data.get("sysParams", {})
    controller_id = sys_params.get("controllerID", "_default")

    # Get device-specific number mapping
    number_map = NUMBER_MAP_KEY.get(controller_id, NUMBER_MAP_KEY["_default"])
    _LOGGER.info("Using number mapping for controller: %s", controller_id)

    # Check if this controller supports parameter editing at all
    # paramsEdits (rmCurrentDataParamsEdits endpoint) OR editParams (editParams endpoint)
    has_params_edits = not skip_params_edits(sys_params)
    has_edit_params = not skip_edit_params(sys_params)

    if not has_params_edits and not has_edit_params:
        _LOGGER.info(
            "Skipping number entity setup for controllerID: %s (neither paramsEdits nor editParams supported)",
            controller_id,
        )
        return async_add_entities([])

    _LOGGER.info(
        "Controller %s supports parameter editing - paramsEdits: %s, editParams: %s",
        controller_id,
        has_params_edits,
        has_edit_params,
    )

    for key in number_map:
        # Get limits using the appropriate method based on controller type
        number_limits = None

        if has_edit_params:
            # For editParams, get limits directly from coordinator data (already fetched)
            edit_params = coordinator.data.get("editParams", {})
            if key in edit_params:
                param_data = edit_params[key]
                if isinstance(param_data, dict) and "minv" in param_data and "maxv" in param_data:
                    number_limits = Limits(param_data["minv"], param_data["maxv"])
                    _LOGGER.debug(
                        "Extracted limits for %s from editParams: min=%s, max=%s",
                        key,
                        number_limits.min,
                        number_limits.max,
                    )
        elif has_params_edits:
            # For paramsEdits, use the API method (needs separate fetch)
            number_limits = await api.get_param_limits(key)

        if number_limits is None:
            _LOGGER.info(
                "Cannot add number entity: %s, numeric limits for this entity is None",
                key,
            )
            continue

        if can_add(key, coordinator, has_params_edits, has_edit_params):
            entity_description = create_number_entity_description(key, controller_id)
            entity_description = apply_limits(entity_description, number_limits)
            entities.append(
                EconetNumber(
                    entity_description,
                    coordinator,
                    api,
                    has_params_edits,
                    has_edit_params,
                )
            )
        else:
            _LOGGER.info(
                "Cannot add number entity - availability key: %s does not exist",
                key,
            )

    return async_add_entities(entities)
