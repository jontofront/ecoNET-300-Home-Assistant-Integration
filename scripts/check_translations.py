#!/usr/bin/env python3
# ruff: noqa: T201
"""Translation checker for ecoNET300 integration.

This script helps ensure all translation files are updated when adding new entities.
"""

import json
from pathlib import Path
import sys

STRINGS_FILE = Path("custom_components/econet300/strings.json")
TRANSLATIONS_DIR = Path("custom_components/econet300/translations")

# Complete translations: a missing key fails the check.
REQUIRED_LANGUAGES = ("en", "pl", "de")
# Partial translations: Home Assistant shows English for missing keys.
PARTIAL_LANGUAGES = ("cz", "fr", "uk")

ENTITY_TYPES = ("binary_sensor", "sensor", "switch", "number")


def load_json_file(file_path: Path) -> dict | None:
    """Load and parse a JSON file."""
    try:
        with file_path.open(encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ JSON error in {file_path}: {e}")
        return None


def get_entity_keys(data: dict, entity_type: str) -> set[str]:
    """Extract entity keys from translation data."""
    return set(data.get("entity", {}).get(entity_type, {}))


def check_translations() -> bool:
    """Check that translation files are in sync with strings.json."""
    print("🔍 Checking translation files...")

    strings_data = load_json_file(STRINGS_FILE)
    translations = {
        language: load_json_file(TRANSLATIONS_DIR / f"{language}.json")
        for language in (*REQUIRED_LANGUAGES, *PARTIAL_LANGUAGES)
    }
    if strings_data is None or any(data is None for data in translations.values()):
        print("❌ Failed to load one or more translation files")
        return False

    all_good = True
    for entity_type in ENTITY_TYPES:
        print(f"\n📋 Checking {entity_type}...")
        strings_keys = get_entity_keys(strings_data, entity_type)
        translated_keys: set[str] = set()
        type_good = True

        for language, data in translations.items():
            keys = get_entity_keys(data, entity_type)
            translated_keys |= keys
            missing = strings_keys - keys
            if not missing:
                continue
            if language in REQUIRED_LANGUAGES:
                print(f"❌ Missing in {language}.json: {sorted(missing)}")
                type_good = False
            else:
                print(f"⚠️  {language}.json: {len(missing)} not translated")

        unknown_keys = translated_keys - strings_keys
        if unknown_keys:
            print(f"❌ Missing in strings.json: {sorted(unknown_keys)}")
            type_good = False

        if type_good:
            print(f"✅ {entity_type}: required translations in sync")
        all_good = all_good and type_good

    if all_good:
        print("\n🎉 Required translation files are in sync!")
    else:
        print(
            "\n⚠️  Translation files are out of sync. Please update missing translations."
        )

    return all_good


if __name__ == "__main__":
    success = check_translations()
    sys.exit(0 if success else 1)
