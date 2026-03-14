"""The ecoNET300 integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import (
    HomeAssistant,
    ServiceCall,
    ServiceResponse,
    SupportsResponse,
    callback,
)
from homeassistant.exceptions import (
    ConfigEntryAuthFailed,
    ConfigEntryNotReady,
    ServiceValidationError,
)
from homeassistant.helpers import device_registry as dr, entity_registry as er
from homeassistant.helpers.issue_registry import async_delete_issue
import voluptuous as vol

from .api import make_api
from .common import AuthError, EconetDataCoordinator
from .common_functions import (
    decode_ecomax_schedule_day,
    decode_ecomax_schedule_metadata,
    summarize_schedule_slots,
)
from .const import (
    DEVICE_CLASS_FUEL_METER,
    DOMAIN,
    NUMBER_OF_AVAILABLE_ECOSTERS,
    NUMBER_OF_AVAILABLE_MIXERS,
    SCHEDULE_TYPE_MAP,
    SCHEDULE_TYPE_REVERSE_MAP,
    SCHEDULE_WEEKDAYS,
    SERVICE_API,
    SERVICE_COORDINATOR,
    SERVICE_FUEL_SENSOR,
    SERVICE_GET_SCHEDULE,
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

# Service schemas
SERVICE_CALIBRATE_SCHEMA = vol.Schema(
    {
        vol.Required("value"): vol.Coerce(float),
    }
)

SERVICE_GET_SCHEDULE_SCHEMA = vol.Schema(
    {
        vol.Required("schedule_type"): str,
        vol.Optional("weekday"): vol.In(SCHEDULE_WEEKDAYS),
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
    for i in range(1, NUMBER_OF_AVAILABLE_MIXERS + 1):
        ghost_identifiers.add((DOMAIN, f"default-uid-mixer-{i}"))
    for i in range(1, NUMBER_OF_AVAILABLE_ECOSTERS + 1):
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


def _find_ecomax_schedules(hass: HomeAssistant) -> dict[str, Any]:
    """Find ecomaxSchedules data from the first available coordinator."""
    for entry_data in hass.data.get(DOMAIN, {}).values():
        if not isinstance(entry_data, dict):
            continue
        coordinator = entry_data.get(SERVICE_COORDINATOR)
        if coordinator and coordinator.data:
            sys_params = coordinator.data.get("sysParams") or {}
            raw_schedules = sys_params.get("schedules") or {}
            schedules = raw_schedules.get("ecomaxSchedules", raw_schedules)
            if schedules:
                return schedules
    return {}


def _decode_single_day(
    tz_key: str, friendly_name: str, weekday: str, schedule_data: list, metadata: dict
) -> dict[str, Any]:
    """Decode a single weekday from a schedule."""
    day_idx = SCHEDULE_WEEKDAYS.index(weekday)
    if day_idx >= len(schedule_data) - 1:
        raise ServiceValidationError(
            f"Day index {day_idx} out of range for schedule '{friendly_name}'"
        )
    slots = decode_ecomax_schedule_day(schedule_data[day_idx])
    return {
        "schedule": {
            "type": friendly_name,
            "api_key": tz_key,
            "weekday": weekday,
            "metadata": metadata,
            "slots": slots,
            "summary": summarize_schedule_slots(slots),
        }
    }


def _decode_all_days(
    tz_key: str, friendly_name: str, schedule_data: list, metadata: dict
) -> dict[str, Any]:
    """Decode all 7 weekdays from a schedule."""
    days: dict[str, Any] = {}
    for idx, day_name in enumerate(SCHEDULE_WEEKDAYS):
        if idx >= len(schedule_data) - 1:
            break
        slots = decode_ecomax_schedule_day(schedule_data[idx])
        days[day_name] = {
            "slots": slots,
            "summary": summarize_schedule_slots(slots),
        }
    return {
        "schedule": {
            "type": friendly_name,
            "api_key": tz_key,
            "metadata": metadata,
            "days": days,
        }
    }


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

    async def async_handle_get_schedule(call: ServiceCall) -> ServiceResponse:
        """Handle get_schedule service call."""
        schedule_type: str = call.data["schedule_type"]
        weekday: str | None = call.data.get("weekday")
        tz_key = SCHEDULE_TYPE_MAP.get(schedule_type, schedule_type)

        schedules = _find_ecomax_schedules(hass)
        if not schedules:
            raise ServiceValidationError("No schedule data available from the device")

        if tz_key not in schedules:
            available = [SCHEDULE_TYPE_REVERSE_MAP.get(k, k) for k in schedules]
            raise ServiceValidationError(
                f"Schedule '{schedule_type}' not found. "
                f"Available: {', '.join(sorted(available))}"
            )

        schedule_data: list = schedules[tz_key]
        friendly_name = SCHEDULE_TYPE_REVERSE_MAP.get(tz_key, tz_key)
        metadata_raw = schedule_data[-1] if len(schedule_data) > 7 else []
        metadata = decode_ecomax_schedule_metadata(metadata_raw)

        if weekday is not None:
            return _decode_single_day(
                tz_key, friendly_name, weekday, schedule_data, metadata
            )
        return _decode_all_days(tz_key, friendly_name, schedule_data, metadata)

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

    hass.services.async_register(
        DOMAIN,
        SERVICE_GET_SCHEDULE,
        async_handle_get_schedule,
        schema=SERVICE_GET_SCHEDULE_SCHEMA,
        supports_response=SupportsResponse.ONLY,
    )


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id, None)

    return unload_ok


async def async_remove_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle removal of an entry - clean up any repair issues."""
    async_delete_issue(hass, DOMAIN, f"connection_failed_{entry.entry_id}")
