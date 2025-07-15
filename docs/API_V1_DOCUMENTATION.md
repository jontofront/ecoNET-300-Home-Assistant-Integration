# ecoNET-300 API V1 Documentation

## Overview

This document provides comprehensive documentation of the ecoNET-300 API V1 endpoints discovered from the econet24.com JavaScript file analysis. These endpoints can be used to interact with ecoNET-300 devices locally.

## Base URL Structure

All API endpoints follow this pattern:
```
http://DEVICE_IP/econet/{endpoint}
```

## Authentication

Most endpoints require basic authentication with username and password.

## Real Device Testing Results

### Device Information
- **Tested Device**: ecoMAX810P-L TOUCH
- **UID**: YOUR_DEVICE_UID
- **Software Version**: 3.2.3879
- **Protocol**: em (ecoMAX)
- **IP Address**: DEVICE_IP
- **Remote Menu**: Enabled ✅
- **Language**: Lithuanian (LT)

### Available Parameters (Confirmed Working)

Based on the `sysParams` response, the following parameters are available:

#### Temperature Sensors
- `tempCO` - Central heating temperature (with setpoint `tempCOSet`)
- `tempCWU` - Hot water temperature (with setpoint `tempCWUSet`)
- `tempExternalSensor` - External temperature sensor (-35°C to 40°C)
- `tempFeeder` - Feeder temperature (0-100°C)
- `tempFlueGas` - Flue gas temperature (0-450°C)
- `mixerTemp1` - Mixer temperature (with setpoint `mixerSetTemp1`)

#### Control Parameters
- `mode` - Boiler operation mode (with CAN_TURN_ON_BOILER capability)
- `boilerPower` - Boiler power output (0-100%)
- `fanPower` - Fan power (0-100%)
- `lambdaLevel` - Lambda sensor level (0-100%)

#### Status Parameters
- `fuelLevel` - Fuel level (0-100%)

### Parameter Index Mapping (Confirmed)

#### Temperature Parameters (1024-1034)
- **1024**: `tempCO` - Central Heating temperature (22.55°C)
- **1025**: `tempCWU` - Hot Water temperature (72.65°C)
- **1028**: Mixer temperature (null)
- **1029**: Mixer temperature (null)
- **1030**: `tempFlueGas` - Flue Gas temperature (20.29°C)
- **1031**: `mixerTemp1` - Mixer 1 temperature (24.52°C)
- **1032-1034**: Other mixer temperatures (null)

#### Setpoint Parameters (1280-1290) - EDITABLE
- **1280**: `tempCOSet` - Central Heating setpoint (41°C, min: 27°C, max: 68°C)
- **1281**: `tempCWUSet` - Hot Water setpoint (20°C)
- **1287**: `mixerSetTemp1` - Mixer 1 setpoint (24°C)
- **1288**: `mixerSetTemp2` - Mixer 2 setpoint (30°C)
- **1289**: `mixerSetTemp3` - Mixer 3 setpoint (25°C)
- **1290**: `mixerSetTemp4` - Mixer 4 setpoint (25°C)

#### Status Parameters (1536-1555)
- **1536-1555**: Various boolean status parameters (pumps, fans, etc.)

#### Control Parameters (1792-2049)
- **1792-1795**: Control values
- **1798**: Unknown control (type 10 - boolean/enum)
- **2048**: Control 1 (0-2 range)
- **2049**: Control 2 (0-2 range)

### Editable Parameters (Confirmed)

#### Parameter 1280 - Central Heating Setpoint
- **Lithuanian Name**: "Katilui užduota temp." (Boiler Set Temperature)
- **Current Value**: 41°C
- **Min**: 27°C
- **Max**: 68°C
- **Type**: 4 (numeric)
- **Parameter Name**: `tempCOSet`

#### Parameter 1798 - Unknown Control
- **Type**: 10 (boolean/enum)
- **No min/max** (likely a switch or enum)

#### Parameter 2048 - Control 1
- **Current Value**: 0
- **Min**: 0
- **Max**: 2
- **Type**: 4 (numeric)
- **Possible values**: 0, 1, 2

#### Parameter 2049 - Control 2
- **Current Value**: 0
- **Min**: 0
- **Max**: 2
- **Type**: 4 (numeric)
- **Possible values**: 0, 1, 2

### Parameter Names (Lithuanian)

Key parameter names from the device:
- **1280**: "Katilui užduota temp." - Boiler Set Temperature
- **1281**: "BVŠ nustatyta temp" - Hot Water Set Temperature
- **1287**: "Maišytuvo 1 nustatyta temperatūra" - Mixer 1 Set Temperature
- **1288**: "Maišytuvo 2 nustatyta temperatūra" - Mixer 2 Set Temperature
- **1289**: "Maišytuvo 3 nustatyta temperatūra" - Mixer 3 Set Temperature
- **1290**: "Maišytuvo 4 nustatyta temperatūra" - Mixer 4 Set Temperature

### Current Device Status (Latest Test)

#### Boiler Status
- **Mode**: 0 (OFF) - Boiler is currently off
- **Boiler Power**: 0% - No power output
- **Status CO**: 0 - Central heating status
- **Status CWU**: 128 - Hot water status

#### Temperature Readings
- **Central Heating**: 22.55°C (setpoint: 41°C)
- **Hot Water**: 72.70°C (setpoint: null)
- **External Sensor**: 16.85°C
- **Feeder**: 21.99°C
- **Flue Gas**: 20.24°C
- **Mixer 1**: 24.52°C (setpoint: 24°C)
- **Mixer 2**: null (setpoint: 30°C)
- **Mixer 3**: null (setpoint: 25°C)
- **Mixer 4**: null (setpoint: 25°C)

#### System Status
- **Fuel Level**: 0% - Empty fuel tank
- **Lambda Level**: 0% - Lambda sensor reading
- **Fan Power**: 0% - Fan is off
- **Thermostat**: 1 - Thermostat status

### Alarm System
The device supports alarm monitoring with the following alarm codes:
- **Alarm Code 0**: Normal operation
- **Alarm Code 7**: System alarm (appears frequently in logs)
- **Alarm Code 2**: Another alarm type

### Module Versions
- **Module A**: 8.30.176.R1
- **Module B**: 1.30.7
- **Module Panel**: 8.11.42
- **Module Lambda**: 3.2.7

## API Endpoints

### 1. System Parameters

#### Get System Parameters
- **Endpoint**: `sysParams`
- **Method**: GET
- **Description**: Retrieves system configuration parameters
- **Response**: JSON object with system information
- **Example**: `GET http://DEVICE_IP/econet/sysParams`

**Response Structure**:
```json
{
  "uid": "YOUR_DEVICE_UID",
  "controllerID": "ecoMAX810P-L TOUCH",
  "softVer": "3.2.3879",
  "routerType": "mr3020-v3",
  "moduleASoftVer": "8.30.176.R1",
  "moduleBSoftVer": "1.30.7",
  "modulePanelSoftVer": "8.11.42",
  "moduleLambdaSoftVer": "3.2.7",
  "protocolType": "em",
  "remoteMenu": true,
  "tiles": [
    {
      "memberName_": "mode",
      "type_": "tile_text",
      "extra_": "CAN_TURN_ON_BOILER"
    },
    {
      "memberName_": "boilerPower",
      "type_": "tile_power"
    },
    {
      "memberName_": "tempCO",
      "setMemberName_": "tempCOSet",
      "type_": "tile_temp"
    }
  ],
  "alarms": [
    {
      "code": 7,
      "fromDate": "2024-12-14 11:51:46",
      "toDate": "2024-12-14 11:51:57",
      "service": false
    }
  ]
}
```

### 2. Regular Parameters

#### Get Current Parameters
- **Endpoint**: `regParams`
- **Method**: GET
- **Description**: Retrieves current device state and parameters
- **Response**: JSON object with current values
- **Example**: `GET http://DEVICE_IP/econet/regParams`

