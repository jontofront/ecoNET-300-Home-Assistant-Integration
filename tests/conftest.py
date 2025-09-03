"""Test configuration for ecoNET300 integration tests."""

from pathlib import Path
import sys
from unittest.mock import AsyncMock, MagicMock

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
import pytest
import pytest_asyncio

# Add the project root to the Python path so tests can import custom_components
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest_asyncio.fixture
async def hass():
    """Create a Home Assistant instance for testing."""
    hass_instance = HomeAssistant("test")

    # Mock the config_entries to avoid initialization issues
    mock_config_entries = MagicMock()
    mock_config_entries.async_forward_entry_setups = AsyncMock(return_value=True)
    mock_config_entries.async_unload_platforms = AsyncMock(return_value=True)
    hass_instance.config_entries = mock_config_entries

    await hass_instance.async_start()
    yield hass_instance
    await hass_instance.async_stop()


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
    return entry
