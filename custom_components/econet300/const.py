"""Constants from the Home Assistant."""

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.components.number import NumberDeviceClass
from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    STATE_CLOSING,
    STATE_OFF,
    STATE_ON,
    STATE_OPENING,
    STATE_PAUSED,
    STATE_PROBLEM,
    STATE_UNKNOWN,
    EntityCategory,
    UnitOfTemperature,
    UnitOfTime,
)

# Constant for the econet Integration integration
DOMAIN = "econet300"

SERVICE_API = "api"
SERVICE_COORDINATOR = "coordinator"

DEVICE_INFO_MANUFACTURER = "PLUM"
DEVICE_INFO_MODEL = "ecoNET300"
DEVICE_INFO_CONTROLLER_NAME = "PLUM ecoNET300"
DEVICE_INFO_MIXER_NAME = "Mixer device"

CONF_ENTRY_TITLE = "ecoNET300"
CONF_ENTRY_DESCRIPTION = "PLUM Econet300"

SERVO_MIXER_VALVE_HA_STATE: dict[int, str] = {
    0: STATE_CLOSING,
    1: STATE_OFF,
    2: STATE_OPENING,
}

## Sys params
API_SYS_PARAMS_URI = "sysParams"
API_SYS_PARAMS_PARAM_UID = "uid"
API_SYS_PARAMS_PARAM_MODEL_ID = "controllerID"
API_SYS_PARAMS_PARAM_SW_REV = "softVer"
API_SYS_PARAMS_PARAM_HW_VER = "routerType"

## Reg params
API_REG_PARAMS_URI = "regParams"
API_REG_PARAMS_PARAM_DATA = "curr"

## Reg params data all in one
API_REG_PARAMS_DATA_URI = "regParamsData"
API_REG_PARAMS_DATA_PARAM_DATA = "data"

## Map names for params data in API_REG_PARAMS_DATA_URI
API_RM_CURRENT_DATA_PARAMS_URI = "rmCurrentDataParams"

## Map units for params data map API_RM_CURRENT_DATA_PARAMS_URI
API_RM_PARAMSUNITSNAMES_URI = "rmParamsUnitsNames"

# Boiler status keys map
# boiler mode names from  endpoint http://LocalIP/econet/rmParamsEnums?
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

# add constants to future
PRODUCT_TYPE = {
    0: "ECOMAX_850P_TYPE",  # regType 0
    1: "ECOMAX_850i_TYPE",  # regType 1
}

## Editable params limits
API_EDIT_PARAM_URI = "rmCurrNewParam"
API_EDITABLE_PARAMS_LIMITS_URI = "rmCurrentDataParamsEdits"
API_EDITABLE_PARAMS_LIMITS_DATA = "data"

EDITABLE_PARAMS_MAPPING_TABLE = {
    "tempCOSet": "1280",
    "tempCWUSet": "1281",
    "mixerSetTemp1": "1287",
    "mixerSetTemp2": "1288",
    "mixerSetTemp3": "1289",
    "mixerSetTemp4": "1290",
    "mixerSetTemp5": "1291",
    "mixerSetTemp6": "1292",
}

###################################
#    NUMBER of AVAILABLE MIXERS
###################################
AVAILABLE_NUMBER_OF_MIXERS = 6
MIXER_AVAILABILITY_KEY = "mixerTemp"
MIXER_KEY = "mixerPumpWorks"

#######################
#    REG PARAM MAPS
#######################

SENSOR_MAP_KEY = {
    "ecoster": {
        "ecoSterTemp1",
        "ecoSterTemp2",
    },
    "lambda": {
        "lambdaStatus",
        "lambdaSet",
        "lambdaLevel",
    },
    "_default": {
        "tempFeeder",
        "fuelLevel",
        "tempCO",
        "tempCOSet",
        "tempCWUSet",
        "tempFlueGas",
        "mode",
        "fanPower",
        "tempCOSet",
        "thermostat",
    },
}

BINARY_SENSOR_MAP_KEY = {
    "_default": {
        "lighter",
        "pumpCOWorks",
        "fanWorks",
        "pumpFireplaceWorks",
        "pumpCWUWorks",
    },
}

SENSOR_MAP = {
    "26": "tempFeeder",
    "28": "tempExternalSensor",
    "97": "fuelLevel",
    "151": "lambdaStatus",
    "153": "lambdaSet",
    "154": "lambdaLevel",
    "155": "workAt100",
    "156": "workAt50",
    "157": "workAt30",
    "158": "FeederWork",
    "159": "FiringUpCount",
    "168": "main_server",
    "170": "signal",
    "171": "status_wifi",
    "1024": "tempCO",
    "1025": "tempCWU",
    "1028": "tempUpperBuffer",
    "1029": "tempLowerBuffer",
    "1030": "tempFlueGas",
    "1792": "mode",
    "1794": "boilerPower",
    "1795": "fanPower",
    "1280": "tempCOSet",
    "1281": "tempCWUSet",
}

