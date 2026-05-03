"""Tests for ecoNET300 diagnostics functionality.

Tests data redaction, diagnostic functions availability, and edge cases.
"""

from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.econet300.diagnostics import (
    RAW_PROBE_ENDPOINTS,
    TO_REDACT,
    _redact_data,
    _snapshot_extended_fetch_result,
    async_collect_extended_endpoint_snapshots,
    async_collect_raw_endpoint_probes,
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
        api.fetch_raw_endpoint = AsyncMock(
            return_value={"status": 200, "body": {}, "error": None}
        )

        out = await async_collect_extended_endpoint_snapshots(api)

        assert out["edit_params"] == {"edit": True}
        assert "_ha_diagnostics_fetch_failed" in out["rm_params_names"]
        assert out["rm_params_data"]["_ha_diagnostics_unavailable"] is True
        assert "raw_probes" in out
        assert isinstance(out["raw_probes"], dict)


class TestRawEndpointProbes:
    """Raw probes that capture HTTP status + body for diagnostic-only endpoints."""

    def test_probe_list_covers_known_diagnostic_endpoints(self):
        """The probe list must include the endpoints reported in issue #231."""
        keys = {key for key, _, _ in RAW_PROBE_ENDPOINTS}
        # See issue #231: device-side errors on these endpoints distinguish
        # heat-pump (gm3_pomp) variants from boiler controllers.
        assert "rm_device_list" in keys
        assert "rm_current_data_object" in keys
        assert "legacy_sys" in keys
        assert "rm_params_data_no_uid" in keys

    def test_probe_list_uses_correct_endpoint_paths(self):
        """Endpoint paths must match the live API names (no leading slash)."""
        spec = {
            key: (endpoint, with_uid) for key, endpoint, with_uid in RAW_PROBE_ENDPOINTS
        }
        assert spec["rm_device_list"] == ("rmDeviceList", False)
        assert spec["rm_current_data_object"] == ("rmCurrentDataObject", False)
        assert spec["legacy_sys"] == ("sys", False)

    @pytest.mark.asyncio
    async def test_probes_capture_status_and_body(self):
        """A successful probe should preserve status + body verbatim."""
        api = MagicMock()
        api.fetch_raw_endpoint = AsyncMock(
            return_value={"status": 200, "body": {"k": "v"}, "error": None}
        )
        out = await async_collect_raw_endpoint_probes(api, timeout_sec=1.0)

        assert set(out.keys()) == {key for key, _, _ in RAW_PROBE_ENDPOINTS}
        for probe in out.values():
            assert probe["status"] == 200
            assert probe["body"] == {"k": "v"}
            assert probe["error"] is None

    @pytest.mark.asyncio
    async def test_probes_capture_device_error_payloads(self):
        """A 200 response containing the device's error string must be preserved."""
        # Heat-pump gm3_pomp returns 200 + JSON error body for unsupported endpoints.
        api = MagicMock()
        api.fetch_raw_endpoint = AsyncMock(
            return_value={
                "status": 200,
                "body": {
                    "error": "'Controller' object has no attribute 'onrmDeviceList'"
                },
                "error": None,
            }
        )
        out = await async_collect_raw_endpoint_probes(api)
        assert (
            out["rm_device_list"]["body"]["error"]
            == "'Controller' object has no attribute 'onrmDeviceList'"
        )

    @pytest.mark.asyncio
    async def test_probes_isolate_per_endpoint_failures(self):
        """A raised exception on one probe must not break the others."""
        api = MagicMock()
        results_iter = iter(
            [
                {"status": 200, "body": {}, "error": None},
                Exception("boom"),
                {"status": 404, "body": None, "error": None},
                {"status": None, "body": None, "error": "TimeoutError()"},
            ]
        )

        async def fake_fetch(*_args, **_kwargs):
            value = next(results_iter)
            if isinstance(value, Exception):
                raise value
            return value

        api.fetch_raw_endpoint = AsyncMock(side_effect=fake_fetch)
        out = await async_collect_raw_endpoint_probes(api)

        # All probes are present even though one raised
        assert len(out) == len(RAW_PROBE_ENDPOINTS)
        # The raising probe is captured as an error dict
        any_with_error = [p for p in out.values() if p.get("error")]
        assert any_with_error, "expected at least one probe to surface an error"


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


class TestDiagnosticsReportSummary:
    """Pure-function summary used by the options-flow diagnostics step."""

    def _summarize(self, **overrides):
        from custom_components.econet300.config_flow import EconetOptionsFlowHandler

        defaults = {
            "sys_params": {
                "controllerID": "ecoMAX360i",
                "protocolType": "gm3_pomp",
                "uid": "ABCDEF",
            },
            "reg_params": {"TempCWU": 47.5, "TempBuforDown": 37.6},
            "extended": {
                "raw_probes": {
                    "rm_device_list": {"status": 200, "body": {}, "error": None},
                    "legacy_sys": {"status": None, "body": None, "error": "Timeout()"},
                }
            },
            "errors": [],
        }
        defaults.update(overrides)
        return EconetOptionsFlowHandler._summarize_report(  # noqa: SLF001
            defaults["sys_params"],
            defaults["reg_params"],
            defaults["extended"],
            defaults["errors"],
        )

    def test_summary_includes_controller_and_protocol(self):
        """Summary should surface controllerID and protocolType for triage."""
        summary = self._summarize()
        assert "ecoMAX360i" in summary
        assert "gm3_pomp" in summary

    def test_summary_reports_uid_presence(self):
        """UID presence is the most common config-flow failure cause; surface it."""
        with_uid = self._summarize()
        assert "uid in sysParams: True" in with_uid

        without_uid = self._summarize(
            sys_params={"controllerID": "ecoMAX360i", "protocolType": "gm3_pomp"}
        )
        assert "uid in sysParams: False" in without_uid

    def test_summary_includes_reg_params_count(self):
        """A non-zero reg_params count tells us the device is responsive."""
        summary = self._summarize()
        assert "regParams keys: 2" in summary

    def test_summary_includes_raw_probe_status_lines(self):
        """Each raw probe should contribute one status line."""
        summary = self._summarize()
        assert "rm_device_list: status=200" in summary
        # Probes with errors include the error repr
        assert "legacy_sys" in summary
        assert "Timeout()" in summary

    def test_summary_handles_collection_errors(self):
        """Collection errors are surfaced as their own block."""
        summary = self._summarize(errors=["sysParams: TimeoutError()"])
        assert "Collection errors:" in summary
        assert "sysParams: TimeoutError()" in summary

    def test_summary_handles_non_dict_sys_params(self):
        """Defensive: sys_params can be None when fetch fails."""
        summary = self._summarize(sys_params=None, reg_params=None)
        assert "controllerID:" in summary
        assert "regParams keys: 0" in summary

    def test_summary_mentions_log_marker(self):
        """User must know which log marker to grep for."""
        summary = self._summarize()
        assert "ECONET300_DIAGNOSTICS_REPORT" in summary


class TestApiRawEndpointHelper:
    """Econet300Api.fetch_raw_endpoint() URL construction + delegation."""

    @pytest.mark.asyncio
    async def test_fetch_raw_endpoint_without_uid(self):
        """URL is built without a uid query string when with_uid=False."""
        from custom_components.econet300.api import Econet300Api
        from custom_components.econet300.mem_cache import MemCache

        client = MagicMock()
        client.host = "http://192.168.1.100"
        client.probe_raw = AsyncMock(
            return_value={"status": 200, "body": {}, "error": None}
        )

        api = Econet300Api(client, MemCache())
        await api.fetch_raw_endpoint("rmDeviceList", timeout_sec=2.5)

        client.probe_raw.assert_awaited_once_with(
            "http://192.168.1.100/econet/rmDeviceList", timeout_sec=2.5
        )

    @pytest.mark.asyncio
    async def test_fetch_raw_endpoint_with_uid_appends_query(self):
        """URL appends ?uid=<uid> when with_uid=True."""
        from custom_components.econet300.api import Econet300Api
        from custom_components.econet300.mem_cache import MemCache

        client = MagicMock()
        client.host = "http://192.168.1.100"
        client.probe_raw = AsyncMock(
            return_value={"status": 200, "body": {}, "error": None}
        )

        api = Econet300Api(client, MemCache())
        api._uid = "TEST_UID"  # noqa: SLF001 — direct attr access OK in tests
        await api.fetch_raw_endpoint("rmParamsData", with_uid=True, timeout_sec=1.0)

        client.probe_raw.assert_awaited_once_with(
            "http://192.168.1.100/econet/rmParamsData?uid=TEST_UID", timeout_sec=1.0
        )


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
