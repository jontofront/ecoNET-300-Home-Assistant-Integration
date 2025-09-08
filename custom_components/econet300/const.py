"""Constants for ecoNET300 integration.

This module contains all constants organized by functionality:
- Core integration constants
- API endpoints and parameters
- Device-specific sensor mappings
- Entity configurations
- Operation modes and status mappings
- Mixer and thermostat configurations
"""

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.number import NumberDeviceClass
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    STATE_OFF,
    STATE_PAUSED,
    STATE_PROBLEM,
    STATE_UNKNOWN,
    EntityCategory,
    UnitOfPower,
    UnitOfTemperature,
    UnitOfTime,
)

# =============================================================================
# CORE INTEGRATION CONSTANTS
# =============================================================================
DOMAIN = "econet300"
SERVICE_API = "api"
SERVICE_COORDINATOR = "coordinator"

# =============================================================================
# DEVICE INFORMATION CONSTANTS
# =============================================================================
DEVICE_INFO_MANUFACTURER = "PLUM"
DEVICE_INFO_MODEL = "ecoNET300"
DEVICE_INFO_CONTROLLER_NAME = "PLUM ecoNET300"
DEVICE_INFO_MIXER_NAME = "Mixer device"
DEVICE_INFO_LAMBDA_NAME = "Module Lambda"
DEVICE_INFO_ECOSTER_NAME = "ecoSTER"

CONF_ENTRY_TITLE = "ecoNET300"
CONF_ENTRY_DESCRIPTION = "PLUM Econet300"

# =============================================================================
# API ENDPOINT CONSTANTS
# =============================================================================
# endpoint url sysParams
API_SYS_PARAMS_URI = "sysParams"

# sysParams property names
API_SYS_PARAMS_PARAM_UID = "uid"
API_SYS_PARAMS_PARAM_MODEL_ID = "controllerID"
API_SYS_PARAMS_PARAM_SW_REV = "softVer"
API_SYS_PARAMS_PARAM_HW_VER = "routerType"

#  endpoint url regParams
API_REG_PARAMS_URI = "regParams"

# regParams property names
API_REG_PARAMS_PARAM_DATA = "curr"

# endpoint url regParamsData
API_REG_PARAMS_DATA_URI = "regParamsData"
API_REG_PARAMS_DATA_PARAM_DATA = "data"

# Editable parameters
API_EDIT_PARAM_URI = "rmCurrNewParam"
API_EDITABLE_PARAMS_LIMITS_URI = "rmCurrentDataParamsEdits"
API_EDITABLE_PARAMS_LIMITS_DATA = "data"

# EditParams endpoint (ecoMAX360 specific)
API_EDIT_PARAMS_URI = "editParams"
API_EDIT_PARAMS_DATA = "data"  # editParams has data key with detailed parameter info

# =============================================================================
# OPERATION MODES AND STATUS MAPPINGS
# =============================================================================
OPERATION_MODE_NAMES = {
    0: STATE_OFF,
    1: "fire_up",
    2: "operation",
    3: "work",
    4: "supervision",
    5: STATE_PAUSED,  # "halted",
    6: "stop",
    7: "burning_off",
    8: "manual",
    9: STATE_PROBLEM,  # "alarm",
    10: "unsealing",
    11: "chimney",
    12: "stabilization",
    13: "no_transmission",
}

# =============================================================================
# MIXER CONFIGURATION CONSTANTS
# =============================================================================
AVAILABLE_NUMBER_OF_MIXERS = 6  # Supports up to 6 mixers (ecoMAX850R2-X has 5)
MIXER_AVAILABILITY_KEY = "mixerTemp"
MIXER_SET_AVAILABILITY_KEY = "mixerSetTemp"

# Dynamically generate SENSOR_MIXER_KEY
SENSOR_MIXER_KEY = {
    i: {f"{MIXER_AVAILABILITY_KEY}{i}", f"{MIXER_SET_AVAILABILITY_KEY}{i}"}
    for i in range(1, AVAILABLE_NUMBER_OF_MIXERS + 1)
}

# Mixer pump binary sensor keys
MIXER_PUMP_BINARY_SENSOR_KEYS = {
    f"mixerPumpWorks{i}" for i in range(1, AVAILABLE_NUMBER_OF_MIXERS + 1)
}

# =============================================================================
# DEVICE-SPECIFIC SENSOR MAPPINGS
# =============================================================================
# ecoMAX360i specific sensors
ECOMAX360I_SENSORS = {
    "PS",
    "Circuit2thermostatTemp",
    "TempClutch",
    "Circuit3thermostatTemp",
    "TempWthr",
    "TempCircuit3",
    "TempCircuit2",
    "TempBuforUp",
    "TempCWU",
    "TempBuforDown",
    "heatingUpperTemp",
    "Circuit1thermostat",
    "heating_work_state_pump4",
    # ecoMAX360 specific temperature circuit and buffer parameters
    "Circuit1ComfortTemp",  # Parameter 238 - Circuit 1 Day Temperature
    "Circuit1EcoTemp",  # Parameter 239 - Circuit 1 Night Temperature
    "BufferTargetTemp",  # Parameter 183 - Buffer Target Temperature
    "Circuit2ComfortTemp",  # Parameter 288 - Circuit 2 Day Temperature
    "Circuit2EcoTemp",  # Parameter 289 - Circuit 2 Night Temperature
    "Circuit3ComfortTemp",  # Parameter 339 - Circuit 3 Day Temperature
    "Circuit3EcoTemp",  # Parameter 340 - Circuit 3 Night Temperature
    "Circuit4ComfortTemp",  # Parameter 390 - Circuit 4 Day Temperature
    "Circuit4EcoTemp",  # Parameter 391 - Circuit 4 Night Temperature
    "Circuit5ComfortTemp",  # Parameter 441 - Circuit 5 Day Temperature
    "Circuit5EcoTemp",  # Parameter 442 - Circuit 5 Night Temperature
    "Circuit6ComfortTemp",  # Parameter 492 - Circuit 6 Day Temperature
    "Circuit6EcoTemp",  # Parameter 493 - Circuit 6 Night Temperature
    "Circuit7ComfortTemp",  # Parameter 543 - Circuit 7 Day Temperature
    "Circuit7EcoTemp",  # Parameter 544 - Circuit 7 Night Temperature
}

