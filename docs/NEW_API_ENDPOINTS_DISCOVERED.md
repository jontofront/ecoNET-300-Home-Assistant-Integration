# New API Endpoints Discovered from dev_set*.js Files

## Overview
This document lists all the API endpoints discovered from the ecoNET24 cloud JavaScript files (`dev_set1.js` through `dev_set5.js`) that may not be covered in your existing test fixtures.

## Core Controller API Endpoints

### Device Management
- **`getDevices`** - Get list of devices with filtering options
  - Parameters: `active`, `notactive`, `blocked`, `deviceType`, `uid`, `prodId`, `softVer`, `ver_mod_a`, `ver_panel`
  - Example: `getDevices?active=true&notactive=false&blocked=false&deviceType=&uid=&prodId=&softVer=&ver_mod_a=&ver_panel=`

- **`getDeviceParams`** - Get device parameters by UID
  - Parameters: `uid`
  - Example: `getDeviceParams?uid={device_uid}`

- **`getDeviceRegParams`** - Get device regulator parameters by UID
  - Parameters: `uid`
  - Example: `getDeviceRegParams?uid={device_uid}`

- **`getCurrentState`** - Get current system state
  - Example: `getCurrentState`

### Remote Menu (RM) API Endpoints
These endpoints provide access to remote menu functionality and are prefixed with `rm`:

- **`rmLangs`** - Get remote menu available languages
  - Parameters: `uid` (optional)
  - Example: `rmLangs?uid={device_uid}` or `rmLangs`

- **`rmCurrentDataParams`** - Get current data parameters for remote menu
  - Parameters: `uid`, `lang` (optional)
  - Example: `rmCurrentDataParams?uid={device_uid}&lang={language}`

- **`rmCurrentDataParamsEdits`** - Get current data parameters edits
  - Parameters: `uid` (optional)
  - Example: `rmCurrentDataParamsEdits?uid={device_uid}` or `rmCurrentDataParamsEdits`

- **`rmParamsNames`** - Get parameter names for remote menu
  - Parameters: `uid`, `lang`
  - Example: `rmParamsNames?uid={device_uid}&lang={language}`

- **`rmCatsNames`** - Get category names for remote menu
  - Parameters: `uid`, `lang`
  - Example: `rmCatsNames?uid={device_uid}&lang={language}`

- **`rmParamsUnitsNames`** - Get parameter unit names
  - Parameters: `uid`, `lang`
  - Example: `rmParamsUnitsNames?uid={device_uid}&lang={language}`

- **`rmParamsEnums`** - Get parameter enumeration values
  - Parameters: `uid`, `lang`
  - Example: `rmParamsEnums?uid={device_uid}&lang={language}`

- **`rmLocksNames`** - Get lock names for remote menu
  - Parameters: `uid`, `lang`
  - Example: `rmLocksNames?uid={device_uid}&lang={language}`

- **`rmStructure`** - Get remote menu structure
  - Parameters: `uid`, `lang`
  - Example: `rmStructure?uid={device_uid}&lang={language}`

- **`rmParamsData`** - Get parameter data for remote menu
  - Parameters: `uid`
  - Example: `rmParamsData?uid={device_uid}`

- **`rmExistingLangs`** - Get existing languages list for remote menu
  - Parameters: `uid` (optional)
  - Example: `rmExistingLangs?uid={device_uid}` or `rmExistingLangs`

- **`rmAlarmsNames`** - Get alarm names for remote menu
  - Parameters: `uid`, `lang`
  - Example: `rmAlarmsNames?uid={device_uid}&lang={language}`

- **`rmParamsDescs`** - Get parameter descriptions
  - Parameters: `uid`, `lang`
  - Example: `rmParamsDescs?uid={device_uid}&lang={language}`

- **`rmCatsDescs`** - Get category descriptions
  - Parameters: `uid`, `lang`
  - Example: `rmCatsDescs?uid={device_uid}&lang={language}`

### Parameter Management
- **`newParam`** - Save new parameter value
  - Parameters: `newParamName`, `newParamValue`, `uid` (optional)
  - Example: `newParam?newParamName={name}&newParamValue={value}` or `newParam?uid={device_uid}&newParamName={name}&newParamValue={value}`

- **`rmNewParam`** - Save new remote menu parameter
  - Parameters: `newParamIndex`, `newParamValue`, `uid` (optional)
  - Example: `rmNewParam?newParamIndex={index}&newParamValue={value}` or `rmNewParam?uid={device_uid}&newParamIndex={index}&newParamValue={value}`

- **`rmCurrNewParam`** - Save current remote menu parameter
  - Parameters: `newParamKey`, `newParamValue`, `uid` (optional)
  - Example: `rmCurrNewParam?newParamKey={key}&newParamValue={value}` or `rmCurrNewParam?uid={device_uid}&newParamKey={key}&newParamValue={value}`

### Access Control
- **`password`** - Get service password
  - Parameters: `uid` (optional)
  - Example: `password` or `call/run/getServicePassword?uid={device_uid}`

