"""Switch for Econet300."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity, SwitchEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .common import Econet300Api, EconetDataCoordinator
from .const import DOMAIN, SERVICE_API, SERVICE_COORDINATOR
from .entity import EconetEntity

_LOGGER = logging.getLogger(__name__)


class BoilerControlError(HomeAssistantError):
    """Raised when boiler control fails."""


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

    def _sync_state(self, value: Any) -> None:
        """Synchronize the state of the switch entity."""
        # Use mode parameter: 0 = OFF, anything else = ON
        mode_value = self.coordinator.data.get("mode", 0)
        self._attr_is_on = mode_value != 0
        self.async_write_ha_state()

    def update_state_from_mode(self, mode_value: int) -> None:
        """Update switch state based on mode value."""
        self._attr_is_on = mode_value != 0
        self.async_write_ha_state()

    @staticmethod
    def _raise_boiler_control_error(message: str) -> None:
        raise BoilerControlError(message)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the switch on."""
        try:
            # Use BOILER_CONTROL parameter: set to 1 to turn on
            success = await self.api.set_param("BOILER_CONTROL", 1)
            if success:
                self._attr_is_on = True
                self.async_write_ha_state()
                _LOGGER.info("Boiler turned ON")
            else:
                _LOGGER.error("Failed to turn boiler ON - API returned failure")
                EconetSwitch._raise_boiler_control_error("Failed to turn boiler ON")
        except Exception as e:
            _LOGGER.error("Failed to turn boiler ON: %s", e)
            raise

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the switch off."""
        try:
            # Use BOILER_CONTROL parameter: set to 0 to turn off
            success = await self.api.set_param("BOILER_CONTROL", 0)
            if success:
                self._attr_is_on = False
                self.async_write_ha_state()
                _LOGGER.info("Boiler turned OFF")
            else:
                _LOGGER.error("Failed to turn boiler OFF - API returned failure")
                EconetSwitch._raise_boiler_control_error("Failed to turn boiler OFF")
        except Exception as e:
            _LOGGER.error("Failed to turn boiler OFF: %s", e)
            raise


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

    # Create boiler control switch
    boiler_switch = create_boiler_switch(coordinator, api)

    # Add the switch entity
    async_add_entities([boiler_switch])

    # Update the switch state based on current data
    if coordinator.data and "mode" in coordinator.data:
        mode_value = coordinator.data["mode"]
        boiler_switch.update_state_from_mode(mode_value)