# ecoSTER thermostat sensors (if moduleEcoSTERSoftVer is not None)
ECOSTER_SENSORS = {
    # ecoSTER temperature sensors
    "ecoSterTemp1",
    "ecoSterTemp2",
    "ecoSterTemp3",
    "ecoSterTemp4",
    "ecoSterTemp5",
    "ecoSterTemp6",
    "ecoSterTemp7",
    "ecoSterTemp8",
    # ecoSTER setpoint sensors
    "ecoSterSetTemp1",
    "ecoSterSetTemp2",
    "ecoSterSetTemp3",
    "ecoSterSetTemp4",
    "ecoSterSetTemp5",
    "ecoSterSetTemp6",
    "ecoSterSetTemp7",
    "ecoSterSetTemp8",
    # ecoSTER mode sensors
    "ecoSterMode1",
    "ecoSterMode2",
    "ecoSterMode3",
    "ecoSterMode4",
    "ecoSterMode5",
    "ecoSterMode6",
    "ecoSterMode7",
    "ecoSterMode8",
}

# Lambda sensor module
LAMBDA_SENSORS = {
    "lambdaStatus",
    "lambdaSet",
    "lambdaLevel",
}

# ecoSOL solar collector sensors (ecoSOL 500, ecoSOL 301, etc.)
ECOSOL_SENSORS = {
    # Temperature sensors
    "T1",  # Collector temperature
    "T2",  # Tank temperature
    "T3",  # Tank temperature
    "T4",  # Return temperature
    "T5",  # Collector temperature - power measurement
    "T6",  # Temperature sensor
    "TzCWU",  # Hot water temperature
    # Pump status sensors
    "P1",  # Pump 1 status
    "P2",  # Pump 2 status
    # Output status
    "H",  # Output status
    # Heat output
    "Uzysk_ca_kowity",  # Total heat output
    # Diagnostic sensors
    "ecosrvAddr",
    "quality",
    "signal",
    "softVer",
    "routerType",
    "protocolType",
    "controllerID",
    "ecosrvSoftVer",
}

# Default sensors for most controllers
DEFAULT_SENSORS = {
    "boilerPower",
    "boilerPowerKW",
    "tempFeeder",
    "fuelLevel",
    "tempCO",
    "tempCOSet",
    "statusCWU",
    "tempCWU",
    "tempCWUSet",
    "tempFlueGas",
    "mode",
    "fanPower",
    "thermostat",
    "tempExternalSensor",
    "tempLowerBuffer",
    "tempUpperBuffer",
    "quality",
    "signal",
    "softVer",
    "controllerID",
    "moduleASoftVer",
    "moduleBSoftVer",
    "moduleCSoftVer",
    "moduleLambdaSoftVer",
    "modulePanelSoftVer",
    "moduleEcoSTERSoftVer",
    # ecoMAX850R2-X specific sensors
    "fuelConsum",
    "fuelStream",
    "tempBack",
    "transmission",
    "statusCO",
    # Diagnostic sensors
    "routerType",
    "protocolType",
}

# Main sensor mapping by controller type
SENSOR_MAP_KEY = {
    "ecoMAX360i": ECOMAX360I_SENSORS,
    "ecoSter": ECOSTER_SENSORS,
    "lambda": LAMBDA_SENSORS,
    "ecoSOL 500": ECOSOL_SENSORS,
    "ecoSOL 301": ECOSOL_SENSORS,  # ecoSOL 301 uses same sensors as ecoSOL 500
    "_default": DEFAULT_SENSORS,
}

# =============================================================================
# DEVICE-SPECIFIC BINARY SENSOR MAPPINGS
# =============================================================================
# Default binary sensors for most controllers
DEFAULT_BINARY_SENSORS = {
    "lighterWorks",
    "pumpCOWorks",
    "fanWorks",
    "feederWorks",
    "pumpFireplaceWorks",
    "pumpCWUWorks",
    "mainSrv",
    "wifi",
    "lan",
    "fuelConsumptionCalc",
    "ecosrvHttps",
    # ecoMAX850R2-X specific binary sensors
    "contactGZC",
    "contactGZCActive",
    "pumpCirculationWorks",
    "pumpSolarWorks",
}

