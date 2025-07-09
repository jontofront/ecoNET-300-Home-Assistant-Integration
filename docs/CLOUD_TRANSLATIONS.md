# ecoNET Cloud Translations Documentation

## Overview
This document tracks translation files found in the ecoNET cloud (econet24.com) system. These translations provide valuable reference for improving our local integration's translation accuracy and completeness.

## Cloud Translation Sources
- **Platform**: econet24.com (ecoNET cloud service)
- **Purpose**: Official translations used by the cloud-based ecoNET system
- **Value**: Reference for accurate entity names, descriptions, and multi-language support

## Translation Files Found

### File Structure
```
econet24.com/static/ui/
├── econet_basicset.js    # Basic language setup and functions
├── econet_transt.js      # Main translation system (19 languages)
├── econet_transp1.js     # Translation part 1
├── econet_transp2.js     # Translation part 2
├── econet_transp3.js     # Translation part 3
└── econet_transp4.js     # Translation part 4
```

### Supported Languages
The ecoNET24 system supports **19 languages**:
- **Primary**: `pl` (Polish), `en` (English), `lt` (Lithuanian)
- **Additional**: `de`, `fr`, `uk`, `da`, `cz`, `it`, `ro`, `bg`, `tr`, `es`, `hr`, `hu`, `sk`, `sr`, `lv`, `nl`, `ru`

**Focus Languages**: EN, PL, LT (as requested)

### Key Translation Categories
1. **Entity Names** - Sensor, binary sensor, switch, and number entity names
2. **State Descriptions** - Operational states and status messages
3. **Parameter Names** - API parameter descriptions
4. **Error Messages** - System error and warning messages
5. **UI Elements** - Interface labels and descriptions

## Cloud vs Local Translation Comparison

### Advantages of Cloud Translations
- ✅ **Official terminology** - Uses exact terms from ecoNET documentation
- ✅ **Complete coverage** - Includes all available entities and parameters
- ✅ **Multi-language support** - Official translations for multiple languages
- ✅ **Consistent naming** - Standardized across all ecoNET devices
- ✅ **Updated regularly** - Maintained by ecoNET developers

### Local Integration Benefits
- ✅ **Offline operation** - No dependency on cloud services
- ✅ **Privacy** - All data stays local
- ✅ **Customization** - Can adapt translations for Home Assistant context
- ✅ **Community input** - Can incorporate user feedback

## Implementation Strategy

### Phase 1: Documentation
- [ ] Document all cloud translation files
- [ ] Map cloud entities to our local entities
- [ ] Identify missing translations in our integration
- [ ] Note any new entity types we could implement

### Phase 2: Integration
- [ ] Update our translation files with cloud references
- [ ] Add missing entity translations
- [ ] Improve translation accuracy
- [ ] Add support for additional languages

### Phase 3: Enhancement
- [ ] Implement new entities found in cloud translations
- [ ] Add missing parameter descriptions
- [ ] Improve error message translations
- [ ] Standardize naming conventions

## Translation File Structure

### Example Cloud Translation Structure
```json
{
  "entity": {
    "binary_sensor": {
      "lambda_status": {
        "name": "Lambda Sensor Status",
        "description": "Indicates if the lambda sensor is active"
      }
    },
    "sensor": {
      "temp_co": {
        "name": "Central Heating Temperature",
        "description": "Current central heating system temperature"
      }
    }
  },
  "state": {
    "mode": {
      "0": "Off",
      "1": "Fire Up",
      "2": "Operation",
      "3": "Work"
    }
  }
}
```

## Notes and Observations

### Language Support
- **Primary**: English (en), Polish (pl)
- **Secondary**: German (de), other European languages
- **Format**: JSON-based translation files
- **Encoding**: UTF-8

### Entity Coverage
- **Sensors**: Temperature, power, status sensors
- **Binary Sensors**: Pump, fan, valve status
- **Switches**: Control switches and relays
- **Numbers**: Setpoint and configuration values

### Translation Quality
- **Professional**: Official ecoNET translations
- **Consistent**: Standardized terminology
- **Complete**: Covers all device parameters
- **Maintained**: Regularly updated by ecoNET

## Translation Reference

A comprehensive translation reference has been created to help with development:

### Reference Documents
- **Manual Reference**: `docs/cloud_translations/MANUAL_TRANSLATION_REFERENCE.md` - Curated translations for key entities
- **Auto-generated Reference**: `docs/cloud_translations/TRANSLATION_REFERENCE.md` - Complete extracted translations
- **Raw Data**: `docs/cloud_translations/raw_translations.json` - Raw extracted data

### How to Use for Development

When adding new entities to the integration:

1. **Check the manual reference** for the exact translation key
2. **Use the official Polish translation** from the reference
3. **Follow the naming convention** shown in the examples
4. **Update all three translation files** (strings.json, en.json, pl.json)

### Example Usage

For a new temperature sensor:

```python
# Use the key from the reference
SENSOR_TEMP_CO = "tempCO"  # From reference: "Boiler temperature" / "Temperatura kotła"

# Update translation files with the official translations
```

## Next Steps

1. **Use Translation Reference**: Reference the manual guide when adding new entities ✅
2. **Compare with Local**: Identify gaps and improvements needed
3. **Update Integration**: Incorporate cloud translations into our local files
4. **Test and Validate**: Ensure translations work correctly in Home Assistant
5. **Community Review**: Get feedback on translation quality and accuracy

## File Locations

### Cloud Translation Files
- **Source**: econet24.com web interface
- **Access**: Via browser developer tools or API
- **Format**: JSON translation files
- **Languages**: Multiple language support

### Local Integration Files
- **Base**: `custom_components/econet300/strings.json`
- **English**: `custom_components/econet300/translations/en.json`
- **Polish**: `custom_components/econet300/translations/pl.json`
- **Script**: `scripts/check_translations.py`

---

**Last Updated**: [Date]
**Cloud Source**: econet24.com
**Integration Version**: [Current Version] 