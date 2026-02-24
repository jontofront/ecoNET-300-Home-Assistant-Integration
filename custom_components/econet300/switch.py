"""Switch for Econet300."""

from __future__ import annotations

import logging
import re
import time
from typing import Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_OFF, EntityCategory
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .common import Econet300Api, EconetDataCoordinator
from .common_functions import (
    camel_to_snake,
    get_duplicate_display_name,
    get_duplicate_entity_key,
    get_validated_entity_component,
    mixer_exists,
)
from .const import (
    BOILER_CONTROL,
    DOMAIN,
    MIXER_RELATED_KEYWORDS,
    OPERATION_MODE_NAMES,
    SERVICE_API,
    SERVICE_COORDINATOR,
)
from .entity import EconetEntity, get_device_info_for_component

_LOGGER = logging.getLogger(__name__)


class BoilerControlError(HomeAssistantError):
    """Raised when boiler control fails."""

    def __init__(self, error: str) -> None:
        """Initialize the error."""
        super().__init__(
            translation_domain=DOMAIN,
            translation_key="boiler_control_failed",
            translation_placeholders={"error": error},
        )


class EconetSwitch(EconetEntity, SwitchEntity):
    """Represents an ecoNET switch entity."""

    entity_description: SwitchEntityDescription

    def __init__(
        self,
        entity_description: SwitchEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
    ):
        """Initialize a new ecoNET switch entity."""
        self.entity_description = entity_description
        self.api = api
        self._attr_is_on = False
        super().__init__(coordinator, api)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator.

        Overrides the base class because the boiler switch reads its state
        from regParams["mode"] rather than a key matching entity_description.key.
        Without this override, _lookup_value() returns None for "boiler_control"
        and _sync_state() is never called.
        """
        if self.coordinator.data is None:
            return
        reg_params = self.coordinator.data.get("regParams", {})
        if not isinstance(reg_params, dict):
            return
        mode_value = reg_params.get("mode")
        if mode_value is None:
            return
        self._sync_state(mode_value)

    def _sync_state(self, value: Any) -> None:
        """Synchronize the state of the switch entity.

        Uses OPERATION_MODE_NAMES to resolve the mode value.
        Mode 0 maps to STATE_OFF; any other known mode is considered ON.
        """
        self._attr_is_on = OPERATION_MODE_NAMES.get(value, STATE_OFF) != STATE_OFF
        self.async_write_ha_state()

    @staticmethod
    def _raise_boiler_control_error(error: str) -> None:
        raise BoilerControlError(error)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        try:
            # Use BOILER_CONTROL parameter: set to 1 to turn on
            success = await self.api.set_param(BOILER_CONTROL, 1)
            if not success:
                EconetSwitch._raise_boiler_control_error("Failed to turn boiler ON")
            self._attr_is_on = True
            self.async_write_ha_state()
            _LOGGER.info("Boiler turned ON")
        except Exception as e:
            _LOGGER.error("Failed to turn boiler ON: %s", e)
            raise

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the boiler off."""
        try:
            # Use BOILER_CONTROL parameter: set to 0 to turn off
            success = await self.api.set_param(BOILER_CONTROL, 0)
            if not success:
                EconetSwitch._raise_boiler_control_error("Failed to turn boiler OFF")
            self._attr_is_on = False
            self.async_write_ha_state()
            _LOGGER.info("Boiler turned OFF")
        except BoilerControlError:
            raise
        except (OSError, TimeoutError) as e:
            _LOGGER.error("Failed to turn boiler OFF: %s", e)
            EconetSwitch._raise_boiler_control_error(f"Error turning boiler OFF: {e}")
        except Exception as e:
            _LOGGER.error("Failed to turn boiler OFF: %s", e)
            raise