MIXER_MAP = {
    "1": {
        "139": "valveMixer1",
        "143": "servoMixer1",
        "1031": "mixerTemp1",
        "1287": "mixerSetTemp1",
    }
}

NUMBER_MAP = {
    "1280": "tempCOSet",
    "1281": "tempCWUSet",
}

BINARY_SENSOR_MAP = {
    "1": "lighter",
    "111": "weatherControl",
    "113": "unseal",
    "117": "thermostat",
    "118": "pumpCOWorks",
    "1536": "fanWorks",
    "1540": "additionalFeeder",
    "1541": "pumpFireplaceWorks",
    "1542": "pumpCWUWorks",
}

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
    "FiringUpCount": None,
    "thermoTemp": UnitOfTemperature.CELSIUS,
    "fanPower": PERCENTAGE,
    "tempFlueGas": UnitOfTemperature.CELSIUS,
    "mixerSetTemp1": UnitOfTemperature.CELSIUS,
    "mixerTemp1": UnitOfTemperature.CELSIUS,
    "tempBack": UnitOfTemperature.CELSIUS,
    "tempCWU": UnitOfTemperature.CELSIUS,
    "boilerPower": PERCENTAGE,
    "fuelLevel": PERCENTAGE,
    "tempUpperBuffer": UnitOfTemperature.CELSIUS,
    "tempLowerBuffer": UnitOfTemperature.CELSIUS,
    "signal": SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    "quality": PERCENTAGE,
    "valveMixer1": PERCENTAGE,
    "burnerOutput": PERCENTAGE,
    "mixerTemp": UnitOfTemperature.CELSIUS,
    "mixerSetTemp": UnitOfTemperature.CELSIUS,
}

STATE_CLASS_MAP: dict[str, SensorStateClass] = {
    "tempFeeder": SensorStateClass.MEASUREMENT,
    "tempExternalSensor": SensorStateClass.MEASUREMENT,
    "lambdaSet": SensorStateClass.MEASUREMENT,
    "lambdaLevel": SensorStateClass.MEASUREMENT,
    "workAt100": SensorStateClass.MEASUREMENT,
    "workAt50": SensorStateClass.MEASUREMENT,
    "workAt30": SensorStateClass.MEASUREMENT,
    "FeederWork": SensorStateClass.MEASUREMENT,
    "FiringUpCount": SensorStateClass.MEASUREMENT,
    "tempCO": SensorStateClass.MEASUREMENT,
    "tempCOSet": SensorStateClass.MEASUREMENT,
    "tempCWUSet": SensorStateClass.MEASUREMENT,
    "boiler_power": SensorStateClass.MEASUREMENT,
    "fanPower": SensorStateClass.MEASUREMENT,
    "tempFlueGas": SensorStateClass.MEASUREMENT,
    "mixerSetTemp1": SensorStateClass.MEASUREMENT,
    "tempBack": SensorStateClass.MEASUREMENT,
    "tempCWU": SensorStateClass.MEASUREMENT,
    "fuelLevel": SensorStateClass.MEASUREMENT,
    "tempUpperBuffer": SensorStateClass.MEASUREMENT,
    "tempLowerBuffer": SensorStateClass.MEASUREMENT,
    "signal": SensorStateClass.MEASUREMENT,
    "quality": SensorStateClass.MEASUREMENT,
    "valveMixer1": SensorStateClass.MEASUREMENT,
    "burnerOutput": SensorStateClass.MEASUREMENT,
    "mixerTemp": SensorStateClass.MEASUREMENT,
    "mixerSetTemp": SensorStateClass.MEASUREMENT,
}

