# ecoMAX850R2-X Boiler Controller Documentation

**Last Updated:** 2025-01-27
**Controller Model:** ecoMAX850R2-X
**Software Version:** 2.0.3521
**Protocol:** em (ecoMAX)

## Overview

The **ecoMAX850R2-X** is a pellet boiler controller from the ecoMAX series, designed for automatic pellet boilers with advanced control capabilities. This controller provides comprehensive monitoring and control of boiler operations, fuel management, and heating system integration.

## Device Specifications

### Hardware Information
- **Controller ID**: ecoMAX850R2-X
- **Software Version**: 2.0.3521
- **Protocol Type**: em (ecoMAX)
- **UID**: UID_1234567890
- **LAN Support**: Disabled
- **Registration Allowed**: Yes
- **Registration Refresh**: 5 seconds

### System Features
- **Boiler Control**: Full ON/OFF control capability
- **Fuel Management**: Pellet fuel level monitoring
- **Temperature Control**: Multiple temperature sensors and setpoints
- **Fan Control**: Variable speed fan control
- **Pump Management**: Multiple pump control circuits
- **Buffer Tank Support**: Upper and lower buffer temperature monitoring
- **Solar Integration**: Solar thermal system support
- **Mixer Circuits**: Up to 5 mixer circuits with individual control

## API Structure

### Core Endpoints

#### 1. System Parameters (`sysParams.json`)
- **Size**: 21KB (756 lines)
- **Purpose**: System configuration, device information, and UI tiles
- **Key Data**: Device info, firmware versions, control tiles, schedules

#### 2. Register Parameters (`regParams.json`)
- **Size**: 2.2KB (71 lines)
- **Purpose**: Current parameter values and system state
- **Key Data**: Real-time sensor readings, pump states, temperature values

## Control Interface (Tiles)

The ecoMAX850R2-X provides a comprehensive tile-based control interface with the following components:

### 1. Boiler Control Tile
```json
{
  "type_": "tile_text",
  "memberName_": "mode",
  "extra_": "CAN_TURN_ON_BOILER",
  "seqNo_": 1
}
```
- **Function**: Boiler ON/OFF control
- **Control**: Direct boiler control capability
- **States**: 0 (OFF), 1-25 (ON)

### 2. Boiler Power Tile
```json
{
  "type_": "tile_power",
  "memberName_": "boilerPower",
  "seqNo_": 2
}
```
- **Function**: Real-time boiler power display
- **Range**: 0-100%
- **Unit**: Percentage

### 3. Fuel Level Tile
```json
{
  "type_": "tile_level",
  "memberName_": "fuelLevel",
  "seqNo_": 3
}
```
- **Function**: Pellet fuel level monitoring
- **Range**: 0-100%
- **Unit**: Percentage

### 4. Fuel Stream Tile
```json
{
  "type_": "tile_stream",
  "memberName_": "fuelStream",
  "seqNo_": 4
}
```
- **Function**: Fuel feed rate monitoring
- **Range**: 0-100%
- **Unit**: Percentage

### 5. Fan Power Tile
```json
{
  "type_": "tile_fan",
  "memberName_": "fanPower",
  "seqNo_": 5
}
```
- **Function**: Combustion fan speed control
- **Range**: 0-100%
- **Unit**: Percentage

### 6. Boiler Temperature Tile
```json
{
  "type_": "tile_temp",
  "memberName_": "tempCO",
  "setMemberName_": "tempCOSet",
  "seqNo_": 9
}
```
- **Function**: Boiler temperature monitoring and control
- **Current**: tempCO (read-only)
- **Setpoint**: tempCOSet (adjustable)
- **Range**: 0-100°C

### 7. Return Temperature Tile
```json
{
  "type_": "tile_temp_ro",
  "memberName_": "tempBack",
  "seqNo_": 10
}
```
- **Function**: Return temperature monitoring
- **Type**: Read-only
- **Range**: 0-100°C

### 8. DHW Temperature Tile
```json
{
  "type_": "tile_temp",
  "memberName_": "tempCWU",
  "setMemberName_": "tempCWUSet",
  "seqNo_": 11
}
```
- **Function**: Domestic Hot Water temperature control
- **Current**: tempCWU (read-only)
- **Setpoint**: tempCWUSet (adjustable)
- **Range**: 0-100°C

## Sensor Parameters

