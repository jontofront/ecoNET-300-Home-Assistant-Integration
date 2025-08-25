# ecoSOL500 Home Assistant Integration Guide

## 🏠 **Integration Overview**

The ecoSOL500 provides **seamless integration** with Home Assistant, offering comprehensive solar collector monitoring with 10 sensors that are automatically created and fully functional. This guide covers everything needed for professional solar system integration.

## 🚀 **Integration Benefits**

### **What You Get**
- **10 Professional Sensors**: Complete solar system monitoring
- **Automatic Integration**: No manual setup required
- **Real-time Monitoring**: Live status of all components
- **Multi-language Support**: English and Polish translations
- **Professional Quality**: Industry-standard monitoring capabilities

### **Home Assistant Features**
- **Sensors**: Temperature, status, and performance metrics
- **Real-time Updates**: Live data from solar system
- **History Integration**: Full Home Assistant history support
- **Automation Ready**: Can be used in automations and scripts

---

## 📋 **Prerequisites**

### **Required Components**
- Home Assistant Core 2025.2.2 or newer
- ecoNET-300 Integration (custom component) - **ecoSOL500 fully supported**
- ecoSOL500 device with network access
- Stable network connection to device

### **Network Setup**
- **Device IP**: Configured and accessible
- **Port**: HTTP (80) - no special ports required
- **Authentication**: IP-based access control
- **Firewall**: Allow HTTP access to device IP

---

## 🔧 **Installation & Configuration**

### **1. Install ecoNET-300 Integration**

#### **Option A: HACS Installation (Recommended)**
```yaml
# Add to HACS custom repositories
repositories:
  - name: "ecoNET-300"
    url: "https://github.com/your-repo/ecoNET-300-Home-Assistant-Integration"
    type: "integration"
```

#### **Option B: Manual Installation**
```bash
# Copy custom_components/econet300 to your Home Assistant config directory
cp -r custom_components/econet300 /config/custom_components/
```

### **2. Restart Home Assistant**
```yaml
# Restart required after installation
# Go to Configuration > System > Restart
```

### **3. Add Integration**
```yaml
# Go to Configuration > Devices & Services > Add Integration
# Search for "ecoNET-300" and select it
# ecoSOL500 will be automatically detected when connected
```

---

## ⚙️ **Configuration**

### **Basic Configuration**
```yaml
# Configuration flow will prompt for:
name: "ecoSOL500 Solar System"        # Friendly name
host: "192.168.1.100"                 # Device IP address
scan_interval: 30                      # Update frequency (seconds)
```

### **Advanced Configuration**
```yaml
# Additional configuration options
econet300:
  host: "192.168.1.100"
  name: "ecoSOL500 Solar System"
  scan_interval: 30
  timeout: 10
  retry_count: 3
  enable_debug: false
```

---

## 📊 **Available Entities**

### **Temperature Sensors**

#### **Collector Temperature Sensors**
```yaml
# Automatically created sensors
sensor.econet_collector_temperature:
  friendly_name: "Collector Temperature"
  unit_of_measurement: "°C"
  device_class: "temperature"
  
sensor.econet_collector_power_temperature:
  friendly_name: "Collector Power Temperature"
  unit_of_measurement: "°C"
  device_class: "temperature"
```

#### **Tank Temperature Sensors**
```yaml
sensor.econet_tank_temperature_1:
  friendly_name: "Tank Temperature 1"
  unit_of_measurement: "°C"
  device_class: "temperature"
  
sensor.econet_tank_temperature_2:
  friendly_name: "Tank Temperature 2"
  unit_of_measurement: "°C"
  device_class: "temperature"
```

#### **Circuit Temperature Sensors**
```yaml
sensor.econet_return_temperature:
  friendly_name: "Return Temperature"
  unit_of_measurement: "°C"
  device_class: "temperature"
  
sensor.econet_hot_water_temperature:
  friendly_name: "Hot Water Temperature"
  unit_of_measurement: "°C"
  device_class: "temperature"
```

#### **General Temperature Sensors**
```yaml
sensor.econet_temperature_sensor:
  friendly_name: "Temperature Sensor"
  unit_of_measurement: "°C"
  device_class: "temperature"
```

### **Status Sensors**

#### **Pump Status Sensors**
```yaml
sensor.econet_pump_1_status:
  friendly_name: "Pump 1 Status"
  icon: "mdi:pump"
  
sensor.econet_pump_2_status:
  friendly_name: "Pump 2 Status"
  icon: "mdi:pump"
```

#### **Output Status Sensors**
```yaml
sensor.econet_output_status:
  friendly_name: "Output Status"
  icon: "mdi:gauge"
```

### **Performance Sensors**

#### **Heat Output Sensors**
```yaml
sensor.econet_total_heat_output:
  friendly_name: "Total Heat Output"
  unit_of_measurement: "%"
  device_class: "power_factor"
  icon: "mdi:gauge"
```

