# ecoNET Cloud Translations Reference

## Overview
This directory contains official translations extracted from ecoNET cloud JavaScript files. These translations provide standardized parameter names and descriptions across multiple languages for Home Assistant integration.

## File Structure

### Main Files
- **`TRANSLATIONS_REFERENCE.md`** - This file (main documentation)
- **`translations_en.json`** - English translations (1105 parameters)
- **`translations_pl.json`** - Polish translations (1101 parameters)
- **`translations_fr.json`** - French translations (872 parameters)

### Legacy Files (Kept for Reference)
- `raw_translations.json` - Original raw data
- `all_languages_translations.json` - Complete multi-language dataset
- `robust_translations.json` - Enhanced translations with additional context

## Available Languages
The ecoNET system supports the following languages with current clean translations:

### ✅ Clean Translation Files Available
- **en** - English (1105 parameters) - Complete coverage
- **pl** - Polish (1101 parameters) - Complete coverage
- **fr** - French (872 parameters) - Partial coverage

### 🌐 Other Supported Languages (Legacy)
- **cz** - Czech
- **ru** - Russian
- **hr** - Croatian
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
- `tempFeeder` → `temp_feeder` - Feeder temperature
- `tempFlueGas` → `temp_flue_gas` - Flue gas temperature
- `tempExternalSensor` → `temp_external_sensor` - External sensor temperature
- `tempBack` → `temp_back` - Return temperature
- `tempUpperBuffer` → `temp_upper_buffer` - Upper buffer temperature
- `tempLowerBuffer` → `temp_lower_buffer` - Lower buffer temperature
- `tempUpperSolar` → `temp_upper_solar` - Upper solar temperature
- `tempLowerSolar` → `temp_lower_solar` - Lower solar temperature
- `tempFireplace` → `temp_fireplace` - Fireplace temperature

### Status Sensors
- `lambdaLevel` → `lambda_level` - Lambda sensor level
- `mode` → `mode` - Operating mode
- `status` → `status` - System status
- `fuelLevel` → `fuel_level` - Fuel level
- `fuelStream` → `fuel_stream` - Fuel stream

### Control Parameters
- `boilerPower` → `boiler_power` - Boiler power
- `fanPower` → `fan_power` - Fan power
- `fanPowerExhaust` → `fan_power_exhaust` - Exhaust fan power
- `refreshRate` → `refresh_rate` - Refresh rate
- `totalGain` → `total_gain` - Total thermal efficiency

### System Parameters
- `savingSchedule` → `saving_schedule` - Saving schedule
- `scheduleSaved` → `schedule_saved` - Schedule saved
- `softwareVersion` → `software_version` - Software version
- `moduleVersion` → `module_version` - Module version
- `panelsConf` → `panels_conf` - Panels configuration

## Best Practices

1. **Always check cloud translations first** before creating new ones
2. **Use official terminology** from ecoNET when available
3. **Maintain consistency** across all translation files
4. **Test translations** after making changes
5. **Follow established naming patterns** for new entities
6. **Prefer complete language coverage** (EN/PL) over partial (FR)

## Example Implementation

### Adding a New Boiler Temperature Sensor

1. **Check cloud reference**: Find `tempCO` → "Boiler temperature" / "Temperatura kotła"
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

### Adding a New Lambda Sensor

1. **Check cloud reference**: Find `lambdaLevel` → "Lambda sensor O2" / "Sonda Lambda O2"
2. **Create constant**: `SENSOR_LAMBDA_LEVEL = "lambdaLevel"`
3. **Update translations**:
   ```json
   // strings.json
   "lambda_level": { "name": "Lambda Sensor O2" }

   // en.json
   "lambda_level": { "name": "Lambda Sensor O2" }

   // pl.json
   "lambda_level": { "name": "Sonda Lambda O2" }
   ```

## Data Source
All translations are extracted from official ecoNET cloud JavaScript files, ensuring accuracy and consistency with the manufacturer's terminology.

## Maintenance
- Translations are automatically extracted from cloud sources
- New parameters are added as they become available
- Language coverage varies by parameter availability
- Regular updates ensure compatibility with latest ecoNET firmware
- Clean translation files are prioritized for Home Assistant integration
- Legacy files maintained for reference and development purposes

## File Locations
- **Primary Reference**: `docs/cloud_translations/clean_translations/TRANSLATIONS_REFERENCE.md`
- **English Translations**: `docs/cloud_translations/clean_translations/translations_en.json`
- **Polish Translations**: `docs/cloud_translations/clean_translations/translations_pl.json`
- **French Translations**: `docs/cloud_translations/clean_translations/translations_fr.json`
- **Available Languages**: `docs/cloud_translations/available_languages.txt`
