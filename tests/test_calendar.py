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


def _discover_schedule_fixtures() -> list[str]:
    """Find all fixture directories containing ecomaxSchedules in sysParams."""
    fixtures_dir = Path(__file__).parent / "fixtures"
    models: list[str] = []
    for sys_file in sorted(fixtures_dir.glob("*/sysParams.json")):
        data = json.loads(sys_file.read_text())
        schedules = data.get("schedules", {})
        if "ecomaxSchedules" in schedules:
            models.append(sys_file.parent.name)
    return models


SCHEDULE_FIXTURE_MODELS = _discover_schedule_fixtures()


def _load_sys_params(model: str) -> dict:
    """Load sysParams fixture for a given model."""
    path = Path(__file__).parent / "fixtures" / model / "sysParams.json"
    with path.open() as f:
        return json.load(f)


@pytest.fixture
def api() -> MagicMock:
    """Create a mock API."""
    mock = MagicMock()
    mock.uid = "test-uid-123"
    mock.host = "192.168.1.100"
    return mock


def _make_coordinator(sys_params: dict) -> MagicMock:
    """Create a mock coordinator with schedule data."""
    mock = MagicMock()
    mock.data = {"sysParams": sys_params}
    mock.single_device_tree = False
    return mock


class TestCreateScheduleCalendarsAllModels:
    """Test create_schedule_calendars across all fixture models with schedules."""

    @pytest.fixture(params=SCHEDULE_FIXTURE_MODELS)
    def model_coordinator(self, request) -> tuple[str, MagicMock]:
        """Create coordinator for each model with schedule data."""
        model = request.param
        sys_params = _load_sys_params(model)
        return model, _make_coordinator(sys_params)

    def test_creates_calendars(self, model_coordinator, api):
        """Factory creates at least one calendar for each model."""
        model, coordinator = model_coordinator
        entities = create_schedule_calendars(coordinator, api)
        assert len(entities) > 0, f"{model} should produce calendar entities"
        assert all(isinstance(e, EconetScheduleCalendar) for e in entities)

    def test_unique_ids(self, model_coordinator, api):
        """Each calendar entity has a unique ID within the same model."""
        model, coordinator = model_coordinator
        entities = create_schedule_calendars(coordinator, api)
        ids = [e._attr_unique_id for e in entities]
        assert len(ids) == len(set(ids)), f"{model} has duplicate calendar IDs"

    def test_async_get_events_all_models(self, model_coordinator, api):
        """async_get_events returns a list for every calendar entity."""
        model, coordinator = model_coordinator
        entities = create_schedule_calendars(coordinator, api)
        tz = datetime.timezone.utc
        start = datetime.datetime(2026, 6, 29, 0, 0, tzinfo=tz)
        end = datetime.datetime(2026, 7, 6, 0, 0, tzinfo=tz)
        hass = MagicMock()

        import asyncio

        loop = asyncio.new_event_loop()
        try:
            for entity in entities:
                with patch("custom_components.econet300.calendar.dt_util") as mock_dt:
                    mock_dt.get_default_time_zone.return_value = tz
                    events = loop.run_until_complete(
                        entity.async_get_events(hass, start, end)
                    )
                    assert isinstance(events, list), (
                        f"{model}/{entity._schedule_type} should return a list"
                    )
        finally:
            loop.close()


class TestCreateScheduleCalendars:
    """Test create_schedule_calendars edge cases."""

    def test_no_data_returns_empty(self, api):
        """No coordinator data returns empty list."""
        coordinator = MagicMock()
        coordinator.data = None
        entities = create_schedule_calendars(coordinator, api)
        assert entities == []

    def test_empty_schedules_returns_empty(self, api):
        """Empty schedules dict returns empty list."""
        coordinator = _make_coordinator({"schedules": {}})
        entities = create_schedule_calendars(coordinator, api)
        assert entities == []


class TestEconetScheduleCalendar:
    """Test EconetScheduleCalendar entity behavior."""

    @pytest.fixture
    def coordinator(self) -> MagicMock:
        """Default coordinator with ecoMAX810P-L data."""
        return _make_coordinator(_load_sys_params("ecoMAX810P-L"))

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
