# ecoMAX810P-L Parameter Names Analysis

## Overview
This document analyzes the parameter names discovered from testing the `rmParamsNames` endpoint locally on an ecoMAX810P-L device at `http://_IP_/econet/rmParamsNames`.

## Test Details
- **Device:** ecoMAX810P-L
- **Endpoint:** `/econet/rmParamsNames`
- **Version:** 61477_1
- **Total Parameters:** 165

## Parameter Categories

### 🔥 **Boiler Control & Operation (0-39)**
- **Airflow Control:**
  - `100% Blow-in output` - Full power airflow setting
  - `50% Blow-in output` - Half power airflow setting
  - `30% Blow-in output` - Low power airflow setting
  - `Firing-up airflow` - Startup airflow configuration
  - `Minimum airflow output` - Minimum airflow threshold

- **Feeder Control:**
  - `100% Feeder operation` - Full power feeder operation time
  - `100% Feeder interval` - Full power feeder interval
  - `50% Feeder operation` - Half power feeder operation time
  - `50% Feeder interval` - Half power feeder interval
  - `30% Feeder operation` - Low power feeder operation time
  - `30% Feeder interval` - Low power feeder interval
  - `Feeding time` - General feeding duration
  - `Firing-up time` - Startup duration
  - `Feed. time` - Feeding duration (alternative)
  - `Feed. interval` - Feeding interval (alternative)
  - `Feeder operat time 2` - Secondary feeder operation time
  - `Feeder interval 2` - Secondary feeder interval

- **Hysteresis Settings:**
  - `50% H2 hysteresis` - Half power H2 hysteresis
  - `30% H1 hysteresis` - Low power H1 hysteresis
  - `Boiler hysteresis` - General boiler hysteresis
  - `HUW cont. hysteresis` - Hot water hysteresis

### 🌡️ **Temperature Control (40-79)**
- **Boiler Temperature:**
  - `Preset boiler temperature` - Target boiler temperature
  - `Min. boiler temperature` - Minimum boiler temperature
  - `Max. boiler temperature` - Maximum boiler temperature
  - `Boiler cooling temperature` - Cooling temperature setting

- **Hot Water (HUW):**
  - `HUW preset temperature` - Hot water target temperature
  - `Minimum HUW temperature` - Minimum hot water temperature
  - `Maximum HUW temperature` - Maximum hot water temperature
  - `HUW disinfection` - Hot water disinfection setting

- **Mixer Circuits (1-4):**
  - `Preset mixer 1-4 temperature` - Target temperatures for each mixer
  - `Min. mixer 1-4 temp.` - Minimum temperatures for each mixer
  - `Max. mixer 1-4 temp.` - Maximum temperatures for each mixer
  - `Mixer 1-4 room therm.` - Room thermostat settings for each mixer
  - `Mixer 1-4 weather control` - Weather compensation for each mixer
  - `Heating curve. mixer 1-4` - Heating curves for each mixer
  - `Mixer 1-4 support` - Support settings for each mixer

### ⚙️ **Control & Regulation (80-119)**
- **Fuzzy Logic:**
  - `Parametr A FuzzyLogic` - Fuzzy logic parameter A
  - `Parametr B FuzzyLogic` - Fuzzy logic parameter B
  - `Parametr C FuzzyLogic` - Fuzzy logic parameter C

- **Lambda Sensor:**
  - `Parameter A Lambda` - Lambda sensor parameter A
  - `Parameter B Lambda` - Lambda sensor parameter B
  - `Parameter C Lambda` - Lambda sensor parameter C
  - `100% Oxygen` - Full power oxygen level
  - `50% Oxygen` - Half power oxygen level
  - `30% Oxygen` - Low power oxygen level
  - `FL Oxygen correction` - Fuzzy logic oxygen correction

- **Regulation:**
  - `Regulation mode` - Overall regulation mode
  - `Airflow power correction 100%/50%/30%` - Power corrections for different levels
  - `100%/50%/30% feeder work correction` - Feeder corrections for different levels

