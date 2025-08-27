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

# sysParams roperty names
API_SYS_PARAMS_PARAM_UID = "uid"
API_SYS_PARAMS_PARAM_MODEL_ID = "controllerID"
API_SYS_PARAMS_PARAM_SW_REV = "softVer"
API_SYS_PARAMS_PARAM_HW_VER = "routerType"

#  endpoint url regParams
API_REG_PARAMS_URI = "regParams"

# regParams roperty names
API_REG_PARAMS_PARAM_DATA = "curr"

# endpoint url regParamsData
API_REG_PARAMS_DATA_URI = "regParamsData"
API_REG_PARAMS_DATA_PARAM_DATA = "data"

# Editable parameters
API_EDIT_PARAM_URI = "rmCurrNewParam"
API_EDITABLE_PARAMS_LIMITS_URI = "rmCurrentDataParamsEdits"
API_EDITABLE_PARAMS_LIMITS_DATA = "data"

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

# ecoSOL 500 solar collector sensors
ECOSOL500_SENSORS = {
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
    "ecoSOL 500": ECOSOL500_SENSORS,
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
    "statusCWU",
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

# ecoSOL 500 solar collector binary sensors
ECOSOL500_BINARY_SENSORS = {
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
    "ecoSOL 500": ECOSOL500_BINARY_SENSORS,
}

# =============================================================================
# NUMBER ENTITY MAPPINGS
# =============================================================================
NUMBER_MAP = {
    "1280": "tempCOSet",  # Boiler temperature setpoint
    "1281": "tempCWUSet",  # Hot water temperature setpoint
    "1287": "mixerSetTemp1",  # Mixer 1 temperature setpoint
    "1288": "mixerSetTemp2",  # Mixer 2 temperature setpoint
    "1289": "mixerSetTemp3",  # Mixer 3 temperature setpoint
    "1290": "mixerSetTemp4",  # Mixer 4 temperature setpoint
    "1291": "mixerSetTemp5",  # Mixer 5 temperature setpoint
    "1292": "mixerSetTemp6",  # Mixer 6 temperature setpoint
}

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
    # ecoSOL500 specific units
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
    # ecoSOL500 diagnostic units
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
    # ecoSOL500 specific device classes
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
    # ecoSOL500 diagnostic device classes
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
}

# Binary sensor device classes
ENTITY_BINARY_DEVICE_CLASS_MAP = {
    # By default all binary sensors device_class are RUNNING
    "mainSrv": BinarySensorDeviceClass.CONNECTIVITY,
    "wifi": BinarySensorDeviceClass.CONNECTIVITY,
    "lan": BinarySensorDeviceClass.CONNECTIVITY,
    "fuelConsumptionCalc": BinarySensorDeviceClass.RUNNING,
    "ecosrvHttps": BinarySensorDeviceClass.CONNECTIVITY,
    "lambdaStatus": BinarySensorDeviceClass.RUNNING,
    "thermostat": BinarySensorDeviceClass.RUNNING,
    "statusCWU": BinarySensorDeviceClass.RUNNING,
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
    # ecoSOL500 specific precision
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
    # ecoSOL500 diagnostic precision
    "ecosrvAddr": None,
    "routerType": None,
    "protocolType": None,
    "ecosrvSoftVer": None,
}