ENTITY_SENSOR_DEVICE_CLASS_MAP: dict[str, SensorDeviceClass | None] = {
    #############################
    #          SENSORS
    #############################
    "tempFeeder": SensorDeviceClass.TEMPERATURE,
    "tempExternalSensor": SensorDeviceClass.TEMPERATURE,
    "tempCO": SensorDeviceClass.TEMPERATURE,
    "boilerPower": SensorDeviceClass.POWER_FACTOR,
    "fanPower": SensorDeviceClass.POWER_FACTOR,
    "tempFlueGas": SensorDeviceClass.TEMPERATURE,
    "mixerSetTemp1": SensorDeviceClass.TEMPERATURE,
    "mixerTemp": SensorDeviceClass.TEMPERATURE,
    "mixerSetTemp": SensorDeviceClass.TEMPERATURE,
    "tempBack": SensorDeviceClass.TEMPERATURE,
    "tempCWU": SensorDeviceClass.TEMPERATURE,
    "tempUpperBuffer": SensorDeviceClass.TEMPERATURE,
    "tempLowerBuffer": SensorDeviceClass.TEMPERATURE,
    "signal": SensorDeviceClass.SIGNAL_STRENGTH,
    "softVer": None,
    "moduleASoftVer": None,
    "moduleBSoftVer": None,
    "modulePanelSoftVer": None,
    "moduleLambdaSoftVer": None,
    "protocolType": None,
    "controllerID": None,
    "valveMixer1": None,
    "servoMixer1": SensorDeviceClass.ENUM,
    "Status_wifi": None,
    "main_server": None,
}

ENTITY_NUMBER_SENSOR_DEVICE_CLASS_MAP = {
    #############################
    #       NUMBER SENSORS
    #############################
    "tempCOSet": NumberDeviceClass.TEMPERATURE,
    "tempCWUSet": NumberDeviceClass.TEMPERATURE,
}


ENTITY_BINARY_DEVICE_CLASS_MAP = {
    #############################
    #      BINARY SENSORS
    #############################
    "lighter": BinarySensorDeviceClass.RUNNING,
    "weatherControl": BinarySensorDeviceClass.RUNNING,
    "unseal": BinarySensorDeviceClass.RUNNING,
    "thermostat": BinarySensorDeviceClass.RUNNING,
    "pumpCOWorks": BinarySensorDeviceClass.RUNNING,
    "fanWorks": BinarySensorDeviceClass.RUNNING,
    "additionalFeeder": BinarySensorDeviceClass.RUNNING,
    "pumpFireplaceWorks": BinarySensorDeviceClass.RUNNING,
    "pumpCWUWorks": BinarySensorDeviceClass.RUNNING,
    "mixerPumpWorks": BinarySensorDeviceClass.RUNNING,
}

"""Add only keys where precision more than 0 needed"""
ENTITY_PRECISION = {
    "tempFeeder": 1,
    "tempExternalSensor": 1,
    "fuelLevel": 0,
    "lambdaLevel": 1,
    "lambdaSet": 1,
    "tempCO": 1,
    "tempCOSet": 0,
    "tempCWUSet": 0,
    "fanPower": 0,
    "mixerSetTemp1": 0,
    "mixerTemp1": 1,
    "tempBack": 2,
    "tempUpperBuffer": 1,
    "tempLowerBuffer": 1,
    "tempCWU": 1,
    "tempFlueGas": 1,
    "mixerTemp": 0,
    "mixerSetTemp": 0,
}

ENTITY_ICON = {
    "mode": "mdi:sync",
    "fanPower": "mdi:fan",
    "temCO": "mdi:thermometer-lines",
    "tempCOSet": "mdi:thermometer-chevron-up",
    "tempCWUSet": "mdi:thermometer-chevron-up",
    "thermostat": "mdi:thermostat",
    "boilerPower": "mdi:gauge",
    "fuelLevel": "mdi:gas-station",
    "lambdaLevel": "mdi:lambda",
    "lambdaSet": "mdi:lambda",
    "lambdaStatus": "mdi:lambda",
    "workAt100": "mdi:counter",
    "workAt50": "mdi:counter",
    "workAt30": "mdi:counter",
    "FeederWork": "mdi:counter",
    "FiringUpCount": "mdi:counter",
    "quality": "mdi:signal",
    "pumpCOWorks": "mdi:pump",
    "fanWorks": "mdi:fan",
    "additionalFeeder": "mdi:screw-lag",
    "pumpFireplaceWorks": "mdi:pump",
    "pumpCWUWorks": "mdi:pump",
    "main_server": "mdi:server",
    "mixerPumpWorks": "mdi:pump",
    "mixerTemp": "mdi:thermometer",
    "mixerSetTemp": "mdi:thermometer",
    "valveMixer1": "mdi:valve",
    "mixerSetTemp1": "mdi:thermometer-chevron-up",
    "servoMixer1": "mdi:valve",
    "mixerTemp1": "mdi:thermometer",
}

ENTITY_ICON_OFF = {
    "pumpCOWorks": "mdi:pump-off",
    "fanWorks": "mdi:fan-off",
    "additionalFeeder": "mdi:screw-lag",
    "pumpFireplaceWorks": "mdi:pump-off",
    "pumpCWUWorks": "mdi:pump-off",
}

