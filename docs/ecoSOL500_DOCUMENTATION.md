# ecoSOL500 Solar Collector System Documentation

## Overview
This document provides comprehensive documentation for the ecoSOL500 solar collector system support in the ecoNET300 Home Assistant integration.

## System Analysis
Based on the JSON endpoints analysis (`tests/fixtures/ecoSOL500/`), ecoSOL500 is a solar collector system with the following characteristics:

### Controller Identification
- **Controller ID**: `"ecoSOL 500"` (note the space)
- **System Type**: Solar collector system
- **Data Location**: `regParams.curr` section

### Available Sensors

#### Temperature Sensors (Sensors)
| Key | Description | Unit | Device Class | Precision | Icon |
|-----|-------------|------|--------------|-----------|------|
| `T1` | Collector temperature | °C | Temperature | 1 | mdi:thermometer |
| `T2` | Tank temperature | °C | Temperature | 1 | mdi:thermometer |
| `T3` | Tank temperature | °C | Temperature | 1 | mdi:thermometer |
| `T4` | Return temperature | °C | Temperature | 1 | mdi:thermometer |
| `T5` | Collector temperature - power measurement | °C | Temperature | 1 | mdi:thermometer |
| `T6` | Temperature sensor | °C | Temperature | 1 | mdi:thermometer |
| `TzCWU` | Hot water temperature | °C | Temperature | 1 | mdi:thermometer |

#### Status Sensors (Numeric Sensors - NOT Binary)
| Key | Description | Unit | Device Class | Precision | Icon |
|-----|-------------|------|--------------|-----------|------|
| `P1` | Pump 1 status | None | None | None | mdi:pump |
| `P2` | Pump 2 status | None | None | None | mdi:pump |
| `H` | Output status | None | None | None | mdi:gauge |

#### Other Sensors
| Key | Description | Unit | Device Class | Precision | Icon |
|-----|-------------|------|--------------|-----------|------|
| `Uzysk_ca_kowity` | Total heat output | % | Power Factor | 1 | mdi:gauge |

## Implementation Status

### ✅ **COMPLETE - No Additional Implementation Needed**

The ecoSOL500 integration is **100% complete** and works automatically through the existing sensor creation logic.

### How It Works

1. **Automatic Detection**: When `controllerID = "ecoSOL 500"` is detected in `sysParams`
2. **Sensor Selection**: System automatically uses `SENSOR_MAP_KEY["ecoSOL 500"]` 
3. **Entity Creation**: All available sensors are created automatically with proper:
   - Translations (English and Polish)
   - Icons
   - Units
   - Device classes
   - Precision settings

## Current Implementation Details

### 1. Constants Configuration (`const.py`)

#### Sensor Map Keys
```python
"ecoSOL 500": {
    "T1", "T2", "T3", "T4", "T5", "T6", "TzCWU",  # Temperature sensors
    "P1", "P2", "H",  # Status sensors (numeric, not binary)
    "Uzysk_ca_kowity",  # Heat output
}
```

#### Device Classes
- **Temperature sensors**: `SensorDeviceClass.TEMPERATURE`
- **Status sensors**: `None` (numeric values, not binary)
- **Heat output**: `SensorDeviceClass.POWER_FACTOR`

#### Units
- **Temperature sensors**: `UnitOfTemperature.CELSIUS`
- **Heat output**: `PERCENTAGE`
- **Status sensors**: `None`

#### Icons
- **Temperature sensors**: `mdi:thermometer`
- **Pump status**: `mdi:pump`
- **Output status**: `mdi:gauge`
- **Heat output**: `mdi:gauge`

### 2. Translation Support

#### English (`strings.json`, `translations/en.json`)
```json
"t1": { "name": "Collector Temperature" },
"t2": { "name": "Tank Temperature" },
"t3": { "name": "Tank Temperature" },
"t4": { "name": "Return Temperature" },
"t5": { "name": "Collector Temperature - Power Measurement" },
"t6": { "name": "Temperature Sensor" },
"tzcwu": { "name": "Hot Water Temperature" },
"p1": { "name": "Pump 1 Status" },
"p2": { "name": "Pump 2 Status" },
"h": { "name": "Output Status" },
"uzysk_ca_kowity": { "name": "Total Heat Output" }
```