# =============================================================================
# ENTITY ICON MAPPINGS
# =============================================================================
ENTITY_ICON = {
    "mode": "mdi:sync",
    "fanPower": "mdi:fan",
    "temCO": "mdi:thermometer-lines",
    "statusCO": "mdi:heating",
    "statusCWU": "mdi:water-boiler",
    "thermostat": "mdi:thermostat",
    "boilerPower": "mdi:gauge",
    "boilerPowerKW": "mdi:gauge",
    "fuelLevel": "mdi:gas-station",
    "lambdaLevel": "mdi:lambda",
    "lambdaSet": "mdi:lambda",
    "lambdaStatus": "mdi:lambda",
    "lighterWorks": "mdi:fire",
    "workAt100": "mdi:counter",
    "workAt50": "mdi:counter",
    "workAt30": "mdi:counter",
    "FeederWork": "mdi:counter",
    "feederWorks": "mdi:screw-lag",
    "FiringUpCount": "mdi:counter",
    "quality": "mdi:signal",
    "pumpCOWorks": "mdi:pump",
    "fanWorks": "mdi:fan",
    "additionalFeeder": "mdi:screw-lag",
    "pumpFireplaceWorks": "mdi:pump",
    "pumpCWUWorks": "mdi:pump",
    "mixerPumpWorks": "mdi:pump",
    "mixerPumpWorks1": "mdi:pump",
    "mixerPumpWorks2": "mdi:pump",
    "mixerPumpWorks3": "mdi:pump",
    "mixerPumpWorks4": "mdi:pump",
    "mixerPumpWorks5": "mdi:pump",
    "mixerPumpWorks6": "mdi:pump",
    "mixerTemp": "mdi:thermometer",
    "mixerSetTemp": "mdi:thermometer",
    "valveMixer1": "mdi:valve",
    "servoMixer1": "mdi:valve",
    "mixerTemp1": "mdi:thermometer",
    "mixerTemp2": "mdi:thermometer",
    "mixerTemp3": "mdi:thermometer",
    "mixerTemp4": "mdi:thermometer",
    "mixerTemp5": "mdi:thermometer",
    "mixerTemp6": "mdi:thermometer",
    "tempUpperBuffer": "mdi:thermometer",
    "tempLowerBuffer": "mdi:thermometer",
    "mainSrv": "mdi:server-network",
    "wifi": "mdi:wifi",
    "lan": "mdi:lan-connect",
    "fuelConsumptionCalc": "mdi:calculator",
    "ecosrvHttps": "mdi:lock",
    "softVer": "mdi:alarm-panel-outline",
    "controllerID": "mdi:alarm-panel-outline",
    "moduleASoftVer": "mdi:raspberry-pi",
    "moduleBSoftVer": "mdi:raspberry-pi",
    "moduleCSoftVer": "mdi:raspberry-pi",
    "moduleLambdaSoftVer": "mdi:raspberry-pi",
    "modulePanelSoftVer": "mdi:alarm-panel-outline",
    "moduleEcoSTERSoftVer": "mdi:raspberry-pi",
    # ecoSTER thermostat icons
    "ecoSterTemp1": "mdi:thermometer",
    "ecoSterTemp2": "mdi:thermometer",
    "ecoSterTemp3": "mdi:thermometer",
    "ecoSterTemp4": "mdi:thermometer",
    "ecoSterTemp5": "mdi:thermometer",
    "ecoSterTemp6": "mdi:thermometer",
    "ecoSterTemp7": "mdi:thermometer",
    "ecoSterTemp8": "mdi:thermometer",
    "ecoSterSetTemp1": "mdi:thermometer",
    "ecoSterSetTemp2": "mdi:thermometer",
    "ecoSterSetTemp3": "mdi:thermometer",
    "ecoSterSetTemp4": "mdi:thermometer",
    "ecoSterSetTemp5": "mdi:thermometer",
    "ecoSterSetTemp6": "mdi:thermometer",
    "ecoSterSetTemp7": "mdi:thermometer",
    "ecoSterSetTemp8": "mdi:thermometer",
    "ecoSterMode1": "mdi:thermostat",
    "ecoSterMode2": "mdi:thermostat",
    "ecoSterMode3": "mdi:thermostat",
    "ecoSterMode4": "mdi:thermostat",
    "ecoSterMode5": "mdi:thermostat",
    "ecoSterMode6": "mdi:thermostat",
    "ecoSterMode7": "mdi:thermostat",
    "ecoSterMode8": "mdi:thermostat",
    "ecoSterContacts1": "mdi:thermostat",
    "ecoSterContacts2": "mdi:thermostat",
    "ecoSterContacts3": "mdi:thermostat",
    "ecoSterContacts4": "mdi:thermostat",
    "ecoSterContacts5": "mdi:thermostat",
    "ecoSterContacts6": "mdi:thermostat",
    "ecoSterContacts7": "mdi:thermostat",
    "ecoSterContacts8": "mdi:thermostat",
    "ecoSterDaySched1": "mdi:calendar-clock",
    "ecoSterDaySched2": "mdi:calendar-clock",
    "ecoSterDaySched3": "mdi:calendar-clock",
    "ecoSterDaySched4": "mdi:calendar-clock",
    "ecoSterDaySched5": "mdi:calendar-clock",
    "ecoSterDaySched6": "mdi:calendar-clock",
    "ecoSterDaySched7": "mdi:calendar-clock",
    "ecoSterDaySched8": "mdi:calendar-clock",
    # ecoMAX360i
    "PS": "mdi:power-plug",
    "Circuit2thermostatTemp": "mdi:thermometer",
    "TempClutch": "mdi:thermometer",
    "Circuit3thermostatTemp": "mdi:thermometer",
    "TempWthr": "mdi:thermometer",
    "TempCircuit3": "mdi:thermometer",
    "TempCircuit2": "mdi:thermometer",
    "TempBuforUp": "mdi:thermometer",
    "TempBuforDown": "mdi:thermometer",
    "heatingUpperTemp": "mdi:thermometer",
    "Circuit1thermostat": "mdi:thermometer",
    "heating_work_state_pump4": "mdi:sync",
    # ecoMAX850R2-X specific icons
    "fuelConsum": "mdi:gas-station",
    "fuelStream": "mdi:gas-station",
    "tempBack": "mdi:thermometer",
    "transmission": "mdi:transmission-tower",
    "contactGZC": "mdi:connection",
    "contactGZCActive": "mdi:connection",
    "pumpCirculationWorks": "mdi:pump",
    "pumpSolarWorks": "mdi:pump",
    # ecoSOL500 specific icons
    "T1": "mdi:thermometer",
    "T2": "mdi:thermometer",
    "T3": "mdi:thermometer",
    "T4": "mdi:thermometer",
    "T5": "mdi:thermometer",
    "T6": "mdi:thermometer",
    "TzCWU": "mdi:thermometer",
    "P1": "mdi:pump",
    "P2": "mdi:pump",
    "H": "mdi:gauge",
    "Uzysk_ca_kowity": "mdi:gauge",
    # ecoSOL500 diagnostic icons
    "ecosrvAddr": "mdi:server",
    "routerType": "mdi:router-wireless",
    "protocolType": "mdi:protocol",
    "ecosrvSoftVer": "mdi:server-network",
}

