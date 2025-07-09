#!/usr/bin/env python3
"""
Extract and organize cloud translations from downloaded JavaScript files.

This script processes the downloaded translation files from econet24.com
and creates a structured reference document for use in the Home Assistant integration.
"""

import json
import re
import os
from pathlib import Path
from typing import Dict, List, Any

def extract_translations_from_js(file_path: str) -> Dict[str, Any]:
    """Extract translations from a JavaScript file."""
    translations = {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for trans["en"] = {...} patterns
        pattern = r'trans\["([^"]+)"\]\s*=\s*({[^}]+})'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for lang, trans_obj in matches:
            # Clean up the JavaScript object
            trans_obj = trans_obj.strip()
            # Remove trailing comma if present
            if trans_obj.endswith(','):
                trans_obj = trans_obj[:-1]
            
            try:
                # Parse as JSON (with some cleanup)
                trans_obj = trans_obj.replace("'", '"')  # Replace single quotes
                trans_obj = re.sub(r',\s*}', '}', trans_obj)  # Remove trailing commas
                trans_obj = re.sub(r',\s*]', ']', trans_obj)  # Remove trailing commas in arrays
                
                parsed = json.loads(trans_obj)
                translations[lang] = parsed
            except json.JSONDecodeError as e:
                print(f"Warning: Could not parse translations for {lang} in {file_path}: {e}")
                continue
    
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return translations

def extract_alarms_from_js(file_path: str) -> Dict[str, Dict[int, str]]:
    """Extract alarm translations from JavaScript file."""
    alarms = {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for trans_alarms["en"] = {...} patterns
        pattern = r'trans_alarms\["([^"]+)"\]\s*=\s*({[^}]+})'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for lang, alarms_obj in matches:
            # Clean up the JavaScript object
            alarms_obj = alarms_obj.strip()
            if alarms_obj.endswith(','):
                alarms_obj = alarms_obj[:-1]
            
            try:
                # Parse as JSON
                alarms_obj = alarms_obj.replace("'", '"')
                alarms_obj = re.sub(r',\s*}', '}', alarms_obj)
                
                parsed = json.loads(alarms_obj)
                alarms[lang] = parsed
            except json.JSONDecodeError as e:
                print(f"Warning: Could not parse alarms for {lang} in {file_path}: {e}")
                continue
    
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    
    return alarms

def categorize_translations(translations: Dict[str, Dict[str, str]]) -> Dict[str, Dict[str, str]]:
    """Categorize translations by type."""
    categories = {
        'ui_general': {},
        'boiler_control': {},
        'sensors': {},
        'parameters': {},
        'alarms': {},
        'modes': {},
        'temperatures': {},
        'other': {}
    }
    
    # Keywords for categorization
    boiler_keywords = ['boiler', 'furnace', 'heating', 'burner', 'flame', 'fuel', 'feeder']
    sensor_keywords = ['temp', 'temperature', 'sensor', 'probe', 'lambda', 'pressure', 'flow']
    parameter_keywords = ['param', 'setting', 'config', 'hysteresis', 'correction', 'curve']
    alarm_keywords = ['alarm', 'error', 'fault', 'warning']
    mode_keywords = ['mode', 'work', 'operation', 'status']
    temp_keywords = ['temp', 'temperature', 'heat', 'cool']
    
    for lang, lang_translations in translations.items():
        for key, value in lang_translations.items():
            key_lower = key.lower()
            
            # Categorize based on keywords
            if any(keyword in key_lower for keyword in boiler_keywords):
                categories['boiler_control'][key] = value
            elif any(keyword in key_lower for keyword in sensor_keywords):
                categories['sensors'][key] = value
            elif any(keyword in key_lower for keyword in parameter_keywords):
                categories['parameters'][key] = value
            elif any(keyword in key_lower for keyword in alarm_keywords):
                categories['alarms'][key] = value
            elif any(keyword in key_lower for keyword in mode_keywords):
                categories['modes'][key] = value
            elif any(keyword in key_lower for keyword in temp_keywords):
                categories['temperatures'][key] = value
            elif key in ['save', 'cancel', 'ok', 'error', 'loading', 'refresh', 'update']:
                categories['ui_general'][key] = value
            else:
                categories['other'][key] = value
    
    return categories

def create_reference_document(translations: Dict[str, Dict[str, str]], 
                            alarms: Dict[str, Dict[int, str]]) -> str:
    """Create a markdown reference document."""
    doc = """# Cloud Translation Reference

This document contains translations extracted from the official econet24.com cloud service.
These translations can be used as a reference when adding new entities to the Home Assistant integration.

## Languages Available

"""
    
    # List available languages
    for lang in sorted(translations.keys()):
        doc += f"- **{lang}**: {len(translations[lang])} translations\n"
    
    doc += "\n## Translation Categories\n\n"
    
    # Categorize translations
    categories = categorize_translations(translations)
    
    for category_name, category_translations in categories.items():
        if not category_translations:
            continue
            
        doc += f"### {category_name.replace('_', ' ').title()}\n\n"
        doc += "| Key | English | Polish |\n"
        doc += "|-----|---------|--------|\n"
        
        # Get English and Polish translations
        en_trans = translations.get('en', {})
        pl_trans = translations.get('pl', {})
        
        for key in sorted(category_translations.keys()):
            en_value = en_trans.get(key, '')
            pl_value = pl_trans.get(key, '')
            
            # Escape pipe characters in values
            en_value = en_value.replace('|', '\\|')
            pl_value = pl_value.replace('|', '\\|')
            
            doc += f"| `{key}` | {en_value} | {pl_value} |\n"
        
        doc += "\n"
    
    # Add alarms section
    if alarms:
        doc += "## Alarm Codes\n\n"
        doc += "| Code | English | Polish |\n"
        doc += "|------|---------|--------|\n"
        
        en_alarms = alarms.get('en', {})
        pl_alarms = alarms.get('pl', {})
        
        for code in sorted(en_alarms.keys(), key=lambda x: int(x) if str(x).isdigit() else 999):
            en_value = en_alarms.get(code, '')
            pl_value = pl_alarms.get(code, '')
            
            en_value = en_value.replace('|', '\\|')
            pl_value = pl_value.replace('|', '\\|')
            
            doc += f"| {code} | {en_value} | {pl_value} |\n"
    
    return doc

def main():
    """Main function to extract and organize translations."""
    js_files_dir = Path("docs/cloud_translations/js_files")
    output_dir = Path("docs/cloud_translations")
    
    if not js_files_dir.exists():
        print(f"Error: {js_files_dir} does not exist. Please run download_cloud_translations.py first.")
        return
    
    # Find all JavaScript files
    js_files = list(js_files_dir.glob("*.js"))
    
    if not js_files:
        print("No JavaScript files found.")
        return
    
    print(f"Processing {len(js_files)} JavaScript files...")
    
    all_translations = {}
    all_alarms = {}
    
    # Process each file
    for js_file in js_files:
        print(f"Processing {js_file.name}...")
        
        # Extract regular translations
        translations = extract_translations_from_js(str(js_file))
        for lang, lang_translations in translations.items():
            if lang not in all_translations:
                all_translations[lang] = {}
            all_translations[lang].update(lang_translations)
        
        # Extract alarm translations
        alarms = extract_alarms_from_js(str(js_file))
        for lang, lang_alarms in alarms.items():
            if lang not in all_alarms:
                all_alarms[lang] = {}
            all_alarms[lang].update(lang_alarms)
    
    # Create reference document
    print("Creating reference document...")
    reference_doc = create_reference_document(all_translations, all_alarms)
    
    # Save reference document
    output_file = output_dir / "TRANSLATION_REFERENCE.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(reference_doc)
    
    print(f"Reference document saved to {output_file}")
    
    # Save raw translations as JSON for programmatic use
    raw_output_file = output_dir / "raw_translations.json"
    with open(raw_output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'translations': all_translations,
            'alarms': all_alarms
        }, f, indent=2, ensure_ascii=False)
    
    print(f"Raw translations saved to {raw_output_file}")
    
    # Print summary
    print("\nSummary:")
    for lang in sorted(all_translations.keys()):
        print(f"  {lang}: {len(all_translations[lang])} translations")
    
    if all_alarms:
        print("\nAlarms:")
        for lang in sorted(all_alarms.keys()):
            print(f"  {lang}: {len(all_alarms[lang])} alarm codes")

if __name__ == "__main__":
    main() 