# ecoMAX810P-L Real-time Data Guide

## 📊 **Real-time Monitoring Overview**

The ecoMAX810P-L provides comprehensive real-time monitoring capabilities through the `rmCurrentDataParams` endpoint. This guide explains how to access and interpret live system data.

## 🚀 **Real-time Data Endpoint**

### **Primary Endpoint**
- **URL**: `http://_IP_/econet/rmCurrentDataParams`
- **Response Time**: <100ms
- **Update Frequency**: Real-time
- **Data Format**: JSON
- **Authentication**: IP-based access

### **Response Structure**
```json
{
  "remoteMenuCurrDataParamsVer": "17127_1",
  "data": {
    "parameter_id": {
      "unit": "unit_type",
      "name": "parameter_name",
      "special": "special_type"
    }
  }
}
```

## 🔍 **Real-time Data Categories**

### **1. Temperature Sensors**
### **2. Status Indicators**
### **3. Pump & Fan Status**
### **4. Valve & Actuator Status**
### **5. System Health Indicators**
### **6. Network & Communication Status**

---

## 🌡️ **1. TEMPERATURE SENSORS**

### **Core Temperature Readings**

| Parameter ID | Name | Unit | Special | Description |
|-------------|------|------|---------|-------------|
| **1024** | Boiler temperature | °C | 1 | Live boiler temperature |
| **1025** | HUW temperature | °C | 1 | Hot water temperature |
| **1028** | Upper buffer temperature | °C | 1 | Upper buffer sensor |
| **1029** | Lower buffer temperature | °C | 1 | Lower buffer sensor |
| **1030** | Emission temperature | °C | 1 | Heating circuit temperature |
| **1031** | Temp. mixer 1 | °C | 1 | Mixer 1 temperature |
| **1032** | Temp. mixer 2 | °C | 1 | Mixer 2 temperature |
| **1033** | Temp. mixer 3 | °C | 1 | Mixer 3 temperature |
| **1034** | Temp. mixer 4 | °C | 1 | Mixer 4 temperature |

### **Environmental Temperatures**

| Parameter ID | Name | Unit | Special | Description |
|-------------|------|------|---------|-------------|
| **26** | Feeder temperature | °C | 1 | Pellet feeder temperature |
| **28** | Weather temperature | °C | 1 | Outdoor temperature sensor |

### **Temperature Setpoints**

| Parameter ID | Name | Unit | Special | Description |
|-------------|------|------|---------|-------------|
| **1280** | Preset boiler temperature | °C | 0 | Target boiler temperature |
| **1281** | HUW preset temperature | °C | 0 | Target hot water temperature |
| **1287** | Preset temp. mixer 1 | °C | 0 | Mixer 1 target temperature |
| **1288** | Preset temp. mixer 2 | °C | 0 | Mixer 2 target temperature |
| **1289** | Preset temp. mixer 3 | °C | 0 | Mixer 3 target temperature |
| **1290** | Preset temp. mixer 4 | °C | 0 | Mixer 4 target temperature |

---

## 📊 **2. STATUS INDICATORS**

### **System Operation Status**

| Parameter ID | Name | Unit | Special | Description |
|-------------|------|------|---------|-------------|
| **1** | Lighter | - | 1 | Ignition system status |
| **3** | Poker | - | 1 | Poker system status |
| **113** | Unseal | - | 1 | System unseal status |
| **114** | Fuel level | - | 1 | Fuel level indicator |
| **117** | Boiler thermostat | - | 1 | Boiler thermostat status |
| **118** | Room thermostat mixer 1 | - | 1 | Mixer 1 room thermostat |
| **119** | Room thermostat mixer 2 | - | 1 | Mixer 2 room thermostat |
| **120** | Room thermostat mixer 3 | - | 1 | Mixer 3 room thermostat |
| **121** | Room thermostat mixer 4 | - | 1 | Mixer 4 room thermostat |

### **Performance Indicators**

| Parameter ID | Name | Unit | Special | Description |
|-------------|------|------|---------|-------------|
| **155** | Work at 100% | - | 0 | 100% output operation |
| **156** | Work at 50% | - | 0 | 50% output operation |
| **157** | Work at 30% | - | 0 | 30% output operation |
| **158** | Feeder work | - | 0 | Feeder operation status |
| **159** | Firing-up count | - | 0 | Number of firing-up attempts |
| **160** | Number of resets | - | 0 | System reset counter |

---

## 🔄 **3. PUMP & FAN STATUS**

### **Pump Operation Status**

