"""Tests for coordinator health diagnostics and polling options.

Covers PR #234 hardening features:
- ``EconetDataCoordinator._with_health`` (online/stale metadata, keep-last-data)
- failure/success bookkeeping (``_on_failed_update`` / ``_on_successful_update``)
- ``EconetOnlineBinarySensor`` (connectivity diagnostic)
- ``EconetHealthSensor`` (data age / failures / last-success timestamp)
- ``polling_settings`` options-flow step (schema defaults + save/reload)
"""

from datetime import UTC, datetime
import time
from typing import NamedTuple
from unittest.mock import MagicMock, PropertyMock, patch

import pytest

from custom_components.econet300.binary_sensor import EconetOnlineBinarySensor
from custom_components.econet300.common import EconetDataCoordinator
from custom_components.econet300.config_flow import EconetOptionsFlowHandler
from custom_components.econet300.const import (
    CONF_POLL_EDIT_PARAMS,
    CONF_POLL_REG_PARAMS,
    CONF_POLL_SYS_PARAMS,
    CONSECUTIVE_FAILURES_THRESHOLD,
    DEFAULT_POLL_EDIT_PARAMS,
    DEFAULT_POLL_REG_PARAMS,
    DEFAULT_POLL_SYS_PARAMS,
    DOMAIN,
    STALE_AFTER_SECONDS,
)
from custom_components.econet300.sensor import EconetHealthSensor
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass


def _bare_coordinator(**overrides) -> EconetDataCoordinator:
    """Build a coordinator instance without running DataUpdateCoordinator.__init__.

    Only the attributes used by the pure health/bookkeeping methods are set, so
    we can exercise them without a real Home Assistant instance.
    """
    coord = object.__new__(EconetDataCoordinator)
    coord._last_success_ts = overrides.get("last_success_ts", 0.0)
    coord._last_failure_ts = overrides.get("last_failure_ts", 0.0)
    coord._consecutive_failures = overrides.get("consecutive_failures", 0)
    coord._last_error = overrides.get("last_error", "")
    coord._poll_reg_params = overrides.get("poll_reg_params", 15)
    coord._poll_sys_params = overrides.get("poll_sys_params", 300)
    coord._poll_edit_params = overrides.get("poll_edit_params", 300)
    coord._edit_params_failures = overrides.get("edit_params_failures", 0)
    return coord


def _make_api() -> MagicMock:
    """Create a mock API with the attributes entities read."""
    api = MagicMock()
    api.uid = "test-uid"
    api.model_id = "ecoMAX360i"
    api.host = "http://test"
    api.sw_rev = "1.0"
    api.hw_ver = "hw1"
    return api


# ============================================================================
# _with_health
# ============================================================================


class TestWithHealth:
    """Test the coordinator health-metadata wrapper."""

    def test_online_fresh_data_is_not_stale(self):
        now = time.time()
        coord = _bare_coordinator(last_success_ts=now)

        result = coord._with_health({"regParams": {"tempCO": 50}}, online=True)
        health = result["_health"]

        assert health["online"] is True
        assert health["stale"] is False
        assert health["stale_seconds"] < 5
        assert health["stale_after_seconds"] == STALE_AFTER_SECONDS
        assert result["regParams"] == {"tempCO": 50}
        assert "_ts" in result

    def test_includes_poll_intervals_and_failures(self):
        coord = _bare_coordinator(
            last_success_ts=time.time(),
            poll_reg_params=20,
            poll_sys_params=120,
            poll_edit_params=0,
            consecutive_failures=2,
            edit_params_failures=1,
            last_error="boom",
        )

        health = coord._with_health({}, online=False)["_health"]

        assert health["poll_reg_params"] == 20
        assert health["poll_sys_params"] == 120
        assert health["poll_edit_params"] == 0
        assert health["consecutive_failures"] == 2
        assert health["edit_params_failures"] == 1
        assert health["last_error"] == "boom"

    def test_marks_stale_when_last_success_is_old(self):
        old = time.time() - (STALE_AFTER_SECONDS + 30)
        coord = _bare_coordinator(last_success_ts=old)

        health = coord._with_health({}, online=False)["_health"]

        assert health["online"] is False
        assert health["stale"] is True
        assert health["stale_seconds"] >= STALE_AFTER_SECONDS

    def test_never_succeeded_is_not_stale(self):
        coord = _bare_coordinator(last_success_ts=0.0)

        health = coord._with_health({}, online=True)["_health"]

        assert health["stale"] is False
        assert health["stale_seconds"] == 0

    def test_falls_back_to_payload_last_success_ts(self):
        old = time.time() - 100
        coord = _bare_coordinator(last_success_ts=0.0)

        health = coord._with_health(
            {"_health": {"last_success_ts": old}}, online=False
        )["_health"]

        assert health["last_success_ts"] == old
        assert 95 <= health["stale_seconds"] <= 120

    def test_does_not_mutate_input_payload(self):
        payload = {"regParams": {"tempCO": 1}}
        coord = _bare_coordinator(last_success_ts=time.time())

        coord._with_health(payload, online=True)

        assert "_health" not in payload


