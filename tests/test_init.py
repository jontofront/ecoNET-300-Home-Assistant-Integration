"""Tests for the ecoNET300 integration initialization and setup."""

from unittest.mock import AsyncMock, MagicMock, patch

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
import pytest

from custom_components.econet300 import (
    DOMAIN,
    SERVICE_API,
    SERVICE_COORDINATOR,
    _cleanup_ghost_devices,
    async_remove_entry,
    async_setup_entry,
    async_unload_entry,
)
from custom_components.econet300.api import AuthError, Econet300Api
from custom_components.econet300.common import EconetDataCoordinator


class TestIntegrationSetup:
    """Test the integration setup and teardown."""

    @pytest.mark.asyncio
    async def test_async_setup_entry_success(
        self, hass: HomeAssistant, mock_config_entry
    ):
        """Test successful integration setup."""
        mock_api = MagicMock(spec=Econet300Api)
        mock_api.uid = "test_uid"

        mock_coordinator = MagicMock(spec=EconetDataCoordinator)
        mock_coordinator.async_config_entry_first_refresh = AsyncMock()

        with (
            patch("custom_components.econet300.make_api", return_value=mock_api),
            patch(
                "custom_components.econet300.EconetDataCoordinator",
                return_value=mock_coordinator,
            ),
            patch(
                "custom_components.econet300._cleanup_ghost_devices"
            ),
        ):
            result = await async_setup_entry(hass, mock_config_entry)

            assert result is True
            assert DOMAIN in hass.data
            assert mock_config_entry.entry_id in hass.data[DOMAIN]
            assert SERVICE_API in hass.data[DOMAIN][mock_config_entry.entry_id]
            assert SERVICE_COORDINATOR in hass.data[DOMAIN][mock_config_entry.entry_id]

    @pytest.mark.asyncio
    async def test_async_setup_entry_auth_error(
        self, hass: HomeAssistant, mock_config_entry
    ):
        """Test integration setup with authentication error."""
        with (
            patch(
                "custom_components.econet300.make_api",
                side_effect=AuthError("Invalid credentials"),
            ),
            pytest.raises(ConfigEntryAuthFailed),
        ):
            await async_setup_entry(hass, mock_config_entry)

    @pytest.mark.asyncio
    async def test_async_setup_entry_timeout_error(
        self, hass: HomeAssistant, mock_config_entry
    ):
        """Test integration setup with timeout error."""
        with (
            patch(
                "custom_components.econet300.make_api",
                side_effect=TimeoutError("Connection timeout"),
            ),
            pytest.raises(ConfigEntryNotReady),
        ):
            await async_setup_entry(hass, mock_config_entry)

    @pytest.mark.asyncio
    async def test_async_setup_entry_connection_error(
        self, hass: HomeAssistant, mock_config_entry
    ):
        """Test integration setup when device is offline (sysParams unavailable)."""
        with (
            patch(
                "custom_components.econet300.make_api",
                side_effect=ConnectionError("Device offline"),
            ),
            pytest.raises(ConfigEntryNotReady),
        ):
            await async_setup_entry(hass, mock_config_entry)

    @pytest.mark.asyncio
    async def test_async_setup_entry_value_error(
        self, hass: HomeAssistant, mock_config_entry
    ):
        """Test integration setup when UID is missing from sysParams."""
        with (
            patch(
                "custom_components.econet300.make_api",
                side_effect=ValueError("Missing uid"),
            ),
            pytest.raises(ConfigEntryNotReady),
        ):
            await async_setup_entry(hass, mock_config_entry)

    @pytest.mark.asyncio
    async def test_async_unload_entry_success(
        self, hass: HomeAssistant, mock_config_entry
    ):
        """Test successful integration unload."""
        # Setup integration data
        hass.data[DOMAIN] = {
            mock_config_entry.entry_id: {
                SERVICE_API: MagicMock(),
                SERVICE_COORDINATOR: MagicMock(),
            }
        }

        # No need to patch since it's mocked in the hass fixture
        result = await async_unload_entry(hass, mock_config_entry)

        assert result is True
        assert mock_config_entry.entry_id not in hass.data[DOMAIN]

    @pytest.mark.asyncio
    async def test_async_unload_entry_failure(
        self, hass: HomeAssistant, mock_config_entry
    ):
        """Test integration unload failure."""
        # Setup integration data
        hass.data[DOMAIN] = {
            mock_config_entry.entry_id: {
                SERVICE_API: MagicMock(),
                SERVICE_COORDINATOR: MagicMock(),
            }
        }

        # Mock the unload to return False for this test
        with patch.object(
            hass.config_entries, "async_unload_platforms", return_value=False
        ):
            result = await async_unload_entry(hass, mock_config_entry)

        assert result is False
        # Data should still be present since unload failed
        assert mock_config_entry.entry_id in hass.data[DOMAIN]

    @pytest.mark.asyncio
    async def test_async_unload_entry_no_data(
        self, hass: HomeAssistant, mock_config_entry
    ):
        """Test integration unload when no data exists."""
        # Ensure no integration data
        hass.data[DOMAIN] = {}

        # No need to patch since it's mocked in the hass fixture
        result = await async_unload_entry(hass, mock_config_entry)

        assert result is True
        # Should not raise an error even if no data exists

    @pytest.mark.asyncio
    async def test_async_remove_entry_cleans_up_issues(
        self, hass: HomeAssistant, mock_config_entry
    ):
        """Test that async_remove_entry cleans up repair issues."""
        with patch(
            "custom_components.econet300.async_delete_issue"
        ) as mock_delete_issue:
            await async_remove_entry(hass, mock_config_entry)

            mock_delete_issue.assert_called_once_with(
                hass,
                DOMAIN,
                f"connection_failed_{mock_config_entry.entry_id}",
            )


