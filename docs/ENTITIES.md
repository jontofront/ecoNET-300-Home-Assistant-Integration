# Entity Reference

Complete reference for all entities provided by the ecoNET300 Home Assistant Integration.

## Overview

| Type           | Count | Description                       |
| -------------- | ----- | --------------------------------- |
| Sensors        | 50+   | Temperature, status, system info  |
| Binary Sensors | 25+   | Pumps, fans, connections, alarms  |
| Events         | 1     | Boiler alarm triggered / cleared  |
| Switches       | 1     | Boiler ON/OFF control             |
| Select         | 1     | Heater mode (Winter/Summer/Auto)  |
| Number         | 15+   | Temperature setpoints             |

---

## Switches

The integration provides a boiler control switch that allows you to turn the boiler ON and OFF directly from Home Assistant.

| Entity Key       | Description                  | Control                    | State Detection  |
| ---------------- | ---------------------------- | -------------------------- | ---------------- |
| `boiler_control` | Boiler ON/OFF control switch | `BOILER_CONTROL` parameter | `mode` parameter |

**Features:**

- **Direct Control**: Turn boiler ON/OFF with a simple switch
- **State Synchronization**: Switch state reflects actual boiler operation mode
- **API Integration**: Uses the ecoNET-300's native `BOILER_CONTROL` parameter
- **Real-time Updates**: Switch state updates based on current boiler mode

---

## Select Entities

The integration provides a heater mode selector that allows you to control the boiler operation mode directly from Home Assistant.

| Entity Key    | Description                    | Options              | API Parameter |
| ------------- | ------------------------------ | -------------------- | ------------- |
| `heater_mode` | Heater operation mode selector | Winter, Summer, Auto | Parameter 55  |

**Features:**

- **Winter Mode**: Full heating operation for cold weather
- **Summer Mode**: Hot water only operation for warm weather
- **Auto Mode**: Automatic mode selection based on conditions
- **Real-time Sync**: Mode selection reflects actual boiler operation
- **API Integration**: Uses ecoNET-300's native parameter 55

---

## Sensors

These sensors are retrieved from the `../econet/regParams` and `../econet/sysParams` endpoints.

### Boiler and Heating

| Entity Key      | Description                | Endpoint              |
| --------------- | -------------------------- | --------------------- |
| `boilerPower`   | Boiler output              | `../econet/regParams` |
| `boilerPowerKW` | Boiler power               | `../econet/regParams` |
| `tempCO`        | Heating temperature        | `../econet/regParams` |
| `tempCOSet`     | Heating target temperature | `../econet/regParams` |
| `tempBack`      | Return temperature         | `../econet/regParams` |
| `statusCO`      | Central heating status     | `../econet/regParams` |

### Hot Water (CWU)

| Entity Key   | Description                  | Endpoint              |
| ------------ | ---------------------------- | --------------------- |
| `tempCWU`    | Water heater temperature     | `../econet/regParams` |
| `tempCWUSet` | Water heater set temperature | `../econet/regParams` |
| `statusCWU`  | Water heater status          | `../econet/regParams` |

### Temperature Sensors

| Entity Key           | Description              | Endpoint              |
| -------------------- | ------------------------ | --------------------- |
| `tempFeeder`         | Feeder temperature       | `../econet/regParams` |
| `tempFlueGas`        | Flue gas temperature     | `../econet/regParams` |
| `tempExternalSensor` | Outside temperature      | `../econet/regParams` |
| `tempLowerBuffer`    | Lower buffer temperature | `../econet/regParams` |
| `tempUpperBuffer`    | Upper buffer temperature | `../econet/regParams` |

### Mixer Temperatures

| Entity Key   | Description         | Endpoint              |
| ------------ | ------------------- | --------------------- |
| `mixerTemp1` | Mixer 1 temperature | `../econet/regParams` |
| `mixerTemp2` | Mixer 2 temperature | `../econet/regParams` |
| `mixerTemp3` | Mixer 3 temperature | `../econet/regParams` |
| `mixerTemp4` | Mixer 4 temperature | `../econet/regParams` |
| `mixerTemp5` | Mixer 5 temperature | `../econet/regParams` |
| `mixerTemp6` | Mixer 6 temperature | `../econet/regParams` |

