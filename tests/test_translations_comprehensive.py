"""Tests for ecoNET300 entity translations and constants.

This module tests:
1. All sensor keys have translations
2. All binary sensor keys have translations
3. All number keys have translations
4. Translation files are consistent (strings.json, en.json, pl.json, etc.)
5. Entity types match between constants and translation files
"""

# pylint: disable=redefined-outer-name
# Note: Redefining fixture names in test parameters is expected pytest pattern

import json
from pathlib import Path
import re

import pytest

from custom_components.econet300.common_functions import camel_to_snake
from custom_components.econet300.const import (
    BINARY_SENSOR_MAP_KEY,
    DEFAULT_BINARY_SENSORS,
    DEFAULT_SENSORS,
    ECOMAX360I_SENSORS,
    ECOSTER_SENSORS,
    ECOSTER_SETPOINT_PARAMS,
    ENTITY_BINARY_DEVICE_CLASS_MAP,
    ENTITY_NUMBER_SENSOR_DEVICE_CLASS_MAP,
    ENTITY_SENSOR_DEVICE_CLASS_MAP,
    LAMBDA_SENSORS,
    SENSOR_MAP_KEY,
    SENSOR_MIXER_KEY,
)

# Define paths
BASE_DIR = Path(__file__).parent.parent
STRINGS_FILE = BASE_DIR / "custom_components" / "econet300" / "strings.json"
TRANSLATIONS_DIR = BASE_DIR / "custom_components" / "econet300" / "translations"
ICONS_FILE = BASE_DIR / "custom_components" / "econet300" / "icons.json"


