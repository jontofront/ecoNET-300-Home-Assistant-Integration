# dev_set1.js Analysis - Controller Class and API Endpoints

## Overview

The `dev_set1.js` file from the econet24.com cloud service contains the **Controller class** that handles all API communications with ecoNET-300 devices. This file is crucial for understanding the complete API structure and available endpoints.

**Source**: https://www.econet24.com/static/ui/dev_set1.js?332fd073

## Key Components

### 1. Controller Class Structure

```javascript
function Controller(destination, ecosrv_address) {
    this.only_device = false;
    this.destination_ = destination;
    this.ecosrvAddress_ = ecosrv_address;
    this.protocol_type = '';
    this.type_ = 0;
}
```

**Properties**:
- `destination_` - Base URL for API endpoints
- `ecosrvAddress_` - ecoNET server address
- `protocol_type` - Device protocol (em, gm3, etc.)
- `type_` - Device type (0=ECOMAX_850P_TYPE, 1=ECOMAX_850i_TYPE)

### 2. API Endpoint Categories

#### A. Remote Menu Data Retrieval

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| `getRemoteMenuLangs()` | `rmLangs` | Get available languages | `uid` |
| `getCurrentParamsEdits()` | `rmCurrentDataParamsEdits` | Get editable current parameters | `uid` |
| `getRemoteMenuParamsNames()` | `rmParamsNames` | Get parameter names | `uid`, `lang` |
| `getRemoteMenuCatsNames()` | `rmCatsNames` | Get category names | `uid`, `lang` |
| `getRemoteMenuParamsUnitsNames()` | `rmParamsUnitsNames` | Get parameter units | `uid`, `lang` |
| `getRemoteMenuParamsEnums()` | `rmParamsEnums` | Get parameter enumerations | `uid`, `lang` |
| `getRemoteMenuLocksNames()` | `rmLocksNames` | Get lock names | `uid`, `lang` |
| `getRemoteMenuStructure()` | `rmStructure` | Get menu structure | `uid`, `lang` |
| `getRemoteMenuCurrDataDisp()` | `rmCurrentDataParams` | Get current data display | `uid`, `lang` |
| `getRemoteMenuParamsData()` | `rmParamsData` | Get parameter data | `uid` |
| `getRemoteMenuExistingLangsList()` | `rmExistingLangs` | Get existing languages list | `uid` |
| `getRemoteMenuAlarmsNames()` | `rmAlarmsNames` | Get alarm names | `uid`, `lang` |
| `getRemoteMenuParamsDescs()` | `rmParamsDescs` | Get parameter descriptions | `uid`, `lang` |
| `getRemoteMenuCatsDescs()` | `rmCatsDescs` | Get category descriptions | `uid`, `lang` |

#### B. Authentication and Security

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| `getPassword()` | `call/run/getServicePassword` | Get service password | `uid` |
| `getETPassword()` | `getETservicePasswords` | Get ET service passwords | `uid` |
| `rmCheckAccess()` | `rmAccess` | Check remote access | `uid`, `password` |

#### C. Parameter Updates

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| `saveParam()` | `newParam` | Save parameter by name | `uid`, `newParamName`, `newParamValue` |
| `rmSaveParam()` | `rmNewParam` | Save remote parameter by index | `uid`, `newParamIndex`, `newParamValue` |
| `rmSaveCurrParam()` | `rmCurrNewParam` | Save current parameter by key | `uid`, `newParamKey`, `newParamValue` |

#### D. Language and Settings

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| `rmSaveLang()` | `rmSaveLang` | Save language setting | `uid`, `lang` |

#### E. Software Updates

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| `updateSoftware()` | `updateEconet` | Update device software | `uid` |

#### F. Device Management

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| `getDevices()` | `devices` | Get device list | Multiple filters |
| `setDeviceSettings()` | `setDeviceSettings` | Set device settings | `uid`, `label`, `serviceAccess`, `alarmNotifications` |
| `setDeviceAddressSettings()` | `setDeviceAddressSettings` | Set device address | `uid`, address fields |
| `updateKey()` | `updateKey` | Update device key | `key`, `uid` |

