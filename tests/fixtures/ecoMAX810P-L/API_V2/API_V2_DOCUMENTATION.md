# ecoNET-300 API V2 Documentation

## Overview
This document provides comprehensive documentation of the ecoNET-300 API V2 endpoints and device information based on analysis of the official JavaScript implementation and the new API structure.

## Base URL Structure
The API V2 uses a RESTful structure with the following base endpoints:
- Device-specific endpoints: `{base_url}/v2/device/{device_uid}/`
- Global endpoints: `{base_url}/v2/`
- Translation endpoints: `{base_url}/v2/getTrans/`

## Core API V2 Endpoints

### Translation and Localization

#### Get Static Translations
```
GET /v2/getTrans/static_ecomax_en.json
GET /v2/getTrans/static_ecomax_pl.json
GET /v2/getTrans/static_ecomax_de.json
```
**Purpose:** Retrieve static translation files for different languages
**Response:** JSON object with parameter names, descriptions, and UI labels

#### Get Dynamic Translations
```
GET /v2/getTrans/dynamic/{device_type}_{language}.json
```
**Purpose:** Retrieve device-specific dynamic translations
**Parameters:**
- `device_type` (string) - Device model (ecomax, ecosol, etc.)
- `language` (string) - Language code (en, pl, de, etc.)

### Device Management V2

#### Get Devices Enhanced
```
GET /v2/getDevices
```
**Parameters:**
- `active` (boolean) - Show active devices
- `notactive` (boolean) - Show inactive devices  
- `blocked` (boolean) - Show blocked devices
- `deviceType` (string) - Filter by device type
- `uid` (string) - Filter by device UID
- `prodId` (string) - Filter by producer ID
- `page` (integer) - Page number for pagination
- `limit` (integer) - Items per page
- `sortBy` (string) - Sort field
- `sortOrder` (string) - Sort order (asc/desc)

#### Get Device Parameters V2
```
GET /v2/device/{uid}/parameters
```
**Parameters:**
- `category` (string) - Parameter category filter
- `group` (string) - Parameter group filter
- `type` (string) - Parameter type filter
- `readonly` (boolean) - Show read-only parameters
- `writable` (boolean) - Show writable parameters

#### Get Parameter Details V2
```
GET /v2/device/{uid}/parameter/{param_id}
```
**Response includes:**
- Parameter metadata
- Current value
- Limits and constraints
- Unit of measurement
- Description and help text
- Translation keys

### Remote Menu V2

#### Get Language Support V2
```
GET /v2/rm/getLanguages
```
**Response:** Enhanced language support with additional metadata

#### Get Parameter Names V2
```
GET /v2/rm/getParamNames
```
**Parameters:**
- `lang` (string) - Language code
- `deviceType` (string) - Device type filter
- `category` (string) - Category filter

#### Get Categories V2
```
GET /v2/rm/getCategories
```
**Parameters:**
- `lang` (string) - Language code
- `deviceType` (string) - Device type filter
- `parent` (string) - Parent category filter

### Parameter Management V2

#### Read Parameter V2
```
GET /v2/device/{uid}/parameter/{param_id}/value
```
**Response:**
```json
{
  "value": 25.5,
  "unit": "°C",
  "timestamp": "2024-01-01T12:00:00Z",
  "quality": "good",
  "status": "ok"
}
```

#### Write Parameter V2
```
POST /v2/device/{uid}/parameter/{param_id}/value
```
**Request Body:**
```json
{
  "value": 26.0,
  "validate": true,
  "confirm": false
}
```

#### Batch Parameter Operations V2
```
POST /v2/device/{uid}/parameters/batch
```
**Request Body:**
```json
{
  "operations": [
    {
      "param_id": "tempCWUSet",
      "action": "read"
    },
    {
      "param_id": "tempCOSet", 
      "action": "write",
      "value": 75.0
    }
  ]
}
```

### Authentication V2