**Expected Response Structure**:
```json
{
  "curr": {
    "mode": 3,
    "boilerPower": 50,
    "tempCO": 65.5,
    "tempCOSet": 75.0,
    "tempCWU": 45.2,
    "tempCWUSet": 55.0,
    "tempExternalSensor": 15.0,
    "fanPower": 75,
    "lambdaLevel": 85,
    "fuelLevel": 80,
    "tempFeeder": 25.0,
    "tempFlueGas": 120.5,
    "mixerTemp1": 45.0,
    "mixerSetTemp1": 50.0
  }
}
```

#### Get Parameter Definitions
- **Endpoint**: `regParamsData`
- **Method**: GET
- **Description**: Retrieves parameter definitions and metadata
- **Response**: JSON object with parameter information
- **Example**: `GET http://DEVICE_IP/econet/regParamsData`

### 3. Remote Menu Parameters (Advanced)

#### Get Current Data Parameters
- **Endpoint**: `rmCurrentDataParams`
- **Method**: GET
- **Description**: Retrieves current data parameters with language support
- **Parameters**: 
  - `uid` (optional): Device UID
  - `lang` (optional): Language code
- **Example**: `GET http://DEVICE_IP/econet/rmCurrentDataParams?uid=YOUR_DEVICE_UID&lang=en`

#### Get Current Data Parameters Edits
- **Endpoint**: `rmCurrentDataParamsEdits`
- **Method**: GET
- **Description**: Retrieves editable current data parameters with limits
- **Parameters**: 
  - `uid` (optional): Device UID
- **Example**: `GET http://DEVICE_IP/econet/rmCurrentDataParamsEdits?uid=YOUR_DEVICE_UID`

#### Get Parameter Names
- **Endpoint**: `rmParamsNames`
- **Method**: GET
- **Description**: Retrieves parameter names in specified language
- **Parameters**: 
  - `uid` (optional): Device UID
  - `lang` (optional): Language code
- **Example**: `GET http://DEVICE_IP/econet/rmParamsNames?uid=YOUR_DEVICE_UID&lang=en`

#### Get Parameter Enums
- **Endpoint**: `rmParamsEnums`
- **Method**: GET
- **Description**: Retrieves parameter enumeration values
- **Parameters**: 
  - `uid` (optional): Device UID
  - `lang` (optional): Language code
- **Example**: `GET http://DEVICE_IP/econet/rmParamsEnums?uid=YOUR_DEVICE_UID&lang=en`

#### Get Parameter Descriptions
- **Endpoint**: `rmParamsDescs`
- **Method**: GET
- **Description**: Retrieves parameter descriptions
- **Parameters**: 
  - `uid` (optional): Device UID
  - `lang` (optional): Language code
- **Example**: `GET http://DEVICE_IP/econet/rmParamsDescs?uid=YOUR_DEVICE_UID&lang=en`

#### Get Menu Structure
- **Endpoint**: `rmStructure`
- **Method**: GET
- **Description**: Retrieves menu structure and parameter organization
- **Parameters**: 
  - `uid` (optional): Device UID
  - `lang` (optional): Language code
- **Example**: `GET http://DEVICE_IP/econet/rmStructure?uid=YOUR_DEVICE_UID&lang=en`

#### Get Parameter Data
- **Endpoint**: `rmParamsData`
- **Method**: GET
- **Description**: Retrieves parameter data
- **Parameters**: 
  - `uid` (optional): Device UID
- **Example**: `GET http://DEVICE_IP/econet/rmParamsData?uid=YOUR_DEVICE_UID`

#### Get Alarm Names
- **Endpoint**: `rmAlarmsNames`
- **Method**: GET
- **Description**: Retrieves alarm definitions and names
- **Parameters**: 
  - `uid` (optional): Device UID
  - `lang` (optional): Language code
- **Example**: `GET http://DEVICE_IP/econet/rmAlarmsNames?uid=YOUR_DEVICE_UID&lang=en`

#### Get Category Names
- **Endpoint**: `rmCatsNames`
- **Method**: GET
- **Description**: Retrieves category names
- **Parameters**: 
  - `uid` (optional): Device UID
  - `lang` (optional): Language code
- **Example**: `GET http://DEVICE_IP/econet/rmCatsNames?uid=YOUR_DEVICE_UID&lang=en`

#### Get Category Descriptions
- **Endpoint**: `rmCatsDescs`
- **Method**: GET
- **Description**: Retrieves category descriptions
- **Parameters**: 
  - `uid` (optional): Device UID
  - `lang` (optional): Language code
- **Example**: `GET http://DEVICE_IP/econet/rmCatsDescs?uid=YOUR_DEVICE_UID&lang=en`

#### Get Parameter Units Names
- **Endpoint**: `rmParamsUnitsNames`
- **Method**: GET
- **Description**: Retrieves parameter unit names
- **Parameters**: 
  - `uid` (optional): Device UID
  - `lang` (optional): Language code
- **Example**: `GET http://DEVICE_IP/econet/rmParamsUnitsNames?uid=YOUR_DEVICE_UID&lang=en`

#### Get Lock Names
- **Endpoint**: `rmLocksNames`
- **Method**: GET
- **Description**: Retrieves lock names
- **Parameters**: 
  - `uid` (optional): Device UID
  - `lang` (optional): Language code
- **Example**: `GET http://DEVICE_IP/econet/rmLocksNames?uid=YOUR_DEVICE_UID&lang=en`

#### Get Available Languages
- **Endpoint**: `rmExistingLangs`
- **Method**: GET
- **Description**: Retrieves list of available languages
- **Parameters**: 
  - `uid` (optional): Device UID
- **Example**: `GET http://DEVICE_IP/econet/rmExistingLangs?uid=YOUR_DEVICE_UID`

### 4. Parameter Control

#### Set Parameter (Basic)
- **Endpoint**: `newParam`
- **Method**: GET
- **Description**: Sets a parameter value using parameter name
- **Parameters**: 
  - `newParamName`: Parameter name
  - `newParamValue`: Parameter value
  - `uid` (optional): Device UID
- **Example**: `GET http://DEVICE_IP/econet/newParam?newParamName=BOILER_CONTROL&newParamValue=1`

**Response**:
```json
{
  "paramName": "BOILER_CONTROL",
  "paramValue": 1,
  "result": "OK"
}
```

#### Set Parameter (Remote Menu - Index)
- **Endpoint**: `rmNewParam`
- **Method**: GET
- **Description**: Sets a parameter value using parameter index
- **Parameters**: 
  - `newParamIndex`: Parameter index
  - `newParamValue`: Parameter value
  - `uid` (optional): Device UID
- **Example**: `GET http://DEVICE_IP/econet/rmNewParam?newParamIndex=1280&newParamValue=75`

#### Set Parameter (Remote Menu - Key)
- **Endpoint**: `rmCurrNewParam`
- **Method**: GET
- **Description**: Sets a parameter value using parameter key
- **Parameters**: 
  - `newParamKey`: Parameter key
  - `newParamValue`: Parameter value
  - `uid` (optional): Device UID
- **Example**: `GET http://DEVICE_IP/econet/rmCurrNewParam?newParamKey=tempCOSet&newParamValue=75`

### 5. Authentication & Access Control

#### Check Remote Access
- **Endpoint**: `rmAccess`
- **Method**: GET
- **Description**: Checks remote access with password
- **Parameters**: 
  - `password`: Access password
  - `uid` (optional): Device UID
- **Example**: `GET http://DEVICE_IP/econet/rmAccess?password=ACCESS_PASSWORD`

#### Save Language
- **Endpoint**: `rmSaveLang`
- **Method**: GET
- **Description**: Saves language preference
- **Parameters**: 
  - `lang`: Language code
  - `uid` (optional): Device UID
- **Example**: `GET http://DEVICE_IP/econet/rmSaveLang?lang=en`

### 6. Device Management

#### Get Device Parameters
- **Endpoint**: `getDeviceParams`
- **Method**: GET
- **Description**: Retrieves device parameters
- **Parameters**: 
  - `uid`: Device UID
- **Example**: `GET http://DEVICE_IP/econet/getDeviceParams?uid=YOUR_DEVICE_UID`

#### Get Device Reg Parameters
- **Endpoint**: `getDeviceRegParams`
- **Method**: GET
- **Description**: Retrieves device regular parameters
- **Parameters**: 
  - `uid`: Device UID
- **Example**: `GET http://DEVICE_IP/econet/getDeviceRegParams?uid=YOUR_DEVICE_UID`

