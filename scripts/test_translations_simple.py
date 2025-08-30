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
from pathlib import Path
import sys
from typing import Dict, List

# Add the custom_components directory to the path
sys.path.insert(
    0, str(Path(__file__).parent.parent / "custom_components" / "econet300")
)

try:
    from const import (
        ENTITY_BINARY_DEVICE_CLASS_MAP,
        ENTITY_NUMBER_SENSOR_DEVICE_CLASS_MAP,
        ENTITY_SENSOR_DEVICE_CLASS_MAP,
    )
except ImportError as e:
    print(f"Error importing constants: {e}")
    sys.exit(1)


def load_json_file(file_path: Path) -> Dict:
    """Load and parse a JSON file."""
    try:
        with open(file_path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error in {file_path}: {e}")
        return {}


def camel_to_snake(name: str) -> str:
    """Convert camelCase to snake_case."""
    import re

    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def check_entity_translations(
    entity_map: Dict,
    entity_type: str,
    strings_data: Dict,
    en_data: Dict,
    pl_data: Dict,
    icons_data: Dict,
) -> Dict[str, List[str]]:
    """Check translations for a specific entity type."""
    issues = {
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
    """Main test function."""
    print("🔍 ecoNET300 Translation Test")
    print("=" * 40)

    # Define file paths
    base_dir = Path(__file__).parent.parent
    strings_file = base_dir / "custom_components" / "econet300" / "strings.json"
    en_file = base_dir / "custom_components" / "econet300" / "translations" / "en.json"
    pl_file = base_dir / "custom_components" / "econet300" / "translations" / "pl.json"
    icons_file = base_dir / "custom_components" / "econet300" / "icons.json"

    # Load files
    print("📁 Loading files...")
    strings_data = load_json_file(strings_file)
    en_data = load_json_file(en_file)
    pl_data = load_json_file(pl_file)
    icons_data = load_json_file(icons_file)

    if not all([strings_data, en_data, pl_data, icons_data]):
        print("❌ Failed to load required files")
        return

    print("✅ All files loaded successfully")
    print()

    # Check each entity type
    print("🔍 Checking entity translations...")

    # Sensors
    print("\n📊 Checking SENSORS...")
    sensor_issues = check_entity_translations(
        ENTITY_SENSOR_DEVICE_CLASS_MAP,
        "sensor",
        strings_data,
        en_data,
        pl_data,
        icons_data,
    )

    # Binary Sensors
    print("\n📊 Checking BINARY SENSORS...")
    binary_issues = check_entity_translations(
        ENTITY_BINARY_DEVICE_CLASS_MAP,
        "binary_sensor",
        strings_data,
        en_data,
        pl_data,
        icons_data,
    )

    # Numbers
    print("\n📊 Checking NUMBERS...")
    number_issues = check_entity_translations(
        ENTITY_NUMBER_SENSOR_DEVICE_CLASS_MAP,
        "number",
        strings_data,
        en_data,
        pl_data,
        icons_data,
    )

    # Generate report
    print("\n" + "=" * 40)
    print("📋 TEST RESULTS")
    print("=" * 40)

    all_issues = []

    # Sensor issues
    if any(sensor_issues.values()):
        print("\n❌ SENSOR ISSUES:")
        for issue_type, issues in sensor_issues.items():
            if issues:
                print(f"   {issue_type.upper()}:")
                for issue in issues:
                    print(f"     - {issue}")
                    all_issues.append(f"SENSOR: {issue}")

    # Binary sensor issues
    if any(binary_issues.values()):
        print("\n❌ BINARY SENSOR ISSUES:")
        for issue_type, issues in binary_issues.items():
            if issues:
                print(f"   {issue_type.upper()}:")
                for issue in issues:
                    print(f"     - {issue}")
                    all_issues.append(f"BINARY_SENSOR: {issue}")

    # Number issues
    if any(number_issues.values()):
        print("\n❌ NUMBER ISSUES:")
        for issue_type, issues in number_issues.items():
            if issues:
                print(f"   {issue_type.upper()}:")
                for issue in issues:
                    print(f"     - {issue}")
                    all_issues.append(f"NUMBER: {issue}")

    # Summary
    print("\n" + "=" * 40)
    if not all_issues:
        print("🎉 ALL TESTS PASSED! No issues found.")
    else:
        print(f"⚠️  TOTAL ISSUES FOUND: {len(all_issues)}")
        print("\n📄 Issues will be saved to: translation_issues.txt")

        # Save issues to file
        with open(base_dir / "translation_issues.txt", "w", encoding="utf-8") as f:
            f.write("ecoNET300 Translation Issues Report\n")
            f.write("=" * 40 + "\n\n")
            for issue in all_issues:
                f.write(f"{issue}\n")

    print("=" * 40)


if __name__ == "__main__":
    main()
