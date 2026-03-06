"""Base entity number for Econet300."""

import asyncio
from dataclasses import dataclass
import logging
import re
import time
import traceback
from typing import Any

import aiohttp
from homeassistant.components.number import (
    NumberEntity,
    NumberEntityDescription,
    NumberMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import Limits
from .common import Econet300Api, EconetDataCoordinator, skip_params_edits
from .common_functions import (
    camel_to_snake,
    ecoster_exists,
    get_duplicate_display_name,
    get_duplicate_entity_key,
    get_validated_entity_component,
    is_ecoster_related,
    mixer_exists,
    validate_parameter_data,
)
from .const import (
    DEVICE_INFO_ADVANCED_PARAMETERS_NAME,
    DEVICE_INFO_MANUFACTURER,
    DEVICE_INFO_MODEL,
    DEVICE_INFO_SERVICE_PARAMETERS_NAME,
    DOMAIN,
    ENTITY_MAX_VALUE,
    ENTITY_MIN_VALUE,
    ENTITY_NUMBER_SENSOR_DEVICE_CLASS_MAP,
    ENTITY_STEP,
    ENTITY_UNIT_MAP,
    MIXER_RELATED_KEYWORDS,
    MIXER_SET_AVAILABILITY_KEY,
    NUMBER_MAP,
    NUMBER_OF_AVAILABLE_MIXERS,
    SENSOR_MIXER_KEY,
    SERVICE_API,
    SERVICE_COORDINATOR,
    UNIT_NAME_TO_HA_UNIT,
)
from .entity import EconetEntity, MixerEntity, get_device_info_for_component

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class EconetNumberEntityDescription(NumberEntityDescription):
    """Describes ecoNET number entity."""

    entity_category: EntityCategory | None = EntityCategory.CONFIG
    param_id: str | None = (
        None  # Original parameter ID for dynamic entities (lookup in mergedData)
    )
    component: str | None = None  # Component for device grouping (huw, mixer_1, etc.)


class EconetNumber(EconetEntity, NumberEntity):
    """Describes ecoNET number sensor entity."""

    entity_description: EconetNumberEntityDescription

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Return if entity should be enabled by default.

        CONFIG category entities are disabled by default.
        Other entities (DIAGNOSTIC or no category) are enabled.
        """
        return self.entity_description.entity_category != EntityCategory.CONFIG

    def __init__(
        self,
        entity_description: EconetNumberEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
    ):
        """Initialize a new ecoNET number entity."""
        self.entity_description = entity_description
        self.api = api
        # Initialize min/max from entity_description or use sensible defaults
        # Use 'is not None' to preserve 0.0 as valid min value
        self._attr_native_min_value = (
            entity_description.native_min_value
            if entity_description.native_min_value is not None
            else 0.0
        )
        self._attr_native_max_value = (
            entity_description.native_max_value
            if entity_description.native_max_value is not None
            else 100.0
        )
        super().__init__(coordinator, api)

    def _sync_state(self, value):
        """Sync the state of the ecoNET number entity."""
        _LOGGER.debug(
            "EconetNumber _sync_state called for entity %s with value: %s",
            self.entity_description.key,
            value,
        )
        _LOGGER.debug(
            "Entity key=%s, translation_key=%s, Value type: %s, Value keys: %s",
            self.entity_description.key,
            self.entity_description.translation_key,
            type(value),
            value.keys() if isinstance(value, dict) else "Not a dict",
        )

        # Handle both dict and direct value
        if isinstance(value, dict) and "value" in value:
            val = value.get("value")
            self._attr_native_value = float(val) if val is not None else None
            _LOGGER.debug("Extracted value from dict: %s", self._attr_native_value)
        elif isinstance(value, (int, float, str)) and value is not None:
            self._attr_native_value = float(value)
            _LOGGER.debug("Using direct value: %s", self._attr_native_value)
        else:
            self._attr_native_value = None
            _LOGGER.debug("Invalid value type, setting to None: %s", value)

        map_key = NUMBER_MAP.get(self.entity_description.key)

        if map_key:
            _LOGGER.debug(
                "Found map_key %s for entity %s, setting value limits",
                map_key,
                self.entity_description.key,
            )
            self._set_value_limits(value)
        else:
            _LOGGER.debug(
                "No map_key found for dynamic entity %s (not in NUMBER_MAP), skipping _set_value_limits",
                self.entity_description.key,
            )
        # Ensure the state is updated in Home Assistant.
        self.async_write_ha_state()
        # Create an asynchronous task for setting the limits.
        self.hass.async_create_task(self.async_set_limits_values())

    def _set_value_limits(self, value):
        """Set native min and max values for the entity."""
        if isinstance(value, dict):
            min_val = value.get("min")
            max_val = value.get("max")
            # Only update if we have valid values, otherwise keep existing values
            if min_val is not None:
                self._attr_native_min_value = float(min_val)
            if max_val is not None:
                self._attr_native_max_value = float(max_val)
        _LOGGER.debug(
            "ecoNETNumber _set_value_limits: min=%s, max=%s",
            self._attr_native_min_value,
            self._attr_native_max_value,
        )

    async def async_set_limits_values(self):
        """Async Sync number limits."""
        # Dynamic entities (with param_id) already have limits from mergedData
        # Skip API lookup for these entities to avoid log spam
        param_id = getattr(self.entity_description, "param_id", None)
        if param_id:
            _LOGGER.debug(
                "Skipping API limits lookup for dynamic entity %s (param_id=%s) - limits already set from mergedData",
                self.entity_description.key,
                param_id,
            )
            return

        _LOGGER.debug("Getting limits for entity key: %s", self.entity_description.key)
        number_limits = await self.api.get_param_limits(self.entity_description.key)
        _LOGGER.debug("Number limits retrieved: %s", number_limits)

        if not number_limits:
            _LOGGER.debug(
                "No API limits available for entity: %s",
                self.entity_description.key,
            )
            return

        # Directly set min and max values based on fetched limits.
        self._attr_native_min_value = (
            float(number_limits.min)
            if number_limits.min is not None
            else self._attr_native_min_value
        )
        self._attr_native_max_value = (
            float(number_limits.max)
            if number_limits.max is not None
            else self._attr_native_max_value
        )
        _LOGGER.debug("Apply number limits: %s", self)
        self.async_write_ha_state()

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device info based on entity component."""
        component = getattr(self.entity_description, "component", None)
        if component:
            return get_device_info_for_component(component, self.api)
        # Fall back to parent class device_info (main boiler device)
        return super().device_info

    @property
    def icon(self) -> str | None:
        """Return icon for entity."""
        if self._is_parameter_locked():
            return "mdi:lock"  # Show lock icon for locked parameters
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes including lock information."""
        attrs: dict[str, Any] = {}
        # Add description from API to help users understand the parameter
        description = self._get_description()
        if description:
            attrs["description"] = description
        if self._is_parameter_locked():
            attrs["locked"] = True
            lock_reason = self._get_lock_reason()
            if lock_reason:
                attrs["lock_reason"] = lock_reason
        return attrs

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        _LOGGER.debug("Set value: %s", value)

        # Check if parameter is locked
        if self._is_parameter_locked():
            lock_reason = self._get_lock_reason() or "Parameter is locked"
            _LOGGER.warning(
                "Cannot set value for locked parameter: %s (%s) - %s",
                self.entity_description.key,
                self.entity_description.name,
                lock_reason,
            )
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                translation_key="parameter_locked",
                translation_placeholders={"lock_reason": lock_reason},
            )

        # Skip processing if the value is unchanged.
        if value == self._attr_native_value:
            return

        if value > self._attr_native_max_value:
            _LOGGER.warning(
                "Requested value: '%s' exceeds maximum allowed value: '%s'",
                value,
                self._attr_native_max_value,
            )

        if value < self._attr_native_min_value:
            _LOGGER.warning(
                "Requested value: '%s' is below allowed value: '%s'",
                value,
                self._attr_native_min_value,
            )
            return

        # For dynamic entities (param_id set), use param_id with rmNewParam
        # For static entities (NUMBER_MAP), use entity key with rmCurrNewParam
        param_id = getattr(self.entity_description, "param_id", None)
        if param_id:
            # Dynamic entity - use param_id (parameter number) with rmNewParam
            # API stores raw float values (mult is just step size, not scaling)
            # Get the parameter's number (index in rmParamsData array)
            merged_data = (
                self.coordinator.data.get("mergedData", {})
                if self.coordinator.data
                else {}
            )
            merged_parameters = merged_data.get("parameters", {})
            param_data = merged_parameters.get(param_id, {})
            param_number = param_data.get("number", param_id)

            _LOGGER.debug(
                "Dynamic entity: param_id=%s, param_number=%s, value=%s",
                param_id,
                param_number,
                value,
            )
            if not await self.api.set_param_by_index(param_number, value):
                _LOGGER.warning(
                    "Setting value failed for param_number %s", param_number
                )
                return
        elif not await self.api.set_param(self.entity_description.key, int(value)):
            # Static entity - use entity key (for NUMBER_MAP entities)
            _LOGGER.warning("Setting value failed")
            return

        self._attr_native_value = value
        self.async_write_ha_state()


class MixerNumber(MixerEntity, NumberEntity):
    """Mixer number class."""

    entity_description: EconetNumberEntityDescription

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Return if entity should be enabled by default.

        CONFIG category entities are disabled by default.
        Other entities (DIAGNOSTIC or no category) are enabled.
        """
        return self.entity_description.entity_category != EntityCategory.CONFIG

    def __init__(
        self,
        description: EconetNumberEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
        idx: int,
    ):
        """Initialize a new instance of the MixerNumber class."""
        # Track last write time to skip coordinator updates briefly after manual changes
        # This prevents stale API data from reverting local state
        self._last_write_time: float = 0.0
        self._write_cooldown_seconds: float = (
            5.0  # Skip updates for 5 seconds after write
        )

        # Initialize min/max from entity_description or use sensible defaults
        # Use 'is not None' to preserve 0.0 as valid min value
        self._attr_native_min_value = (
            description.native_min_value
            if description.native_min_value is not None
            else 0.0
        )
        self._attr_native_max_value = (
            description.native_max_value
            if description.native_max_value is not None
            else 100.0
        )
        super().__init__(description, coordinator, api, idx)

    def _sync_state(self, value):
        """Sync the state of the mixer number entity."""
        # Skip updates briefly after a manual write to prevent stale data reverting state
        if time.monotonic() - self._last_write_time < self._write_cooldown_seconds:
            _LOGGER.debug(
                "Skipping _sync_state for %s (within cooldown after write)",
                self.entity_description.key,
            )
            return

        _LOGGER.debug(
            "MixerNumber _sync_state for entity %s: %s",
            self.entity_description.key,
            value,
        )
        _LOGGER.debug(
            "Entity key=%s, translation_key=%s, Value type: %s, Value keys: %s",
            self.entity_description.key,
            self.entity_description.translation_key,
            type(value),
            value.keys() if isinstance(value, dict) else "Not a dict",
        )

        # Handle both dict and direct value
        if isinstance(value, dict) and "value" in value:
            val = value.get("value")
            self._attr_native_value = float(val) if val is not None else None
            _LOGGER.debug("Extracted value from dict: %s", self._attr_native_value)
        elif isinstance(value, (int, float, str)) and value is not None:
            self._attr_native_value = float(value)
            _LOGGER.debug("Using direct value: %s", self._attr_native_value)
        else:
            self._attr_native_value = None
            _LOGGER.debug("Invalid value type, setting to None: %s", value)

        map_key = NUMBER_MAP.get(self.entity_description.key)

        if map_key:
            _LOGGER.debug(
                "Found map_key %s for mixer entity %s, setting value limits",
                map_key,
                self.entity_description.key,
            )
            self._set_value_limits(value)
        else:
            _LOGGER.debug(
                "No map_key found for mixer entity %s (not in NUMBER_MAP), skipping _set_value_limits",
                self.entity_description.key,
            )
        # Ensure the state is updated in Home Assistant.
        self.async_write_ha_state()
        # Create an asynchronous task for setting the limits.
        self.hass.async_create_task(self.async_set_limits_values())

    def _set_value_limits(self, value):
        """Set native min and max values for the entity."""
        if isinstance(value, dict):
            min_val = value.get("min")
            max_val = value.get("max")
            # Only update if we have valid values, otherwise keep existing values
            if min_val is not None:
                self._attr_native_min_value = float(min_val)
            if max_val is not None:
                self._attr_native_max_value = float(max_val)
        _LOGGER.debug(
            "MixerNumber _set_value_limits: min=%s, max=%s",
            self._attr_native_min_value,
            self._attr_native_max_value,
        )

    async def async_set_limits_values(self):
        """Async Sync number limits."""
        # Dynamic mixer entities (with param_id) already have limits from mergedData
        param_id = getattr(self.entity_description, "param_id", None)
        if param_id:
            _LOGGER.debug(
                "Skipping API limits lookup for dynamic mixer entity %s (param_id=%s)",
                self.entity_description.key,
                param_id,
            )
            return

        number_limits = await self.api.get_param_limits(self.entity_description.key)
        _LOGGER.debug("Number limits retrieved: %s", number_limits)

        if not number_limits:
            _LOGGER.debug(
                "No API limits available for mixer entity: %s",
                self.entity_description.key,
            )
            return

        # Directly set min and max values based on fetched limits.
        self._attr_native_min_value = (
            float(number_limits.min)
            if number_limits.min is not None
            else self._attr_native_min_value
        )
        self._attr_native_max_value = (
            float(number_limits.max)
            if number_limits.max is not None
            else self._attr_native_max_value
        )
        _LOGGER.debug("Apply mixer number limits: %s", self)
        self.async_write_ha_state()

    @property
    def icon(self) -> str | None:
        """Return icon for entity."""
        if self._is_parameter_locked():
            return "mdi:lock"  # Show lock icon for locked parameters
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes including lock information."""
        attrs: dict[str, Any] = {}
        description = self._get_description()
        if description:
            attrs["description"] = description
        if self._is_parameter_locked():
            attrs["locked"] = True
            lock_reason = self._get_lock_reason()
            if lock_reason:
                attrs["lock_reason"] = lock_reason
        return attrs

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        _LOGGER.debug("Set mixer value: %s", value)

        # Check if parameter is locked
        if self._is_parameter_locked():
            lock_reason = self._get_lock_reason() or "Parameter is locked"
            _LOGGER.warning(
                "Cannot set value for locked parameter: %s (%s) - %s",
                self.entity_description.key,
                self.entity_description.name,
                lock_reason,
            )
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                translation_key="parameter_locked",
                translation_placeholders={"lock_reason": lock_reason},
            )

        # Skip processing if the value is unchanged.
        if value == self._attr_native_value:
            return

        if value > self._attr_native_max_value:
            _LOGGER.warning(
                "Requested mixer value: '%s' exceeds maximum allowed value: '%s'",
                value,
                self._attr_native_max_value,
            )

        if value < self._attr_native_min_value:
            _LOGGER.warning(
                "Requested mixer value: '%s' is below allowed value: '%s'",
                value,
                self._attr_native_min_value,
            )
            return

        if not await self.api.set_param(self.entity_description.key, int(value)):
            _LOGGER.warning("Setting mixer value failed")
            return

        self._attr_native_value = value
        self._last_write_time = time.monotonic()  # Record write time for cooldown
        self.async_write_ha_state()


class ServiceParameterNumber(EconetNumber):
    """Service parameter number entity - hidden by default per HA documentation."""

    _attr_entity_category = EntityCategory.CONFIG
    _attr_entity_registry_visible_default = False

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device info for service parameters."""
        return DeviceInfo(
            identifiers={(DOMAIN, f"{self.api.uid}-service-parameters")},
            name=DEVICE_INFO_SERVICE_PARAMETERS_NAME,
            manufacturer=DEVICE_INFO_MANUFACTURER,
            model=DEVICE_INFO_MODEL,
            via_device=(DOMAIN, self.api.uid),
        )


class AdvancedParameterNumber(EconetNumber):
    """Advanced parameter number entity - hidden by default per HA documentation."""

    _attr_entity_category = EntityCategory.CONFIG
    _attr_entity_registry_visible_default = False

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device info for advanced parameters."""
        return DeviceInfo(
            identifiers={(DOMAIN, f"{self.api.uid}-advanced-parameters")},
            name=DEVICE_INFO_ADVANCED_PARAMETERS_NAME,
            manufacturer=DEVICE_INFO_MANUFACTURER,
            model=DEVICE_INFO_MODEL,
            via_device=(DOMAIN, self.api.uid),
        )


def can_add(key: str, coordinator: EconetDataCoordinator) -> bool:
    """Check if a given entity can be added based on the availability of data in the coordinator."""
    try:
        return (
            coordinator.has_param_edit_data(key)
            and coordinator.data["paramsEdits"][key]
        )
    except KeyError as e:
        _LOGGER.error("KeyError in can_add: %s", e)
        return False


def create_number_entity_description(
    key: str, limits: Limits | None = None
) -> EconetNumberEntityDescription:
    """Create ecoNET300 number entity description."""
    map_key = NUMBER_MAP.get(str(key), str(key))
    _LOGGER.debug("Creating number entity for key: %s", map_key)

    # Use limits if provided, otherwise use default values
    min_value = (
        float(limits.min)
        if limits and limits.min is not None
        else float(ENTITY_MIN_VALUE.get(map_key, 0))
    )
    max_value = (
        float(limits.max)
        if limits and limits.max is not None
        else float(ENTITY_MAX_VALUE.get(map_key, 100))
    )

    return EconetNumberEntityDescription(
        key=key,
        translation_key=camel_to_snake(map_key),
        device_class=ENTITY_NUMBER_SENSOR_DEVICE_CLASS_MAP.get(map_key),
        mode=NumberMode.BOX,  # Show as input box instead of slider
        native_unit_of_measurement=ENTITY_UNIT_MAP.get(map_key),
        native_min_value=min_value,
        native_max_value=max_value,
        native_step=ENTITY_STEP.get(map_key, 1),
        entity_category=EntityCategory.CONFIG,
    )


def is_mixer_related_entity(param_name: str, param_key: str) -> tuple[bool, int | None]:
    """Check if a dynamic entity is mixer-related and return the mixer number.

    Args:
        param_name: The parameter name (e.g., "Preset mixer 1 temperature")
        param_key: The parameter key (e.g., "preset_mixer1_temperature")

    Returns:
        Tuple of (is_mixer_related, mixer_number)

    """

    # Check parameter name for mixer patterns
    mixer_patterns = [
        r"mixer\s*(\d+)",  # "mixer 1", "mixer1"
        r"mixer(\d+)",  # "mixer1"
        r"(\d+)\s*mixer",  # "1 mixer"
    ]

    for pattern in mixer_patterns:
        match = re.search(pattern, param_name.lower())
        if match:
            mixer_num = int(match.group(1))
            if 1 <= mixer_num <= NUMBER_OF_AVAILABLE_MIXERS:
                return True, mixer_num

    # Check parameter key for mixer patterns
    mixer_key_patterns = [
        r"mixer(\d+)",  # "mixer1"
        r"(\d+)_mixer",  # "1_mixer"
    ]

    for pattern in mixer_key_patterns:
        match = re.search(pattern, param_key.lower())
        if match:
            mixer_num = int(match.group(1))
            if 1 <= mixer_num <= NUMBER_OF_AVAILABLE_MIXERS:
                return True, mixer_num

    return False, None


def should_be_number_entity(param: dict) -> bool:
    """Check if parameter should be a number entity.

    Args:
        param: Parameter dictionary from merged data

    Returns:
        True if parameter should be a number entity

    """
    has_enum = "enum" in param
    is_editable = param.get("edit", False)

    # Must be editable and not have enum
    if not is_editable or has_enum:
        return False

    # Check for unit_name - if present, it's a number entity
    unit_name = param.get("unit_name", "")
    if unit_name:
        return True

    # Even without unit_name, check if it's a numeric parameter
    # Parameters with decimal multiplier (mult < 1) are numeric (e.g., heating curve 0.1-4.0)
    mult = param.get("mult", 1)
    if isinstance(mult, (int, float)) and mult < 1:
        return True

    # Parameters with fractional min/max are numeric
    minv = param.get("minv")
    maxv = param.get("maxv")
    if minv is not None and maxv is not None:
        if isinstance(minv, (int, float)) and isinstance(maxv, (int, float)):
            # Fractional values indicate numeric parameter
            if minv != int(minv) or maxv != int(maxv):
                return True

    return False


async def create_mixer_number_entities(
    coordinator: EconetDataCoordinator, api: Econet300Api
) -> list[MixerNumber]:
    """Create mixer number entities dynamically based on available mixers."""
    entities: list[MixerNumber] = []

    try:
        _LOGGER.debug("Entering create_mixer_number_entities function")
        _LOGGER.debug("Creating mixer number entities dynamically...")

        # Use the same logic as sensor.py - check SENSOR_MIXER_KEY
        for mixer_idx, mixer_keys in SENSOR_MIXER_KEY.items():
            _LOGGER.debug("Checking mixer %d with keys: %s", mixer_idx, mixer_keys)
            # Skip if coordinator data is not available
            if coordinator.data is None:
                _LOGGER.info("Mixer: %d skipped - coordinator data is None", mixer_idx)
                continue

            # Check if all required mixer keys have valid (non-null) values
            reg_params = coordinator.data.get("regParams", {})
            if reg_params is None or any(
                reg_params.get(mixer_key) is None for mixer_key in mixer_keys
            ):
                _LOGGER.info(
                    "Mixer: %d will not be created due to invalid data.", mixer_idx
                )
                continue

            _LOGGER.debug("Mixer %d passed validation, creating entity", mixer_idx)
            # Create the mixer set temperature key (e.g., "mixerSetTemp1")
            mixer_set_temp_key = f"{MIXER_SET_AVAILABILITY_KEY}{mixer_idx}"

            # Create entity description with default limits (like mixer sensors)
            # Mixer sensors don't need API limits, they get data from regParams
            entity_description = create_number_entity_description(
                mixer_set_temp_key,
                None,  # No limits needed, like mixer sensors
            )

            # Create and add the entity
            entity = MixerNumber(entity_description, coordinator, api, mixer_idx)
            entities.append(entity)
            _LOGGER.debug(
                "Created mixer number entity: %s (Mixer %d)",
                mixer_set_temp_key,
                mixer_idx,
            )
            _LOGGER.debug(
                "MixerNumber device_info: %s",
                entity.device_info,
            )

        _LOGGER.debug(
            "Exiting create_mixer_number_entities with %d entities",
            len(entities),
        )

    except (
        aiohttp.ClientError,
        asyncio.TimeoutError,
        ValueError,
        TypeError,
        AttributeError,
        KeyError,
    ) as e:
        _LOGGER.error("Exception in create_mixer_number_entities: %s", e)
        _LOGGER.error("Exception type: %s", type(e))
        _LOGGER.error("Traceback: %s", traceback.format_exc())

    return entities


def create_dynamic_number_entity_description(
    param_id: str,
    param: dict,
    display_name: str | None = None,
    entity_key_override: str | None = None,
    sequence_num: int | None = None,
    coordinator_data: dict | None = None,
) -> EconetNumberEntityDescription:
    """Create a number entity description from parameter data.

    Args:
        param_id: Parameter ID (string)
        param: Parameter dictionary from merged data
        display_name: Optional display name override for duplicate handling
        entity_key_override: Optional entity key override for duplicate handling
        sequence_num: Sequence number for duplicate parameters (for device grouping)
        coordinator_data: Coordinator data for device validation

    Returns:
        EconetNumberEntityDescription for the parameter

    """
    # Get unit mapping
    unit_name = param.get("unit_name", "")
    ha_unit = UNIT_NAME_TO_HA_UNIT.get(unit_name)

    # Get min/max values
    min_value = float(param.get("minv", 0))
    max_value = float(param.get("maxv", 100))

    # Use mult from API as step if available, otherwise use heuristics
    mult = param.get("mult")
    if mult is not None and mult > 0:
        step = float(mult)
    elif unit_name in {"%", "°C"} or unit_name in ["sek.", "min.", "h."]:
        step = 1.0
    elif max_value - min_value > 100:
        step = 5.0
    else:
        step = 1.0

    # Generate translation key
    param_key = param.get("key", f"parameter_{param_id}")
    translation_key = param_key

    # Generate entity key - use override if provided (for duplicates)
    # Guard against collision with static NUMBER_MAP keys (e.g., "1280")
    base_key = entity_key_override or param_key
    entity_key = f"dyn_{base_key}" if base_key in NUMBER_MAP else base_key

    # Use display_name override if provided (for duplicates)
    name = display_name or param.get("name", f"Parameter {param_id}")

    # Determine component for device grouping (with hardware validation)
    param_name = param.get("name", "")
    description = param.get("description", "")
    component = get_validated_entity_component(
        param_name, param_key, description, sequence_num, coordinator_data
    )

    _LOGGER.debug(
        "Creating entity description for param_id=%s, name=%s, key=%s, entity_key=%s, component=%s",
        param_id,
        name,
        param_key,
        entity_key,
        component,
    )

    return EconetNumberEntityDescription(
        key=entity_key,  # Use category-prefixed key
        name=name,  # Add explicit name (or override for duplicates)
        translation_key=translation_key,
        device_class=None,  # No specific device class for dynamic entities
        mode=NumberMode.BOX,  # Always show as number input box
        native_unit_of_measurement=ha_unit,
        native_min_value=min_value,
        native_max_value=max_value,
        native_step=step,
        entity_category=EntityCategory.CONFIG,  # All dynamic entities in Configuration
        param_id=param_id,  # Store original param_id for mergedData lookup
        component=component,  # Component for device grouping
    )


async def _create_basic_entities(
    api: Econet300Api, coordinator: EconetDataCoordinator
) -> list[EconetNumber]:
    """Create basic NUMBER_MAP entities.

    Args:
        api: API instance
        coordinator: Data coordinator

    Returns:
        List of basic number entities

    """
    entities: list[EconetNumber] = []
    _LOGGER.info("Creating basic NUMBER_MAP entities (always shown)")
    for key in NUMBER_MAP:
        # Skip mixer entities as they are created dynamically
        map_value = NUMBER_MAP.get(key)
        if map_value and map_value.startswith("mixerSetTemp"):
            continue
        number_limits = await api.get_param_limits(key)
        if number_limits is None:
            _LOGGER.info(
                "Cannot add basic number entity: %s, numeric limits for this entity is None",
                key,
            )
            continue

        if can_add(key, coordinator):
            entity_description = create_number_entity_description(key, number_limits)
            entities.append(EconetNumber(entity_description, coordinator, api))
            _LOGGER.info("Created basic number entity: %s (%s)", key, map_value)
        else:
            _LOGGER.info(
                "Cannot add basic number entity - availability key: %s does not exist",
                key,
            )
    _LOGGER.info("Created %d basic NUMBER_MAP entities", len(entities))
    return entities


def _create_mixer_entity_by_category(
    entity_description: EconetNumberEntityDescription,
    coordinator: EconetDataCoordinator,
    api: Econet300Api,
    mixer_num: int,
    param_name: str,
) -> NumberEntity:
    """Create mixer entity.

    All mixer entities are grouped into their respective "Mixer X settings" devices.

    Args:
        entity_description: Entity description
        coordinator: Data coordinator
        api: API instance
        mixer_num: Mixer number (1-4)
        param_name: Parameter name

    Returns:
        EconetNumber entity grouped under Mixer device

    """
    entity = EconetNumber(
        entity_description,
        coordinator,
        api,
    )

    _LOGGER.info(
        "Created mixer number entity: %s (Mixer %d)",
        param_name,
        mixer_num,
    )

    return entity


def _create_regular_entity_by_category(
    entity_description: EconetNumberEntityDescription,
    coordinator: EconetDataCoordinator,
    api: Econet300Api,
    param_name: str,
    param_id: str,
    param: dict,
) -> NumberEntity:
    """Create regular number entity.

    Args:
        entity_description: Entity description
        coordinator: Data coordinator
        api: API instance
        param_name: Parameter name
        param_id: Parameter ID
        param: Parameter dictionary

    Returns:
        EconetNumber entity

    """
    entity = EconetNumber(
        entity_description,
        coordinator,
        api,
    )

    _LOGGER.info(
        "Created number entity: %s (%s) - %s to %s %s",
        param_name,
        param_id,
        param.get("minv", 0),
        param.get("maxv", 100),
        param.get("unit_name", ""),
    )

    return entity


def _create_dynamic_entity_from_param(
    param_id: str,
    param: dict,
    coordinator: EconetDataCoordinator,
    api: Econet300Api,
    basic_param_ids: set[str],
    display_name: str | None = None,
    entity_key_override: str | None = None,
    sequence_num: int | None = None,
) -> NumberEntity | None:
    """Create a dynamic entity from a parameter.

    Args:
        param_id: Parameter ID
        param: Parameter dictionary
        coordinator: Data coordinator
        api: API instance
        basic_param_ids: Set of basic parameter IDs to skip
        display_name: Optional display name override for duplicate handling
        entity_key_override: Optional entity key override for duplicate handling
        sequence_num: Sequence number for duplicate parameters (for device grouping)

    Returns:
        Created entity or None if skipped

    """
    # Validate parameter data first
    is_valid, error_msg = validate_parameter_data(param)
    if not is_valid:
        _LOGGER.debug(
            "Skipping invalid parameter %s: %s",
            param_id,
            error_msg,
        )
        return None

    # Skip basic parameters (already created from NUMBER_MAP)
    # Compare using data_id which maps to regParams keys (e.g., "1280", "1281")
    # Note: param_id is an array index ("0", "1", etc.), not a regParams key
    param_data_id = param.get("data_id")
    if param_data_id and param_data_id in basic_param_ids:
        _LOGGER.debug(
            "Skipping parameter %s (data_id=%s) - already created as basic NUMBER_MAP entity",
            param_id,
            param_data_id,
        )
        return None

    if not should_be_number_entity(param):
        return None

    # Check if ecoSTER-related and if ecoSTER panel is connected
    if is_ecoster_related(param):
        if not ecoster_exists(coordinator.data):
            _LOGGER.debug(
                "Skipping number %s - ecoSTER panel not connected",
                param.get("name", param_id),
            )
            return None

    param_name = display_name or param.get("name", f"Parameter {param_id}")

    _LOGGER.debug(
        "Parameter %s qualifies as number entity: name=%s, unit_name=%s, edit=%s",
        param_id,
        param_name,
        param.get("unit_name", "No unit"),
        param.get("edit", False),
    )

    try:
        entity_description = create_dynamic_number_entity_description(
            param_id,
            param,
            display_name,
            entity_key_override,
            sequence_num,
            coordinator.data,
        )

        # Check if this is a mixer-related entity
        param_key = param.get("key", f"parameter_{param_id}")
        is_mixer_related, mixer_num = is_mixer_related_entity(param_name, param_key)

        if is_mixer_related:
            _LOGGER.debug(
                "Found mixer-related entity: '%s' -> Mixer %d",
                param_name,
                mixer_num,
            )

        # Create entity based on type
        if is_mixer_related and mixer_num is not None:
            # Check if the mixer actually exists in the boiler
            if not mixer_exists(coordinator.data, mixer_num):
                _LOGGER.debug(
                    "Skipping mixer entity '%s' - Mixer %d does not exist",
                    param_name,
                    mixer_num,
                )
                return None

            return _create_mixer_entity_by_category(
                entity_description,
                coordinator,
                api,
                mixer_num,
                param_name,
            )

        return _create_regular_entity_by_category(
            entity_description,
            coordinator,
            api,
            param_name,
            param_id,
            param,
        )

    except (ValueError, KeyError, TypeError) as e:
        _LOGGER.warning(
            "Failed to create dynamic number entity for parameter %s: %s",
            param_id,
            e,
        )
        return None


async def _create_dynamic_entities_from_merged_data(
    merged_data: dict,
    coordinator: EconetDataCoordinator,
    api: Econet300Api,
    basic_param_ids: set[str],
) -> list[NumberEntity]:
    """Create dynamic entities from merged parameter data.

    Service and advanced parameters are created but hidden by default
    using entity_registry_visible_default = False per HA documentation.

    Args:
        merged_data: Merged parameter data
        coordinator: Data coordinator
        api: API instance
        basic_param_ids: Set of basic parameter IDs to skip

    Returns:
        List of dynamic entities

    """
    entities: list[NumberEntity] = []
    key_counts: dict[str, int] = {}  # Track how many times each key has been used
    _LOGGER.debug("Using dynamic number entity creation from merged parameter data")

    _LOGGER.debug(
        "Starting dynamic entity creation. Total parameters: %d",
        len(merged_data["parameters"]),
    )

    # Debug: Log first few parameters to understand structure
    for param_count, (param_id, param) in enumerate(merged_data["parameters"].items()):
        if param_count < 5:  # Log first 5 parameters for debugging
            categories = param.get("categories", [param.get("category", "")])
            _LOGGER.debug(
                "Sample parameter %s: name=%s, unit_name=%s, edit=%s, has_enum=%s, categories=%s",
                param_id,
                param.get("name", "No name"),
                param.get("unit_name", "No unit"),
                param.get("edit", False),
                "enum" in param,
                categories,
            )

    # First pass: count duplicates to know which keys need numbering
    key_totals: dict[str, int] = {}
    for param_id, param in merged_data["parameters"].items():
        if not should_be_number_entity(param):
            continue
        # Skip if data_id matches a NUMBER_MAP key (regParams ID)
        param_data_id = param.get("data_id")
        if param_data_id and param_data_id in basic_param_ids:
            continue
        param_key = param.get("key", f"parameter_{param_id}")
        key_totals[param_key] = key_totals.get(param_key, 0) + 1

    number_entity_count = 0

    for param_id, param in merged_data["parameters"].items():
        _LOGGER.debug("Processing parameter %s: %s", param_id, param)

        # Get parameter key - this is what determines uniqueness
        param_key = param.get("key", f"parameter_{param_id}")
        description = param.get("description", "")

        # Handle duplicates with meaningful suffixes (e.g., "Mixer 1" instead of "1")
        display_name = None
        entity_key_override = None

        if key_totals.get(param_key, 1) > 1:
            key_counts[param_key] = key_counts.get(param_key, 0) + 1
            sequence_num = key_counts[param_key]

            # For mixer-related duplicates, validate mixer exists before creating
            # Check for keywords that indicate mixer-related parameters
            desc_lower = description.lower() if description else ""
            is_mixer_related = any(kw in desc_lower for kw in MIXER_RELATED_KEYWORDS)
            if is_mixer_related:
                if not mixer_exists(coordinator.data, sequence_num):
                    _LOGGER.debug(
                        "Skipping number %s (Mixer %d) - mixer not connected",
                        param.get("name", param_id),
                        sequence_num,
                    )
                    continue

            param_name = param.get("name", f"Parameter {param_id}")
            display_name = get_duplicate_display_name(
                param_name, sequence_num, description
            )
            entity_key_override = get_duplicate_entity_key(
                param_key, sequence_num, description
            )
        else:
            sequence_num = None

        # Create number entity
        entity = _create_dynamic_entity_from_param(
            param_id,
            param,
            coordinator,
            api,
            basic_param_ids,
            display_name,
            entity_key_override,
            sequence_num,
        )
        if entity:
            entities.append(entity)
            number_entity_count += 1

    _LOGGER.debug(
        "Found %d parameters that qualify as number entities",
        number_entity_count,
    )
    _LOGGER.debug(
        "Created %d dynamic number entities (Information categories handled as sensors). "
        "Service/advanced parameters are hidden by default (entity_registry_visible_default=False).",
        len(entities),
    )

    return entities


async def _create_legacy_entities(
    api: Econet300Api, coordinator: EconetDataCoordinator
) -> list[NumberEntity]:
    """Create legacy entities from NUMBER_MAP (fallback).

    Args:
        api: API instance
        coordinator: Data coordinator

    Returns:
        List of legacy entities

    """
    entities: list[NumberEntity] = []
    _LOGGER.info("Falling back to legacy number entity creation from NUMBER_MAP")

    # Create mixer number entities dynamically
    _LOGGER.debug("Creating mixer number entities...")
    mixer_entities = await create_mixer_number_entities(coordinator, api)
    _LOGGER.debug("Created %d mixer number entities", len(mixer_entities))
    entities.extend(mixer_entities)

    # Create other number entities from NUMBER_MAP (excluding mixer entities)
    for key in NUMBER_MAP:
        # Skip mixer entities as they are created dynamically above
        map_value = NUMBER_MAP.get(key)
        if map_value and map_value.startswith("mixerSetTemp"):
            continue
        number_limits = await api.get_param_limits(key)
        if number_limits is None:
            _LOGGER.info(
                "Cannot add number entity: %s, numeric limits for this entity is None",
                key,
            )
            continue

        if can_add(key, coordinator):
            entity_description = create_number_entity_description(key, number_limits)
            entities.append(EconetNumber(entity_description, coordinator, api))
        else:
            _LOGGER.info(
                "Cannot add number entity - availability key: %s does not exist",
                key,
            )

    return entities


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the number platform.

    Dynamic entities are always created. Service and advanced parameters
    are hidden by default using entity_registry_visible_default = False,
    following Home Assistant documentation recommendations.
    """
    coordinator = hass.data[DOMAIN][entry.entry_id][SERVICE_COORDINATOR]
    api = hass.data[DOMAIN][entry.entry_id][SERVICE_API]

    entities: list[NumberEntity] = []

    # Define basic parameter IDs from NUMBER_MAP (always shown)
    basic_param_ids = set(NUMBER_MAP.keys())

    # Check if we should skip params edits for certain controllers
    sys_params = None
    if coordinator.data is not None:
        sys_params = coordinator.data.get("sysParams")
    if sys_params is None:
        sys_params = {}
    if skip_params_edits(sys_params):
        _LOGGER.info("Skipping number entity setup for controllerID: ecoMAX360i")
        return async_add_entities(entities)

    # Always create basic NUMBER_MAP entities first
    basic_entities = await _create_basic_entities(api, coordinator)
    entities.extend(basic_entities)

    # Get merged parameter data from coordinator (already fetched during update)
    merged_data = None
    if coordinator.data is not None:
        merged_data = coordinator.data.get("mergedData")
        _LOGGER.debug(
            "Using coordinator cached mergedData: %s parameters",
            len(merged_data.get("parameters", {})) if merged_data else 0,
        )

    if merged_data and "parameters" in merged_data:
        # Create dynamic entities from merged data
        dynamic_entities = await _create_dynamic_entities_from_merged_data(
            merged_data, coordinator, api, basic_param_ids
        )
        entities.extend(dynamic_entities)

        # Create mixer number entities dynamically (even in dynamic mode)
        _LOGGER.debug("About to call create_mixer_number_entities...")
        mixer_entities = await create_mixer_number_entities(coordinator, api)
        _LOGGER.debug(
            "create_mixer_number_entities returned %d entities",
            len(mixer_entities),
        )
        entities.extend(mixer_entities)
        _LOGGER.debug("Total entities after adding mixer entities: %d", len(entities))
    else:
        # Fallback to legacy entity creation
        legacy_entities = await _create_legacy_entities(api, coordinator)
        entities.extend(legacy_entities)

    # Final check - if no entities were created, log a warning
    mixer_count = len([e for e in entities if isinstance(e, MixerNumber)])
    dynamic_count = len([e for e in entities if e not in basic_entities])
    _LOGGER.info(
        "Final entity count: %d total entities created (%d basic + %d advanced + %d mixer)",
        len(entities),
        len(basic_entities),
        dynamic_count,
        mixer_count,
    )
    if not entities:
        _LOGGER.warning(
            "No number entities could be created. This may indicate that your device "
            "does not support the rmParamsData endpoint for dynamic entities, and "
            "the legacy NUMBER_MAP entities are not available on your device."
        )

    return async_add_entities(entities)