#### Get Device Sys Parameters
- **Endpoint**: `getDeviceSysParams`
- **Method**: GET
- **Description**: Retrieves device system parameters
- **Parameters**: 
  - `uid`: Device UID
- **Example**: `GET http://DEVICE_IP/econet/getDeviceSysParams?uid=YOUR_DEVICE_UID`

#### Get Device Editable Parameters
- **Endpoint**: `getDeviceEditableParams`
- **Method**: GET
- **Description**: Retrieves device editable parameters
- **Parameters**: 
  - `uid`: Device UID
- **Example**: `GET http://DEVICE_IP/econet/getDeviceEditableParams?uid=YOUR_DEVICE_UID`

#### Get Device Alarms
- **Endpoint**: `getDeviceAlarms`
- **Method**: GET
- **Description**: Retrieves device alarms
- **Parameters**: 
  - `uid`: Device UID
- **Example**: `GET http://DEVICE_IP/econet/getDeviceAlarms?uid=YOUR_DEVICE_UID`

### 7. Scheduling

#### Save Schedules
- **Endpoint**: `saveSchedules`
- **Method**: GET
- **Description**: Saves device schedules
- **Parameters**: 
  - `scheduleType`: Type of schedule
  - `timeOfWeek`: Time of week
  - `values`: Schedule values
  - `scheduleDev`: Schedule device
  - `uid` (optional): Device UID
- **Example**: `GET http://DEVICE_IP/econet/saveSchedules?scheduleType=heating&timeOfWeek=1&values=75&scheduleDev=boiler`

#### Get Schedules
- **Endpoint**: `getSchedule`
- **Method**: GET
- **Description**: Retrieves device schedules
- **Parameters**: 
  - `uid` (optional): Device UID
- **Example**: `GET http://DEVICE_IP/econet/getSchedule?uid=YOUR_DEVICE_UID`

### 8. Software Updates

#### Check Software Update
- **Endpoint**: `checkSoftwareUpdate`
- **Method**: GET
- **Description**: Checks for software updates
- **Parameters**: 
  - `protocol`: Protocol type
  - `router` (optional): Router type
- **Example**: `GET http://DEVICE_IP/econet/checkSoftwareUpdate?protocol=em&router=ecoMAX810P-L`

#### Update Software
- **Endpoint**: `updateEconet`
- **Method**: GET
- **Description**: Updates device software
- **Parameters**: 
  - `uid` (optional): Device UID
- **Example**: `GET http://DEVICE_IP/econet/updateEconet?uid=YOUR_DEVICE_UID`

### 9. Logging & Monitoring

#### Get Econet Log
- **Endpoint**: `getEconetLog`
- **Method**: GET
- **Description**: Retrieves econet log
- **Parameters**: 
  - `uid`: Device UID
- **Example**: `GET http://DEVICE_IP/econet/getEconetLog?uid=YOUR_DEVICE_UID`

#### Get Fuel Consumption
- **Endpoint**: `getFuelConsumption`
- **Method**: GET
- **Description**: Retrieves fuel consumption data
- **Parameters**: 
  - `uid`: Device UID
  - `fromDate`: Start date
  - `toDate`: End date
- **Example**: `GET http://DEVICE_IP/econet/getFuelConsumption?uid=YOUR_DEVICE_UID&fromDate=2024-01-01&toDate=2024-01-31`

### 10. Device Control

#### Restart Device
- **Endpoint**: `restartDevice`
- **Method**: GET
- **Description**: Restarts the device
- **Parameters**: 
  - `uid`: Device UID
- **Example**: `GET http://DEVICE_IP/econet/restartDevice?uid=YOUR_DEVICE_UID`

## Error Responses

### Common Error Codes
- `UNAUTHORIZED`: Authentication failed
- `NOTYPE`: Invalid parameter type
- `ERROR`: General error

### Error Response Format
```json
{
  "result": "ERROR",
  "message": "Error description"
}
```

## Testing Examples

### Using cURL

```bash
# Get system parameters
curl -u admin:password "http://DEVICE_IP/econet/sysParams"

# Get current parameters
curl -u admin:password "http://DEVICE_IP/econet/regParams"

# Turn boiler ON
curl -u admin:password "http://DEVICE_IP/econet/newParam?newParamName=BOILER_CONTROL&newParamValue=1"

# Turn boiler OFF
curl -u admin:password "http://DEVICE_IP/econet/newParam?newParamName=BOILER_CONTROL&newParamValue=0"

# Set temperature
curl -u admin:password "http://DEVICE_IP/econet/rmCurrNewParam?newParamKey=tempCOSet&newParamValue=75"
```

### Using JavaScript (Browser Console)

```javascript
// Get system parameters
fetch('/econet/sysParams')
  .then(response => response.json())
  .then(data => console.log('System params:', data));

// Get current parameters
fetch('/econet/regParams')
  .then(response => response.json())
  .then(data => console.log('Current params:', data));

// Turn boiler ON
fetch('/econet/newParam?newParamName=BOILER_CONTROL&newParamValue=1')
  .then(response => response.json())
  .then(data => console.log('Boiler ON response:', data));

// Turn boiler OFF
fetch('/econet/newParam?newParamName=BOILER_CONTROL&newParamValue=0')
  .then(response => response.json())
  .then(data => console.log('Boiler OFF response:', data));
```

## Integration with Home Assistant

Your current integration already implements several of these endpoints:

### Implemented Endpoints
- ✅ `sysParams` - System parameters
- ✅ `regParams` - Current parameters
- ✅ `regParamsData` - Parameter definitions
- ✅ `rmCurrentDataParamsEdits` - Editable parameters with limits
- ✅ `newParam` - Basic parameter setting
- ✅ `rmCurrNewParam` - Advanced parameter setting

### Potential New Endpoints to Implement
- 🔄 `rmCurrentDataParams` - Current data with language support
- 🔄 `rmParamsNames` - Parameter names
- 🔄 `rmParamsEnums` - Parameter enumerations
- 🔄 `rmStructure` - Menu structure
- 🔄 `rmAlarmsNames` - Alarm definitions
- 🔄 `getDeviceAlarms` - Device alarms
- 🔄 `getFuelConsumption` - Fuel consumption data
- 🔄 `getEconetLog` - Device logs

## Development Recommendations

### High Priority Features
1. **Boiler Control** - Implement ON/OFF control using the `mode` parameter
2. **Temperature Control** - Add number entities for `tempCOSet` and `tempCWUSet`
3. **Alarm Monitoring** - Create binary sensors for alarm detection
4. **Mixer Control** - Add number entity for `mixerSetTemp1`

### Medium Priority Features
1. **Fuel Level Monitoring** - Add sensor for `fuelLevel`
2. **Fan Control** - Add number entity for `fanPower`
3. **Lambda Sensor** - Add sensor for `lambdaLevel`
4. **Temperature Sensors** - Add sensors for all temperature readings

### Low Priority Features
1. **Language Support** - Implement multi-language parameter names
2. **Menu Structure** - Use `rmStructure` for organized parameter categories
3. **Scheduling** - Implement schedule management
4. **Device Logs** - Add logging capabilities

## Notes

1. **Language Support**: Many endpoints support language parameters (`lang`) for internationalization
2. **UID Parameter**: Most endpoints support an optional `uid` parameter for multi-device setups
3. **Authentication**: All endpoints require proper authentication
4. **Caching**: The JavaScript implementation uses `cache: false` for most requests
5. **Error Handling**: Implement proper error handling for all API calls
6. **Device Specific**: The ecoMAX810P-L TOUCH has specific parameter ranges and capabilities

## Next Steps

1. Test the remaining endpoints on your local device
2. Implement additional endpoints in your Home Assistant integration
3. Add support for language-specific parameter names
4. Implement alarm monitoring functionality
5. Add fuel consumption tracking
6. Implement device logging capabilities 

## **Parameter Mapping Analysis:**

### **Temperature Parameters (1024-1034)**
- **1024**: 22.55°C = `tempCO` (Central Heating)
- **1025**: 72.65°C = `tempCWU` (Hot Water)
- **1028**: null = Mixer temperature
- **1029**: null = Mixer temperature
- **1030**: 20.29°C = `tempFlueGas` (Flue Gas)
- **1031**: 24.52°C = `mixerTemp1`
- **1032-1034**: null = Other mixer temperatures