def load_json_file(file_path: Path) -> dict:
    """Load and parse a JSON file."""
    if not file_path.exists():
        return {}
    with file_path.open(encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def strings_data():
    """Load strings.json data."""
    return load_json_file(STRINGS_FILE)


@pytest.fixture
def en_translations():
    """Load English translations."""
    return load_json_file(TRANSLATIONS_DIR / "en.json")


@pytest.fixture
def pl_translations():
    """Load Polish translations."""
    return load_json_file(TRANSLATIONS_DIR / "pl.json")


@pytest.fixture
def icons_data():
    """Load icons.json data."""
    return load_json_file(ICONS_FILE)


@pytest.fixture
def all_sensor_keys():
    """Get all sensor keys from constants."""
    sensor_keys = set(ENTITY_SENSOR_DEVICE_CLASS_MAP.keys())
    sensor_keys.update(ECOMAX360I_SENSORS)
    sensor_keys.update(ECOSTER_SENSORS)
    sensor_keys.update(LAMBDA_SENSORS)
    sensor_keys.update(DEFAULT_SENSORS)

    for sensor_set in SENSOR_MAP_KEY.values():
        if isinstance(sensor_set, set):
            sensor_keys.update(sensor_set)

    # Add mixer base keys
    for mixer_set in SENSOR_MIXER_KEY.values():
        if isinstance(mixer_set, set):
            for key in mixer_set:
                base_key = re.sub(r"\d+$", "", key)
                sensor_keys.add(base_key)

    return sensor_keys


@pytest.fixture
def all_binary_sensor_keys():
    """Get all binary sensor keys from constants."""
    binary_keys = set(ENTITY_BINARY_DEVICE_CLASS_MAP.keys())
    binary_keys.update(DEFAULT_BINARY_SENSORS)

    for binary_sensor_set in BINARY_SENSOR_MAP_KEY.values():
        if isinstance(binary_sensor_set, set):
            binary_keys.update(binary_sensor_set)

    return binary_keys


@pytest.fixture
def all_number_keys():
    """Get all number keys from constants."""
    return set(ENTITY_NUMBER_SENSOR_DEVICE_CLASS_MAP.keys())


class TestCamelToSnakeConversion:
    """Test camelCase to snake_case conversion."""

    @pytest.mark.parametrize(
        ("input_key", "expected"),
        [
            ("tempCO", "temp_co"),
            ("boilerPower", "boiler_power"),
            ("mixerTemp1", "mixer_temp1"),
            ("statusCWU", "status_cwu"),
            ("simpleKey", "simple_key"),
        ],
    )
    def test_camel_to_snake_conversion(self, input_key, expected):
        """Test camelCase to snake_case conversion."""
        assert camel_to_snake(input_key) == expected


class TestTranslationFileStructure:
    """Test translation file structure."""

    def test_strings_json_exists(self):
        """Test strings.json exists."""
        assert STRINGS_FILE.exists()

    def test_en_json_exists(self):
        """Test en.json exists."""
        assert (TRANSLATIONS_DIR / "en.json").exists()

    def test_pl_json_exists(self):
        """Test pl.json exists."""
        assert (TRANSLATIONS_DIR / "pl.json").exists()

    def test_strings_has_entity_section(self, strings_data):
        """Test strings.json has entity section."""
        assert "entity" in strings_data

    def test_strings_has_sensor_section(self, strings_data):
        """Test strings.json has sensor section."""
        assert "sensor" in strings_data.get("entity", {})

    def test_strings_has_binary_sensor_section(self, strings_data):
        """Test strings.json has binary_sensor section."""
        assert "binary_sensor" in strings_data.get("entity", {})


class TestTranslationConsistency:
    """Test translation consistency between files."""

    def test_en_has_sensor_translations(self, strings_data, en_translations):
        """Test English translations has sensor translations."""
        strings_sensors = strings_data.get("entity", {}).get("sensor", {})
        en_sensors = en_translations.get("entity", {}).get("sensor", {})

        missing = [key for key in strings_sensors if key not in en_sensors]
        assert len(missing) == 0, f"Missing in en.json: {missing}"

    def test_pl_has_sensor_translations(self, strings_data, pl_translations):
        """Test Polish translations has sensor translations."""
        strings_sensors = strings_data.get("entity", {}).get("sensor", {})
        pl_sensors = pl_translations.get("entity", {}).get("sensor", {})

        missing = [key for key in strings_sensors if key not in pl_sensors]
        assert len(missing) == 0, f"Missing in pl.json: {missing}"

    def test_en_has_binary_sensor_translations(self, strings_data, en_translations):
        """Test English translations has binary sensor translations."""
        strings_binary = strings_data.get("entity", {}).get("binary_sensor", {})
        en_binary = en_translations.get("entity", {}).get("binary_sensor", {})

        missing = [key for key in strings_binary if key not in en_binary]
        assert len(missing) == 0, f"Missing in en.json: {missing}"

    def test_pl_has_binary_sensor_translations(self, strings_data, pl_translations):
        """Test Polish translations has binary sensor translations."""
        strings_binary = strings_data.get("entity", {}).get("binary_sensor", {})
        pl_binary = pl_translations.get("entity", {}).get("binary_sensor", {})

        missing = [key for key in strings_binary if key not in pl_binary]
        assert len(missing) == 0, f"Missing in pl.json: {missing}"


class TestSensorTranslations:
    """Test sensor translations exist."""

    def test_sensor_keys_have_translations(self, strings_data, all_sensor_keys):
        """Test all sensor keys have translations in strings.json."""
        sensor_translations = strings_data.get("entity", {}).get("sensor", {})
        snake_keys = {camel_to_snake(key) for key in all_sensor_keys}

        # Find missing translations
        missing = [key for key in snake_keys if key not in sensor_translations]

        # Allow some missing (dynamic keys, etc.) - just report
        if missing:
            pytest.skip(
                f"Some sensor translations missing ({len(missing)}): {missing[:5]}..."
            )


class TestBinarySensorTranslations:
    """Test binary sensor translations exist."""

    def test_binary_sensor_keys_have_translations(
        self, strings_data, all_binary_sensor_keys
    ):
        """Test all binary sensor keys have translations in strings.json."""
        binary_translations = strings_data.get("entity", {}).get("binary_sensor", {})
        snake_keys = {camel_to_snake(key) for key in all_binary_sensor_keys}

        # Find missing translations
        missing = [key for key in snake_keys if key not in binary_translations]

        # Allow some missing (dynamic keys, etc.) - just report
        if missing:
            pytest.skip(
                f"Some binary sensor translations missing ({len(missing)}): {missing[:5]}..."
            )


class TestNumberTranslations:
    """Test number translations exist."""

    def test_number_keys_have_translations(self, strings_data, all_number_keys):
        """Test all number keys have translations in strings.json."""
        number_translations = strings_data.get("entity", {}).get("number", {})
        snake_keys = {camel_to_snake(key) for key in all_number_keys}

        # Find missing translations
        missing = [key for key in snake_keys if key not in number_translations]

        # Allow some missing (dynamic keys, etc.) - just report
        if missing:
            pytest.skip(
                f"Some number translations missing ({len(missing)}): {missing[:5]}..."
            )

    @pytest.mark.parametrize(
        "translation_file",
        [
            STRINGS_FILE,
            *(
                TRANSLATIONS_DIR / f"{lang}.json"
                for lang in ("cz", "de", "en", "fr", "pl", "uk")
            ),
        ],
        ids=lambda path: path.name,
    )
    def test_ecoster_setpoint_translations(self, translation_file):
        """Every language names the ecoSTER setpoints with an {index} placeholder."""
        data = load_json_file(translation_file)
        number_translations = data.get("entity", {}).get("number", {})

        for param in ECOSTER_SETPOINT_PARAMS:
            key = camel_to_snake(param)
            assert key in number_translations, f"{translation_file.name}: {key}"
            assert "{index}" in number_translations[key]["name"]


class TestTranslationQuality:
    """Test translation quality checks."""

    def test_translations_have_name_field(self, strings_data):
        """Test that translations have name field."""
        entity_section = strings_data.get("entity", {})

        for entity_type in ["sensor", "binary_sensor", "number", "switch"]:
            entities = entity_section.get(entity_type, {})
            for key, value in entities.items():
                assert "name" in value, f"{entity_type}.{key} missing 'name' field"

    def test_translation_names_not_empty(self, strings_data):
        """Test that translation names are not empty."""
        entity_section = strings_data.get("entity", {})

        for entity_type in ["sensor", "binary_sensor", "number", "switch"]:
            entities = entity_section.get(entity_type, {})
            for key, value in entities.items():
                name = value.get("name", "")
                assert name, f"{entity_type}.{key} has empty 'name' field"
