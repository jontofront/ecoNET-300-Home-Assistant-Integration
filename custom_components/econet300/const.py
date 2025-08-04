"""Constants from the Home Assistant."""

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

# Constant for the econet Integration integration
DOMAIN = "econet300"

SERVICE_API = "api"
SERVICE_COORDINATOR = "coordinator"

DEVICE_INFO_MANUFACTURER = "PLUM"
DEVICE_INFO_MODEL = "ecoNET300"
DEVICE_INFO_CONTROLLER_NAME = "PLUM ecoNET300"
DEVICE_INFO_MIXER_NAME = "Mixer device"
DEVICE_INFO_LAMBDA_NAME = "Module Lambda"

CONF_ENTRY_TITLE = "ecoNET300"
CONF_ENTRY_DESCRIPTION = "PLUM Econet300"

# Sys params
API_SYS_PARAMS_URI = "sysParams"
API_SYS_PARAMS_PARAM_UID = "uid"
API_SYS_PARAMS_PARAM_MODEL_ID = "controllerID"
API_SYS_PARAMS_PARAM_SW_REV = "softVer"
API_SYS_PARAMS_PARAM_HW_VER = "routerType"

# Reg params
API_REG_PARAMS_URI = "regParams"
API_REG_PARAMS_PARAM_DATA = "curr"

# Reg params data all in one
API_REG_PARAMS_DATA_URI = "regParamsData"
API_REG_PARAMS_DATA_PARAM_DATA = "data"

# Boiler status keys map
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

# Editable params limits
API_EDIT_PARAM_URI = "rmCurrNewParam"
API_EDITABLE_PARAMS_LIMITS_URI = "rmCurrentDataParamsEdits"
API_EDITABLE_PARAMS_LIMITS_DATA = "data"

###################################
#    NUMBER of AVAILABLE MIXERS
###################################
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

#######################
#    REG PARAM MAPS
#######################

SENSOR_MAP_KEY = {
    "ecoMAX360i": {
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
    },
    # ecoSTER thermostat sensors if moduleEcoSTERSoftVer is not None
    "ecoSTER": {
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
    },
    "lambda": {
        "lambdaStatus",
        "lambdaSet",
        "lambdaLevel",
    },
    "_default": {
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
    },
}

BINARY_SENSOR_MAP_KEY = {
    "_default": {
        "lighterWorks",
        "pumpCOWorks",
        "fanWorks",
        "feederWorks",
        "pumpFireplaceWorks",
        "pumpCWUWorks",
        "mainSrv",
        "wifi",
        "lan",
        "lambdaStatus",
        "thermostat",
        "statusCWU",
        # ecoMAX850R2-X specific binary sensors
        "contactGZC",
        "contactGZCActive",
        "pumpCirculation",
        "pumpCirculationWorks",
        "pumpSolar",
        "pumpSolarWorks",
        "pumpFireplace",
        "pumpFireplaceWorks",
        "pumpCO",
        "pumpCWU",
    },
    # ecoSTER thermostat binary sensors if moduleEcoSTERSoftVer is not None
    "ecoSTER": {
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
    },
}

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
}

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

# By default all sensors device_class are None
ENTITY_SENSOR_DEVICE_CLASS_MAP: dict[str, SensorDeviceClass | None] = {
    #############################
    #          SENSORS
    #############################
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
}

ENTITY_NUMBER_SENSOR_DEVICE_CLASS_MAP = {
    #############################
    #       NUMBER SENSORS
    #############################
    "tempCOSet": NumberDeviceClass.TEMPERATURE,
    "tempCWUSet": NumberDeviceClass.TEMPERATURE,
    # ecoMAX850R2-X specific number entities
    "mixerSetTemp5": NumberDeviceClass.TEMPERATURE,
}


ENTITY_BINARY_DEVICE_CLASS_MAP = {
    #############################
    #      BINARY SENSORS
    #############################
    # By default all binary sensors device_class are RUNNING
    "mainSrv": BinarySensorDeviceClass.CONNECTIVITY,
    "wifi": BinarySensorDeviceClass.CONNECTIVITY,
    "lan": BinarySensorDeviceClass.CONNECTIVITY,
    "lambdaStatus": BinarySensorDeviceClass.RUNNING,
    "thermostat": BinarySensorDeviceClass.RUNNING,
    "statusCWU": BinarySensorDeviceClass.RUNNING,
}

"""Add only keys where precision more than 0 needed"""
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
}

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
    "lan": "mdi:lan-connect",
    "softVer": "mdi:alarm-panel-outline",
    "controllerID": "mdi:alarm-panel-outline",
    "moduleASoftVer": "mdi:raspberry-pi",
    "moduleBSoftVer": "mdi:raspberry-pi",
    "moduleCSoftVer": "mdi:raspberry-pi",
    "moduleLambdaSoftVer": "mdi:raspberry-pi",
    "modulePanelSoftVer": "mdi:alarm-panel-outline",
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
    "TempBuforDown": "mdi:thermometer",
    "heatingUpperTemp": "mdi:thermometer",
    "heating_work_state_pump4": "mdi:sync",
}

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
    "lan": "mdi:lan-disconnect",
    "lighterWorks": "mdi:fire-off",
    "lambdaStatus": "mdi:lambda-off",
    "thermostat": "mdi:thermostat-off",
}

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