| Parameter ID | Name | Unit | Special | Description |
|-------------|------|------|---------|-------------|
| **1541** | Boiler pump | - | 1 | Boiler pump operation |
| **1542** | HUW pump | - | 1 | Hot water pump operation |
| **1543** | Circulating pump | - | 1 | Circulating pump operation |
| **1544** | Pump mixer 1 | - | 1 | Mixer 1 pump operation |
| **1547** | Pump mixer 2 | - | 1 | Mixer 2 pump operation |
| **1550** | Pump mixer 3 | - | 1 | Mixer 3 pump operation |
| **1553** | Pump mixer 4 | - | 1 | Mixer 4 pump operation |

### **Fan & Airflow Status**

| Parameter ID | Name | Unit | Special | Description |
|-------------|------|------|---------|-------------|
| **1536** | Fan | - | 1 | Fan operation status |
| **1538** | Feeder | - | 1 | Pellet feeder operation |
| **1540** | Additional feeder | - | 1 | Secondary feeder status |

---

## 🎛️ **4. VALVE & ACTUATOR STATUS**

### **Mixer Valve Control**

| Parameter ID | Name | Unit | Special | Description |
|-------------|------|------|---------|-------------|
| **139** | Valve mixer 1 | % | 0 | Mixer 1 valve position |
| **140** | Valve mixer 2 | % | 0 | Mixer 2 valve position |
| **141** | Valve mixer 3 | % | 0 | Mixer 3 valve position |
| **142** | Valve mixer 4 | % | 0 | Mixer 4 valve position |

### **Servo Actuator Status**

| Parameter ID | Name | Unit | Special | Description |
|-------------|------|------|---------|-------------|
| **143** | Servo mixer 1 | - | 4 | Mixer 1 servo status |
| **144** | Servo mixer 2 | - | 4 | Mixer 2 servo status |
| **145** | Servo mixer 3 | - | 4 | Mixer 3 servo status |
| **146** | Servo mixer 4 | - | 4 | Mixer 4 servo status |

### **Valve Position Indicators**

| Parameter ID | Name | Unit | Special | Description |
|-------------|------|------|---------|-------------|
| **147** | Valve mixer 1 | - | 3 | Mixer 1 valve indicator |
| **148** | Valve mixer 2 | - | 3 | Mixer 2 valve indicator |
| **149** | Valve mixer 3 | - | 3 | Mixer 3 valve indicator |
| **150** | Valve mixer 4 | - | 3 | Mixer 4 valve indicator |

---

## 🛡️ **5. SYSTEM HEALTH INDICATORS**

### **Oxygen & Combustion**

| Parameter ID | Name | Unit | Special | Description |
|-------------|------|------|---------|-------------|
| **151** | Oxygen | - | 2 | Oxygen sensor reading |
| **154** | Oxygen | % | 1 | Oxygen percentage |

### **Safety & Monitoring**

| Parameter ID | Name | Unit | Special | Description |
|-------------|------|------|---------|-------------|
| **1792** | - | - | 7 | System status indicator |
| **1794** | Burner output | % | 0 | Current burner output |

---

## 🌐 **6. NETWORK & COMMUNICATION STATUS**

### **Network Configuration**

| Parameter ID | Name | Unit | Special | Description |
|-------------|------|------|---------|-------------|
| **161** | IP: | - | 0 | IP address display |
| **162** | Mask: | - | 0 | Network mask display |
| **163** | Gateway: | - | 0 | Gateway address display |
| **164** | Server: | - | 5 | Server configuration |
| **165** | IP: | - | 0 | Secondary IP display |
| **166** | Mask: | - | 0 | Secondary mask display |
| **167** | Gateway: | - | 0 | Secondary gateway display |
| **168** | Server: | - | 5 | Secondary server config |

### **WiFi & Security**

| Parameter ID | Name | Unit | Special | Description |
|-------------|------|------|---------|-------------|
| **169** | Encryption: | - | 6 | Encryption type |
| **170** | Signal strenght: | % | 0 | WiFi signal strength |
| **171** | Wifi status: | - | 5 | WiFi connection status |
| **173** | SSID: | - | 0 | WiFi network name |

---

## 🔧 **Data Interpretation Guide**

### **Unit Types**
- **Unit 0**: No unit (raw values)
- **Unit 1**: Temperature (°C)
- **Unit 2**: Percentage (%)
- **Unit 3**: Time (seconds)
- **Unit 4**: Count (integer)
- **Unit 5**: Selection (enum)
- **Unit 6**: Selection with encryption
- **Unit 7**: System status
- **Unit 8**: Time (10x multiplier)
- **Unit 31**: Special status indicators

