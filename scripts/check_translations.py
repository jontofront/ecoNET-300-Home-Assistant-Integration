#!/usr/bin/env python3
# ruff: noqa: T201
"""Translation checker for ecoNET300 integration.

This script helps ensure all translation files are updated when adding new entities.
"""

import json
from pathlib import Path
import sys

# Paths to translation files
STRINGS_FILE = "custom_components/econet300/strings.json"
EN_TRANSLATIONS = "custom_components/econet300/translations/en.json"
PL_TRANSLATIONS = "custom_components/econet300/translations/pl.json"


def load_json_file(file_path):
    """Load and parse a JSON file."""
    try:
        with Path(file_path).open(encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON error in {file_path}: {e}")
        return None


def get_entity_keys(data, entity_type):
    """Extract entity keys from translation data."""
    keys = set()
    if data and "entity" in data and entity_type in data["entity"]:
        keys.update(data["entity"][entity_type].keys())
    return keys


def check_translations():
    """Check if all translation files are in sync."""
    print("🔍 Checking translation files...")

    # Load all translation files
    strings_data = load_json_file(STRINGS_FILE)
    en_data = load_json_file(EN_TRANSLATIONS)
    pl_data = load_json_file(PL_TRANSLATIONS)

    if not all([strings_data, en_data, pl_data]):
        print("❌ Failed to load one or more translation files")
        return False

    # Check each entity type
    entity_types = ["binary_sensor", "sensor", "switch", "number"]
    all_good = True

    for entity_type in entity_types:
        print(f"\n📋 Checking {entity_type}...")

        strings_keys = get_entity_keys(strings_data, entity_type)
        en_keys = get_entity_keys(en_data, entity_type)
        pl_keys = get_entity_keys(pl_data, entity_type)

        # Find missing keys
        missing_in_en = strings_keys - en_keys
        missing_in_pl = strings_keys - pl_keys
        missing_in_strings = (en_keys | pl_keys) - strings_keys

        if missing_in_en:
            print(f"❌ Missing in en.json: {missing_in_en}")
            all_good = False

        if missing_in_pl:
            print(f"❌ Missing in pl.json: {missing_in_pl}")
            all_good = False

        if missing_in_strings:
            print(f"❌ Missing in strings.json: {missing_in_strings}")
            all_good = False

        if not any([missing_in_en, missing_in_pl, missing_in_strings]):
            print(f"✅ {entity_type}: All translation files in sync")

    if all_good:
        print("\n🎉 All translation files are in sync!")
    else:
        print(
            "\n⚠️  Translation files are out of sync. Please update missing translations."
        )

    return all_good


if __name__ == "__main__":
    success = check_translations()
    sys.exit(0 if success else 1)
