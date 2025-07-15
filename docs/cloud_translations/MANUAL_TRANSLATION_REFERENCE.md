# Manual Cloud Translation Reference

This document contains key translations manually extracted from the official econet24.com cloud service.
These translations can be used as a reference when adding new entities to the Home Assistant integration.

## Key Sensor Translations

### Temperature Sensors

| Key | English | Polish | Description |
|-----|---------|--------|-------------|
| `tempCO` | Boiler temperature | Temperatura kotła | Main boiler temperature |
| `tempCWU` | HUW temperature | Temperatura CWU | Hot water temperature |
| `tempBack` | Return temperature | Temperatura powrotu | Return water temperature |
| `tempExternalSensor` | Outside temperature | Temperatura zewnętrzna | External temperature sensor |
| `tempFlueGas` | Flue gas temperature | Temperatura spalin | Exhaust gas temperature |
| `tempFeeder` | Feeder temperature | Temperatura podajnika | Fuel feeder temperature |
| `tempUpperBuffer` | Upper buffer temperature | Temperatura bufora górna | Upper buffer tank temperature |
| `tempLowerBuffer` | Lower buffer temperature | Temperatura bufora dolna | Lower buffer tank temperature |
| `tempUpperSolar` | Upper solar temperature | Temperatura solara górna | Upper solar collector temperature |
| `tempLowerSolar` | Lower solar temperature | Temperatura solara dolna | Lower solar collector temperature |
| `tempFireplace` | Fireplace temperature | Temperatura kominka | Fireplace temperature |
| `tempOpticalSensor` | Flame | Płomień | Optical flame sensor |
| `tempAirIn` | Intake air temperature | Temperatura powietrza wlotowego | Air intake temperature |
| `tempAirOut` | Exhaust air temperature | Temperatura powietrza wylotowego | Air exhaust temperature |
| `tempExchanger` | Exchanger temperature | Temperatura wymiennika | Heat exchanger temperature |

### Room Temperature Sensors (ecoSTER)

| Key | English | Polish | Description |
|-----|---------|--------|-------------|
| `ecoSterTemp1` | Room temperature 1 | Temperatura pokojowa 1 | Room temperature sensor 1 |
| `ecoSterTemp2` | Room temperature 2 | Temperatura pokojowa 2 | Room temperature sensor 2 |
| `ecoSterTemp3` | Room temperature 3 | Temperatura pokojowa 3 | Room temperature sensor 3 |
| `ecoSterTemp4` | Room temperature 4 | Temperatura pokojowa 4 | Room temperature sensor 4 |
| `ecoSterTemp5` | Room temperature 5 | Temperatura pokojowa 5 | Room temperature sensor 5 |
| `ecoSterTemp6` | Room temperature 6 | Temperatura pokojowa 6 | Room temperature sensor 6 |
| `ecoSterTemp7` | Room temperature 7 | Temperatura pokojowa 7 | Room temperature sensor 7 |
| `ecoSterTemp8` | Room temperature 8 | Temperatura pokojowa 8 | Room temperature sensor 8 |

### Circuit Temperature Sensors

| Key | English | Polish | Description |
|-----|---------|--------|-------------|
| `circuitTemp1` | Circuit 1 temperature | Temperatura obiegu 1 | Heating circuit 1 temperature |
| `circuitTemp2` | Circuit 2 temperature | Temperatura obiegu 2 | Heating circuit 2 temperature |
| `circuitTemp3` | Circuit 3 temperature | Temperatura obiegu 3 | Heating circuit 3 temperature |
| `circuitTemp4` | Circuit 4 temperature | Temperatura obiegu 4 | Heating circuit 4 temperature |
| `circuitTemp5` | Circuit 5 temperature | Temperatura obiegu 5 | Heating circuit 5 temperature |
| `circuitTemp6` | Circuit 6 temperature | Temperatura obiegu 6 | Heating circuit 6 temperature |
| `circuitTemp7` | Circuit 7 temperature | Temperatura obiegu 7 | Heating circuit 7 temperature |
| `circuitTemp8` | Circuit 8 temperature | Temperatura obiegu 8 | Heating circuit 8 temperature |

### Mixer Temperature Sensors

| Key | English | Polish | Description |
|-----|---------|--------|-------------|
| `mixerTemp1` | Mixer 1 temperature | Temperatura mieszacza 1 | Mixing valve 1 temperature |
| `mixerTemp2` | Mixer 2 temperature | Temperatura mieszacza 2 | Mixing valve 2 temperature |
| `mixerTemp3` | Mixer 3 temperature | Temperatura mieszacza 3 | Mixing valve 3 temperature |
| `mixerTemp4` | Mixer 4 temperature | Temperatura mieszacza 4 | Mixing valve 4 temperature |
| `mixerTemp5` | Mixer 5 temperature | Temperatura mieszacza 5 | Mixing valve 5 temperature |
| `mixerTemp6` | Mixer 6 temperature | Temperatura mieszacza 6 | Mixing valve 6 temperature |
| `mixerTemp7` | Mixer 7 temperature | Temperatura mieszacza 7 | Mixing valve 7 temperature |
| `mixerTemp8` | Mixer 8 temperature | Temperatura mieszacza 8 | Mixing valve 8 temperature |

### Other Sensors

