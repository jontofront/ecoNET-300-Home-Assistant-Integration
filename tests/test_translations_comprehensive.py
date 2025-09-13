#!/usr/bin/env python3
"""Comprehensive test for ecoNET300 entity translations and constants.

This script implements step-by-step logic to check:
1. All sensor keys in ENTITY_SENSOR_DEVICE_CLASS_MAP have translations
2. All binary sensor keys in ENTITY_BINARY_DEVICE_CLASS_MAP have translations
3. All number keys in ENTITY_NUMBER_SENSOR_DEVICE_CLASS_MAP have translations
4. All switch keys have translations
5. All keys have corresponding icons
6. All translations exist in strings.json, en.json, and pl.json
7. Cloud translation reference compliance
"""

import json
import logging
from pathlib import Path
import re
import sys

# Set up logging
_LOGGER = logging.getLogger(__name__)

# Add the custom_components directory to the path
custom_components_path = str(
    Path(__file__).parent.parent / "custom_components" / "econet300"
)
if custom_components_path not in sys.path:
    sys.path.insert(0, custom_components_path)

try:
    from common_functions import camel_to_snake  # type: ignore[import-untyped]
    from const import (  # type: ignore[import-untyped]
        BINARY_SENSOR_MAP_KEY,
        DEFAULT_BINARY_SENSORS,
        DEFAULT_SENSORS,
        # Additional sensor mappings
        ECOMAX360I_SENSORS,
        ECOSOL500_BINARY_SENSORS,
        ECOSOL500_SENSORS,
        ECOSTER_SENSORS,
        ENTITY_BINARY_DEVICE_CLASS_MAP,
        ENTITY_NUMBER_SENSOR_DEVICE_CLASS_MAP,
        ENTITY_SENSOR_DEVICE_CLASS_MAP,
        LAMBDA_SENSORS,
        SENSOR_MAP_KEY,
        SENSOR_MIXER_KEY,
    )

    CONSTANTS_AVAILABLE = True
except ImportError as e:
    _LOGGER.warning("Could not import constants: %s", e)
    CONSTANTS_AVAILABLE = False
    # Define fallback empty values
    ENTITY_BINARY_DEVICE_CLASS_MAP = {}
    ENTITY_NUMBER_SENSOR_DEVICE_CLASS_MAP = {}
    ENTITY_SENSOR_DEVICE_CLASS_MAP = {}
    ECOMAX360I_SENSORS = set()
    ECOSTER_SENSORS = set()
    LAMBDA_SENSORS = set()
    ECOSOL500_SENSORS = set()
    DEFAULT_SENSORS = set()
    DEFAULT_BINARY_SENSORS = set()
    ECOSOL500_BINARY_SENSORS = set()
    BINARY_SENSOR_MAP_KEY = {}
    SENSOR_MAP_KEY = {}

    # Fallback camel_to_snake function
    def camel_to_snake(name: str) -> str:
        """Convert camelCase to snake_case."""
        name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


# Define the paths
BASE_DIR = Path(__file__).parent.parent
STRINGS_FILE = BASE_DIR / "custom_components" / "econet300" / "strings.json"
EN_TRANSLATIONS = (
    BASE_DIR / "custom_components" / "econet300" / "translations" / "en.json"
)
PL_TRANSLATIONS = (
    BASE_DIR / "custom_components" / "econet300" / "translations" / "pl.json"
)
CZ_TRANSLATIONS = (
    BASE_DIR / "custom_components" / "econet300" / "translations" / "cz.json"
)
FR_TRANSLATIONS = (
    BASE_DIR / "custom_components" / "econet300" / "translations" / "fr.json"
)
UK_TRANSLATIONS = (
    BASE_DIR / "custom_components" / "econet300" / "translations" / "uk.json"
)
ICONS_FILE = BASE_DIR / "custom_components" / "econet300" / "icons.json"
CLOUD_TRANSLATIONS_REF = (
    BASE_DIR / "docs" / "cloud_translations" / "MANUAL_TRANSLATION_REFERENCE.md"
)


