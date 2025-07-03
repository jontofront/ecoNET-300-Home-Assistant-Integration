# ecoNET-300 API Documentation

## Overview
This document provides comprehensive documentation of the ecoNET-300 API endpoints and device information based on analysis of the official JavaScript implementation.

## Base URL Structure
The API uses a RESTful structure with the following base endpoints:
- Device-specific endpoints: `{base_url}?uid={device_uid}&`
- Global endpoints: `{base_url}`

## Core API Endpoints

### Device Management

#### Get Devices
```
GET /getDevices
```
**Parameters:**
- `active` (boolean) - Show active devices
- `notactive` (boolean) - Show inactive devices  
- `blocked` (boolean) - Show blocked devices
- `deviceType` (string) - Filter by device type
- `uid` (string) - Filter by device UID
- `prodId` (string) - Filter by producer ID
- `page` (integer) - Page number for pagination
- `softVer` (string) - Filter by software version
- `v_mod_a` (string) - Module A version filter
- `v_panel` (string) - Panel version filter

#### Get Device Parameters
```
GET /getDeviceParams?uid={device_uid}
```

#### Get Device Regular Parameters
```
GET /getDeviceRegParams?uid={device_uid}
```

#### Get Device System Parameters
```
GET /getDeviceSysParams?uid={device_uid}
```

#### Get Device Editable Parameters
```
GET /getDeviceEditableParams?uid={device_uid}
```

#### Get Device Alarms
```
GET /getDeviceAlarms?uid={device_uid}
```

### Remote Menu Endpoints

#### Get Remote Menu Languages
```
GET /rmLangs?uid={device_uid}
```

#### Get Current Parameters Edits
```
GET /rmCurrentDataParamsEdits?uid={device_uid}
```

#### Get Remote Menu Parameters Names
```
GET /rmParamsNames?uid={device_uid}&lang={language}
```

#### Get Remote Menu Categories Names
```
GET /rmCatsNames?uid={device_uid}&lang={language}
```

#### Get Remote Menu Parameters Units Names
```
GET /rmParamsUnitsNames?uid={device_uid}&lang={language}
```

#### Get Remote Menu Parameters Enums
```
GET /rmParamsEnums?uid={device_uid}&lang={language}
```

#### Get Remote Menu Locks Names
```
GET /rmLocksNames?uid={device_uid}&lang={language}
```

#### Get Remote Menu Structure
```
GET /rmStructure?uid={device_uid}&lang={language}
```

#### Get Remote Menu Current Data Display
```
GET /rmCurrentDataParams?uid={device_uid}&lang={language}
```

#### Get Remote Menu Parameters Data
```
GET /rmParamsData?uid={device_uid}
```

#### Get Remote Menu Existing Languages List
```
GET /rmExistingLangs?uid={device_uid}
```

#### Get Remote Menu Alarms Names
```
GET /rmAlarmsNames?uid={device_uid}&lang={language}
```

#### Get Remote Menu Parameters Descriptions
```
GET /rmParamsDescs?uid={device_uid}&lang={language}
```

#### Get Remote Menu Categories Descriptions
```
GET /rmCatsDescs?uid={device_uid}&lang={language}
```

### Parameter Management

#### Save Parameter
```
GET /newParam?newParamName={name}&newParamValue={value}
```

#### Save Remote Menu Parameter
```
GET /rmNewParam?uid={device_uid}&newParamIndex={index}&newParamValue={value}
```

#### Save Current Remote Menu Parameter
```
GET /rmCurrNewParam?uid={device_uid}&newParamKey={key}&newParamValue={value}
```

### Authentication & Access Control

#### Get Password
```
GET /call/run/getServicePassword?uid={device_uid}
```

#### Get ET Service Passwords
```
GET /getETservicePasswords?uid={device_uid}
```

#### Check Remote Menu Access
```
GET /rmAccess?uid={device_uid}&password={password}
```

#### Save Remote Menu Language
```
GET /rmSaveLang?uid={device_uid}&lang={language}
```

### Device Configuration

#### Get Device Configuration
```
GET /getDeviceConfig?uid={device_uid}&file_prefix={prefix}
```

#### Check Device Config File Exists
```
GET /isDevConfigFileExists?uid={device_uid}
```

#### Get Device Config Files Info Dictionary
```
GET /getDevConfigFilesInfoDict?uid={device_uid}
```

#### Get Update State Element
```
GET /getUpdateStateElement?uid={device_uid}
```

#### Get Black/White Lists
```
GET /getBlWhLists?uid={device_uid}
```