---

## 🎛️ **Advanced Configuration**

### **Custom Entity Names**
```yaml
# Customize entity names for better organization
homeassistant:
  customize:
    sensor.econet_collector_temperature:
      friendly_name: "Solar Collector Temperature"
      icon: "mdi:solar-panel"
      
    sensor.econet_hot_water_temperature:
      friendly_name: "Domestic Hot Water Temperature"
      icon: "mdi:water-thermometer"
      
    sensor.econet_pump_1_status:
      friendly_name: "Solar Pump 1 Status"
      icon: "mdi:pump"
```

### **Entity Groups**
```yaml
# Group related entities for easier management
group:
  solar_collector_system:
    name: "Solar Collector System"
    entities:
      - sensor.econet_collector_temperature
      - sensor.econet_collector_power_temperature
      - sensor.econet_total_heat_output
      
  solar_tank_system:
    name: "Solar Tank System"
    entities:
      - sensor.econet_tank_temperature_1
      - sensor.econet_tank_temperature_2
      - sensor.econet_hot_water_temperature
      
  solar_pump_system:
    name: "Solar Pump System"
    entities:
      - sensor.econet_pump_1_status
      - sensor.econet_pump_2_status
      - sensor.econet_output_status
```

---

## 🤖 **Automation Examples**

### **1. Solar Performance Monitoring**

#### **High Collector Temperature Alert**
```yaml
automation:
  - alias: "High Collector Temperature Alert"
    description: "Alert when collector temperature gets too high"
    trigger:
      platform: numeric_state
      entity_id: sensor.econet_collector_temperature
      above: 80
    action:
      - service: notify.mobile_app
        data:
          title: "Solar Collector Alert"
          message: "Collector temperature is {{ states('sensor.econet_collector_temperature') }}°C"
    mode: single
```

#### **Low Solar Performance Alert**
```yaml
automation:
  - alias: "Low Solar Performance Alert"
    description: "Alert when solar heat output is low"
    trigger:
      platform: numeric_state
      entity_id: sensor.econet_total_heat_output
      below: 10
    condition:
      - condition: time
        after: "08:00:00"
        before: "18:00:00"
    action:
      - service: notify.mobile_app
        data:
          title: "Solar Performance Alert"
          message: "Solar heat output is only {{ states('sensor.econet_total_heat_output') }}%"
    mode: single
```

### **2. Temperature-Based Control**

#### **Hot Water Temperature Monitoring**
```yaml
automation:
  - alias: "Hot Water Temperature Check"
    description: "Monitor hot water temperature for efficiency"
    trigger:
      platform: numeric_state
      entity_id: sensor.econet_hot_water_temperature
      above: 75
    action:
      - service: notify.mobile_app
        data:
          title: "Hot Water Ready"
          message: "Hot water temperature is {{ states('sensor.econet_hot_water_temperature') }}°C"
    mode: single
```

#### **Tank Temperature Optimization**
```yaml
automation:
  - alias: "Tank Temperature Optimization"
    description: "Track tank temperature efficiency"
    trigger:
      platform: numeric_state
      entity_id: sensor.econet_tank_temperature_1
      above: 70
    condition:
      - condition: time
        after: "06:00:00"
        before: "22:00:00"
    action:
      - service: notify.mobile_app
        data:
          title: "Tank Temperature High"
          message: "Tank 1 temperature is {{ states('sensor.econet_tank_temperature_1') }}°C"
    mode: single
```

### **3. Pump Status Monitoring**

#### **Pump Performance Tracking**
```yaml
automation:
  - alias: "Pump Performance Monitoring"
    description: "Monitor pump operation for maintenance"
    trigger:
      platform: numeric_state
      entity_id: sensor.econet_pump_1_status
      above: 50
    action:
      - service: notify.mobile_app
        data:
          title: "Pump 1 Active"
          message: "Pump 1 is operating at {{ states('sensor.econet_pump_1_status') }}% capacity"
    mode: single
```

#### **System Output Monitoring**
```yaml
automation:
  - alias: "System Output Monitoring"
    description: "Track system output performance"
    trigger:
      platform: numeric_state
      entity_id: sensor.econet_output_status
      above: 0
    action:
      - service: notify.mobile_app
        data:
          title: "Solar System Active"
          message: "System output is {{ states('sensor.econet_output_status') }}"
    mode: single
```

---

## 📱 **Dashboard Configuration**

### **Lovelace Dashboard Example**

#### **Solar System Overview Card**
```yaml
type: vertical-stack
title: "Solar Collector System"
cards:
  - type: gauge
    name: "Collector Temperature"
    entity: sensor.econet_collector_temperature
    min: 0
    max: 100
    severity:
      green: 0
      yellow: 60
      red: 80
      
  - type: entities
    title: "Solar System Status"
    entities:
      - entity: sensor.econet_total_heat_output
        name: "Heat Output"
      - entity: sensor.econet_pump_1_status
        name: "Pump 1 Status"
      - entity: sensor.econet_pump_2_status
        name: "Pump 2 Status"
```

