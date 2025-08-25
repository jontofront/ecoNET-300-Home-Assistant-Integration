# ecoMAX360 Device Overview

## Summary
The **ecoMAX360** is an intelligent pellet boiler system with advanced controls and comprehensive monitoring capabilities. This device is **fully implemented and working** in the ecoNET-300 Home Assistant integration, providing real-time monitoring and control of heating system parameters.

## Device Capabilities

### Core Features
- **Intelligent Pellet Boiler Control** - Advanced pellet boiler management with lambda sensor support
- **Multi-Circuit Heating** - Support for up to 7 independent heating circuits
- **Buffer Tank Integration** - Comprehensive buffer tank monitoring and control
- **Weather Compensation** - External temperature sensor integration for adaptive heating
- **Advanced Scheduling** - Multi-zone temperature control with time-based programming
- **Real-time Monitoring** - Continuous monitoring of all critical system parameters

### Heating Circuits
- **Circuit 1-7** - Independent heating circuits with individual temperature control
- **Thermostat Integration** - Each circuit supports thermostat temperature monitoring
- **Base/Comfort/Eco Modes** - Multiple temperature setpoints per circuit
- **Automatic Regulation** - Intelligent heating circuit management

### Temperature Monitoring
- **Boiler Temperature** - Core boiler temperature monitoring
- **Buffer Tank Temperatures** - Upper and lower buffer tank monitoring
- **Circuit Temperatures** - Individual circuit temperature tracking
- **External Temperature** - Weather compensation sensor
- **Clutch Temperature** - Mechanical system temperature monitoring
- **DHW Temperature** - Domestic hot water temperature

## API Support

### Supported Endpoints
- **`sysParams`** ✅ **Fully Supported** - System parameters and device information
- **`regParams`** ✅ **Fully Supported** - Register parameters and current values
- **`regParamsData`** ✅ **Fully Supported** - Parameter metadata and configuration
- **`rmCurrentDataParams`** ⚠️ **Limited Support** - Real-time data (endpoint error in test fixtures)

### Data Availability
- **System Information** - Software versions, module status, network configuration
- **Parameter Values** - Current values for all configurable parameters
- **Parameter Metadata** - Min/max limits, units, descriptions, editability
- **Real-time Data** - Live sensor readings and system status

## Home Assistant Integration

### Current Implementation Status
- **✅ Fully Implemented** - All core functionality is working
- **✅ Device Detection** - Automatic detection via controller ID
- **✅ Sensor Creation** - All available sensors are automatically created
- **✅ Parameter Mapping** - Comprehensive parameter-to-entity mapping
- **⚠️ Limited Real-time Data** - Some real-time endpoints may have issues

### Available Entities
- **Temperature Sensors** - All temperature readings (boiler, circuits, buffer, external)
- **Status Sensors** - System status, pump states, operation modes
- **Configuration Sensors** - Software versions, module information
- **Setpoint Sensors** - Temperature setpoints and control parameters

### Integration Benefits
1. **Real-time Monitoring** - Live temperature and status information
2. **Automation Ready** - Full Home Assistant automation support
3. **Dashboard Integration** - Beautiful, responsive dashboards
4. **Multi-zone Control** - Independent circuit temperature management
5. **Weather Integration** - External temperature sensor for smart heating
6. **Buffer Management** - Comprehensive buffer tank monitoring

## Device Identification

### Controller ID
- **Primary ID**: `ecoMAX360i`
- **Alternative IDs**: `ecoMAX360`, `ecoMAX360i`

### Software Versions
- **Module Panel**: S003.68_1.82
- **ecoSRV**: 3.2.3842
- **Module A**: S002.28

### Supported Protocols
- **ecoNET Protocol** - Primary communication protocol
- **REST API** - JSON-based parameter access
- **Real-time Updates** - Continuous data streaming

## Current Limitations

### Known Issues
- **Real-time Data Endpoint** - Some devices may have communication issues
- **Parameter Editability** - Some parameters may be read-only
- **Circuit Support** - Not all 7 circuits may be active on all devices

### Workarounds
- **Parameter Polling** - Regular parameter updates provide near real-time data
- **Status Monitoring** - System status provides operational information
- **Configuration Backup** - Parameter metadata ensures proper entity creation

## Getting Started

### Installation
1. **Install HACS** (Home Assistant Community Store)
2. **Add Repository** - ecoNET-300 integration
3. **Install Integration** - Automatic device detection
4. **Configure Device** - Enter IP address and credentials
5. **Verify Entities** - Check that all sensors are created

### Configuration
- **IP Address** - Device network address
- **Username** - Device login credentials
- **Password** - Device authentication
- **Scan Interval** - Data update frequency (default: 30 seconds)

### First Steps
1. **Check Device Status** - Verify connection and data flow
2. **Review Sensors** - Explore available temperature and status sensors
3. **Create Dashboard** - Build custom monitoring dashboard
4. **Set Up Automations** - Configure temperature-based automations
5. **Monitor Performance** - Track heating efficiency and system health

## Support and Documentation

### Additional Resources
- **Parameters Guide** - Detailed parameter descriptions and values
- **API Documentation** - Complete API endpoint reference
- **Home Assistant Guide** - Integration setup and configuration
- **Implementation Details** - Technical implementation information

### Getting Help
- **GitHub Issues** - Report bugs and request features
- **Community Support** - Home Assistant community forums
- **Documentation** - Comprehensive device documentation
- **Test Fixtures** - Sample data for development and testing

---

*Last Updated: December 2024*  
*Status: Fully Implemented and Working*  
*Integration Version: ecoNET-300 v1.1.8*
