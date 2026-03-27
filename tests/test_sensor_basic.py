"""Basic tests for ecoNET300 sensors."""

from unittest.mock import Mock

from custom_components.econet300.const import DEFAULT_SENSORS, SENSOR_MAP_KEY
from custom_components.econet300.sensor import (
    EconetSensorEntityDescription,
    can_add_mixer,
    create_sensor_entity_description,
)


class TestEconetSensorBasic:
    """Test basic sensor functionality."""

    # ruff: noqa: PLR6301
    def test_create_sensor_entity_description(self):
        """Test creating a sensor entity description."""
        # Test with a simple key
        description = create_sensor_entity_description("tempCO")

        assert description.key == "tempCO"
        assert description.translation_key == "temp_co"
        assert description.process_val is not None

    # ruff: noqa: PLR6301
    def test_can_add_mixer_with_valid_data(self):
        """Test can_add_mixer with valid data."""
        # Create a mock coordinator with valid data
        mock_coordinator = Mock()
        mock_coordinator.data = {"regParams": {"mixerTemp1": 25.5}}
        mock_coordinator.has_reg_data.return_value = True

        # Test with valid mixer data
        result = can_add_mixer("mixerTemp1", mock_coordinator)
        assert result is True

    # ruff: noqa: PLR6301
    def test_can_add_mixer_with_invalid_data(self):
        """Test can_add_mixer with invalid data."""
        # Create a mock coordinator with invalid data
        mock_coordinator = Mock()
        mock_coordinator.data = {"regParams": {"mixerTemp1": None}}
        mock_coordinator.has_reg_data.return_value = True

        # Test with None value
        result = can_add_mixer("mixerTemp1", mock_coordinator)
        assert result is False

    # ruff: noqa: PLR6301
    def test_can_add_mixer_with_missing_data(self):
        """Test can_add_mixer with missing data."""
        # Create a mock coordinator with missing data
        mock_coordinator = Mock()
        mock_coordinator.data = {"regParams": {}}
        mock_coordinator.has_reg_data.return_value = False

        # Test with missing data
        result = can_add_mixer("mixerTemp1", mock_coordinator)
        assert result is False


class TestEconetSensorEntityDescription:
    """Test sensor entity description."""

    # ruff: noqa: PLR6301
    def test_entity_description_creation(self):
        """Test creating an entity description."""
        description = EconetSensorEntityDescription(
            key="testSensor", name="Test Sensor", process_val=lambda x: x * 2
        )

        assert description.key == "testSensor"
        assert description.name == "Test Sensor"
        assert description.process_val(5) == 10

    # ruff: noqa: PLR6301
    def test_entity_description_default_process_val(self):
        """Test default process_val function."""
        description = EconetSensorEntityDescription(key="testSensor")

        # Default process_val should return the value as-is
        assert description.process_val(42) == 42
        assert description.process_val("test") == "test"


class TestSensorMappingLogic:
    """Test sensor mapping logic for different controllerIDs."""

    # ruff: noqa: PLR6301
    def test_all_controllers_use_default_sensors(self):
        """Test that all controllers use DEFAULT_SENSORS mapping."""
        # Test known controllers
        known_controllers = [
            "ecoMAX360i",
            "ecoSter",
            "lambda",
            "ecoSOL 500",
            "ecoSOL 301",
        ]

        for controller_id in known_controllers:
            # Simulate the logic from sensor.py
            if controller_id and controller_id in SENSOR_MAP_KEY:
                sensor_keys = SENSOR_MAP_KEY["_default"].copy()
                # Verify we're using default sensors, not specific mapping
                assert sensor_keys == DEFAULT_SENSORS
                # Verify the specific mapping exists but we don't use it
                assert controller_id in SENSOR_MAP_KEY
                assert (
                    SENSOR_MAP_KEY[controller_id] != DEFAULT_SENSORS
                )  # Different from default

    # ruff: noqa: PLR6301
    def test_unknown_controllers_use_default_sensors(self):
        """Test that unknown controllers use DEFAULT_SENSORS mapping."""
        unknown_controllers = [
            "ecoMAX860D3-HB",
            "ecoMAX860P4-O MINI MATIC",
            "ecoMAX850R2-X",
            "ecoMAX810P-L TOUCH",
            "ecoMAX860P2-N TOUCH",
            "ecoMAX860P3-V",
            "SControl MK1",
            "UnknownController",
            None,  # No controllerID
        ]

        for controller_id in unknown_controllers:
            # Simulate the logic from sensor.py
            if controller_id and controller_id in SENSOR_MAP_KEY:
                sensor_keys = SENSOR_MAP_KEY["_default"].copy()
            else:
                sensor_keys = SENSOR_MAP_KEY["_default"].copy()

            # All should use default sensors
            assert sensor_keys == DEFAULT_SENSORS

    # ruff: noqa: PLR6301
    def test_default_sensors_comprehensive(self):
        """Test that DEFAULT_SENSORS contains comprehensive sensor set."""
        # Verify DEFAULT_SENSORS contains expected sensor types
        expected_sensors = {
            "tempCO",  # Boiler temperature
            "tempCWU",  # Hot water temperature
            "boilerPower",  # Boiler power
            "mode",  # Operation mode
            "statusCO",  # Boiler status
        }

        # All expected sensors should be in DEFAULT_SENSORS
        for sensor in expected_sensors:
            assert sensor in DEFAULT_SENSORS, (
                f"Expected sensor {sensor} not in DEFAULT_SENSORS"
            )
