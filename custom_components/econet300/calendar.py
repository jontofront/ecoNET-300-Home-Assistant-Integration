"""Support for ecoNET300 schedule calendar entities."""

from __future__ import annotations

import datetime
import logging
from typing import Any

from homeassistant.components.calendar import (
    CalendarEntity,
    CalendarEntityDescription,
    CalendarEvent,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
import homeassistant.util.dt as dt_util

from .common import Econet300Api, EconetDataCoordinator
from .common_functions import (
    decode_ecomax_schedule_day,
    decode_ecomax_schedule_metadata,
    iter_device_schedules,
    merge_active_slot_ranges,
)
from .const import DOMAIN, SERVICE_API, SERVICE_COORDINATOR
from .entity import EconetEntity, get_device_info_for_component

_LOGGER = logging.getLogger(__name__)

_SCHEDULE_FRIENDLY_SUMMARIES: dict[str, str] = {
    "boiler": "Boiler",
    "boiler_clean": "Boiler Clean",
    "boiler_work": "Boiler Work",
    "circulation_pump": "Circulation Pump",
    "exchanger_clean": "Exchanger Clean",
    "water_heater": "Water Heater",
    "water_heater_2": "Water Heater 2",
}


def _event_summary(friendly_name: str) -> str:
    """Return a human-readable event summary for a schedule type."""
    if friendly_name.startswith("mixer_"):
        num = friendly_name.split("_", 1)[1]
        return f"Mixer {num}"
    if friendly_name.startswith("thermostat_"):
        num = friendly_name.split("_", 1)[1]
        return f"Thermostat {num}"
    return _SCHEDULE_FRIENDLY_SUMMARIES.get(friendly_name, friendly_name)


class EconetScheduleCalendar(EconetEntity, CalendarEntity):
    """Calendar entity representing a weekly ecoMAX schedule."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
        schedule_type: str,
        api_key: str,
        component: str | None = None,
    ) -> None:
        """Initialize the schedule calendar entity."""
        self.entity_description = CalendarEntityDescription(
            key=f"schedule_{schedule_type}",
            translation_key=f"schedule_{schedule_type}",
        )
        self.api = api
        self._api_key = api_key
        self._component = component
        self._schedule_type = schedule_type
        self._event_summary = _event_summary(schedule_type)
        self._cached_event: CalendarEvent | None = None
        self._metadata: dict[str, Any] = {}
        super().__init__(coordinator, api)

    @property
    def device_info(self):
        """Return device info, grouping mixer/HUW schedules with their device."""
        if self._component:
            return get_device_info_for_component(
                self._component,
                self.api,
                single_device=self.coordinator.single_device_tree,
            )
        return super().device_info

    @property
    def event(self) -> CalendarEvent | None:
        """Return the current or next upcoming event."""
        return self._cached_event

    def _get_schedule_data(self) -> list | None:
        """Fetch raw schedule bitmask array from coordinator data."""
        if self.coordinator.data is None:
            return None
        sys_params = self.coordinator.data.get("sysParams") or {}
        raw_schedules = sys_params.get("schedules") or {}
        schedules = raw_schedules.get("ecomaxSchedules", raw_schedules)
        return schedules.get(self._api_key)

    def _is_schedule_enabled(self) -> bool:
        """Return True if the schedule is enabled (on_off_mode != 0)."""
        return self._metadata.get("on_off_mode", 1) != 0

    @callback
    def _handle_coordinator_update(self) -> None:
        """Update cached event when coordinator data changes."""
        schedule_data = self._get_schedule_data()
        if not schedule_data:
            self._cached_event = None
            self._metadata = {}
            self.async_write_ha_state()
            return

        metadata_raw = schedule_data[-1] if len(schedule_data) > 7 else []
        self._metadata = decode_ecomax_schedule_metadata(metadata_raw)

        now = dt_util.now()
        self._cached_event = self._find_current_or_next_event(schedule_data, now)
        self.async_write_ha_state()

    def _find_current_or_next_event(
        self, schedule_data: list, now: datetime.datetime
    ) -> CalendarEvent | None:
        """Find the event that is active now, or the next upcoming one."""
        if not self._is_schedule_enabled():
            return None

        current_time = now.time()
        today = now.date()

        for day_offset in range(8):
            check_date = today + datetime.timedelta(days=day_offset)
            weekday_idx = (check_date.weekday() + 1) % 7
            if weekday_idx >= len(schedule_data) or weekday_idx >= 7:
                continue

            slots = decode_ecomax_schedule_day(schedule_data[weekday_idx])
            ranges = merge_active_slot_ranges(slots)

            for start_time, end_time in ranges:
                start_dt = datetime.datetime.combine(
                    check_date, start_time, tzinfo=now.tzinfo
                )
                end_dt = datetime.datetime.combine(
                    check_date,
                    end_time if end_time != datetime.time(0, 0) else datetime.time(0, 0),
                    tzinfo=now.tzinfo,
                )
                if end_time == datetime.time(0, 0):
                    end_dt += datetime.timedelta(days=1)

                if day_offset == 0 and end_dt.time() == datetime.time(0, 0) and end_dt.date() <= today:
                    pass
                elif day_offset == 0 and end_time != datetime.time(0, 0) and end_time <= current_time:
                    continue

                if start_dt <= now < end_dt or start_dt > now:
                    return CalendarEvent(
                        summary=self._event_summary,
                        start=start_dt,
                        end=end_dt,
                    )

        return None

    async def async_get_events(
        self,
        hass: HomeAssistant,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
    ) -> list[CalendarEvent]:
        """Return calendar events within a datetime range."""
        schedule_data = self._get_schedule_data()
        if not schedule_data or not self._is_schedule_enabled():
            return []

        events: list[CalendarEvent] = []
        tz = start_date.tzinfo or dt_util.get_default_time_zone()
        current_date = start_date.date()
        end = end_date.date()

        while current_date <= end:
            weekday_idx = (current_date.weekday() + 1) % 7
            if weekday_idx < 7 and weekday_idx < len(schedule_data):
                slots = decode_ecomax_schedule_day(schedule_data[weekday_idx])
                ranges = merge_active_slot_ranges(slots)

                for start_time, end_time in ranges:
                    event_start = datetime.datetime.combine(
                        current_date, start_time, tzinfo=tz
                    )
                    if end_time == datetime.time(0, 0):
                        event_end = datetime.datetime.combine(
                            current_date + datetime.timedelta(days=1),
                            datetime.time(0, 0),
                            tzinfo=tz,
                        )
                    else:
                        event_end = datetime.datetime.combine(
                            current_date, end_time, tzinfo=tz
                        )

                    if event_end > start_date and event_start < end_date:
                        events.append(
                            CalendarEvent(
                                summary=self._event_summary,
                                start=event_start,
                                end=event_end,
                            )
                        )

            current_date += datetime.timedelta(days=1)

        return events

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return schedule metadata as extra state attributes."""
        attrs: dict[str, Any] = {}
        attrs["schedule_enabled"] = self._is_schedule_enabled()
        if self._metadata:
            attrs["metadata"] = self._metadata
        return attrs

    async def async_added_to_hass(self) -> None:
        """Sync initial state when entity is added."""
        await super().async_added_to_hass()
        self._handle_coordinator_update()


def create_schedule_calendars(
    coordinator: EconetDataCoordinator, api: Econet300Api
) -> list[EconetScheduleCalendar]:
    """Create calendar entities for each schedule type present on the device."""
    entities: list[EconetScheduleCalendar] = []

    for friendly_name, api_key, component in iter_device_schedules(coordinator.data):
        entities.append(
            EconetScheduleCalendar(
                coordinator, api, friendly_name, api_key, component
            )
        )

    _LOGGER.info("Created %d schedule calendar entities", len(entities))
    return entities


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the calendar platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id][SERVICE_COORDINATOR]
    api = hass.data[DOMAIN][entry.entry_id][SERVICE_API]

    entities = create_schedule_calendars(coordinator, api)
    async_add_entities(entities)
