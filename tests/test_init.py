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
    async_remove_config_entry_device,
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
        # Mock the API creation
        mock_api = MagicMock(spec=Econet300Api)
        mock_api.uid = "test_uid"

        # Mock the coordinator
        mock_coordinator = MagicMock(spec=EconetDataCoordinator)
        mock_coordinator.async_config_entry_first_refresh = AsyncMock()

        device_registry = MagicMock()
        device_registry.async_get_device.return_value = None
        device_registry.async_get_device_by_identifier.return_value = None

        # Platforms link their devices to the controller device by its
        # registry id, so it must exist before they are set up.
        def check_controller_device_registered(*_args):
            device_registry.async_get_or_create.assert_called_once()
            return True

        forward_entry_setups = AsyncMock(side_effect=check_controller_device_registered)

        with (
            patch("custom_components.econet300.make_api", return_value=mock_api),
            patch(
                "custom_components.econet300.EconetDataCoordinator",
                return_value=mock_coordinator,
            ),
            patch(
                "custom_components.econet300.dr.async_get",
                return_value=device_registry,
            ),
            patch.object(
                hass.config_entries,
                "async_forward_entry_setups",
                forward_entry_setups,
            ),
        ):
            result = await async_setup_entry(hass, mock_config_entry)

            assert result is True
            assert DOMAIN in hass.data
            assert mock_config_entry.entry_id in hass.data[DOMAIN]
            assert SERVICE_API in hass.data[DOMAIN][mock_config_entry.entry_id]
            assert SERVICE_COORDINATOR in hass.data[DOMAIN][mock_config_entry.entry_id]

        create_kwargs = device_registry.async_get_or_create.call_args.kwargs
        assert create_kwargs["config_entry_id"] == mock_config_entry.entry_id
        assert create_kwargs["identifiers"] == {(DOMAIN, "test_uid")}
        assert (
            mock_coordinator.controller_device_id
            == device_registry.async_get_or_create.return_value.id
        )
        forward_entry_setups.assert_awaited_once()

    @pytest.mark.parametrize("supports_via_device_id", [True, False])
    def test_cleanup_ghost_devices_removes_default_uid_devices(
        self, mock_config_entry, supports_via_device_id
    ):
        """Test devices left by a failed init with the default uid are removed."""
        ghost_identifier = (DOMAIN, "default-uid-mixer-2")
        ghost_device = MagicMock(id="ghost-device-id")

        def get_device_by_identifier(identifier, _config_entry_id):
            return ghost_device if identifier == ghost_identifier else None

        def get_device(identifiers):
            return ghost_device if ghost_identifier in identifiers else None

        device_registry = MagicMock()
        device_registry.async_get_device_by_identifier.side_effect = (
            get_device_by_identifier
        )
        device_registry.async_get_device.side_effect = get_device

        with (
            patch(
                "custom_components.econet300.dr.async_get",
                return_value=device_registry,
            ),
            patch(
                "custom_components.econet300.HA_SUPPORTS_VIA_DEVICE_ID",
                supports_via_device_id,
            ),
        ):
            _cleanup_ghost_devices(MagicMock(), mock_config_entry, "test_uid")

        device_registry.async_remove_device.assert_called_once_with("ghost-device-id")
        if supports_via_device_id:
            device_registry.async_get_device_by_identifier.assert_any_call(
                ghost_identifier, mock_config_entry.entry_id
            )
            device_registry.async_get_device.assert_not_called()
        else:
            device_registry.async_get_device_by_identifier.assert_not_called()

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
        # Mock the issue registry delete function
        with patch(
            "custom_components.econet300.async_delete_issue"
        ) as mock_delete_issue:
            await async_remove_entry(hass, mock_config_entry)

            # Verify that delete_issue was called with correct parameters
            mock_delete_issue.assert_called_once_with(
                hass,
                DOMAIN,
                f"connection_failed_{mock_config_entry.entry_id}",
            )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("identifier", "expected"),
        [
            ("test_uid-ecoster-3", True),
            ("test_uid-ecoster-1", False),
            ("test_uid", False),
            ("other_uid-ecoster-3", False),
        ],
    )
    async def test_remove_device_only_for_empty_ecoster_slot(
        self, hass: HomeAssistant, mock_config_entry, identifier, expected
    ):
        """Test only an ecoSTER device on an empty slot can be deleted."""
        api = MagicMock(spec=Econet300Api)
        api.uid = "test_uid"
        coordinator = MagicMock(spec=EconetDataCoordinator)
        coordinator.data = {"regParams": {"ecoSterTemp1": 21.5, "ecoSterTemp3": None}}
        hass.data[DOMAIN] = {
            mock_config_entry.entry_id: {
                SERVICE_API: api,
                SERVICE_COORDINATOR: coordinator,
            }
        }
        device_entry = MagicMock(identifiers={(DOMAIN, identifier)})

        result = await async_remove_config_entry_device(
            hass, mock_config_entry, device_entry
        )

        assert result is expected

    @pytest.mark.asyncio
    async def test_remove_device_rejected_when_entry_not_loaded(
        self, hass: HomeAssistant, mock_config_entry
    ):
        """Test no device can be deleted while the entry has no runtime data."""
        hass.data[DOMAIN] = {}
        device_entry = MagicMock(identifiers={(DOMAIN, "test_uid-ecoster-3")})

        result = await async_remove_config_entry_device(
            hass, mock_config_entry, device_entry
        )

        assert result is False
