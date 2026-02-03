"""The ecoNET300 integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall, callback
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.issue_registry import async_delete_issue
import voluptuous as vol

from .api import make_api
from .common import AuthError, EconetDataCoordinator
from .const import DOMAIN, SERVICE_API, SERVICE_COORDINATOR
from .mem_cache import MemCache

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.NUMBER,
    Platform.SWITCH,
    Platform.SELECT,
]

# Service names
SERVICE_RESET_FUEL_METER = "reset_fuel_meter"
SERVICE_CALIBRATE_FUEL_METER = "calibrate_fuel_meter"

# Service schema
SERVICE_CALIBRATE_SCHEMA = vol.Schema(
    {
        vol.Required("value"): vol.Coerce(float),
    }
)

# Required for polling integrations
PARALLEL_UPDATES = 1


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Econet300 Integration from a config entry."""

    hass.data.setdefault(DOMAIN, {})

    cache = MemCache()

    try:
        data: dict[str, str] = dict(entry.data)
        api = await make_api(hass, cache, data)

        coordinator = EconetDataCoordinator(hass, api, entry)
        await coordinator.async_config_entry_first_refresh()

        hass.data[DOMAIN][entry.entry_id] = {
            SERVICE_API: api,
            SERVICE_COORDINATOR: coordinator,
        }
    except AuthError as auth_error:
        raise ConfigEntryAuthFailed("Client not authenticated") from auth_error
    except TimeoutError as timeout_error:
        raise ConfigEntryNotReady("Target not found") from timeout_error
    else:
        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

        # Register services if not already registered
        await async_setup_services(hass)

        return True


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up integration services."""
    # Only register services once
    if hass.services.has_service(DOMAIN, SERVICE_RESET_FUEL_METER):
        return

    @callback
    def async_get_fuel_meter_entity(entity_id: str):
        """Get the fuel meter entity from entity_id."""
        from .sensor import DEVICE_CLASS_FUEL_METER, FuelConsumptionTotalSensor

        entity_registry = er.async_get(hass)
        entity_entry = entity_registry.async_get(entity_id)

        if entity_entry is None:
            _LOGGER.error("Entity %s not found", entity_id)
            return None

        # Find the entity in all config entries
        for entry_id, entry_data in hass.data.get(DOMAIN, {}).items():
            coordinator = entry_data.get(SERVICE_COORDINATOR)
            if coordinator is None:
                continue

            # Check if this coordinator has our fuel meter entity
            for entity in coordinator.async_contexts():
                if hasattr(entity, "entity_id") and entity.entity_id == entity_id:
                    if isinstance(entity, FuelConsumptionTotalSensor):
                        return entity

        _LOGGER.error("Fuel meter entity %s not found in any coordinator", entity_id)
        return None

    async def async_handle_reset_fuel_meter(call: ServiceCall) -> None:
        """Handle reset fuel meter service call."""
        entity_ids = call.data.get("entity_id", [])
        if isinstance(entity_ids, str):
            entity_ids = [entity_ids]

        for entity_id in entity_ids:
            entity = async_get_fuel_meter_entity(entity_id)
            if entity is not None:
                await entity.async_reset_meter()
                _LOGGER.info("Reset fuel meter: %s", entity_id)

    async def async_handle_calibrate_fuel_meter(call: ServiceCall) -> None:
        """Handle calibrate fuel meter service call."""
        entity_ids = call.data.get("entity_id", [])
        if isinstance(entity_ids, str):
            entity_ids = [entity_ids]

        value = call.data.get("value", 0.0)

        for entity_id in entity_ids:
            entity = async_get_fuel_meter_entity(entity_id)
            if entity is not None:
                await entity.async_calibrate_meter(value)
                _LOGGER.info("Calibrated fuel meter %s to %.3f kg", entity_id, value)

    hass.services.async_register(
        DOMAIN,
        SERVICE_RESET_FUEL_METER,
        async_handle_reset_fuel_meter,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_CALIBRATE_FUEL_METER,
        async_handle_calibrate_fuel_meter,
        schema=SERVICE_CALIBRATE_SCHEMA,
    )


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok


async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle removal of an entry - clean up any repair issues."""
    async_delete_issue(hass, DOMAIN, f"connection_failed_{entry.entry_id}")
