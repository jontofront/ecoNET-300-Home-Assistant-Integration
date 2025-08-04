# ecoMAX850R2-X vs ecoMAX810P-L Sensor Comparison

## Overview
This document compares the sensor capabilities and features between the **ecoMAX850R2-X** (newer model) and **ecoMAX810P-L** (older model) boiler controllers.

## Key Differences Summary

### 🔄 **Data Structure**
- **ecoMAX850R2-X**: Direct parameter names in `regParams.json`
- **ecoMAX810P-L**: Numbered parameters requiring mapping via `rmCurrentDataParams.json`

### 🆕 **New Features in ecoMAX850R2-X**

## 1. ecoSTER Thermostat System Integration

### New ecoSTER Sensors
| Parameter | Type | Description | Value Range |
|-----------|------|-------------|-------------|
| `ecoSterTemp1` | Temperature | ecoSTER Thermostat 1 Temperature | 0-100°C |
| `ecoSterTemp2` | Temperature | ecoSTER Thermostat 2 Temperature | 0-100°C |
| `ecoSterTemp3` | Temperature | ecoSTER Thermostat 3 Temperature | 0-100°C |
| `ecoSterSetTemp1` | Temperature | ecoSTER Thermostat 1 Setpoint | 0-100°C |
| `ecoSterSetTemp2` | Temperature | ecoSTER Thermostat 2 Setpoint | 0-100°C |
| `ecoSterSetTemp3` | Temperature | ecoSTER Thermostat 3 Setpoint | 0-100°C |
| `ecoSterMode1` | Mode | ecoSTER Thermostat 1 Mode | 0-255 |
| `ecoSterMode2` | Mode | ecoSTER Thermostat 2 Mode | 0-255 |
| `ecoSterMode3` | Mode | ecoSTER Thermostat 3 Mode | 0-255 |
| `ecoSterContacts1` | Binary | ecoSTER Thermostat 1 Contacts | true/false |
| `ecoSterContacts2` | Binary | ecoSTER Thermostat 2 Contacts | true/false |
| `ecoSterContacts3` | Binary | ecoSTER Thermostat 3 Contacts | true/false |
| `ecoSterDaySched1` | Binary | ecoSTER Day Schedule 1 | true/false |
| `ecoSterDaySched2` | Binary | ecoSTER Day Schedule 2 | true/false |
| `ecoSterDaySched3` | Binary | ecoSTER Day Schedule 3 | true/false |

## 2. Enhanced Fuel Management

### New Fuel Sensors
| Parameter | Type | Description | Value Range |
|-----------|------|-------------|-------------|
| `fuelConsum` | Consumption | Fuel Consumption | 0.0+ |
| `fuelStream` | Stream | Fuel Stream Rate | 0.0+ |

## 3. Extended Mixer Support

### Additional Mixer Controls
| Parameter | Type | Description | Value Range |
|-----------|------|-------------|-------------|
| `mixerSetTemp5` | Temperature | Mixer 5 Temperature Setpoint | 0-100°C |
| `mixerTemp5` | Temperature | Mixer 5 Current Temperature | 0-100°C |
| `mixerPumpWorks5` | Binary | Mixer 5 Pump Status | true/false |

## 4. System Configuration Differences

### Software Versions
- **ecoMAX850R2-X**: `ecosrvSoftVer: "2.0.3521"`
- **ecoMAX810P-L**: Different software version structure

### Module Versions (ecoMAX850R2-X)
```json
"modulesVers": [
    ["lbModuleAVerCurr", "103.31.25", 192],
    ["lbPanelModuleVerCurr", "103.30.20", 149],
    ["lbEcoSTERModuleVer1Curr", "10.11.8", 3]
]
```

## 5. UI Tile System (ecoMAX850R2-X)

### New Tile Types
- `tile_text` - Text display tiles
- `tile_power` - Power display tiles
- `tile_level` - Level indicator tiles
- `tile_stream` - Stream flow tiles
- `tile_fan` - Fan control tiles
- `tile_temp` - Temperature control tiles
- `tile_temp_ro` - Read-only temperature tiles
- `tile_temp_wave` - ecoSTER thermostat tiles

### Special Tile Features
- **CAN_TURN_ON_BOILER** - Boiler control capability
- **ecoSter Integration** - Advanced thermostat control
- **Wave Temperature Control** - ecoSTER specific controls

## 6. Missing Features in ecoMAX850R2-X

