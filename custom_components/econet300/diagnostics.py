"""Diagnostics for the ecoNET300 integration."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.device_registry import DeviceEntry
from homeassistant.loader import async_get_integration

from .const import DOMAIN, SERVICE_API, SERVICE_COORDINATOR

# Data to redact from diagnostics
TO_REDACT = [
    "password",
    "username",  # May contain sensitive info
    "host",  # May contain internal network info
    "uid",  # Device UID - unique device identifier
    "device_uid",  # Device UID in coordinator data
    "identifiers",  # Device identifiers containing UIDs
    "key",  # API keys and secrets
    "ssid",  # WiFi network name
    "wlan0",  # WiFi interface IP address
    "eth0",  # Ethernet interface IP address
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
    try:
        # Get integration version
        try:
            integration = await async_get_integration(hass, entry.domain)
            integration_version = (
                str(integration.version) if integration.version else "unknown"
            )
        except (ImportError, ValueError, KeyError):
            integration_version = "unknown"

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
                try:
                    coordinator_data = {
                        "last_update_success": getattr(
                            coordinator, "last_update_success", None
                        ),
                        "last_update_time": coordinator.last_update_time.isoformat()
                        if hasattr(coordinator, "last_update_time")
                        and coordinator.last_update_time
                        else None,
                        "data": getattr(coordinator, "data", None) or {},
                    }
                except (AttributeError, TypeError, ValueError) as e:
                    coordinator_data = {
                        "error": f"Failed to get coordinator data: {e!s}"
                    }

            # Get API information
            if api:
                try:
                    api_info = {
                        "host": getattr(api, "host", None),
                        "uid": getattr(api, "uid", None),
                        "model_id": getattr(api, "model_id", None),
                        "sw_rev": getattr(api, "sw_rev", None),
                        "hw_ver": getattr(api, "hw_ver", None),
                    }
                except (AttributeError, TypeError, ValueError) as e:
                    api_info = {"error": f"Failed to get API info: {e!s}"}

                # Get raw API endpoint data for troubleshooting
                try:
                    api_endpoint_data = {
                        "sys_params": await api.fetch_sys_params(),
                        "reg_params": await api.fetch_reg_params(),
                        "reg_params_data": await api.fetch_reg_params_data(),
                        "param_edit_data": await api.fetch_param_edit_data(),
                    }
                except (
                    AttributeError,
                    TypeError,
                    ValueError,
                    KeyError,
                    ConnectionError,
                    TimeoutError,
                ) as e:
                    api_endpoint_data = {
                        "error": f"Failed to fetch API endpoint data: {e!s}"
                    }
            else:
                api_endpoint_data = {"error": "API not available"}

        # Get connection status
        try:
            connection_status = {
                "entry_state": entry.state.value
                if hasattr(entry.state, "value")
                else str(entry.state),
                "disabled_by": entry.disabled_by.value
                if entry.disabled_by and hasattr(entry.disabled_by, "value")
                else str(entry.disabled_by),
                "pref_disable_new_entities": getattr(
                    entry, "pref_disable_new_entities", None
                ),
                "pref_disable_polling": getattr(entry, "pref_disable_polling", None),
            }
        except (AttributeError, TypeError, ValueError) as e:
            connection_status = {"error": f"Failed to get connection status: {e!s}"}

        return {
            "integration_version": integration_version,
            "entry_data": _redact_data(dict(entry.data), TO_REDACT),
            "entry_options": getattr(entry, "options", {}),
            "connection_status": connection_status,
            "api_info": _redact_data(api_info, TO_REDACT),
            "coordinator_data": coordinator_data,
            "api_endpoint_data": _redact_data(api_endpoint_data, TO_REDACT),
        }
    except (AttributeError, TypeError, ValueError, KeyError) as e:
        return {
            "error": f"Failed to get config entry diagnostics: {e!s}",
            "entry_data": _redact_data(dict(entry.data), TO_REDACT),
        }


async def async_get_device_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry, device: DeviceEntry
) -> dict[str, Any]:
    """Return diagnostics for a device."""
    try:
        # Get integration version
        try:
            integration = await async_get_integration(hass, entry.domain)
            integration_version = (
                str(integration.version) if integration.version else "unknown"
            )
        except (ImportError, ValueError, KeyError):
            integration_version = "unknown"

        device_data = {}

        # Get device information
        try:
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
        except (AttributeError, TypeError, ValueError) as e:
            device_data = {"error": f"Failed to get device info: {e!s}"}

        # Get entities associated with this device
        entity_data: dict[str, Any] = {"entity_count": 0, "entities": []}
        try:
            entity_registry = er.async_get(hass)
            device_entities = [
                entity_registry.async_get(entity_id)
                for entity_id in entity_registry.entities
                if entity_registry.entities[entity_id].device_id == device.id
            ]

            entity_data["entity_count"] = len(device_entities)

            for entity in device_entities:
                if entity is None:
                    continue

                # Get current entity state
                entity_state = hass.states.get(entity.entity_id)
                current_value = None
                unit_of_measurement = None
                attributes = {}

                if entity_state:
                    current_value = entity_state.state
                    unit_of_measurement = entity_state.attributes.get(
                        "unit_of_measurement"
                    )
                    # Get key attributes (limit to avoid too much data)
                    key_attributes = [
                        "device_class",
                        "state_class",
                        "friendly_name",
                        "icon",
                        "entity_category",
                        "last_updated",
                        "last_changed",
                    ]
                    attributes = {
                        attr: entity_state.attributes.get(attr)
                        for attr in key_attributes
                        if entity_state.attributes.get(attr) is not None
                    }

                entity_info = {
                    "entity_id": entity.entity_id,
                    "name": entity.name,
                    "platform": entity.platform,
                    "disabled_by": entity.disabled_by.value
                    if entity.disabled_by and hasattr(entity.disabled_by, "value")
                    else str(entity.disabled_by),
                    "current_value": current_value,
                    "unit_of_measurement": unit_of_measurement,
                    "attributes": attributes,
                }
                entities_list = entity_data["entities"]
                if isinstance(entities_list, list):
                    entities_list.append(entity_info)
        except (AttributeError, TypeError, ValueError, KeyError, ImportError) as e:
            entity_data = {"error": f"Failed to get entity info: {e!s}"}

        # Get current data for this device from coordinator
        coordinator_data = {}
        try:
            if entry.entry_id in hass.data.get(DOMAIN, {}):
                integration_data = hass.data[DOMAIN][entry.entry_id]
                coordinator = integration_data.get(SERVICE_COORDINATOR)

                if coordinator and coordinator.data:
                    # Filter data relevant to this device
                    device_uid = device.identifiers
                    if device_uid:
                        # Get the UID from device identifiers
                        device_uid_str = (
                            next(iter(device_uid))[1] if device_uid else None
                        )
                        if device_uid_str:
                            coordinator_data = {
                                "device_uid": device_uid_str,
                                "last_update": coordinator.last_update_time.isoformat()
                                if hasattr(coordinator, "last_update_time")
                                and coordinator.last_update_time
                                else None,
                                "data_available": bool(coordinator.data),
                            }
        except (AttributeError, TypeError, ValueError, KeyError) as e:
            coordinator_data = {"error": f"Failed to get coordinator data: {e!s}"}

        # Get raw API endpoint data for troubleshooting
        api_endpoint_data = {}
        try:
            if entry.entry_id in hass.data.get(DOMAIN, {}):
                integration_data = hass.data[DOMAIN][entry.entry_id]
                api = integration_data.get(SERVICE_API)

                if api:
                    try:
                        api_endpoint_data = {
                            "sys_params": await api.fetch_sys_params(),
                            "reg_params": await api.fetch_reg_params(),
                            "reg_params_data": await api.fetch_reg_params_data(),
                            "param_edit_data": await api.fetch_param_edit_data(),
                        }
                    except (
                        AttributeError,
                        TypeError,
                        ValueError,
                        KeyError,
                        ConnectionError,
                        TimeoutError,
                    ) as e:
                        api_endpoint_data = {
                            "error": f"Failed to fetch API endpoint data: {e!s}"
                        }
        except (AttributeError, TypeError, ValueError, KeyError) as e:
            api_endpoint_data = {"error": f"Failed to get API endpoint data: {e!s}"}

    except (AttributeError, TypeError, ValueError, KeyError) as e:
        return {
            "error": f"Failed to get device diagnostics: {e!s}",
            "device_info": {"device_id": device.id if device else "unknown"},
        }
    else:
        return {
            "integration_version": integration_version,
            "device_info": _redact_data(device_data, TO_REDACT),
            "entity_info": entity_data,
            "coordinator_data": _redact_data(coordinator_data, TO_REDACT),
            "api_endpoint_data": _redact_data(api_endpoint_data, TO_REDACT),
        }
