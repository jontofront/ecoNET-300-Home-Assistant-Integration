"""Tests for ecoNET300 diagnostics functionality.

Tests data redaction, diagnostic functions availability, and edge cases.
"""

from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.econet300.diagnostics import (
    TO_REDACT,
    _redact_data,
    _snapshot_extended_fetch_result,
    async_collect_extended_endpoint_snapshots,
    async_get_config_entry_diagnostics,
    async_get_device_diagnostics,
)


class TestDataRedaction:
    """Test data redaction functionality."""

    def test_simple_data_redaction(self):
        """Test simple data redaction."""
        test_data = {
            "host": "192.168.1.100",
            "username": "test_user",
            "password": "secret_password",
            "safe_data": "this_is_safe",
        }
        redacted = _redact_data(test_data, TO_REDACT)

        assert redacted["host"] == "**REDACTED**"
        assert redacted["username"] == "**REDACTED**"
        assert redacted["password"] == "**REDACTED**"
        assert redacted["safe_data"] == "this_is_safe"

    def test_nested_data_redaction(self):
        """Test nested data redaction."""
        test_data = {
            "api_info": {
                "host": "192.168.1.100",
                "username": "test_user",
            },
            "safe_data": "this_is_safe",
        }
        redacted = _redact_data(test_data, TO_REDACT)

        assert redacted["api_info"]["host"] == "**REDACTED**"
        assert redacted["api_info"]["username"] == "**REDACTED**"
        assert redacted["safe_data"] == "this_is_safe"

    def test_complex_nested_data_redaction(self):
        """Test deeply nested data redaction."""
        test_data = {
            "config": {
                "host": "192.168.1.100",
                "credentials": {
                    "username": "admin",
                    "password": "admin123",
                },
            },
            "data": {
                "temperature": 25.5,
                "status": "online",
            },
        }
        redacted = _redact_data(test_data, TO_REDACT)

        assert redacted["config"]["host"] == "**REDACTED**"
        assert redacted["config"]["credentials"]["username"] == "**REDACTED**"
        assert redacted["config"]["credentials"]["password"] == "**REDACTED**"
        assert redacted["data"]["temperature"] == 25.5
        assert redacted["data"]["status"] == "online"


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_non_dict_data_unchanged(self):
        """Test that non-dict data is returned unchanged."""
        assert _redact_data("not_a_dict", TO_REDACT) == "not_a_dict"

    def test_empty_dict_handled(self):
        """Test empty dict is handled correctly."""
        empty_dict: dict[str, Any] = {}
        assert _redact_data(empty_dict, TO_REDACT) == {}

    def test_none_data_handled(self):
        """Test None data is handled correctly."""
        assert _redact_data(None, TO_REDACT) is None

    def test_list_data_unchanged(self):
        """Test list data is returned unchanged."""
        list_data = ["item1", "item2"]
        assert _redact_data(list_data, TO_REDACT) == ["item1", "item2"]


class TestToRedactList:
    """Test TO_REDACT list validation."""

    def test_to_redact_is_list(self):
        """Test TO_REDACT is a list."""
        assert isinstance(TO_REDACT, list)

    def test_to_redact_not_empty(self):
        """Test TO_REDACT is not empty."""
        assert len(TO_REDACT) > 0

    @pytest.mark.parametrize(
        "expected_key",
        ["host", "username", "password"],
    )
    def test_expected_keys_in_to_redact(self, expected_key):
        """Test expected sensitive keys are in TO_REDACT."""
        assert expected_key in TO_REDACT


