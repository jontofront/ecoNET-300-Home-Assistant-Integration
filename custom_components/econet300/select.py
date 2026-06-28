"""Select entities for ecoNET300 integration.

This module implements select entities for the ecoNET300 integration.
Uses Home Assistant icon translation system via icons.json.
"""

import logging
import re
from typing import Any, NoReturn

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api import Econet300Api
from .common import EconetDataCoordinator
from .common_functions import (
    camel_to_snake,
    ecoster_exists,
    find_heater_mode_param,
    get_duplicate_display_name,
    get_duplicate_entity_key,
    get_heater_mode_options,
    get_validated_entity_component,
    heater_mode_icon,
    heater_mode_option_to_value,
    heater_mode_value_to_option,
    is_ecomax360i_controller,
    is_ecoster_related,
    mixer_exists,
)
from .const import (
    DOMAIN,
    MIXER_RELATED_KEYWORDS,
    SELECT_KEY_GET_INDEX,
    SELECT_KEY_POST_INDEX,
    SELECT_KEY_VALUES,
    SERVICE_API,
    SERVICE_COORDINATOR,
)
from .entity import EconetEntity, get_device_info_for_component

_LOGGER = logging.getLogger(__name__)


def _device_info(api: Econet300Api) -> DeviceInfo:
    """Return main ecoNET300 device info for editParams entities."""
    return DeviceInfo(
        identifiers={(DOMAIN, api.uid)},
        name="PLUM ecoNET300",
        manufacturer="PLUM",
        model="ecoNET300",
        configuration_url=api.host,
        sw_version=api.sw_rev,
        hw_version=api.hw_ver,
    )


class HeaterModeSelectError(HomeAssistantError):
    """Raised when heater mode selection fails."""

    def __init__(self, mode: str) -> None:
        """Initialize the error."""
        super().__init__(
            translation_domain=DOMAIN,
            translation_key="heater_mode_change_failed",
            translation_placeholders={"mode": mode},
        )


