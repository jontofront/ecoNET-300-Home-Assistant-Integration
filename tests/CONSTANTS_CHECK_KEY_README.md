# ecoNET300 Constants Check Key Test Documentation

## Overview

The `test_cons_check_key.py` test script is a sophisticated analysis tool that examines fixture files to determine the correct entity types for ecoNET300 Home Assistant integration. It analyzes JSON fixture files to identify which parameters should be binary sensors vs. regular sensors, and checks for mismatches with the current Home Assistant constants configuration.

## Purpose

This test serves several critical functions:

1. **Entity Type Validation**: Determines whether parameters should be binary sensors or regular sensors based on their data types in fixture files
2. **Constants Consistency Check**: Identifies mismatches between fixture data and Home Assistant constants
3. **Configuration Recommendations**: Provides specific guidance on how to fix entity type mismatches
4. **Missing Entity Detection**: Finds parameters that exist in fixtures but are not defined in the Home Assistant integration
5. **Best Practices Enforcement**: Ensures compliance with Home Assistant entity type guidelines

## How It Works

### 1. **Fixture Analysis**

The test analyzes two key fixture files:

- **`regParams.json`**: Contains register parameters with their current values
- **`sysParams.json`**: Contains system parameters with their current values

### 2. **Entity Type Determination**

Based on the data types in the fixture files:

- **Boolean values (True/False)** → **Binary Sensors**
- **Numeric/String values** → **Regular Sensors**

### 3. **Constants Validation**

Compares fixture-derived entity types against Home Assistant constants:

- `ENTITY_BINARY_DEVICE_CLASS_MAP` - Binary sensor mappings
- `ENTITY_SENSOR_DEVICE_CLASS_MAP` - Regular sensor mappings
- `DEFAULT_BINARY_SENSORS` - Default binary sensor list
- `DEFAULT_SENSORS` - Default sensor list

### 4. **Mismatch Detection**

Identifies three types of issues:

- **Wrong Entity Types**: Parameters in wrong constant lists
- **Missing Entities**: Parameters not defined in constants
- **Type Mismatches**: Fixture vs. constants type disagreements

## Test Structure

### **Core Functions**

#### `analyze_entity_types(data: dict)`

- Analyzes JSON data to categorize keys as binary or regular sensors
- Returns two lists: binary sensors and regular sensors

#### `check_entity_type_mismatches()`

- Compares fixture analysis against Home Assistant constants
- Generates detailed mismatch reports and recommendations

#### `print_mismatch_analysis()`

- Displays comprehensive analysis of all detected issues
- Categorizes problems by severity and type

#### `generate_separate_tables()`

- Creates three organized tables for better analysis:
  1. **Missing Entities** - Not in constants
  2. **Type Mismatches** - Different types
  3. **Correctly Configured** - Matching types

### **Analysis Categories**

#### **Binary Sensors (Boolean Values)**

- Connection status (wifi, lan, mainSrv)
- Operational status (pumps, fans, thermostats)
- Contact sensors (doors, windows)
- Presence detection
- Error states

#### **Regular Sensors (Non-Boolean Values)**

- Temperature measurements
- Pressure readings
- Power consumption
- Version numbers
- Configuration values
- Status codes

## Usage Instructions

### **Running the Test**

```bash
# From the project root directory
python tests/test_cons_check_key.py

# Or from the tests directory
cd tests
python test_cons_check_key.py
```

### **Expected Output**

The test provides comprehensive output including:

1. **Fixture Analysis Results**

   - Binary sensor counts and lists
   - Regular sensor counts and lists
   - Combined analysis summary

2. **Entity Type Mismatches**

   - Wrong entity type assignments
   - Missing entity definitions
   - Specific recommendations for fixes

3. **Home Assistant Guidelines**

   - Best practices for entity types
   - Device class recommendations
   - Configuration examples

4. **Generated Reports**
   - `fixture_entity_analysis.txt` - Detailed analysis report
   - `separate_tables_analysis.txt` - Organized table format

### **Generated Files**

#### **`fixture_entity_analysis.txt`**

- Complete analysis of both fixture files
- Entity type breakdowns
- Mismatch details and recommendations