# ecoSTER thermostat binary sensors
ECOSTER_BINARY_SENSORS = {
    # ecoSTER contact sensors
    "ecoSterContacts1",
    "ecoSterContacts2",
    "ecoSterContacts3",
    "ecoSterContacts4",
    "ecoSterContacts5",
    "ecoSterContacts6",
    "ecoSterContacts7",
    "ecoSterContacts8",
    # ecoSTER day schedule sensors
    "ecoSterDaySched1",
    "ecoSterDaySched2",
    "ecoSterDaySched3",
    "ecoSterDaySched4",
    "ecoSterDaySched5",
    "ecoSterDaySched6",
    "ecoSterDaySched7",
    "ecoSterDaySched8",
}

# ecoSOL solar collector binary sensors (ecoSOL 500, ecoSOL 301, etc.)
ECOSOL_BINARY_SENSORS = {
    "wifi",
    "lan",
    "mainSrv",
    "fuelConsumptionCalc",
    "ecosrvHttps",
}

# Main binary sensor mapping by controller type
BINARY_SENSOR_MAP_KEY = {
    "_default": DEFAULT_BINARY_SENSORS,
    "ecoSter": ECOSTER_BINARY_SENSORS,
    "ecoSOL 500": ECOSOL_BINARY_SENSORS,
    "ecoSOL 301": ECOSOL_BINARY_SENSORS,  # ecoSOL 301 uses same binary sensors as ecoSOL 500
}

# Helper: Extract ecoSOL controller IDs for easy access
ECOSOL_CONTROLLER_IDS = {
    controller_id
    for controller_id, sensor_set in BINARY_SENSOR_MAP_KEY.items()
    if sensor_set == ECOSOL_BINARY_SENSORS
}

# =============================================================================
# NUMBER ENTITY MAPPINGS
# =============================================================================
# Default number entities for most controllers
DEFAULT_NUMBER_MAP = {
    "1280": "tempCOSet",  # Boiler temperature setpoint
    "1281": "tempCWUSet",  # Hot water temperature setpoint
    "1287": "mixerSetTemp1",  # Mixer 1 temperature setpoint
    "1288": "mixerSetTemp2",  # Mixer 2 temperature setpoint
    "1289": "mixerSetTemp3",  # Mixer 3 temperature setpoint
    "1290": "mixerSetTemp4",  # Mixer 4 temperature setpoint
    "1291": "mixerSetTemp5",  # Mixer 5 temperature setpoint
    "1292": "mixerSetTemp6",  # Mixer 6 temperature setpoint
    "55": "heaterMode",  # Heater mode (Summer/Winter/Auto)
}

# ecoMAX360i specific number entities
ECOMAX360I_NUMBER_MAP = {
    "1280": "tempCOSet",  # Boiler temperature setpoint
    "1281": "tempCWUSet",  # Hot water temperature setpoint
    "55": "heaterMode",  # Heater mode (Summer/Winter/Auto)
    # ecoMAX360 circuit temperature setpoints
    "238": "Circuit1ComfortTemp",  # Circuit 1 Day Temperature
    "239": "Circuit1EcoTemp",  # Circuit 1 Night Temperature
    "288": "Circuit2ComfortTemp",  # Circuit 2 Day Temperature
    "289": "Circuit2EcoTemp",  # Circuit 2 Night Temperature
    "338": "Circuit3ComfortTemp",  # Circuit 3 Day Temperature
    "339": "Circuit3EcoTemp",  # Circuit 3 Night Temperature
    "946": "Circuit4ComfortTemp",  # Circuit 4 Day Temperature
    "947": "Circuit4EcoTemp",  # Circuit 4 Night Temperature
    "997": "Circuit5ComfortTemp",  # Circuit 5 Day Temperature
    "998": "Circuit5EcoTemp",  # Circuit 5 Night Temperature
    "755": "Circuit6ComfortTemp",  # Circuit 6 Day Temperature
    "756": "Circuit6EcoTemp",  # Circuit 6 Night Temperature
    "805": "Circuit7ComfortTemp",  # Circuit 7 Day Temperature
    "806": "Circuit7EcoTemp",  # Circuit 7 Night Temperature
}

# Main number mapping by controller type
NUMBER_MAP_KEY = {
    "ecoMAX360i": ECOMAX360I_NUMBER_MAP,
    "_default": DEFAULT_NUMBER_MAP,
}

# Legacy NUMBER_MAP for backward compatibility
NUMBER_MAP = DEFAULT_NUMBER_MAP

# =============================================================================
# HEATER SUMMER/WINTER/AUTO MODE MAPPINGS
# =============================================================================
# HEATER SUMMER/WINTER/AUTO MODE MAPPINGS
# =============================================================================
# Note: Display names are now handled by the translation system
# Numeric keys with option names for Home Assistant select entities

HEATER_MODE_VALUES = {
    0: "winter",
    1: "summer",
    2: "auto",
}


# Heater mode parameter index (API parameter 55)
HEATER_MODE_PARAM_INDEX = "55"

# =============================================================================
# PARAMETER ENDPOINT MAPPINGS
# =============================================================================
# Parameters that use the rmNewParam endpoint with newParamIndex
RMNEWPARAM_PARAMS = {
    "55",  # Heater mode (Summer/Winter/Auto)
    # Add other parameters here that need rmNewParam endpoint
    # Example: "56", "57", etc.
}

# Control parameters that use the newParam endpoint with newParamName
CONTROL_PARAMS = {
    "BOILER_CONTROL",  # Boiler ON/OFF control
    # Add other control parameters here
    # Example: "PUMP_CONTROL", "FAN_CONTROL", etc.
}

# Individual control parameter constants
BOILER_CONTROL = "BOILER_CONTROL"

