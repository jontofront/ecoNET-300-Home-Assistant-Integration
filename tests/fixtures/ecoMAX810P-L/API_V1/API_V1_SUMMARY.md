# ecoNET-300 API V1 Translation Resources

## Overview
This directory contains translation resources and sample data extracted from the **API V1** (classic ecoNET API) JavaScript files. These resources are used for development, testing, and maintaining consistency with the official ecoNET24 web interface.

## Files Description

### 📄 **econet_transp1_translations.json**
- **Source**: `econet_transp1.js` from ecoNET24 web interface
- **Content**: Comprehensive UI translations including:
  - Schedule management
  - User management
  - Network settings
  - Device control
  - Temperature settings
  - System messages
  - Password management
  - Software updates
  - Device types
  - User interface elements
  - Registration forms
  - Device management
  - Thermostat names
  - System states
  - History and data
  - Search and filtering
  - Configuration
  - Access control
  - Remote menu
  - Special features
- **Use Case**: Reference for UI consistency, error handling, and parameter mapping

### 📄 **translation_resources_lt_en_pl.json**
- **Source**: `econet_transt.js` from ecoNET24 web interface
- **Content**: Focused translations for Lithuanian (LT), English (EN), and Polish (PL):
  - Language names
  - Country mappings
  - UI translations
  - Device-specific translations
  - Translation functions documentation
- **Use Case**: Localization support for Home Assistant integration

### 📄 **static_ecomax_en_sample.json**
- **Source**: Sample translation file structure for API V2
- **Content**: English translation structure with:
  - Parameter metadata
  - UI elements
  - Categories and groups
  - Value mappings
  - Help text
- **Use Case**: Reference for translation structure and parameter organization

### 📄 **static_ecomax_pl_sample.json**
- **Source**: Sample translation file structure for API V2
- **Content**: Polish translation structure (same as English but with Polish translations)
- **Use Case**: Reference for Polish localization and parameter organization

### 📄 **sysParams.json**
- **Source**: ecoNET-300 API V1 system parameters
- **Content**: System configuration parameters including:
  - Device identification
  - Network settings
  - System configuration
  - Hardware parameters
  - Firmware information
- **Use Case**: Reference for system configuration and device identification

### 📄 **rmParamsData.json**
- **Source**: ecoNET-300 API V1 remote module parameters
- **Content**: Comprehensive parameter data including:
  - Parameter definitions
  - Value ranges
  - Units
  - Access permissions
  - Default values
- **Use Case**: Reference for parameter mapping and validation

### 📄 **rmParamsEnums.json**
- **Source**: ecoNET-300 API V1 parameter enumerations
- **Content**: Enumeration values for parameters including:
  - Status codes
  - Mode values
  - Error codes
  - State definitions
- **Use Case**: Reference for parameter value interpretation

### 📄 **rmParamsNames.json**
- **Source**: ecoNET-300 API V1 parameter names
- **Content**: Human-readable parameter names and descriptions
- **Use Case**: Reference for UI labels and parameter identification

### 📄 **rmStructure.json**
- **Source**: ecoNET-300 API V1 remote module structure
- **Content**: Parameter hierarchy and organization including:
  - Parameter groups
  - Categories
  - Relationships
  - Access paths
- **Use Case**: Reference for parameter organization and navigation

### 📄 **rmCurrentDataParams.json**
- **Source**: ecoNET-300 API V1 current data parameters
- **Content**: Real-time data parameters including:
  - Temperature readings
  - Status values
  - Current states
  - Live measurements
- **Use Case**: Reference for real-time data collection

### 📄 **rmCurrentDataParamsEdits.json**
- **Source**: ecoNET-300 API V1 editable current data parameters
- **Content**: Parameters that can be modified in real-time
- **Use Case**: Reference for writable parameters and controls

### 📄 **rmCurrentDataParams_v2.json**
- **Source**: ecoNET-300 API V1 current data parameters (version 2)
- **Content**: Updated real-time data parameters
- **Use Case**: Reference for newer parameter definitions