### **Setpoint Parameters (1280-1290)**
- **1280**: 41 = `tempCOSet` (Central Heating setpoint)
- **1281**: 20 = `tempCWUSet` (Hot Water setpoint)
- **1287**: 24 = `mixerSetTemp1`
- **1288**: 30 = `mixerSetTemp2`
- **1289**: 25 = `mixerSetTemp3`
- **1290**: 25 = `mixerSetTemp4`

### **Status Parameters (1536-1555)**
- **1536-1555**: Various boolean status parameters (pumps, fans, etc.)

### **Control Parameters (1792-2049)**
- **1792-1795**: Control values
- **2048-2049**: Additional control parameters

## **Now let's test the editable parameters endpoint!**

In your browser console, paste this command:

```javascript
fetch('/econet/rmCurrentDataParamsEdits')
  .then(r => r.json())
  .then(data => console.log('rmCurrentDataParamsEdits:', data))
  .catch(err => console.error('Error:', err));
```

**This will show us which parameters are editable and their limits!**

## **Development Notes:**

### **Parameter Index Mapping for Your Integration:**
```python
<code_block_to_apply_changes_from>
```

### **Key Findings:**
1. **Parameter Indexes**: Your device uses numeric indexes (1024, 1280, etc.) for parameters
2. **Editable Parameters**: Setpoints (1280-1290) are likely editable
3. **Read-only Parameters**: Temperatures (1024-1034) are read-only
4. **Status Parameters**: Boolean values (1536-1555) for pump/fan status

**Go ahead and test the rmCurrentDataParamsEdits endpoint!** This will tell us exactly which parameters can be controlled and their min/max limits. 

## **Alarm Definitions Analysis:**

### **Alarm Code Meanings:**
- **0**: "Tiekimo pertrūkių" (Feeding interruptions) - Normal operation
- **1**: "Katilo temperatūros jutiklio gedimas" (Boiler temperature sensor failure)
- **2**: "Katilo maksimalios temperatūros peržen." (Boiler maximum temperature exceeded)
- **3**: "Tiekiklio temperatūros jutiklio gedimas" (Feeder temperature sensor failure)
- **4**: "Tiekiklio maksimalios temperatūros peržen." (Feeder maximum temperature exceeded)
- **5**: "Šmetamųjų dujų jutiklio gedimas" (Flue gas sensor failure)
- **7**: "Nepavykęs katilo užkūrimo bandymas. Ištuštinkite peleninę." (Failed boiler ignition attempt. Empty the ash pan.)
- **11**: "Sugedęs ventiliatorius" (Broken fan)
- **255**: "Aliarmas tęsiasi!" (Alarm continues!)

## **Now let's test the menu structure!**

In your browser console, paste this command:

```javascript
fetch('/econet/rmStructure?lang=en')
  .then(r => r.json())
  .then(data => console.log('rmStructure:', data))
  .catch(err => console.error('Error:', err));
```

**This will show us how the parameters are organized in menus!**

## **Development Implementation Plan:**

### **Alarm Monitoring for Your Integration:**
1. **Binary Sensor**: "Boiler Alarm" - Active when any alarm code > 0
2. **Sensor**: "Alarm Code" - Shows current alarm code
3. **Sensor**: "Alarm Description" - Shows alarm description in Lithuanian

### **Alarm Priority:**
- **High Priority**: Codes 1, 2, 3, 4, 5, 11 (sensor failures, temperature exceeded)
- **Medium Priority**: Code 7 (ignition failure - needs ash pan emptying)
- **Low Priority**: Code 0 (normal operation)

### **Key Findings:**
- **Alarm Code 7** (most frequent in your logs) = **Failed ignition, empty ash pan**
- **Alarm Code 2** = **Boiler temperature exceeded**
- **Alarm Code 0** = **Normal operation**

**Go ahead and test the menu structure endpoint!** This will help us understand how to organize the parameters in your Home Assistant integration. 

## **Menu Structure Analysis:**

### **Key Findings:**
1. **Type 3** = Data parameters (with `data_id` linking to parameter indexes)
2. **Type 7** = Menu separators/categories
3. **Type 1** = Menu items
4. **Type 0** = Other menu elements
5. **Lock** = Some parameters are locked (require password)

### **Parameter Mapping in Menu:**
- **data_id: "1024"** = Central Heating temperature
- **data_id: "1025"** = Hot Water temperature  
- **data_id: "1030"** = Flue Gas temperature
- **data_id: "1031"** = Mixer 1 temperature
- **data_id: "1287"** = Mixer 1 setpoint (editable)
- **data_id: "1536"** = Pump CO status
- **data_id: "1538"** = Pump CWU status
- **data_id: "1540"** = Fan status
- **data_id: "1541"** = Other pump status
- **data_id: "1542"** = Other pump status

## **✅ rmCurrentDataParams - Current Data Parameters (with Language Support)**

**Endpoint:** `/econet/rmCurrentDataParams?lang=en`  
**Response Version:** 17127

### **Key Parameter Categories:**

#### **🌡️ Temperature Sensors (special: 1, unit: 1 = °C):**
- **1024**: Katilo temperatūra (Boiler Temperature)
- **1025**: BVŠ temperatūra (DHW Temperature) 
- **1028**: Viršutinė buferio temperatūra (Upper Buffer Temperature)
- **1029**: Žemutinė buferio temperatūra (Lower Buffer Temperature)
- **1030**: Išmetamųjų dujų temperatūra (Flue Gas Temperature)
- **1031**: Temperatūra maišytuvo 1 (Mixer 1 Temperature)
- **1032**: Temperatūra maišytuvo 2 (Mixer 2 Temperature)
- **1033**: Temperatūra maišytuvo 3 (Mixer 3 Temperature)
- **1034**: Temperatūra maišytuvo 4 (Mixer 4 Temperature)
- **26**: Tiektuvo temperatūra (Supply Temperature)
- **28**: Oro temperatūra (Air Temperature)

#### **🎛️ Setpoint Parameters (special: 0, unit: 1 = °C):**
- **1280**: Katilui užduota temp. (Boiler Setpoint Temperature)
- **1281**: BVŠ nustatyta temp (DHW Setpoint Temperature)
- **1287**: Nustatyta temperatūra maišyt. 1 (Mixer 1 Setpoint)
- **1288**: Nustatyta temperatūra maišyt. 2 (Mixer 2 Setpoint)
- **1289**: Nustatyta temperatūra maišyt. 3 (Mixer 3 Setpoint)
- **1290**: Nustatyta temperatūra maišyt. 4 (Mixer 4 Setpoint)

#### **🔧 Binary Status Sensors (special: 1, unit: 31 = ON/OFF):**
- **1536**: Ventiliatorius (Fan)
- **1538**: Tiekiklis (Feeder)
- **1540**: Papil. tiekiklis (Additional Feeder)
- **1541**: Katilo siurblys (Boiler Pump)
- **1542**: BVŠ siurblys (DHW Pump)
- **1543**: Cirk. siurb. (Circulation Pump)
- **1544**: Siurblys maišytuvo 1 (Mixer 1 Pump)
- **1547**: Siurblys maišytuvo 2 (Mixer 2 Pump)
- **1550**: Siurblys maišytuvo 3 (Mixer 3 Pump)
- **1553**: Siurblys maišytuvo 4 (Mixer 4 Pump)

#### **🎚️ Valve Controls (special: 0, unit: 5 = %):**
- **139**: Vožtuvas maišytuvo 1 (Mixer 1 Valve)
- **140**: Vožtuvas maišytuvo 2 (Mixer 2 Valve)
- **141**: Vožtuvas maišytuvo 3 (Mixer 3 Valve)
- **142**: Vožtuvas maišytuvo 4 (Mixer 4 Valve)

