#!/usr/bin/env python3
"""Test script to check if keys from fixture files are binary sensors or regular sensors.

This script analyzes the regParams.json and sysParams.json files to determine:
- True/False values = Binary sensors
- Other values = Regular sensors

Also checks for entity type mismatches in the Home Assistant integration constants.
"""

import json
import logging
from pathlib import Path
import sys

# Set up logging
_LOGGER = logging.getLogger(__name__)

# Define the paths to fixture files
BASE_DIR = Path(__file__).parent
REG_PARAMS_FILE = BASE_DIR / "fixtures" / "ecoMAX810P-L" / "regParams.json"
SYS_PARAMS_FILE = BASE_DIR / "fixtures" / "ecoMAX810P-L" / "sysParams.json"

# Add the custom_components directory to the path to import constants
sys.path.insert(0, str(BASE_DIR.parent / "custom_components" / "econet300"))

# Try to import constants at module level
try:
    from const import (  # type: ignore[import-untyped]
        DEFAULT_BINARY_SENSORS,
        DEFAULT_SENSORS,
        ENTITY_BINARY_DEVICE_CLASS_MAP,
        ENTITY_SENSOR_DEVICE_CLASS_MAP,
    )

    CONSTANTS_AVAILABLE = True
except ImportError as e:
    _LOGGER.warning("Could not import constants: %s", e)
    CONSTANTS_AVAILABLE = False
    # Define fallback empty values
    DEFAULT_BINARY_SENSORS = []
    DEFAULT_SENSORS = []
    ENTITY_BINARY_DEVICE_CLASS_MAP = {}
    ENTITY_SENSOR_DEVICE_CLASS_MAP = {}


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


def analyze_entity_types(data: dict) -> tuple[list[str], list[str]]:
    """Analyze data to determine which keys are binary sensors vs regular sensors."""
    binary_sensors = []
    regular_sensors = []

    for key, value in data.items():
        if isinstance(value, bool):
            # Boolean values (True/False) indicate binary sensors
            binary_sensors.append(key)
        else:
            # Non-boolean values indicate regular sensors
            regular_sensors.append(key)

    return binary_sensors, regular_sensors


def check_entity_type_mismatches(
    fixture_binary: list[str], fixture_regular: list[str]
) -> dict[str, list[str]]:
    """Check for entity type mismatches between fixtures and Home Assistant constants."""
    if not CONSTANTS_AVAILABLE:
        return {
            "wrong_binary_sensors": [],
            "wrong_regular_sensors": [],
            "missing_binary_sensors": [],
            "missing_regular_sensors": [],
            "mismatches": [],
            "recommendations": [],
        }

    wrong_binary_sensors = []
    wrong_regular_sensors = []
    missing_binary_sensors = []
    missing_regular_sensors = []
    mismatches = []
    recommendations = []

    # Create sets for easy comparison
    ha_binary = set(ENTITY_BINARY_DEVICE_CLASS_MAP.keys())
    ha_sensors = set(ENTITY_SENSOR_DEVICE_CLASS_MAP.keys())
    ha_default_binary = set(DEFAULT_BINARY_SENSORS)
    ha_default_sensors = set(DEFAULT_SENSORS)

    # Check fixture binary sensors against HA constants
    for key in fixture_binary:
        if key in ha_sensors:
            wrong_binary_sensors.append(key)
            mismatches.append(
                f"'{key}' is in fixture as binary sensor but defined as sensor in HA"
            )
            recommendations.append(
                f"Move '{key}' from DEFAULT_SENSORS to DEFAULT_BINARY_SENSORS"
            )
        elif key not in ha_binary and key not in ha_default_binary:
            missing_binary_sensors.append(key)
            recommendations.append(
                f"Add '{key}' to DEFAULT_BINARY_SENSORS (fixture shows boolean value)"
            )

    # Check fixture regular sensors against HA constants
    for key in fixture_regular:
        if key in ha_binary or key in ha_default_binary:
            wrong_regular_sensors.append(key)
            mismatches.append(
                f"'{key}' is in fixture as regular sensor but defined as binary sensor in HA"
            )
            recommendations.append(
                f"Move '{key}' from DEFAULT_BINARY_SENSORS to DEFAULT_SENSORS"
            )
        elif key not in ha_sensors and key not in ha_default_sensors:
            missing_regular_sensors.append(key)
            recommendations.append(
                f"Add '{key}' to DEFAULT_SENSORS (fixture shows non-boolean value)"
            )

    return {
        "wrong_binary_sensors": wrong_binary_sensors,
        "wrong_regular_sensors": wrong_regular_sensors,
        "missing_binary_sensors": missing_binary_sensors,
        "missing_regular_sensors": missing_regular_sensors,
        "mismatches": mismatches,
        "recommendations": recommendations,
    }


