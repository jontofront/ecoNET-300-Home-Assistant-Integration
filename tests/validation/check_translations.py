#!/usr/bin/env python3
"""Translation validation script for ecoNET300 integration."""

import json
import sys
from pathlib import Path
from typing import Dict, Set, List


def load_json_file(file_path: Path) -> Dict:
    """Load and parse a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ JSON syntax error in {file_path}: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        sys.exit(1)


def extract_entity_keys(data: Dict, prefix: str = "") -> Set[str]:
    """Recursively extract all entity keys from translation data."""
    keys = set()
    
    if isinstance(data, dict):
        for key, value in data.items():
            current_path = f"{prefix}.{key}" if prefix else key
            
            if key == "entity":
                # Extract entity keys
                if isinstance(value, dict):
                    for entity_type, entities in value.items():
                        if isinstance(entities, dict):
                            for entity_key, entity_data in entities.items():
                                if isinstance(entity_data, dict) and "name" in entity_data:
                                    keys.add(entity_key)
            else:
                # Recursively search other sections
                keys.update(extract_entity_keys(value, current_path))
    
    return keys


def check_translation_consistency():
    """Check translation consistency across all files."""
    base_path = Path("custom_components/econet300")
    
    # Load translation files
    strings_json = load_json_file(base_path / "strings.json")
    en_json = load_json_file(base_path / "translations" / "en.json")
    pl_json = load_json_file(base_path / "translations" / "pl.json")
    
    print("🔍 Checking translation consistency...")
    
    # Extract entity keys from each file
    strings_keys = extract_entity_keys(strings_json)
    en_keys = extract_entity_keys(en_json)
    pl_keys = extract_entity_keys(pl_json)
    
    print(f"📊 Found {len(strings_keys)} keys in strings.json")
    print(f"📊 Found {len(en_keys)} keys in en.json")
    print(f"📊 Found {len(pl_keys)} keys in pl.json")
    
    # Check for missing keys
    missing_in_en = strings_keys - en_keys
    missing_in_pl = strings_keys - pl_keys
    
    # Check for extra keys
    extra_in_en = en_keys - strings_keys
    extra_in_pl = pl_keys - strings_keys
    
    # Report results
    issues_found = False
    
    if missing_in_en:
        print(f"❌ Missing keys in en.json: {sorted(missing_in_en)}")
        issues_found = True
    
    if missing_in_pl:
        print(f"❌ Missing keys in pl.json: {sorted(missing_in_pl)}")
        issues_found = True
    
    if extra_in_en:
        print(f"⚠️  Extra keys in en.json: {sorted(extra_in_en)}")
        issues_found = True
    
    if extra_in_pl:
        print(f"⚠️  Extra keys in pl.json: {sorted(extra_in_pl)}")
        issues_found = True
    
    if not issues_found:
        print("✅ All translation files are consistent!")
    else:
        print("\n💡 To fix missing translations, add them to the respective language files.")
        print("💡 To fix extra translations, remove them or add them to strings.json if needed.")
    
    return not issues_found


def check_json_syntax():
    """Check JSON syntax for all translation files."""
    base_path = Path("custom_components/econet300")
    files_to_check = [
        base_path / "strings.json",
        base_path / "translations" / "en.json",
        base_path / "translations" / "pl.json"
    ]
    
    print("🔍 Checking JSON syntax...")
    
    all_valid = True
    for file_path in files_to_check:
        try:
            load_json_file(file_path)
            print(f"✅ {file_path.name}: Valid JSON")
        except Exception as e:
            print(f"❌ {file_path.name}: {e}")
            all_valid = False
    
    return all_valid


def main():
    """Main validation function."""
    print("🌐 ecoNET300 Translation Validation")
    print("=" * 40)
    
    # Check JSON syntax first
    syntax_ok = check_json_syntax()
    print()
    
    if syntax_ok:
        # Check translation consistency
        consistency_ok = check_translation_consistency()
        
        if consistency_ok:
            print("\n🎉 All translation checks passed!")
            sys.exit(0)
        else:
            print("\n❌ Translation consistency issues found.")
            sys.exit(1)
    else:
        print("\n❌ JSON syntax errors found.")
        sys.exit(1)


if __name__ == "__main__":
    main() 