#### Update Black/White Lists
```
GET /updateBlWhLists/?whiteList={whitelist}&blackList={blacklist}&uid={device_uid}
```

### Device Control

#### Restart Device
```
GET /restartDevice?uid={device_uid}
```

#### Set Device Settings
```
GET /setDevSettings?uid={device_uid}&label={label}&serviceAccess={access}&alarmNotifications={notifications}
```

#### Set Device Address Settings
```
GET /setDevAddrSettings?uid={device_uid}&street={street}&house={house}&apartment={apartment}&postalCode={code}&city={city}&country={country}
```

#### Change Advanced User Password
```
GET /changeAdvancedUserPass?uid={device_uid}&serviceParamsPass={password}
```

### Software Updates

#### Update Software
```
GET /updateEconet?uid={device_uid}
```

#### Check Software Update
```
GET /checkSoftwareUpdate?protocol={protocol}&router={router_type}
```

#### Confirm Update
```
GET /confirmUpdate/?uid={device_uid}
```

#### Cancel Update
```
GET /cancelUpdate/?uid={device_uid}
```

#### Get Update Progress
```
GET /getUpdateProgress/?uid={device_uid}
```

#### Get Update Config Progress
```
GET /getUpdateConfigProgress/?uid={device_uid}
```

### Logging & Monitoring

#### Get Econet Log
```
GET /getEconetLog?uid={device_uid}
```

#### Get Econet Log File
```
GET /getEconetFlLog?uid={device_uid}
```

#### Start Econet Log File
```
GET /startEconetLogFl?uid={device_uid}
```

#### Stop Econet Log File
```
GET /stopEconetLogFl?uid={device_uid}
```

### History & Analytics

#### Get History Parameters Values
```
GET /getHistoryParamsValues?uid={device_uid}&fromDate={from}&toDate={to}
```

#### Get Fuel Consumption
```
GET /getFuelConsumption?uid={device_uid}&fromDate={from}&toDate={to}
```

#### Get Yield Heats
```
POST /getYieldHeats/
```
**Body:**
```json
{
  "uid": "device_uid",
  "days": "number_of_days"
}
```

### Schedules

#### Save Schedules
```
GET /saveSchedules?uid={device_uid}&scheduleType={param}&timeOfWeek={mode}&values={value}&scheduleDev={device}
```

#### Save Ventilation Schedules
```
GET /saveVentSchedules?uid={device_uid}&data={data}&param={param}&value={value}
```

#### Get Schedules
```
GET /getSchedule?uid={device_uid}
```

### Translations

#### Get ET Translations
```
POST /service/getETtranslations/
```
**Body:**
```json
{
  "ver": "version",
  "client": "client_id", 
  "lang": "language",
  "regName": "controller_id"
}
```

## Device Types & Protocols

### Supported Device Types
- `ecoMAX360i` - ecoMAX 360i boiler
- `ecoMAX810P-L` - ecoMAX 810P-L boiler
- `ecoMAX860P2-N` - ecoMAX 860P2-N boiler
- `ecoMAX860P3-V` - ecoMAX 860P3-V boiler
- `ecoSOL` - ecoSOL solar system
- `SControl MK1` - SControl MK1 controller

### Protocol Types
- `em` - ecoMAX protocol
- `gm3` - ecoTronic protocol
- `gm3_pomp` - ecoTronic pump protocol

## Parameter Mappings

### Common Parameters
| Parameter ID | Name | Description | Unit |
|-------------|------|-------------|------|
| 112 | boilerHeatingCurve | Boiler heating curve | None |
| 1280 | tempCOSet | Heating target temperature | °C |
| 1281 | tempCWUSet | Water heater set temperature | °C |
| 1287 | mixerSetTemp1 | Mixer 1 target temperature | °C |
| 1288 | mixerSetTemp2 | Mixer 2 target temperature | °C |
| 1289 | mixerSetTemp3 | Mixer 3 target temperature | °C |
| 1290 | mixerSetTemp4 | Mixer 4 target temperature | °C |
| 1291 | mixerSetTemp5 | Mixer 5 target temperature | °C |
| 1292 | mixerSetTemp6 | Mixer 6 target temperature | °C |

### ecoMAX 850i Parameters
| Parameter ID | Name | Description |
|-------------|------|-------------|
| 2057 | CWU_WORK_MODE | CWU work mode |
| 2050 | WORK_MODE_H_1 | Heating circuit 1 work mode |
| 2051 | WORK_MODE_H_2 | Heating circuit 2 work mode |
| 2052 | WORK_MODE_H_3 | Heating circuit 3 work mode |
| 2053 | WORK_MODE_H_4 | Heating circuit 4 work mode |
| 2054 | WORK_MODE_H_5 | Heating circuit 5 work mode |
| 2055 | WORK_MODE_H_6 | Heating circuit 6 work mode |