### 📄 **regParams.json**
- **Source**: ecoNET-300 API V1 register parameters
- **Content**: Register-based parameter definitions
- **Use Case**: Reference for register mapping and communication

### 📄 **regParamsData.json**
- **Source**: ecoNET-300 API V1 register parameter data
- **Content**: Detailed register parameter information
- **Use Case**: Reference for register-level parameter handling

### 📄 **rmAlarmsNames.json**
- **Source**: ecoNET-300 API V1 alarm names
- **Content**: Alarm code definitions and descriptions
- **Use Case**: Reference for alarm handling and user notifications

## Usage in Home Assistant Integration

### 1. **UI Consistency**
Use these translations to maintain consistency with the official ecoNET24 web interface:
```python
# Example: Load translations for UI elements
with open("tests/fixtures/ecoMAX810P-L/API_V1/econet_transp1_translations.json") as f:
    translations = json.load(f)
    ui_text = translations["translations"]["en"]["user_interface"]["save"]
```

### 2. **Error Handling**
Reference system messages for proper error handling:
```python
# Example: Use error messages from translations
error_msg = translations["translations"]["en"]["system_messages"]["save_error"]
```

### 3. **Parameter Mapping**
Map device parameters to user-friendly names:
```python
# Example: Map thermostat names
thermostat_names = translations["translations"]["en"]["thermostat_names"]
entity_name = thermostat_names.get("thermostat1TZ", "Thermostat 1")
```

### 4. **Localization**
Support multiple languages in your integration:
```python
# Example: Get localized country names
with open("tests/fixtures/ecoMAX810P-L/API_V1/translation_resources_lt_en_pl.json") as f:
    resources = json.load(f)
    country_name = resources["countries"]["pl"]["PL"]  # "Polska"
```

### 5. **Parameter Mapping**
Use parameter files for device configuration:
```python
# Example: Load parameter definitions
with open("tests/fixtures/ecoMAX810P-L/API_V1/rmParamsData.json") as f:
    params = json.load(f)
    param_info = params.get("param_id")
    min_val = param_info["min"]
    max_val = param_info["max"]
    unit = param_info["unit"]
```

### 6. **Alarm Handling**
Reference alarm codes for proper error handling:
```python
# Example: Get alarm descriptions
with open("tests/fixtures/ecoMAX810P-L/API_V1/rmAlarmsNames.json") as f:
    alarms = json.load(f)
    alarm_desc = alarms.get("alarm_code", "Unknown alarm")
```

### 7. **System Configuration**
Use system parameters for device identification:
```python
# Example: Get device information
with open("tests/fixtures/ecoMAX810P-L/API_V1/sysParams.json") as f:
    sys_params = json.load(f)
    device_name = sys_params.get("device_name", "Unknown")
    firmware_version = sys_params.get("firmware_version", "Unknown")
```

## API V1 vs V2

| Aspect | API V1 | API V2 |
|--------|--------|--------|
| **Authentication** | Simple API key | Session-based |
| **Translations** | Basic | Rich metadata |
| **Real-time Data** | Polling only | WebSocket support |
| **Batch Operations** | No | Yes |
| **Historical Data** | Limited | Full access |
| **Scheduling** | Basic | Advanced |

## Best Practices

1. **Keep API V1 files here** for reference and development
2. **Use translations for UI consistency** with official interface
3. **Reference error messages** for proper error handling
4. **Map parameter names** to user-friendly labels
5. **Support localization** using the language resources

## References

- **Source Files**:
  - [econet_transp1.js](https://www.econet24.com/static/ui/econet_transp1.js?ae7cdce1)
  - [econet_transt.js](https://www.econet24.com/static/ui/econet_transt.js?8c71c880)
- **Home Assistant**: [Internationalization](https://developers.home-assistant.io/docs/internationalization/core/)
- **Home Assistant**: [Custom Integration Structure](https://developers.home-assistant.io/docs/creating_component_structure/)

---

**Note**: These files are for development and reference purposes. The actual Home Assistant integration should use the translation files in `custom_components/econet300/translations/` for runtime localization. 