#### **📊 Statistics & Counters (special: 0, unit: 4 = hours, unit: 0 = count):**
- **155**: Darbo laik. su galing. 100% (Operating Time 100% Power)
- **156**: Darbo laikas su galing. 50% (Operating Time 50% Power)
- **157**: Darbo laikas su galingumu 30% (Operating Time 30% Power)
- **158**: Tiektuvo darbo laikas (Feeder Operating Time)
- **159**: Uždegimų kiekis (Ignition Count)
- **160**: Katilo pakart. paleid. kiekis (Boiler Restart Count)

#### **📡 Network & Communication:**
- **161-168**: IP, Template, Gateway, Server settings
- **170**: Signalo stiprumas (Signal Strength)
- **171**: WiFi statusas (WiFi Status)
- **173**: SSID

#### **⚡ Power & Performance:**
- **1794**: Katilo galingum. (Boiler Power %)

### **Special Types Mapping:**
- **special: 0** = Standard parameters (setpoints, valves, counters)
- **special: 1** = Status sensors (temperatures, binary states)
- **special: 2** = Oxygen sensor
- **special: 3** = Valve status
- **special: 4** = Mixer drive
- **special: 5** = Network/communication status
- **special: 6** = Protection status
- **special: 7** = Empty/placeholder

### **Unit Types:**
- **unit: 0** = Text/count
- **unit: 1** = Temperature (°C)
- **unit: 4** = Time (hours)
- **unit: 5** = Percentage (%)
- **unit: 31** = Binary (ON/OFF)

## **✅ rmParamsEnums - Parameter Enumeration Values**

**Endpoint:** `/econet/rmParamsEnums`  
**Response Version:** 23521

### **Key Enumeration Categories:**

#### **🔄 Basic Binary States:**
- **Enum 1**: `["OFF", "ON"]` - Standard ON/OFF states
- **Enum 5**: `["Atjungtas", "Įjungtas"]` - Lithuanian ON/OFF (Disconnected/Connected)
- **Enum 10**: `["Išjungtas", "Įjungtas"]` - Lithuanian ON/OFF (Turned off/Turned on)
- **Enum 13**: `["NE", "TAIP"]` - Lithuanian NO/YES
- **Enum 15**: `["Išjungtas", "Įjungtas"]` - Another ON/OFF variant
- **Enum 19**: `["NE", "TAIP"]` - Another YES/NO variant
- **Enum 20**: `["NE", "TAIP"]` - Another YES/NO variant
- **Enum 21**: `["NE", "TAIP"]` - Another YES/NO variant
- **Enum 22**: `["NE", "TAIP"]` - Another YES/NO variant
- **Enum 24**: `["Išjungta", "Įjungta"]` - Female form ON/OFF
- **Enum 25**: `["Išjungti", "Įjungti"]` - Plural form ON/OFF

#### **🔥 Boiler Operating States:**
- **Enum 7**: `["IŠJUNGTAS", "Uždegimas", "STABILIZACIJA", "DARBAS", "Priežiūra", "Užgesinimas", "SUSTOJ.", "IŠJ.PAGAL REIKAL.", "RANKINI", "ALIARM", "Įtrūkimas", "KAMINKRĖTYS", "PALEIDIMAS", "TRANSMISIJOS STOKA"]`
  - **0**: IŠJUNGTAS (TURNED OFF)
  - **1**: Uždegimas (Ignition)
  - **2**: STABILIZACIJA (Stabilization)
  - **3**: DARBAS (Working)
  - **4**: Priežiūra (Maintenance)
  - **5**: Užgesinimas (Extinguishing)
  - **6**: SUSTOJ. (Stopped)
  - **7**: IŠJ.PAGAL REIKAL. (Turned off by demand)
  - **8**: RANKINI (Manual)
  - **9**: ALIARM (Alarm)
  - **10**: Įtrūkimas (Breakdown)
  - **11**: KAMINKRĖTYS (Chimney sweep)
  - **12**: PALEIDIMAS (Starting)
  - **13**: TRANSMISIJOS STOKA (Transmission failure)

#### **🌡️ Season Modes:**
- **Enum 11**: `["Žiemos", "Vasaros", "Auto", "Žiemos", "Vasaros"]` - Winter/Summer/Auto modes

#### **🔧 Control Modes:**
- **Enum 8**: `["Standartinis", "FuzzyLogic", "Lambda FuzzyLogic"]` - Control algorithms
- **Enum 9**: `["Išjungtas", "Prioritetas", "Be prioriteto"]` - Priority modes
- **Enum 14**: `["Išjungta", "CŠ įjungta", "Įjung.grind.", "Tiktai siurblys"]` - DHW modes
- **Enum 16**: `["Išjungtas", "Universalus", "ecoSTER T1", "ecoSTER T2", "ecoSTER T3", ...]` - Sensor types

#### **📡 Network & Communication:**
- **Enum 6**: `["", "OPEN", "WEP", "WPA", "WPA2"]` - WiFi security types
- **Enum 2**: `["STOP", "START", "", "Kalibravimas"]` - Start/Stop/Calibration
- **Enum 3**: `["", "Kalibravimas"]` - Calibration mode
- **Enum 4**: `["STOP", "OFF", "ON"]` - Stop/Off/On states

#### **⛽ Fuel Level:**
- **Enum 17**: `["100% kuro lygis", "0% kuro lygis", ""]` - Fuel level indicators

#### **🎛️ Power Levels:**
- **Enum 26**: `["30%", "50%", "100%"]` - Power level settings

#### **🔧 Feeder & Maintenance:**
- **Enum 23**: `["Tiekikl. ir grotel", "Tik grotelės"]` - Feeder and grate modes
- **Enum 24**: `["Rezervinis katilas", "Aliarmai", "Cirkuliacinis siurblys"]` - Additional functions

### **Usage in Home Assistant:**
- **Select Entities**: For mode selection (seasons, control algorithms, sensor types)
- **Sensor States**: For boiler operating states and status monitoring
- **Binary Sensors**: For simple ON/OFF states
- **Alarm Detection**: Boiler state "ALIARM" (9) indicates alarm condition

## **✅ rmParamsDescs - Parameter Descriptions**

**Endpoint:** `/econet/rmParamsDescs`  
**Response Version:** 16688

### **Key Parameter Categories with Descriptions:**

#### **🔥 Boiler Control & Power Management:**
- **Fan Power Control**: Ventiliatoriaus galingumas esant maksimaliam/pusei/minimaliam degiklio darbo galingumui
- **Feeder Timing**: Tiekiklio darbo laikas ir pertraukos laikas at different power levels
- **Power Modulation**: Temperature thresholds between power levels
- **Boiler Hysteresis**: Automatic boiler activation when temperature drops below setpoint

#### **🧠 Fuzzy Logic Control:**
- **Fuzzy Logic Mode**: STANDARD vs FUZZY LOGIC vs Lambda FuzzyLogic algorithms
- **Fan Adjustment**: Ventiliatoriaus koregavimas esant Fuzzy Logic darbo režimui
- **Power Limits**: Minimalus/maksimalus galingumas Fuzzy Logic režimui
- **PID Parameters**: Automatic boiler power modulation parameters

#### **🌡️ Temperature Control:**
- **Boiler Setpoint**: Nustatyta katilo temperatūra (27-68°C range)
- **DHW Setpoint**: BVŠ nustatyta temp (hot water temperature)
- **Mixer Setpoints**: Nustatyta temperatūra maišyt. 1-4 (mixer temperature setpoints)
- **Buffer Control**: Upper/lower buffer temperature control
- **Summer Mode**: VASARA režimas (summer mode with outdoor temperature thresholds)

#### **⚙️ Ignition & Maintenance:**
- **Ignition Process**: Uždegimo žvakė, kuro dozės tiekimo laikas, uždegimo bandymų laikas
- **Flue Gas Monitoring**: Išmetamųjų dujų temperatūra for ignition detection
- **Maintenance Mode**: Priežiūra režimas with automatic extinguishing
- **Fuel Level**: Kuro lygio slenkstis (fuel level threshold)

#### **🎚️ Mixer System Control:**
- **Mixer Modes**: IŠJ/CŠ įjungta/Įjung.grind./Tiktai siurblys (OFF/DHW/Floor heating/Pump only)
- **Valve Control**: Vožtuvo atidarymo laikas, stiprintuvo judesių kontrolė
- **Temperature Limits**: Min/max mixer temperature restrictions
- **Room Thermostat**: Kambario termostato kontaktų atidarymo kontrolė