def load_json_file(file_path: Path) -> dict:
    """Load and parse a JSON file."""
    try:
        with file_path.open(encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        _LOGGER.error("File not found: %s", file_path)
        return {}
    except json.JSONDecodeError as e:
        _LOGGER.error("JSON decode error in %s: %s", file_path, e)
        return {}


def load_cloud_translations_reference() -> dict[str, dict[str, str]]:
    """Load cloud translations reference from the markdown file."""
    cloud_translations = {}

    try:
        with CLOUD_TRANSLATIONS_REF.open(encoding="utf-8") as f:
            content = f.read()

        # Parse the markdown content to extract translations
        # This is a simplified parser - you might need to enhance it
        lines = content.split("\n")

        for line in lines:
            line = line.strip()
            if line.startswith("|") and "|" in line[1:]:
                parts: list[str] = []
                parts.extend(p.strip() for p in line.split("|")[1:-1])
                if len(parts) >= 3 and parts[0] and parts[1] and parts[2]:
                    key = parts[0].strip()
                    english = parts[1].strip()
                    polish = parts[2].strip()

                    if key and english and polish:
                        cloud_translations[key] = {"en": english, "pl": polish}

    except (FileNotFoundError, OSError, UnicodeDecodeError) as e:
        _LOGGER.warning("Could not load cloud translations reference: %s", e)

    return cloud_translations


def step_1_extract_entity_keys_from_constants() -> tuple[set[str], set[str], set[str]]:
    """STEP 1: Extract entity keys from constants."""
    _LOGGER.info("🔑 STEP 1: Extracting entity keys from constants...")

    if not CONSTANTS_AVAILABLE:
        _LOGGER.warning("Constants not available, using empty sets")
        return set(), set(), set()

    # Extract from device class maps (these are the main entity mappings)
    sensor_keys = set(ENTITY_SENSOR_DEVICE_CLASS_MAP.keys())
    binary_sensor_keys = set(ENTITY_BINARY_DEVICE_CLASS_MAP.keys())
    number_keys = set(ENTITY_NUMBER_SENSOR_DEVICE_CLASS_MAP.keys())

    # Extract from additional sensor mappings
    additional_sensor_keys = set()
    additional_binary_sensor_keys = set()

    # Add device-specific sensor mappings
    additional_sensor_keys.update(ECOMAX360I_SENSORS)
    additional_sensor_keys.update(ECOSTER_SENSORS)
    additional_sensor_keys.update(LAMBDA_SENSORS)
    additional_sensor_keys.update(ECOSOL500_SENSORS)
    additional_sensor_keys.update(DEFAULT_SENSORS)

    # Add device-specific binary sensor mappings
    additional_binary_sensor_keys.update(DEFAULT_BINARY_SENSORS)
    additional_binary_sensor_keys.update(ECOSOL500_BINARY_SENSORS)

    # Add keys from mapping dictionaries
    for sensor_set in SENSOR_MAP_KEY.values():
        if isinstance(sensor_set, set):
            additional_sensor_keys.update(sensor_set)

    for binary_sensor_set in BINARY_SENSOR_MAP_KEY.values():
        if isinstance(binary_sensor_set, set):
            additional_binary_sensor_keys.update(binary_sensor_set)

    # Handle dynamically generated mixer keys from SENSOR_MIXER_KEY
    # These generate keys like mixerTemp1, mixerSetTemp1, etc.
    # We need to add the base keys (mixerTemp, mixerSetTemp) for translation matching
    mixer_base_keys = set()
    for mixer_set in SENSOR_MIXER_KEY.values():
        if isinstance(mixer_set, set):
            for key in mixer_set:
                # Extract base key by removing the number suffix
                # e.g., mixerTemp1 -> mixerTemp, mixerSetTemp1 -> mixerSetTemp
                base_key = re.sub(r"\d+$", "", key)
                mixer_base_keys.add(base_key)

    additional_sensor_keys.update(mixer_base_keys)
    _LOGGER.info(
        "   🔧 Added %d mixer base keys: %s",
        len(mixer_base_keys),
        ", ".join(sorted(mixer_base_keys)),
    )

    # Combine all keys
    all_sensor_keys = sensor_keys | additional_sensor_keys
    all_binary_sensor_keys = binary_sensor_keys | additional_binary_sensor_keys

    _LOGGER.info("   📊 Found %d sensor keys from device class maps", len(sensor_keys))
    _LOGGER.info(
        "   📊 Found %d additional sensor keys from mappings",
        len(additional_sensor_keys),
    )
    _LOGGER.info("   📊 Found %d total sensor keys", len(all_sensor_keys))
    _LOGGER.info(
        "   📊 Found %d binary sensor keys from device class maps",
        len(binary_sensor_keys),
    )
    _LOGGER.info(
        "   📊 Found %d additional binary sensor keys from mappings",
        len(additional_binary_sensor_keys),
    )
    _LOGGER.info("   📊 Found %d total binary sensor keys", len(all_binary_sensor_keys))
    _LOGGER.info("   📊 Found %d number keys", len(number_keys))

    # Show breakdown of key sources for debugging
    _LOGGER.info("   🔍 Sensor key breakdown:")
    _LOGGER.info("      - Device class maps: %s", ", ".join(sorted(sensor_keys)[:5]))
    if len(sensor_keys) > 5:
        _LOGGER.info("        ... and %d more", len(sensor_keys) - 5)

    _LOGGER.info("      - ECOMAX360i: %s", ", ".join(sorted(ECOMAX360I_SENSORS)[:3]))
    _LOGGER.info("      - ECOSTER: %s", ", ".join(sorted(ECOSTER_SENSORS)[:3]))
    _LOGGER.info("      - LAMBDA: %s", ", ".join(sorted(LAMBDA_SENSORS)[:3]))
    _LOGGER.info("      - ECOSOL500: %s", ", ".join(sorted(ECOSOL500_SENSORS)[:3]))
    _LOGGER.info("      - DEFAULT: %s", ", ".join(sorted(DEFAULT_SENSORS)[:3]))

    _LOGGER.info("   🔍 Binary sensor key breakdown:")
    _LOGGER.info(
        "      - Device class maps: %s", ", ".join(sorted(binary_sensor_keys)[:3])
    )
    _LOGGER.info("      - DEFAULT: %s", ", ".join(sorted(DEFAULT_BINARY_SENSORS)[:3]))
    _LOGGER.info(
        "      - ECOSOL500: %s", ", ".join(sorted(ECOSOL500_BINARY_SENSORS)[:3])
    )

    return all_sensor_keys, all_binary_sensor_keys, number_keys


def step_2_convert_keys_to_snake_case(
    sensor_keys: set[str], binary_sensor_keys: set[str], number_keys: set[str]
) -> tuple[set[str], set[str], set[str]]:
    """STEP 2: Convert all entity keys from camelCase to snake_case."""
    _LOGGER.info("🐍 STEP 2: Converting keys from camelCase to snake_case...")

    sensor_snake = {camel_to_snake(key) for key in sensor_keys}
    binary_sensor_snake = {camel_to_snake(key) for key in binary_sensor_keys}
    number_snake = {camel_to_snake(key) for key in number_keys}

    _LOGGER.info("   📊 Converted %d sensor keys to snake_case", len(sensor_snake))
    _LOGGER.info(
        "   📊 Converted %d binary sensor keys to snake_case", len(binary_sensor_snake)
    )
    _LOGGER.info("   📊 Converted %d number keys to snake_case", len(number_snake))

    # Show some examples
    if sensor_keys:
        example_key = list(sensor_keys)[0]
        example_snake = camel_to_snake(example_key)
        _LOGGER.info("   💡 Example: '%s' -> '%s'", example_key, example_snake)

    return sensor_snake, binary_sensor_snake, number_snake


def step_3_extract_translation_keys_from_files() -> tuple[
    set[str], set[str], set[str], set[str]
]:
    """STEP 3: Extract translation keys from translation files."""
    _LOGGER.info("🌐 STEP 3: Extracting translation keys from files...")

    strings_data = load_json_file(STRINGS_FILE)

    # Extract sensor keys
    sensor_keys = set()
    if "entity" in strings_data and "sensor" in strings_data["entity"]:
        sensor_keys = set(strings_data["entity"]["sensor"].keys())

    # Extract binary sensor keys
    binary_sensor_keys = set()
    if "entity" in strings_data and "binary_sensor" in strings_data["entity"]:
        binary_sensor_keys = set(strings_data["entity"]["binary_sensor"].keys())

    # Extract number keys
    number_keys = set()
    if "entity" in strings_data and "number" in strings_data["entity"]:
        number_keys = set(strings_data["entity"]["number"].keys())

    # Extract switch keys
    switch_keys = set()
    if "entity" in strings_data and "switch" in strings_data["entity"]:
        switch_keys = set(strings_data["entity"]["switch"].keys())

    _LOGGER.info("   🌐 Found %d sensor translations", len(sensor_keys))
    _LOGGER.info("   🌐 Found %d binary sensor translations", len(binary_sensor_keys))
    _LOGGER.info("   🌐 Found %d number translations", len(number_keys))
    _LOGGER.info("   🌐 Found %d switch translations", len(switch_keys))

    return sensor_keys, binary_sensor_keys, number_keys, switch_keys


def step_4_check_translations_exist(
    entity_snake_keys: set[str], translation_keys: set[str], entity_type: str
) -> tuple[list[str], list[str]]:
    """STEP 4: Check if entity keys have corresponding translations."""
    _LOGGER.info("🔍 STEP 4: Checking %s translations...", entity_type)

    missing_translations = []
    extra_translations = []

    # Check for missing translations
    missing_translations = [
        key for key in entity_snake_keys if key not in translation_keys
    ]

    # Check for extra translations
    extra_translations = [
        key for key in translation_keys if key not in entity_snake_keys
    ]

    _LOGGER.info("   ❌ Missing translations: %d", len(missing_translations))
    _LOGGER.info("   ⚠️  Extra translations: %d", len(extra_translations))

    if missing_translations:
        _LOGGER.info("   📝 Missing: %s", ", ".join(sorted(missing_translations)[:5]))
        if len(missing_translations) > 5:
            _LOGGER.info("   ... and %d more", len(missing_translations) - 5)

    if extra_translations:
        _LOGGER.info("   📝 Extra: %s", ", ".join(sorted(extra_translations)[:5]))
        if len(extra_translations) > 5:
            _LOGGER.info("   ... and %d more", len(extra_translations) - 5)

    return missing_translations, extra_translations


def step_5_check_cloud_translations_reference(
    missing_translations: list[str], entity_type: str
) -> dict[str, list]:
    """STEP 5: Check cloud translations reference for missing translations."""
    _LOGGER.info(
        "☁️  STEP 5: Checking cloud translations reference for %s...", entity_type
    )

    cloud_translations = load_cloud_translations_reference()

    results: dict[str, list] = {
        "found_in_cloud": [],
        "not_found_in_cloud": [],
        "cloud_suggestions": [],
    }

    for missing_key in missing_translations:
        # Try to find the key in cloud translations
        found = False
        for cloud_key, translations in cloud_translations.items():
            if camel_to_snake(cloud_key) == missing_key:
                results["found_in_cloud"].append(
                    {
                        "missing_key": missing_key,
                        "cloud_key": cloud_key,
                        "english": translations.get("en", "N/A"),
                        "polish": translations.get("pl", "N/A"),
                    }
                )
                found = True
                break

        if not found:
            results["not_found_in_cloud"].append(missing_key)

    _LOGGER.info("   ☁️  Found in cloud reference: %d", len(results["found_in_cloud"]))
    _LOGGER.info(
        "   ❌ Not found in cloud reference: %d", len(results["not_found_in_cloud"])
    )

    # Show cloud suggestions
    if results["found_in_cloud"]:
        _LOGGER.info("   💡 Cloud translation suggestions:")
        for item in results["found_in_cloud"][:3]:  # Show first 3
            if isinstance(item, dict):
                _LOGGER.info(
                    "      '%s' -> '%s' (EN: %s, PL: %s)",
                    item.get("missing_key", "N/A"),
                    item.get("cloud_key", "N/A"),
                    item.get("english", "N/A"),
                    item.get("polish", "N/A"),
                )

    return results


def step_6_check_icons_exist(entity_keys: set[str], icon_keys: set[str]) -> list[str]:
    """STEP 6: Check if entity keys have corresponding icons."""
    _LOGGER.info("🎨 STEP 6: Checking icons for entities...")

    missing_icons = []

    missing_icons = [key for key in entity_keys if key not in icon_keys]

    _LOGGER.info("   ❌ Missing icons: %d", len(missing_icons))

    if missing_icons:
        _LOGGER.info(
            "   📝 Missing icons for: %s", ", ".join(sorted(missing_icons)[:5])
        )
        if len(missing_icons) > 5:
            _LOGGER.info("   ... and %d more", len(missing_icons) - 5)

    return missing_icons


def get_api_endpoint_info(key: str) -> dict[str, str]:
    """Get API endpoint information for a given translation key."""
    # Map of known translation keys to their API endpoints and values
    api_mapping = {
        "unseal": {
            "endpoint": "tests/fixtures/ecoMAX810P-L/rmCurrentDataParams.json",
            "parameter_id": "113",
            "name": "Unseal",
            "unit": "31",
            "special": "1",
            "description": "Binary sensor for unseal status (unit 31 = boolean)",
        },
        "weather_control": {
            "endpoint": "tests/fixtures/ecoMAX810P-L/rmParamsData.json",
            "parameter_indices": "79-82, 115",
            "names": "Mixer 1-4 weather control, Weather control the boiler",
            "values": "1, 1, 1, 1, 1",
            "units": "31, 31, 31, 31, 31",
            "ranges": "0-1, 0-1, 0-1, 0-1, 1-1",
            "offsets": "13, 13, 13, 13, 16",
            "description": "Binary sensors for weather control status (unit 31 = boolean)",
        },
    }

    return api_mapping.get(
        key, {"endpoint": "Unknown", "description": "No API mapping found"}
    )


def _check_translation_file_consistency(
    strings_data: dict, translation_data: dict, language: str
) -> list[str]:
    """Check if all keys in strings.json exist in a specific translation file."""
    missing_keys: list[str] = []

    if "entity" in strings_data:
        for entity_type in ["sensor", "binary_sensor", "number", "switch"]:
            if entity_type in strings_data["entity"]:
                missing_keys.extend(
                    f"{entity_type}.{key}"
                    for key in strings_data["entity"][entity_type]
                    if (
                        entity_type not in translation_data.get("entity", {})
                        or key not in translation_data["entity"][entity_type]
                    )
                )

    return missing_keys


def _log_missing_translations_with_api_info(
    missing_keys: list[str], language: str
) -> None:
    """Log missing translations with detailed API information."""
    _LOGGER.info("   ❌ Missing in %s: %d", language, len(missing_keys))

    if missing_keys:
        for missing in sorted(missing_keys):
            entity_type, key = missing.split(".", 1)
            api_info = get_api_endpoint_info(key)
            _LOGGER.info("      - %s", missing)
            _LOGGER.info("        📁 Endpoint: %s", api_info.get("endpoint", "Unknown"))

            # Log API information if available
            if "parameter_id" in api_info:
                _LOGGER.info("        🔑 Parameter ID: %s", api_info["parameter_id"])
            if "parameter_indices" in api_info:
                _LOGGER.info(
                    "        🔑 Parameter Indices: %s", api_info["parameter_indices"]
                )
            if "name" in api_info:
                _LOGGER.info("        📝 Name: %s", api_info["name"])
            if "names" in api_info:
                _LOGGER.info("        📝 Names: %s", api_info["names"])
            if "value" in api_info:
                _LOGGER.info("        💾 Value: %s", api_info["value"])
            if "values" in api_info:
                _LOGGER.info("        💾 Values: %s", api_info["values"])
            if "unit" in api_info:
                _LOGGER.info("        📏 Unit: %s", api_info["unit"])
            if "units" in api_info:
                _LOGGER.info("        📏 Units: %s", api_info["units"])
            if "special" in api_info:
                _LOGGER.info("        ⚙️ Special: %s", api_info["special"])
            if "ranges" in api_info:
                _LOGGER.info("        📊 Ranges: %s", api_info["ranges"])
            if "offsets" in api_info:
                _LOGGER.info("        🔧 Offsets: %s", api_info["offsets"])
            _LOGGER.info(
                "        📋 Description: %s",
                api_info.get("description", "No description"),
            )


def _log_simple_missing_translations(missing_keys: list[str], language: str) -> None:
    """Log missing translations without detailed API information."""
    _LOGGER.info("   ❌ Missing in %s: %d", language, len(missing_keys))

    if missing_keys:
        for missing in sorted(missing_keys):
            _LOGGER.info("      - %s", missing)


def step_7_check_translation_files_consistency() -> dict[str, list[str]]:
    """STEP 7: Check consistency between strings.json, en.json, pl.json, cz.json, fr.json, and uk.json."""
    _LOGGER.info("📋 STEP 7: Checking translation file consistency...")

    # Load all translation files
    strings_data = load_json_file(STRINGS_FILE)
    en_data = load_json_file(EN_TRANSLATIONS)
    pl_data = load_json_file(PL_TRANSLATIONS)
    cz_data = load_json_file(CZ_TRANSLATIONS)
    fr_data = load_json_file(FR_TRANSLATIONS)
    uk_data = load_json_file(UK_TRANSLATIONS)

    # Check consistency for each language
    issues: dict[str, list[str]] = {
        "missing_in_en": _check_translation_file_consistency(
            strings_data, en_data, "English"
        ),
        "missing_in_pl": _check_translation_file_consistency(
            strings_data, pl_data, "Polish"
        ),
        "missing_in_cz": _check_translation_file_consistency(
            strings_data, cz_data, "Czech"
        ),
        "missing_in_fr": _check_translation_file_consistency(
            strings_data, fr_data, "French"
        ),
        "missing_in_uk": _check_translation_file_consistency(
            strings_data, uk_data, "Ukrainian"
        ),
        "missing_in_strings": [],
    }

    # Log results with detailed API information for English and Polish
    _log_missing_translations_with_api_info(issues["missing_in_en"], "English")
    _log_missing_translations_with_api_info(issues["missing_in_pl"], "Polish")

    # Log results without detailed API information for other languages
    _log_simple_missing_translations(issues["missing_in_cz"], "Czech")
    _log_simple_missing_translations(issues["missing_in_fr"], "French")
    _log_simple_missing_translations(issues["missing_in_uk"], "Ukrainian")
    _log_simple_missing_translations(issues["missing_in_strings"], "strings.json")

    return issues


def _generate_summary_statistics(
    sensor_keys: set[str],
    binary_sensor_keys: set[str],
    number_keys: set[str],
    sensor_snake: set[str],
    binary_sensor_snake: set[str],
    number_snake: set[str],
) -> list[str]:
    """Generate summary statistics section of the report."""
    report_lines = []
    report_lines.append("📊 SUMMARY STATISTICS")
    report_lines.append("-" * 30)
    report_lines.append(f"Original sensor keys: {len(sensor_keys)}")
    report_lines.append(f"Original binary sensor keys: {len(binary_sensor_keys)}")
    report_lines.append(f"Original number keys: {len(number_keys)}")
    report_lines.append(f"Snake_case sensor keys: {len(sensor_snake)}")
    report_lines.append(f"Snake_case binary sensor keys: {len(binary_sensor_snake)}")
    report_lines.append(f"Snake_case number keys: {len(number_snake)}")
    report_lines.append("")
    return report_lines


def _generate_translation_issues_section(
    missing_sensor_trans: list[str],
    missing_binary_trans: list[str],
    missing_number_trans: list[str],
) -> list[str]:
    """Generate translation issues section of the report."""
    report_lines = []
    total_missing_translations = (
        len(missing_sensor_trans)
        + len(missing_binary_trans)
        + len(missing_number_trans)
    )

    if total_missing_translations > 0:
        report_lines.append("❌ TRANSLATION ISSUES")
        report_lines.append("-" * 30)
        report_lines.append(f"Missing sensor translations: {len(missing_sensor_trans)}")
        report_lines.append(
            f"Missing binary sensor translations: {len(missing_binary_trans)}"
        )
        report_lines.append(f"Missing number translations: {len(missing_number_trans)}")
        report_lines.append("")

        if missing_sensor_trans:
            report_lines.append("Missing Sensor Translations:")
            report_lines.extend(f"  - {item}" for item in sorted(missing_sensor_trans))
            report_lines.append("")

        if missing_binary_trans:
            report_lines.append("Missing Binary Sensor Translations:")
            report_lines.extend(f"  - {item}" for item in sorted(missing_binary_trans))
            report_lines.append("")

        if missing_number_trans:
            report_lines.append("Missing Number Translations:")
            report_lines.extend(f"  - {item}" for item in sorted(missing_number_trans))
            report_lines.append("")

    return report_lines


def _generate_icon_issues_section(
    missing_sensor_icons: list[str],
    missing_binary_icons: list[str],
    missing_number_icons: list[str],
) -> list[str]:
    """Generate icon issues section of the report."""
    report_lines = []
    total_missing_icons = (
        len(missing_sensor_icons)
        + len(missing_binary_icons)
        + len(missing_number_icons)
    )

    if total_missing_icons > 0:
        report_lines.append("🎨 ICON ISSUES")
        report_lines.append("-" * 30)
        report_lines.append(f"Missing sensor icons: {len(missing_sensor_icons)}")
        report_lines.append(f"Missing binary sensor icons: {len(missing_binary_icons)}")
        report_lines.append(f"Missing number icons: {len(missing_number_icons)}")
        report_lines.append("")

    return report_lines


def _generate_detailed_missing_translations(
    missing_keys: list[str], language: str
) -> list[str]:
    """Generate detailed missing translations with API information."""
    report_lines = []
    if missing_keys:
        report_lines.append(f"Missing in {language}: {len(missing_keys)}")
        for missing in sorted(missing_keys):
            entity_type, key = missing.split(".", 1)
            api_info = get_api_endpoint_info(key)
            report_lines.append(f"  - {missing}")
            report_lines.append(
                f"    📁 Endpoint: {api_info.get('endpoint', 'Unknown')}"
            )
            if "parameter_id" in api_info:
                report_lines.append(f"    🔑 Parameter ID: {api_info['parameter_id']}")
            if "parameter_indices" in api_info:
                report_lines.append(
                    f"    🔑 Parameter Indices: {api_info['parameter_indices']}"
                )
            if "name" in api_info:
                report_lines.append(f"    📝 Name: {api_info['name']}")
            if "names" in api_info:
                report_lines.append(f"    📝 Names: {api_info['names']}")
            if "value" in api_info:
                report_lines.append(f"    💾 Value: {api_info['value']}")
            if "values" in api_info:
                report_lines.append(f"    💾 Values: {api_info['values']}")
            if "unit" in api_info:
                report_lines.append(f"    📏 Unit: {api_info['unit']}")
            if "units" in api_info:
                report_lines.append(f"    📏 Units: {api_info['units']}")
            if "special" in api_info:
                report_lines.append(f"    ⚙️ Special: {api_info['special']}")
            if "ranges" in api_info:
                report_lines.append(f"    📊 Ranges: {api_info['ranges']}")
            if "offsets" in api_info:
                report_lines.append(f"    🔧 Offsets: {api_info['offsets']}")
            report_lines.append(
                f"    📋 Description: {api_info.get('description', 'No description')}"
            )
        report_lines.append("")
    else:
        report_lines.append(f"Missing in {language}: {len(missing_keys)}")
    return report_lines


def _generate_simple_missing_translations(
    missing_keys: list[str], language: str
) -> list[str]:
    """Generate simple missing translations without API information."""
    report_lines = []
    if missing_keys:
        report_lines.append(f"Missing in {language}: {len(missing_keys)}")
        report_lines.extend(f"  - {missing}" for missing in sorted(missing_keys))
        report_lines.append("")
    else:
        report_lines.append(f"Missing in {language}: {len(missing_keys)}")
    return report_lines


def _generate_consistency_issues_section(
    consistency_issues: dict[str, list[str]],
) -> list[str]:
    """Generate consistency issues section of the report."""
    report_lines = []
    total_consistency_issues = (
        len(consistency_issues["missing_in_en"])
        + len(consistency_issues["missing_in_pl"])
        + len(consistency_issues["missing_in_cz"])
        + len(consistency_issues["missing_in_fr"])
        + len(consistency_issues["missing_in_uk"])
        + len(consistency_issues["missing_in_strings"])
    )

    if total_consistency_issues > 0:
        report_lines.append("📋 CONSISTENCY ISSUES")
        report_lines.append("-" * 30)

        # Missing in English and Polish (with detailed API info)
        report_lines.extend(
            _generate_detailed_missing_translations(
                consistency_issues["missing_in_en"], "English"
            )
        )
        report_lines.extend(
            _generate_detailed_missing_translations(
                consistency_issues["missing_in_pl"], "Polish"
            )
        )

        # Missing in other languages (simple format)
        for lang_key, lang_name in [
            ("missing_in_cz", "Czech"),
            ("missing_in_fr", "French"),
            ("missing_in_uk", "Ukrainian"),
            ("missing_in_strings", "strings.json"),
        ]:
            report_lines.extend(
                _generate_simple_missing_translations(
                    consistency_issues[lang_key], lang_name
                )
            )

        report_lines.append("")

    return report_lines


def step_8_check_entity_type_mismatches(
    sensor_snake: set[str], binary_sensor_snake: set[str], number_snake: set[str]
) -> list[str]:
    """STEP 8: Check for entity type mismatches between constants and translation files."""
    _LOGGER.info("🔑 STEP 8: Checking entity type mismatches...")

    strings_data = load_json_file(STRINGS_FILE)

    # Create a mapping of entity keys to their correct entity type
    entity_type_map = {}
    for key in sensor_snake:
        entity_type_map[key] = "sensor"
    for key in binary_sensor_snake:
        entity_type_map[key] = "binary_sensor"
    for key in number_snake:
        entity_type_map[key] = "number"

    mismatches = []

    if "entity" in strings_data:
        for entity_type in ["sensor", "binary_sensor", "number", "switch"]:
            if entity_type in strings_data["entity"]:
                for key in strings_data["entity"][entity_type]:
                    expected_entity_type = entity_type_map.get(key)
                    if expected_entity_type and expected_entity_type != entity_type:
                        mismatches.append(
                            f"'{key}' should be in {expected_entity_type} section, not {entity_type}"
                        )

    _LOGGER.info("   ❌ Entity type mismatches: %d", len(mismatches))

    if mismatches:
        _LOGGER.info("   📝 Mismatches: %s", ", ".join(mismatches[:3]))
        if len(mismatches) > 3:
            _LOGGER.info("   ... and %d more", len(mismatches) - 3)

    return mismatches


def step_9_generate_comprehensive_report(
    sensor_keys: set[str],
    binary_sensor_keys: set[str],
    number_keys: set[str],
    sensor_snake: set[str],
    binary_sensor_snake: set[str],
    number_snake: set[str],
    missing_sensor_trans: list[str],
    missing_binary_trans: list[str],
    missing_number_trans: list[str],
    missing_sensor_icons: list[str],
    missing_binary_icons: list[str],
    missing_number_icons: list[str],
    consistency_issues: dict[str, list[str]],
    entity_type_mismatches: list[str],
    cloud_results: dict[str, dict],
) -> str:
    """STEP 9: Generate comprehensive test report."""
    _LOGGER.info("📋 STEP 9: Generating comprehensive report...")

    report_lines = []
    report_lines.append("ecoNET300 Comprehensive Translation Test Report")
    report_lines.append("=" * 60)
    report_lines.append("")

    # Generate each section using helper functions
    report_lines.extend(
        _generate_summary_statistics(
            sensor_keys,
            binary_sensor_keys,
            number_keys,
            sensor_snake,
            binary_sensor_snake,
            number_snake,
        )
    )

    report_lines.extend(
        _generate_translation_issues_section(
            missing_sensor_trans, missing_binary_trans, missing_number_trans
        )
    )

    report_lines.extend(
        _generate_icon_issues_section(
            missing_sensor_icons, missing_binary_icons, missing_number_icons
        )
    )

    report_lines.extend(_generate_consistency_issues_section(consistency_issues))

    # Entity type mismatches
    if entity_type_mismatches:
        report_lines.append("🔑 ENTITY TYPE MISMATCHES")
        report_lines.append("-" * 30)
        report_lines.extend(
            f"  - {mismatch}" for mismatch in sorted(entity_type_mismatches)
        )
        report_lines.append("")

    # Cloud translation suggestions
    if cloud_results.get("found_in_cloud"):
        report_lines.append("☁️  CLOUD TRANSLATION SUGGESTIONS")
        report_lines.append("-" * 30)
        for item in cloud_results["found_in_cloud"]:
            if isinstance(item, dict):
                report_lines.append(
                    f"  - {item.get('missing_key', 'N/A')} -> {item.get('cloud_key', 'N/A')}"
                )
                report_lines.append(f"    EN: {item.get('english', 'N/A')}")
                report_lines.append(f"    PL: {item.get('polish', 'N/A')}")
                report_lines.append("")

    # Total issues
    total_missing_translations = (
        len(missing_sensor_trans)
        + len(missing_binary_trans)
        + len(missing_number_trans)
    )
    total_missing_icons = (
        len(missing_sensor_icons)
        + len(missing_binary_icons)
        + len(missing_number_icons)
    )
    total_consistency_issues = sum(
        len(issues) for issues in consistency_issues.values()
    )
    total_issues = (
        total_missing_translations
        + total_missing_icons
        + total_consistency_issues
        + len(entity_type_mismatches)
    )

    report_lines.append("=" * 60)
    if total_issues == 0:
        report_lines.append("🎉 ALL TESTS PASSED! No issues found.")
    else:
        report_lines.append(f"⚠️  TOTAL ISSUES FOUND: {total_issues}")
    report_lines.append("=" * 60)

    return "\n".join(report_lines)


def main():
    """Implement main test function with step-by-step logic."""
    # Configure logging for console output
    logging.basicConfig(
        level=logging.INFO, format="%(message)s", handlers=[logging.StreamHandler()]
    )

    _LOGGER.info("🔍 ecoNET300 Comprehensive Translation Test")
    _LOGGER.info("=" * 60)
    _LOGGER.info("Implementing step-by-step translation validation logic...")
    _LOGGER.info("")

    # STEP 1: Extract entity keys from constants
    sensor_keys, binary_sensor_keys, number_keys = (
        step_1_extract_entity_keys_from_constants()
    )
    _LOGGER.info("")

    # STEP 2: Convert keys to snake_case
    sensor_snake, binary_sensor_snake, number_snake = step_2_convert_keys_to_snake_case(
        sensor_keys, binary_sensor_keys, number_keys
    )
    _LOGGER.info("")

    # STEP 3: Extract translation keys from files
    (
        trans_sensor_keys,
        trans_binary_sensor_keys,
        trans_number_keys,
        trans_switch_keys,
    ) = step_3_extract_translation_keys_from_files()
    _LOGGER.info("")

    # STEP 4: Check translations exist
    missing_sensor_trans, extra_sensor_trans = step_4_check_translations_exist(
        sensor_snake, trans_sensor_keys, "sensor"
    )
    _LOGGER.info("")

    missing_binary_trans, extra_binary_trans = step_4_check_translations_exist(
        binary_sensor_snake, trans_binary_sensor_keys, "binary_sensor"
    )
    _LOGGER.info("")

    missing_number_trans, extra_number_trans = step_4_check_translations_exist(
        number_snake, trans_number_keys, "number"
    )
    _LOGGER.info("")

    # STEP 5: Check cloud translations reference
    cloud_sensor_results = step_5_check_cloud_translations_reference(
        missing_sensor_trans, "sensor"
    )
    _LOGGER.info("")

    cloud_binary_results = step_5_check_cloud_translations_reference(
        missing_binary_trans, "binary_sensor"
    )
    _LOGGER.info("")

    cloud_number_results = step_5_check_cloud_translations_reference(
        missing_number_trans, "number"
    )
    _LOGGER.info("")

    # STEP 6: Check icons exist
    icons_data = load_json_file(ICONS_FILE)
    icon_keys = set(icons_data.keys()) if icons_data else set()
    missing_sensor_icons = step_6_check_icons_exist(sensor_keys, icon_keys)
    _LOGGER.info("")

    missing_binary_icons = step_6_check_icons_exist(binary_sensor_keys, icon_keys)
    _LOGGER.info("")

    missing_number_icons = step_6_check_icons_exist(number_keys, icon_keys)
    _LOGGER.info("")

    # STEP 7: Check translation file consistency
    consistency_issues = step_7_check_translation_files_consistency()
    _LOGGER.info("")

    # STEP 8: Check entity type mismatches
    entity_type_mismatches = step_8_check_entity_type_mismatches(
        sensor_snake, binary_sensor_snake, number_snake
    )
    _LOGGER.info("")

    # STEP 9: Generate comprehensive report
    report_content = step_9_generate_comprehensive_report(
        sensor_keys,
        binary_sensor_keys,
        number_keys,
        sensor_snake,
        binary_sensor_snake,
        number_snake,
        missing_sensor_trans,
        missing_binary_trans,
        missing_number_trans,
        missing_sensor_icons,
        missing_binary_icons,
        missing_number_icons,
        consistency_issues,
        entity_type_mismatches,
        {
            "sensor": cloud_sensor_results,
            "binary_sensor": cloud_binary_results,
            "number": cloud_number_results,
        },
    )

    # Display final report
    _LOGGER.info("=" * 60)
    _LOGGER.info("📋 FINAL TEST RESULTS")
    _LOGGER.info("=" * 60)
    _LOGGER.info("")
    _LOGGER.info(report_content)

    # Save detailed report to file
    report_file = BASE_DIR / "tests" / "test_reports" / "translation_test_report.txt"
    report_file.parent.mkdir(exist_ok=True)
    with report_file.open("w", encoding="utf-8") as f:
        f.write(report_content)

    _LOGGER.info("")
    _LOGGER.info("📄 Detailed report saved to: %s", report_file)


if __name__ == "__main__":
    main()