### Temperature Sensors
| Parameter | Description | Type | Range | Unit |
|-----------|-------------|------|-------|------|
| `tempCO` | Boiler temperature | Read | 0-100 | °C |
| `tempCOSet` | Boiler temperature setpoint | Write | 0-100 | °C |
| `tempBack` | Return temperature | Read | 0-100 | °C |
| `tempCWU` | DHW temperature | Read | 0-100 | °C |
| `tempCWUSet` | DHW temperature setpoint | Write | 0-100 | °C |
| `tempExternalSensor` | External temperature | Read | -35-50 | °C |
| `tempLowerBuffer` | Lower buffer temperature | Read | 0-100 | °C |
| `tempUpperBuffer` | Upper buffer temperature | Read | 0-100 | °C |
| `tempFeeder` | Feeder temperature | Read | 0-100 | °C |

### Mixer Circuit Temperatures
| Parameter | Description | Type | Range | Unit |
|-----------|-------------|------|-------|------|
| `mixerTemp1` | Mixer 1 temperature | Read | 0-100 | °C |
| `mixerTemp2` | Mixer 2 temperature | Read | 0-100 | °C |
| `mixerTemp3` | Mixer 3 temperature | Read | 0-100 | °C |
| `mixerTemp4` | Mixer 4 temperature | Read | 0-100 | °C |
| `mixerTemp5` | Mixer 5 temperature | Read | 0-100 | °C |
| `mixerSetTemp1` | Mixer 1 setpoint | Write | 0-100 | °C |
| `mixerSetTemp2` | Mixer 2 setpoint | Write | 0-100 | °C |
| `mixerSetTemp3` | Mixer 3 setpoint | Write | 0-100 | °C |
| `mixerSetTemp4` | Mixer 4 setpoint | Write | 0-100 | °C |
| `mixerSetTemp5` | Mixer 5 setpoint | Write | 0-100 | °C |

### ecoSTER Thermostat Sensors
| Parameter | Description | Type | Range | Unit |
|-----------|-------------|------|-------|------|
| `ecoSterTemp1` | ecoSTER 1 temperature | Read | 0-100 | °C |
| `ecoSterTemp2` | ecoSTER 2 temperature | Read | 0-100 | °C |
| `ecoSterTemp3` | ecoSTER 3 temperature | Read | 0-100 | °C |
| `ecoSterSetTemp1` | ecoSTER 1 setpoint | Write | 0-100 | °C |
| `ecoSterSetTemp2` | ecoSTER 2 setpoint | Write | 0-100 | °C |
| `ecoSterSetTemp3` | ecoSTER 3 setpoint | Write | 0-100 | °C |

## Control Parameters

### System Status
| Parameter | Description | Type | Values |
|-----------|-------------|------|--------|
| `mode` | Boiler operating mode | Read | 0-25 |
| `statusCO` | Central heating status | Read | 0-10 |
| `statusCWU` | DHW status | Read | 0-10 |
| `thermostat` | Thermostat status | Read | 0-1 |

### Pump Control
| Parameter | Description | Type | Values |
|-----------|-------------|------|--------|
| `pumpCO` | Central heating pump | Write | true/false |
| `pumpCOWorks` | CH pump working status | Read | true/false |
| `pumpCWU` | DHW pump | Write | true/false |
| `pumpCWUWorks` | DHW pump working status | Read | true/false |
| `pumpCirculation` | Circulation pump | Write | true/false |
| `pumpCirculationWorks` | Circulation pump status | Read | true/false |
| `pumpSolar` | Solar pump | Write | true/false |
| `pumpSolarWorks` | Solar pump status | Read | true/false |
| `pumpFireplace` | Fireplace pump | Write | true/false |
| `pumpFireplaceWorks` | Fireplace pump status | Read | true/false |

### Mixer Pump Control
| Parameter | Description | Type | Values |
|-----------|-------------|------|--------|
| `mixerPumpWorks1` | Mixer 1 pump status | Read | true/false |
| `mixerPumpWorks2` | Mixer 2 pump status | Read | true/false |
| `mixerPumpWorks3` | Mixer 3 pump status | Read | true/false |
| `mixerPumpWorks4` | Mixer 4 pump status | Read | true/false |
| `mixerPumpWorks5` | Mixer 5 pump status | Read | true/false |

### Power and Performance
| Parameter | Description | Type | Range | Unit |
|-----------|-------------|------|-------|------|
| `boilerPower` | Boiler power output | Read | 0-100 | % |
| `boilerPowerKW` | Boiler power in kW | Read | 0-50 | kW |
| `fanPower` | Fan power | Read | 0-100 | % |
| `fuelConsum` | Fuel consumption | Read | 0-999 | kg/h |