- **`etpassword`** - Get ET service passwords
  - Parameters: `uid` (optional)
  - Example: `etpassword` or `getETservicePasswords?uid={device_uid}`

- **`rmAccess`** - Check remote menu access
  - Parameters: `password`, `uid` (optional)
  - Example: `rmAccess?password={password}` or `rmAccess?uid={device_uid}&password={password}`

- **`rmSaveLang`** - Save remote menu language
  - Parameters: `uid` (optional)
  - Example: `rmSaveLang?uid={device_uid}` or `rmSaveLang`

### Scheduling System
- **`setSchedule`** - Set device schedule
  - Parameters: `uid` (optional)
  - Example: `setSchedule?uid={device_uid}` or `setSchedule`

- **`saveSchedules`** - Save ecoMAX schedules
  - Parameters: `uid` (optional)
  - Example: `saveSchedules?uid={device_uid}` or `saveSchedules`

- **`getSchedule`** - Get device schedule
  - Parameters: `uid` (optional)
  - Example: `getSchedule?uid={device_uid}` or `getSchedule`

- **`saveVentSchedules`** - Save ventilation schedules
  - Parameters: `uid`, `data`, `param`, `value`
  - Example: `saveVentSchedules?uid={device_uid}&data={data}&param={param}&value={value}`

### Software and Updates
- **`updateSoftware`** - Update device software
  - Parameters: `uid` (optional)
  - Example: `updateSoftware` or `updateEconet?uid={device_uid}`

- **`checkSoftwareUpdate`** - Check for software updates
  - Parameters: `protocol`, `uid` (optional)
  - Example: `checkSoftwareUpdate?protocol={protocol}&uid={device_uid}`

### ecoMAX-Specific Endpoints

#### Fuel Consumption
- **`getFuelConsumption`** - Get fuel consumption data
  - Parameters: `uid`, `fromDate`, `toDate`
  - Example: `getFuelConsumption?uid={device_uid}&fromDate={from_date}&toDate={to_date}`

#### History and Data
- **`getHistoryParamsValues`** - Get historical parameter values
  - Parameters: `uid`, `fromDate`, `toDate`
  - Example: `getHistoryParamsValues?uid={device_uid}&fromDate={from_date}&toDate={to_date}`

### Service Endpoints
- **`deleteDeviceAlarms`** - Delete device alarms (POST)
  - Parameters: `uid` (in POST data)
  - Headers: `X-CSRFToken`
  - Example: `POST /service/deleteDeviceAlarms`

- **`getETtranslations`** - Get ET translations (POST)
  - Parameters: `ver`, `client`, `lang`, `regName`
  - Headers: `Accept: json`, `Content-Type: application/x-www-form-urlencoded`
  - Example: `POST /service/getETtranslations/`

### Additional Endpoints
- **`saveAlertDateUser`** - Save alert date for user
  - Parameters: `userDate`
  - Example: `saveAlertDateUser?userDate={date}`

- **`getAlertsDates`** - Get alerts dates
  - Example: `getAlertsDates`

- **`deviceTypes`** - Get available device types
  - Example: `deviceTypes`

- **`uids`** - Get available UIDs
  - Example: `uids`

## ecoMAX360-Specific Features

### Advanced Scheduling
The ecoMAX360i supports advanced scheduling with multiple time zones:
- **Thermostat time zones**: `thermostat1TZ`, `thermostat2TZ`, `thermostat3TZ`
- **Mixer circuit time zones**: `mixer1TZ` through `mixer10TZ`
- **Heating circuit time zones**: `circuit1TZ` through `circuit7TZ`

### Fuel Consumption Tracking
- Historical fuel consumption data with hourly/daily granularity
- Chart visualization with configurable time ranges
- Data export capabilities

### Enhanced Parameter Management
- Support for up to 8 room temperature sensors (`ecoSterTemp1` through `ecoSterTemp8`)
- Support for up to 8 mixer circuits (`mixerTemp1` through `mixerTemp8`)
- Lambda sensor monitoring with special precision handling

## Missing Test Fixtures

Based on the discovered endpoints, you may need to create test fixtures for:

1. **Remote Menu endpoints** (all `rm*` endpoints)
2. **Fuel consumption data** (`getFuelConsumption`)
3. **Historical data** (`getHistoryParamsValues`)
4. **Scheduling data** (`getSchedule`, `setSchedule`)
5. **Device management** (`getDevices`, `getDeviceParams`)
6. **Access control** (`password`, `etpassword`, `rmAccess`)
7. **Software updates** (`checkSoftwareUpdate`, `updateSoftware`)

## Next Steps

1. **Create test fixtures** for the missing endpoints
2. **Test ecoMAX360-specific features** like fuel consumption and advanced scheduling
3. **Implement remote menu support** in your integration
4. **Add fuel consumption monitoring** for ecoMAX devices
5. **Support advanced scheduling** for temperature control systems

## Source Files
- `dev_set1.js` - Core controller and API endpoints
- `dev_set2.js` - Schema and parameter management
- `dev_set3.js` - Remote menu and parameter handling
- `dev_set4.js` - Scheduling and fuel consumption
- `dev_set5.js` - Device-specific features and updates