### 🔧 **System Configuration (120-159)**
- **Pump Control:**
  - `CH pump activation temperature` - Central heating pump activation
  - `CH pump standstill when loading HUW` - Pump behavior during hot water loading
  - `Circulating pump standstill time` - Pump off time
  - `Circulating pump operation time` - Pump on time
  - `Boiler pump lock` - Pump lockout settings

- **Thermostat Control:**
  - `Thermostat select.` (5 instances) - Thermostat selection options
  - `Off by thermostat` (4 instances) - Thermostat off settings
  - `Thermostat lock` - Thermostat lockout
  - `Boiler lock from thermostate` - Boiler lockout from thermostat

- **Advanced Features:**
  - `SUMMER mode` - Summer operation mode
  - `SUMMER mode act. temperature` - Summer mode activation temperature
  - `SUMMER mode deact. temperature` - Summer mode deactivation temperature
  - `Buffer support:` - Buffer tank support
  - `Reserve boiler` - Backup boiler settings

### 🚨 **Safety & Monitoring (160-164)**
- **Safety Features:**
  - `Alarm level` - Alarm threshold settings
  - `No fuel detection time` - Fuel detection timeout
  - `Max.burner temp.` - Maximum burner temperature
  - `Ex.temp.w.no fuel` - Exhaust temperature without fuel
  - `Fan rotation detection` - Fan monitoring
  - `Feeder sensor mode` - Feeder sensor configuration

- **System Status:**
  - `Show advanced setup` - Advanced configuration display
  - `Alarms` - Alarm system configuration

## Key Insights

### 🎯 **Parameter Organization**
1. **Sequential Indexing:** Parameters are organized in logical groups with sequential numbering
2. **Power Levels:** Clear distinction between 100%, 50%, and 30% power settings
3. **Mixer Circuits:** Comprehensive support for up to 4 mixer circuits with full parameter sets
4. **Safety First:** Multiple safety parameters for fuel detection, temperature limits, and monitoring

### 🔍 **Integration Opportunities**
1. **Temperature Control:** 4 mixer circuits with full temperature control capabilities
2. **Power Management:** Granular control over different power levels (100%, 50%, 30%)
3. **Safety Monitoring:** Comprehensive safety and monitoring parameters
4. **Advanced Control:** Fuzzy logic, lambda sensor, and weather compensation support

### 📊 **Parameter Count by Category**
- **Boiler Control:** ~40 parameters
- **Temperature Control:** ~40 parameters  
- **Control & Regulation:** ~40 parameters
- **System Configuration:** ~40 parameters
- **Safety & Monitoring:** ~5 parameters

## Home Assistant Integration Recommendations

### 🚀 **HIGH PRIORITY**
1. **Temperature Sensors:** Implement all 4 mixer temperature sensors
2. **Boiler Control:** Temperature setpoints and power levels
3. **Safety Monitoring:** Alarm levels and safety parameters
4. **Hot Water Control:** HUW temperature and pump settings

### 🔧 **MEDIUM PRIORITY**
1. **Mixer Circuits:** Full mixer circuit control and monitoring
2. **Lambda Sensor:** Oxygen level monitoring and control
3. **Fuzzy Logic:** Advanced control parameters
4. **Weather Compensation:** Weather-based temperature control

### ⚙️ **LOW PRIORITY**
1. **Advanced Setup:** Configuration display options
2. **System Status:** Detailed system monitoring
3. **Maintenance:** Cleaning and maintenance parameters
4. **Diagnostics:** System diagnostic parameters

## Next Steps

1. **Test Additional Endpoints:** Continue testing other `rm*` endpoints locally
2. **Parameter Mapping:** Map parameter names to their corresponding values and units
3. **Control Implementation:** Implement parameter modification capabilities
4. **Safety Integration:** Integrate safety monitoring and alarm systems
5. **Advanced Features:** Implement fuzzy logic and lambda sensor support

This local testing provides **real-world validation** of the API endpoints and shows the actual parameter structure of your ecoMAX810P-L device, which is invaluable for accurate Home Assistant integration.
