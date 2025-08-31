"""Select entities for ecoNET300 integration."""

import logging
from typing import Any

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import Econet300Api
from .common import EconetDataCoordinator
from .const import HEATER_MODE_NAMES, HEATER_MODE_PARAM_INDEX, HEATER_MODE_VALUES
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
    ):
        """Initialize a new ecoNET select entity."""
        self.entity_description = entity_description
        self.api = api
        self._attr_current_option = None
        super().__init__(coordinator, api)

    @property
    def options(self) -> list[str]:
        """Return the available options."""
        return list(HEATER_MODE_VALUES.keys())

    @property
    def current_option(self) -> str | None:
        """Return the currently selected option."""
        return self._attr_current_option

    def _sync_state(self, value: Any) -> None:
        """Synchronize the state of the select entity."""
        # For heater mode, we need to get the value from the parameter index 55
        # The value comes from the coordinator data
        if self.entity_description.key == "heater_mode":
            # Get the value from the parameter index 55
            heater_mode_value = self.coordinator.data.get("paramsEdits", {}).get(
                HEATER_MODE_PARAM_INDEX
            )

            if heater_mode_value is not None:
                # Extract the actual value if it's a dict
                if isinstance(heater_mode_value, dict) and "value" in heater_mode_value:
                    numeric_value = heater_mode_value["value"]
                else:
                    numeric_value = heater_mode_value

                # Map the numeric value to the option name
                if numeric_value in HEATER_MODE_NAMES:
                    self._attr_current_option = HEATER_MODE_NAMES[numeric_value]
                else:
                    self._attr_current_option = None
                    _LOGGER.warning("Unknown heater mode value: %s", numeric_value)
            else:
                self._attr_current_option = None
                _LOGGER.debug("Heater mode value not found in coordinator data")
        # Handle other select entities if needed
        elif value is not None and value in HEATER_MODE_NAMES:
            self._attr_current_option = HEATER_MODE_NAMES[value]
        else:
            self._attr_current_option = None

        self.async_write_ha_state()

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        try:
            if option not in HEATER_MODE_VALUES:
                self._raise_heater_mode_error(f"Invalid option: {option}")

            # Get the numeric value for the selected option
            value = HEATER_MODE_VALUES[option]

            # Use the parameter index (55) to set the value
            success = await self.api.set_param(HEATER_MODE_PARAM_INDEX, value)

            if success:
                self._attr_current_option = option
                self.async_write_ha_state()
                _LOGGER.info("Heater mode changed to: %s", option)
            else:
                _LOGGER.error(
                    "Failed to change heater mode to %s - API returned failure", option
                )
                self._raise_heater_mode_error(
                    f"Failed to change heater mode to {option}"
                )

        except Exception as e:
            _LOGGER.error("Failed to change heater mode to %s: %s", option, e)
            raise HeaterModeSelectError(
                f"Failed to change heater mode to {option}"
            ) from e

    @staticmethod
    def _raise_heater_mode_error(message: str) -> None:
        """Raise a HeaterModeSelectError with the given message."""
        raise HeaterModeSelectError(message)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the select platform."""
    coordinator = hass.data[config_entry.entry_id]["coordinator"]
    api = hass.data[config_entry.entry_id]["api"]

    # Create heater mode select entity
    heater_mode_description = SelectEntityDescription(
        key="heater_mode",
        translation_key="heater_mode",
        icon="mdi:thermostat",
    )

    entities = [
        EconetSelect(heater_mode_description, coordinator, api),
    ]

    async_add_entities(entities)