# ============================================================================
# failure / success bookkeeping
# ============================================================================


class TestFailureBookkeeping:
    """Test failure counter, last-error capture and repair-issue handling."""

    def test_failed_update_increments_and_records_error(self):
        coord = _bare_coordinator(consecutive_failures=0)
        coord.hass = MagicMock()
        coord._config_entry = MagicMock(entry_id="e1")

        with patch("custom_components.econet300.common.async_create_issue") as create:
            coord._on_failed_update(ValueError("connection refused"))

        assert coord._consecutive_failures == 1
        assert coord._last_failure_ts > 0
        assert coord._last_error == "connection refused"
        create.assert_not_called()

    def test_failed_update_creates_issue_at_threshold(self):
        coord = _bare_coordinator(
            consecutive_failures=CONSECUTIVE_FAILURES_THRESHOLD - 1
        )
        coord.hass = MagicMock()
        coord._config_entry = MagicMock(entry_id="e1")

        with patch("custom_components.econet300.common.async_create_issue") as create:
            coord._on_failed_update(TimeoutError())

        assert coord._consecutive_failures == CONSECUTIVE_FAILURES_THRESHOLD
        create.assert_called_once()

    def test_failed_update_uses_class_name_when_message_empty(self):
        coord = _bare_coordinator(consecutive_failures=0)
        coord.hass = MagicMock()
        coord._config_entry = MagicMock(entry_id="e1")

        with patch("custom_components.econet300.common.async_create_issue"):
            coord._on_failed_update(TimeoutError())

        assert coord._last_error == "TimeoutError"

    def test_successful_update_resets_and_clears_issue(self):
        coord = _bare_coordinator(consecutive_failures=3)
        coord.hass = MagicMock()
        coord._config_entry = MagicMock(entry_id="e1")

        with patch("custom_components.econet300.common.async_delete_issue") as delete:
            coord._on_successful_update()

        assert coord._consecutive_failures == 0
        delete.assert_called_once()


# ============================================================================
# EconetOnlineBinarySensor
# ============================================================================


class TestEconetOnlineBinarySensor:
    """Test the live-polling connectivity diagnostic sensor."""

    def _sensor(self, data) -> EconetOnlineBinarySensor:
        coordinator = MagicMock()
        coordinator.data = data
        return EconetOnlineBinarySensor(coordinator, _make_api())

    def test_unique_id(self):
        sensor = self._sensor({"_health": {"online": True}})
        assert sensor.unique_id == "test-uid-health-online"

    def test_is_on_true_when_online(self):
        sensor = self._sensor({"_health": {"online": True}})
        assert sensor.available is True
        assert sensor.is_on is True

    def test_is_on_false_when_offline(self):
        sensor = self._sensor({"_health": {"online": False}})
        assert sensor.is_on is False

    def test_unavailable_without_data(self):
        sensor = self._sensor(None)
        assert sensor.available is False
        assert sensor.is_on is False

    def test_extra_state_attributes(self):
        sensor = self._sensor(
            {
                "_health": {
                    "online": True,
                    "stale": False,
                    "stale_seconds": 7,
                    "consecutive_failures": 0,
                    "poll_reg_params": 15,
                }
            }
        )
        attrs = sensor.extra_state_attributes
        assert attrs["stale_seconds"] == 7
        assert attrs["poll_reg_params"] == 15
        assert "last_error" in attrs


# ============================================================================
# EconetHealthSensor
# ============================================================================


