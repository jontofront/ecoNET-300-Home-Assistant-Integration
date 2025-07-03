#!/usr/bin/env python3
"""Validate translation consistency for ecoNET300 integration."""

import json
import logging
from pathlib import Path
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
_LOGGER = logging.getLogger(__name__)


def load_json_file(file_path: Path) -> dict:
    """Load and parse a JSON file."""
    try:
        with file_path.open(encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        _LOGGER.error("JSON syntax error in %s: %s", file_path, e)
        sys.exit(1)
    except FileNotFoundError:
        _LOGGER.error("File not found: %s", file_path)
        sys.exit(1)


def extract_entity_keys(data: dict, prefix: str = "") -> set[str]:
    """Recursively extract all entity keys from translation data."""
    keys = set()
    if isinstance(data, dict):
        for value in data.values():
            if isinstance(value, dict):
                for entity_key, entity_data in value.items():
                    if isinstance(entity_data, dict) and "name" in entity_data:
                        keys.add(entity_key)
            else:
                keys.update(extract_entity_keys(value, prefix))
    return keys


def check_translation_consistency() -> bool:
    """Check translation consistency across all files."""
    base_path = Path("custom_components/econet300")
    strings_json = load_json_file(base_path / "strings.json")
    en_json = load_json_file(base_path / "translations" / "en.json")
    pl_json = load_json_file(base_path / "translations" / "pl.json")
    _LOGGER.info("Checking translation consistency...")
    strings_keys = extract_entity_keys(strings_json)
    en_keys = extract_entity_keys(en_json)
    pl_keys = extract_entity_keys(pl_json)
    _LOGGER.info("Found %d keys in strings.json", len(strings_keys))
    _LOGGER.info("Found %d keys in en.json", len(en_keys))
    _LOGGER.info("Found %d keys in pl.json", len(pl_keys))
    missing_in_en = strings_keys - en_keys
    missing_in_pl = strings_keys - pl_keys
    extra_in_en = en_keys - strings_keys
    extra_in_pl = pl_keys - strings_keys
    issues_found = False
    if missing_in_en:
        _LOGGER.error("Missing keys in en.json: %s", sorted(missing_in_en))
        issues_found = True
    if missing_in_pl:
        _LOGGER.error("Missing keys in pl.json: %s", sorted(missing_in_pl))
        issues_found = True
    if extra_in_en:
        _LOGGER.warning("Extra keys in en.json: %s", sorted(extra_in_en))
        issues_found = True
    if extra_in_pl:
        _LOGGER.warning("Extra keys in pl.json: %s", sorted(extra_in_pl))
        issues_found = True
    if not issues_found:
        _LOGGER.info("All translation files are consistent!")
    else:
        _LOGGER.info(
            "To fix missing translations, add them to the respective language files."
        )
        _LOGGER.info(
            "To fix extra translations, remove them or add them to strings.json if needed."
        )
    return not issues_found


def check_json_syntax() -> bool:
    """Check JSON syntax for all translation files."""
    base_path = Path("custom_components/econet300")
    files_to_check = [
        base_path / "strings.json",
        base_path / "translations" / "en.json",
        base_path / "translations" / "pl.json",
    ]
    _LOGGER.info("Checking JSON syntax...")
    all_valid = True
    results = []
    for file_path in files_to_check:
        result = {"name": file_path.name, "error": None}
        try:
            load_json_file(file_path)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            result["error"] = e
            all_valid = False
        results.append(result)
    for r in results:
        if r["error"] is None:
            _LOGGER.info("%s: Valid JSON", r["name"])
        else:
            _LOGGER.error("%s: %s", r["name"], r["error"])
    return all_valid


def main() -> None:
    """Run translation validation."""
    _LOGGER.info("ecoNET300 Translation Validation")
    _LOGGER.info("=" * 40)
    syntax_ok = check_json_syntax()
    _LOGGER.info("")
    if syntax_ok:
        consistency_ok = check_translation_consistency()
        if consistency_ok:
            _LOGGER.info("All translation checks passed!")
            sys.exit(0)
        else:
            _LOGGER.error("Translation consistency issues found.")
            sys.exit(1)
    else:
        _LOGGER.error("JSON syntax errors found.")
        sys.exit(1)


if __name__ == "__main__":
    main()