class TestGhostDeviceCleanup:
    """Test ghost device cleanup logic."""

    def test_cleanup_handles_missing_device_registry(
        self, hass: HomeAssistant, mock_config_entry
    ):
        """Test cleanup doesn't crash when device registry is unavailable."""
        with patch(
            "custom_components.econet300.dr.async_get",
            side_effect=Exception("Not loaded"),
        ):
            _cleanup_ghost_devices(hass, mock_config_entry, "real-uid")

    def test_cleanup_removes_ghost_device(
        self, hass: HomeAssistant, mock_config_entry
    ):
        """Test cleanup removes a device with default-uid identifier."""
        mock_device = MagicMock()
        mock_device.id = "ghost_device_id"
        mock_device.name = "Ghost Boiler"

        mock_reg = MagicMock()
        mock_reg.async_get_device.side_effect = (
            lambda identifiers: mock_device
            if (DOMAIN, "default-uid") in identifiers
            else None
        )

        with patch(
            "custom_components.econet300.dr.async_get", return_value=mock_reg
        ):
            _cleanup_ghost_devices(hass, mock_config_entry, "real-uid")

        mock_reg.async_remove_device.assert_called()

    def test_cleanup_no_ghost_devices(
        self, hass: HomeAssistant, mock_config_entry
    ):
        """Test cleanup does nothing when no ghost devices exist."""
        mock_reg = MagicMock()
        mock_reg.async_get_device.return_value = None

        with patch(
            "custom_components.econet300.dr.async_get", return_value=mock_reg
        ):
            _cleanup_ghost_devices(hass, mock_config_entry, "real-uid")

        mock_reg.async_remove_device.assert_not_called()

    def test_cleanup_handles_attribute_error(
        self, hass: HomeAssistant, mock_config_entry
    ):
        """Test cleanup handles partially initialized device registry."""
        mock_reg = MagicMock()
        mock_reg.async_get_device.side_effect = AttributeError("No devices attr")

        with patch(
            "custom_components.econet300.dr.async_get", return_value=mock_reg
        ):
            _cleanup_ghost_devices(hass, mock_config_entry, "real-uid")