class TestEconetHealthSensor:
    """Test the coordinator-health diagnostic sensors."""

    def _coordinator(self, health) -> MagicMock:
        coordinator = MagicMock()
        coordinator.data = {"_health": health}
        return coordinator

    def test_numeric_value_passthrough(self):
        coordinator = self._coordinator({"stale_seconds": 42})
        sensor = EconetHealthSensor(
            coordinator,
            _make_api(),
            "stale_seconds",
            "health_data_age",
            device_class=SensorDeviceClass.DURATION,
            state_class=SensorStateClass.MEASUREMENT,
        )
        assert sensor.native_value == 42
        assert sensor._attr_suggested_display_precision == 0

    def test_consecutive_failures_value(self):
        coordinator = self._coordinator({"consecutive_failures": 3})
        sensor = EconetHealthSensor(
            coordinator, _make_api(), "consecutive_failures", "health_consecutive_failures"
        )
        assert sensor.native_value == 3

    def test_timestamp_value_is_timezone_aware(self):
        ts = 1700000000.0
        coordinator = self._coordinator({"last_success_ts": ts})
        sensor = EconetHealthSensor(
            coordinator,
            _make_api(),
            "last_success_ts",
            "health_last_success",
            device_class=SensorDeviceClass.TIMESTAMP,
        )
        assert sensor.native_value == datetime.fromtimestamp(ts, tz=UTC)
        assert sensor._attr_suggested_display_precision is None

    def test_timestamp_zero_is_none(self):
        coordinator = self._coordinator({"last_success_ts": 0})
        sensor = EconetHealthSensor(
            coordinator,
            _make_api(),
            "last_success_ts",
            "health_last_success",
            device_class=SensorDeviceClass.TIMESTAMP,
        )
        assert sensor.native_value is None

    def test_unavailable_without_data(self):
        coordinator = MagicMock()
        coordinator.data = None
        sensor = EconetHealthSensor(
            coordinator, _make_api(), "stale_seconds", "health_data_age"
        )
        assert sensor.available is False


# ============================================================================
# polling_settings options flow
# ============================================================================


class _PollingFlowMocks(NamedTuple):
    """Options-flow handler with typed MagicMock stand-ins for HA flow methods."""

    handler: EconetOptionsFlowHandler
    hass: MagicMock
    show_form: MagicMock
    create_entry: MagicMock


class TestPollingSettingsOptionsFlow:
    """Test the polling-settings options-flow step."""

    def _handler(self) -> _PollingFlowMocks:
        handler = EconetOptionsFlowHandler()
        hass = MagicMock()
        handler.hass = hass
        show_form = MagicMock(return_value={"type": "form"})
        create_entry = MagicMock(return_value={"type": "create_entry"})
        handler.async_show_form = show_form
        handler.async_create_entry = create_entry
        return _PollingFlowMocks(handler, hass, show_form, create_entry)

    @pytest.mark.asyncio
    async def test_form_uses_defaults_when_unconfigured(self):
        mocks = self._handler()
        with patch.object(
            EconetOptionsFlowHandler, "config_entry", new_callable=PropertyMock
        ) as cfg:
            cfg.return_value = MagicMock(options={})
            await mocks.handler.async_step_polling_settings(None)

        mocks.show_form.assert_called_once()
        kwargs = mocks.show_form.call_args.kwargs
        assert kwargs["step_id"] == "polling_settings"

        defaults = {
            marker.schema: marker.default()
            for marker in kwargs["data_schema"].schema
        }
        assert defaults[CONF_POLL_REG_PARAMS] == DEFAULT_POLL_REG_PARAMS
        assert defaults[CONF_POLL_SYS_PARAMS] == DEFAULT_POLL_SYS_PARAMS
        assert defaults[CONF_POLL_EDIT_PARAMS] == DEFAULT_POLL_EDIT_PARAMS

    @pytest.mark.asyncio
    async def test_form_uses_existing_options_as_defaults(self):
        mocks = self._handler()
        with patch.object(
            EconetOptionsFlowHandler, "config_entry", new_callable=PropertyMock
        ) as cfg:
            cfg.return_value = MagicMock(options={CONF_POLL_REG_PARAMS: 30})
            await mocks.handler.async_step_polling_settings(None)

        kwargs = mocks.show_form.call_args.kwargs
        defaults = {
            marker.schema: marker.default()
            for marker in kwargs["data_schema"].schema
        }
        assert defaults[CONF_POLL_REG_PARAMS] == 30

    @pytest.mark.asyncio
    async def test_submit_saves_options_and_reloads(self):
        mocks = self._handler()
        user_input = {
            CONF_POLL_REG_PARAMS: 20,
            CONF_POLL_SYS_PARAMS: 120,
            CONF_POLL_EDIT_PARAMS: 0,
        }
        with patch.object(
            EconetOptionsFlowHandler, "config_entry", new_callable=PropertyMock
        ) as cfg:
            cfg.return_value = MagicMock(options={"existing": True}, entry_id="e1")
            await mocks.handler.async_step_polling_settings(user_input)

        mocks.create_entry.assert_called_once()
        saved = mocks.create_entry.call_args.kwargs["data"]
        assert saved[CONF_POLL_REG_PARAMS] == 20
        assert saved[CONF_POLL_EDIT_PARAMS] == 0
        assert saved["existing"] is True
        mocks.hass.config_entries.async_reload.assert_called_once_with("e1")
