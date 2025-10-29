"""Select entities for ecoNET300 integration."""

import logging
from typing import Any

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import Econet300Api
from .common import EconetDataCoordinator, skip_edit_params, skip_params_edits
from .const import (
    CIRCUIT1_WORK_STATE_VALUES,
    DOMAIN,
    HEATER_MODE_PARAM_INDEX,
    HEATER_MODE_VALUES,
    SELECT_MAP_KEY,
    SERVICE_API,
    SERVICE_COORDINATOR,
)
from .entity import EconetEntity

_LOGGER = logging.getLogger(__name__)


class HeaterModeSelectError(HomeAssistantError):
    """Raised when heater mode selection fails."""


class EconetSelect(EconetEntity, SelectEntity):
    """Represents an ecoNET select entity."""

    entity_description: SelectEntityDescription

    def __init__(
        self,
        entity_description: SelectEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
        param_index: str,
        value_mapping: dict[int, str],
    ):
        """Initialize a new ecoNET select entity."""
        self.entity_description = entity_description
        self.api = api
        self._param_index = param_index
        self._value_mapping = value_mapping
        self._attr_current_option = None
        super().__init__(coordinator, api)

    @property
    def options(self) -> list[str]:
        """Return the available options."""
        return list(self._value_mapping.values())

    @property
    def current_option(self) -> str | None:
        """Return the current option."""
        return self._attr_current_option

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return entity specific state attributes."""
        current_option = self._attr_current_option
        numeric_value = (
            self._get_numeric_value(current_option) if current_option else None
        )

        return {
            "numeric_value": numeric_value,
            "available_options": list(self._value_mapping.values()),
            "api_parameter": self._param_index,
        }

    def _get_numeric_value(self, option_name: str) -> int | None:
        """Convert option name to numeric value for API."""
        for value, name in self._value_mapping.items():
            if name == option_name:
                return value
        return None

    def _get_option_name(self, numeric_value: int) -> str | None:
        """Convert numeric value to option name."""
        return self._value_mapping.get(numeric_value)

    def _sync_state(self, value: Any) -> None:
        """Synchronize the state of the select entity."""
        # Value is already extracted from the appropriate data source by the base entity class
        # It could be from editParams or paramsEdits depending on controller type

        if value is not None:
            # Extract the actual value if it's a dict
            if isinstance(value, dict) and "value" in value:
                numeric_value = value["value"]
            else:
                numeric_value = value

            # Map the numeric value to the option name using our value mapping
            if isinstance(numeric_value, (int, float)):
                option_name = self._get_option_name(int(numeric_value))
                if option_name is not None:
                    self._attr_current_option = option_name
                else:
                    self._attr_current_option = None
                    _LOGGER.warning(
                        "Unknown value %s for select entity %s",
                        numeric_value,
                        self.entity_description.translation_key,
                    )
            else:
                self._attr_current_option = None
                _LOGGER.warning(
                    "Invalid value type %s for select entity %s",
                    type(numeric_value),
                    self.entity_description.translation_key,
                )
        else:
            self._attr_current_option = None
            _LOGGER.debug(
                "Value not found for select entity %s",
                self.entity_description.translation_key,
            )

        self.async_write_ha_state()

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        try:
            # Get the numeric value for the selected option
            value = self._get_numeric_value(option)
            if value is None:
                self._raise_select_error(f"Invalid option: {option}")

            # Use the parameter index to set the value
            success = await self.api.set_param(self._param_index, value)

            if success:
                # Update the current option
                old_option = self._attr_current_option
                self._attr_current_option = option

                # Log the change with context for better logbook entries
                _LOGGER.info(
                    "%s changed from '%s' to '%s' (API value: %d)",
                    self.entity_description.translation_key,
                    old_option or "unknown",
                    option,
                    value,
                )

                # Write the state change to trigger Home Assistant's state change logging
                self.async_write_ha_state()

                # Additional context for debugging
                _LOGGER.debug(
                    "%s state updated: %s -> %s (API value: %d)",
                    self.entity_description.translation_key,
                    old_option,
                    option,
                    value,
                )
            else:
                _LOGGER.error(
                    "Failed to change %s to %s - API returned failure",
                    self.entity_description.translation_key,
                    option,
                )
                self._raise_select_error(
                    f"Failed to change {self.entity_description.translation_key} to {option}"
                )

        except Exception as e:
            _LOGGER.error(
                "Failed to change %s to %s: %s",
                self.entity_description.translation_key,
                option,
                e,
            )
            raise HeaterModeSelectError(
                f"Failed to change {self.entity_description.translation_key} to {option}"
            ) from e

    @staticmethod
    def _raise_select_error(message: str) -> None:
        """Raise a HeaterModeSelectError with the given message."""
        raise HeaterModeSelectError(message)


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
    _LOGGER.debug("Entry data keys: %s", list(entry_data.keys()))

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

    # Get controller ID to determine which select entities to create
    sys_params = coordinator.data.get("sysParams", {})
    controller_id = sys_params.get("controllerID", "_default")
    _LOGGER.info("Setting up select entities for controller: %s", controller_id)

    # Get select mapping for this controller
    select_map = SELECT_MAP_KEY.get(controller_id, SELECT_MAP_KEY["_default"])

    entities = []
    for param_index, (entity_key, value_mapping) in select_map.items():
        # Check if parameter exists in coordinator data
        has_params_edits = not skip_params_edits(sys_params)
        has_edit_params = not skip_edit_params(sys_params)

        # Check if data exists for this parameter
        param_exists = False
        if has_edit_params:
            edit_params = coordinator.data.get("editParams", {})
            param_exists = param_index in edit_params
        elif has_params_edits:
            params_edits = coordinator.data.get("paramsEdits", {})
            param_exists = param_index in params_edits

        if not param_exists:
            _LOGGER.debug(
                "Parameter %s not found in coordinator data, skipping select entity %s",
                param_index,
                entity_key,
            )
            continue

        # Create select entity description
        # Use param_index as key so base entity can find data in coordinator
        entity_description = SelectEntityDescription(
            key=param_index,
            translation_key=entity_key,
            icon="mdi:dip-switch" if "work_state" in entity_key else "mdi:thermostat",
        )

        # Create select entity
        entities.append(
            EconetSelect(
                entity_description, coordinator, api, param_index, value_mapping
            )
        )
        _LOGGER.debug("Created select entity: %s (param: %s)", entity_key, param_index)

    _LOGGER.info("Adding %d select entities", len(entities))
    async_add_entities(entities)
