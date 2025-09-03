"""Tests for the ecoNET300 integration diagnostics functionality."""

# pylint: disable=redefined-outer-name

from unittest.mock import MagicMock, patch

from homeassistant.config_entries import ConfigEntry, ConfigEntryState
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntry
from homeassistant.helpers.entity_registry import EntityRegistry, RegistryEntry
import pytest

from custom_components.econet300 import DOMAIN, SERVICE_API, SERVICE_COORDINATOR
from custom_components.econet300.api import Econet300Api
from custom_components.econet300.common import EconetDataCoordinator
from custom_components.econet300.diagnostics import (
    TO_REDACT,
    _redact_data,
    async_get_config_entry_diagnostics,
    async_get_device_diagnostics,
)


@pytest.fixture
def mock_config_entry():
    """Create a mock config entry for testing."""
    entry = MagicMock(spec=ConfigEntry)
    entry.entry_id = "test_entry_id"
    entry.data = {
        "host": "192.168.1.100",
        "username": "test_user",
        "password": "test_password",
    }
    entry.options = {"polling_interval": 30}
    entry.state = ConfigEntryState.LOADED
    entry.disabled_by = None
    entry.pref_disable_new_entities = False
    entry.pref_disable_polling = False
    return entry


@pytest.fixture
def mock_device_entry():
    """Create a mock device entry for testing."""
    device = MagicMock(spec=DeviceEntry)
    device.id = "test_device_id"
    device.name = "ecoNET300 Test Device"
    device.manufacturer = "PLUM"
    device.model = "ecoNET300"
    device.sw_version = "1.0.0"
    device.hw_version = "1.0"
    device.identifiers = {("econet300", "test_uid")}
    device.connections = set()
    device.suggested_area = "Boiler Room"
    device.disabled_by = None
    return device


@pytest.fixture
def mock_api():
    """Create a mock API for testing."""
    api = MagicMock(spec=Econet300Api)
    api.host = "192.168.1.100"
    api.uid = "test_uid"
    api.model_id = "ecoNET300"
    api.sw_rev = "1.0.0"
    api.hw_ver = "1.0"
    return api


@pytest.fixture
def mock_coordinator():
    """Create a mock coordinator for testing."""
    coordinator = MagicMock(spec=EconetDataCoordinator)
    coordinator.last_update_success = True
    coordinator.last_update_time = MagicMock()
    coordinator.last_update_time.isoformat.return_value = "2024-01-01T12:00:00"
    coordinator.data = {
        "sysParams": {"uid": "test_uid", "controllerID": "ecoNET300"},
        "regParams": {"tempCO": 65.5, "mode": 2},
        "paramsEdits": {"1280": {"min": 27, "max": 68}},
    }
    return coordinator


@pytest.fixture
def mock_entity_registry():
    """Create a mock entity registry for testing."""
    registry = MagicMock(spec=EntityRegistry)

    # Mock entities
    entity1 = MagicMock(spec=RegistryEntry)
    entity1.entity_id = "sensor.econet300_boiler_temperature"
    entity1.name = "Boiler Temperature"
    entity1.platform = "econet300"
    entity1.disabled_by = None

    entity2 = MagicMock(spec=RegistryEntry)
    entity2.entity_id = "binary_sensor.econet300_boiler_running"
    entity2.name = "Boiler Running"
    entity2.platform = "econet300"
    entity2.disabled_by = None

    # Mock registry behavior
    registry.entities = {
        "sensor.econet300_boiler_temperature": entity1,
        "binary_sensor.econet300_boiler_running": entity2,
    }

    def get_entity(entity_id):
        return registry.entities.get(entity_id)

    registry.async_get = MagicMock(side_effect=get_entity)

    return registry


class TestRedactData:
    """Test the _redact_data function."""

    def test_redact_sensitive_data(self):
        """Test that sensitive data is properly redacted."""
        data = {
            "host": "192.168.1.100",
            "username": "test_user",
            "password": "secret_password",
            "safe_data": "this_is_safe",
        }

        result = _redact_data(data, TO_REDACT)

        assert result["host"] == "**REDACTED**"
        assert result["username"] == "**REDACTED**"
        assert result["password"] == "**REDACTED**"
        assert result["safe_data"] == "this_is_safe"

    def test_redact_nested_data(self):
        """Test that nested sensitive data is properly redacted."""
        data = {
            "api_info": {
                "host": "192.168.1.100",
                "username": "test_user",
            },
            "safe_data": "this_is_safe",
        }

        result = _redact_data(data, TO_REDACT)

        assert result["api_info"]["host"] == "**REDACTED**"
        assert result["api_info"]["username"] == "**REDACTED**"
        assert result["safe_data"] == "this_is_safe"

    def test_non_dict_data(self):
        """Test that non-dict data is returned unchanged."""
        data = "not_a_dict"
        result = _redact_data(data, TO_REDACT)
        assert result == "not_a_dict"

    def test_empty_data(self):
        """Test that empty dict is handled correctly."""
        data = {}
        result = _redact_data(data, TO_REDACT)
        assert result == {}


