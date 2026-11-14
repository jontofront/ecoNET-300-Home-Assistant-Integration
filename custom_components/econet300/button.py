"""DHW boost button for the ecoNET300 integration.

The momentary one-shot DHW loading trigger lives with the water-heater
platform code; this thin module satisfies Home Assistant's per-platform
module resolution for Platform.BUTTON.
"""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, SERVICE_API, SERVICE_COORDINATOR
from .water_heater import (
    EconetDhwBoostButton,
    _dhw_platform_supported,
    _valid_boost_param,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the DHW boost button for supported controllers."""
    services = hass.data[DOMAIN][entry.entry_id]
    coordinator = services[SERVICE_COORDINATOR]
    data = coordinator.data or {}
    if _dhw_platform_supported(data) and _valid_boost_param(data):
        async_add_entities([EconetDhwBoostButton(coordinator, services[SERVICE_API])])
