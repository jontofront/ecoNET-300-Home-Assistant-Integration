"""Tests for RM endpoint probe and legacy-only coordinator behavior."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.econet300.api import Econet300Api
from custom_components.econet300.common import EconetDataCoordinator
from custom_components.econet300.const import API_RM_DATA_KEY, RM_PROBE_TIMEOUT_SEC


class TestProbeRmSupport:
    """Test API.probe_rm_support()."""

    @pytest.mark.asyncio
    async def test_probe_returns_false_when_client_returns_none(self):
        """When get_with_short_timeout returns None, probe_rm_support returns False."""
        client = MagicMock()
        client.host = "http://192.168.1.1"
        client.get_with_short_timeout = AsyncMock(return_value=None)
        cache = MagicMock()
        api = Econet300Api(client, cache)
        api._uid = "test-uid"

        result = await api.probe_rm_support()

        assert result is False
        client.get_with_short_timeout.assert_called_once()
        call_kw = client.get_with_short_timeout.call_args
        assert call_kw[1]["timeout_sec"] == RM_PROBE_TIMEOUT_SEC

    @pytest.mark.asyncio
    async def test_probe_returns_false_when_response_has_no_data_key(self):
        """When response dict has no 'data' key, probe_rm_support returns False."""
        client = MagicMock()
        client.host = "http://192.168.1.1"
        client.get_with_short_timeout = AsyncMock(return_value={"other": "value"})
        cache = MagicMock()
        api = Econet300Api(client, cache)
        api._uid = "test-uid"

        result = await api.probe_rm_support()

        assert result is False

    @pytest.mark.asyncio
    async def test_probe_returns_true_when_response_has_data_key(self):
        """When response has API_RM_DATA_KEY, probe_rm_support returns True."""
        client = MagicMock()
        client.host = "http://192.168.1.1"
        client.get_with_short_timeout = AsyncMock(
            return_value={API_RM_DATA_KEY: [{"value": 1}]}
        )
        cache = MagicMock()
        api = Econet300Api(client, cache)
        api._uid = "test-uid"

        result = await api.probe_rm_support()

        assert result is True


class TestCoordinatorLegacyOnly:
    """Test coordinator skips RM/merged when probe returns False (legacy-only module)."""

    @pytest.mark.asyncio
    async def test_coordinator_skips_rm_and_merged_when_probe_false(
        self, hass, load_fixture
    ):
        """When probe_rm_support returns False, result has rmData={}, mergedData=None."""
        sys_params = load_fixture("ecoMAX860D3-HB", "sysParams.json") or {}
        reg_params = load_fixture("ecoMAX860D3-HB", "regParams.json") or {}
        reg_params_data = load_fixture("ecoMAX860D3-HB", "regParamsData.json") or {}

        mock_api = MagicMock(spec=Econet300Api)
        mock_api.fetch_sys_params = AsyncMock(return_value=sys_params)
        mock_api.fetch_param_edit_data = AsyncMock(return_value={})
        mock_api.fetch_reg_params = AsyncMock(return_value=reg_params)
        mock_api.fetch_reg_params_data = AsyncMock(return_value=reg_params_data)
        mock_api.probe_rm_support = AsyncMock(return_value=False)

        config_entry = MagicMock()
        config_entry.entry_id = "test-entry-id"
        config_entry.data = {"host": "192.168.1.1"}

        coordinator = EconetDataCoordinator(hass, mock_api, config_entry)
        coordinator._rm_supported = None

        result = await coordinator._async_update_data()

        assert result["sysParams"] == sys_params
        assert result["regParams"] == reg_params
        assert result["regParamsData"] == reg_params_data
        assert result["rmData"] == {}
        assert result["mergedData"] is None
        mock_api.probe_rm_support.assert_called_once()
        mock_api.fetch_merged_rm_data.assert_not_called()