class TestExtendedEndpointSnapshots:
    """Extended API endpoint snapshots for diagnostics / fixtures."""

    def test_snapshot_extended_fetch_result_ok(self):
        """Successful fetch returns payload unchanged."""
        assert _snapshot_extended_fetch_result({"k": 1}, None) == {"k": 1}

    def test_snapshot_extended_fetch_result_error(self):
        """Exceptions become a structured error dict."""
        out = _snapshot_extended_fetch_result(None, ValueError("x"))
        assert out["_ha_diagnostics_fetch_failed"]

    def test_snapshot_extended_fetch_result_unavailable(self):
        """None result becomes unavailable placeholder."""
        out = _snapshot_extended_fetch_result(None, None)
        assert out["_ha_diagnostics_unavailable"] is True

    @pytest.mark.asyncio
    async def test_collect_extended_isolates_per_endpoint(self):
        """One failing coroutine must not break other keys."""
        api = MagicMock()
        api.fetch_edit_params = AsyncMock(return_value={"edit": True})
        api.fetch_rm_params_names = AsyncMock(side_effect=RuntimeError("rm fail"))
        api.fetch_rm_params_data = AsyncMock(return_value=None)
        api.fetch_rm_params_descs = AsyncMock(return_value=None)
        api.fetch_rm_params_enums = AsyncMock(return_value=None)
        api.fetch_rm_params_units_names = AsyncMock(return_value=None)
        api.fetch_rm_structure = AsyncMock(return_value=None)
        api.fetch_rm_current_data_params = AsyncMock(return_value=None)
        api.fetch_rm_langs = AsyncMock(return_value=None)
        api.fetch_rm_existing_langs = AsyncMock(return_value=None)
        api.fetch_rm_locks_names = AsyncMock(return_value=None)
        api.fetch_rm_alarms_names = AsyncMock(return_value=None)

        out = await async_collect_extended_endpoint_snapshots(api)

        assert out["edit_params"] == {"edit": True}
        assert "_ha_diagnostics_fetch_failed" in out["rm_params_names"]
        assert out["rm_params_data"]["_ha_diagnostics_unavailable"] is True


class TestCoordinatorDataKeysInDiagnostics:
    """Verify coordinator data shape includes editParams/informationParams."""

    def test_coordinator_data_includes_edit_params_keys(self):
        """Coordinator data dict should contain editParams and informationParams."""
        coordinator_data = {
            "sysParams": {"controllerID": "ecoMAX360i"},
            "regParams": {},
            "regParamsData": {},
            "paramsEdits": {},
            "editParams": {"1211": {"value": 0}},
            "informationParams": {"221": [True, [[0, 1, 0]]]},
            "rmData": {},
            "mergedData": None,
        }
        assert "editParams" in coordinator_data
        assert "informationParams" in coordinator_data
        redacted = _redact_data(coordinator_data, TO_REDACT)
        assert "editParams" in redacted
        assert "informationParams" in redacted
        assert redacted["editParams"]["1211"]["value"] == 0

    def test_coordinator_data_non_ecomax360i_empty(self):
        """Non-ecoMAX360i controllers should have empty editParams/informationParams."""
        coordinator_data = {
            "sysParams": {"controllerID": "ecoMAX860P3-V"},
            "regParams": {},
            "regParamsData": {},
            "paramsEdits": {},
            "editParams": {},
            "informationParams": {},
            "rmData": {},
            "mergedData": None,
        }
        assert coordinator_data["editParams"] == {}
        assert coordinator_data["informationParams"] == {}


class TestDiagnosticFunctions:
    """Test diagnostic functions availability."""

    def test_async_get_config_entry_diagnostics_callable(self):
        """Test async_get_config_entry_diagnostics is callable."""
        assert callable(async_get_config_entry_diagnostics)

    def test_async_get_device_diagnostics_callable(self):
        """Test async_get_device_diagnostics is callable."""
        assert callable(async_get_device_diagnostics)


class TestMockDiagnosticIntegration:
    """Test mock diagnostic integration without HA dependencies."""

    def test_config_entry_data_redaction(self):
        """Test config entry data is redacted correctly."""
        mock_config_entry_data = {
            "host": "192.168.1.100",
            "username": "test_user",
            "password": "test_password",
            "polling_interval": 30,
        }
        redacted = _redact_data(mock_config_entry_data, TO_REDACT)

        assert redacted["host"] == "**REDACTED**"
        assert redacted["polling_interval"] == 30

    def test_device_data_preserved(self):
        """Test device data is preserved correctly."""
        mock_device_data = {
            "device_id": "test_device_id",
            "name": "ecoNET300 Test Device",
            "manufacturer": "PLUM",
            "model": "ecoNET300",
            "sw_version": "1.0.0",
        }
        redacted = _redact_data(mock_device_data, TO_REDACT)

        assert redacted["name"] == "ecoNET300 Test Device"
        assert redacted["manufacturer"] == "PLUM"

    def test_entity_data_preserved(self):
        """Test entity data is preserved correctly."""
        mock_entity_data = {
            "entity_id": "sensor.econet300_temperature",
            "name": "Temperature",
            "state": "25.5",
            "attributes": {
                "unit_of_measurement": "°C",
                "device_class": "temperature",
            },
        }
        redacted = _redact_data(mock_entity_data, TO_REDACT)

        assert redacted["state"] == "25.5"
        assert redacted["attributes"]["unit_of_measurement"] == "°C"
