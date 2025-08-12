"""Basic tests for ecoNET300 sensors."""

from unittest.mock import Mock

from custom_components.econet300.binary_sensor import create_binary_entity_description
from custom_components.econet300.number import create_number_entity_description
from custom_components.econet300.sensor import (
    EconetSensorEntityDescription,
    can_add_mixer,
    create_sensor_entity_description,
)
from custom_components.econet300.switch import create_boiler_switch


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
        mock_coordinator.data = {"regParams": {"mixerTemp1": 25.5}}
        mock_coordinator.has_reg_data.return_value = True

        # Test with valid mixer data
        result = can_add_mixer("mixerTemp1", mock_coordinator)
        assert result is True

    def test_can_add_mixer_with_invalid_data(self):
        """Test can_add_mixer with invalid data."""
        # Create a mock coordinator with invalid data
        mock_coordinator = Mock()
        mock_coordinator.data = {"regParams": {"mixerTemp1": None}}
        mock_coordinator.has_reg_data.return_value = True

        # Test with None value
        result = can_add_mixer("mixerTemp1", mock_coordinator)
        assert result is False

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

    def test_entity_description_creation(self):
        """Test creating an entity description."""
        description = EconetSensorEntityDescription(
            key="testSensor", name="Test Sensor", process_val=lambda x: x * 2
        )

        assert description.key == "testSensor"
        assert description.name == "Test Sensor"
        assert description.process_val(5) == 10

    def test_entity_description_default_process_val(self):
        """Test default process_val function."""
        description = EconetSensorEntityDescription(key="testSensor")

        # Default process_val should return the value as-is
        assert description.process_val(42) == 42
        assert description.process_val("test") == "test"

    def test_icon_translation_enabled(self):
        """Test that icon translations are enabled via translation_key."""
        description = create_sensor_entity_description("tempCO")

        # Should have translation_key set for icon translations
        assert description.translation_key == "temp_co"
        # Should NOT have hardcoded icon (icon translations will handle this)
        assert not hasattr(description, "icon") or description.icon is None

    def test_all_sensor_types_have_translation_keys(self):
        """Test that all sensor entity creation functions use translation_key."""
        # Test main sensor creation
        main_desc = create_sensor_entity_description("tempCO")
        assert main_desc.translation_key == "temp_co"

        # Test lambda sensor creation
        from custom_components.econet300.sensor import (
            create_lambda_sensor_entity_description,
        )

        lambda_desc = create_lambda_sensor_entity_description("lambdaLevel")
        assert lambda_desc.translation_key == "lambda_level"

        # Test ecoSTER sensor creation
        from custom_components.econet300.sensor import (
            create_ecoster_sensor_entity_description,
        )

        ecoster_desc = create_ecoster_sensor_entity_description("ecoSterTemp1")
        assert ecoster_desc.translation_key == "eco_ster_temp1"

        # Test mixer sensor creation
        from custom_components.econet300.sensor import (
            create_mixer_sensor_entity_description,
        )

        mixer_desc = create_mixer_sensor_entity_description("mixerTemp1")
        assert mixer_desc.translation_key == "mixer_temp1"

        # Test binary sensor creation
        binary_desc = create_binary_entity_description("pumpCOWorks")
        assert binary_desc.translation_key == "pump_co_works"

        # Test switch creation
        switch_desc = create_boiler_switch(Mock(), Mock()).entity_description
        assert switch_desc.translation_key == "boiler_control"

        # Test number creation
        number_desc = create_number_entity_description("tempCOSet")
        assert number_desc.translation_key == "temp_co_set"