def print_analysis(title: str, binary_sensors: list[str], regular_sensors: list[str]):
    """Print the analysis results in a formatted way."""
    _LOGGER.info("=" * 60)
    _LOGGER.info("📊 %s", title)
    _LOGGER.info("=" * 60)

    _LOGGER.info("🔘 BINARY SENSORS (%d):", len(binary_sensors))
    if binary_sensors:
        for key in sorted(binary_sensors):
            _LOGGER.info("   ✅ %s", key)
    else:
        _LOGGER.info("   (none found)")

    _LOGGER.info("📊 REGULAR SENSORS (%d):", len(regular_sensors))
    if regular_sensors:
        for key in sorted(regular_sensors):
            _LOGGER.info("   📈 %s", key)
    else:
        _LOGGER.info("   (none found)")


def print_home_assistant_recommendations():
    """Print Home Assistant documentation recommendations for entity types."""
    _LOGGER.info("=" * 60)
    _LOGGER.info("🏠 HOME ASSISTANT ENTITY TYPE RECOMMENDATIONS")
    _LOGGER.info("=" * 60)

    _LOGGER.info("🔘 BINARY SENSORS should be used for:")
    _LOGGER.info("   • On/Off states (True/False)")
    _LOGGER.info("   • Connection status (wifi, lan, mainSrv)")
    _LOGGER.info("   • Operational status (pumps, fans, thermostats)")
    _LOGGER.info("   • Contact sensors (doors, windows)")
    _LOGGER.info("   • Presence detection")
    _LOGGER.info("   • Error states")

    _LOGGER.info("📊 REGULAR SENSORS should be used for:")
    _LOGGER.info("   • Temperature measurements")
    _LOGGER.info("   • Pressure readings")
    _LOGGER.info("   • Power consumption")
    _LOGGER.info("   • Version numbers")
    _LOGGER.info("   • Configuration values")
    _LOGGER.info("   • Status codes (non-boolean)")

    _LOGGER.info("🔧 DEVICE CLASSES for Binary Sensors:")
    _LOGGER.info("   • BinarySensorDeviceClass.CONNECTIVITY - for wifi, lan, mainSrv")
    _LOGGER.info("   • BinarySensorDeviceClass.RUNNING - for operational status")
    _LOGGER.info("   • BinarySensorDeviceClass.PRESENCE - for presence detection")
    _LOGGER.info("   • BinarySensorDeviceClass.OPENING - for contact sensors")

    _LOGGER.info("🔧 DEVICE CLASSES for Sensors:")
    _LOGGER.info("   • SensorDeviceClass.TEMPERATURE - for temperature values")
    _LOGGER.info("   • SensorDeviceClass.POWER - for power measurements")
    _LOGGER.info("   • SensorDeviceClass.SIGNAL_STRENGTH - for signal quality")
    _LOGGER.info("   • None - for version numbers, status codes, etc.")


