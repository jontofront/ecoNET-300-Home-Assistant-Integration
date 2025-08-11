# ecoMAX360 Home Assistant Integration Guide

## Overview
The ecoMAX360 is **fully implemented and working** in the ecoNET-300 Home Assistant integration. This guide covers installation, configuration, available entities, and advanced features for integrating your ecoMAX360 device with Home Assistant.

## Installation

### Prerequisites
- **Home Assistant**: Version 2025.2.2 or newer
- **HACS**: Home Assistant Community Store installed
- **Network Access**: ecoMAX360 accessible on your network
- **Credentials**: Username and password for the device

### Installation Steps

#### 1. Install HACS (if not already installed)
1. Go to **Settings** → **Add-ons** → **Add-on Store**
2. Search for "HACS" and install it
3. Follow the HACS setup wizard
4. Restart Home Assistant

#### 2. Add the ecoNET-300 Repository
1. Open **HACS** → **Integrations**
2. Click the **+** button in the bottom right
3. Search for "ecoNET-300"
4. Click **Download**
5. Restart Home Assistant

#### 3. Add the Integration
1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "ecoNET-300"
4. Click on the integration
5. Enter your device details:
   - **IP Address**: Your ecoMAX360's network address
   - **Username**: Device login username
   - **Password**: Device login password
   - **Scan Interval**: Data update frequency (default: 30 seconds)

#### 4. Verify Installation
1. Check the integration status shows "Connected"
2. Verify entities are being created
3. Check the logs for any errors

## Configuration

### Basic Configuration
```yaml
# Example configuration.yaml entry
econet300:
  host: "192.168.1.100"  # Your ecoMAX360 IP address
  username: "admin"       # Device username
  password: "password"    # Device password
  scan_interval: 30       # Update frequency in seconds
```

### Advanced Configuration
```yaml
# Advanced configuration options
econet300:
  host: "192.168.1.100"
  username: "admin"
  password: "password"
  scan_interval: 30
  timeout: 10             # API request timeout
  retry_count: 3          # Retry attempts on failure
  verify_ssl: false       # SSL verification (if needed)
```

### Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `host` | Required | Device IP address or hostname |
| `username` | Required | Device login username |
| `password` | Required | Device login password |
| `scan_interval` | 30 | Data update frequency in seconds |
| `timeout` | 10 | API request timeout in seconds |
| `retry_count` | 3 | Number of retry attempts on failure |
| `verify_ssl` | true | SSL certificate verification |

## Available Entities

### Temperature Sensors
The integration automatically creates temperature sensors for all available parameters:

#### Circuit Temperature Sensors
- **`sensor.temp_circuit_1`** - Circuit 1 temperature
- **`sensor.temp_circuit_2`** - Circuit 2 temperature  
- **`sensor.temp_circuit_3`** - Circuit 3 temperature
- **`sensor.temp_circuit_4`** - Circuit 4 temperature
- **`sensor.temp_circuit_5`** - Circuit 5 temperature
- **`sensor.temp_circuit_6`** - Circuit 6 temperature
- **`sensor.temp_circuit_7`** - Circuit 7 temperature

#### System Temperature Sensors
- **`sensor.temp_clutch`** - Clutch temperature
- **`sensor.temp_wthr`** - Weather temperature
- **`sensor.temp_cwu`** - DHW temperature
- **`sensor.temp_bufor_up`** - Upper buffer temperature
- **`sensor.temp_bufor_down`** - Lower buffer temperature

#### Thermostat Temperature Sensors
- **`sensor.circuit_2_thermostat_temp`** - Circuit 2 thermostat temperature
- **`sensor.circuit_3_thermostat_temp`** - Circuit 3 thermostat temperature
- **`sensor.circuit_4_thermostat_temp`** - Circuit 4 thermostat temperature
- **`sensor.circuit_5_thermostat_temp`** - Circuit 5 thermostat temperature
- **`sensor.circuit_6_thermostat_temp`** - Circuit 6 thermostat temperature
- **`sensor.circuit_7_thermostat_temp`** - Circuit 7 thermostat temperature