# =============================================================================
# ENTITY UNIT MAPPINGS
# =============================================================================
# By default all sensors unit_of_measurement are None
ENTITY_UNIT_MAP = {
    "tempCO": UnitOfTemperature.CELSIUS,
    "tempCOSet": UnitOfTemperature.CELSIUS,
    "tempCWUSet": UnitOfTemperature.CELSIUS,
    "tempExternalSensor": UnitOfTemperature.CELSIUS,
    "tempFeeder": UnitOfTemperature.CELSIUS,
    "lambdaLevel": PERCENTAGE,
    "lambdaSet": PERCENTAGE,
    "workAt100": UnitOfTime.HOURS,
    "workAt50": UnitOfTime.HOURS,
    "workAt30": UnitOfTime.HOURS,
    "FeederWork": UnitOfTime.HOURS,
    "thermoTemp": UnitOfTemperature.CELSIUS,
    "fanPower": PERCENTAGE,
    "tempFlueGas": UnitOfTemperature.CELSIUS,
    "mixerSetTemp1": UnitOfTemperature.CELSIUS,
    "mixerSetTemp2": UnitOfTemperature.CELSIUS,
    "mixerSetTemp3": UnitOfTemperature.CELSIUS,
    "mixerSetTemp4": UnitOfTemperature.CELSIUS,
    "mixerSetTemp5": UnitOfTemperature.CELSIUS,
    "mixerSetTemp6": UnitOfTemperature.CELSIUS,
    "mixerTemp1": UnitOfTemperature.CELSIUS,
    "mixerTemp2": UnitOfTemperature.CELSIUS,
    "mixerTemp3": UnitOfTemperature.CELSIUS,
    "mixerTemp4": UnitOfTemperature.CELSIUS,
    "mixerTemp5": UnitOfTemperature.CELSIUS,
    "mixerTemp6": UnitOfTemperature.CELSIUS,
    "tempBack": UnitOfTemperature.CELSIUS,
    "tempCWU": UnitOfTemperature.CELSIUS,
    "boilerPower": PERCENTAGE,
    "boilerPowerKW": UnitOfPower.KILO_WATT,
    "fuelLevel": PERCENTAGE,
    "tempUpperBuffer": UnitOfTemperature.CELSIUS,
    "tempLowerBuffer": UnitOfTemperature.CELSIUS,
    "signal": SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    "quality": PERCENTAGE,
    "valveMixer1": PERCENTAGE,
    "burnerOutput": PERCENTAGE,
    "mixerTemp": UnitOfTemperature.CELSIUS,
    "mixerSetTemp": UnitOfTemperature.CELSIUS,
    # ecoMAX850R2-X specific units
    "fuelConsum": PERCENTAGE,
    "fuelStream": PERCENTAGE,
    "transmission": None,
    # ecoSTER thermostat units
    "ecoSterTemp1": UnitOfTemperature.CELSIUS,
    "ecoSterTemp2": UnitOfTemperature.CELSIUS,
    "ecoSterTemp3": UnitOfTemperature.CELSIUS,
    "ecoSterTemp4": UnitOfTemperature.CELSIUS,
    "ecoSterTemp5": UnitOfTemperature.CELSIUS,
    "ecoSterTemp6": UnitOfTemperature.CELSIUS,
    "ecoSterTemp7": UnitOfTemperature.CELSIUS,
    "ecoSterTemp8": UnitOfTemperature.CELSIUS,
    "ecoSterSetTemp1": UnitOfTemperature.CELSIUS,
    "ecoSterSetTemp2": UnitOfTemperature.CELSIUS,
    "ecoSterSetTemp3": UnitOfTemperature.CELSIUS,
    "ecoSterSetTemp4": UnitOfTemperature.CELSIUS,
    "ecoSterSetTemp5": UnitOfTemperature.CELSIUS,
    "ecoSterSetTemp6": UnitOfTemperature.CELSIUS,
    "ecoSterSetTemp7": UnitOfTemperature.CELSIUS,
    "ecoSterSetTemp8": UnitOfTemperature.CELSIUS,
    "ecoSterMode1": None,
    "ecoSterMode2": None,
    "ecoSterMode3": None,
    "ecoSterMode4": None,
    "ecoSterMode5": None,
    "ecoSterMode6": None,
    "ecoSterMode7": None,
    "ecoSterMode8": None,
    # ecoMAX360i
    "Circuit2thermostatTemp": UnitOfTemperature.CELSIUS,
    "TempClutch": UnitOfTemperature.CELSIUS,
    "Circuit3thermostatTemp": UnitOfTemperature.CELSIUS,
    "TempWthr": UnitOfTemperature.CELSIUS,
    "TempCircuit3": UnitOfTemperature.CELSIUS,
    "TempCircuit2": UnitOfTemperature.CELSIUS,
    "TempBuforUp": UnitOfTemperature.CELSIUS,
    "TempBuforDown": UnitOfTemperature.CELSIUS,
    "heatingUpperTemp": UnitOfTemperature.CELSIUS,
    "Circuit1thermostat": UnitOfTemperature.CELSIUS,
    # ecoMAX360-cf8 specific temperature circuit and buffer parameters
    "Circuit1ComfortTemp": UnitOfTemperature.CELSIUS,
    "Circuit1EcoTemp": UnitOfTemperature.CELSIUS,
    "BufferTargetTemp": UnitOfTemperature.CELSIUS,
    "Circuit2ComfortTemp": UnitOfTemperature.CELSIUS,
    "Circuit2EcoTemp": UnitOfTemperature.CELSIUS,
    "Circuit3ComfortTemp": UnitOfTemperature.CELSIUS,
    "Circuit3EcoTemp": UnitOfTemperature.CELSIUS,
    "Circuit4ComfortTemp": UnitOfTemperature.CELSIUS,
    "Circuit4EcoTemp": UnitOfTemperature.CELSIUS,
    "Circuit5ComfortTemp": UnitOfTemperature.CELSIUS,
    "Circuit5EcoTemp": UnitOfTemperature.CELSIUS,
    "Circuit6ComfortTemp": UnitOfTemperature.CELSIUS,
    "Circuit6EcoTemp": UnitOfTemperature.CELSIUS,
    "Circuit7ComfortTemp": UnitOfTemperature.CELSIUS,
    "Circuit7EcoTemp": UnitOfTemperature.CELSIUS,
    # ecoSOL specific units (ecoSOL 500, ecoSOL 301, etc.)
    "T1": UnitOfTemperature.CELSIUS,
    "T2": UnitOfTemperature.CELSIUS,
    "T3": UnitOfTemperature.CELSIUS,
    "T4": UnitOfTemperature.CELSIUS,
    "T5": UnitOfTemperature.CELSIUS,
    "T6": UnitOfTemperature.CELSIUS,
    "TzCWU": UnitOfTemperature.CELSIUS,
    "P1": None,
    "P2": None,
    "H": None,
    "Uzysk_ca_kowity": PERCENTAGE,
    # ecoSOL diagnostic units
    "ecosrvAddr": None,
    "softVer": None,
    "routerType": None,
    "protocolType": None,
    "controllerID": None,
    "ecosrvSoftVer": None,
}