## URL Structure Analysis

### Local Device URLs
For local device communication, the URLs follow this pattern:
```
http://DEVICE_IP/econet/{endpoint}
```

### Cloud Service URLs
For cloud service communication, the URLs follow this pattern:
```
https://www.econet24.com/api/{endpoint}?uid={device_uid}&{parameters}
```

## Key Insights for Home Assistant Integration

### 1. Parameter Update Methods

The file reveals three different ways to update parameters:

1. **`saveParam()`** - Updates by parameter name (for local devices)
2. **`rmSaveParam()`** - Updates by parameter index (for remote devices)
3. **`rmSaveCurrParam()`** - Updates by parameter key (for current data)

### 2. Authentication Requirements

- **Local devices**: Most endpoints work without authentication
- **Remote devices**: Require `uid` parameter and sometimes password
- **Service parameters**: Require service password authentication

### 3. Language Support

The system supports multiple languages with dedicated endpoints:
- `rmLangs` - Available languages
- `rmExistingLangs` - Existing language list
- `rmSaveLang` - Save language preference

### 4. Device Types

```javascript
var ECOMAX_850P_TYPE = 0;
var ECOMAX_850i_TYPE = 1;
```

This suggests the system supports different ecoMAX variants.

## Implementation Strategy for Home Assistant

### 1. Local Device Integration

For your ecoMAX810P-L TOUCH device, use these endpoints:

```python
# Base URL
BASE_URL = "http://YOUR_DEVICE_IP/econet"

# Key endpoints
ENDPOINTS = {
    "system_params": "/sysParams",
    "current_data": "/rmCurrentDataParams",
    "editable_params": "/rmCurrentDataParamsEdits",
    "parameter_names": "/rmParamsNames",
    "parameter_enums": "/rmParamsEnums",
    "parameter_descs": "/rmParamsDescs",
    "category_names": "/rmCatsNames",
    "alarm_names": "/rmAlarmsNames",
    "menu_structure": "/rmStructure"
}
```

### 2. Parameter Update Strategy

```python
# For local devices, use parameter names
def update_parameter(parameter_name, value):
    url = f"{BASE_URL}/newParam"
    params = {
        "newParamName": parameter_name,
        "newParamValue": value
    }
    # Make GET request
```

### 3. Error Handling

The file includes a `logError()` function that logs:
- HTTP status
- Error message
- Full response object

### 4. Caching Strategy

All AJAX calls use `cache: false`, indicating the system expects fresh data on each request.

## Comparison with Our Previous Testing

### ✅ Confirmed Endpoints
Our previous testing confirmed these endpoints work on your device:
- `sysParams` ✅
- `rmCurrentDataParams` ✅
- `rmCurrentDataParamsEdits` ✅
- `rmParamsNames` ✅
- `rmAlarmsNames` ✅

### 🔍 New Endpoints to Test
Based on `dev_set1.js`, we should also test:
- `rmParamsEnums` - Parameter enumerations
- `rmParamsDescs` - Parameter descriptions
- `rmCatsNames` - Category names
- `rmStructure` - Menu structure
- `rmParamsUnitsNames` - Parameter units
- `rmLocksNames` - Lock names

## Next Steps

1. **Test Additional Endpoints**: Try the new endpoints we discovered
2. **Implement Controller Pattern**: Use the Controller class structure for our integration
3. **Add Authentication Support**: Implement password-based authentication for protected endpoints
4. **Add Language Support**: Implement multi-language support using the language endpoints

## Conclusion

The `dev_set1.js` file provides a complete blueprint for the ecoNET-300 API. It confirms our previous findings and reveals additional capabilities we can implement in the Home Assistant integration. The Controller class pattern is well-structured and provides a solid foundation for building a robust integration. 