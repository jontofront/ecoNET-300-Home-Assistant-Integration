"""Provide info to system health for ecoNET300 integration."""

from __future__ import annotations

from typing import Any

from homeassistant.components import system_health
from homeassistant.core import HomeAssistant, callback

from .const import DOMAIN, SERVICE_API


@callback
def async_register(
    hass: HomeAssistant,
    register: system_health.SystemHealthRegistration,
) -> None:
    """Register system health callbacks."""
    register.async_register_info(system_health_info)


async def system_health_info(hass: HomeAssistant) -> dict[str, Any]:
    """Get info for the info page."""
    info: dict[str, Any] = {}

    for entry_data in hass.data.get(DOMAIN, {}).values():
        if not isinstance(entry_data, dict):
            continue

        api = entry_data.get(SERVICE_API)
        if api is None:
            continue

        info["host"] = api.host
        info["controller_model"] = api.model_id
        info["software_version"] = api.sw_rev
        info["hardware_version"] = api.hw_ver
        info["can_reach_device"] = system_health.async_check_can_reach_url(
            hass, api.host
        )
        break

    return info