#### **📡 Network & Communication:**
- **WiFi Security**: OPEN/WEP/WPA/WPA2 security types
- **Signal Strength**: Signalo stiprumas monitoring
- **Server Configuration**: IP, Template, Gateway settings

#### **🔧 Advanced Features:**
- **Lambda Sensor**: Deguonies kiekis išmetamosiose dujose (oxygen content)
- **Buffer System**: Buferio krovimo procesas (buffer charging process)
- **Backup Boiler**: Atsarginis katilas (backup boiler control)
- **Circulation Pump**: Cirkuliacinis siurblys control

### **Critical Safety Parameters:**
- **DHW Safety**: "Pernelyg aukšta temperatūra gali nudeginti vartotoją karštu vandeniu!"
- **Fuel Shortage**: Kuro trukumo nustatymas (fuel shortage detection)
- **Fan Blocking**: Ventiliatoriaus blokavimo signalas (fan blocking detection)
- **Temperature Limits**: Maksimalios tiektuvo temperatūros peržengimas

### **Professional Parameters:**
- **Hidden Settings**: "Nustatymas TAIP verte prives prie paslėptų profesionalių parametrų parodymo"
- **Service Access**: Katilo darbo blokavimo galimybė po kambario termostato kontaktų atidarymo

## **✅ rmCatsNames - Menu Category Names**

**Endpoint:** `/econet/rmCatsNames`  
**Response Version:** 26533

### **Complete Menu Structure:**

#### **🏠 Main Menu Categories:**
- **0**: Pagrindinis meniu (Main Menu)
- **1**: Informacijos (Information)
- **2**: Katilo nustatymai (Boiler Settings)
- **3**: BVŠ nustatymai (DHW Settings)
- **4**: Vasaros/Žiemos (Summer/Winter)
- **5**: Maišytuvo 1 nustatymai (Mixer 1 Settings)
- **6**: Maišytuvo 2 nustatymai (Mixer 2 Settings)
- **7**: Maišytuvo 3 nustatymai (Mixer 3 Settings)
- **8**: Maišytuvo 4 nustatymai (Mixer 4 Settings)
- **9**: Kaminkrėtys režimas (Chimney Sweep Mode)
- **10**: Aliarmai (Alarms)
- **11**: Servisiniai nustat. (Service Settings)

#### **📊 Information Categories:**
- **12-15**: Informacijos (Information) - Multiple info screens
- **16**: Maišytuvo informacija 1 (Mixer 1 Information)
- **17**: Maišytuvo informacija 2 (Mixer 2 Information)
- **18**: Maišytuvo informacija 3 (Mixer 3 Information)
- **19**: Maišytuvo informacija 4 (Mixer 4 Information)
- **20-21**: Informacijos ecoNET WiFi (ecoNET WiFi Information)
- **22**: Informacijos ecoNET Ethernet (ecoNET Ethernet Information)
- **38**: Informacijos (Information)

#### **🔧 Service & Professional:**
- **23**: Serviso skaičiuoklės (Service Counters)
- **24**: Galingumo moduliavimas (Power Modulation)
- **25**: Kuro lygis (Fuel Level)
- **26**: Servisiniai nustat. (Service Settings)
- **27**: Degiklio pasirinkimas (Burner Selection)
- **28**: Profesionalūs nustatymai (Professional Settings)
- **29**: Aptarnavimo informacija (Service Information)

#### **⚙️ Advanced Settings:**
- **30**: Katilo nustatymai (Boiler Settings)
- **31**: CŠ ir BVŠ nustatymaai (CH and DHW Settings)
- **32**: Buferio nustatymai (Buffer Settings)
- **33**: Maišytuvo 1 nustatymai (Mixer 1 Settings)
- **34**: Maišytuvo 2 nustatymai (Mixer 2 Settings)
- **35**: Maišytuvo 3 nustatymai (Mixer 3 Settings)
- **36**: Maišytuvo 4 nustatymai (Mixer 4 Settings)
- **37**: Išėjimo H (Output H)

#### **🔥 Boiler Operation:**
- **39**: Uždegimas (Ignition)
- **40**: Galingumo moduliav (Power Modulation)
- **41**: Užgesinimas (Extinguishing)
- **42**: PRIEŽIŪRA (Maintenance)
- **43**: Lambda zondas (Lambda Sensor)

### **Home Assistant Integration Organization:**
- **Main Dashboard**: Categories 0-11 (user-accessible settings)
- **Service Panel**: Categories 23-29 (professional settings)
- **Advanced Control**: Categories 39-43 (boiler operation)
- **Information Display**: Categories 12-22, 38 (status and monitoring)

## **🎯 COMPLETE API EXPLORATION SUMMARY**

### **✅ Successfully Tested Endpoints (11/12):**
1. **sysParams** - Device identification and capabilities
2. **regParams** - Real-time parameter values
3. **regParamsData** - Parameter definitions with min/max limits
4. **rmCurrentDataParamsEdits** - User-editable parameters
5. **rmParamsNames** - Lithuanian parameter names
6. **rmAlarmsNames** - Alarm codes and descriptions
7. **rmStructure** - Menu organization structure
8. **rmCurrentDataParams** - All available sensors and data
9. **rmParamsEnums** - Parameter enumeration values
10. **rmParamsDescs** - Detailed parameter descriptions
11. **rmCatsNames** - Menu category names

### **❌ Not Available:**
- **rmExistingLangs** - Language support (not implemented on ecoMAX810P-L TOUCH)

### **🔥 Device Capabilities Discovered:**
- **Model**: ecoMAX810P-L TOUCH
- **Software**: Version 3.2.3879
- **Language**: Lithuanian interface
- **Sensors**: 11+ temperature sensors, 10+ binary status sensors
- **Controls**: 6 temperature setpoints, 4 mixer controls
- **Alarms**: 9 different alarm types
- **Modes**: 14 boiler operating states, 3 season modes
- **Advanced**: Fuzzy Logic, Lambda sensor, buffer control

### **✅ Ready for Home Assistant Integration:**
- **Sensors**: All temperature readings with proper units
- **Numbers**: Setpoint controls with min/max limits
- **Binary Sensors**: Pump/fan/feeder statuses
- **Switches**: Boiler ON/OFF control
- **Select Entities**: Mode selection (seasons, algorithms)
- **Alarm Monitoring**: Real-time alarm detection
- **Safety Features**: DHW temperature limits, fuel monitoring

## **✅ Complete Parameter Names Mapping**

**Endpoint:** `/econet/rmParamsNames`  
**Response Version:** 61477

### **🔥 Boiler Control Parameters (0-17):**
- **0**: 100% ventil.galinguma (100% Fan Power)
- **1**: 100% Tiekimo darbas (100% Feeder Work)
- **2**: 100% Tiekimo pertr. (100% Feeder Break)
- **3**: 50% ventil.galinguma (50% Fan Power)
- **4**: 50% Tiekimo darbas (50% Feeder Work)
- **5**: 50% Tiekimo pertr. (50% Feeder Break)
- **6**: 30% ventil.galinguma (30% Fan Power)
- **7**: 30% Tiekimo darbas (30% Feeder Work)
- **8**: 30% Tiekimo darbas (30% Feeder Work)
- **9**: 50% Histerezė H2 (50% Hysteresis H2)
- **10**: 30% Histerezė H1 (30% Hysteresis H1)
- **11**: Katilo histerezė (Boiler Hysteresis)
- **12**: FLventil.koregav. (FL Fan Adjustment)
- **13**: Minimalus katilo galingumas FL (Minimal Boiler Power FL)
- **14**: Maksimalus katilo galingumas FL (Maximal Boiler Power FL)
- **15**: Parametras A FuzzyLogic (Parameter A FuzzyLogic)
- **16**: Parametras B FuzzyLogic (Parameter B FuzzyLogic)
- **17**: Parametras C FuzzyLogic (Parameter C FuzzyLogic)