class EconetDynamicSwitch(EconetEntity, SwitchEntity):
    """Represents a dynamic ecoNET switch entity from mergedData."""

    _attr_has_entity_name = True

    @property
    def entity_registry_enabled_default(self) -> bool:
        """Return if entity should be enabled by default.

        CONFIG category entities are disabled by default.
        Switches without category are also disabled (they are config controls).
        """
        entity_category = getattr(self.entity_description, "entity_category", None)
        # Switches are disabled by default unless explicitly not CONFIG
        return entity_category is not None and entity_category != EntityCategory.CONFIG

    def __init__(
        self,
        entity_description: SwitchEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
        param_id: str,
        param: dict,
        sequence_num: int | None = None,
    ):
        """Initialize a new dynamic ecoNET switch entity."""
        super().__init__(coordinator, api)
        self.entity_description = entity_description
        self._param_id = param_id
        self._param = param
        self._attr_is_on = False

        # Track last write time to skip coordinator updates briefly after manual changes
        # This prevents stale API data from reverting local state
        self._last_write_time: float = 0.0
        self._write_cooldown_seconds: float = (
            5.0  # Skip updates for 5 seconds after write
        )

        # Get enum values for on/off mapping
        enum_data = param.get("enum", {})
        self._enum_values = enum_data.get("values", [])
        self._on_value = self._get_on_value()
        self._off_value = self._get_off_value()

        # Set unique ID
        self._attr_unique_id = f"econet300_switch_{param_id}"

        # Determine which component this entity belongs to (with hardware validation)
        param_name = param.get("name", "")
        param_key = param.get("key", "")
        description = param.get("description", "")
        self._component = get_validated_entity_component(
            param_name, param_key, description, sequence_num, coordinator.data
        )

        # Set initial state
        self._update_state_from_param()

    def _get_on_value(self) -> int:
        """Get the numeric value that represents ON."""
        # Usually ON is at index 1, but check for variations
        for i, val in enumerate(self._enum_values):
            if val.upper() in ("ON", "1", "TRUE", "YES", "ENABLED"):
                return i
        return 1 if len(self._enum_values) > 1 else 0

    def _get_off_value(self) -> int:
        """Get the numeric value that represents OFF."""
        # Usually OFF is at index 0
        for i, val in enumerate(self._enum_values):
            if val.upper() in ("OFF", "0", "FALSE", "NO", "DISABLED"):
                return i
        return 0

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
                self._attr_is_on = value == self._on_value

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info based on entity component."""
        return get_device_info_for_component(self._component, self.api)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    @property
    def icon(self) -> str | None:
        """Return icon for entity."""
        # Check if locked
        if self._is_parameter_locked():
            return "mdi:lock"
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes including lock information."""
        attrs: dict[str, Any] = {
            "param_id": self._param_id,
            "enum_values": self._enum_values,
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

    async def async_added_to_hass(self) -> None:
        """Handle entity added to Home Assistant."""
        self._update_state_from_param()
        self.async_on_remove(
            self.coordinator.async_add_listener(self._handle_coordinator_update)
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from coordinator."""
        # Skip updates briefly after a manual write to prevent stale data reverting state
        if time.monotonic() - self._last_write_time < self._write_cooldown_seconds:
            _LOGGER.debug(
                "Skipping coordinator update for %s (within cooldown after write)",
                self.entity_description.key,
            )
            return
        self._update_state_from_param()
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        await self._set_switch_state(turn_on=True)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        await self._set_switch_state(turn_on=False)

    async def _set_switch_state(self, turn_on: bool) -> None:
        """Set switch state (shared logic for turn_on/turn_off)."""
        action = "ON" if turn_on else "OFF"
        target_value = self._on_value if turn_on else self._off_value
        translation_key = (
            "switch_turn_on_failed" if turn_on else "switch_turn_off_failed"
        )

        if self._is_parameter_locked():
            lock_reason = self._get_lock_reason() or "Parameter is locked"
            _LOGGER.warning(
                "Cannot turn %s locked switch %s: %s",
                action,
                self.entity_description.key,
                lock_reason,
            )
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                translation_key=translation_key,
                translation_placeholders={"error": f"Switch is locked: {lock_reason}"},
            )

        param_number = self._param.get("number", self._param_id)
        try:
            success = await self.api.set_param_by_index(param_number, target_value)
        except Exception as e:
            _LOGGER.error(
                "Failed to turn %s switch %s: %s",
                action,
                self.entity_description.key,
                e,
            )
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                translation_key=translation_key,
                translation_placeholders={"error": str(e)},
            ) from e

        if success:
            self._attr_is_on = turn_on
            self._last_write_time = time.monotonic()  # Record write time for cooldown
            self.async_write_ha_state()
            _LOGGER.info("Switch %s turned %s", self.entity_description.key, action)
        else:
            raise HomeAssistantError(
                translation_domain=DOMAIN,
                translation_key=translation_key,
                translation_placeholders={
                    "error": f"Failed to turn {action.lower()} {self.entity_description.name}"
                },
            )


def should_be_switch_entity(param: dict) -> bool:
    """Check if a parameter should be a switch entity.

    Switch entities are parameters with exactly 2 enum values (On/Off).
    """
    if "enum" not in param:
        return False

    enum_data = param.get("enum", {})
    values = enum_data.get("values", [])

    # Must have exactly 2 values
    if len(values) != 2:
        return False

    # Check if it looks like an On/Off switch
    values_upper = [v.upper() for v in values if v]
    on_off_patterns = [
        {"OFF", "ON"},
        {"0", "1"},
        {"FALSE", "TRUE"},
        {"NO", "YES"},
        {"DISABLED", "ENABLED"},
    ]

    for pattern in on_off_patterns:
        if set(values_upper) == pattern:
            return True

    # Also accept if first value is empty and second is something (like calibration toggle)
    if values[0] == "" and values[1]:
        return True

    return False


def create_dynamic_switches(
    coordinator: EconetDataCoordinator,
    api: Econet300Api,
) -> list[SwitchEntity]:
    """Create dynamic switch entities from mergedData."""
    entities: list[SwitchEntity] = []
    key_counts: dict[str, int] = {}  # Track how many times each key has been used

    if coordinator.data is None:
        _LOGGER.debug("No coordinator data for dynamic switches")
        return entities

    merged_data = coordinator.data.get("mergedData")
    if not merged_data:
        _LOGGER.debug("No mergedData for dynamic switches")
        return entities

    parameters = merged_data.get("parameters", {})
    _LOGGER.debug("Creating dynamic switches from %d parameters", len(parameters))

    # First pass: count duplicates to know which keys need numbering
    key_totals: dict[str, int] = {}
    for param_id, param in parameters.items():
        if not should_be_switch_entity(param):
            continue
        param_name = param.get("name", f"Parameter {param_id}")
        base_key = param.get("key") or camel_to_snake(param_name)
        key_totals[base_key] = key_totals.get(base_key, 0) + 1

    for param_id, param in parameters.items():
        if not should_be_switch_entity(param):
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
                        "Skipping switch %s - mixer %d not connected",
                        param_name,
                        mixer_num,
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
                        "Skipping switch %s (Mixer %d) - mixer not connected",
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

        entity_description = SwitchEntityDescription(
            key=entity_key,
            name=display_name,
            translation_key=entity_key,
        )

        entity = EconetDynamicSwitch(
            entity_description,
            coordinator,
            api,
            param_id,
            param,
            sequence_num,
        )

        entities.append(entity)
        _LOGGER.debug(
            "Created dynamic switch: %s (param_id=%s, values=%s)",
            display_name,
            param_id,
            param.get("enum", {}).get("values", []),
        )

    return entities


def create_boiler_switch(
    coordinator: EconetDataCoordinator, api: Econet300Api
) -> EconetSwitch:
    """Create boiler control switch entity."""
    entity_description = SwitchEntityDescription(
        key="boiler_control",
        name="Boiler On/Off",
        translation_key="boiler_control",
    )

    return EconetSwitch(entity_description, coordinator, api)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the switch platform."""
    coordinator: EconetDataCoordinator = hass.data[DOMAIN][entry.entry_id][
        SERVICE_COORDINATOR
    ]
    api: Econet300Api = hass.data[DOMAIN][entry.entry_id][SERVICE_API]

    entities: list[SwitchEntity] = []

    # Create boiler control switch (static)
    # Initial state is synced automatically via _handle_coordinator_update()
    # once the entity is added to Home Assistant.
    entities.append(create_boiler_switch(coordinator, api))
    _LOGGER.info("Created 1 static switch entity (boiler control)")

    # Create dynamic switch entities from mergedData
    dynamic_switches = create_dynamic_switches(coordinator, api)
    entities.extend(dynamic_switches)
    _LOGGER.info("Created %d dynamic switch entities", len(dynamic_switches))

    _LOGGER.info("Adding %d total switch entities", len(entities))
    async_add_entities(entities)
