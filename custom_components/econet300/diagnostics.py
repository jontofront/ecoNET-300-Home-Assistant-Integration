"""Diagnostics for the ecoNET300 integration."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntry

from .const import DOMAIN, SERVICE_API, SERVICE_COORDINATOR

# Data to redact from diagnostics
TO_REDACT = [
    "password",
    "username",  # May contain sensitive info
    "host",  # May contain internal network info
]


def _redact_data(data: Any, to_redact: list[str]) -> Any:
    """Redact sensitive data from a dictionary."""
    if not isinstance(data, dict):
        return data

    redacted: dict[str, Any] = {}
    for key, value in data.items():
        if key in to_redact:
            redacted[key] = "**REDACTED**"
        elif isinstance(value, dict):
            redacted[key] = _redact_data(value, to_redact)
        else:
            redacted[key] = value

    return redacted


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator_data = {}
    api_info = {}
    connection_status = {}

    # Get integration data if available
    if entry.entry_id in hass.data.get(DOMAIN, {}):
        integration_data = hass.data[DOMAIN][entry.entry_id]
        coordinator = integration_data.get(SERVICE_COORDINATOR)
        api = integration_data.get(SERVICE_API)

        # Get coordinator data
        if coordinator:
            coordinator_data = {
                "last_update_success": coordinator.last_update_success,
                "last_update_time": coordinator.last_update_time.isoformat()
                if coordinator.last_update_time
                else None,
                "data": coordinator.data or {},
            }

        # Get API information
        if api:
            api_info = {
                "host": api.host,
                "uid": api.uid,
                "model_id": api.model_id,
                "sw_rev": api.sw_rev,
                "hw_ver": api.hw_ver,
            }

    # Get connection status
    connection_status = {
        "entry_state": entry.state.value
        if hasattr(entry.state, "value")
        else str(entry.state),
        "disabled_by": entry.disabled_by.value
        if entry.disabled_by and hasattr(entry.disabled_by, "value")
        else str(entry.disabled_by),
        "pref_disable_new_entities": entry.pref_disable_new_entities,
        "pref_disable_polling": entry.pref_disable_polling,
    }

    return {
        "entry_data": _redact_data(dict(entry.data), TO_REDACT),
        "entry_options": entry.options,
        "connection_status": connection_status,
        "api_info": _redact_data(api_info, TO_REDACT),
        "coordinator_data": coordinator_data,
    }


async def async_get_device_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry, device: DeviceEntry
) -> dict[str, Any]:
    """Return diagnostics for a device."""
    device_data = {}
    entity_data = {}

    # Get device information
    device_data = {
        "device_id": device.id,
        "name": device.name,
        "manufacturer": device.manufacturer,
        "model": device.model,
        "sw_version": device.sw_version,
        "hw_version": device.hw_version,
        "identifiers": list(device.identifiers),
        "connections": list(device.connections),
        "suggested_area": device.suggested_area,
        "disabled_by": device.disabled_by.value
        if device.disabled_by and hasattr(device.disabled_by, "value")
        else str(device.disabled_by),
    }

    # Get entities associated with this device
    entity_registry = hass.helpers.entity_registry.async_get()
    device_entities = [
        entity_registry.async_get(entity_id)
        for entity_id in entity_registry.entities
        if entity_registry.entities[entity_id].device_id == device.id
    ]

    entity_data = {
        "entity_count": len(device_entities),
        "entities": [
            {
                "entity_id": entity.entity_id,
                "name": entity.name,
                "platform": entity.platform,
                "disabled_by": entity.disabled_by.value
                if entity.disabled_by and hasattr(entity.disabled_by, "value")
                else str(entity.disabled_by),
            }
            for entity in device_entities
            if entity is not None
        ],
    }

    # Get current data for this device from coordinator
    coordinator_data = {}
    if entry.entry_id in hass.data.get(DOMAIN, {}):
        integration_data = hass.data[DOMAIN][entry.entry_id]
        coordinator = integration_data.get(SERVICE_COORDINATOR)

        if coordinator and coordinator.data:
            # Filter data relevant to this device
            device_uid = device.identifiers
            if device_uid:
                # Get the UID from device identifiers
                device_uid_str = next(iter(device_uid))[1] if device_uid else None
                if device_uid_str:
                    coordinator_data = {
                        "device_uid": device_uid_str,
                        "last_update": coordinator.last_update_time.isoformat()
                        if coordinator.last_update_time
                        else None,
                        "data_available": bool(coordinator.data),
                    }

    return {
        "device_info": device_data,
        "entity_info": entity_data,
        "coordinator_data": coordinator_data,
    }