# =============================================================================
# ENTITY STATE CLASS MAPPINGS
# =============================================================================
# By default all sensors state_class are MEASUREMENT
STATE_CLASS_MAP: dict[str, SensorStateClass | None] = {
    "lambdaStatus": None,
    "mode": None,
    "thermostat": None,
    "statusCO": None,
    "statusCWU": None,
    "softVer": None,
    "controllerID": None,
    "moduleASoftVer": None,
    "moduleBSoftVer": None,
    "moduleCSoftVer": None,
    "moduleLambdaSoftVer": None,
    "modulePanelSoftVer": None,
    # Diagnostic sensors (non-numeric)
    "routerType": None,
    "protocolType": None,
    "moduleEcoSTERSoftVer": None,
    # ecoMAX360i
    "PS": None,
    "heating_work_state_pump4": None,
}

# =============================================================================
# ENTITY DEVICE CLASS MAPPINGS
# =============================================================================

ENTITY_SENSOR_DEVICE_CLASS_MAP: dict[str, SensorDeviceClass | None] = {
    "tempFeeder": SensorDeviceClass.TEMPERATURE,
    "tempExternalSensor": SensorDeviceClass.TEMPERATURE,
    "tempCO": SensorDeviceClass.TEMPERATURE,
    "tempCOSet": SensorDeviceClass.TEMPERATURE,
    "boilerPower": SensorDeviceClass.POWER_FACTOR,
    "boilerPowerKW": SensorDeviceClass.POWER,
    "fanPower": SensorDeviceClass.POWER_FACTOR,
    "tempFlueGas": SensorDeviceClass.TEMPERATURE,
    "mixerSetTemp1": SensorDeviceClass.TEMPERATURE,
    "mixerSetTemp2": SensorDeviceClass.TEMPERATURE,
    "mixerSetTemp3": SensorDeviceClass.TEMPERATURE,
    "mixerSetTemp4": SensorDeviceClass.TEMPERATURE,
    "mixerSetTemp5": SensorDeviceClass.TEMPERATURE,
    "mixerSetTemp6": SensorDeviceClass.TEMPERATURE,
    "mixerTemp1": SensorDeviceClass.TEMPERATURE,
    "mixerTemp2": SensorDeviceClass.TEMPERATURE,
    "mixerTemp3": SensorDeviceClass.TEMPERATURE,
    "mixerTemp4": SensorDeviceClass.TEMPERATURE,
    "mixerTemp5": SensorDeviceClass.TEMPERATURE,
    "mixerTemp6": SensorDeviceClass.TEMPERATURE,
    "mixerTemp": SensorDeviceClass.TEMPERATURE,
    "mixerSetTemp": SensorDeviceClass.TEMPERATURE,
    "tempBack": SensorDeviceClass.TEMPERATURE,
    "tempCWU": SensorDeviceClass.TEMPERATURE,
    "statusCO": None,
    "statusCWU": None,
    "tempUpperBuffer": SensorDeviceClass.TEMPERATURE,
    "tempLowerBuffer": SensorDeviceClass.TEMPERATURE,
    "signal": SensorDeviceClass.SIGNAL_STRENGTH,
    "servoMixer1": SensorDeviceClass.ENUM,
    # ecoMAX850R2-X specific device classes
    "fuelConsum": SensorDeviceClass.POWER_FACTOR,
    "fuelStream": SensorDeviceClass.POWER_FACTOR,
    "transmission": None,
    # ecoSTER thermostat device classes
    "ecoSterTemp1": SensorDeviceClass.TEMPERATURE,
    "ecoSterTemp2": SensorDeviceClass.TEMPERATURE,
    "ecoSterTemp3": SensorDeviceClass.TEMPERATURE,
    "ecoSterTemp4": SensorDeviceClass.TEMPERATURE,
    "ecoSterTemp5": SensorDeviceClass.TEMPERATURE,
    "ecoSterTemp6": SensorDeviceClass.TEMPERATURE,
    "ecoSterTemp7": SensorDeviceClass.TEMPERATURE,
    "ecoSterTemp8": SensorDeviceClass.TEMPERATURE,
    "ecoSterSetTemp1": SensorDeviceClass.TEMPERATURE,
    "ecoSterSetTemp2": SensorDeviceClass.TEMPERATURE,
    "ecoSterSetTemp3": SensorDeviceClass.TEMPERATURE,
    "ecoSterSetTemp4": SensorDeviceClass.TEMPERATURE,
    "ecoSterSetTemp5": SensorDeviceClass.TEMPERATURE,
    "ecoSterSetTemp6": SensorDeviceClass.TEMPERATURE,
    "ecoSterSetTemp7": SensorDeviceClass.TEMPERATURE,
    "ecoSterSetTemp8": SensorDeviceClass.TEMPERATURE,
    "ecoSterMode1": None,
    "ecoSterMode2": None,
    "ecoSterMode3": None,
    "ecoSterMode4": None,
    "ecoSterMode5": None,
    "ecoSterMode6": None,
    "ecoSterMode7": None,
    "ecoSterMode8": None,
    # ecoMAX360i
    "Circuit2thermostatTemp": SensorDeviceClass.TEMPERATURE,
    "TempClutch": SensorDeviceClass.TEMPERATURE,
    "Circuit3thermostatTemp": SensorDeviceClass.TEMPERATURE,
    "TempWthr": SensorDeviceClass.TEMPERATURE,
    "TempCircuit3": SensorDeviceClass.TEMPERATURE,
    "TempCircuit2": SensorDeviceClass.TEMPERATURE,
    "TempBuforUp": SensorDeviceClass.TEMPERATURE,
    "TempBuforDown": SensorDeviceClass.TEMPERATURE,
    "heatingUpperTemp": SensorDeviceClass.TEMPERATURE,
    "Circuit1thermostat": SensorDeviceClass.TEMPERATURE,
    # ecoMAX360-cf8 specific temperature circuit and buffer parameters
    "Circuit1ComfortTemp": SensorDeviceClass.TEMPERATURE,
    "Circuit1EcoTemp": SensorDeviceClass.TEMPERATURE,
    "BufferTargetTemp": SensorDeviceClass.TEMPERATURE,
    "Circuit2ComfortTemp": SensorDeviceClass.TEMPERATURE,
    "Circuit2EcoTemp": SensorDeviceClass.TEMPERATURE,
    "Circuit3ComfortTemp": SensorDeviceClass.TEMPERATURE,
    "Circuit3EcoTemp": SensorDeviceClass.TEMPERATURE,
    "Circuit4ComfortTemp": SensorDeviceClass.TEMPERATURE,
    "Circuit4EcoTemp": SensorDeviceClass.TEMPERATURE,
    "Circuit5ComfortTemp": SensorDeviceClass.TEMPERATURE,
    "Circuit5EcoTemp": SensorDeviceClass.TEMPERATURE,
    "Circuit6ComfortTemp": SensorDeviceClass.TEMPERATURE,
    "Circuit6EcoTemp": SensorDeviceClass.TEMPERATURE,
    "Circuit7ComfortTemp": SensorDeviceClass.TEMPERATURE,
    "Circuit7EcoTemp": SensorDeviceClass.TEMPERATURE,
    # ecoSOL specific device classes (ecoSOL 500, ecoSOL 301, etc.)
    "T1": SensorDeviceClass.TEMPERATURE,
    "T2": SensorDeviceClass.TEMPERATURE,
    "T3": SensorDeviceClass.TEMPERATURE,
    "T4": SensorDeviceClass.TEMPERATURE,
    "T5": SensorDeviceClass.TEMPERATURE,
    "T6": SensorDeviceClass.TEMPERATURE,
    "TzCWU": SensorDeviceClass.TEMPERATURE,
    "P1": None,
    "P2": None,
    "H": None,
    "Uzysk_ca_kowity": SensorDeviceClass.POWER_FACTOR,
    # ecoSOL diagnostic device classes
    "ecosrvAddr": None,
    "softVer": None,
    "routerType": None,
    "protocolType": None,
    "controllerID": None,
    "ecosrvSoftVer": None,
}

