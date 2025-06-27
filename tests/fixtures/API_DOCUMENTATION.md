# ecoNET-300 API Documentation

## Boiler Control API

### Boiler ON/OFF Control

The boiler can be controlled using the `BOILER_CONTROL` parameter through the `/econet/newParam` endpoint.

#### Endpoint
```
GET /econet/newParam
```

#### Parameters
- `newParamName`: The parameter name (always "BOILER_CONTROL")
- `newParamValue`: The desired state (0 = OFF, 1 = ON)

#### Examples

**Turn Boiler ON:**
```
GET http://DEVICE_IP/econet/newParam?newParamName=BOILER_CONTROL&newParamValue=1
```

**Response:**
```json
{
  "paramName": "BOILER_CONTROL",
  "paramValue": 1,
  "result": "OK"
}
```

**Turn Boiler OFF:**
```
GET http://DEVICE_IP/econet/newParam?newParamName=BOILER_CONTROL&newParamValue=0
```

**Response:**
```json
{
  "paramName": "BOILER_CONTROL",
  "paramValue": 0,
  "result": "OK"
}
```

#### Error Responses

**Invalid Parameter:**
```json
{
  "result": "NOTYPE"
}
```

**Authentication Error:**
```json
{
  "result": "UNAUTHORIZED"
}
```

## Boiler State Reading

### Current Boiler Mode

The current boiler state can be read from the `mode` parameter in the `/econet/regParams` endpoint.

#### Mode Values
- `0`: OFF
- `1`: Fire up
- `2`: Operation
- `3`: Work
- `4`: Supervision
- `5`: Halted/Paused
- `6`: Stop
- `7`: Burning off
- `8`: Manual
- `9`: Alarm
- `10`: Unsealing
- `11`: Chimney
- `12`: Stabilization
- `13`: No transmission

#### Example Response
```json
{
  "curr": {
    "mode": 3,
    "boilerPower": 50,
    "tempCO": 65.5,
    ...
  }
}
```

## Integration Usage

### Home Assistant Switch Entity

The boiler control is implemented as a switch entity in Home Assistant:

- **Entity ID**: `switch.boiler_on_off`
- **Name**: "Boiler On/Off"
- **States**: ON/OFF
- **Control**: Uses `BOILER_CONTROL` parameter
- **State Reading**: Uses `mode` parameter

### Switch Behavior

1. **Turn ON**: Sets `BOILER_CONTROL=1`
2. **Turn OFF**: Sets `BOILER_CONTROL=0`
3. **State Detection**: 
   - `mode=0` → Switch shows OFF
   - `mode=1-25` → Switch shows ON

## Testing

### Direct API Testing

You can test the API directly in your browser's developer console:

```javascript
// Turn boiler ON
fetch('/econet/newParam?newParamName=BOILER_CONTROL&newParamValue=1')
  .then(response => response.json())
  .then(data => console.log('ON response:', data));

// Turn boiler OFF
fetch('/econet/newParam?newParamName=BOILER_CONTROL&newParamValue=0')
  .then(response => response.json())
  .then(data => console.log('OFF response:', data));
```

### cURL Testing

```bash
# Turn ON
curl "http://DEVICE_IP/econet/newParam?newParamName=BOILER_CONTROL&newParamValue=1"

# Turn OFF
curl "http://DEVICE_IP/econet/newParam?newParamName=BOILER_CONTROL&newParamValue=0"
```

## Notes

- The `BOILER_CONTROL` parameter is the correct way to control the boiler ON/OFF state
- The `mode` parameter is read-only and reflects the current boiler operation mode
- Authentication is required for all API calls
- The API returns JSON responses with a `result` field indicating success/failure 