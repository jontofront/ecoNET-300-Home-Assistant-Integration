# Boiler Control Feature

## Overview

The boiler control feature allows you to turn the ecoNET-300 boiler ON and OFF through Home Assistant using a switch entity.

## Implementation Details

### API Endpoint
- **URL**: `/econet/newParam`
- **Method**: GET
- **Authentication**: Required

### Parameters
- **newParamName**: `BOILER_CONTROL`
- **newParamValue**: `0` (OFF) or `1` (ON)

### Working API Calls

#### Turn Boiler ON
```
GET http://DEVICE_IP/econet/newParam?newParamName=BOILER_CONTROL&newParamValue=1
```

**Expected Response:**
```json
{
  "paramName": "BOILER_CONTROL",
  "paramValue": 1,
  "result": "OK"
}
```

#### Turn Boiler OFF
```
GET http://DEVICE_IP/econet/newParam?newParamName=BOILER_CONTROL&newParamValue=0
```

**Expected Response:**
```json
{
  "paramName": "BOILER_CONTROL",
  "paramValue": 0,
  "result": "OK"
}
```

## Home Assistant Integration

### Switch Entity
- **Entity ID**: `switch.boiler_on_off`
- **Name**: "Boiler On/Off"
- **Icon**: `mdi:fire`
- **States**: ON/OFF

### State Detection
The switch reads the current boiler state from the `mode` parameter:
- `mode = 0` → Switch shows OFF
- `mode = 1-25` → Switch shows ON

### Control Actions
- **Turn ON**: Sets `BOILER_CONTROL=1`
- **Turn OFF**: Sets `BOILER_CONTROL=0`

## Testing

### Browser Console Test
```javascript
// Test turning boiler ON
fetch('/econet/newParam?newParamName=BOILER_CONTROL&newParamValue=1')
  .then(response => response.json())
  .then(data => console.log('ON response:', data));

// Test turning boiler OFF
fetch('/econet/newParam?newParamName=BOILER_CONTROL&newParamValue=0')
  .then(response => response.json())
  .then(data => console.log('OFF response:', data));
```

### cURL Test
```bash
# Turn ON
curl "http://DEVICE_IP/econet/newParam?newParamName=BOILER_CONTROL&newParamValue=1"

# Turn OFF
curl "http://DEVICE_IP/econet/newParam?newParamName=BOILER_CONTROL&newParamValue=0"
```

## Troubleshooting

### Common Issues

1. **"NOTYPE" Error**
   - **Cause**: Wrong parameter name or endpoint
   - **Solution**: Use `BOILER_CONTROL` parameter with `/econet/newParam` endpoint

2. **"UNAUTHORIZED" Error**
   - **Cause**: Missing or incorrect authentication
   - **Solution**: Ensure proper login to the ecoNET-300 web interface

3. **Switch State Not Updating**
   - **Cause**: Coordinator not refreshing data
   - **Solution**: Check if `mode` parameter is available in coordinator data

### Debug Logs
Enable debug logging in Home Assistant:
```yaml
logger:
  default: info
  logs:
    custom_components.econet300: debug
```

## Files Modified

1. **`custom_components/econet300/switch.py`**
   - Added boiler control switch implementation
   - Uses `BOILER_CONTROL` parameter for control
   - Uses `mode` parameter for state detection

2. **`custom_components/econet300/api.py`**
   - Updated `set_param` method to use correct endpoint
   - Changed from `/econet/rmCurrNewParam` to `/econet/newParam`
   - Changed parameter name from `newParamKey` to `newParamName`

3. **Translation Files**
   - Added English and Polish translations for "Boiler On/Off"

## Verification

To verify the implementation works:

1. **Test API directly** using browser console or cURL
2. **Check Home Assistant logs** for successful API calls
3. **Verify switch state** updates correctly after control actions
4. **Test both ON and OFF** operations

## Notes

- The `BOILER_CONTROL` parameter is the correct way to control boiler ON/OFF
- The `mode` parameter is read-only and shows current operation state
- Authentication is required for all API operations
- The switch provides a simple ON/OFF interface for boiler control 