# ecoNET Cloud Translations Reference

## Overview
This directory contains official translations extracted from ecoNET cloud JavaScript files. These translations provide standardized parameter names and descriptions across multiple languages for Home Assistant integration.

## File Structure

### Main Files
- **`TRANSLATIONS_REFERENCE.md`** - This file (main documentation)
- **`translations_en.json`** - English translations
- **`translations_pl.json`** - Polish translations
- **`translations_fr.json`** - French translations

### Legacy Files (Kept for Reference)
- `raw_translations.json` - Original raw data
- `all_languages_translations.json` - Complete multi-language dataset
- `robust_translations.json` - Enhanced translations with additional context

## Available Languages
The ecoNET system supports the following languages:
- **en** - English (1105 parameters)
- **cz** - Czech (1030 parameters)
- **ru** - Russian (976 parameters)
- **hr** - Croatian (477 parameters)
- **pl** - Polish
- **fr** - French
- **lv** - Latvian
- **es** - Spanish
- **bg** - Bulgarian
- **hu** - Hungarian
- **it** - Italian
- **ro** - Romanian
- **tr** - Turkish
- **uk** - Ukrainian

## Usage in Home Assistant

### Translation Key Format
- Use `camel_to_snake` format for entity keys
- Example: `tempCO` → `temp_co`
- Keys must match exactly across all translation files

### Required Files to Update
1. **`custom_components/econet300/strings.json`** - Base English strings
2. **`custom_components/econet300/translations/en.json`** - English translations
3. **`custom_components/econet300/translations/pl.json`** - Polish translations

### Translation Structure Example
```json
{
  "entity": {
    "sensor": {
      "temp_co": {
        "name": "Boiler Temperature"
      }
    }
  }
}
```

## Common Translation Patterns

### Temperature Sensors
- `tempCO` → `temp_co` - Boiler temperature
- `tempCWU` → `temp_cwu` - Hot water temperature
- `tempOpticalSensor` → `temp_optical_sensor` - Flame temperature

### Status Sensors
- `lambdaLevel` → `lambda_level` - Lambda sensor level
- `mode` → `mode` - Operating mode
- `status` → `status` - System status

### Control Parameters
- `boilerPower` → `boiler_power` - Boiler power
- `fanPower` → `fan_power` - Fan power
- `refreshRate` → `refresh_rate` - Refresh rate

## Best Practices

1. **Always check cloud translations first** before creating new ones
2. **Use official terminology** from ecoNET when available
3. **Maintain consistency** across all translation files
4. **Test translations** after making changes
5. **Follow established naming patterns** for new entities

## Example Implementation

### Adding a New Boiler Temperature Sensor

1. **Check cloud reference**: Find `tempCO` → "Boiler temperature"
2. **Create constant**: `SENSOR_TEMP_CO = "tempCO"`
3. **Update translations**:
   ```json
   // strings.json
   "temp_co": { "name": "Boiler Temperature" }

   // en.json
   "temp_co": { "name": "Boiler Temperature" }

   // pl.json
   "temp_co": { "name": "Temperatura kotła" }
   ```

## Data Source
All translations are extracted from official ecoNET cloud JavaScript files, ensuring accuracy and consistency with the manufacturer's terminology.

## Maintenance
- Translations are automatically extracted from cloud sources
- New parameters are added as they become available
- Language coverage varies by parameter availability
- Regular updates ensure compatibility with latest ecoNET firmware