### System Status

| Entity Key   | Description | Endpoint              |
| ------------ | ----------- | --------------------- |
| `mode`       | Boiler mode | `../econet/regParams` |
| `fanPower`   | Fan power   | `../econet/regParams` |
| `thermostat` | Thermostat  | `../econet/regParams` |

### Fuel and Consumption

| Entity Key   | Description      | Endpoint              |
| ------------ | ---------------- | --------------------- |
| `fuelLevel`  | Fuel level       | `../econet/regParams` |
| `fuelConsum` | Fuel consumption | `../econet/regParams` |
| `fuelStream` | Fuel stream      | `../econet/regParams` |

### ecoSTER Room Thermostats

| Entity Key     | Description            | Endpoint              |
| -------------- | ---------------------- | --------------------- |
| `ecosterTemp1` | Room temperature 1     | `../econet/regParams` |
| `ecosterTemp2` | Room temperature 2     | `../econet/regParams` |
| `ecosterTemp3` | Room temperature 3     | `../econet/regParams` |
| `ecosterTemp4` | Room temperature 4     | `../econet/regParams` |
| `ecosterTemp5` | Room temperature 5     | `../econet/regParams` |
| `ecosterTemp6` | Room temperature 6     | `../econet/regParams` |
| `ecosterTemp7` | Room temperature 7     | `../econet/regParams` |
| `ecosterTemp8` | Room temperature 8     | `../econet/regParams` |
| `ecosterMode1` | Room thermostat 1 mode | `../econet/regParams` |
| `ecosterMode2` | Room thermostat 2 mode | `../econet/regParams` |
| `ecosterMode3` | Room thermostat 3 mode | `../econet/regParams` |
| `ecosterMode4` | Room thermostat 4 mode | `../econet/regParams` |
| `ecosterMode5` | Room thermostat 5 mode | `../econet/regParams` |
| `ecosterMode6` | Room thermostat 6 mode | `../econet/regParams` |
| `ecosterMode7` | Room thermostat 7 mode | `../econet/regParams` |
| `ecosterMode8` | Room thermostat 8 mode | `../econet/regParams` |

### Lambda Sensor Module

| Entity Key     | Description   | Endpoint              |
| -------------- | ------------- | --------------------- |
| `lambdaStatus` | Lambda status | `../econet/regParams` |
| `lambdaSet`    | Lambda set    | `../econet/regParams` |
| `lambdaLevel`  | Lambda level  | `../econet/regParams` |

### ecoSOL 500 Solar System

| Entity Key        | Description                               | Endpoint              |
| ----------------- | ----------------------------------------- | --------------------- |
| `T1`              | Collector Temperature                     | `../econet/regParams` |
| `T2`              | Tank Temperature                          | `../econet/regParams` |
| `T3`              | Tank Temperature                          | `../econet/regParams` |
| `T4`              | Return Temperature                        | `../econet/regParams` |
| `T5`              | Collector Temperature - Power Measurement | `../econet/regParams` |
| `T6`              | Temperature Sensor                        | `../econet/regParams` |
| `TzCWU`           | Hot Water Temperature                     | `../econet/regParams` |
| `P1`              | Pump 1 Status                             | `../econet/regParams` |
| `P2`              | Pump 2 Status                             | `../econet/regParams` |
| `H`               | Output Status                             | `../econet/regParams` |
| `Uzysk_ca_kowity` | Total Heat Output                         | `../econet/regParams` |

### System Information

| Entity Key             | Description            | Endpoint              |
| ---------------------- | ---------------------- | --------------------- |
| `quality`              | Signal quality         | `../econet/sysParams` |
| `signal`               | Signal strength        | `../econet/sysParams` |
| `softVer`              | Module ecoNET version  | `../econet/sysParams` |
| `controllerID`         | Controller name        | `../econet/sysParams` |
| `moduleASoftVer`       | Module A version       | `../econet/sysParams` |
| `moduleBSoftVer`       | Module B version       | `../econet/sysParams` |
| `moduleCSoftVer`       | Module C version       | `../econet/sysParams` |
| `moduleLambdaSoftVer`  | Module Lambda version  | `../econet/sysParams` |
| `modulePanelSoftVer`   | Module Panel version   | `../econet/sysParams` |
| `moduleEcoSTERSoftVer` | Module ecoSTER version | `../econet/sysParams` |
| `transmission`         | Transmission           | `../econet/regParams` |

