"""Support for ecoNET300 alarm event entities."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.event import EventEntity, EventEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .common import Econet300Api, EconetDataCoordinator
from .common_functions import has_active_alarm, parse_alarm_entry
from .const import DOMAIN, SERVICE_API, SERVICE_COORDINATOR
from .entity import EconetEntity

_LOGGER = logging.getLogger(__name__)

EVENT_ALARM_TRIGGERED = "alarm_triggered"
EVENT_ALARM_CLEARED = "alarm_cleared"


class BoilerAlarmEvent(EconetEntity, EventEntity):
    """Event entity that fires when a new boiler alarm is detected or cleared."""

    _attr_has_entity_name = True
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_event_types = [EVENT_ALARM_TRIGGERED, EVENT_ALARM_CLEARED]

    def __init__(
        self,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
    ) -> None:
        """Initialize the boiler alarm event entity."""
        self.entity_description = EventEntityDescription(
            key="boiler_alarm",
            translation_key="boiler_alarm",
        )
        self.api = api
        self._previous_alarm_count: int | None = None
        self._previous_latest_from_date: str | None = None
        self._previous_had_active: bool | None = None
        super().__init__(coordinator, api)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Detect new alarms or cleared alarms and fire events."""
        if self.coordinator.data is None:
            return

        sys_params = self.coordinator.data.get("sysParams") or {}
        alarms: list[dict[str, Any]] = sys_params.get("alarms", [])
        alarm_names: dict[str, str] = (self.coordinator.data.get("rmData") or {}).get(
            "alarmsNames"
        ) or {}

        current_count = len(alarms)
        current_latest_from = alarms[0].get("fromDate") if alarms else None
        current_has_active = has_active_alarm(alarms)

        # Skip the very first update (initial load) to avoid false positives
        if self._previous_alarm_count is not None:
            new_alarm_detected = (
                current_count > self._previous_alarm_count
                or current_latest_from != self._previous_latest_from_date
            ) and current_latest_from is not None

            if new_alarm_detected:
                parsed = parse_alarm_entry(alarms[0], alarm_names)
                self._trigger_event(
                    EVENT_ALARM_TRIGGERED,
                    {
                        "alarm_code": parsed["alarm_code"],
                        "description": parsed["description"],
                        "from_date": parsed["from_date"],
                        "is_active": parsed["is_active"],
                    },
                )
                _LOGGER.info(
                    "New alarm detected: code=%s, description=%s",
                    parsed["alarm_code"],
                    parsed["description"],
                )

            alarm_cleared = (
                self._previous_had_active is True and not current_has_active
            )
            if alarm_cleared and not new_alarm_detected:
                self._trigger_event(EVENT_ALARM_CLEARED)
                _LOGGER.info("Active alarm cleared")

        self._previous_alarm_count = current_count
        self._previous_latest_from_date = current_latest_from
        self._previous_had_active = current_has_active
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        """Seed previous state on first load to avoid false positives on restart."""
        await super().async_added_to_hass()

        if self.coordinator.data is not None:
            sys_params = self.coordinator.data.get("sysParams") or {}
            alarms: list[dict[str, Any]] = sys_params.get("alarms", [])
            self._previous_alarm_count = len(alarms)
            self._previous_latest_from_date = (
                alarms[0].get("fromDate") if alarms else None
            )
            self._previous_had_active = has_active_alarm(alarms)


def create_alarm_event_entities(
    coordinator: EconetDataCoordinator, api: Econet300Api
) -> list[BoilerAlarmEvent]:
    """Create alarm event entities from sysParams.alarms data.

    Only creates entities if alarm data is present in the coordinator.
    """
    if coordinator.data is None:
        return []

    sys_params = coordinator.data.get("sysParams") or {}
    if "alarms" not in sys_params:
        _LOGGER.debug("No alarms key in sysParams, skipping alarm event entities")
        return []

    entities = [BoilerAlarmEvent(coordinator, api)]
    _LOGGER.info("Created %d alarm event entities", len(entities))
    return entities


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the event platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id][SERVICE_COORDINATOR]
    api = hass.data[DOMAIN][entry.entry_id][SERVICE_API]

    entities = create_alarm_event_entities(coordinator, api)
    async_add_entities(entities)
