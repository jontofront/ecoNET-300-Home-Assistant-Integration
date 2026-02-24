# Fuel Consumption Tracking

This guide explains how to track fuel consumption using the ecoNET300 integration.

## Built-in Sensors

The integration provides built-in sensors for fuel consumption tracking on supported controllers.

### Fuel Stream Sensor

The `sensor.econet300_fuel_stream` sensor provides the **current fuel consumption rate** in kg/h (kilograms per hour).

| Property             | Value                                          |
| -------------------- | ---------------------------------------------- |
| **Unit**             | kg/h                                           |
| **State Class**      | MEASUREMENT                                    |
| **Update Frequency** | Every coordinator update (default: 60 seconds) |

**Typical values during operation:**

- Idle/Standby: 0 kg/h
- Low power: 0.5 - 1.5 kg/h
- Medium power: 1.5 - 3.0 kg/h
- High power: 3.0 - 5.0+ kg/h

Values depend on your boiler model, fuel type, and heating demand.

### Fuel Consumption Total Sensor (Built-in Meter)

The `sensor.econet300_fuel_consumption_total` sensor automatically tracks **total fuel consumption** in kg.

| Property         | Value                      |
| ---------------- | -------------------------- |
| **Unit**         | kg                         |
| **State Class**  | TOTAL_INCREASING           |
| **Device Class** | econet300\_\_fuel_meter    |
| **Persistence**  | Yes (survives HA restarts) |

This sensor:

- Automatically integrates the fuel stream rate over time
- Persists across Home Assistant restarts
- Uses `TOTAL_INCREASING` state class for long-term statistics
- Can be reset or calibrated using service actions

### Fuel Level Sensor

The `sensor.econet300_fuel_level` sensor shows the fuel hopper level as a percentage.

---

## Service Actions

The integration provides two service actions for managing the fuel consumption meter:

### Reset Fuel Meter

**Service:** `econet300.reset_fuel_meter`

Resets the fuel consumption meter to zero. Use this at the start of a new tracking period.

**Example:**

```yaml
service: econet300.reset_fuel_meter
target:
  entity_id: sensor.econet300_fuel_consumption_total
```

### Calibrate Fuel Meter

**Service:** `econet300.calibrate_fuel_meter`

Sets the fuel consumption meter to a specific value. Useful when you want to sync with external measurements.

**Parameters:**

| Parameter | Type  | Description              |
| --------- | ----- | ------------------------ |
| `value`   | float | The value to set (in kg) |

**Example:**

```yaml
service: econet300.calibrate_fuel_meter
target:
  entity_id: sensor.econet300_fuel_consumption_total
data:
  value: 150.5
```

### Automation Examples

**Reset monthly:**

```yaml
automation:
  - alias: "Reset fuel consumption monthly"
    trigger:
      - platform: time
        at: "00:00:00"
    condition:
      - condition: template
        value_template: "{{ now().day == 1 }}"
    action:
      - service: econet300.reset_fuel_meter
        target:
          entity_id: sensor.econet300_fuel_consumption_total
```

**Reset at season start:**

```yaml
automation:
  - alias: "Reset fuel at heating season start"
    trigger:
      - platform: date
        at: "2025-10-01"
    action:
      - service: econet300.reset_fuel_meter
        target:
          entity_id: sensor.econet300_fuel_consumption_total
```

---

## Utility Meter for Period Tracking

If you want to track consumption per day/week/month without resetting the total, use the Utility Meter helper:

1. Go to **Settings > Devices & Services > Helpers**
2. Click **+ Create Helper**
3. Select **"Utility meter"**
4. Configure:

| Setting               | Value                                     |
| --------------------- | ----------------------------------------- |
| **Name**              | Daily Fuel Consumption                    |
| **Input sensor**      | `sensor.econet300_fuel_consumption_total` |
| **Meter reset cycle** | Daily                                     |

This creates separate daily/weekly/monthly counters while keeping the total intact.

---

## Statistics and History

With `state_class: TOTAL_INCREASING`, Home Assistant automatically tracks:

- **Sum**: Total accumulated consumption
- **Sum Increase**: Consumption added in each period

View statistics in:

- **Developer Tools > Statistics**
- **Energy Dashboard** (with custom cards)
- **History graphs**

---

## Fuel Consumption Calculation

The integration calculates fuel consumption based on:

1. **Fuel Stream Rate** (`fuelStream`) - Current consumption rate in kg/h
2. **Time Delta** - Time between coordinator updates (typically 60 seconds)
3. **Integration** - `total += fuelStream * (time_delta / 3600)`

### Verification Formula

You can verify the fuel stream value makes sense:

```text
Energy Output (kW) = Fuel Stream (kg/h) x Calorific Value (kWh/kg)
```

Example:

- Fuel Stream: 1.35 kg/h
- Calorific Value: 5.0 kWh/kg (typical for pellets)
- Expected Power: 1.35 x 5.0 = 6.75 kW

Compare with `sensor.econet300_boiler_power_kw` to verify accuracy.

---

## Controller Support

The fuel consumption tracking is only available on controllers that support the `fuelStream` parameter:

| Controller    | fuel_stream | Tracking Available |
| ------------- | ----------- | ------------------ |
| ecoMAX860P3-O | Yes         | Yes                |
| ecoMAX860P3-V | Yes         | Yes                |
| ecoMAX860P2-N | Yes         | Yes                |
| ecoMAX850R2-X | Yes         | Yes                |
| SControl MK1  | Yes         | Yes                |
| ecoMAX810P-L  | No (null)   | No                 |
| ecoMAX360     | No          | No                 |

If your controller doesn't support `fuelStream`, the consumption total sensor will not be created.

---

## Dashboard Example

```yaml
type: entities
title: Fuel Consumption
entities:
  - entity: sensor.econet300_fuel_stream
    name: Current Rate
  - entity: sensor.econet300_fuel_consumption_total
    name: Total Consumed
  - entity: sensor.econet300_fuel_level
    name: Hopper Level
```

### Graph Card Example

```yaml
type: custom:mini-graph-card
entities:
  - entity: sensor.econet300_fuel_consumption_total
    name: Total Fuel
  - entity: sensor.econet300_fuel_stream
    name: Current Rate
    y_axis: secondary
hours_to_show: 168
points_per_hour: 1
```

---

## Troubleshooting

### Fuel Stream Shows 0

- Check if the boiler is actively heating
- Verify the boiler is not in standby/supervision mode
- Check the `mode` sensor for current operation state

### Total Not Increasing

- Ensure `fuel_stream` sensor is available and showing values > 0
- Check Home Assistant logs for errors
- Verify the coordinator is updating (check `last_update` attribute)

### Values Seem Incorrect

1. Verify your feeder efficiency setting in the controller
2. Check the fuel calorific value setting
3. Compare with `boiler_power_kw` using the formula above

### Sensor Not Created

- Check if your controller supports `fuelStream` (see support table above)
- Check Home Assistant logs for "fuelStream not available" message

---

## Related Documentation

- [ENTITIES.md](ENTITIES.md) - Complete entity reference
- [DIAGNOSTICS.md](DIAGNOSTICS.md) - Troubleshooting with diagnostics