### **⚙️ Power Modulation (18-25):**
- **18**: Reguliav.tvarka: (Regulation Order)
- **19**: Prapūtimo galingumo korektūra 100% (Blowing Power Correction 100%)
- **20**: Tiekiklio darbo korektūra 100% (Feeder Work Correction 100%)
- **21**: Prapūtimo galingumo korektūra 50% (Blowing Power Correction 50%)
- **22**: Tiekiklio darbo korektūra 50% (Feeder Work Correction 50%)
- **23**: 30% Prapūtimo galingumo korektūra (30% Blowing Power Correction)
- **24**: 30% Tiekiklio darbo korektūra (30% Feeder Work Correction)

### **🔥 Ignition & Maintenance (25-40):**
- **25**: Užkūrim.ventiliator. (Ignition Fan)
- **26**: Užd.priet.test.laik. (Ignition Pretest Time)
- **27**: Uždegim.test.laik.2 (Ignition Test Time 2)
- **28**: Tiekiklio darbas (Feeder Work)
- **29**: Užkūrimo laikas (Ignition Time)
- **30**: Išmetamų dujų delta (Flue Gas Delta)
- **31**: Išmetamųjų dujų delta 2 (Flue Gas Delta 2)
- **32**: Išmetamų dujų temp. uždegimo pabaigoje (Flue Gas Temp at Ignition End)
- **33**: Bandomasis kiekis (Test Amount)
- **34**: Priežiūros laikas (Maintenance Time)
- **35**: Padavimo laikas (Supply Time)
- **36**: Tiekiklio intervalas (Feeder Interval)
- **37**: Ventiliatoriaus min. galingumas (Fan Min Power)
- **38**: Parametras A Lambda (Parameter A Lambda)
- **39**: Parametr B Lambda (Parameter B Lambda)
- **40**: Parametras C Lambda (Parameter C Lambda)

### **🌡️ Oxygen & Temperature Control (41-50):**
- **41**: 100% Deguonis (100% Oxygen)
- **42**: 50% Deguonis (50% Oxygen)
- **43**: 30% Deguonis (30% Oxygen)
- **44**: Pūtimo koregavimo diapazonas (Blowing Adjustment Range)
- **45**: FLdeguonies koreg. (FL Oxygen Correction)
- **46**: Katilui užduota temp. (Boiler Set Temperature) - **ID: 1280**
- **47**: Minimali katilo temperatūra (Minimal Boiler Temperature)
- **48**: Maksimali katilo temperatūra (Maximal Boiler Temperature)
- **49**: BVŠ nustatyta temp (DHW Set Temperature) - **ID: 1281**
- **50**: BVŠ minimali temperatūra (DHW Minimal Temperature)

### **🚿 DHW & Summer Mode (51-60):**
- **51**: BVŠ maksimali temperatūra (DHW Maximal Temperature)
- **52**: BVŠsiurb.darb.tvarka (DHW Pump Work Order)
- **53**: BVŠ kolektoriaus histerezė (DHW Collector Hysteresis)
- **54**: BVŠ dezinfekcija (DHW Disinfection)
- **55**: VASARA režimas (SUMMER Mode)
- **56**: Režimo VASARA įjungimo temp. (SUMMER Mode On Temperature)
- **57**: Režimo VASARA išjungimo temp. (SUMMER Mode Off Temperature)
- **58**: CŠ siurblio prijungimo temperatūra (CH Pump Connection Temperature)
- **59**: CŠ siurblio sustabdymas BVŠ krovimo metu (CH Pump Stop During DHW Charging)
- **60**: Katilo temp.didin. nuo BVŠ ir maišytuvo (Boiler Temp Increase from DHW and Mixer)

### **🎚️ Mixer System (61-100):**
- **61**: BVŠ darbo ilginimas (DHW Work Extension)
- **62**: Šilumos keitiklis (Heat Exchanger)
- **63**: Maišytuvo 1 nustatyta temperatūra (Mixer 1 Set Temperature) - **ID: 1287**
- **64**: Maišytuvo 2 nustatyta temperatūra (Mixer 2 Set Temperature) - **ID: 1288**
- **65**: Maišytuvo 3 nustatyta temperatūra (Mixer 3 Set Temperature) - **ID: 1289**
- **66**: Maišytuvo 4 nustatyta temperatūra (Mixer 4 Set Temperature) - **ID: 1290**
- **67-70**: Minimali maišytuvo 1-4 temperatūra (Minimal Mixer 1-4 Temperature)
- **71-74**: Maksimali maišytuvo 1-4 temperatūra (Maximal Mixer 1-4 Temperature)
- **75-78**: Kambario termostatas 1-4 (Room Thermostat 1-4)
- **79-82**: Maišytuvo 1-4 oro reguliavimas (Mixer 1-4 Air Regulation)
- **83-86**: Maišytuvo 1-4 šildymo kreivė (Mixer 1-4 Heating Curve)
- **87-90**: Maišytuvo 1-4 aptarnavimas (Mixer 1-4 Service)
- **91-94**: Proporcingumo diapazonas (Proportional Range)
- **95-98**: Nuolatinis integracijos laikas (Continuous Integration Time)
- **99-102**: Siurblio atjungimas nuo termostato (Pump Disconnection from Thermostat)

### **🔧 Advanced Control (103-120):**
- **103-106**: Vožtuv.atidar.laikas (Valve Opening Time)
- **107-110**: MaišytuvoNejautrumas 1-4 (Mixer Insensitivity 1-4)
- **111**: Katilo oro reguliavimas (Boiler Air Regulation)
- **112**: Katilo šild.kreivė (Boiler Heating Curve)
- **113**: Katilo atšaldymo temperatūra (Boiler Cooling Temperature)
- **114-117**: Termost.pasirinik. (Thermostat Selection)
- **118**: Cirkuliacinio siurblio prastovos laikas (Circulation Pump Idle Time)
- **119**: Cirkuliacinio siurblio darbo laikas (Circulation Pump Work Time)
- **120-124**: Lygiagretus kreivės perstūmimas (Parallel Curve Shift)

### **📊 Monitoring & Safety (125-140):**
- **125-129**: Kamabrinės temperatūros koeficientas (Room Temperature Coefficient)
- **130**: Žarsteklio ciklo laikas (Grate Cycle Time)
- **131**: Degiklio valymas (Burner Cleaning)
- **132**: Stabilizacijos laikas (Stabilization Time)
- **133**: Gesinimo laikas (Extinguishing Time)
- **134**: Prapūtimo stiprumas (Blowing Strength)
- **135**: Buferio aptarnav (Buffer Service)
- **136**: Krovimo pradžios temperatūra (Charging Start Temperature)
- **137**: Krovimo pabaigos temperatūra (Charging End Temperature)
- **138**: Aliarminis lygis (Alarm Level)
- **139**: Kuro trūkumo detekcijos laikas (Fuel Shortage Detection Time)
- **140**: Įtraukimas (Inclusion)

### **🔧 Additional Features (141-150):**
- **141**: 2 tiekiklio darbo laikas (2nd Feeder Work Time)
- **142**: Tiekiklio 2 darbo laikas (Feeder 2 Work Time)
- **143**: Rezervinis katilas (Backup Boiler)
- **144**: Ventiliatoriaus darbo prailginimas (Fan Work Extension)
- **145**: Maksimali tiektuvo temperatūra (Maximal Feeder Temperature)
- **146**: Išmetamų dujų temp. neesant kurui (Flue Gas Temp Without Fuel)
- **147**: Histerezės funkcija (Hysteresis Function)
- **148**: katilo blokavimas nuo termostato (Boiler Blocking from Thermostat)
- **149**: Blokada nuo termost. (Blocking from Thermostat)
- **150**: Katilo siurblio blokavimas (Boiler Pump Blocking)

### **⚙️ System Control (151-155):**
- **151**: Darbas laiku (Work by Time)
- **152**: Darbas su Lambda (Work with Lambda)
- **153**: Tiekiklio užrakinimas (Feeder Locking)
- **154**: Kuro aptikimas: deguonis (Fuel Detection: Oxygen)
- **155**: Kuro aptikimas: laikas (Fuel Detection: Time)
- **156**: Ventiliatoriaus apsisukimų aptikimas (Fan Rotation Detection)
- **157**: Tiektuvo daviklio režimas (Feeder Sensor Mode)
- **158**: Išėjimo H1 (Output H1)
- **159**: Išėjimo H2 ir H3 (Output H2 and H3)
- **160**: Katilo galingumas (Boiler Power)
- **161**: Darbo laikas (Work Time)
- **162**: Rodyk išplėstinius (Show Extended)
- **163**: Aliarmai (Alarms)