#### **Temperature Overview Card**
```yaml
type: entities
title: "Temperature Overview"
entities:
  - entity: sensor.econet_collector_temperature
    name: "Collector"
    icon: "mdi:solar-panel"
  - entity: sensor.econet_tank_temperature_1
    name: "Tank 1"
    icon: "mdi:thermometer"
  - entity: sensor.econet_tank_temperature_2
    name: "Tank 2"
    icon: "mdi:thermometer"
  - entity: sensor.econet_hot_water_temperature
    name: "Hot Water"
    icon: "mdi:water-thermometer"
  - entity: sensor.econet_return_temperature
    name: "Return"
    icon: "mdi:thermometer"
```

#### **Performance Monitoring Card**
```yaml
type: entities
title: "Performance Monitoring"
entities:
  - entity: sensor.econet_total_heat_output
    name: "Heat Output"
    icon: "mdi:gauge"
  - entity: sensor.econet_output_status
    name: "System Output"
    icon: "mdi:gauge"
  - entity: sensor.econet_collector_power_temperature
    name: "Power Temperature"
    icon: "mdi:thermometer"
```

---

## 🔍 **Troubleshooting**

### **Common Issues**

#### **1. Sensors Not Appearing**
```yaml
# Check device detection
# Verify controllerID = "ecoSOL 500" in sysParams
# Restart integration if needed
# Check Home Assistant logs for errors
```

#### **2. Data Not Updating**
```yaml
# Check scan_interval setting
# Verify device is accessible
# Check network connectivity
# Restart integration if needed
```

#### **3. Translation Issues**
```yaml
# Verify language settings in Home Assistant
# Check translation files are loaded
# Restart Home Assistant if needed
```

### **Debug Mode**
```yaml
# Enable debug logging
econet300:
  enable_debug: true
  
# Check logs for detailed information
# Look for API request/response details
# Monitor sensor creation process
```

---

## 📊 **Performance Optimization**

### **Polling Frequency**
```yaml
# Recommended settings for different use cases
scan_interval: 30      # General monitoring
scan_interval: 60      # Solar system monitoring
scan_interval: 300     # Performance tracking
```

### **Entity Filtering**
```yaml
# Only create entities you need
# Disable unused sensors for better performance
# Use entity customization for better organization
# Group related entities together
```

---

## 🎯 **Best Practices**

### **1. Entity Organization**
- Use descriptive friendly names
- Group related entities together
- Implement logical naming conventions
- Use appropriate icons and device classes

### **2. Automation Design**
- Start with simple automations
- Test thoroughly before production
- Use appropriate triggers and conditions
- Implement safety checks and fallbacks

### **3. Performance Management**
- Monitor system resources
- Use appropriate polling frequencies
- Implement error handling
- Regular maintenance and updates

### **4. User Experience**
- Create intuitive dashboards
- Provide clear status information
- Implement helpful notifications
- Use consistent design patterns

---

## 🚧 **Implementation Status**

### **Current Phase**: ✅ **Complete and Working**
- ✅ **API Integration**: Fully integrated with ecoNET system
- ✅ **Entity Creation**: All 10 sensors created automatically
- ✅ **Translation Support**: English and Polish included
- ✅ **Device Classes**: Proper sensor classification
- ✅ **Testing**: Validated with real device data

### **What This Means**
- **No additional development needed** - ecoSOL500 works out of the box
- **Automatic detection** - system recognizes ecoSOL500 controllers automatically
- **Full functionality** - all documented sensors are available
- **Professional quality** - production-ready integration

---

## 🎉 **Conclusion**

The ecoSOL500 integration with Home Assistant provides **professional-grade solar system monitoring** with:

- **10 comprehensive sensors** for complete system monitoring
- **Automatic integration** with no manual setup required
- **Real-time monitoring** of all system components
- **Professional quality** monitoring capabilities
- **Multi-language support** for international users

This integration represents the **gold standard** for solar system monitoring, providing everything needed for professional solar collector management in Home Assistant.

## 📚 **Additional Resources**

- **Device Overview**: See `overview.md`
- **Parameter Reference**: See `parameters.md`
- **API Support**: See `api_support.md`
- **ecoNET-300 Integration**: Main integration documentation

## 🔗 **Getting Help**

### **Support Resources**
- **Documentation**: All aspects documented in detail
- **Test Fixtures**: Real device data for validation
- **Integration Guide**: Complete usage examples
- **API Reference**: Technical implementation details

### **Community Support**
- **GitHub Issues**: Report bugs and request features
- **Discussions**: Share ideas and experiences
- **Documentation**: Help improve guides and examples

---

**The ecoSOL500 integration is complete and working perfectly! Enjoy professional-grade solar system monitoring in Home Assistant! 🏆✨**