class EconetSelect(EconetEntity, SelectEntity):
    """Represents an ecoNET select entity."""

    entity_description: SelectEntityDescription
    select_key: str

    def __init__(
        self,
        entity_description: SelectEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
        select_key: str,
        merged_param: dict | None = None,
    ):
        """Initialize a new ecoNET select entity.

        When ``merged_param`` is provided, the entity resolves its name,
        options, and write ID from mergedData (issue #235). Otherwise it falls
        back to the hardcoded ``SELECT_KEY_*`` constants for legacy RM-less
        modules.
        """
        self.entity_description = entity_description
        self.api = api
        self.select_key = select_key
        self._merged_param = merged_param
        self._attr_current_option = None
        if merged_param is not None:
            name = merged_param.get("name")
            if name:
                self._attr_name = name
        super().__init__(coordinator, api)

    @property
    def options(self) -> list[str]:
        """Return the available options.

        With mergedData the options are the controller-native enum strings
        (e.g. ``Zima``/``Lato``); otherwise the hardcoded values are displayed
        as title-cased English names.
        """
        if self._merged_param is not None:
            return get_heater_mode_options(self._merged_param)
        values_dict = SELECT_KEY_VALUES.get(self.select_key, {})
        return [value.title() for value in values_dict.values()]

    def _is_locked(self) -> bool:
        """Return True when the resolved merged parameter is locked."""
        return bool(self._merged_param and self._merged_param.get("locked", False))

    def _lock_reason(self) -> str | None:
        """Return the merged parameter lock reason, if any."""
        return (self._merged_param or {}).get("lock_reason")

    @property
    def _state_index(self) -> str:
        """Return the regParamsData index used to read the current state."""
        return SELECT_KEY_GET_INDEX.get(self.select_key, "unknown")

    def _write_index(self) -> Any:
        """Return the parameter index used to write this select.

        Resolved from ``mergedData`` (``number``/``index``) when available,
        otherwise the hardcoded legacy ``SELECT_KEY_POST_INDEX`` fallback.
        """
        if self._merged_param is not None:
            return self._merged_param.get("number", self._merged_param.get("index"))
        return SELECT_KEY_POST_INDEX.get(self.select_key, "unknown")

    @property
    def icon(self) -> str | None:
        """Return the icon for the entity.

        For merged entities the icon is derived from the current option in a
        language-independent way (Zima/Winter -> snowflake, etc.), and a lock
        icon is shown when the parameter is locked. For the legacy fallback,
        Home Assistant handles icons via ``icons.json`` based on the option.
        """
        if self._is_locked():
            return "mdi:lock"
        if self._merged_param is not None:
            return heater_mode_icon(self._attr_current_option)
        return None

    @property
    def current_option(self) -> str | None:
        """Return the current option, matching the displayed ``options``."""
        if not self._attr_current_option:
            return None
        if self._merged_param is not None:
            return self._attr_current_option
        return self._attr_current_option.title()

    def _value_to_option(self, value: int) -> str | None:
        """Map a numeric reg value to the displayed option string."""
        if self._merged_param is not None:
            return heater_mode_value_to_option(self._merged_param, value)
        return SELECT_KEY_VALUES.get(self.select_key, {}).get(value)

    def _option_to_value(self, option: str) -> int | None:
        """Map a displayed option string back to its numeric value."""
        if self._merged_param is not None:
            return heater_mode_option_to_value(self._merged_param, option)
        return get_heater_mode_value(option.lower())

    def _sync_state(self, value: str | None) -> None:
        """Synchronize the state of the select entity."""
        _LOGGER.debug("🔄 _sync_state called with value: %s", value)
        self._attr_current_option = value
        self.async_write_ha_state()

    @property
    def available(self) -> bool:
        """Return availability combining stale-data check and value presence."""
        if not super().available:
            return False
        return self._attr_available

    def _refresh_from_reg_params(self) -> None:
        """Resolve the current heater-mode option from regParamsData[2049]."""
        data = self.coordinator.data
        reg_params_data = (data or {}).get("regParamsData") or {}
        raw_value = reg_params_data.get(self._state_index)
        _LOGGER.debug(
            "🎯 Heater mode current state (%s): %s", self._state_index, raw_value
        )

        if raw_value is None:
            self._attr_available = False
            self._sync_state(None)
            return

        option = self._value_to_option(raw_value)
        if option is not None:
            self._attr_available = True
            self._sync_state(option)
        else:
            _LOGGER.warning(
                "❌ Unknown heater mode value: %s (options: %s)",
                raw_value,
                self.options,
            )
            self._attr_available = False
            self._sync_state(None)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return entity specific state attributes."""
        current_option = self._attr_current_option
        heater_mode_value = (
            self._option_to_value(current_option) if current_option else None
        )

        current_state_value = None
        if self.coordinator.data is not None:
            reg_params_data = self.coordinator.data.get("regParamsData") or {}
            current_state_value = reg_params_data.get(self._state_index)

        attrs: dict[str, Any] = {
            "heater_mode_value": heater_mode_value,
            "current_state_value": current_state_value,
            "available_options": self.options,
            "setting_parameter": self._write_index(),
            "current_state_parameter": self._state_index,
        }
        if self._is_locked():
            attrs["locked"] = True
            lock_reason = self._lock_reason()
            if lock_reason:
                attrs["lock_reason"] = lock_reason
        return attrs

    async def async_added_to_hass(self):
        """Handle added to hass - read heater_mode state from regParamsData."""
        _LOGGER.debug(
            "🏠 async_added_to_hass called for: %s", self.entity_description.key
        )
        # Register for coordinator updates first.
        await super().async_added_to_hass()

        if self.entity_description.key == "heater_mode":
            self._refresh_from_reg_params()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug(
            "🔄 _handle_coordinator_update called for: %s", self.entity_description.key
        )

        if self.coordinator.data is None:
            _LOGGER.debug("❌ Coordinator data is None")
            return

        if self.entity_description.key == "heater_mode":
            self._refresh_from_reg_params()
        else:
            super()._handle_coordinator_update()

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        _LOGGER.debug("🎯 async_select_option called with option: %s", option)

        if self._is_locked():
            lock_reason = self._lock_reason() or "Parameter is locked"
            _LOGGER.warning("Cannot change locked heater_mode: %s", lock_reason)
            self._raise_heater_mode_error(f"Heater mode is locked: {lock_reason}")

        try:
            value = self._option_to_value(option)
            _LOGGER.debug("🔢 Converted option '%s' to value: %s", option, value)

            if value is None:
                _LOGGER.error("❌ Invalid option: %s", option)
                self._raise_heater_mode_error(f"Invalid option: {option}")

            param_index = self._write_index()
            if self._merged_param is not None:
                if param_index is None:
                    self._raise_heater_mode_error(f"No write index for {option}")
                _LOGGER.debug(
                    "📡 Setting heater mode via index %s to value %s",
                    param_index,
                    value,
                )
                success = await self.api.set_param_by_index(param_index, value)
            else:
                _LOGGER.debug(
                    "📡 Setting heater mode via param %s to value %s",
                    param_index,
                    value,
                )
                success = await self.api.set_param(param_index, value)
            _LOGGER.debug("📡 API call result: %s", success)

            if success:
                old_option = self._attr_current_option
                self._attr_current_option = option
                self._attr_available = True
                _LOGGER.info(
                    "Heater mode changed from '%s' to '%s' (API value: %s)",
                    old_option or "unknown",
                    option,
                    value,
                )
                self.async_write_ha_state()
            else:
                _LOGGER.error(
                    "Failed to change heater mode to %s - API returned failure", option
                )
                self._raise_heater_mode_error(
                    f"Failed to change heater mode to {option}"
                )

        except HeaterModeSelectError:
            raise
        except Exception as e:
            _LOGGER.error("Failed to change heater mode to %s: %s", option, e)
            raise HeaterModeSelectError(option) from e

    @staticmethod
    def _raise_heater_mode_error(mode: str) -> NoReturn:
        """Raise a HeaterModeSelectError with the given mode."""
        raise HeaterModeSelectError(mode)


class EconetDynamicSelect(EconetEntity, SelectEntity):
    """Represents a dynamic ecoNET select entity from mergedData."""

    _attr_has_entity_name = True

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Return if entity should be enabled by default.

        CONFIG category entities are disabled by default.
        Selects without category are also disabled (they are config controls).
        """
        entity_category = getattr(self.entity_description, "entity_category", None)
        # Selects are disabled by default unless explicitly not CONFIG
        return entity_category is not None and entity_category != EntityCategory.CONFIG

    def __init__(
        self,
        entity_description: SelectEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
        param_id: str,
        param: dict,
        sequence_num: int | None = None,
    ):
        """Initialize a new dynamic ecoNET select entity."""
        super().__init__(coordinator, api)
        self.entity_description = entity_description
        self._param_id = param_id
        self._param = param
        self._attr_current_option = None

        # Get enum values
        enum_data = param.get("enum", {})
        self._enum_values = enum_data.get("values", [])
        self._first_index = enum_data.get("first", 0)

        # Set unique ID
        self._attr_unique_id = f"econet300_select_{param_id}"

        # Determine which component this entity belongs to (with hardware validation)
        param_name = param.get("name", "")
        param_key = param.get("key", "")
        description = param.get("description", "")
        self._component = get_validated_entity_component(
            param_name, param_key, description, sequence_num, coordinator.data
        )

        # Set initial state
        self._update_state_from_param()

    @property
    def options(self) -> list[str]:
        """Return the available options."""
        return [v for v in self._enum_values if v]

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info based on entity component."""
        return get_device_info_for_component(
            self._component,
            self.api,
            single_device=self.coordinator.single_device_tree,
        )

    @property
    def available(self) -> bool:
        """Return True when data is fresh and the parameter is still present.

        The coordinator keeps the last payload on transient failures, so
        ``last_update_success`` stays True even while the device is
        unreachable. Availability is therefore driven by the staleness flag
        in the coordinator ``_health`` block, matching every other entity.
        """
        data = self.coordinator.data or {}
        health = data.get("_health") or {}
        if bool(health.get("stale")):
            return False
        parameters = (data.get("mergedData") or {}).get("parameters", {})
        return self._param_id in parameters

    @property
    def icon(self) -> str | None:
        """Return icon for entity."""
        if self._is_parameter_locked():
            return "mdi:lock"
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        attrs: dict[str, Any] = {
            "param_id": self._param_id,
            "options": self._enum_values,
        }
        # Add description from API to help users understand the parameter
        description = self._param.get("description")
        if description:
            attrs["description"] = description
        if self._is_parameter_locked():
            attrs["locked"] = True
            lock_reason = self._get_lock_reason()
            if lock_reason:
                attrs["lock_reason"] = lock_reason
        return attrs

    def _update_state_from_param(self) -> None:
        """Update state from parameter value."""
        if self.coordinator.data is None:
            return

        merged_data = self.coordinator.data.get("mergedData")
        if not merged_data:
            return

        parameters = merged_data.get("parameters", {})
        param_data = parameters.get(self._param_id)
        if param_data:
            value = param_data.get("value")
            if value is not None:
                # Convert numeric value to option string
                index = int(value) - self._first_index
                if 0 <= index < len(self._enum_values):
                    self._attr_current_option = self._enum_values[index]

    async def async_added_to_hass(self) -> None:
        """Handle entity added to Home Assistant."""
        self._update_state_from_param()
        self.async_on_remove(
            self.coordinator.async_add_listener(self._handle_coordinator_update)
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from coordinator."""
        self._update_state_from_param()
        self.async_write_ha_state()

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        if self._is_parameter_locked():
            lock_reason = self._get_lock_reason() or "Parameter is locked"
            _LOGGER.warning(
                "Cannot change locked select %s: %s",
                self.entity_description.key,
                lock_reason,
            )
            self._raise_select_error(f"Select is locked: {lock_reason}")

        try:
            # Convert option to numeric value
            if option in self._enum_values:
                value = self._enum_values.index(option) + self._first_index
            else:
                self._raise_select_error(f"Invalid option: {option}")

            # Dynamic selects must use the parameter index (rmNewParam endpoint),
            # matching the EconetDynamicSwitch pattern. Falling back to set_param
            # routes through newParamName=<id>, which the controller silently
            # ignores, so the UI change never persists (issue #225).
            param_number = self._param.get("number", self._param_id)
            success = await self.api.set_param_by_index(param_number, value)
            if success:
                self._attr_current_option = option
                self.async_write_ha_state()
                _LOGGER.info(
                    "Select %s changed to %s (param_index=%s, value=%s)",
                    self.entity_description.key,
                    option,
                    param_number,
                    value,
                )
            else:
                self._raise_select_error(
                    f"Failed to set {self.entity_description.name}"
                )
        except HomeAssistantError:
            raise
        except Exception as e:
            _LOGGER.error(
                "Failed to change select %s: %s", self.entity_description.key, e
            )
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                translation_key="select_change_failed",
                translation_placeholders={"error": str(e)},
            ) from e

    @staticmethod
    def _raise_select_error(error: str) -> None:
        """Raise a HomeAssistantError with a translated message."""
        raise HomeAssistantError(
            translation_domain=DOMAIN,
            translation_key="select_change_failed",
            translation_placeholders={"error": error},
        )


