---
description: Home Assistant Entity Type Selection Guidelines
globs:
alwaysApply: true
---

# Home Assistant Entity Type Selection Guidelines

## 🎯 **CRITICAL: Always Check Entity Type Before Implementation**

Before implementing any new entity, ALWAYS determine the correct entity type based on these guidelines.

## 📊 **Entity Type Decision Matrix**

### **Binary Sensor** (`BinarySensorEntity`)
**Use when:**
- ✅ Data represents ON/OFF states
- ✅ Boolean values (true/false, 1/0, yes/no)
- ✅ Status indicators (running/stopped, connected/disconnected)
- ✅ Presence detection (occupied/vacant, detected/not detected)

**Examples:**
- Pump status (running/stopped)
- Fan status (on/off)
- Alarm status (active/inactive)
- Connectivity status (connected/disconnected)
- Door/window sensors (open/closed)

**Device Classes:**
- `CONNECTIVITY` - Network, WiFi, LAN status
- `RUNNING` - Pumps, fans, motors
- `PROBLEM` - Alarms, errors, warnings
- `OCCUPANCY` - Motion, presence
- `OPENING` - Doors, windows, covers

### **Sensor** (`SensorEntity`)
**Use when:**
- ✅ Data represents measurements or values
- ✅ Numeric readings (temperature, pressure, humidity)
- ✅ Text descriptions or states
- ✅ Enum values that are read-only
- ✅ Calculated values or statistics

**Examples:**
- Temperature readings (22.5°C)
- Pressure values (1.2 bar)
- Humidity levels (65%)
- Status descriptions ("Running", "Stopped")
- Alarm codes (7) or descriptions ("Boiler temperature exceeded")
- Version numbers ("3.2.3879")

**Device Classes:**
- `TEMPERATURE` - Temperature sensors
- `POWER` - Power consumption
- `SIGNAL_STRENGTH` - Signal quality
- `ENUM` - Discrete text values
- `TIMESTAMP` - Time values

### **Number** (`NumberEntity`)
**Use when:**
- ✅ User can SET/CHANGE the value
- ✅ Numeric values with min/max limits
- ✅ Configuration parameters
- ✅ Setpoints or target values

**Examples:**
- Temperature setpoints (target temperature)
- Pressure setpoints
- Timer values
- Configuration limits

**Device Classes:**
- `TEMPERATURE` - Temperature setpoints
- `PRESSURE` - Pressure setpoints
- `DURATION` - Time settings

### **Switch** (`SwitchEntity`)
**Use when:**
- ✅ User can TURN ON/OFF something
- ✅ Control actions (start/stop, enable/disable)
- ✅ Boolean control (true/false)

**Examples:**
- Boiler ON/OFF control
- Pump start/stop
- System enable/disable
- Feature toggles

### **Select** (`SelectEntity`)
**Use when:**
- ✅ User can CHOOSE from predefined options
- ✅ Multiple discrete choices
- ✅ Mode selection
- ✅ Configuration options

**Examples:**
- Operation modes (Auto, Manual, Schedule)
- Season modes (Summer, Winter, Auto)
- Control algorithms
- Sensor types

## 🚫 **Common Mistakes to Avoid**

### **❌ DON'T use Binary Sensor for:**
- Numeric values (use Sensor)
- User-controllable values (use Switch/Number)
- Text descriptions (use Sensor with ENUM device class)

### **❌ DON'T use Sensor for:**
- User-controllable values (use Number/Select)
- Simple ON/OFF states (use Binary Sensor)

### **❌ DON'T use Switch for:**
- Read-only status (use Binary Sensor)
- Numeric values (use Number)
- Multiple choice options (use Select)

### **❌ DON'T use Number for:**
- Read-only measurements (use Sensor)
- ON/OFF states (use Binary Sensor)
- Multiple choice options (use Select)

## 🔍 **Decision Flow Chart**

```
Is the data user-controllable?
├─ YES → Is it numeric with min/max?
│   ├─ YES → Use Number
│   └─ NO → Is it multiple choice?
│       ├─ YES → Use Select
│       └─ NO → Use Switch
└─ NO → Is it ON/OFF state?
    ├─ YES → Use Binary Sensor
    └─ NO → Is it numeric/text value?
        ├─ YES → Use Sensor
        └─ NO → Use Sensor (default)
```

## 📋 **Checklist Before Implementation**

Before creating any entity, ask:

1. **Is this user-controllable?**
   - YES → Number, Select, or Switch
   - NO → Binary Sensor or Sensor

2. **What type of data is it?**
   - Boolean (ON/OFF) → Binary Sensor
   - Numeric measurement → Sensor
   - Numeric setpoint → Number
   - Text description → Sensor
   - Multiple choice → Select
   - Control action → Switch

3. **What device class should it use?**
   - Check Home Assistant documentation for appropriate device class
   - Use `None` if no specific device class applies

4. **What entity category should it use?**
   - `DIAGNOSTIC` - System information, versions, status
   - `CONFIG` - Configuration parameters
   - `None` - Primary functionality

## 🎯 **Examples from ecoNET-300 Integration**

### **✅ Correct Implementations:**

**Binary Sensors:**
- `alarm_active` - Boolean alarm status
- `pump_co_works` - Boolean pump status
- `fan_works` - Boolean fan status

**Sensors:**
- `temp_co` - Temperature measurement
- `alarm_code` - Numeric alarm code
- `alarm_description` - Text alarm description
- `soft_ver` - Version string

**Numbers:**
- `temp_co_set` - Temperature setpoint (user-controllable)
- `temp_cwu_set` - Hot water setpoint (user-controllable)

**Switches:**
- `boiler_control` - Boiler ON/OFF control

## 📚 **Reference Links**

- [Home Assistant Entity Documentation](https://developers.home-assistant.io/docs/core/entity)
- [Binary Sensor Documentation](https://developers.home-assistant.io/docs/core/entity/binary-sensor)
- [Sensor Documentation](https://developers.home-assistant.io/docs/core/entity/sensor)
- [Number Documentation](https://developers.home-assistant.io/docs/core/entity/number)
- [Switch Documentation](https://developers.home-assistant.io/docs/core/entity/switch)
- [Select Documentation](https://developers.home-assistant.io/docs/core/entity/select)

## ⚠️ **Remember**

**ALWAYS** check this guide before implementing any new entity to avoid mistakes and ensure proper Home Assistant integration standards.
