"""Tests for the ecoNET300 calendar entity (schedule calendars)."""

from __future__ import annotations

import datetime
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from custom_components.econet300.calendar import (
    EconetScheduleCalendar,
    create_schedule_calendars,
)


@pytest.fixture
def sys_params() -> dict:
    """Load the ecoMAX810P-L sysParams fixture."""
    fixture_path = (
        Path(__file__).parent / "fixtures" / "ecoMAX810P-L" / "sysParams.json"
    )
    with fixture_path.open() as f:
        return json.load(f)


@pytest.fixture
def coordinator(sys_params) -> MagicMock:
    """Create a mock coordinator with schedule data."""
    mock = MagicMock()
    mock.data = {"sysParams": sys_params}
    mock.single_device_tree = False
    return mock


@pytest.fixture
def api() -> MagicMock:
    """Create a mock API."""
    mock = MagicMock()
    mock.uid = "test-uid-123"
    mock.host = "192.168.1.100"
    return mock


class TestCreateScheduleCalendars:
    """Test create_schedule_calendars factory function."""

    def test_creates_calendars_from_fixture(self, coordinator, api):
        """Factory creates one calendar per schedule type."""
        entities = create_schedule_calendars(coordinator, api)
        assert len(entities) > 0
        assert all(isinstance(e, EconetScheduleCalendar) for e in entities)

    def test_no_data_returns_empty(self, api):
        """No coordinator data returns empty list."""
        coordinator = MagicMock()
        coordinator.data = None
        entities = create_schedule_calendars(coordinator, api)
        assert entities == []

    def test_unique_ids(self, coordinator, api):
        """Each calendar has a unique ID."""
        entities = create_schedule_calendars(coordinator, api)
        ids = [e._attr_unique_id for e in entities]
        assert len(ids) == len(set(ids))


class TestEconetScheduleCalendar:
    """Test EconetScheduleCalendar entity behavior."""

    def _make_calendar(
        self, coordinator, api, schedule_type="boiler", api_key="boilerTZ"
    ) -> EconetScheduleCalendar:
        """Create a calendar entity for testing."""
        return EconetScheduleCalendar(
            coordinator, api, schedule_type, api_key, component=None
        )

    def test_unique_id_format(self, coordinator, api):
        """Unique ID includes UID and schedule type."""
        cal = self._make_calendar(coordinator, api)
        assert cal._attr_unique_id == "test-uid-123-schedule-boiler"

    def test_translation_key(self, coordinator, api):
        """Translation key follows expected pattern."""
        cal = self._make_calendar(coordinator, api)
        assert cal._attr_translation_key == "schedule_boiler"

    @patch("custom_components.econet300.calendar.dt_util")
    def test_async_get_events(self, mock_dt_util, coordinator, api):
        """async_get_events returns events within the date range."""
        tz = datetime.timezone.utc
        mock_dt_util.get_default_time_zone.return_value = tz

        cal = self._make_calendar(coordinator, api)
        cal.coordinator = coordinator

        start = datetime.datetime(2026, 6, 29, 0, 0, tzinfo=tz)
        end = datetime.datetime(2026, 6, 30, 0, 0, tzinfo=tz)

        hass = MagicMock()
        import asyncio

        events = asyncio.get_event_loop().run_until_complete(
            cal.async_get_events(hass, start, end)
        )
        assert isinstance(events, list)

    def test_extra_state_attributes_default(self, coordinator, api):
        """Extra state attrs include schedule_enabled."""
        cal = self._make_calendar(coordinator, api)
        attrs = cal.extra_state_attributes
        assert "schedule_enabled" in attrs

    def test_event_is_none_without_update(self, coordinator, api):
        """Event property returns None before first coordinator update."""
        cal = self._make_calendar(coordinator, api)
        assert cal.event is None