def should_be_select_entity(param: dict) -> bool:
    """Check if a parameter should be a select entity.

    Select entities are parameters with 3+ enum values,
    or 2 values that are NOT On/Off type.
    """
    if "enum" not in param:
        return False

    enum_data = param.get("enum", {})
    values = enum_data.get("values", [])

    # Filter out empty values
    non_empty_values = [v for v in values if v]

    # Must have at least 2 options
    if len(non_empty_values) < 2:
        return False

    # If 3+ options, it's definitely a select
    if len(non_empty_values) >= 3:
        return True

    # If exactly 2 options, check if NOT On/Off type (those are switches)
    if len(non_empty_values) == 2:
        values_upper = [v.upper() for v in non_empty_values]
        on_off_patterns = [
            {"OFF", "ON"},
            {"0", "1"},
            {"FALSE", "TRUE"},
            {"NO", "YES"},
            {"DISABLED", "ENABLED"},
        ]

        for pattern in on_off_patterns:
            if set(values_upper) == pattern:
                return False  # It's a switch, not a select

        # Check for empty + something pattern (calibration toggle = switch)
        if values[0] == "" and values[1]:
            return False

        # 2 options that are not On/Off = select
        return True

    return False


def create_dynamic_selects(
    coordinator: EconetDataCoordinator,
    api: Econet300Api,
) -> list[SelectEntity]:
    """Create dynamic select entities from mergedData."""
    entities: list[SelectEntity] = []
    key_counts: dict[str, int] = {}  # Track how many times each key has been used

    if coordinator.data is None:
        _LOGGER.debug("No coordinator data for dynamic selects")
        return entities

    merged_data = coordinator.data.get("mergedData")
    if not merged_data:
        _LOGGER.debug("No mergedData for dynamic selects")
        return entities

    parameters = merged_data.get("parameters", {})
    _LOGGER.debug("Creating dynamic selects from %d parameters", len(parameters))

    # The heater-mode parameter is exposed by the static select.heater_mode
    # entity (issue #235); skip it here so we do not emit a duplicate dynamic
    # select that would shadow the canonical entity.
    heater_param = find_heater_mode_param(merged_data)
    heater_param_id = id(heater_param) if heater_param is not None else None
    heater_param_number = (
        heater_param.get("number", heater_param.get("index"))
        if heater_param is not None
        else None
    )

    def _is_heater_mode_param(param: dict) -> bool:
        """Return True when param is the heater-mode param handled statically."""
        return heater_param is not None and (
            id(param) == heater_param_id
            or param.get("number", param.get("index")) == heater_param_number
        )

    # First pass: count duplicates to know which keys need numbering
    key_totals: dict[str, int] = {}
    for param_id, param in parameters.items():
        if not should_be_select_entity(param) or _is_heater_mode_param(param):
            continue
        param_name = param.get("name", f"Parameter {param_id}")
        base_key = param.get("key") or camel_to_snake(param_name)
        key_totals[base_key] = key_totals.get(base_key, 0) + 1

    for param_id, param in parameters.items():
        if not should_be_select_entity(param):
            continue
        if _is_heater_mode_param(param):
            _LOGGER.debug(
                "Skipping dynamic select for heater-mode param %s (handled by "
                "static select.heater_mode)",
                param_id,
            )
            continue

        # Check for mixer-related entities and skip non-existent mixers
        param_name = param.get("name", f"Parameter {param_id}")
        param_key = param.get("key", f"param_{param_id}")

        # Check if mixer-related and if mixer exists
        if "mixer" in param_name.lower() or "mixer" in param_key.lower():
            mixer_match = re.search(r"mixer\s*(\d+)", param_name.lower())
            if mixer_match:
                mixer_num = int(mixer_match.group(1))
                if not mixer_exists(coordinator.data, mixer_num):
                    _LOGGER.debug(
                        "Skipping select %s - mixer %d not connected",
                        param_name,
                        mixer_num,
                    )
                    continue

        # Check if ecoSTER-related and if ecoSTER panel is connected
        if is_ecoster_related(param):
            if not ecoster_exists(coordinator.data):
                _LOGGER.debug(
                    "Skipping select %s - ecoSTER panel not connected",
                    param_name,
                )
                continue

        # Create entity key - handle duplicates with meaningful suffixes
        base_key = param.get("key") or camel_to_snake(param_name)
        description = param.get("description", "")

        # Only add suffixes if there are duplicates
        if key_totals.get(base_key, 1) > 1:
            key_counts[base_key] = key_counts.get(base_key, 0) + 1
            sequence_num = key_counts[base_key]

            # For mixer-related duplicates, validate mixer exists before creating
            # Check for keywords that indicate mixer-related parameters
            desc_lower = description.lower() if description else ""
            is_mixer_related = any(kw in desc_lower for kw in MIXER_RELATED_KEYWORDS)
            if is_mixer_related:
                if not mixer_exists(coordinator.data, sequence_num):
                    _LOGGER.debug(
                        "Skipping select %s (Mixer %d) - mixer not connected",
                        param_name,
                        sequence_num,
                    )
                    continue

            entity_key = get_duplicate_entity_key(base_key, sequence_num, description)
            display_name = get_duplicate_display_name(
                param_name, sequence_num, description
            )
        else:
            sequence_num = None
            entity_key = base_key
            display_name = param_name

        entity_description = SelectEntityDescription(
            key=entity_key,
            name=display_name,
            translation_key=entity_key,
        )

        entity = EconetDynamicSelect(
            entity_description,
            coordinator,
            api,
            param_id,
            param,
            sequence_num,
        )

        entities.append(entity)
        _LOGGER.debug(
            "Created dynamic select: %s (param_id=%s, values=%s)",
            display_name,
            param_id,
            param.get("enum", {}).get("values", []),
        )

    return entities