ENTITY_VALUE_PROCESSOR = {
    "mode": lambda x: OPERATION_MODE_NAMES.get(x, STATE_UNKNOWN),
    "thermostat": (
        lambda x: (
            STATE_ON
            if str(x).strip() == "true"
            else (STATE_OFF if str(x).strip() == "false" else None)
        )
    ),
    "lambdaStatus": (
        lambda x: (
            "stop"
            if x == 0
            else ("start" if x == 1 else ("working" if x == 2 else STATE_UNKNOWN))
        )
    ),
    "status_wifi": lambda x: "Connected" if x == 1 else "Disconnected",
    "main_server": lambda x: "Server available" if x == 1 else "Server not available",
    "servoMixer1": lambda x: SERVO_MIXER_VALVE_HA_STATE.get(x, STATE_UNKNOWN),
}


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
    "status_wifi": EntityCategory.DIAGNOSTIC,
    "main_server": EntityCategory.DIAGNOSTIC,
    "workAt100": EntityCategory.DIAGNOSTIC,
    "workAt50": EntityCategory.DIAGNOSTIC,
    "workAt30": EntityCategory.DIAGNOSTIC,
    "FeederWork": EntityCategory.DIAGNOSTIC,
    "FiringUpCount": EntityCategory.DIAGNOSTIC,
}

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

ENTITY_VISIBLE = {
    "tempCOSet": True,
    "tempCWUSet": True,
}

# Default values for visible 'entity_registry_visible_default=False,' in sensor.py
REG_PARAM_VISIBLE_DEFAULT = {
    "tempUpperBuffer": False,
    "tempLowerBuffer": False,
}

PRODUCT_MODEL = {
    # Models name which known us connect with ecoNET300
    "ecoMAX810P-L TOUCH"
    "SControl MK1"
    "ecoMAX860P2-N TOUCH"
    "ecoMAX860P3-V"
    "ecoSOL 301"
}

ALARMS_NAMES = {
    0: "No power",
    1: "Boiler sensor error",
    2: "Exceeding the maximum temperature of the boiler",
    3: "Sensor fault feeder",
    4: "Exceeding the maximum temperature of the tray",
    5: "Sensor fault system",
    6: "Exceeding the maximum flue gas temperature",
    7: "Firing up the boiler failed",
    8: "No fuel",
    9: "Loss of Containment",
    10: "Pressure sensor failed",
    11: "Faulty fan ",
    12: "ID Fan Pressure can not be reached ",
    13: "Burning off error ",
    14: "Photocell sensor failed",
    15: "Linear actuator blocked",
    16: "Incorrect work parameters",
    17: "Precaution of condensation ",
    18: "STB is disabled . Manual reset is needed when TB <65 °C Boiler STB ",
    19: "Opening the contact STB tray ",
    20: "Minimum water pressure exceeded",
    21: "Maximum water pressure exceeded",
    22: "Fuel feeder locked",
    23: "Extinguished flame ",
    24: "Faulty exhaust fan",
    25: "Error loading external feeder ",
    26: "Error Sensor solar collector SH ",
    27: "Error Sensor solar circuit SL ",
    28: "Sensor fault circuit H1- S",
    29: "Sensor fault circuit H2 - S",
    30: "Sensor fault circuit H3 - S",
    31: "Error weather sensor WS ",
    32: "HUW sensor error ",
    33: "Sensor error H0- S",
    34: "It takes frost protection - heat source are not included ",
    35: "It takes frost protection - the source of the attached ",
    36: "Exceeded max. Temperature solar collector ",
    37: "Exceeded max. Flow temperature of the floor ",
    38: "Cooling preventive solid fuel boiler ",
    39: "No communication with ecoLAMBDA ",
    40: "Lock the primary air damper ",
    41: "Lock the secondary air damper ",
    42: "Feeder full",
    43: "Furnace full",
    44: "No communication with B module",
    45: "Cleaning servomotor error",
    46: "Minimum pressure exceeded",
    47: "Maximum pressure exceeded",
    48: "Pressure sensor damage",
    49: "Maximum main heat source temperature exceeded",
    50: "Maximum additional heat source temperature exceeded",
    51: "Solar is OFF - temperature  is too high - wait for temperature drop",
    52: "Alarm for auger control system malfunction",
    53: "Clogged auger Alarm",
    54: "Temperature above maximum for the thermocouple.",
    55: "Thermocouple wired improperly.",
    255: "Alarm unknown",
}