class TestConfigEntryDiagnostics:
    """Test the async_get_config_entry_diagnostics function."""

    @pytest.mark.asyncio
    async def test_config_entry_diagnostics_with_integration_data(
        self,
        hass: HomeAssistant,
        mock_config_entry,
        mock_api,
        mock_coordinator,
    ):
        """Test config entry diagnostics when integration data is available."""
        # Setup integration data
        hass.data[DOMAIN] = {
            mock_config_entry.entry_id: {
                SERVICE_API: mock_api,
                SERVICE_COORDINATOR: mock_coordinator,
            }
        }

        result = await async_get_config_entry_diagnostics(hass, mock_config_entry)

        # Check that sensitive data is redacted
        assert result["entry_data"]["password"] == "**REDACTED**"
        assert result["entry_data"]["username"] == "**REDACTED**"
        assert result["entry_data"]["host"] == "**REDACTED**"

        # Check that safe data is included
        assert result["entry_options"] == {"polling_interval": 30}
        assert result["connection_status"]["entry_state"] == "loaded"
        assert result["connection_status"]["pref_disable_new_entities"] is False

        # Check API info is redacted
        assert result["api_info"]["host"] == "**REDACTED**"
        assert result["api_info"]["uid"] == "test_uid"
        assert result["api_info"]["model_id"] == "ecoNET300"

        # Check coordinator data
        assert result["coordinator_data"]["last_update_success"] is True
        assert result["coordinator_data"]["data"]["sysParams"]["uid"] == "test_uid"

    @pytest.mark.asyncio
    async def test_config_entry_diagnostics_without_integration_data(
        self,
        hass: HomeAssistant,
        mock_config_entry,
    ):
        """Test config entry diagnostics when no integration data is available."""
        # Ensure no integration data
        hass.data[DOMAIN] = {}

        result = await async_get_config_entry_diagnostics(hass, mock_config_entry)

        # Check that sensitive data is still redacted
        assert result["entry_data"]["password"] == "**REDACTED**"
        assert result["entry_data"]["username"] == "**REDACTED**"
        assert result["entry_data"]["host"] == "**REDACTED**"

        # Check that empty data structures are returned
        assert not result["api_info"]
        assert not result["coordinator_data"]

    @pytest.mark.asyncio
    async def test_config_entry_diagnostics_with_partial_data(
        self,
        hass: HomeAssistant,
        mock_config_entry,
        mock_api,
    ):
        """Test config entry diagnostics with partial integration data."""
        # Setup partial integration data (API but no coordinator)
        hass.data[DOMAIN] = {
            mock_config_entry.entry_id: {
                SERVICE_API: mock_api,
                SERVICE_COORDINATOR: None,
            }
        }

        result = await async_get_config_entry_diagnostics(hass, mock_config_entry)

        # Check API info is present and redacted
        assert result["api_info"]["uid"] == "test_uid"
        assert result["api_info"]["host"] == "**REDACTED**"

        # Check coordinator data is empty
        assert not result["coordinator_data"]


