"""Water heater entities for ecoNET300 integration.

This module implements water heater entities for HUW (Hot Water) control.
"""

import logging
from typing import Any

from homeassistant.components.water_heater import (
    WaterHeaterEntity,
    WaterHeaterEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import Econet300Api
from .common import EconetDataCoordinator
from .const import (
    DOMAIN,
    HUW_CATEGORY_NAME,
    HUW_NAME_PATTERN,
    SERVICE_API,
    SERVICE_COORDINATOR,
)
from .entity import EconetEntity

_LOGGER = logging.getLogger(__name__)


class EconetWaterHeater(EconetEntity, WaterHeaterEntity):
    """Represents an ecoNET water heater entity for HUW control."""

    entity_description: WaterHeaterEntityDescription

    def __init__(
        self,
        entity_description: WaterHeaterEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
    ):
        """Initialize a new ecoNET water heater entity."""
        self.entity_description = entity_description
        self.api = api
        self._attr_temperature_unit = UnitOfTemperature.CELSIUS
        self._attr_current_temperature = None
        self._attr_target_temperature = None
        self._attr_min_temp = 20.0  # Default minimum
        self._attr_max_temp = 55.0  # Default maximum
        self._attr_operation_list: list[str] = ["off", "on"]
        self._attr_current_operation = "off"
        # Cache parameter ID found dynamically
        self._huw_preset_temp_param_id: str | None = None
        super().__init__(coordinator, api)

    def _find_all_huw_parameters(self, merged_parameters: dict) -> dict[str, dict]:
        """Find all HUW parameters from merged_parameters by category and name.

        Searches for all parameters where name contains "HUW" (like SQL LIKE '%HUW%').
        Only uses parameters from merged_parameters (with category field from rmStructure).

        Args:
            merged_parameters: Dictionary of all parameters (with category field from merged data)

        Returns:
            Dictionary of HUW parameter IDs to parameter data

        """
        huw_parameters: dict[str, dict] = {}

        for param_id, param_data in merged_parameters.items():
            if not isinstance(param_data, dict):
                continue

            # Only use parameters from HUW category (from merged_parameters)
            param_category = param_data.get("category", "")
            if (
                not param_category
                or HUW_CATEGORY_NAME.lower() not in param_category.lower()
            ):
                continue

            # Check if parameter name contains HUW_NAME_PATTERN (like %HUW%)
            param_name = param_data.get("name", "").upper()
            if HUW_NAME_PATTERN in param_name:
                huw_parameters[param_id] = param_data
                _LOGGER.debug(
                    "Found HUW parameter '%s' (ID: %s) in category '%s'",
                    param_data.get("name", "Unknown"),
                    param_id,
                    param_data.get("category", "Unknown"),
                )

        return huw_parameters

    def _find_huw_parameter(
        self, merged_parameters: dict, search_patterns: list[str]
    ) -> str | None:
        """Find specific HUW parameter ID from merged_parameters by category and name pattern.

        Uses _find_all_huw_parameters to get all HUW parameters, then searches for
        a specific one matching the search patterns.

        Args:
            merged_parameters: Dictionary of all parameters (with category field from merged data)
            search_patterns: List of strings to search for in parameter name/key
                            (e.g., ["HUW preset", "huw_preset_temperature"])

        Returns:
            Parameter ID (string) if found, None otherwise

        """
        # Get all HUW parameters first
        huw_parameters = self._find_all_huw_parameters(merged_parameters)

        # Search for specific parameter matching patterns
        for param_id, param_data in huw_parameters.items():
            param_name = param_data.get("name", "").lower()
            param_key = param_data.get("key", "").lower()

            for pattern in search_patterns:
                pattern_lower = pattern.lower()
                if pattern_lower in param_name or pattern_lower in param_key:
                    _LOGGER.debug(
                        "Found HUW parameter '%s' (ID: %s) matching pattern '%s'",
                        param_data.get("name", "Unknown"),
                        param_id,
                        pattern,
                    )
                    return str(param_id)

        return None

    @property
    def current_temperature(self) -> float | None:
        """Return the current temperature."""
        if self.coordinator.data is None:
            return None

        reg_params = self.coordinator.data.get("regParams", {})
        temp_cwu = reg_params.get("tempCWU")
        return float(temp_cwu) if temp_cwu is not None else None

    @property
    def target_temperature(self) -> float | None:
        """Return the target temperature."""
        return self._attr_target_temperature

    @property
    def min_temp(self) -> float:
        """Return the minimum temperature."""
        return self._attr_min_temp

    @property
    def max_temp(self) -> float:
        """Return the maximum temperature."""
        return self._attr_max_temp

    @property
    def operation_list(self) -> list[str]:
        """Return the list of available operation modes."""
        return self._attr_operation_list

    @property
    def current_operation(self) -> str | None:
        """Return the current operation mode."""
        if self.coordinator.data is None:
            return None

        reg_params = self.coordinator.data.get("regParams", {})
        pump_cwu_works = reg_params.get("pumpCWUWorks", 0)
        return "on" if pump_cwu_works else "off"

    def _sync_state(self, value: dict | float | None) -> None:
        """Synchronize the state of the water heater entity."""
        _LOGGER.debug("Water heater _sync_state called with value: %s", value)

        # Always update from merged data if available
        if self.coordinator.data is not None:
            merged_data = self.coordinator.data.get("mergedData", {})
            merged_parameters = merged_data.get("parameters", {})

            # Find HUW preset temperature parameter dynamically if not cached
            if not self._huw_preset_temp_param_id:
                self._huw_preset_temp_param_id = self._find_huw_parameter(
                    merged_parameters,
                    ["HUW preset temperature", "huw_preset_temperature", "huw preset"],
                )

            # Get target temperature and min/max limits from HUW preset temperature parameter
            if self._huw_preset_temp_param_id:
                preset_param = merged_parameters.get(self._huw_preset_temp_param_id, {})
                if isinstance(preset_param, dict):
                    # Get target temperature value
                    if "value" in preset_param:
                        preset_value = preset_param.get("value")
                        if preset_value is not None:
                            self._attr_target_temperature = float(preset_value)

                    # Get min/max limits directly from the parameter's minv/maxv fields
                    if "minv" in preset_param:
                        min_value = preset_param.get("minv")
                        if min_value is not None:
                            self._attr_min_temp = float(min_value)
                    if "maxv" in preset_param:
                        max_value = preset_param.get("maxv")
                        if max_value is not None:
                            self._attr_max_temp = float(max_value)

        # Handle direct value if provided
        if value is not None:
            if isinstance(value, dict):
                target_temp = value.get("value")
                if target_temp is not None:
                    self._attr_target_temperature = float(target_temp)
            elif isinstance(value, (int, float)):
                self._attr_target_temperature = float(value)

        self.async_write_ha_state()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug("Water heater coordinator update")

        if self.coordinator.data is None:
            return

        # Read from merged data
        merged_data = self.coordinator.data.get("mergedData", {})
        merged_parameters = merged_data.get("parameters", {})

        # Find HUW preset temperature parameter if not cached
        if not self._huw_preset_temp_param_id:
            self._huw_preset_temp_param_id = self._find_huw_parameter(
                merged_parameters,
                ["HUW preset temperature", "huw_preset_temperature", "huw preset"],
            )

        if self._huw_preset_temp_param_id:
            preset_param = merged_parameters.get(self._huw_preset_temp_param_id, {})
            if isinstance(preset_param, dict):
                self._sync_state(preset_param)
            else:
                # Fallback: try to get value directly
                value = (
                    preset_param.get("value")
                    if isinstance(preset_param, dict)
                    else preset_param
                )
                self._sync_state(value)
        else:
            # No HUW preset parameter found, still try to sync with None
            self._sync_state(None)

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Set the target temperature."""
        temperature = kwargs.get("temperature")
        if temperature is None:
            _LOGGER.error("Temperature not provided")
            return

        _LOGGER.debug("Setting water heater temperature to: %s", temperature)

        # Validate temperature range
        if temperature < self.min_temp or temperature > self.max_temp:
            _LOGGER.warning(
                "Temperature %s is outside valid range [%s, %s]",
                temperature,
                self.min_temp,
                self.max_temp,
            )
            return

        # Find HUW preset temperature parameter if not cached
        if not self._huw_preset_temp_param_id and self.coordinator.data is not None:
            merged_data = self.coordinator.data.get("mergedData", {})
            merged_parameters = merged_data.get("parameters", {})
            self._huw_preset_temp_param_id = self._find_huw_parameter(
                merged_parameters,
                ["HUW preset temperature", "huw_preset_temperature", "huw preset"],
            )

        if not self._huw_preset_temp_param_id:
            _LOGGER.error("HUW preset temperature parameter not found")
            return

        # Set HUW preset temperature parameter
        success = await self.api.set_param(
            self._huw_preset_temp_param_id, int(temperature)
        )
        if success:
            self._attr_target_temperature = temperature
            _LOGGER.info("Water heater target temperature set to %s°C", temperature)
            self.async_write_ha_state()
        else:
            _LOGGER.error("Failed to set water heater temperature")

    async def async_set_operation_mode(self, operation_mode: str) -> None:
        """Set the operation mode."""
        _LOGGER.debug("Setting water heater operation mode to: %s", operation_mode)
        # Note: Operation mode is derived from pump status, so we don't set it directly
        # This could be enhanced to control pump mode if needed
        _LOGGER.info("Operation mode change requested: %s", operation_mode)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the water heater platform."""
    _LOGGER.debug(
        "Setting up water heater platform for entry: %s", config_entry.entry_id
    )

    if DOMAIN not in hass.data:
        _LOGGER.error("DOMAIN %s not found in hass.data", DOMAIN)
        return

    if config_entry.entry_id not in hass.data[DOMAIN]:
        _LOGGER.error(
            "Entry %s not found in hass.data[%s]",
            config_entry.entry_id,
            DOMAIN,
        )
        return

    entry_data = hass.data[DOMAIN][config_entry.entry_id]

    if SERVICE_COORDINATOR not in entry_data:
        _LOGGER.error("SERVICE_COORDINATOR not found in entry data")
        return

    if SERVICE_API not in entry_data:
        _LOGGER.error("SERVICE_API not found in entry data")
        return

    coordinator = entry_data[SERVICE_COORDINATOR]
    api = entry_data[SERVICE_API]

    _LOGGER.debug("Successfully retrieved coordinator and API")

    # Create water heater entity
    entity_description = WaterHeaterEntityDescription(
        key="huw_water_heater",
        translation_key="huw_water_heater",
    )

    entity = EconetWaterHeater(entity_description, coordinator, api)
    async_add_entities([entity])
    _LOGGER.info("Added water heater entity")
