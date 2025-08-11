# ecoMAX360 Parameters Guide

## Overview
This document details the configurable parameters available for the ecoMAX360 device. The ecoMAX360 supports a comprehensive set of parameters covering heating circuits, temperature control, buffer management, and system configuration.

## Parameter Categories

### Heating Circuit Parameters
The ecoMAX360 supports up to 7 independent heating circuits, each with its own temperature control and thermostat integration.

#### Circuit Temperature Sensors
| Parameter | Description | Unit | Current Value | Min | Max | Editable |
|-----------|-------------|------|---------------|-----|-----|----------|
| `TempCircuit1` | Circuit 1 temperature | °C | 43.2 | -50 | 150 | Yes |
| `TempCircuit2` | Circuit 2 temperature | °C | 16.2 | -50 | 150 | Yes |
| `TempCircuit3` | Circuit 3 temperature | °C | 43.2 | -50 | 150 | Yes |
| `TempCircuit4` | Circuit 4 temperature | °C | 999.0 | -50 | 150 | Yes |
| `TempCircuit5` | Circuit 5 temperature | °C | 999.0 | -50 | 150 | Yes |
| `TempCircuit6` | Circuit 6 temperature | °C | 999.0 | -50 | 150 | Yes |
| `TempCircuit7` | Circuit 7 temperature | °C | 999.0 | -50 | 150 | Yes |

#### Circuit Thermostat Parameters
| Parameter | Description | Unit | Current Value | Min | Max | Editable |
|-----------|-------------|------|---------------|-----|-----|----------|
| `Circuit1thermostat` | Circuit 1 thermostat | - | 0 | 0 | 1 | Yes |
| `Circuit2thermostatTemp` | Circuit 2 thermostat temperature | °C | 15.37 | 0 | 50 | Yes |
| `Circuit3thermostatTemp` | Circuit 3 thermostat temperature | °C | 19.97 | 0 | 50 | Yes |
| `Circuit4thermostatTemp` | Circuit 4 thermostat temperature | °C | 0 | 0 | 50 | Yes |
| `Circuit5thermostatTemp` | Circuit 5 thermostat temperature | °C | 0 | 0 | 50 | Yes |
| `Circuit6thermostatTemp` | Circuit 6 thermostat temperature | °C | 0 | 0 | 50 | Yes |
| `Circuit7thermostatTemp` | Circuit 7 thermostat temperature | °C | 0 | 0 | 50 | Yes |

### Temperature Control Parameters

#### Core Temperature Sensors
| Parameter | Description | Unit | Current Value | Min | Max | Editable |
|-----------|-------------|------|---------------|-----|-----|----------|
| `TempClutch` | Clutch temperature | °C | 43.0 | -50 | 150 | Yes |
| `TempWthr` | Weather temperature | °C | 1.2 | -50 | 50 | Yes |
| `TempCWU` | DHW temperature | °C | null | 0 | 100 | Yes |

#### Buffer Tank Parameters
| Parameter | Description | Unit | Current Value | Min | Max | Editable |
|-----------|-------------|------|---------------|-----|-----|----------|
| `TempBuforUp` | Upper buffer temperature | °C | -26.8 | -50 | 150 | Yes |
| `TempBuforDown` | Lower buffer temperature | °C | null | -50 | 150 | Yes |

### System Configuration Parameters

#### Software Versions
| Parameter | Description | Value | Editable |
|-----------|-------------|-------|----------|
| `modulePanelSoftVer` | Panel software version | S003.68_1.82 | No |
| `ecosrvSoftVer` | ecoSRV software version | 3.2.3842 | No |
| `moduleASoftVer` | Module A software version | S002.28 | No |

#### Network Configuration
| Parameter | Description | Value | Editable |
|-----------|-------------|-------|----------|
| `eth0` | Ethernet IP address | 0.0.0.0 | Yes |
| `ecosrvPort` | ecoSRV port | 443 | Yes |
| `mainSrv` | Main server flag | true | No |

### Advanced Control Parameters

#### Power Supply
| Parameter | Description | Unit | Current Value | Min | Max | Editable |
|-----------|-------------|------|---------------|-----|-----|----------|
| `PS` | Power supply status | - | S003.68 | - | - | No |

#### Heating Control
| Parameter | Description | Unit | Current Value | Min | Max | Editable |
|-----------|-------------|------|---------------|-----|-----|----------|
| `heatingUpperTemp` | Upper heating temperature | °C | - | 0 | 100 | Yes |
| `heating_work_state_pump4` | Pump 4 work state | - | - | 0 | 1 | Yes |

## Parameter Metadata

### Data Structure
Each parameter includes comprehensive metadata:

```json
{
  "curr": {
    "ParameterName": "Current Value"
  },
  "currUnits": {
    "ParameterName": "Unit Type"
  },
  "currNumbers": {
    "ParameterName": "Raw Number Value"
  }
}
```

### Unit Types
- **1**: Temperature (°C)
- **2**: Percentage (%)
- **3**: Power (kW)
- **4**: Flow (l/min)
- **5**: Pressure (bar)
- **6**: Time (minutes)
- **7**: Status (on/off)

### Editability
- **Yes**: Parameter can be modified via API
- **No**: Parameter is read-only
- **Conditional**: Parameter editability depends on system state

## Parameter Access

### API Endpoints
- **`regParams`**: Current parameter values and units
- **`regParamsData`**: Parameter metadata and configuration
- **`sysParams`**: System-level parameters and information

### Update Frequency
- **Default Scan Interval**: 30 seconds
- **Real-time Updates**: Available for supported parameters
- **Manual Refresh**: Available via Home Assistant interface

## Home Assistant Integration

### Automatic Entity Creation
The integration automatically creates entities for all available parameters:

- **Temperature Sensors**: All temperature parameters with proper units
- **Status Sensors**: Binary and numeric status parameters
- **Configuration Sensors**: System information and version data

### Entity Naming
Parameters are automatically converted to Home Assistant-friendly names:
- `TempCircuit1` → `temp_circuit_1`
- `Circuit1thermostat` → `circuit_1_thermostat`
- `TempBuforUp` → `temp_bufor_up`

### Device Classes
- **Temperature**: `SensorDeviceClass.TEMPERATURE`
- **Status**: `SensorDeviceClass.ENUM`
- **Configuration**: `SensorDeviceClass.ENUM`

## Parameter Optimization

### Recommended Settings
- **Circuit Temperatures**: Set based on room requirements
- **Buffer Temperatures**: Optimize for heating efficiency
- **Weather Compensation**: Enable for energy savings
- **Thermostat Integration**: Configure per circuit needs

### Energy Efficiency
- **Temperature Setpoints**: Balance comfort and efficiency
- **Buffer Management**: Optimize heat storage and distribution
- **Circuit Scheduling**: Use time-based temperature control
- **Weather Integration**: Adaptive heating based on conditions

## Troubleshooting

### Common Issues
1. **Parameter Not Found**: Check parameter name spelling
2. **Value Out of Range**: Verify min/max limits
3. **Edit Permission Denied**: Parameter may be read-only
4. **Unit Mismatch**: Check parameter unit configuration

### Debug Information
- **Parameter Values**: Available in Home Assistant developer tools
- **API Responses**: Check integration logs for detailed information
- **Test Fixtures**: Reference sample data for parameter structure

---

*Last Updated: December 2024*  
*Total Parameters: 25+*  
*Editable Parameters: 20+*  
*Read-only Parameters: 5+*