### **Special Types**
- **Special 0**: Standard parameter
- **Special 1**: Status indicator
- **Special 2**: Oxygen sensor
- **Special 3**: Valve position
- **Special 4**: Servo status
- **Special 5**: Network status
- **Special 6**: Encryption status
- **Special 7**: System status

### **Value Ranges**
- **Temperatures**: -20°C to +120°C
- **Percentages**: 0% to 100%
- **Time**: 0.1s to 2550s
- **Status**: 0 (Off) to 1 (On)
- **Counters**: 0 to 255

---

## 📡 **Real-time Monitoring Implementation**

### **Home Assistant Integration**

#### **1. Temperature Sensors**
```yaml
# Example temperature sensor configuration
sensor:
  - platform: template
    sensors:
      boiler_temperature:
        friendly_name: "Boiler Temperature"
        unit_of_measurement: "°C"
        value_template: "{{ states('sensor.econet_boiler_temp') }}"
      
      huw_temperature:
        friendly_name: "Hot Water Temperature"
        unit_of_measurement: "°C"
        value_template: "{{ states('sensor.econet_huw_temp') }}"
```

#### **2. Status Binary Sensors**
```yaml
# Example status sensor configuration
binary_sensor:
  - platform: template
    sensors:
      boiler_pump_status:
        friendly_name: "Boiler Pump Status"
        value_template: "{{ states('binary_sensor.econet_boiler_pump') == 'on' }}"
      
      fan_status:
        friendly_name: "Fan Status"
        value_template: "{{ states('binary_sensor.econet_fan') == 'on' }}"
```

#### **3. Control Switches**
```yaml
# Example control switch configuration
switch:
  - platform: template
    switches:
      boiler_control:
        friendly_name: "Boiler Control"
        value_template: "{{ states('switch.econet_boiler') }}"
        turn_on:
          service: script.turn_on_boiler
        turn_off:
          service: script.turn_off_boiler
```

### **Automation Examples**

#### **1. Temperature-Based Control**
```yaml
# Automatically adjust boiler temperature based on outdoor temperature
automation:
  - alias: "Adjust Boiler Temperature for Weather"
    trigger:
      platform: numeric_state
      entity_id: sensor.weather_temperature
      below: 5
    action:
      service: input_number.set_value
      target:
        entity_id: input_number.boiler_target_temp
      data:
        value: 85
```

#### **2. Pump Protection**
```yaml
# Protect pumps from running when system is too cold
automation:
  - alias: "Protect Pumps from Cold"
    trigger:
      platform: numeric_state
      entity_id: sensor.boiler_temperature
      below: 20
    action:
      service: switch.turn_off
      target:
        entity_id: switch.boiler_pump
```

#### **3. Energy Optimization**
```yaml
# Optimize heating based on time and occupancy
automation:
  - alias: "Night Temperature Reduction"
    trigger:
      platform: time
      at: "22:00:00"
    action:
      service: input_number.set_value
      target:
        entity_id: input_number.boiler_target_temp
      data:
        value: 60
```

---

## 📊 **Data Collection & Analysis**

### **Polling Frequency Recommendations**
- **Critical Parameters**: Every 10 seconds (temperatures, safety)
- **Status Parameters**: Every 30 seconds (pumps, fans, valves)
- **Configuration Parameters**: Every 5 minutes (setpoints, modes)
- **Network Parameters**: Every 1 minute (connection status)

### **Data Storage**
- **Short-term**: Home Assistant history (7 days)
- **Medium-term**: InfluxDB or similar (30 days)
- **Long-term**: CSV export or cloud storage (1 year)

### **Performance Monitoring**
- **Response Time**: Track API response times
- **Data Quality**: Monitor for missing or invalid values
- **System Health**: Track error rates and connection stability

---

## 🎯 **Best Practices**

### **1. Efficient Data Collection**
- Use appropriate polling frequencies
- Implement exponential backoff for errors
- Cache static data (parameter names, descriptions)

### **2. Error Handling**
- Implement retry logic for failed requests
- Log all API errors for debugging
- Provide fallback values for critical parameters

### **3. User Experience**
- Show loading states during data updates
- Provide clear error messages
- Implement data validation before display

### **4. System Integration**
- Use Home Assistant's built-in validation
- Implement proper entity naming conventions
- Provide comprehensive device information

---

## 🎉 **Conclusion**

The ecoMAX810P-L's real-time monitoring capabilities provide **unprecedented visibility** into your heating system:

- **Live temperature monitoring** of all circuits
- **Real-time status tracking** of all components
- **Instant performance feedback** for optimization
- **Comprehensive system health** monitoring

This real-time data foundation enables **intelligent automation**, **energy optimization**, and **predictive maintenance** in your Home Assistant setup. 🏆✨