# Number entity device classes
ENTITY_NUMBER_SENSOR_DEVICE_CLASS_MAP = {
    "tempCOSet": NumberDeviceClass.TEMPERATURE,
    "tempCWUSet": NumberDeviceClass.TEMPERATURE,
    # ecoMAX850R2-X specific number entities
    "mixerSetTemp5": NumberDeviceClass.TEMPERATURE,
    # ecoMAX360 circuit temperature setpoints
    "Circuit1ComfortTemp": NumberDeviceClass.TEMPERATURE,
    "Circuit1EcoTemp": NumberDeviceClass.TEMPERATURE,
    "Circuit2ComfortTemp": NumberDeviceClass.TEMPERATURE,
    "Circuit2EcoTemp": NumberDeviceClass.TEMPERATURE,
    "Circuit3ComfortTemp": NumberDeviceClass.TEMPERATURE,
    "Circuit3EcoTemp": NumberDeviceClass.TEMPERATURE,
    "Circuit4ComfortTemp": NumberDeviceClass.TEMPERATURE,
    "Circuit4EcoTemp": NumberDeviceClass.TEMPERATURE,
    "Circuit5ComfortTemp": NumberDeviceClass.TEMPERATURE,
    "Circuit5EcoTemp": NumberDeviceClass.TEMPERATURE,
    "Circuit6ComfortTemp": NumberDeviceClass.TEMPERATURE,
    "Circuit6EcoTemp": NumberDeviceClass.TEMPERATURE,
    "Circuit7ComfortTemp": NumberDeviceClass.TEMPERATURE,
    "Circuit7EcoTemp": NumberDeviceClass.TEMPERATURE,
}