def print_mismatch_analysis(mismatches: dict[str, list[str]]):
    """Print detailed analysis of entity type mismatches."""
    _LOGGER.info("=" * 80)
    _LOGGER.info("🔍 ENTITY TYPE MISMATCH ANALYSIS")
    _LOGGER.info("=" * 80)

    # Wrong entity type assignments
    if mismatches["wrong_binary_sensors"]:
        _LOGGER.info(
            "❌ SENSORS INCORRECTLY IN BINARY_SENSORS (%d):",
            len(mismatches["wrong_binary_sensors"]),
        )
        _LOGGER.info(
            "   These should be moved from DEFAULT_BINARY_SENSORS to DEFAULT_SENSORS:"
        )
        for key in sorted(mismatches["wrong_binary_sensors"]):
            _LOGGER.info(
                "   🔴 %s - Fixture shows non-boolean value (should be sensor)", key
            )

    if mismatches["wrong_regular_sensors"]:
        _LOGGER.info(
            "❌ BINARY SENSORS INCORRECTLY IN SENSORS (%d):",
            len(mismatches["wrong_regular_sensors"]),
        )
        _LOGGER.info(
            "   These should be moved from DEFAULT_SENSORS to DEFAULT_BINARY_SENSORS:"
        )
        for key in sorted(mismatches["wrong_regular_sensors"]):
            _LOGGER.info(
                "   🔴 %s - Fixture shows boolean value (should be binary_sensor)", key
            )

    # Missing entities
    if mismatches["missing_binary_sensors"]:
        _LOGGER.info(
            "⚠️  MISSING BINARY SENSORS (%d):", len(mismatches["missing_binary_sensors"])
        )
        _LOGGER.info(
            "   These are in fixtures as binary sensors but not defined in const.py:"
        )
        for key in sorted(mismatches["missing_binary_sensors"]):
            _LOGGER.info("   🟡 %s - Add to DEFAULT_BINARY_SENSORS", key)

    if mismatches["missing_regular_sensors"]:
        _LOGGER.info(
            "⚠️  MISSING REGULAR SENSORS (%d):",
            len(mismatches["missing_regular_sensors"]),
        )
        _LOGGER.info(
            "   These are in fixtures as regular sensors but not defined in const.py:"
        )
        for key in sorted(mismatches["missing_regular_sensors"]):
            _LOGGER.info("   🟡 %s - Add to DEFAULT_SENSORS", key)

    # Summary
    total_issues: int = (
        len(mismatches["wrong_binary_sensors"])
        + len(mismatches["wrong_regular_sensors"])
        + len(mismatches["missing_binary_sensors"])
        + len(mismatches["missing_regular_sensors"])
    )

    if total_issues == 0:
        _LOGGER.info("✅ NO ENTITY TYPE MISMATCHES FOUND!")
    else:
        _LOGGER.info("📊 TOTAL ISSUES FOUND: %d", total_issues)


def generate_separate_tables(
    reg_params: dict, sys_params: dict, all_binary: list[str], all_regular: list[str]
) -> str:
    """Generate three separate tables for better organization."""
    if not CONSTANTS_AVAILABLE:
        return "Error: Could not import constants"

    # Create sets for easy comparison
    ha_binary = set(ENTITY_BINARY_DEVICE_CLASS_MAP.keys())
    ha_sensors = set(ENTITY_SENSOR_DEVICE_CLASS_MAP.keys())
    ha_default_binary = set(DEFAULT_BINARY_SENSORS)
    ha_default_sensors = set(DEFAULT_SENSORS)

    # Collect all entities from fixtures
    all_entities = []
    for key, value in reg_params.items():
        all_entities.append((key, value, "regParams.json"))
    for key, value in sys_params.items():
        all_entities.append((key, value, "sysParams.json"))

    # Categorize entities
    missing_entities = []
    type_mismatches = []
    correct_entities = []

    for key, value, source in all_entities:
        entity_type = "BINARY_SENSOR" if isinstance(value, bool) else "SENSOR"
        in_const = (
            "YES"
            if key in ha_binary
            or key in ha_sensors
            or key in ha_default_binary
            or key in ha_default_sensors
            else "NO"
        )

        # Determine actual type in constants
        actual_type = "UNKNOWN"
        if key in ha_binary or key in ha_default_binary:
            actual_type = "BINARY_SENSOR"
        elif key in ha_sensors or key in ha_default_sensors:
            actual_type = "SENSOR"

        # Categorize
        if in_const == "NO":
            missing_entities.append((key, entity_type, source))
        elif entity_type != actual_type:
            type_mismatches.append((key, entity_type, actual_type, source))
        else:
            correct_entities.append((key, entity_type, source))

    # Generate tables
    tables = []

    # Table 1: Missing entities
    tables.append("=" * 80)
    tables.append("📋 TABLE 1: ENTITIES NOT IN CONSTANTS (NEED TO BE ADDED)")
    tables.append("=" * 80)
    tables.append("KEY | ENTITY_TYPE | SOURCE_FILE")
    tables.append("-" * 50)
    for key, entity_type, source in sorted(missing_entities):
        tables.append(f"{key:<20} | {entity_type:<12} | {source}")
    tables.append(f"\nTotal missing: {len(missing_entities)} entities\n")

    # Table 2: Type mismatches
    tables.append("=" * 80)
    tables.append("⚠️  TABLE 2: ENTITIES WITH DIFFERENT TYPES (MISMATCHES)")
    tables.append("=" * 80)
    tables.append("KEY | EXPECTED_TYPE | ACTUAL_TYPE | SOURCE_FILE")
    tables.append("-" * 60)
    for key, expected_type, actual_type, source in sorted(type_mismatches):
        tables.append(f"{key:<20} | {expected_type:<13} | {actual_type:<12} | {source}")
    tables.append(f"\nTotal mismatches: {len(type_mismatches)} entities\n")

    # Table 3: Correctly configured entities
    tables.append("=" * 80)
    tables.append("✅ TABLE 3: ENTITIES THAT ARE THE SAME (CORRECTLY CONFIGURED)")
    tables.append("=" * 80)
    tables.append("KEY | ENTITY_TYPE | SOURCE_FILE")
    tables.append("-" * 50)
    for key, entity_type, source in sorted(correct_entities):
        tables.append(f"{key:<20} | {entity_type:<12} | {source}")
    tables.append(f"\nTotal correct: {len(correct_entities)} entities\n")

    # Summary
    tables.append("=" * 80)
    tables.append("📊 SUMMARY")
    tables.append("=" * 80)
    tables.append(f"Total entities analyzed: {len(all_entities)}")
    tables.append(f"Missing entities: {len(missing_entities)}")
    tables.append(f"Type mismatches: {len(type_mismatches)}")
    tables.append(f"Correctly configured: {len(correct_entities)}")

    return "\n".join(tables)