---

## Binary Sensors

> **Connected vs. running convention.** In the ecoNET protocol many components
> expose a pair of boolean keys: a base key (e.g. `pumpCO`, `fan`, `blowFan1`)
> meaning the component is *connected/present*, and a `*Works`/`*Active`
> counterpart (e.g. `pumpCOWorks`, `fanWorks`, `blowFan1Active`) meaning it is
> *running right now*. The integration only exposes the running-state key as a
> `RUNNING` binary sensor; the base "connected" boolean is filtered out of the
> sensor sweep to avoid duplicated entities.

### Pump Status

| Entity Key             | Description                  | Endpoint              |
| ---------------------- | ---------------------------- | --------------------- |
| `pumpCOWorks`          | Central heating pump working | `../econet/regParams` |
| `pumpCWUWorks`         | Hot water pump working       | `../econet/regParams` |
| `pumpSolarWorks`       | Solar pump working           | `../econet/regParams` |
| `pumpCirculationWorks` | Circulation pump working     | `../econet/regParams` |
| `pumpFireplaceWorks`   | Fireplace pump working       | `../econet/regParams` |

### Fan Status

| Entity Key         | Description  | Endpoint              |
| ------------------ | ------------ | --------------------- |
| `fanWorks`         | Fan working  | `../econet/regParams` |
| `fan2ExhaustWorks` | Exhaust fan  | `../econet/regParams` |
| `blowFan1Active`   | Blower fan 1 | `../econet/regParams` |
| `blowFan2Active`   | Blower fan 2 | `../econet/regParams` |

### Feeders and Outputs

| Entity Key               | Description       | Endpoint              |
| ------------------------ | ----------------- | --------------------- |
| `feederOuterWorks`       | Outer feeder      | `../econet/regParams` |
| `feeder2AdditionalWorks` | Additional feeder | `../econet/regParams` |
| `outerBoilerWorks`       | Outer boiler      | `../econet/regParams` |
| `alarmOutputWorks`       | Alarm output      | `../econet/regParams` |

### System Components

| Entity Key     | Description      | Endpoint              |
| -------------- | ---------------- | --------------------- |
| `lighterWorks` | Lighter working  | `../econet/regParams` |
| `feederWorks`  | Feeder working   | `../econet/regParams` |
| `thermostat`   | Thermostat       | `../econet/regParams` |
| `statusCWU`    | Hot water status | `../econet/regParams` |

### Network and Communication

| Entity Key | Description         | Endpoint              |
| ---------- | ------------------- | --------------------- |
| `mainSrv`  | Econet24.com server | `../econet/regParams` |
| `wifi`     | Wi-Fi connection    | `../econet/regParams` |
| `lan`      | LAN connection      | `../econet/regParams` |

### ecoMAX850R2-X Specific

| Entity Key         | Description        | Endpoint              |
| ------------------ | ------------------ | --------------------- |
| `contactGZC`       | GZC contact        | `../econet/regParams` |
| `contactGZCActive` | GZC contact active | `../econet/regParams` |

### ecoSTER Room Thermostats

| Entity Key         | Description                    | Endpoint              |
| ------------------ | ------------------------------ | --------------------- |
| `ecosterContacts1` | Room thermostat 1 contacts     | `../econet/regParams` |
| `ecosterContacts2` | Room thermostat 2 contacts     | `../econet/regParams` |
| `ecosterContacts3` | Room thermostat 3 contacts     | `../econet/regParams` |
| `ecosterContacts4` | Room thermostat 4 contacts     | `../econet/regParams` |
| `ecosterContacts5` | Room thermostat 5 contacts     | `../econet/regParams` |
| `ecosterContacts6` | Room thermostat 6 contacts     | `../econet/regParams` |
| `ecosterContacts7` | Room thermostat 7 contacts     | `../econet/regParams` |
| `ecosterContacts8` | Room thermostat 8 contacts     | `../econet/regParams` |
| `ecosterDaySched1` | Room thermostat 1 day schedule | `../econet/regParams` |
| `ecosterDaySched2` | Room thermostat 2 day schedule | `../econet/regParams` |
| `ecosterDaySched3` | Room thermostat 3 day schedule | `../econet/regParams` |
| `ecosterDaySched4` | Room thermostat 4 day schedule | `../econet/regParams` |
| `ecosterDaySched5` | Room thermostat 5 day schedule | `../econet/regParams` |
| `ecosterDaySched6` | Room thermostat 6 day schedule | `../econet/regParams` |
| `ecosterDaySched7` | Room thermostat 7 day schedule | `../econet/regParams` |
| `ecosterDaySched8` | Room thermostat 8 day schedule | `../econet/regParams` |

