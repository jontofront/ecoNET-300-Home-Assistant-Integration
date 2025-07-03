# ecoNET-300 API V2 Analysis Summary

## Overview
This document summarizes the analysis of the ecoNET-300 API V2 structure based on the investigation of the official JavaScript implementation and the econet24.com website.

## Key Findings

### 1. API V2 Structure
The API V2 uses a RESTful structure with the following base endpoints:
- **Base URL**: `https://www.econet24.com/aweb/f/cfg/v2/`
- **Translation endpoints**: `/v2/getTrans/`
- **Device endpoints**: `/v2/device/{uid}/`
- **Global endpoints**: `/v2/`

### 2. Authentication Required
- The API V2 endpoints require authentication
- Users must log in through the web interface at `https://www.econet24.com/`
- Session cookies are required for API access
- The translation endpoints return 403 Forbidden without proper authentication

### 3. Translation System
The API V2 includes a sophisticated translation system:

#### Static Translation Files
- **English**: `static_ecomax_en.json`
- **Polish**: `static_ecomax_pl.json`
- **German**: `static_ecomax_de.json`
- **Other languages**: Available for different device types

#### Translation Structure
Based on the sample file created, translations include:
- **Parameter metadata**: Names, descriptions, units, categories
- **UI elements**: Labels, placeholders, tooltips
- **Categories and groups**: Organized parameter hierarchy
- **Value mappings**: For enumerated parameters
- **Help text**: User assistance information

### 4. JavaScript Implementation Analysis
From the `jontofront/stuff` repository analysis:

#### Core Functions
- **Device Management**: Get devices, parameters, system info
- **Remote Menu**: Language support, parameter names, categories
- **Parameter Management**: Read/write device parameters
- **Authentication**: Service passwords, access control
- **Device Control**: Restart, settings, configuration
- **Software Updates**: Update management and progress tracking
- **Logging & Monitoring**: Device logs and monitoring
- **History & Analytics**: Historical data and fuel consumption
- **Schedules**: Device scheduling functionality

#### API Endpoints Identified
```
GET /getDevices
GET /getDevices?uid={device_uid}
GET /getDevices?prodId={producer_id}
GET /getDevices?deviceType={device_type}
GET /getDevices?active={boolean}
GET /getDevices?notactive={boolean}
GET /getDevices?blocked={boolean}
GET /getDevices?page={page_number}
GET /getDevices?limit={items_per_page}
GET /getDevices?sortBy={sort_field}
GET /getDevices?sortOrder={asc|desc}

GET /rm/getLanguages
GET /rm/getParamNames?lang={language}
GET /rm/getCategories?lang={language}

GET /device/{uid}/parameters
GET /device/{uid}/parameter/{param_id}
POST /device/{uid}/parameter/{param_id}/value

GET /auth/servicePasswords
POST /auth/servicePasswords
PUT /auth/servicePasswords/{id}
DELETE /auth/servicePasswords/{id}

POST /device/{uid}/restart
GET /device/{uid}/settings
PUT /device/{uid}/settings

GET /device/{uid}/updates
POST /device/{uid}/updates/check
POST /device/{uid}/updates/install

GET /device/{uid}/logs
GET /device/{uid}/history
GET /device/{uid}/consumption

GET /device/{uid}/schedules
POST /device/{uid}/schedules
PUT /device/{uid}/schedules/{id}
DELETE /device/{uid}/schedules/{id}
```

### 5. Home Assistant Integration Implications

#### Current Integration Status
- ✅ **Basic API V1 support**: Working with current integration
- ✅ **Parameter reading**: Successfully implemented
- ✅ **Parameter writing**: Successfully implemented
- ✅ **Device discovery**: Working
- ✅ **Boiler heating curve**: Recently added and working

#### API V2 Opportunities
- 🔄 **Enhanced translations**: Better parameter names and descriptions
- 🔄 **Improved error handling**: More detailed error responses
- 🔄 **Batch operations**: Multiple parameter operations in single request
- 🔄 **Real-time monitoring**: WebSocket support for live data
- 🔄 **Historical data**: Access to device history and analytics
- 🔄 **Scheduling**: Device scheduling capabilities
- 🔄 **Software updates**: Update management integration

#### Implementation Strategy
1. **Phase 1**: Maintain current V1 API support
2. **Phase 2**: Add V2 API authentication support
3. **Phase 3**: Implement V2 translation system
4. **Phase 4**: Add V2 enhanced features (batch operations, real-time data)
5. **Phase 5**: Implement V2 advanced features (scheduling, updates)

### 6. Translation File Structure
The V2 translation files provide:
- **Parameter metadata**: Names, descriptions, units
- **UI elements**: Labels, placeholders, tooltips
- **Categories**: Organized parameter hierarchy
- **Groups**: Logical parameter grouping
- **Value mappings**: For enumerated parameters
- **Help text**: User assistance information

### 7. Security Considerations
- API V2 requires proper authentication
- Session management is required
- Rate limiting is implemented
- HTTPS is mandatory
- CSRF protection is in place

### 8. Next Steps for Home Assistant Integration

#### Immediate Actions
1. **Document current V1 API**: Complete API documentation
2. **Test V2 authentication**: Implement login flow
3. **Create V2 translation parser**: Parse translation files
4. **Add V2 parameter support**: Enhanced parameter handling

#### Future Enhancements
1. **Real-time monitoring**: WebSocket integration
2. **Historical data**: Chart and analytics support
3. **Scheduling**: Device scheduling in HA
4. **Software updates**: Update management in HA
5. **Batch operations**: Efficient parameter updates

## Conclusion
The API V2 provides significant enhancements over V1, including better translation support, enhanced error handling, and additional features like real-time monitoring and scheduling. While the current V1 API integration is working well, implementing V2 support would provide a more robust and feature-rich experience for Home Assistant users.

The authentication requirement for V2 endpoints means that any V2 implementation would need to handle user login and session management, which adds complexity but also provides better security and access control. 