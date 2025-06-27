"""Basic tests for ecoNET300 sensors."""

import pytest
from unittest.mock import Mock

from custom_components.econet300.sensor import (
    EconetSensor,
    EconetSensorEntityDescription,
    create_sensor_entity_description,
    can_add_mixer,
)


class TestEconetSensorBasic:
    """Test basic sensor functionality."""

    def test_create_sensor_entity_description(self):
        """Test creating a sensor entity description."""
        # Test with a simple key
        description = create_sensor_entity_description("tempCO")
        
        assert description.key == "tempCO"
        assert description.translation_key == "temp_co"
        assert description.process_val is not None

    def test_can_add_mixer_with_valid_data(self):
        """Test can_add_mixer with valid data."""
        # Create a mock coordinator with valid data
        mock_coordinator = Mock()
        mock_coordinator.data = {
            "regParams": {
                "mixerTemp1": 25.5
            }
        }
        mock_coordinator.has_reg_data.return_value = True
        
        # Test with valid mixer data
        result = can_add_mixer("mixerTemp1", mock_coordinator)
        assert result is True

    def test_can_add_mixer_with_invalid_data(self):
        """Test can_add_mixer with invalid data."""
        # Create a mock coordinator with invalid data
        mock_coordinator = Mock()
        mock_coordinator.data = {
            "regParams": {
                "mixerTemp1": None
            }
        }
        mock_coordinator.has_reg_data.return_value = True
        
        # Test with None value
        result = can_add_mixer("mixerTemp1", mock_coordinator)
        assert result is False

    def test_can_add_mixer_with_missing_data(self):
        """Test can_add_mixer with missing data."""
        # Create a mock coordinator with missing data
        mock_coordinator = Mock()
        mock_coordinator.data = {
            "regParams": {}
        }
        mock_coordinator.has_reg_data.return_value = False
        
        # Test with missing data
        result = can_add_mixer("mixerTemp1", mock_coordinator)
        assert result is False


class TestEconetSensorEntityDescription:
    """Test sensor entity description."""

    def test_entity_description_creation(self):
        """Test creating an entity description."""
        description = EconetSensorEntityDescription(
            key="testSensor",
            name="Test Sensor",
            process_val=lambda x: x * 2
        )
        
        assert description.key == "testSensor"
        assert description.name == "Test Sensor"
        assert description.process_val(5) == 10

    def test_entity_description_default_process_val(self):
        """Test default process_val function."""
        description = EconetSensorEntityDescription(
            key="testSensor"
        )
        
        # Default process_val should return the value as-is
        assert description.process_val(42) == 42
        assert description.process_val("test") == "test" 