def save_separate_tables_report(
    reg_params: dict, sys_params: dict, all_binary: list[str], all_regular: list[str]
):
    """Save the separate tables report to a file."""
    report_content = generate_separate_tables(
        reg_params, sys_params, all_binary, all_regular
    )

    report_file = BASE_DIR / "separate_tables_analysis.txt"
    with report_file.open("w", encoding="utf-8") as f:
        f.write("ecoNET300 Separate Tables Analysis Report\n")
        f.write("=" * 60 + "\n\n")
        f.write("Three separate tables for better organization:\n")
        f.write("1. Missing entities (not in constants)\n")
        f.write("2. Type mismatches (different types)\n")
        f.write("3. Correctly configured entities\n")
        f.write("=" * 60 + "\n\n")
        f.write(report_content)

    _LOGGER.info("📊 Separate tables report saved to: %s", report_file)
    return report_file


def main():
    """Run the main test function."""
    # Configure logging for console output
    logging.basicConfig(
        level=logging.INFO, format="%(message)s", handlers=[logging.StreamHandler()]
    )

    _LOGGER.info("🔍 ecoNET300 Fixture Entity Type Analysis")
    _LOGGER.info("=" * 60)

    # Load regParams.json
    _LOGGER.info("📁 Loading regParams.json...")
    reg_params = load_json_file(REG_PARAMS_FILE)

    if not reg_params:
        _LOGGER.error("Failed to load regParams.json")
        return

    _LOGGER.info("✅ Loaded %d keys from regParams.json", len(reg_params))

    # Load sysParams.json
    _LOGGER.info("📁 Loading sysParams.json...")
    sys_params = load_json_file(SYS_PARAMS_FILE)

    if not sys_params:
        _LOGGER.error("Failed to load sysParams.json")
        return

    _LOGGER.info("✅ Loaded %d keys from sysParams.json", len(sys_params))

    # Analyze regParams.json
    reg_binary, reg_regular = analyze_entity_types(reg_params)
    print_analysis("regParams.json Analysis", reg_binary, reg_regular)

    # Analyze sysParams.json
    sys_binary, sys_regular = analyze_entity_types(sys_params)
    print_analysis("sysParams.json Analysis", sys_binary, sys_regular)

    # Combined analysis
    all_binary = reg_binary + sys_binary
    all_regular = reg_regular + sys_regular

    print_analysis("COMBINED Analysis", all_binary, all_regular)

    # Check for entity type mismatches
    _LOGGER.info("=" * 60)
    _LOGGER.info("🔍 CHECKING ENTITY TYPE MISMATCHES")
    _LOGGER.info("=" * 60)

    mismatches = check_entity_type_mismatches(all_binary, all_regular)

    if mismatches["mismatches"]:
        _LOGGER.info("❌ ENTITY TYPE MISMATCHES (%d):", len(mismatches["mismatches"]))
        for mismatch in mismatches["mismatches"]:
            _LOGGER.info("   ⚠️  %s", mismatch)
    else:
        _LOGGER.info("✅ No entity type mismatches found!")

    if mismatches["recommendations"]:
        _LOGGER.info("💡 RECOMMENDATIONS (%d):", len(mismatches["recommendations"]))
        for rec in mismatches["recommendations"]:
            _LOGGER.info("   🔧 %s", rec)

    # Print detailed mismatch analysis
    print_mismatch_analysis(mismatches)

    # Print Home Assistant recommendations
    print_home_assistant_recommendations()

    # Summary statistics
    _LOGGER.info("=" * 60)
    _LOGGER.info("📋 SUMMARY STATISTICS")
    _LOGGER.info("=" * 60)
    _LOGGER.info("📁 regParams.json: %d total keys", len(reg_params))
    _LOGGER.info("   🔘 Binary sensors: %d", len(reg_binary))
    _LOGGER.info("   📊 Regular sensors: %d", len(reg_regular))

    _LOGGER.info("📁 sysParams.json: %d total keys", len(sys_params))
    _LOGGER.info("   🔘 Binary sensors: %d", len(sys_binary))
    _LOGGER.info("   📊 Regular sensors: %d", len(sys_regular))

    _LOGGER.info("🔍 TOTAL ANALYSIS:")
    _LOGGER.info("   🔘 Binary sensors: %d", len(all_binary))
    _LOGGER.info("   📊 Regular sensors: %d", len(all_regular))
    _LOGGER.info("   📈 Total entities: %d", len(all_binary) + len(all_regular))

    # Save detailed report to file
    report_file = BASE_DIR / "fixture_entity_analysis.txt"
    with report_file.open("w", encoding="utf-8") as f:
        f.write("ecoNET300 Fixture Entity Type Analysis Report\n")
        f.write("=" * 60 + "\n\n")

        f.write("regParams.json Analysis:\n")
        f.write("-" * 30 + "\n")
        f.write(f"Binary sensors ({len(reg_binary)}):\n")
        f.writelines(f"  - {key}\n" for key in sorted(reg_binary))
        f.write(f"\nRegular sensors ({len(reg_regular)}):\n")
        f.writelines(f"  - {key}\n" for key in sorted(reg_regular))

        f.write("\nsysParams.json Analysis:\n")
        f.write("-" * 30 + "\n")
        f.write(f"Binary sensors ({len(sys_binary)}):\n")
        f.writelines(f"  - {key}\n" for key in sorted(sys_binary))
        f.write(f"\nRegular sensors ({len(sys_regular)}):\n")
        f.writelines(f"  - {key}\n" for key in sorted(sys_regular))

        f.write("\nCombined Analysis:\n")
        f.write("-" * 30 + "\n")
        f.write(f"Total binary sensors: {len(all_binary)}\n")
        f.write(f"Total regular sensors: {len(all_regular)}\n")
        f.write(f"Total entities: {len(all_binary) + len(all_regular)}\n")

        if mismatches["mismatches"]:
            f.write(f"\nEntity Type Mismatches ({len(mismatches['mismatches'])}):\n")
            f.write("-" * 30 + "\n")
            for mismatch in mismatches["mismatches"]:
                f.write(f"  - {mismatch}\n")

        if mismatches["recommendations"]:
            f.write(f"\nRecommendations ({len(mismatches['recommendations'])}):\n")
            f.write("-" * 30 + "\n")
            for rec in mismatches["recommendations"]:
                f.write(f"  - {rec}\n")

    _LOGGER.info("📄 Detailed report saved to: %s", report_file)

    # Save detailed table report
    save_separate_tables_report(reg_params, sys_params, all_binary, all_regular)


if __name__ == "__main__":
    main()
