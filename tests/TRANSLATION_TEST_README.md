# ecoNET300 Comprehensive Translation Test

## Overview

This test script implements a step-by-step logic to validate all entity translations in the ecoNET300 Home Assistant integration. It checks for missing translations, icon mismatches, and ensures consistency across all translation files.

## What the Test Does

### 🔑 STEP 1: Extract Entity Keys from Constants

- Extracts sensor keys from `ENTITY_SENSOR_DEVICE_CLASS_MAP`
- Extracts binary sensor keys from `ENTITY_BINARY_DEVICE_CLASS_MAP`
- Extracts number keys from `ENTITY_NUMBER_SENSOR_DEVICE_CLASS_MAP`

### 🐍 STEP 2: Convert Keys to snake_case

- Uses `common_functions.camel_to_snake()` to convert all camelCase keys
- Example: `mixerSetTemp2` → `mixer_set_temp2`
- This is crucial because Home Assistant translation keys use snake_case

### 🌐 STEP 3: Extract Translation Keys from Files

- Loads `strings.json`, `en.json`, and `pl.json`
- Extracts existing translation keys for each entity type
- Identifies sensor, binary_sensor, number, and switch translations

### 🔍 STEP 4: Check Translations Exist

- Compares snake_case entity keys with translation keys
- Identifies missing translations (entities without translations)
- Identifies extra translations (translations without entities)

### ☁️ STEP 5: Check Cloud Translations Reference

- Loads cloud translation reference from `MANUAL_TRANSLATION_REFERENCE.md`
- Suggests official translations for missing keys
- Helps maintain consistency with ecoNET cloud terminology

### 🎨 STEP 6: Check Icons Exist

- Verifies that all entity keys have corresponding icons in `icons.json`
- Identifies missing icons that need to be added

### 📋 STEP 7: Check Translation File Consistency

- Ensures all keys in `strings.json` exist in `en.json` and `pl.json`
- Identifies missing English or Polish translations

### 🔑 STEP 8: Check Entity Type Mismatches

- Verifies that entities are in the correct translation sections
- Example: A sensor shouldn't be in the binary_sensor section

### 📋 STEP 9: Generate Comprehensive Report

- Creates detailed report with all findings
- Saves report to `translation_test_report.txt`
- Provides actionable recommendations

## Key Features

### Translation Validation

- **Missing Translations**: Entities that exist in constants but lack translations
- **Extra Translations**: Translations that exist but don't correspond to entities
- **Cloud Reference**: Suggests official translations from ecoNET cloud

### Icon Validation

- Ensures every entity has a corresponding icon
- Prevents entities from appearing without visual representation

### Consistency Checks

- Cross-references all three translation files
- Identifies missing English or Polish translations
- Ensures entity type categorization is correct

### Step-by-Step Logic

- Each step is clearly defined and logged
- Easy to debug and understand the validation process
- Comprehensive error reporting

## Usage

```bash
# Run the comprehensive translation test
python tests/test_translations_comprehensive.py
```

## Output

The test provides:

1. **Real-time logging** of each step
2. **Detailed statistics** for each entity type
3. **Specific issues** with actionable recommendations
4. **Cloud translation suggestions** for missing keys
5. **Comprehensive report** saved to file

## Example Output

```text
🔍 ecoNET300 Comprehensive Translation Test
============================================================
Implementing step-by-step translation validation logic...

🔑 STEP 1: Extracting entity keys from constants...
   📊 Found 84 sensor keys
   📊 Found 7 binary sensor keys
   📊 Found 3 number keys

🐍 STEP 2: Converting keys from camelCase to snake_case...
   📊 Converted 84 sensor keys to snake_case
   💡 Example: 'mixerSetTemp2' -> 'mixer_set_temp2'

🌐 STEP 3: Extracting translation keys from files...
   🌐 Found 110 sensor translations
   🌐 Found 45 binary sensor translations
   🌐 Found 0 number translations

🔍 STEP 4: Checking sensor translations...
   ❌ Missing translations: 3
   ⚠️  Extra translations: 29
   📝 Missing: mixer_set_temp, mixer_temp, tz_cwu
```

## Benefits

1. **Automated Validation**: No need to manually check each translation
2. **Cloud Compliance**: Ensures translations match official ecoNET terminology
3. **Comprehensive Coverage**: Checks all aspects of translation consistency
4. **Actionable Reports**: Provides specific recommendations for fixes
5. **Step-by-Step Logic**: Easy to understand and debug

## Integration with Development Workflow

This test should be run:

- Before committing translation changes
- When adding new entities
- During integration testing
- As part of CI/CD pipeline

## Files Checked

- `custom_components/econet300/const.py` - Entity constants
- `custom_components/econet300/strings.json` - Base English strings
- `custom_components/econet300/translations/en.json` - English translations
- `custom_components/econet300/translations/pl.json` - Polish translations
- `custom_components/econet300/icons.json` - Entity icons
- `docs/cloud_translations/MANUAL_TRANSLATION_REFERENCE.md` - Cloud reference

## Next Steps

After running this test, developers should:

1. **Add missing translations** using cloud reference suggestions
2. **Fix entity type mismatches** by moving keys to correct sections
3. **Add missing icons** for entities without visual representation
4. **Ensure consistency** across all translation files
5. **Re-run the test** to verify all issues are resolved
