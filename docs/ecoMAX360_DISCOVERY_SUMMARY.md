# ecoMAX360 Device Discovery Summary

## Overview
This document summarizes the ecoMAX360 and ecoMAX-related information discovered from the ecoNET24 cloud JavaScript files (`dev_set1.js` through `dev_set5.js` and translation files).

## ecoMAX Device Types Identified

### Supported ecoMAX Models
- **ecoMAX 850P** - Basic pellet boiler system (Type 0)
- **ecoMAX 850i** - Advanced pellet boiler system with intelligent features (Type 1)
- **ecoMAX 360i** - Intelligent pellet boiler system with advanced controls

### Device Type Constants
```javascript
var ECOMAX_850P_TYPE = 0;
var ECOMAX_850i_TYPE = 1;
```

### Device Schema Prefixes
```javascript
var ECOMAX_SCHEMA_PREFIX = 'schema_';
var ECOMAX360I_SCHEMA_PREFIX = 'ecoMAX360i_schemat';
```

### Image Mapping
```javascript
let imagemap = {
    'ecoTRONIC100': 3,
    'ecoVENT': 3,
    'ecoMAX360i': 13,  // ecoMAX360i uses image ID 13
    'ecoFLOOR': 3,
    'e-GP': 3
};
```

## ecoMAX-Specific Parameters and Features

### Core Boiler Parameters
- **boilerPower** - Boiler output power (0-100%)
- **boilerPowerKW** - Boiler power in kilowatts
- **fuelStream** - Fuel consumption rate (kg/h)
- **lambdaLevel** - Lambda sensor oxygen level (%)
- **lambdaSet** - Lambda sensor setpoint (%)
- **lambdaStatus** - Lambda sensor status

### Temperature Sensors
- **T1** - Primary temperature sensor
- **T2** - Secondary temperature sensor
- **T3** - Tertiary temperature sensor
- **T4** - Quaternary temperature sensor
- **T5** - Quinary temperature sensor
- **T6** - Senary temperature sensor
- **tempCO** - Boiler temperature
- **tempCOSet** - Boiler temperature setpoint
- **tempCWU** - DHW temperature
- **tempExternalSensor** - External temperature sensor
- **tempBack** - Return temperature
- **tempFeeder** - Feeder temperature
- **tempFlueGas** - Flue gas temperature
- **tempExchanger** - Heat exchanger temperature
- **tempAirIn** - Air inlet temperature
- **tempAirOut** - Air outlet temperature

### Fan Controls
- **fanPower** - Main fan power
- **fanPowerExhaust** - Exhaust fan power
- **blowFan1BlowPower** - Blower fan #1 power
- **blowFan2BlowPower** - Blower fan #2 power
- **AIRFLOW_POWER_100** - Airflow power at 100% boiler power
- **AIRFLOW_POWER_50** - Airflow power at 50% boiler power

### Room Temperature Control (ecoSterTemp)
- **ecoSterTemp1** through **ecoSterTemp8** - Room temperature sensors 1-8
- **ecoSterSetTemp1** through **ecoSterSetTemp8** - Room temperature setpoints 1-8
- **STER_TEMP_DAY_X** - Day temperature for room X
- **STER_TEMP_NIGHT_X** - Night temperature for room X
- **STER_TEMP_SET_PARTY_X** - Party temperature for room X
- **STER_TEMP_SET_SUMMER_X** - Summer temperature for room X
- **STER_TEMP_ANTIFREEZ_X** - Antifreeze temperature for room X
- **STER_MODE_X** - Mode for room X
- **WORK_MODE_H_X** - Working mode for room X

### Mixer Circuit Controls (mixerTemp)
- **mixerTemp1** through **mixerTemp8** - Mixer circuit temperatures 1-8
- **mixerSetTemp1** through **mixerSetTemp8** - Mixer circuit setpoints 1-8
- **MIX_SET_TEMP_X** - Mixer X set temperature
- **SET_TEMP_H_X** - Heating circuit X set temperature
- **REGULATION_H_X** - Heating circuit X regulation
- **HANDLING_H_X** - Heating circuit X handling

### Pump Controls
- **pumpCO** - Boiler circulation pump
- **pumpCOW** - Boiler water pump
- **pumpMixerX** - Mixer circuit X pump
- **mixerPumpWorksX** - Mixer circuit X pump status
- **CIRCULATION_PUMP_ECOMAX** - Main circulation pump

### DHW (Domestic Hot Water) Controls
- **CWU_SET_TEMP** - DHW set temperature
- **CWU_WORK_MODE** - DHW working mode
- **TzCWU** - DHW temperature zone

### Additional Parameters
- **mode** - Operation mode
- **totalGain** - Total heat gain (kWh)
- **tempFireplace** - Fireplace temperature
- **tempLowerSolar** - Lower solar temperature

## ecoMAX Scheduling System

### Schedule Modes
```javascript
var scheduleEcomaxModes = ["sunday", "monday", "thuesday", "wednesday", "thursday", "friday", "saturday"];
```

### Schedule Parameters
- **ecomaxSchedules** - Main ecoMAX scheduling parameter
- **thermostat1TZ** through **thermostat3TZ** - Thermostat time zones
- **mixer1TZ** through **mixer8TZ** - Mixer circuit time zones
- **circuit1TZ** through **circuit7TZ** - Heating circuit time zones

