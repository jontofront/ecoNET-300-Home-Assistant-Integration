"""The ecoNET300 integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall, callback
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.helpers import device_registry as dr, entity_registry as er
from homeassistant.helpers.issue_registry import async_delete_issue
import voluptuous as vol

from .api import make_api
from .common import AuthError, EconetDataCoordinator
from .const import (
    DEVICE_CLASS_FUEL_METER,
    DOMAIN,
    SERVICE_API,
    SERVICE_COORDINATOR,
    SERVICE_FUEL_SENSOR,
)
from .mem_cache import MemCache
from .sensor import FuelConsumptionTotalSensor

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
    except (ConnectionError, ValueError) as init_error:
        raise ConfigEntryNotReady(
            "Device not ready - cannot fetch system parameters"
        ) from init_error
    else:
        # Clean up ghost devices created by failed API inits (uid = "default-uid")
        _cleanup_ghost_devices(hass, entry, api.uid)

        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

        # Register services if not already registered
        await async_setup_services(hass)

        return True


def _cleanup_ghost_devices(
    hass: HomeAssistant, entry: ConfigEntry, real_uid: str
) -> None:
    """Remove orphaned devices created by failed API inits with default-uid.

    When api.init() previously failed silently, entities registered under
    devices with identifier (DOMAIN, "default-uid"). These ghost devices
    persist in the device registry even after the API recovers.
    """
    try:
        device_reg = dr.async_get(hass)
    except Exception:  # noqa: BLE001
        _LOGGER.debug("Device registry not available, skipping ghost cleanup")
        return

    ghost_identifiers: set[tuple[str, str]] = {
        (DOMAIN, "default-uid"),
        (DOMAIN, "default-uid-huw"),
        (DOMAIN, "default-uid-buffer"),
        (DOMAIN, "default-uid-lambda"),
        (DOMAIN, "default-uid-solar"),
    }
    # Also cover mixer ghost devices (up to 4 mixers)
    for i in range(1, 5):
        ghost_identifiers.add((DOMAIN, f"default-uid-mixer-{i}"))
    # Also cover ecoster ghost devices (up to 8)
    for i in range(1, 9):
        ghost_identifiers.add((DOMAIN, f"default-uid-ecoster-{i}"))

    removed = 0
    for ghost_id in ghost_identifiers:
        try:
            device = device_reg.async_get_device(identifiers={ghost_id})
        except (AttributeError, TypeError):
            continue
        if device is not None:
            _LOGGER.warning(
                "Removing ghost device %s (identifier: %s) created by failed init",
                device.name,
                ghost_id,
            )
            device_reg.async_remove_device(device.id)
            removed += 1

    if removed:
        _LOGGER.info(
            "Cleaned up %d ghost device(s) - real device uid: %s", removed, real_uid
        )


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up integration services."""
    # Only register services once
    if hass.services.has_service(DOMAIN, SERVICE_RESET_FUEL_METER):
        return

    @callback
    def async_get_fuel_meter_entity(
        entity_id: str,
    ) -> FuelConsumptionTotalSensor | None:
        """Get the fuel meter entity from entity_id."""
        entity_registry = er.async_get(hass)
        entity_entry = entity_registry.async_get(entity_id)

        if entity_entry is None:
            _LOGGER.error("Entity %s not found", entity_id)
            return None
        if entity_entry.original_device_class != DEVICE_CLASS_FUEL_METER:
            _LOGGER.error("Entity %s is not a fuel meter", entity_id)
            return None

        # Look up via stored reference in hass.data
        for entry_data in hass.data.get(DOMAIN, {}).values():
            if not isinstance(entry_data, dict):
                continue
            fuel_sensor = entry_data.get(SERVICE_FUEL_SENSOR)
            if (
                isinstance(fuel_sensor, FuelConsumptionTotalSensor)
                and hasattr(fuel_sensor, "entity_id")
                and fuel_sensor.entity_id == entity_id
            ):
                return fuel_sensor

        _LOGGER.error("Fuel meter entity %s not found in any config entry", entity_id)
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