# =============================================================================
# ENTITY ICON OFF MAPPINGS
# =============================================================================
ENTITY_ICON_OFF = {
    "pumpCOWorks": "mdi:pump-off",
    "fanWorks": "mdi:fan-off",
    "additionalFeeder": "mdi:screw-lag",
    "pumpFireplaceWorks": "mdi:pump-off",
    "pumpCWUWorks": "mdi:pump-off",
    "mixerPumpWorks1": "mdi:pump-off",
    "mixerPumpWorks2": "mdi:pump-off",
    "mixerPumpWorks3": "mdi:pump-off",
    "mixerPumpWorks4": "mdi:pump-off",
    "mixerPumpWorks5": "mdi:pump-off",
    "mixerPumpWorks6": "mdi:pump-off",
    "statusCWU": "mdi:water-boiler-off",
    "mainSrv": "mdi:server-network-off",
    "wifi": "mdi:wifi-off",
    "lan": "mdi:lan-disconnect",
    "fuelConsumptionCalc": "mdi:calculator-off",
    "ecosrvHttps": "mdi:lock-off",
    "lighterWorks": "mdi:fire-off",
    "thermostat": "mdi:thermostat-off",
    # ecoMAX850R2-X specific off icons
    "contactGZC": "mdi:connection-off",
    "contactGZCActive": "mdi:connection-off",
    "pumpCirculationWorks": "mdi:pump-off",
    "pumpSolarWorks": "mdi:pump-off",
    # ecoSTER thermostat off icons
    "ecoSterContacts1": "mdi:thermostat-off",
    "ecoSterContacts2": "mdi:thermostat-off",
    "ecoSterContacts3": "mdi:thermostat-off",
    "ecoSterContacts4": "mdi:thermostat-off",
    "ecoSterContacts5": "mdi:thermostat-off",
    "ecoSterContacts6": "mdi:thermostat-off",
    "ecoSterContacts7": "mdi:thermostat-off",
    "ecoSterContacts8": "mdi:thermostat-off",
    "ecoSterDaySched1": "mdi:calendar-clock-off",
    "ecoSterDaySched2": "mdi:calendar-clock-off",
    "ecoSterDaySched3": "mdi:calendar-clock-off",
    "ecoSterDaySched4": "mdi:calendar-clock-off",
    "ecoSterDaySched5": "mdi:calendar-clock-off",
    "ecoSterDaySched6": "mdi:calendar-clock-off",
    "ecoSterDaySched7": "mdi:calendar-clock-off",
    "ecoSterDaySched8": "mdi:calendar-clock-off",
}

# =============================================================================
# ENTITY VALUE PROCESSORS
# =============================================================================
NO_CWU_TEMP_SET_STATUS_CODE = 128

ENTITY_VALUE_PROCESSOR = {
    "mode": lambda x: OPERATION_MODE_NAMES.get(x, STATE_UNKNOWN),
    "lambdaStatus": (
        lambda x: (
            "stop"
            if x == 0
            else ("start" if x == 1 else ("working" if x == 2 else STATE_UNKNOWN))
        )
    ),
    "statusCWU": lambda x: "Not set" if x == NO_CWU_TEMP_SET_STATUS_CODE else "Set",
    "thermostat": lambda x: "ON" if x == 1 else "OFF",
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
}

# =============================================================================
# ENTITY VALUE LIMITS
# =============================================================================
ENTITY_MIN_VALUE = {
    "tempCOSet": 27,
    "tempCWUSet": 20,
}

ENTITY_MAX_VALUE = {
    "tempCOSet": 68,
    "tempCWUSet": 55,
}

ENTITY_STEP = {
    "tempCOSet": 1,
    "tempCWUSet": 1,
}