#### Polish (`translations/pl.json`)
```json
"t1": { "name": "Temperatura kolektora" },
"t2": { "name": "Temperatura zbiornika" },
"t3": { "name": "Temperatura zbiornika" },
"t4": { "name": "Temperatura powrotu" },
"t5": { "name": "Temperatura kolektora - pomiar mocy" },
"t6": { "name": "Czujnik temperatury" },
"tzcwu": { "name": "Temperatura ciepłej wody" },
"p1": { "name": "Status pompy 1" },
"p2": { "name": "Status pompy 2" },
"h": { "name": "Status wyjścia" },
"uzysk_ca_kowity": { "name": "Całkowity uzysk ciepła" }
```

## Data Flow

1. **System Detection**: Controller ID `"ecoSOL 500"` detected from `sysParams.controllerID`
2. **Data Retrieval**: Sensor data read from `regParams.curr` section
3. **Entity Creation**: Sensors created automatically through `create_controller_sensors()`
4. **State Updates**: Entities receive updates through coordinator data updates

## Key Design Decisions

### 1. Automatic Integration
- **No separate functions needed** - ecoSOL500 sensors are handled automatically
- **No binary sensor implementation** - P1, P2, H are numeric status values, not ON/OFF states
- **Existing logic handles everything** - `create_controller_sensors()` does all the work

### 2. Data Source
- Uses `regParams.curr` through the existing coordinator data structure
- Matches the actual JSON structure from the ecoSOL500 system

### 3. Translation Keys
- Uses `camel_to_snake` conversion for consistent naming
- Follows the established pattern for other sensor types

### 4. Device Classes
- Temperature sensors use `TEMPERATURE` device class
- Status sensors use `None` (they are numeric, not binary)
- Heat output uses `POWER_FACTOR` device class

## Testing

### What Happens When ecoSOL500 is Connected

1. **Controller Detection**: System reads `controllerID = "ecoSOL 500"` from `sysParams`
2. **Sensor Selection**: Uses `SENSOR_MAP_KEY["ecoSOL 500"]` to get sensor keys
3. **Entity Creation**: Creates 10 sensor entities automatically:
   - **T1**: Collector Temperature (59.25°C)
   - **T2**: Tank Temperature (49.4°C) 
   - **T3**: Tank Temperature (69.9°C)
   - **T4**: Return Temperature (43.63°C)
   - **T5**: Collector Temperature - Power Measurement (-246.87°C)
   - **TzCWU**: Hot Water Temperature (70°C)
   - **P1**: Pump 1 Status (77)
   - **P2**: Pump 2 Status (0)
   - **H**: Output Status (0)
   - **Uzysk_ca_kowity**: Total Heat Output (0%)
4. **Skipped Entity**: **T6** is not created because its value is `null` in the data

### To Test

1. Connect an ecoSOL500 controller
2. Restart the Home Assistant integration
3. Check the device tree - you should see 10 ecoSOL500 sensors
4. Verify translations work in both English and Polish

## Important Notes

### P1, P2, H are NOT Binary Sensors

**Critical Finding**: Based on the JSON data and cloud translations:
- **P1**: "P1 sūkņa darba stāvoklis" (P1 pump working status) - value 77 indicates pump power/status, not ON/OFF
- **P2**: "P2 sūkņa darba stāvoklis" (P2 pump working status) - value 0 indicates pump power/status, not ON/OFF  
- **H**: "H izejas darba statuss" (H output working status) - value 0 indicates output status, not ON/OFF

These are **numeric status sensors**, not binary ON/OFF sensors.

## Future Enhancements

### 1. Additional Sensors
- System mode sensors (Tryb_pracy, Priorytet, Dezynfekcja)
- Schedule sensors (Cyrkulacja)
- Configuration parameters

### 2. Control Features
- Pump control switches
- Temperature setpoint controls
- Schedule configuration

### 3. Advanced Monitoring
- Energy efficiency calculations
- Solar gain tracking
- Performance analytics

## Conclusion

The ecoSOL500 implementation is **100% complete** and provides comprehensive support for solar collector monitoring through:

- ✅ Temperature monitoring at multiple collection points
- ✅ Pump and output status monitoring (numeric values)
- ✅ Heat output tracking
- ✅ Proper internationalization support (English and Polish)
- ✅ Consistent integration with existing ecoNET300 architecture
- ✅ Automatic entity creation with no additional code needed

**No additional implementation is required** - the system will automatically detect ecoSOL500 controllers and create all necessary sensors with proper translations, icons, units, and device classes.