def get_select_option_name(select_key: str, numeric_value: int) -> str | None:
    """Convert numeric value to option name for any select entity."""
    values_dict = SELECT_KEY_VALUES.get(select_key, {})
    return values_dict.get(numeric_value)


def get_select_option_value(select_key: str, option_name: str) -> int | None:
    """Convert option name to numeric value for any select entity."""
    values_dict = SELECT_KEY_VALUES.get(select_key, {})
    for value, name in values_dict.items():
        if name == option_name:
            return value
    return None


# Legacy functions for backward compatibility
def get_heater_mode_name(numeric_value: int) -> str | None:
    """Convert numeric heater mode value to option name."""
    return get_select_option_name("heaterMode", numeric_value)


def get_heater_mode_value(option_name: str) -> int | None:
    """Convert option name to numeric heater mode value for API."""
    return get_select_option_value("heaterMode", option_name)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the select platform."""
    _LOGGER.debug("Setting up select platform for entry: %s", config_entry.entry_id)

    # Check if DOMAIN data exists
    if DOMAIN not in hass.data:
        _LOGGER.error("DOMAIN %s not found in hass.data", DOMAIN)
        return

    # Check if entry data exists
    if config_entry.entry_id not in hass.data[DOMAIN]:
        _LOGGER.error(
            "Entry %s not found in hass.data[%s]", config_entry.entry_id, DOMAIN
        )
        return

    entry_data = hass.data[DOMAIN][config_entry.entry_id]

    # Check if required services exist
    if SERVICE_COORDINATOR not in entry_data:
        _LOGGER.error("SERVICE_COORDINATOR not found in entry data")
        return

    if SERVICE_API not in entry_data:
        _LOGGER.error("SERVICE_API not found in entry data")
        return

    coordinator = entry_data[SERVICE_COORDINATOR]
    api = entry_data[SERVICE_API]

    _LOGGER.debug("Successfully retrieved coordinator and API")

    # Create select entities based on available configurations
    entities: list[SelectEntity] = []

    # Create static select entities (heaterMode, etc.)
    sys_params = (coordinator.data or {}).get("sysParams") or {}
    controller_id = sys_params.get("controllerID")
    merged_data = (coordinator.data or {}).get("mergedData")
    heater_param = find_heater_mode_param(merged_data)
    if heater_param is not None:
        _LOGGER.debug(
            "Resolved heater_mode param from mergedData: number=%s name=%s",
            heater_param.get("number", heater_param.get("index")),
            heater_param.get("name"),
        )
    for select_key in SELECT_KEY_POST_INDEX:
        # disable-unsupported-heater-mode
        # On this ecoMAX360i, the generic upstream heaterMode write returns API failure.
        # Do not expose it; Mode DHW/other editParams remain available.
        if select_key == "heaterMode" and is_ecomax360i_controller(controller_id):
            _LOGGER.info(
                "Skipping unsupported static heaterMode control for ecoMAX360i"
            )
            continue
        _LOGGER.debug("Creating select entity: %s", select_key)
        # Convert camelCase to snake_case for entity key
        entity_key = camel_to_snake(select_key)

        entity_description = SelectEntityDescription(
            key=entity_key,
            translation_key=entity_key,
            # Icon will be handled by Home Assistant icon translations via icons.json
        )

        # heaterMode resolves its write ID/options from mergedData when
        # available; other static selects keep the hardcoded fallback.
        merged_param = heater_param if select_key == "heaterMode" else None
        entity = EconetSelect(
            entity_description, coordinator, api, select_key, merged_param
        )
        entities.append(entity)
        _LOGGER.debug("Created select entity: %s", select_key)

    _LOGGER.info("Created %d static select entities", len(entities))

    # Create dynamic select entities from mergedData
    dynamic_selects = create_dynamic_selects(coordinator, api)
    entities.extend(dynamic_selects)
    _LOGGER.info("Created %d dynamic select entities", len(dynamic_selects))

    entities.extend(_create_edit_param_selects(coordinator, api))

    _LOGGER.info("Adding %d total select entities", len(entities))
    async_add_entities(entities)


# =============================================================================
# Local editParams select entities (preserve uid-edit_<pid>)
# =============================================================================
class EditParamSelect(CoordinatorEntity[EconetDataCoordinator], SelectEntity):
    """Editable discrete parameter from editParams."""

    _attr_entity_category = EntityCategory.CONFIG

    def __init__(
        self, coordinator: EconetDataCoordinator, api: Econet300Api, pid: str
    ) -> None:
        """Initialize the editable select entity for the given parameter id."""
        super().__init__(coordinator)
        self._api = api
        self._pid = str(pid)

        info = (coordinator.data or {}).get("editParamCatalog", {}).get(self._pid, {})
        pname = info.get("name", f"Param {self._pid}")
        self._attr_name = f"{pname} ({self._pid})"

        self._attr_device_info = _device_info(api)

        options = info.get("options") or []
        self._attr_options = [str(o) for o in options]

    @property
    def unique_id(self) -> str | None:
        """Return the stable unique id preserving the legacy uid-edit_ scheme."""
        return f"{self._api.uid}-edit_{self._pid}"

    @property
    def current_option(self) -> str | None:
        """Return the current parameter value as a string option."""
        info = (
            (self.coordinator.data or {}).get("editParamCatalog", {}).get(self._pid, {})
        )
        val = info.get("value")
        if val is None:
            return None
        try:
            sval = str(int(val))
        except (TypeError, ValueError):
            return None
        return sval if sval in (self.options or []) else None

    @property
    def available(self) -> bool:
        """Return True when data is fresh and the parameter is in the catalog."""
        data = self.coordinator.data or {}
        health = data.get("_health") or {}
        return (not bool(health.get("stale"))) and self._pid in data.get(
            "editParamCatalog", {}
        )

    async def async_select_option(self, option: str) -> None:
        """Write the selected option back to the controller."""
        try:
            value = int(option)
        except ValueError as e:
            raise HomeAssistantError(
                f"Invalid option '{option}' for param {self._pid}"
            ) from e

        ok = await self._api.set_param(self._pid, value)
        if not ok:
            raise HomeAssistantError(f"Failed to set param {self._pid} to {value}")

        self.coordinator.force_edit_params_refresh()
        await self.coordinator.async_request_refresh()

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return the main ecoNET300 device info for this entity."""
        return self._attr_device_info


def _create_edit_param_selects(
    coordinator: EconetDataCoordinator, api: Econet300Api
) -> list[SelectEntity]:
    catalog: dict[str, dict[str, Any]] = (coordinator.data or {}).get(
        "editParamCatalog", {}
    ) or {}
    entities: list[SelectEntity] = []
    for pid, info in catalog.items():
        if info.get("kind") != "select":
            continue
        entities.append(EditParamSelect(coordinator, api, pid))
    _LOGGER.info("Adding %d editable Select entities from editParams", len(entities))
    return entities
