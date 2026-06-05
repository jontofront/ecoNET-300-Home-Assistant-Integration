"""Number/select parameter mappings, unit-name lookups and static regParams/CDP deduplication sets used by the options flow."""

from homeassistant.const import (
    PERCENTAGE as _PERCENTAGE,
    UnitOfEnergy as _UnitOfEnergy,
    UnitOfMass as _UnitOfMass,
    UnitOfPower as _UnitOfPower,
    UnitOfTemperature as _UnitOfTemperature,
    UnitOfTime as _UnitOfTime,
)

from .controllers import (
    DEFAULT_BINARY_SENSORS,
    DEFAULT_SENSORS,
    ECOMAX360I_SENSORS,
    ECOSOL_BINARY_SENSORS,
    ECOSOL_SENSORS,
    ECOSTER_BINARY_SENSORS,
    ECOSTER_SENSORS,
    LAMBDA_SENSORS,
)
from .core import MIXER_PUMP_BINARY_SENSOR_KEYS, SENSOR_MIXER_KEY

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
    "55": "heaterMode",  # Heater mode (Summer/Winter/Auto)
}

# =============================================================================
# SELECT ENTITY MAPPINGS
# =============================================================================

# Select entity parameter mappings (for writing settings)
SELECT_KEY_POST_INDEX: dict[str, str] = {
    "heaterMode": "55",  # Heater mode winter/summer/auto
    # Add more select entities here as they are created
    # "pumpMode": "56",
    # "fanMode": "57",
}

# Select entity current state mappings (for reading current state)
SELECT_KEY_GET_INDEX: dict[str, str] = {
    "heaterMode": "2049",  # Heater mode current state
    # Add more select entities here as they are created
    # "pumpMode": "2050",
    # "fanMode": "2051",
}

# Select entity value mappings (numeric value -> display name)
SELECT_KEY_VALUES: dict[str, dict[int, str]] = {
    "heaterMode": {
        0: "winter",
        1: "summer",
        2: "auto",
    },
    # Add more select entities here as they are created
    # "pumpMode": {
    #     0: "Off",
    #     1: "On",
    #     2: "Auto",
    # },
}


# Legacy constants for backward compatibility
HEATER_MODE_VALUES = SELECT_KEY_VALUES["heaterMode"]
HEATER_MODE_PARAM_INDEX = SELECT_KEY_POST_INDEX["heaterMode"]
HEATER_MODE_CURRENT_STATE_PARAM = SELECT_KEY_GET_INDEX["heaterMode"]

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
# DYNAMIC ENTITY UNIT MAPPINGS
# =============================================================================
# Mapping from ecoNET unit names to Home Assistant units
# Used for dynamic number entity creation from merged parameter data
UNIT_NAME_TO_HA_UNIT = {
    "%": _PERCENTAGE,
    "°C": _UnitOfTemperature.CELSIUS,
    "sek.": _UnitOfTime.SECONDS,
    "min.": _UnitOfTime.MINUTES,
    "h.": _UnitOfTime.HOURS,
    "kg": _UnitOfMass.KILOGRAMS,
    "kg/h": "kg/h",  # Mass flow rate for fuel stream
    "kW": _UnitOfPower.KILO_WATT,
    "kWh": _UnitOfEnergy.KILO_WATT_HOUR,
    "r/min": "r/min",  # Custom unit for revolutions per minute
}

# =============================================================================
# UNIT MAPPINGS (shared by dynamic entity helpers)
# =============================================================================
# Maps unit index from rmCurrentDataParams to human-readable unit string.
UNIT_INDEX_TO_NAME: dict[int, str] = {
    0: "",
    1: "°C",
    2: "sek.",
    3: "min.",
    4: "h.",
    5: "%",
    6: "kg",
    7: "kW",
    8: "r/min",
    31: "",  # Boolean/state indicator (no unit)
}

# --- Static entity deduplication ---------------------------------------------
# regParamsData IDs already handled by static entities (number, select).
# These are skipped in the Options Flow key listing to avoid duplicates.
STATIC_REGPARAMS_DATA_IDS: set[str] = (
    set(NUMBER_MAP.keys())
    | set(SELECT_KEY_POST_INDEX.values())
    | set(SELECT_KEY_GET_INDEX.values())
)

# All static regParams keys (sensors + binary sensors across all controllers).
# Used to filter already-mapped keys in the Options Flow when selecting
# custom entities from the regParams endpoint.
STATIC_REGPARAMS_KEYS: set[str] = (
    DEFAULT_SENSORS
    | DEFAULT_BINARY_SENSORS
    | ECOMAX360I_SENSORS
    | ECOSTER_SENSORS
    | LAMBDA_SENSORS
    | ECOSOL_SENSORS
    | ECOSOL_BINARY_SENSORS
    | ECOSTER_BINARY_SENSORS
    | set().union(*SENSOR_MIXER_KEY.values())
    | MIXER_PUMP_BINARY_SENSOR_KEYS
)

# --- rmCurrentDataParams ID → regParams key mapping --------------------------
# The rmCurrentDataParams endpoint provides only metadata (name, unit, special)
# but NOT current values.  The actual live values are in regParams under
# camelCase keys.  This mapping allows CustomSensor to read the value from
# regParams when the user creates a custom entity from rmCurrentDataParams.
CDP_ID_TO_REGPARAMS: dict[str, str] = {
    # Monitoring – temperatures
    "1024": "tempCO",
    "1025": "tempCWU",
    "1028": "tempUpperBuffer",
    "1029": "tempLowerBuffer",
    "1030": "tempFlueGas",
    "1031": "mixerTemp1",
    "1032": "mixerTemp2",
    "1033": "mixerTemp3",
    "1034": "mixerTemp4",
    # Monitoring – low-ID sensors
    "1": "lighter",
    "26": "tempFeeder",
    "28": "tempExternalSensor",
    "114": "fuelLevel",
    "117": "thermostat",
    # Monitoring – pumps / actuators
    "1536": "fan",
    "1538": "feeder",
    "1540": "feeder2Additional",
    "1541": "pumpCO",
    "1542": "pumpCWU",
    "1543": "pumpCirculation",
    "1544": "mixerPumpWorks1",
    "1547": "mixerPumpWorks2",
    "1550": "mixerPumpWorks3",
    "1553": "mixerPumpWorks4",
    # Monitoring – burner
    "1794": "boilerPower",
    # Setpoints (editable) – also in NUMBER_MAP but kept for completeness
    "1280": "tempCOSet",
    "1281": "tempCWUSet",
    "1287": "mixerSetTemp1",
    "1288": "mixerSetTemp2",
    "1289": "mixerSetTemp3",
    "1290": "mixerSetTemp4",
}

# IDs from rmCurrentDataParams that already have static entities.
# Used to filter the Options Flow to prevent duplicate entity creation.
STATIC_CDP_IDS: set[str] = set(CDP_ID_TO_REGPARAMS.keys()) & {
    k for k, v in CDP_ID_TO_REGPARAMS.items() if v in STATIC_REGPARAMS_KEYS
}