### Features Present in ecoMAX810P-L but NOT in ecoMAX850R2-X
| Parameter | Type | Description |
|-----------|------|-------------|
| `lambdaSet` | Lambda | Lambda sensor setpoint |
| `lambdaLevel` | Lambda | Lambda sensor level |
| `lambdaStatus` | Lambda | Lambda sensor status |
| `tempFlueGas` | Temperature | Flue gas temperature |
| `feederWorks` | Binary | Feeder working status |
| `feeder` | Binary | Feeder status |
| `lighterWorks` | Binary | Lighter working status |
| `lighter` | Binary | Lighter status |
| `fan` | Binary | Fan status |
| `fanWorks` | Binary | Fan working status |
| `blowFan1` | Binary | Blow fan 1 status |
| `blowFan2` | Binary | Blow fan 2 status |
| `blowFan1Active` | Binary | Blow fan 1 active |
| `blowFan2Active` | Binary | Blow fan 2 active |
| `fan2Exhaust` | Binary | Exhaust fan 2 status |
| `fan2ExhaustWorks` | Binary | Exhaust fan 2 working |
| `feederOuter` | Binary | Outer feeder status |
| `feederOuterWorks` | Binary | Outer feeder working |
| `feeder2Additional` | Binary | Additional feeder 2 |
| `feeder2AdditionalWorks` | Binary | Additional feeder 2 working |
| `outerBoiler` | Binary | Outer boiler status |
| `outerBoilerWorks` | Binary | Outer boiler working |
| `alarmOutput` | Binary | Alarm output status |
| `alarmOutputWorks` | Binary | Alarm output working |

## 7. Common Sensors (Both Models)

### Temperature Sensors
| Parameter | ecoMAX850R2-X | ecoMAX810P-L | Description |
|-----------|---------------|--------------|-------------|
| `tempCO` | ✅ | ✅ | Boiler temperature |
| `tempCOSet` | ✅ | ✅ | Boiler temperature setpoint |
| `tempCWU` | ✅ | ✅ | Hot water temperature |
| `tempCWUSet` | ✅ | ✅ | Hot water temperature setpoint |
| `tempExternalSensor` | ✅ | ✅ | External temperature sensor |
| `tempFeeder` | ✅ | ✅ | Feeder temperature |
| `tempUpperBuffer` | ✅ | ✅ | Upper buffer temperature |
| `tempLowerBuffer` | ✅ | ✅ | Lower buffer temperature |
| `tempBack` | ✅ | ✅ | Return temperature |
| `mixerTemp1-4` | ✅ | ✅ | Mixer temperatures 1-4 |
| `mixerSetTemp1-4` | ✅ | ✅ | Mixer setpoints 1-4 |

### Status Sensors
| Parameter | ecoMAX850R2-X | ecoMAX810P-L | Description |
|-----------|---------------|--------------|-------------|
| `mode` | ✅ | ✅ | Operation mode |
| `statusCO` | ✅ | ✅ | Central heating status |
| `statusCWU` | ✅ | ✅ | Hot water status |
| `thermostat` | ✅ | ✅ | Thermostat status |
| `transmission` | ✅ | ✅ | Transmission status |

### Power & Performance
| Parameter | ecoMAX850R2-X | ecoMAX810P-L | Description |
|-----------|---------------|--------------|-------------|
| `boilerPower` | ✅ | ✅ | Boiler power percentage |
| `boilerPowerKW` | ✅ | ✅ | Boiler power in kW |
| `fanPower` | ✅ | ✅ | Fan power percentage |
| `fuelLevel` | ✅ | ✅ | Fuel level percentage |

### Pump Controls
| Parameter | ecoMAX850R2-X | ecoMAX810P-L | Description |
|-----------|---------------|--------------|-------------|
| `pumpCO` | ✅ | ✅ | Central heating pump |
| `pumpCOWorks` | ✅ | ✅ | Central heating pump working |
| `pumpCWU` | ✅ | ✅ | Hot water pump |
| `pumpCWUWorks` | ✅ | ✅ | Hot water pump working |
| `pumpCirculation` | ✅ | ✅ | Circulation pump |
| `pumpCirculationWorks` | ✅ | ✅ | Circulation pump working |
| `pumpSolar` | ✅ | ✅ | Solar pump |
| `pumpSolarWorks` | ✅ | ✅ | Solar pump working |
| `pumpFireplace` | ✅ | ✅ | Fireplace pump |
| `pumpFireplaceWorks` | ✅ | ✅ | Fireplace pump working |
| `mixerPumpWorks1-4` | ✅ | ✅ | Mixer pumps 1-4 working |

## 8. Integration Implications

### Home Assistant Integration
- **ecoMAX850R2-X** will work with the current `_default` sensor mapping
- **New ecoSTER sensors** may need additional mapping in `SENSOR_MAP_KEY`
- **Missing lambda sensors** in ecoMAX850R2-X (no combustion optimization)
- **Enhanced fuel monitoring** with consumption and stream sensors

### Recommended Actions
1. Add ecoSTER sensor mappings to `const.py`
2. Create ecoSTER-specific entity descriptions
3. Add fuel consumption and stream sensors
4. Update device class mappings for new sensors
5. Consider adding ecoSTER thermostat controls as switches/numbers

## 9. Conclusion

The **ecoMAX850R2-X** represents a significant evolution with:
- **Advanced ecoSTER thermostat integration**
- **Enhanced fuel monitoring capabilities**
- **Extended mixer support (5 mixers vs 4)**
- **Modern UI tile system**
- **Simplified data structure**

However, it **lacks some advanced combustion monitoring features** (lambda sensors, flue gas temperature) that are present in the ecoMAX810P-L, suggesting it may be optimized for different use cases or fuel types.