### **🎯 Key Parameter IDs for Home Assistant:**
- **1280**: Katilui užduota temp. (Boiler Set Temperature)
- **1281**: BVŠ nustatyta temp (DHW Set Temperature)
- **1287**: Maišytuvo 1 nustatyta temperatūra (Mixer 1 Set Temperature)
- **1288**: Maišytuvo 2 nustatyta temperatūra (Mixer 2 Set Temperature)
- **1289**: Maišytuvo 3 nustatyta temperatūra (Mixer 3 Set Temperature)
- **1290**: Maišytuvo 4 nustatyta temperatūra (Mixer 4 Set Temperature)

## **Development Summary:**

### **✅ What We've Discovered:**
1. **Device**: ecoMAX810P-L TOUCH with full API access
2. **Parameters**: 11+ temperature sensors, 4 mixer controls, pump/fan statuses
3. **Editable**: Central heating setpoint (27-68°C), mixer setpoints
4. **Alarms**: 9 different alarm types with Lithuanian descriptions
5. **Menu Structure**: Organized parameter hierarchy
6. **Language**: Lithuanian interface with parameter names

### **✅ Ready to Implement:**
- **Number Entities**: Temperature setpoints
- **Sensors**: All temperature readings
- **Binary Sensors**: Pump/fan statuses, alarm detection
- **Switch**: Boiler ON/OFF control
- **Alarm Monitoring**: Real-time alarm detection

**Go ahead and test the final endpoint!** Then we can create a comprehensive implementation plan for your Home Assistant integration. 

## **Let's Test the Remaining Endpoints:**

### **1. Current Data Parameters (with language support):**
In your browser console, run:

```javascript
fetch('/econet/rmCurrentDataParams?lang=en')
  .then(r => r.json())
  .then(data => console.log('rmCurrentDataParams:', data))
  .catch(err => console.error('Error:', err));
```

### **2. Parameter Enumerations:**

```javascript
fetch('/econet/rmParamsEnums')
  .then(r => r.json())
  .then(data => console.log('rmParamsEnums:', data))
  .catch(err => console.error('Error:', err));
```

### **3. Parameter Descriptions:**

```javascript
fetch('/econet/rmParamsDescs')
  .then(r => r.json())
  .then(data => console.log('rmParamsDescs:', data))
  .catch(err => console.error('Error:', err));
```

### **4. Category Names:**

```javascript
fetch('/econet/rmCatsNames')
  .then(r => r.json())
  .then(data => console.log('rmCatsNames:', data))
  .catch(err => console.error('Error:', err));
```

### **5. Available Languages:**

```javascript
fetch('/econet/rmExistingLangs')
  .then(r => r.json())
  .then(data => console.log('rmExistingLangs:', data))
  .catch(err => console.error('Error:', err));
```

**Please test these endpoints one by one and share the responses!** This will give us a complete picture of the API capabilities for your Home Assistant integration.

After we test these, we'll have explored all the major endpoints from the JavaScript file and can create a comprehensive implementation plan! 🚀 

## **Remaining Endpoints to Test:**

### **1. Parameter Enumerations:**
```javascript
<code_block_to_apply_changes_from>
```

### **2. Parameter Descriptions:**
```javascript
fetch('/econet/rmParamsDescs')
  .then(r => r.json())
  .then(data => console.log('rmParamsDescs:', data))
  .catch(err => console.error('Error:', err));
```

### **3. Category Names:**
```javascript
fetch('/econet/rmCatsNames')
  .then(r => r.json())
  .then(data => console.log('rmCatsNames:', data))
  .catch(err => console.error('Error:', err));
```

### **4. Available Languages:**
```javascript
fetch('/econet/rmExistingLangs')
  .then(r => r.json())
  .then(data => console.log('rmExistingLangs:', data))
  .catch(err => console.error('Error:', err));
```

## **🎯 What We've Discovered So Far:**

### **✅ Complete Parameter Mapping:**
- **11 Temperature Sensors** (boiler, DHW, buffer, flue gas, mixers, supply, air)
- **6 Setpoint Controls** (boiler, DHW, 4 mixers)
- **10 Binary Status Sensors** (fan, feeders, pumps)
- **4 Valve Controls** (mixer valves)
- **6 Statistics/Counters** (operating times, ignition count)
- **Network & Power monitoring**

### **✅ Ready for Home Assistant Integration:**
- **Sensors**: All temperature readings with proper units
- **Numbers**: Setpoint controls with min/max limits
- **Binary Sensors**: Pump/fan/feeder statuses
- **Switches**: Boiler ON/OFF control
- **Alarm Monitoring**: Real-time alarm detection

**Please test the remaining 4 endpoints and share the responses!** This will complete our API documentation and we can then create a comprehensive implementation plan for your Home Assistant integration. 🚀 

## **🔍 Key Discoveries from dev_set2.js:**

### **1. Parameter Connection Mappings:**
```javascript
var PARAMETERS_CONN = {
    "tempCO": ["CO_TEMP_SET", "CO_TEMP_SET"],
    "tempCWU": ["CWU_SET_TEMP", "CWU_SET_TEMP"],
    "mixerTemp1": ["MIX_SET_TEMP_1", "SET_TEMP_H_1"],
    "mixerTemp2": ["MIX_SET_TEMP_2", "SET_TEMP_H_2"],
    "mixerTemp3": ["MIX_SET_TEMP_3", "SET_TEMP_H_3"],
    "mixerTemp4": ["MIX_SET_TEMP_4", "SET_TEMP_H_4"],
    // ... up to mixerTemp8
}
```

### **2. Remote Menu Parameter IDs:**
```javascript
var RM_PARAMETERS_CONN = {
    "tempCO": "1280",
    "tempCWU": "1281", 
    "mixerTemp1": "1287",
    "mixerTemp2": "1288",
    "mixerTemp3": "1289",
    "mixerTemp4": "1290",
    "mixerTemp5": "1291",
    "mixerTemp6": "1292"
}
```

**This confirms our API findings!** The parameter IDs we discovered (1280, 1281, 1287-1290) match exactly with the web interface mappings.

### **3. ecoSTER Temperature Control:**
```javascript
var ecoSterTemp1 = [
    "STER_TEMP_DAY_1", "STER_TEMP_NIGHT_1", 
    "STER_TEMP_SET_PARTY_1", "STER_TEMP_SET_SUMMER_1",
    "STER_TEMP_ANTIFREEZ_1", "STER_MODE_1", "WORK_MODE_H_1"
]
```

### **4. Pump System Mappings:**
```javascript
var FonkoPumps = {"P1":"CWUCOUT","P3":"H2OUTnum","P4":"H1OUTnum"};
var GalmetPumps = {"P1":"LPOutnum","P2":"LPUpN","P3":"CWUCOUT","P4":"H1OUTnum","P5":"H2OUTnum"};
var PumpsDict = {59:FonkoPumps, 60:GalmetPumps, 62:FonkoPumps, 63:GalmetPumps, 61:EsnodPumps, 96:ThermoshopPumps};
```

### **5. Tile System for UI:**
```javascript
var tiles_type_temp = "tile_temp";
var tiles_type_temp_ro = "tile_temp_ro";
var tiles_type_level = "tile_level";
var tiles_type_flame = "tile_flame";
var tiles_type_fan = "tile_fan";
var tiles_type_pump = "tile_pump";
```

## **🎯 What This Tells Us:**

### **✅ Confirmation of Our API Analysis:**
- **Parameter IDs match** our API discoveries
- **Mixer system** supports up to 8 mixers (not just 4)
- **ecoSTER integration** for room temperature control
- **Multiple pump configurations** for different boiler models

### **🔧 Additional Capabilities:**
- **Real-time UI updates** with tile system
- **Multiple pump types** (Fonko, Galmet, Esnod, Thermoshop)
- **Advanced temperature control** with ecoSTER panels
- **Dynamic parameter connections**