# Binary sensor device classes
ENTITY_BINARY_DEVICE_CLASS_MAP = {
    # By default all binary sensors device_class are RUNNING
    "mainSrv": BinarySensorDeviceClass.CONNECTIVITY,
    "wifi": BinarySensorDeviceClass.CONNECTIVITY,
    "lan": BinarySensorDeviceClass.CONNECTIVITY,
    "fuelConsumptionCalc": BinarySensorDeviceClass.RUNNING,
    "ecosrvHttps": BinarySensorDeviceClass.CONNECTIVITY,
    # ecoMAX850R2-X specific binary sensors
    "contactGZC": BinarySensorDeviceClass.CONNECTIVITY,
    "contactGZCActive": BinarySensorDeviceClass.CONNECTIVITY,
}

# =============================================================================
# ENTITY PRECISION MAPPINGS
# =============================================================================
# Add only keys where precision more than 0 needed
ENTITY_PRECISION = {
    "tempFeeder": 1,
    "tempExternalSensor": 1,
    "lambdaLevel": 1,
    "lambdaSet": 1,
    "tempCO": 1,
    "mixerTemp1": 1,
    "mixerTemp2": 1,
    "mixerTemp3": 1,
    "mixerTemp4": 1,
    "mixerTemp5": 1,
    "mixerTemp6": 1,
    "tempBack": 2,
    "tempUpperBuffer": 1,
    "tempLowerBuffer": 1,
    "tempCWU": 1,
    "tempFlueGas": 1,
    "fanPower": 0,
    "statusCO": None,
    "statusCWU": None,
    "thermostat": None,
    "lambdaStatus": None,
    "mode": None,
    "softVer": None,
    "controllerID": None,
    "moduleASoftVer": None,
    "moduleBSoftVer": None,
    "moduleCSoftVer": None,
    "moduleLambdaSoftVer": None,
    "modulePanelSoftVer": None,
    # ecoMAX360i
    "PS": None,
    "TempBuforDown": 1,
    # ecoMAX360-cf8 specific temperature circuit and buffer parameters
    "Circuit1ComfortTemp": 1,
    "Circuit1EcoTemp": 1,
    "BufferTargetTemp": 1,
    "Circuit2ComfortTemp": 1,
    "Circuit2EcoTemp": 1,
    "Circuit3ComfortTemp": 1,
    "Circuit3EcoTemp": 1,
    "Circuit4ComfortTemp": 1,
    "Circuit4EcoTemp": 1,
    "Circuit5ComfortTemp": 1,
    "Circuit5EcoTemp": 1,
    "Circuit6ComfortTemp": 1,
    "Circuit6EcoTemp": 1,
    "Circuit7ComfortTemp": 1,
    "Circuit7EcoTemp": 1,
    # ecoSTER thermostat precision
    "ecoSterTemp1": 1,
    "ecoSterTemp2": 1,
    "ecoSterTemp3": 1,
    "ecoSterTemp4": 1,
    "ecoSterTemp5": 1,
    "ecoSterTemp6": 1,
    "ecoSterTemp7": 1,
    "ecoSterTemp8": 1,
    "ecoSterSetTemp1": 1,
    "ecoSterSetTemp2": 1,
    "ecoSterSetTemp3": 1,
    "ecoSterSetTemp4": 1,
    "ecoSterSetTemp5": 1,
    "ecoSterSetTemp6": 1,
    "ecoSterSetTemp7": 1,
    "ecoSterSetTemp8": 1,
    "heatingUpperTemp": 1,
    "Circuit1thermostat": 1,
    "heating_work_state_pump4": None,
    # ecoSOL specific precision (ecoSOL 500, ecoSOL 301, etc.)
    "T1": 1,
    "T2": 1,
    "T3": 1,
    "T4": 1,
    "T5": 1,
    "T6": 1,
    "TzCWU": 1,
    "P1": None,
    "P2": None,
    "H": None,
    "Uzysk_ca_kowity": 1,
    # ecoSOL diagnostic precision
    "ecosrvAddr": None,
    "routerType": None,
    "protocolType": None,
    "ecosrvSoftVer": None,
}

NO_CWU_TEMP_SET_STATUS_CODE = 128

ENTITY_VALUE_PROCESSOR = {
    "mode": lambda x: SENSOR_MODE_MAPPING.get(x, STATE_UNKNOWN),
    "lambdaStatus": lambda x: SENSOR_LAMBDA_STATUS_MAPPING.get(x, STATE_UNKNOWN),
    "statusCWU": lambda x: SENSOR_STATUS_CWU_MAPPING.get(x, STATE_UNKNOWN),
    "statusCO": lambda x: SENSOR_STATUS_CO_MAPPING.get(x, STATE_UNKNOWN),
    "thermostat": lambda x: SENSOR_THERMOSTAT_MAPPING.get(x, STATE_UNKNOWN),
}