#### Service Password Management V2
```
GET /v2/auth/servicePasswords
POST /v2/auth/servicePasswords
PUT /v2/auth/servicePasswords/{id}
DELETE /v2/auth/servicePasswords/{id}
```

#### Access Control V2
```
GET /v2/auth/accessControl
POST /v2/auth/accessControl
PUT /v2/auth/accessControl/{id}
DELETE /v2/auth/accessControl/{id}
```

### Device Control V2

#### Restart Device V2
```
POST /v2/device/{uid}/restart
```
**Request Body:**
```json
{
  "type": "soft", // or "hard"
  "confirm": true,
  "reason": "Maintenance"
}
```

#### Device Settings V2
```
GET /v2/device/{uid}/settings
PUT /v2/device/{uid}/settings
```

#### Configuration Management V2
```
GET /v2/device/{uid}/config
POST /v2/device/{uid}/config/backup
POST /v2/device/{uid}/config/restore
```

### Software Updates V2

#### Update Management V2
```
GET /v2/device/{uid}/updates
POST /v2/device/{uid}/updates/check
POST /v2/device/{uid}/updates/install
```

#### Update Progress V2
```
GET /v2/device/{uid}/updates/progress
```

### Logging & Monitoring V2

#### Device Logs V2
```
GET /v2/device/{uid}/logs
```
**Parameters:**
- `level` (string) - Log level filter
- `startDate` (string) - Start date filter
- `endDate` (string) - End date filter
- `limit` (integer) - Number of log entries

#### Real-time Monitoring V2
```
GET /v2/device/{uid}/monitor
```
**Response:** WebSocket connection for real-time data

### History & Analytics V2

#### Historical Data V2
```
GET /v2/device/{uid}/history
```
**Parameters:**
- `parameter` (string) - Parameter ID
- `startDate` (string) - Start date
- `endDate` (string) - End date
- `interval` (string) - Data interval (1m, 5m, 1h, 1d)

#### Fuel Consumption V2
```
GET /v2/device/{uid}/consumption
```
**Parameters:**
- `type` (string) - Consumption type (fuel, electricity, etc.)
- `period` (string) - Time period (day, week, month, year)

### Schedules V2

#### Schedule Management V2
```
GET /v2/device/{uid}/schedules
POST /v2/device/{uid}/schedules
PUT /v2/device/{uid}/schedules/{id}
DELETE /v2/device/{uid}/schedules/{id}
```

#### Schedule Templates V2
```
GET /v2/schedules/templates
POST /v2/schedules/templates
```

## Response Formats

### Standard Response V2
```json
{
  "success": true,
  "data": {},
  "meta": {
    "timestamp": "2024-01-01T12:00:00Z",
    "version": "2.0",
    "requestId": "uuid"
  },
  "errors": []
}
```

### Error Response V2
```json
{
  "success": false,
  "data": null,
  "meta": {
    "timestamp": "2024-01-01T12:00:00Z",
    "version": "2.0",
    "requestId": "uuid"
  },
  "errors": [
    {
      "code": "PARAMETER_NOT_FOUND",
      "message": "Parameter not found",
      "details": "Parameter ID 123 does not exist"
    }
  ]
}
```

## Authentication

### API Key Authentication
```
Authorization: Bearer {api_key}
```

### Session Authentication
```
Cookie: session={session_token}
```

## Rate Limiting
- **Standard:** 100 requests per minute
- **Premium:** 1000 requests per minute
- **Enterprise:** 10000 requests per minute

## WebSocket Support
The API V2 supports WebSocket connections for real-time data:
```
wss://api.econet24.com/v2/ws/device/{uid}
```

## Migration from V1
- All V1 endpoints are deprecated but still supported
- V2 provides enhanced functionality and better error handling
- Migration guide available at `/v2/migration`

## SDK Support
- JavaScript SDK available
- Python SDK in development
- REST API documentation with OpenAPI 3.0 specification 