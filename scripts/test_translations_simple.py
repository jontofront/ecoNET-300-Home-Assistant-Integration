#!/usr/bin/env python3
"""Simple test for ecoNET300 entity translations and constants.

This script checks:
1. All sensor keys in ENTITY_SENSOR_DEVICE_CLASS_MAP have translations
2. All binary sensor keys in ENTITY_BINARY_DEVICE_CLASS_MAP have translations
3. All number keys in ENTITY_NUMBER_SENSOR_DEVICE_CLASS_MAP have translations
4. All keys have corresponding icons
5. All translations exist in strings.json, en.json, and pl.json
"""

import json
import logging
from pathlib import Path
import re
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# Add the custom_components directory to the path
custom_components_path = str(
    Path(__file__).parent.parent / "custom_components" / "econet300"
)
sys.path.insert(0, custom_components_path)

try:
    from const import (  # type: ignore[import-untyped]
        ENTITY_BINARY_DEVICE_CLASS_MAP,
        ENTITY_NUMBER_SENSOR_DEVICE_CLASS_MAP,
        ENTITY_SENSOR_DEVICE_CLASS_MAP,
    )
except ImportError as e:
    logger.error("Error importing constants: %s", e)
    logger.error("Tried to import from: %s", custom_components_path)
    logger.error("Current sys.path: %s...", sys.path[:3])
    sys.exit(1)


def load_json_file(file_path: Path) -> dict:
    """Load and parse a JSON file."""
    try:
        with file_path.open(encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("❌ File not found: %s", file_path)
        return {}
    except json.JSONDecodeError as e:
        logger.error("❌ JSON decode error in %s: %s", file_path, e)
        return {}


def camel_to_snake(name: str) -> str:
    """Convert camelCase to snake_case."""
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def check_entity_translations(
    entity_map: dict,
    entity_type: str,
    strings_data: dict,
    en_data: dict,
    pl_data: dict,
    icons_data: dict,
) -> dict[str, list[str]]:
    """Check translations for a specific entity type."""
    issues: dict[str, list[str]] = {
        "missing_translations": [],
        "missing_in_en": [],
        "missing_in_pl": [],
        "missing_icons": [],
    }

    entity_keys = set(entity_map.keys())

    # Check if entity type exists in strings.json
    if "entity" not in strings_data or entity_type not in strings_data["entity"]:
        issues["missing_translations"].extend(
            [f"Missing {entity_type} section in strings.json"]
        )
        return issues

    translation_keys = set(strings_data["entity"][entity_type].keys())

    # Check each entity key has translation
    for key in entity_keys:
        snake_key = camel_to_snake(key)
        if snake_key not in translation_keys:
            issues["missing_translations"].append(f"{key} -> {snake_key}")

    # Check if translations exist in en.json
    if "entity" not in en_data or entity_type not in en_data["entity"]:
        issues["missing_in_en"].append(f"Missing {entity_type} section in en.json")
    else:
        en_keys = set(en_data["entity"][entity_type].keys())
        for key in translation_keys:
            if key not in en_keys:
                issues["missing_in_en"].append(f"{entity_type}.{key}")

    # Check if translations exist in pl.json
    if "entity" not in pl_data or entity_type not in pl_data["entity"]:
        issues["missing_in_pl"].append(f"Missing {entity_type} section in pl.json")
    else:
        pl_keys = set(pl_data["entity"][entity_type].keys())
        for key in translation_keys:
            if key not in pl_keys:
                issues["missing_in_pl"].append(f"{entity_type}.{key}")

    # Check if icons exist
    icon_keys = set(icons_data.keys()) if icons_data else set()
    for key in entity_keys:
        if key not in icon_keys:
            issues["missing_icons"].append(key)

    return issues


def main():
    """Run the main test function."""
    logger.info("🔍 ecoNET300 Translation Test")
    logger.info("=" * 40)

    # Define file paths
    base_dir = Path(__file__).parent.parent
    strings_file = base_dir / "custom_components" / "econet300" / "strings.json"
    en_file = base_dir / "custom_components" / "econet300" / "translations" / "en.json"
    pl_file = base_dir / "custom_components" / "econet300" / "translations" / "pl.json"
    icons_file = base_dir / "custom_components" / "econet300" / "icons.json"

    # Load files
    logger.info("📁 Loading files...")
    strings_data = load_json_file(strings_file)
    en_data = load_json_file(en_file)
    pl_data = load_json_file(pl_file)
    icons_data = load_json_file(icons_file)

    if not all([strings_data, en_data, pl_data, icons_data]):
        logger.error("❌ Failed to load required files")
        return

    logger.info("✅ All files loaded successfully")
    logger.info("")

    # Check each entity type
    logger.info("🔍 Checking entity translations...")

    # Sensors
    logger.info("\n📊 Checking SENSORS...")
    sensor_issues = check_entity_translations(
        ENTITY_SENSOR_DEVICE_CLASS_MAP,
        "sensor",
        strings_data,
        en_data,
        pl_data,
        icons_data,
    )

    # Binary Sensors
    logger.info("\n📊 Checking BINARY SENSORS...")
    binary_issues = check_entity_translations(
        ENTITY_BINARY_DEVICE_CLASS_MAP,
        "binary_sensor",
        strings_data,
        en_data,
        pl_data,
        icons_data,
    )

    # Numbers
    logger.info("\n📊 Checking NUMBERS...")
    number_issues = check_entity_translations(
        ENTITY_NUMBER_SENSOR_DEVICE_CLASS_MAP,
        "number",
        strings_data,
        en_data,
        pl_data,
        icons_data,
    )

    # Generate report
    logger.info("\n%s", "=" * 40)
    logger.info("📋 TEST RESULTS")
    logger.info("=" * 40)

    all_issues = []

    # Sensor issues
    if any(sensor_issues.values()):
        logger.warning("\n❌ SENSOR ISSUES:")
        for issue_type, issues in sensor_issues.items():
            if issues:
                logger.warning("   %s:", issue_type.upper())
                for issue in issues:
                    logger.warning("     - %s", issue)
                    all_issues.append(f"SENSOR: {issue}")

    # Binary sensor issues
    if any(binary_issues.values()):
        logger.warning("\n❌ BINARY SENSOR ISSUES:")
        for issue_type, issues in binary_issues.items():
            if issues:
                logger.warning("   %s:", issue_type.upper())
                for issue in issues:
                    logger.warning("     - %s", issue)
                    all_issues.append(f"BINARY_SENSOR: {issue}")

    # Number issues
    if any(number_issues.values()):
        logger.warning("\n❌ NUMBER ISSUES:")
        for issue_type, issues in number_issues.items():
            if issues:
                logger.warning("   %s:", issue_type.upper())
                for issue in issues:
                    logger.warning("     - %s", issue)
                    all_issues.append(f"NUMBER: {issue}")

    # Summary
    logger.info("\n%s", "=" * 40)
    if not all_issues:
        logger.info("🎉 ALL TESTS PASSED! No issues found.")
    else:
        logger.warning("⚠️  TOTAL ISSUES FOUND: %s", len(all_issues))
        logger.info("\n📄 Issues will be saved to: translation_issues.txt")

        # Save issues to file
        with (base_dir / "translation_issues.txt").open("w", encoding="utf-8") as f:
            f.write("ecoNET300 Translation Issues Report\n")
            f.write("=" * 40 + "\n\n")
            for issue in all_issues:
                f.write(f"{issue}\n")

    logger.info("=" * 40)


if __name__ == "__main__":
    main()