| Key | English | Polish | Description |
|-----|---------|--------|-------------|
| `fuelLevel` | Fuel level | Poziom paliwa | Fuel tank level |
| `lambdaLevel` | Lambda - oxygen level | Lambda - poziom tlenu | Lambda sensor oxygen level |
| `pressure` | Pressure | Ciśnienie | System pressure |
| `fanPower` | Fan output | Moc nadmuchu | Fan power output |
| `boilerPower` | Boiler output | Moc kotła | Boiler power output |
| `fuelStream` | Fuel stream | Strumień paliwa | Fuel flow rate |

## Binary Sensors

### Status Sensors

| Key | English | Polish | Description |
|-----|---------|--------|-------------|
| `lambdaStatus` | Lambda status | Status Lambda | Lambda sensor status |
| `thermostat` | Thermostat | Termostat | Thermostat contact status |
| `statusCO` | Central heating status | Status CO | Central heating status |
| `statusCWU` | Hot water status | Status CWU | Hot water status |

### Operation Mode Sensors

| Key | English | Polish | Description |
|-----|---------|--------|-------------|
| `mode` | Operation mode | Tryb pracy | Current operation mode |
| `work_mode` | Operation mode | Tryb pracy | Work mode status |
| `lighting` | Fire up | Rozpalanie | Boiler ignition status |
| `work` | Work | Praca | Boiler working status |
| `extinction` | Burning OFF | Wygaszanie | Boiler extinction status |
| `cleaning` | Cleaning | Czyszczenie | Boiler cleaning status |
| `supervision` | Supervision | Nadzór | Boiler supervision status |

## Switches

### Control Switches

| Key | English | Polish | Description |
|-----|---------|--------|-------------|
| `boiler_control` | Boiler control | Sterowanie kotłem | Boiler control switch |
| `boiler_control_on` | Turn on boiler | Włącz kocioł | Turn boiler on |
| `boiler_control_off` | Turn off boiler | Wyłącz kocioł | Turn boiler off |
| `lambda_start` | START | START | Lambda sensor start |
| `lambda_stop` | STOP | STOP | Lambda sensor stop |

## Common UI Elements

| Key | English | Polish | Description |
|-----|---------|--------|-------------|
| `save` | Save | Zapisz | Save button |
| `cancel` | Cancel | Anuluj | Cancel button |
| `ok` | OK | OK | OK button |
| `refresh` | Refresh | Odśwież | Refresh button |
| `update` | Update | Aktualizuj | Update button |
| `error` | Error! | Błąd! | Error message |
| `loading` | Loading... | Ładowanie... | Loading message |

## Boiler Types

| Key | English | Polish | Description |
|-----|---------|--------|-------------|
| `boiler_gas` | Gas boiler | Kocioł gazowy | Gas boiler |
| `boiler_oil` | Oil boiler | Kocioł olejowy | Oil boiler |
| `boiler_gas_oil` | Gas/oil boiler | Kocioł gazowy/olejowy | Gas/oil boiler |
| `pellet_boiler` | Pellet boiler | Kocioł peletowy | Pellet boiler |
| `boiler_electric` | Electric boiler | Kocioł elektryczny | Electric boiler |

## Operation Modes

| Key | English | Polish | Description |
|-----|---------|--------|-------------|
| `auto` | Auto | Auto | Automatic mode |
| `auto_eco` | Auto-Eco | Auto-Eco | Automatic eco mode |
| `day` | Day | Dzień | Day mode |
| `night` | Night | Noc | Night mode |
| `summer_mode` | Summer mode | Tryb LATO | Summer mode |
| `mode_schedule` | Schedule mode | Tryb harmonogram | Schedule mode |
| `mode_eco` | Economy mode | Tryb ekonomiczny | Economy mode |
| `mode_comfort` | Comfort mode | Tryb komfortowy | Comfort mode |

## Parameters

| Key | English | Polish | Description |
|-----|---------|--------|-------------|
| `parameters` | Parameters | Parametry | Parameters |
| `user_parameters` | User parameters | Parametry użytkownika | User parameters |
| `service_parameters` | Service parameters | Parametry serwisowe | Service parameters |
| `boiler_settings` | Boiler settings | Ustawienia kotła | Boiler settings |
| `cwu_settings` | HUW settings | Ustawienia CWU | Hot water settings |

## Usage Guidelines

1. **For new sensors**: Use the exact key from this reference when adding new entities
2. **Translation format**: Follow the pattern `key_name` → `Key Name` for English
3. **Polish translations**: Use the provided Polish translations for consistency
4. **Device classes**: Choose appropriate device classes based on the sensor type
5. **Icons**: Select appropriate icons based on the measurement type

## Example Implementation

When adding a new temperature sensor:

```python
# In const.py
SENSOR_TEMP_CO = "tempCO"

# In strings.json
{
  "entity": {
    "sensor": {
      "temp_co": {
        "name": "Boiler Temperature"
      }
    }
  }
}

# In translations/en.json
{
  "entity": {
    "sensor": {
      "temp_co": {
        "name": "Boiler Temperature"
      }
    }
  }
}

# In translations/pl.json
{
  "entity": {
    "sensor": {
      "temp_co": {
        "name": "Temperatura kotła"
      }
    }
  }
}
```

This reference ensures consistent naming and translations across the integration. 