class TestDeviceDiagnostics:
    """Test the async_get_device_diagnostics function."""

    @pytest.mark.asyncio
    async def test_device_diagnostics_with_entities(
        self,
        hass: HomeAssistant,
        mock_config_entry,
        mock_device_entry,
        mock_coordinator,
        mock_entity_registry,
    ):
        """Test device diagnostics with associated entities."""
        # Setup integration data
        hass.data[DOMAIN] = {
            mock_config_entry.entry_id: {
                SERVICE_COORDINATOR: mock_coordinator,
            }
        }

        # Mock the entity registry
        with patch(
            "homeassistant.helpers.entity_registry.async_get",
            return_value=mock_entity_registry,
        ):
            result = await async_get_device_diagnostics(
                hass, mock_config_entry, mock_device_entry
            )

        # Check device info
        assert result["device_info"]["device_id"] == "test_device_id"
        assert result["device_info"]["name"] == "ecoNET300 Test Device"
        assert result["device_info"]["manufacturer"] == "PLUM"
        assert result["device_info"]["model"] == "ecoNET300"

        # Check entity info
        assert result["entity_info"]["entity_count"] == 2
        assert len(result["entity_info"]["entities"]) == 2

        # Check coordinator data
        assert result["coordinator_data"]["device_uid"] == "test_uid"
        assert result["coordinator_data"]["data_available"] is True

    @pytest.mark.asyncio
    async def test_device_diagnostics_without_coordinator(
        self,
        hass: HomeAssistant,
        mock_config_entry,
        mock_device_entry,
        mock_entity_registry,
    ):
        """Test device diagnostics without coordinator data."""
        # Setup integration data without coordinator
        hass.data[DOMAIN] = {
            mock_config_entry.entry_id: {
                SERVICE_COORDINATOR: None,
            }
        }

        # Mock the entity registry
        with patch(
            "homeassistant.helpers.entity_registry.async_get",
            return_value=mock_entity_registry,
        ):
            result = await async_get_device_diagnostics(
                hass, mock_config_entry, mock_device_entry
            )

        # Check device info is still present
        assert result["device_info"]["device_id"] == "test_device_id"

        # Check coordinator data is empty
        assert not result["coordinator_data"]

    @pytest.mark.asyncio
    async def test_device_diagnostics_without_entities(
        self,
        hass: HomeAssistant,
        mock_config_entry,
        mock_device_entry,
        mock_coordinator,
    ):
        """Test device diagnostics without associated entities."""
        # Setup integration data
        hass.data[DOMAIN] = {
            mock_config_entry.entry_id: {
                SERVICE_COORDINATOR: mock_coordinator,
            }
        }

        # Mock empty entity registry
        mock_empty_registry = MagicMock(spec=EntityRegistry)
        mock_empty_registry.entities = {}
        mock_empty_registry.async_get = MagicMock(return_value=None)

        with patch(
            "homeassistant.helpers.entity_registry.async_get",
            return_value=mock_empty_registry,
        ):
            result = await async_get_device_diagnostics(
                hass, mock_config_entry, mock_device_entry
            )

        # Check device info is present
        assert result["device_info"]["device_id"] == "test_device_id"

        # Check entity info shows no entities
        assert result["entity_info"]["entity_count"] == 0
        assert result["entity_info"]["entities"] == []

    @pytest.mark.asyncio
    async def test_device_diagnostics_with_disabled_entities(
        self,
        hass: HomeAssistant,
        mock_config_entry,
        mock_device_entry,
        mock_coordinator,
    ):
        """Test device diagnostics with disabled entities."""
        # Setup integration data
        hass.data[DOMAIN] = {
            mock_config_entry.entry_id: {
                SERVICE_COORDINATOR: mock_coordinator,
            }
        }

        # Mock entity registry with disabled entity
        mock_registry = MagicMock(spec=EntityRegistry)
        entity = MagicMock(spec=RegistryEntry)
        entity.entity_id = "sensor.econet300_disabled"
        entity.name = "Disabled Sensor"
        entity.platform = "econet300"
        entity.disabled_by = "user"

        mock_registry.entities = {"sensor.econet300_disabled": entity}

        def get_entity_by_id(entity_id):
            return mock_registry.entities.get(entity_id)

        mock_registry.async_get = MagicMock(side_effect=get_entity_by_id)

        with patch(
            "homeassistant.helpers.entity_registry.async_get",
            return_value=mock_registry,
        ):
            result = await async_get_device_diagnostics(
                hass, mock_config_entry, mock_device_entry
            )

        # Check that disabled entity is included
        assert result["entity_info"]["entity_count"] == 1
        assert result["entity_info"]["entities"][0]["disabled_by"] == "user"


class TestDiagnosticsIntegration:
    """Integration tests for diagnostics functionality."""

    @pytest.mark.asyncio
    async def test_diagnostics_with_real_data_structure(
        self,
        hass: HomeAssistant,
        mock_config_entry,
        mock_device_entry,  # pylint: disable=redefined-outer-name
    ):
        """Test diagnostics with realistic data structures."""
        # Create realistic API data
        api = MagicMock(spec=Econet300Api)
        api.host = "http://192.168.1.100"
        api.uid = "ecoNET300_001"
        api.model_id = "ecoMAX850R2-X"
        api.sw_rev = "2.1.5"
        api.hw_ver = "1.2"

        # Create realistic coordinator data
        coordinator = MagicMock(spec=EconetDataCoordinator)
        coordinator.last_update_success = True
        coordinator.last_update_time = MagicMock()
        coordinator.last_update_time.isoformat.return_value = "2024-01-15T14:30:00"
        coordinator.data = {
            "sysParams": {
                "uid": "ecoNET300_001",
                "controllerID": "ecoMAX850R2-X",
                "softVer": "2.1.5",
                "routerType": "1.2",
            },
            "regParams": {
                "tempCO": 68.5,
                "tempCOSet": 70,
                "mode": 2,
                "boilerPower": 85,
                "fanWorks": True,
                "pumpCOWorks": True,
            },
            "paramsEdits": {
                "1280": {"min": 27, "max": 68},  # tempCOSet limits
                "1281": {"min": 20, "max": 55},  # tempCWUSet limits
            },
        }

        # Setup integration data
        hass.data[DOMAIN] = {
            mock_config_entry.entry_id: {
                SERVICE_API: api,
                SERVICE_COORDINATOR: coordinator,
            }
        }

        # Test config entry diagnostics
        config_result = await async_get_config_entry_diagnostics(
            hass, mock_config_entry
        )

        # Verify sensitive data is redacted
        assert config_result["entry_data"]["password"] == "**REDACTED**"
        assert config_result["api_info"]["host"] == "**REDACTED**"

        # Verify operational data is present
        assert config_result["api_info"]["uid"] == "ecoNET300_001"
        assert config_result["api_info"]["model_id"] == "ecoMAX850R2-X"
        assert config_result["coordinator_data"]["data"]["regParams"]["tempCO"] == 68.5

        # Test device diagnostics
        device_result = await async_get_device_diagnostics(
            hass, mock_config_entry, mock_device_entry
        )

        # Verify device info
        assert device_result["device_info"]["name"] == "ecoNET300 Test Device"
        assert device_result["coordinator_data"]["device_uid"] == "ecoNET300_001"