### Status Sensors
- **`sensor.circuit_1_thermostat`** - Circuit 1 thermostat status
- **`sensor.heating_work_state_pump_4`** - Pump 4 work state
- **`sensor.heating_upper_temp`** - Upper heating temperature

### Configuration Sensors
- **`sensor.module_panel_soft_ver`** - Panel software version
- **`sensor.ecosrv_soft_ver`** - ecoSRV software version
- **`sensor.module_a_soft_ver`** - Module A software version
- **`sensor.ecosrv_port`** - ecoSRV port
- **`sensor.main_srv`** - Main server status

## Advanced Configuration

### Custom Entity Names
You can customize entity names in the Home Assistant interface:

1. Go to **Settings** → **Devices & Services**
2. Click on the ecoNET-300 integration
3. Click **Configure**
4. Modify entity names as needed
5. Click **Submit**

### Entity Customization
```yaml
# Example customize.yaml entries
sensor.temp_circuit_1:
  friendly_name: "Living Room Temperature"
  icon: mdi:thermometer

sensor.temp_circuit_2:
  friendly_name: "Bedroom Temperature"
  icon: mdi:thermometer

sensor.temp_wthr:
  friendly_name: "Outside Temperature"
  icon: mdi:weather-partly-cloudy
```

### Scan Interval Optimization
- **Frequent Updates**: 15-30 seconds for active monitoring
- **Standard Monitoring**: 30-60 seconds for normal operation
- **Background Monitoring**: 60-300 seconds for passive monitoring

## Automation Examples

### Temperature-Based Heating Control
```yaml
# Automatically adjust heating based on outside temperature
automation:
  - alias: "Adjust Heating for Cold Weather"
    trigger:
      platform: numeric_state
      entity_id: sensor.temp_wthr
      below: 5
    action:
      - service: input_number.set_value
        target:
          entity_id: input_number.heating_setpoint
        data:
          value: 22
```

### Circuit Temperature Monitoring
```yaml
# Alert when circuit temperatures are too low
automation:
  - alias: "Low Circuit Temperature Alert"
    trigger:
      platform: numeric_state
      entity_id: sensor.temp_circuit_1
      below: 15
    action:
      - service: notify.mobile_app
        data:
          message: "Circuit 1 temperature is too low: {{ states('sensor.temp_circuit_1') }}°C"
```

### Buffer Tank Management
```yaml
# Monitor buffer tank efficiency
automation:
  - alias: "Buffer Tank Efficiency Check"
    trigger:
      platform: time_pattern
      hours: "*/2"
    action:
      - service: input_text.set_value
        target:
          entity_id: input_text.buffer_efficiency_log
        data:
          value: "Buffer Up: {{ states('sensor.temp_bufor_up') }}°C, Buffer Down: {{ states('sensor.temp_bufor_down') }}°C"
```

### Weather Compensation
```yaml
# Adaptive heating based on weather
automation:
  - alias: "Weather Compensation Heating"
    trigger:
      platform: numeric_state
      entity_id: sensor.temp_wthr
      below: 0
    action:
      - service: input_number.set_value
        target:
          entity_id: input_number.heating_setpoint
        data:
          value: 24
```

## Dashboard Configuration

### Basic Monitoring Dashboard
```yaml
# Example dashboard configuration
views:
  - title: "ecoMAX360 Monitoring"
    path: ecomax360
    type: custom:grid-layout
    badges: []
    cards:
      - type: vertical-stack
        cards:
          - type: entities
            title: "Circuit Temperatures"
            entities:
              - entity: sensor.temp_circuit_1
                name: "Circuit 1"
              - entity: sensor.temp_circuit_2
                name: "Circuit 2"
              - entity: sensor.temp_circuit_3
                name: "Circuit 3"
          
          - type: entities
            title: "System Temperatures"
            entities:
              - entity: sensor.temp_clutch
                name: "Clutch"
              - entity: sensor.temp_wthr
                name: "Weather"
              - entity: sensor.temp_cwu
                name: "DHW"
```