### ecoSOL 500 Solar System

| Entity Key            | Description                 | Endpoint              |
| --------------------- | --------------------------- | --------------------- |
| `fuelConsumptionCalc` | Fuel consumption calculator | `../econet/regParams` |
| `ecosrvHttps`         | ecoNET server HTTPS         | `../econet/regParams` |

---

## Number Entities

### Temperature Setpoints

| Entity Key   | Description                          | Endpoint              |
| ------------ | ------------------------------------ | --------------------- |
| `tempCOSet`  | Central heating temperature setpoint | `../econet/regParams` |
| `tempCWUSet` | Hot water temperature setpoint       | `../econet/regParams` |

### Mixer Temperature Setpoints

| Entity Key      | Description                | Endpoint              |
| --------------- | -------------------------- | --------------------- |
| `mixerSetTemp1` | Mixer 1 target temperature | `../econet/regParams` |
| `mixerSetTemp2` | Mixer 2 target temperature | `../econet/regParams` |
| `mixerSetTemp3` | Mixer 3 target temperature | `../econet/regParams` |
| `mixerSetTemp4` | Mixer 4 target temperature | `../econet/regParams` |
| `mixerSetTemp5` | Mixer 5 target temperature | `../econet/regParams` |
| `mixerSetTemp6` | Mixer 6 target temperature | `../econet/regParams` |

### ecoSTER Room Thermostat Setpoints

| Entity Key        | Description                | Endpoint              |
| ----------------- | -------------------------- | --------------------- |
| `ecosterSetTemp1` | Room thermostat 1 setpoint | `../econet/regParams` |
| `ecosterSetTemp2` | Room thermostat 2 setpoint | `../econet/regParams` |
| `ecosterSetTemp3` | Room thermostat 3 setpoint | `../econet/regParams` |
| `ecosterSetTemp4` | Room thermostat 4 setpoint | `../econet/regParams` |
| `ecosterSetTemp5` | Room thermostat 5 setpoint | `../econet/regParams` |
| `ecosterSetTemp6` | Room thermostat 6 setpoint | `../econet/regParams` |
| `ecosterSetTemp7` | Room thermostat 7 setpoint | `../econet/regParams` |
| `ecosterSetTemp8` | Room thermostat 8 setpoint | `../econet/regParams` |

---

## Alarm and Event Entities (v1.2.3+)

| Entity Key     | Platform      | Description                                  | Category   |
| -------------- | ------------- | -------------------------------------------- | ---------- |
| `last_alarm`   | Sensor        | Most recent alarm description                | Diagnostic |
| `alarm_count`  | Sensor        | Total number of alarms (recent 5 in attrs)   | Diagnostic |
| `alarm_active` | Binary Sensor | ON when any alarm is currently active        | Diagnostic |
| `boiler_alarm` | Event         | Fires `alarm_triggered` / `alarm_cleared`    | Diagnostic |

**Full documentation, attributes, and automation examples:**
**[Alarms & Events Guide](ALARMS_AND_EVENTS.md)**

---

## Dynamic Entities (v1.2.0+)

Starting with v1.2.0, the integration also creates dynamic entities from the `mergedData` API endpoint. These include:

- **165+ parameters** from the boiler's remote menu
- **Automatic entity type detection** (Number, Switch, Select, Sensor)
- **Category-based grouping** (CONFIG entities disabled by default)
- **Parameter locking** support with lock icons

For more information about dynamic entities, see [DYNAMIC_ENTITY_VALIDATION.md](DYNAMIC_ENTITY_VALIDATION.md).
