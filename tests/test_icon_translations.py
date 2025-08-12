"""Tests for ecoNET300 icon translation system."""

import json
from pathlib import Path
from unittest.mock import Mock

from custom_components.econet300.binary_sensor import create_binary_entity_description
from custom_components.econet300.number import create_number_entity_description
from custom_components.econet300.sensor import create_sensor_entity_description
from custom_components.econet300.switch import create_boiler_switch


class TestIconTranslationSystem:
    """Test the complete icon translation system."""

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
                assert "on" in sensor_icons["state"], (
                    f"{sensor_key} should have 'on' state icon"
                )
                assert "off" in sensor_icons["state"], (
                    f"{sensor_key} should have 'off' state icon"
                )

    def test_sensor_icon_translations(self):
        """Test sensor icon translations have appropriate icons."""
        with Path("custom_components/econet300/icons.json").open() as f:
            icons_data = json.load(f)

        sensors = icons_data["entity"]["sensor"]

        # Test that temperature sensors use thermometer icons
        temp_sensors = ["temp_co", "temp_water", "temp_room", "mixer_temp1"]
        for sensor_key in temp_sensors:
            if sensor_key in sensors:
                assert sensors[sensor_key]["default"] == "mdi:thermometer", (
                    f"{sensor_key} should use thermometer icon"
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
        assert boiler_icons["state"]["on"] == "mdi:fire", (
            "boiler_control on state should use fire icon"
        )
        assert boiler_icons["state"]["off"] == "mdi:fire-off", (
            "boiler_control off state should use fire-off icon"
        )

    def test_number_icon_translations(self):
        """Test number icon translations have appropriate icons."""
        with Path("custom_components/econet300/icons.json").open() as f:
            icons_data = json.load(f)

        numbers = icons_data["entity"]["number"]

        # Test that temperature setpoint numbers use thermometer icons
        temp_numbers = ["temp_co_set", "temp_water_set", "temp_room_set"]
        for number_key in temp_numbers:
            if number_key in numbers:
                assert numbers[number_key]["default"] == "mdi:thermometer", (
                    f"{number_key} should use thermometer icon"
                )

    def test_translation_key_consistency(self):
        """Test that all entity types use consistent translation_key format."""
        # Test sensor translation keys
        sensor_desc = create_sensor_entity_description("tempCO")
        assert sensor_desc.translation_key == "temp_co"

        # Test binary sensor translation keys
        binary_desc = create_binary_entity_description("pumpCOWorks")
        assert binary_desc.translation_key == "pump_co_works"

        # Test switch translation keys
        switch_desc = create_boiler_switch(Mock(), Mock()).entity_description
        assert switch_desc.translation_key == "boiler_control"

        # Test number translation keys
        number_desc = create_number_entity_description("tempCOSet")
        assert number_desc.translation_key == "temp_co_set"

    def test_no_hardcoded_icons(self):
        """Test that no entities have hardcoded icon properties."""
        # Test sensor - should not have icon property
        sensor_desc = create_sensor_entity_description("tempCO")
        assert not hasattr(sensor_desc, "icon") or sensor_desc.icon is None

        # Test binary sensor - should not have icon property
        binary_desc = create_binary_entity_description("pumpCOWorks")
        assert not hasattr(binary_desc, "icon") or binary_desc.icon is None

        # Test switch - should not have icon property
        switch_desc = create_boiler_switch(Mock(), Mock()).entity_description
        assert not hasattr(switch_desc, "icon") or switch_desc.icon is None

        # Test number - should not have icon property
        number_desc = create_number_entity_description("tempCOSet")
        assert not hasattr(number_desc, "icon") or number_desc.icon is None

    def test_icon_translation_keys_exist_in_icons_json(self):
        """Test that all translation keys exist in icons.json."""
        with Path("custom_components/econet300/icons.json").open() as f:
            icons_data = json.load(f)

        # Test key entities exist in icons.json
        test_cases = [
            ("sensor", "temp_co"),
            ("binary_sensor", "pump_co_works"),
            ("switch", "boiler_control"),
            ("number", "temp_co_set"),
        ]

        for entity_type, translation_key in test_cases:
            assert entity_type in icons_data["entity"], (
                f"Entity type {entity_type} should exist"
            )
            assert translation_key in icons_data["entity"][entity_type], (
                f"Translation key {translation_key} should exist in {entity_type}"
            )

    def test_icon_file_json_validity(self):
        """Test that icons.json is valid JSON and follows expected schema."""
        icons_file = Path("custom_components/econet300/icons.json")

        with icons_file.open() as f:
            icons_data = json.load(f)

        # Test required top-level keys
        assert "entity" in icons_data, "icons.json must have 'entity' key"

        # Test entity structure
        for entity_type, entities in icons_data["entity"].items():
            assert isinstance(entities, dict), (
                f"Entity type {entity_type} must be a dictionary"
            )

            for entity_key, icon_config in entities.items():
                assert isinstance(icon_config, dict), (
                    f"Entity {entity_key} must have icon configuration"
                )
                assert "default" in icon_config, (
                    f"Entity {entity_key} must have 'default' icon"
                )
                assert isinstance(icon_config["default"], str), (
                    f"Default icon for {entity_key} must be a string"
                )
                assert icon_config["default"].startswith("mdi:"), (
                    f"Default icon for {entity_key} must start with 'mdi:'"
                )

    def test_state_based_icon_structure(self):
        """Test that state-based icons have correct structure."""
        with Path("custom_components/econet300/icons.json").open() as f:
            icons_data = json.load(f)

        # Test binary sensors with state-based icons
        binary_sensors = icons_data["entity"]["binary_sensor"]
        state_based_sensors = ["pump_co_works", "fan_works", "status_cwu", "wifi"]

        for sensor_key in state_based_sensors:
            if sensor_key in binary_sensors:
                sensor_config = binary_sensors[sensor_key]
                if "state" in sensor_config:
                    state_config = sensor_config["state"]
                    assert "on" in state_config, (
                        f"{sensor_key} state config must have 'on' icon"
                    )
                    assert "off" in state_config, (
                        f"{sensor_key} state config must have 'off' icon"
                    )
                    assert state_config["on"].startswith("mdi:"), (
                        f"{sensor_key} 'on' icon must start with 'mdi:'"
                    )
                    assert state_config["off"].startswith("mdi:"), (
                        f"{sensor_key} 'off' icon must start with 'mdi:'"
                    )

    def test_icon_naming_conventions(self):
        """Test that icon names follow Material Design Icon conventions."""
        with Path("custom_components/econet300/icons.json").open() as f:
            icons_data = json.load(f)

        # Test all icons follow mdi: naming convention
        def check_icon_naming(data, path=""):
            for key, value in data.items():
                current_path = f"{path}.{key}" if path else key

                if isinstance(value, dict):
                    check_icon_naming(value, current_path)
                elif key == "default" or key in ["on", "off"]:
                    if isinstance(value, str):
                        assert value.startswith("mdi:"), (
                            f"Icon at {current_path} must start with 'mdi:'"
                        )
                        assert " " not in value, (
                            f"Icon at {current_path} must not contain spaces"
                        )
                        assert value.count(":") == 1, (
                            f"Icon at {current_path} must have exactly one colon"
                        )

        check_icon_naming(icons_data["entity"])