# =============================================================================
# ENTITY CATEGORY MAPPINGS
# =============================================================================
ENTITY_CATEGORY = {
    "signal": EntityCategory.DIAGNOSTIC,
    "quality": EntityCategory.DIAGNOSTIC,
    "softVer": EntityCategory.DIAGNOSTIC,
    "moduleASoftVer": EntityCategory.DIAGNOSTIC,
    "moduleBSoftVer": EntityCategory.DIAGNOSTIC,
    "modulePanelSoftVer": EntityCategory.DIAGNOSTIC,
    "moduleLambdaSoftVer": EntityCategory.DIAGNOSTIC,
    "protocolType": EntityCategory.DIAGNOSTIC,
    "controllerID": EntityCategory.DIAGNOSTIC,
    "moduleCSoftVer": EntityCategory.DIAGNOSTIC,
    "mainSrv": EntityCategory.DIAGNOSTIC,
    "wifi": EntityCategory.DIAGNOSTIC,
    "lan": EntityCategory.DIAGNOSTIC,
    "fuelConsumptionCalc": EntityCategory.DIAGNOSTIC,
    "ecosrvHttps": EntityCategory.DIAGNOSTIC,
    "ecosrvAddr": EntityCategory.DIAGNOSTIC,
    "routerType": EntityCategory.DIAGNOSTIC,
    "ecosrvSoftVer": EntityCategory.DIAGNOSTIC,
    "moduleEcoSTERSoftVer": EntityCategory.DIAGNOSTIC,
}

# =============================================================================
# ENTITY VALUE LIMITS
# =============================================================================
ENTITY_MIN_VALUE = {
    "tempCOSet": 27,
    "tempCWUSet": 20,
    # ecoMAX360 circuit temperature setpoints
    "Circuit1ComfortTemp": 10,
    "Circuit1EcoTemp": 10,
    "Circuit2ComfortTemp": 10,
    "Circuit2EcoTemp": 10,
    "Circuit3ComfortTemp": 10,
    "Circuit3EcoTemp": 10,
    "Circuit4ComfortTemp": 10,
    "Circuit4EcoTemp": 10,
    "Circuit5ComfortTemp": 10,
    "Circuit5EcoTemp": 10,
    "Circuit6ComfortTemp": 10,
    "Circuit6EcoTemp": 10,
    "Circuit7ComfortTemp": 10,
    "Circuit7EcoTemp": 10,
}

ENTITY_MAX_VALUE = {
    "tempCOSet": 68,
    "tempCWUSet": 55,
    # ecoMAX360 circuit temperature setpoints
    "Circuit1ComfortTemp": 35,
    "Circuit1EcoTemp": 35,
    "Circuit2ComfortTemp": 35,
    "Circuit2EcoTemp": 35,
    "Circuit3ComfortTemp": 35,
    "Circuit3EcoTemp": 35,
    "Circuit4ComfortTemp": 35,
    "Circuit4EcoTemp": 35,
    "Circuit5ComfortTemp": 35,
    "Circuit5EcoTemp": 35,
    "Circuit6ComfortTemp": 35,
    "Circuit6EcoTemp": 35,
    "Circuit7ComfortTemp": 35,
    "Circuit7EcoTemp": 35,
}

ENTITY_STEP = {
    "tempCOSet": 1,
    "tempCWUSet": 1,
    # ecoMAX360 circuit temperature setpoints
    "Circuit1ComfortTemp": 0.1,
    "Circuit1EcoTemp": 0.1,
    "Circuit2ComfortTemp": 0.1,
    "Circuit2EcoTemp": 0.1,
    "Circuit3ComfortTemp": 0.1,
    "Circuit3EcoTemp": 0.1,
    "Circuit4ComfortTemp": 0.1,
    "Circuit4EcoTemp": 0.1,
    "Circuit5ComfortTemp": 0.1,
    "Circuit5EcoTemp": 0.1,
    "Circuit6ComfortTemp": 0.1,
    "Circuit6EcoTemp": 0.1,
    "Circuit7ComfortTemp": 0.1,
    "Circuit7EcoTemp": 0.1,
}

# Sensor value mappings for both display and icon support
SENSOR_MODE_MAPPING: dict[int, str] = {
    0: "off",
    1: "manual",
    2: "auto",
    3: "service",
    4: "test",
    5: "pause",
    6: "error",
    7: "standby",
    8: "emergency",
    9: "maintenance",
    10: "calibration",
}

SENSOR_LAMBDA_STATUS_MAPPING: dict[int, str] = {
    0: "stop",
    1: "start",
    2: "working",
    3: "error",
    4: "maintenance",
}

SENSOR_STATUS_CWU_MAPPING: dict[int, str] = {
    0: "not_set",
    1: "set",
    128: "no_temp_set",
}

SENSOR_STATUS_CO_MAPPING: dict[int, str] = {
    0: "off",
    1: "pause",
    2: "reload",
    3: "fire",
    4: "fire",
    5: "alert",
    6: "alert",
    7: "test_tube",
    8: "stop_circle",
    9: "gauge",
    10: "help_circle",
}

SENSOR_THERMOSTAT_MAPPING: dict[int, str] = {
    0: "off",
    1: "on",
}
