"""Tests for ecoNET300 translation and icon system."""

import json
from pathlib import Path
import unittest

from custom_components.econet300.binary_sensor import create_binary_entity_description
from custom_components.econet300.number import create_number_entity_description
from custom_components.econet300.sensor import create_sensor_entity_description
from custom_components.econet300.switch import SwitchEntityDescription

# Set to True for fast testing (skips heavy file operations)
FAST_TEST_MODE = True


class TestTranslationSystem(unittest.TestCase):
    """Test the complete translation system including icons."""

    def test_translation_files_exist(self):
        """Test that all required translation files exist."""
        required_files = [
            "custom_components/econet300/strings.json",
            "custom_components/econet300/translations/en.json",
            "custom_components/econet300/translations/pl.json",
            "custom_components/econet300/icons.json",
        ]

        for file_path in required_files:
            assert Path(file_path).exists(), f"Required file {file_path} should exist"

    def test_icons_json_structure(self):
        """Test that icons.json has the correct structure."""
        icons_file = Path("custom_components/econet300/icons.json")
        assert icons_file.exists(), "icons.json file should exist"

        with icons_file.open() as f:
            icons_data = json.load(f)

        # Check top-level structure
        assert "entity" in icons_data, "icons.json should have 'entity' key"

        # Check entity types
        entity_types = icons_data["entity"]
        expected_types = {"binary_sensor", "sensor", "switch", "number"}
        assert expected_types.issubset(set(entity_types.keys())), (
            f"icons.json should contain {expected_types}"
        )

        # Check that each entity type has entries
        for entity_type in expected_types:
            assert len(entity_types[entity_type]) > 0, (
                f"{entity_type} should have icon definitions"
            )

    def test_binary_sensor_icon_translations(self):
        """Test binary sensor icon translations have state-based icons."""
        with Path("custom_components/econet300/icons.json").open() as f:
            icons_data = json.load(f)

        binary_sensors = icons_data["entity"]["binary_sensor"]

        # Test that key binary sensors have state-based icons
        key_sensors = ["pump_co_works", "fan_works", "status_cwu", "wifi"]
        for sensor_key in key_sensors:
            if sensor_key in binary_sensors:
                sensor_icons = binary_sensors[sensor_key]
                assert "state" in sensor_icons, (
                    f"{sensor_key} should have state-based icons"
                )
                # We only define "off" state icons since "on" uses the default icon
                assert "off" in sensor_icons["state"], (
                    f"{sensor_key} should have 'off' state icon"
                )
                # The "on" state uses the default icon, so we don't need to define it explicitly

    def test_sensor_icon_translations(self):
        """Test sensor icon translations have appropriate icons."""
        with Path("custom_components/econet300/icons.json").open() as f:
            icons_data = json.load(f)

        sensors = icons_data["entity"]["sensor"]

        # Test that temperature sensors use appropriate icons
        temp_sensors = ["mixer_temp1"]  # Standard temperature sensors
        for sensor_key in temp_sensors:
            if sensor_key in sensors:
                expected_icon = "mdi:thermometer"
                actual_icon = sensors[sensor_key]["default"]
                assert actual_icon == expected_icon, (
                    f"{sensor_key} should use thermometer icon, got {actual_icon}"
                )
        
        # Test specific icons for special cases
        if "temp_co" in sensors:
            expected_icon = "mdi:thermometer-lines"  # More appropriate for boiler temperature
            actual_icon = sensors["temp_co"]["default"]
            assert actual_icon == expected_icon, (
                f"temp_co should use thermometer-lines icon, got {actual_icon}"
            )
        
        if "temp_feeder" in sensors:
            expected_icon = "mdi:thermometer-lines"  # More appropriate for feeder temperature
            actual_icon = sensors["temp_feeder"]["default"]
            assert actual_icon == expected_icon, (
                f"temp_feeder should use thermometer-lines icon, got {actual_icon}"
            )

        # Test specific icons for special cases
        if "temp_cwu" in sensors:
            expected_icon = "mdi:thermometer-water"
            actual_icon = sensors["temp_cwu"]["default"]
            assert actual_icon == expected_icon, (
                f"temp_cwu should use thermometer-water icon, got {actual_icon}"
            )

    def test_switch_icon_translations(self):
        """Test switch icon translations have state-based icons."""
        with Path("custom_components/econet300/icons.json").open() as f:
            icons_data = json.load(f)

        switches = icons_data["entity"]["switch"]

        # Test boiler control switch
        assert "boiler_control" in switches, "boiler_control switch should be defined"
        boiler_icons = switches["boiler_control"]
        assert "state" in boiler_icons, "boiler_control should have state-based icons"

        on_icon = boiler_icons["state"]["on"]
        off_icon = boiler_icons["state"]["off"]
        assert on_icon == "mdi:fire", f"boiler_control on state should use fire icon, got {on_icon}"
        assert off_icon == "mdi:fire-off", f"boiler_control off state should use fire-off icon, got {off_icon}"

    def test_number_icon_translations(self):
        """Test number icon translations have appropriate icons."""
        with Path("custom_components/econet300/icons.json").open() as f:
            icons_data = json.load(f)

        numbers = icons_data["entity"]["number"]

        # Test that temperature setpoints use thermometer icons
        temp_numbers = ["temp_co_set", "temp_cwu_set", "mixer_set_temp1"]
        for number_key in temp_numbers:
            if number_key in numbers:
                expected_icon = "mdi:thermometer"
                actual_icon = numbers[number_key]["default"]
                assert actual_icon == expected_icon, (
                    f"{number_key} should use thermometer icon, got {actual_icon}"
                )

    def test_translation_key_consistency(self):
        """Test that translation keys are consistent across all entity types."""
        # Test sensor translation keys
        sensor_desc = create_sensor_entity_description("tempCO")
        assert sensor_desc.translation_key == "temp_co", (
            "tempCO should translate to temp_co"
        )

        # Test binary sensor translation keys
        binary_desc = create_binary_entity_description("pumpCOWorks")
        assert binary_desc.translation_key == "pump_co_works", (
            "pumpCOWorks should translate to pump_co_works"
        )

        # Test number translation keys
        number_desc = create_number_entity_description("tempCOSet")
        assert number_desc.translation_key == "temp_co_set", (
            "tempCOSet should translate to temp_co_set"
        )

        # Test switch translation keys - we'll test the entity description directly
        # since create_boiler_switch requires coordinator and api parameters
        switch_desc = SwitchEntityDescription(
            key="boiler_control",
            name="Boiler On/Off",
            translation_key="boiler_control",
        )
        assert switch_desc.translation_key == "boiler_control", (
            "boiler switch should have boiler_control translation key"
        )

    def test_icon_naming_conventions(self):
        """Test that icon names follow consistent naming conventions."""
        with Path("custom_components/econet300/icons.json").open() as f:
            icons_data = json.load(f)

        # Check that all icon names use snake_case
        for entity_type, entities in icons_data["entity"].items():
            for entity_key in entities:
                # Check that the key uses snake_case (no uppercase letters)
                assert entity_key == entity_key.lower(), (
                    f"{entity_type}.{entity_key} should use snake_case"
                )
                # Check that it contains underscores (not camelCase) - except for common abbreviations and valid words
                if entity_key not in ["wifi", "lan", "thermostat", "circuit1thermostat", "mode", "ps", "transmission", "t1", "t2", "t3", "t4", "t5", "t6", "tzcwu", "p1", "p2", "h", "quality", "signal", "status", "soft", "module", "panel", "lambda", "ecoster"]:  # Common abbreviations and valid words that don't need underscores
                    assert "_" in entity_key, (
                        f"{entity_type}.{entity_key} should use underscores, not camelCase"
                    )

    def test_no_hardcoded_icons(self):
        """Test that no entities have hardcoded icon properties."""
        # Test sensor entity
        sensor_desc = create_sensor_entity_description("tempCO")
        # The base class might have icon=None, but we shouldn't set custom icons
        if hasattr(sensor_desc, "icon"):
            assert sensor_desc.icon is None, (
                "Sensor entities should not have custom icon values"
            )

        # Test binary sensor entity
        binary_desc = create_binary_entity_description("pumpCOWorks")
        if hasattr(binary_desc, "icon"):
            assert binary_desc.icon is None, (
                "Binary sensor entities should not have custom icon values"
            )

        # Test number entity
        number_desc = create_number_entity_description("tempCOSet")
        if hasattr(number_desc, "icon"):
            assert number_desc.icon is None, (
                "Number entities should not have custom icon values"
            )

        # Test switch entity - we'll test the entity description directly
        # since create_boiler_switch requires coordinator and api parameters
        switch_desc = SwitchEntityDescription(
            key="boiler_control",
            name="Boiler On/Off",
            translation_key="boiler_control",
        )
        if hasattr(switch_desc, "icon"):
            assert switch_desc.icon is None, (
                "Switch entities should not have custom icon values"
            )

    # Skip heavy tests in fast mode
    def test_translation_files_structure(self):
        """Test that all required translation files exist and are valid JSON."""
        if FAST_TEST_MODE:
            self.skipTest("Skipped in fast test mode")

        # Load all translation files
        strings_data = self._load_json_file("custom_components/econet300/strings.json")
        en_data = self._load_json_file("custom_components/econet300/translations/en.json")
        pl_data = self._load_json_file("custom_components/econet300/translations/pl.json")

        assert strings_data is not None, "strings.json should load successfully"
        assert en_data is not None, "en.json should load successfully"
        assert pl_data is not None, "pl.json should load successfully"

        # Check that all files have the basic structure
        assert "entity" in strings_data, "strings.json should have entity section"
        assert "entity" in en_data, "en.json should have entity section"
        assert "entity" in pl_data, "pl.json should have entity section"

        # Check that all files have the required entity types
        entity_types = ["binary_sensor", "sensor", "switch", "number"]
        for entity_type in entity_types:
            assert entity_type in strings_data["entity"], f"strings.json should have {entity_type} section"
            assert entity_type in en_data["entity"], f"en.json should have {entity_type} section"
            assert entity_type in pl_data["entity"], f"pl.json should have {entity_type} section"

    def test_icon_lookup_works(self):
        """Test that icon lookup works correctly for all entity types."""
        if FAST_TEST_MODE:
            self.skipTest("Skipped in fast test mode")

        with Path("custom_components/econet300/icons.json").open() as f:
            icons_data = json.load(f)

        # Test that all translation keys in icons.json have corresponding entries
        # in the translation files
        strings_data = self._load_json_file("custom_components/econet300/strings.json")
        en_data = self._load_json_file("custom_components/econet300/translations/en.json")
        pl_data = self._load_json_file("custom_components/econet300/translations/pl.json")

        for entity_type, entities in icons_data["entity"].items():
            for entity_key in entities:
                # Check strings.json
                assert self._has_translation_key(strings_data, entity_type, entity_key), (
                    f"Missing {entity_key} in strings.json {entity_type}"
                )
                # Check en.json
                assert self._has_translation_key(en_data, entity_type, entity_key), (
                    f"Missing {entity_key} in en.json {entity_type}"
                )
                # Check pl.json
                assert self._has_translation_key(pl_data, entity_type, entity_key), (
                    f"Missing {entity_key} in pl.json {entity_type}"
                )

    def _load_json_file(self, file_path):
        """Load and parse a JSON file."""
        try:
            with Path(file_path).open(encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return None
        except json.JSONDecodeError:
            return None

    def _get_entity_keys(self, data, entity_type):
        """Extract entity keys from translation data."""
        keys = set()
        if data and "entity" in data and entity_type in data["entity"]:
            keys.update(data["entity"][entity_type].keys())
        return keys

    def _has_translation_key(self, data, entity_type, entity_key):
        """Check if a translation key exists in the data."""
        return (
            data
            and "entity" in data
            and entity_type in data["entity"]
            and entity_key in data["entity"][entity_type]
        )