## Data Structures

### Parameter Object
```json
{
  "value": "numeric_value",
  "min": "minimum_value", 
  "max": "maximum_value",
  "unit": "unit_id",
  "mult": "multiplier",
  "sec": "section_number",
  "pos": "position_in_section",
  "edit": "boolean_editable"
}
```

### Device Object
```json
{
  "uid": "device_unique_id",
  "label": "device_name",
  "time": "last_update_timestamp",
  "serviceParamsEdit": "boolean",
  "state": "device_state",
  "protocolType": "protocol_type",
  "controllerID": "controller_id",
  "softVer": "software_version",
  "moduleAVer": "module_a_version",
  "modulePanelVer": "panel_version"
}
```

## Error Handling

### Common Error Responses
```json
{
  "error": "error_message"
}
```

### HTTP Status Codes
- `200` - Success
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `500` - Internal Server Error

## Authentication

### Service Password
- Used for accessing service-level parameters
- SHA-512 hashed
- 4-character minimum (padded with zeros)

### ET Service Password
- Used for ecoTronic device access
- Device-specific passwords

## Rate Limiting
- No explicit rate limiting documented
- Recommended: 1 request per second per device

## Best Practices

### Error Handling
1. Always check for error responses
2. Implement retry logic for network failures
3. Handle authentication failures gracefully

### Data Polling
1. Use appropriate polling intervals (30-60 seconds)
2. Implement exponential backoff for failures
3. Respect device capabilities

### Parameter Updates
1. Validate parameter ranges before sending
2. Check device state before updates
3. Implement confirmation for critical changes

## Integration Examples

### Python Example
```python
import requests
import hashlib

class EconetAPI:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.username = username
        self.password = password
        self.session = requests.Session()
    
    def get_devices(self):
        response = self.session.get(f"{self.base_url}/getDevices")
        return response.json()
    
    def get_device_params(self, uid):
        response = self.session.get(f"{self.base_url}/getDeviceParams?uid={uid}")
        return response.json()
    
    def set_parameter(self, uid, param_name, value):
        response = self.session.get(
            f"{self.base_url}/newParam?uid={uid}&newParamName={param_name}&newParamValue={value}"
        )
        return response.json()
```

### JavaScript Example
```javascript
class EconetController {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
    }
    
    async getDevices() {
        const response = await fetch(`${this.baseUrl}/getDevices`);
        return await response.json();
    }
    
    async getDeviceParams(uid) {
        const response = await fetch(`${this.baseUrl}/getDeviceParams?uid=${uid}`);
        return await response.json();
    }
    
    async setParameter(uid, paramName, value) {
        const response = await fetch(
            `${this.baseUrl}/newParam?uid=${uid}&newParamName=${paramName}&newParamValue=${value}`
        );
        return await response.json();
    }
}
```

## Security Considerations

1. **HTTPS Required**: Always use HTTPS for production
2. **Password Security**: Store passwords securely, use SHA-512 hashing
3. **Access Control**: Implement proper access control for service parameters
4. **Input Validation**: Validate all input parameters
5. **Error Information**: Don't expose sensitive information in error messages

## Troubleshooting

### Common Issues

1. **Authentication Failures**
   - Check password format and hashing
   - Verify device UID
   - Check service access permissions

2. **Parameter Update Failures**
   - Validate parameter ranges
   - Check device state
   - Verify parameter editability

3. **Connection Issues**
   - Check network connectivity
   - Verify device is online
   - Check firewall settings

### Debug Information
- Enable debug logging in your implementation
- Monitor API response times
- Track parameter update success rates

## Version History

- **v1.0** - Initial documentation based on JavaScript analysis
- **v1.1** - Added parameter mappings and device types
- **v1.2** - Added security considerations and best practices

## References

- [ecoNET-300 Home Assistant Integration](https://github.com/jontofront/ecoNET-300-Home-Assistant-Integration)
- [Official JavaScript Implementation](https://github.com/jontofront/stuff)
- [PLUM Heating Systems](https://www.plum.pl/)

---

*This documentation is based on analysis of the official JavaScript implementation and may be updated as the API evolves.* 

## Docs and Fixtures

### Docs
- `docs/`

### Fixtures
- `tests/fixtures/ecoMAX810P-L/API_V2/` 