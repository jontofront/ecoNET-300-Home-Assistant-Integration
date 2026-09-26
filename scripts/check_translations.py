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
CZ_TRANSLATIONS = "custom_components/econet300/translations/cz.json"
FR_TRANSLATIONS = "custom_components/econet300/translations/fr.json"
UK_TRANSLATIONS = "custom_components/econet300/translations/uk.json"
DE_TRANSLATIONS = "custom_components/econet300/translations/de.json"


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
    cz_data = load_json_file(CZ_TRANSLATIONS)
    fr_data = load_json_file(FR_TRANSLATIONS)
    uk_data = load_json_file(UK_TRANSLATIONS)
    de_data = load_json_file(DE_TRANSLATIONS)

    if not all([strings_data, en_data, pl_data, cz_data, fr_data, uk_data, de_data]):
        print("❌ Failed to load one or more translation files")
        return False

    # Check each entity type
    entity_types = ["binary_sensor", "sensor", "switch", "number"]
    all_good = True

    # Accumulate missing keys per file across all entity types
    files_missing = {
        "en.json": set(),
        "pl.json": set(),
        "cz.json": set(),
        "fr.json": set(),
        "uk.json": set(),
        "de.json": set(),
    }

    for entity_type in entity_types:
        print(f"\n📋 Checking {entity_type}...")

        strings_keys = get_entity_keys(strings_data, entity_type)
        en_keys = get_entity_keys(en_data, entity_type)
        pl_keys = get_entity_keys(pl_data, entity_type)
        cz_keys = get_entity_keys(cz_data, entity_type)
        fr_keys = get_entity_keys(fr_data, entity_type)
        uk_keys = get_entity_keys(uk_data, entity_type)
        de_keys = get_entity_keys(de_data, entity_type)

        # Find missing keys
        missing_in_en = strings_keys - en_keys
        missing_in_pl = strings_keys - pl_keys
        missing_in_cz = strings_keys - cz_keys
        missing_in_fr = strings_keys - fr_keys
        missing_in_uk = strings_keys - uk_keys
        missing_in_de = strings_keys - de_keys
        missing_in_strings = (
            en_keys | pl_keys | cz_keys | fr_keys | uk_keys | de_keys
        ) - strings_keys

        files_missing["en.json"] |= missing_in_en
        files_missing["pl.json"] |= missing_in_pl
        files_missing["cz.json"] |= missing_in_cz
        files_missing["fr.json"] |= missing_in_fr
        files_missing["uk.json"] |= missing_in_uk
        files_missing["de.json"] |= missing_in_de

        if missing_in_en:
            print(f"❌ Missing in en.json: {missing_in_en}")
            all_good = False

        if missing_in_pl:
            print(f"❌ Missing in pl.json: {missing_in_pl}")
            all_good = False

        if missing_in_cz:
            print(f"❌ Missing in cz.json: {missing_in_cz}")
            all_good = False

        if missing_in_fr:
            print(f"❌ Missing in fr.json: {missing_in_fr}")
            all_good = False

        if missing_in_uk:
            print(f"❌ Missing in uk.json: {missing_in_uk}")
            all_good = False

        if missing_in_de:
            print(f"❌ Missing in de.json: {missing_in_de}")
            all_good = False

        if missing_in_strings:
            print(f"❌ Missing in strings.json: {missing_in_strings}")
            all_good = False

        if not any(
            [
                missing_in_en,
                missing_in_pl,
                missing_in_cz,
                missing_in_fr,
                missing_in_uk,
                missing_in_de,
                missing_in_strings,
            ]
        ):
            print(f"✅ {entity_type}: All translation files in sync")

    print("\n📄 Per-file sync status:")
    for file_name, missing_keys in files_missing.items():
        if not missing_keys:
            print(f"✅ {file_name} is fully in sync with strings.json")

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
