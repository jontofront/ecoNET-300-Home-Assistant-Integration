"""Test icon system with real fixture data from ecoMAX810P-L."""

import json
from pathlib import Path
from unittest.mock import Mock

import pytest

from custom_components.econet300.api import Econet300Api
from custom_components.econet300.binary_sensor import create_binary_sensors
from custom_components.econet300.common import EconetDataCoordinator
from custom_components.econet300.common_functions import camel_to_snake
from custom_components.econet300.sensor import create_controller_sensors


class TestFixtureBasedIcons:
    """Test icon system with real fixture data."""

    @pytest.fixture
    def fixture_data(self):
        """Load real fixture data from ecoMAX810P-L."""
        fixture_path = (
            Path(__file__).parent / "fixtures" / "ecoMAX810P-L" / "regParams.json"
        )
        with fixture_path.open(encoding="utf-8") as f:
            return json.load(f)

    @pytest.fixture
    def mock_api(self):
        """Create mock API with fixture data."""
        api = Mock(spec=Econet300Api)
        api.get_sys_params.return_value = {
            "controllerID": "ecoMAX810P-L",
            "softVer": "1.2.3",
            "routerType": "WiFi",
        }
        return api

    @pytest.fixture
    def mock_coordinator(self, fixture_data, mock_api):
        """Create mock coordinator with fixture data."""
        coordinator = Mock(spec=EconetDataCoordinator)
        # Structure data as expected by the sensor creation functions
        coordinator.data = {
            "regParams": fixture_data["curr"],
            "sysParams": {
                "controllerID": "ecoMAX810P-L",
                "softVer": "1.2.3",
                "routerType": "WiFi",
            },
        }
        coordinator.api = mock_api
        return coordinator

    def test_fixture_data_structure(self, fixture_data):
        """Test that fixture data has expected structure."""
        assert "curr" in fixture_data
        assert "thermostat" in fixture_data["curr"]
        assert "pumpCOWorks" in fixture_data["curr"]
        assert "tempCO" in fixture_data["curr"]
        assert "mixerTemp1" in fixture_data["curr"]

        # Fixture data loaded successfully
        assert len(fixture_data["curr"]) > 0

    def test_icon_translation_keys_from_fixture(self, fixture_data):
        """Test that all fixture data keys have proper translation keys."""
        missing_icons = []
        found_icons = []

        # Load icons.json to check against
        icons_path = (
            Path(__file__).parent.parent
            / "custom_components"
            / "econet300"
            / "icons.json"
        )
        with icons_path.open(encoding="utf-8") as f:
            icons_data = json.load(f)

        # Check each fixture key
        for api_key in fixture_data["curr"]:
            translation_key = camel_to_snake(api_key)

            # Check if icon exists in any entity type
            icon_found = False
            for entity_type in ["binary_sensor", "sensor", "switch", "number"]:
                if entity_type in icons_data["entity"]:
                    if translation_key in icons_data["entity"][entity_type]:
                        icon_found = True
                        found_icons.append(f"✅ {api_key} → {translation_key}")
                        break

            if not icon_found:
                missing_icons.append(f"❌ {api_key} → {translation_key}")

        # Assert that we have good icon coverage (at least 80%)
        coverage_percentage = (len(found_icons) / len(fixture_data["curr"])) * 100

        assert coverage_percentage >= 80, (
            f"Icon coverage too low: {coverage_percentage:.1f}%"
        )

    def test_sensor_creation_with_fixture_data(self, mock_coordinator, mock_api):
        """Test that sensors can be created from fixture data."""
        # Create sensors using the fixture data
        sensors = create_controller_sensors(mock_coordinator, mock_api)

        assert len(sensors) > 0, "No sensors created from fixture data"

        # Sensors created successfully

        # Check that key sensors have proper translation keys
        for sensor in sensors:
            assert hasattr(sensor, "translation_key"), (
                f"Sensor {sensor.name} missing translation_key"
            )
            assert sensor.translation_key, (
                f"Sensor {sensor.name} has empty translation_key"
            )

            # Check that translation key follows naming convention
            assert "_" in sensor.translation_key, (
                f"Translation key should use snake_case: {sensor.translation_key}"
            )

            # Sensor has proper translation key

    def test_binary_sensor_creation_with_fixture_data(self, mock_coordinator, mock_api):
        """Test that binary sensors can be created from fixture data."""
        # Create binary sensors using the fixture data
        binary_sensors = create_binary_sensors(mock_coordinator, mock_api)

        assert len(binary_sensors) > 0, "No binary sensors created from fixture data"

        # Binary sensors created successfully

        # Check that key binary sensors have proper translation keys
        for sensor in binary_sensors:
            assert hasattr(sensor, "translation_key"), (
                f"Binary sensor {sensor.name} missing translation_key"
            )
            assert sensor.translation_key, (
                f"Binary sensor {sensor.name} has empty translation_key"
            )

            # Check that translation key follows naming convention
            assert "_" in sensor.translation_key, (
                f"Translation key should use snake_case: {sensor.translation_key}"
            )

            # Binary sensor has proper translation key

    def test_specific_fixture_entities_have_icons(self, fixture_data):
        """Test that specific important entities from fixture have icons."""
        important_entities = [
            "tempCO",  # Boiler temperature
            "tempCWU",  # Hot water temperature
            "pumpCOWorks",  # Boiler pump
            "fanWorks",  # Fan
            "thermostat",  # Thermostat
            "statusCWU",  # Hot water status
            "statusCO",  # Heating status
            "mixerTemp1",  # Mixer temperature
            "mixerPumpWorks1",  # Mixer pump
        ]

        # Load icons.json
        icons_path = (
            Path(__file__).parent.parent
            / "custom_components"
            / "econet300"
            / "icons.json"
        )
        with icons_path.open(encoding="utf-8") as f:
            icons_data = json.load(f)

        missing_important_icons = []

        for entity_key in important_entities:
            if entity_key in fixture_data["curr"]:
                translation_key = camel_to_snake(entity_key)

                # Check if icon exists
                icon_found = False
                for entity_type in ["binary_sensor", "sensor", "switch", "number"]:
                    if entity_type in icons_data["entity"]:
                        if translation_key in icons_data["entity"][entity_type]:
                            icon_found = True
                            # Icon found for entity
                            break

                if not icon_found:
                    missing_important_icons.append(f"❌ {entity_key} → {translation_key}")

        # Check if any important icons are missing

        # All important entities should have icons
        assert len(missing_important_icons) == 0, (
            f"Missing icons for important entities: {missing_important_icons}"
        )

    def test_fixture_data_values_are_valid(self, fixture_data):
        """Test that fixture data contains valid values for testing."""
        curr_data = fixture_data["curr"]

        # Check that we have a mix of different data types
        boolean_values = [
            v for v in curr_data.values() if isinstance(v, bool)
        ]
        numeric_values = [
            v for v in curr_data.values()
            if isinstance(v, (int, float)) and v is not None
        ]

        # Fixture data analysis completed

        # Should have reasonable amount of each type
        assert len(boolean_values) >= 10, "Not enough boolean values for testing"
        assert len(numeric_values) >= 15, "Not enough numeric values for testing"

        # Check specific important values
        if "tempCO" in curr_data:
            temp_co = curr_data["tempCO"]
            assert isinstance(temp_co, (int, float)), (
                f"tempCO should be numeric, got {type(temp_co)}"
            )
            assert temp_co > 0, f"tempCO should be positive, got {temp_co}"

        if "thermostat" in curr_data:
            thermostat = curr_data["thermostat"]
            assert isinstance(thermostat, (int, bool)), (
                f"thermostat should be int/bool, got {type(thermostat)}"
            )

    def test_icon_json_structure_matches_fixture_needs(self, fixture_data):
        """Test that icons.json structure can handle all fixture entity types."""
        icons_path = (
            Path(__file__).parent.parent
            / "custom_components"
            / "econet300"
            / "icons.json"
        )
        with icons_path.open(encoding="utf-8") as f:
            icons_data = json.load(f)

        # Get all entity types from icons.json
        available_entity_types = set(icons_data["entity"].keys())

        # Check that we have all necessary entity types
        required_entity_types = {"binary_sensor", "sensor", "switch", "number"}
        missing_entity_types = required_entity_types - available_entity_types

        assert len(missing_entity_types) == 0, (
            f"Missing entity types in icons.json: {missing_entity_types}"
        )

        # All required entity types present

        # Check that each entity type has reasonable number of icons
        for entity_type in required_entity_types:
            icon_count = len(icons_data["entity"][entity_type])
            assert icon_count > 0, f"No icons defined for {entity_type}"