### ecoSTER Control
| Parameter | Description | Type | Values |
|-----------|-------------|------|--------|
| `ecoSterMode1` | ecoSTER 1 mode | Read | 0-255 |
| `ecoSterMode2` | ecoSTER 2 mode | Read | 0-255 |
| `ecoSterMode3` | ecoSTER 3 mode | Read | 0-255 |
| `ecoSterContacts1` | ecoSTER 1 contacts | Read | true/false |
| `ecoSterContacts2` | ecoSTER 2 contacts | Read | true/false |
| `ecoSterContacts3` | ecoSTER 3 contacts | Read | true/false |
| `ecoSterDaySched1` | ecoSTER 1 day schedule | Read | true/false |
| `ecoSterDaySched2` | ecoSTER 2 day schedule | Read | true/false |
| `ecoSterDaySched3` | ecoSTER 3 day schedule | Read | true/false |

### Additional Controls
| Parameter | Description | Type | Values |
|-----------|-------------|------|--------|
| `contactGZC` | GZC contact | Read | true/false |
| `contactGZCActive` | GZC contact active | Read | true/false |
| `transmission` | Transmission setting | Read | 0-10 |

## Home Assistant Integration

### Supported Entity Types

#### Sensors
- **Temperature Sensors**: All temperature readings (boiler, DHW, buffer, mixer, ecoSTER)
- **Power Sensors**: Boiler power, fan power
- **Fuel Sensors**: Fuel level, fuel stream, fuel consumption
- **Status Sensors**: Operating mode, heating status, DHW status

#### Binary Sensors
- **Pump Status**: All pump working states
- **Contact Status**: GZC contacts, ecoSTER contacts
- **Schedule Status**: ecoSTER day schedules

#### Switches
- **Boiler Control**: Main boiler ON/OFF control
- **Pump Control**: Individual pump control (CH, DHW, circulation, solar, fireplace)

#### Number Entities
- **Temperature Setpoints**: Boiler, DHW, mixer setpoints
- **ecoSTER Setpoints**: Individual ecoSTER temperature setpoints

### Entity Naming Convention
- **Boiler Temperature**: `sensor.boiler_temperature`
- **DHW Temperature**: `sensor.dhw_temperature`
- **Boiler Power**: `sensor.boiler_power`
- **Fuel Level**: `sensor.fuel_level`
- **Boiler Control**: `switch.boiler_control`
- **CH Pump**: `switch.central_heating_pump`

## API Endpoints

### Standard ecoNET-300 Endpoints
- `/econet/sysParams` - System parameters
- `/econet/regParams` - Register parameters
- `/econet/regParamsData` - Parameter definitions
- `/econet/rmCurrentDataParams` - Real-time data
- `/econet/rmCurrentDataParamsEdits` - Editable parameters
- `/econet/rmParamsData` - Parameter database
- `/econet/rmStructure` - Menu structure
- `/econet/rmParamsNames` - Parameter names
- `/econet/rmParamsEnums` - Parameter enumerations
- `/econet/rmAlarmsNames` - Alarm definitions

### Control Endpoints
- `/econet/newParam` - Parameter modification
- `/econet/setParam` - Parameter setting

## Testing and Validation

### Test Files Location
```
tests/fixtures/ecoMAX850R2-X/
├── sysParams.json      # System parameters (21KB)
└── regParams.json      # Register parameters (2.2KB)
```

### Validation Checklist
- [x] System parameters structure validated
- [x] Register parameters structure validated
- [x] Temperature sensor ranges verified
- [x] Pump control parameters identified
- [x] Mixer circuit parameters documented
- [x] ecoSTER integration parameters mapped
- [x] Fuel management parameters documented
- [x] Power and performance parameters identified

## Troubleshooting

### Common Issues

1. **Temperature Sensor Readings**
   - **Issue**: Null values in mixer temperatures
   - **Cause**: Mixer circuits not configured or active
   - **Solution**: Check mixer circuit configuration

2. **Pump Status**
   - **Issue**: Pump shows working but not active
   - **Cause**: Pump control vs. pump status confusion
   - **Solution**: Use `pumpXXXWorks` for status, `pumpXXX` for control

3. **ecoSTER Integration**
   - **Issue**: ecoSTER parameters showing null
   - **Cause**: ecoSTER modules not connected
   - **Solution**: Verify ecoSTER module connections

## Version History

### v1.1.5 (Current)
- Initial documentation created
- Complete parameter mapping
- Test fixtures included
- Home Assistant integration guidelines

## References

- [ecoNET-300 API V1 Documentation](../API_V1_DOCUMENTATION.md)
- [Boiler Control README](../BOILER_CONTROL_README.md)
- [Cloud Translations Reference](../cloud_translations/MANUAL_TRANSLATION_REFERENCE.md)