### Schedule Mapping
```javascript
var schedulesMap = {
    "thermostat1TZ": "ecoSterTemp1",
    "thermostat2TZ": "ecoSterTemp2", 
    "thermostat3TZ": "ecoSterTemp3",
    "mixer1TZ": "mixerTemp1",
    "mixer2TZ": "mixerTemp2",
    "mixer3TZ": "mixerTemp3",
    "mixer4TZ": "mixerTemp4",
    "mixer5TZ": "mixerTemp5",
    "mixer6TZ": "mixerTemp6",
    "mixer7TZ": "mixerTemp7",
    "mixer8TZ": "mixerTemp8",
    "mixer9TZ": "mixerTemp9",
    "mixer10TZ": "mixerTemp10"
};
```

## ecoMAX-Specific Functions

### Boiler Power Display
```javascript
function getBoilerPowerParam() {
    var powerKW = getRegParamIfExists("boilerPowerKW");
    var powerPercent = getRegParamIfExists("boilerPower");
    if (powerKW.val == null && powerPercent.val != null) {
        return powerPercent;
    } else {
        return powerKW;
    }
}
```

### Lambda Sensor Display
```javascript
// Lambda level and setpoint handling with special precision (divided by 10)
if (p == "lambdaSet" || p == "lambdaLevel") {
    value /= 10;
}
```

### Schema Management
```javascript
function updateSchemaForPanels(ecoSterIds) {
    if (controller.type_ == ECOMAX_850i_TYPE) {
        // Special handling for ecoMAX 850i panels
    }
}

function updateSchemaForMixer(mixerIdNum, mixerIDLetter) {
    if (controller.type_ == ECOMAX_850i_TYPE) {
        // Special handling for ecoMAX 850i mixers
    }
}
```

## ecoMAX Device Type Differences

### ecoMAX 850i vs ecoMAX 850P
- **ecoSterTemp handling**: ecoMAX 850i has special room temperature sensor logic
- **Mixer temperature handling**: ecoMAX 850i has enhanced mixer circuit support
- **Parameter editing**: ecoMAX 850i has read-only mode for certain parameters
- **Schema display**: ecoMAX 850i has enhanced schema visualization
- **Remote menu parameters**: Different parameter connection mappings

### ecoMAX 360i Specific Features
- **Schema prefix**: Uses `ecoMAX360i_schemat` prefix
- **Image ID**: Uses image ID 13 for device identification
- **Advanced controls**: Enhanced scheduling and temperature control

## Protocol Support

### EM Protocol
- ecoMAX devices support EM (ecoMAX) protocol
- Special handling for ecoMAX 850i type
- Enhanced parameter management

### GM3 Protocol
- ecoMAX devices can also support GM3 protocol
- Special handling for different device types

## Integration Notes

### Home Assistant Considerations
1. **Sensors**: Temperature sensors (T1-T6, ecoSterTemp1-8, mixerTemp1-8), power, fuel consumption
2. **Binary Sensors**: Pump status, fan status, lambda sensor status
3. **Numbers**: Temperature setpoints, power setpoints, lambda setpoints
4. **Switches**: Pump controls, fan controls
5. **Climate**: Room temperature control for ecoSterTemp devices
6. **Translations**: Full multi-language support for all ecoMAX parameters

### Parameter Precision
```javascript
var regParamsPrecision = {
    "boilerPowerKW": 1,      // 1 decimal place
    "boilerPower": 0,        // 0 decimal places
    "fuelStream": 1,         // 1 decimal place
    "ecoSterTemp": 1,        // 1 decimal place
    "ecoSterSetTemp": 1,     // 1 decimal place
    "tempExternalSensor": 1, // 1 decimal place
    "lambdaSet": 1,          // 1 decimal place (stored as 10x)
    "lambdaLevel": 1,        // 1 decimal place (stored as 10x)
    "thermoTemp": 1,         // 1 decimal place
    "thermoSetTemp": 0       // 0 decimal places
};
```

### Units
```javascript
var regParamsUnit = {
    'T1': '°C', 'T2': '°C', 'T3': '°C', 'T4': '°C', 'T5': '°C', 'T6': '°C',
    'P1': '%', 'P2': '%',
    'tempCO': '°C', 'tempCOSet': '°C', 'tempCWU': '°C',
    'boilerPowerKW': 'kW', 'boilerPower': '%',
    'fuelStream': 'kg/h',
    'lambdaLevel': '%', 'lambdaSet': '%',
    'totalGain': 'kWh'
};
```

## Source Files
- `dev_set1.js` - Controller and device type definitions
- `dev_set2.js` - Schema management and parameter connections
- `dev_set3.js` - Parameter management and remote menu handling
- `dev_set4.js` - Scheduling system and chart options
- `dev_set5.js` - Device-specific fixes and fuel consumption
- `econet_transp*.js` - Multi-language translations

## Next Steps
1. Extract specific parameter mappings from the JavaScript files
2. Identify Home Assistant entity types for each ecoMAX feature
3. Create translation files following the established pattern
4. Implement ecoMAX-specific device detection
5. Add ecoMAX scheduling and temperature control to the integration
6. Implement lambda sensor monitoring and control