### Advanced Dashboard with Charts
```yaml
# Advanced dashboard with historical data
views:
  - title: "ecoMAX360 Advanced"
    path: ecomax360-advanced
    type: custom:grid-layout
    cards:
      - type: custom:mini-graph-card
        title: "Circuit Temperature Trends"
        entities:
          - entity: sensor.temp_circuit_1
            name: "Circuit 1"
          - entity: sensor.temp_circuit_2
            name: "Circuit 2"
        hours_to_show: 24
        points_per_hour: 2
      
      - type: custom:mini-graph-card
        title: "Buffer Tank Temperatures"
        entities:
          - entity: sensor.temp_bufor_up
            name: "Upper Buffer"
          - entity: sensor.temp_bufor_down
            name: "Lower Buffer"
        hours_to_show: 12
        points_per_hour: 4
```

## Troubleshooting

### Common Issues

#### Connection Problems
1. **Check Network Connectivity**
   - Verify the device is accessible from your network
   - Test with ping or browser access
   - Check firewall settings

2. **Authentication Issues**
   - Verify username and password
   - Check for special characters in credentials
   - Try resetting device credentials

3. **API Endpoint Errors**
   - Check device software version
   - Verify API endpoint availability
   - Check integration logs for specific errors

#### Entity Issues
1. **Missing Entities**
   - Restart the integration
   - Check integration logs for errors
   - Verify device parameter support

2. **Entity Values Not Updating**
   - Check scan interval settings
   - Verify network connectivity
   - Check for API rate limiting

3. **Incorrect Values**
   - Verify parameter units
   - Check for data conversion issues
   - Review parameter metadata

### Debug Information

#### Enable Debug Logging
```yaml
# Add to configuration.yaml
logger:
  default: info
  logs:
    custom_components.econet300: debug
```

#### Check Integration Status
1. Go to **Settings** → **Devices & Services**
2. Click on the ecoNET-300 integration
3. Check the **Status** section
4. Review any error messages

#### View Raw Data
1. Go to **Developer Tools** → **States**
2. Search for "econet300" entities
3. Review entity attributes and values
4. Check for any error states

### Getting Help

#### Community Support
- **Home Assistant Community**: [community.home-assistant.io](https://community.home-assistant.io)
- **GitHub Issues**: Report bugs and request features
- **Discord**: Join the Home Assistant Discord server

#### Documentation
- **Integration Documentation**: This guide and related documents
- **API Reference**: Complete API endpoint documentation
- **Test Fixtures**: Sample data for development

#### Log Analysis
When reporting issues, include:
- Home Assistant version
- Integration version
- Device model and software version
- Relevant log entries
- Steps to reproduce the issue

## Performance Optimization

### Network Optimization
- **Local Network**: Ensure device is on the same network
- **Wired Connection**: Use Ethernet when possible
- **Network Quality**: Check for network congestion
- **DNS Resolution**: Use IP addresses instead of hostnames

### Home Assistant Optimization
- **Scan Interval**: Balance between responsiveness and performance
- **Entity Filtering**: Only create needed entities
- **Caching**: Leverage Home Assistant's built-in caching
- **Database**: Regular database maintenance

### Device Optimization
- **Firmware Updates**: Keep device firmware current
- **Network Settings**: Optimize device network configuration
- **Parameter Optimization**: Configure device for efficiency
- **Maintenance**: Regular device maintenance and cleaning

---

*Last Updated: December 2024*  
*Integration Status: Fully Implemented and Working*  
*Home Assistant Version: 2025.2.2+*  
*ecoNET-300 Version: v1.1.8*