#### **`separate_tables_analysis.txt`**

- Three organized tables for easy reference
- Missing entities, type mismatches, and correct configurations
- Summary statistics

## Home Assistant Guidelines

### **Binary Sensor Best Practices**

Binary sensors should be used for:

- **On/Off states** (True/False values)
- **Connection status** (wifi, lan, mainSrv)
- **Operational status** (pumps, fans, thermostats)
- **Contact sensors** (doors, windows)
- **Presence detection**
- **Error states**

**Recommended Device Classes:**

- `BinarySensorDeviceClass.CONNECTIVITY` - for wifi, lan, mainSrv
- `BinarySensorDeviceClass.RUNNING` - for operational status
- `BinarySensorDeviceClass.PRESENCE` - for presence detection
- `BinarySensorDeviceClass.OPENING` - for contact sensors

### **Regular Sensor Best Practices**

Regular sensors should be used for:

- **Temperature measurements** (numeric values)
- **Pressure readings** (numeric values)
- **Power consumption** (numeric values)
- **Version numbers** (string values)
- **Configuration values** (numeric/string)
- **Status codes** (non-boolean values)

**Recommended Device Classes:**

- `SensorDeviceClass.TEMPERATURE` - for temperature values
- `SensorDeviceClass.POWER` - for power measurements
- `SensorDeviceClass.SIGNAL_STRENGTH` - for signal quality
- `None` - for version numbers, status codes, etc.

## Integration with Development Workflow

### **When to Run This Test**

1. **After Adding New Fixtures**: When new device fixture files are added
2. **Before Constants Updates**: Before modifying `const.py` entity definitions
3. **During Code Reviews**: To ensure entity type consistency
4. **After Device Support**: When adding support for new ecoNET devices

### **How to Use Results**

1. **Review Missing Entities**: Add new parameters to appropriate constant lists
2. **Fix Type Mismatches**: Move parameters between `DEFAULT_SENSORS` and `DEFAULT_BINARY_SENSORS`
3. **Update Device Classes**: Apply appropriate device classes based on recommendations
4. **Validate Changes**: Re-run test after making changes

### **Example Fix Process**

```python
# Before: Parameter in wrong list
DEFAULT_SENSORS = ["wifi", "lan", "mainSrv"]  # ❌ Wrong!

# After: Parameter in correct list
DEFAULT_BINARY_SENSORS = ["wifi", "lan", "mainSrv"]  # ✅ Correct!
DEFAULT_SENSORS = ["tempCO", "tempCWU", "softVer"]   # ✅ Correct!
```

## Troubleshooting

### **Common Issues**

1. **Import Errors**: Ensure `const.py` is accessible from the test directory
2. **Missing Fixtures**: Check that fixture files exist in the expected locations
3. **Permission Errors**: Ensure write permissions for report file generation

### **Debug Mode**

The test provides detailed logging for troubleshooting:

- Fixture loading status
- Entity type analysis results
- Constants import verification
- Mismatch detection details

## Advanced Features

### **Three-Table Analysis System**

The test generates three organized tables for comprehensive analysis:

1. **Table 1: Missing Entities**

   - Parameters not defined in constants
   - Source file identification
   - Entity type recommendations

2. **Table 2: Type Mismatches**

   - Parameters with conflicting types
   - Expected vs. actual types
   - Source file tracking

3. **Table 3: Correctly Configured**
   - Parameters with matching types
   - Validation of existing configuration
   - Success confirmation

### **Recommendation Engine**

The test provides specific, actionable recommendations:

- Exact constant list changes needed
- Parameter movement instructions
- Device class suggestions
- Best practice guidance

## Summary

The `test_cons_check_key.py` test is an essential tool for maintaining entity type consistency in the ecoNET300 Home Assistant integration. It ensures that:

- **Entity types match their actual data characteristics**
- **Constants are properly organized and maintained**
- **New parameters are correctly categorized**
- **Home Assistant best practices are followed**

By running this test regularly and following its recommendations, developers can maintain a robust, consistent, and user-friendly Home Assistant integration that properly represents the ecoNET300 system's capabilities.
