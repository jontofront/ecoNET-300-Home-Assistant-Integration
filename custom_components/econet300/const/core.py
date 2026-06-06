"""Core constants, coordinator/cache config, device info, polling, components, API + RM endpoints, structure types, alarm codes, operation modes and mixer configuration."""

from homeassistant.const import (
    STATE_OFF as _STATE_OFF,
    STATE_PAUSED as _STATE_PAUSED,
    STATE_PROBLEM as _STATE_PROBLEM,
)

# =============================================================================
# CORE INTEGRATION CONSTANTS
# =============================================================================
DOMAIN = "econet300"
SERVICE_API = "api"
SERVICE_COORDINATOR = "coordinator"
SERVICE_FUEL_SENSOR = "fuel_sensor"
SERVICE_GET_SCHEDULE = "get_schedule"

# regParams key for the fuel flow rate sensor (kg/h).
SENSOR_FUEL_STREAM = "fuelStream"

# Custom device class for fuel consumption meter to allow targeting with services
DEVICE_CLASS_FUEL_METER = "econet300__fuel_meter"

# Max sub-interval (seconds) for fuel consumption integration.
# If fuelStream does not change within this period, integration is still triggered.
FUEL_MAX_SUB_INTERVAL_SECONDS = 300

# Sensitive sysParams/regParams keys that must never be exposed as entity states
# or surfaced in diagnostics. The all-sensors path iterates every device key, so
# these are filtered out before entity creation and reused as the diagnostics
# redaction list to keep a single source of truth.
SENSITIVE_PARAM_KEYS = frozenset(
    {
        "device_uid",  # Device UID in coordinator data
        "eth0",  # Ethernet interface IP address
        "host",  # May contain internal network info
        "identifiers",  # Device identifiers containing UIDs
        "key",  # API keys and secrets
        "login",  # Account login name
        "password",  # Account password hash
        "servicePassword",  # Service password hash
        "ssid",  # WiFi network name
        "uid",  # Device UID - unique device identifier
        "username",  # May contain sensitive info
        "wlan0",  # WiFi interface IP address
    }
)

# =============================================================================
# COORDINATOR CONFIGURATION CONSTANTS
# =============================================================================
# Number of consecutive failures before creating a repair issue
CONSECUTIVE_FAILURES_THRESHOLD = 5

# Timeout in seconds for probing RM endpoint support (legacy-only modules return 404)
RM_PROBE_TIMEOUT_SEC = 2

# Max concurrent HTTP requests to the ecoNET module.
# The module runs on a TP-Link MR3020 with very limited resources;
# too many parallel connections cause timeouts (see GitHub issue #210).
MAX_CONCURRENT_API_REQUESTS = 3

# Coordinator update timeouts (seconds)
# First update: static metadata cache is cold -> 6+ parallel RM API calls needed
UPDATE_TIMEOUT_FIRST_SEC = 120
# Subsequent updates: only dynamic data fetched (cached metadata reused)
UPDATE_TIMEOUT_SEC = 30

# RM endpoint dataset keys for data coordinator (order matches tasks list)
RM_CORE_DATASET_KEYS = [
    "currentDataParams",
    "paramsNames",
    "paramsData",
    "langs",
]

RM_ADDITIONAL_DATASET_KEYS = [
    "paramsDescs",
    "paramsEnums",
    "alarmsNames",
]

# =============================================================================
# CACHE CONFIGURATION FOR STATIC METADATA
# =============================================================================
# Static metadata rarely changes - cache for 24 hours to reduce API load.
CACHE_KEY_STATIC_METADATA = "static_metadata"
CACHE_STATIC_METADATA_TTL = 86400  # 24 hours

# =============================================================================
# DEVICE INFORMATION CONSTANTS
# =============================================================================
DEVICE_INFO_MANUFACTURER = "PLUM"
DEVICE_INFO_MODEL = "ecoNET300"
DEVICE_INFO_CONTROLLER_NAME = "PLUM ecoNET300"
DEVICE_INFO_MIXER_NAME = "Mixer device"
DEVICE_INFO_LAMBDA_NAME = "Module Lambda"
DEVICE_INFO_ECOSTER_NAME = "ecoSTER"
DEVICE_INFO_HUW_NAME = "HUW Tank"
DEVICE_INFO_BUFFER_NAME = "Buffer"
DEVICE_INFO_SOLAR_NAME = "Solar"
DEVICE_INFO_SERVICE_PARAMETERS_NAME = "Service Parameters"
DEVICE_INFO_ADVANCED_PARAMETERS_NAME = "Advanced Parameters"

CONF_ENTRY_TITLE = "ecoNET300"
CONF_ENTRY_DESCRIPTION = "PLUM Econet300"

# =============================================================================
# HARDENING / POLLING
# =============================================================================
CONF_POLL_REG_PARAMS = "poll_reg_params"
CONF_POLL_SYS_PARAMS = "poll_sys_params"
CONF_POLL_EDIT_PARAMS = "poll_edit_params"

# Conservative defaults for the small ecoNET300 web server.
DEFAULT_POLL_REG_PARAMS = 15
DEFAULT_POLL_SYS_PARAMS = 300
DEFAULT_POLL_EDIT_PARAMS = 300

# Keep last values during short glitches, but do not allow silent flat-lines forever.
STALE_AFTER_SECONDS = 600


# =============================================================================
# DEVICE COMPONENT IDENTIFIERS
# =============================================================================
# These constants identify device components for grouping entities in Home Assistant.
# When adding a new device type, add a constant here and update DEFAULT_COMPONENT_STATUS.
COMPONENT_BOILER = "boiler"
COMPONENT_HUW = "huw"
COMPONENT_MIXER_1 = "mixer_1"
COMPONENT_MIXER_2 = "mixer_2"
COMPONENT_MIXER_3 = "mixer_3"
COMPONENT_MIXER_4 = "mixer_4"
COMPONENT_MIXER_5 = "mixer_5"
COMPONENT_MIXER_6 = "mixer_6"
COMPONENT_LAMBDA = "lambda"
COMPONENT_BUFFER = "buffer"
COMPONENT_SOLAR = "solar"

# Default component status template - used when no reg_params available
DEFAULT_COMPONENT_STATUS: dict[str, bool] = {
    COMPONENT_BOILER: True,
    COMPONENT_HUW: False,
    COMPONENT_MIXER_1: False,
    COMPONENT_MIXER_2: False,
    COMPONENT_MIXER_3: False,
    COMPONENT_MIXER_4: False,
    COMPONENT_MIXER_5: False,
    COMPONENT_MIXER_6: False,
    COMPONENT_LAMBDA: False,
    COMPONENT_BUFFER: False,
    COMPONENT_SOLAR: False,
}

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

# Legacy parameter modification endpoint (non-RM, uses newParamName)
API_NEW_PARAM_URI = "newParam"

# Editable parameters
API_EDITABLE_PARAMS_LIMITS_URI = "rmCurrentDataParamsEdits"
API_EDITABLE_PARAMS_LIMITS_DATA = "data"

# Optional LAN endpoint for editable-parameter metadata (module-dependent; may 404)
API_EDIT_PARAMS_URI = "editParams"

# =============================================================================
# RM... ENDPOINT CONSTANTS (Remote Menu API)
# =============================================================================
# These endpoints provide structured data for the ecoNET24 web interface
# Based on analysis of dev_set1.js and test fixtures

# Core RM endpoints for parameter management
API_RM_PARAMS_NAMES_URI = "rmParamsNames"
API_RM_PARAMS_DATA_URI = "rmParamsData"
API_RM_PARAMS_DESCS_URI = "rmParamsDescs"
API_RM_PARAMS_ENUMS_URI = "rmParamsEnums"
API_RM_PARAMS_UNITS_NAMES_URI = "rmParamsUnitsNames"

# RM endpoints for categories and structure
API_RM_STRUCTURE_URI = "rmStructure"

# RM endpoints for current data
API_RM_CURRENT_DATA_PARAMS_URI = "rmCurrentDataParams"
API_RM_CURRENT_DATA_PARAMS_EDITS_URI = "rmCurrentDataParamsEdits"

# RM endpoints for system information
API_RM_LANGS_URI = "rmLangs"
API_RM_EXISTING_LANGS_URI = "rmExistingLangs"
API_RM_LOCKS_NAMES_URI = "rmLocksNames"
API_RM_ALARMS_NAMES_URI = "rmAlarmsNames"

# RM endpoints for authentication and parameter modification
API_RM_ACCESS_URI = "rmAccess"  # Service password authentication
API_RM_NEW_PARAM_URI = "rmNewParam"  # Save parameter by index
API_RM_CURR_NEW_PARAM_URI = "rmCurrNewParam"  # Save current param by key

# RM endpoint data key (all endpoints use "data" as the key)
API_RM_DATA_KEY = "data"

# =============================================================================
# RM STRUCTURE ENTRY TYPES
# =============================================================================
# These constants define the entry types in rmStructure API response
# Each entry in the structure has a "type" field indicating its purpose

RM_STRUCTURE_TYPE_CATEGORY = 0  # Category entry - defines category context
RM_STRUCTURE_TYPE_PARAMETER = 1  # Editable parameter entry
RM_STRUCTURE_TYPE_DATA_REF = 3  # Data reference (read-only, has data_id)
RM_STRUCTURE_TYPE_MENU_GROUP = 7  # Menu group/header (resets pass_index)

# =============================================================================
# ALARM CODE CONSTANTS
# =============================================================================
ALARM_CODE_POWER_OUTAGE = 0
ALARM_CODE_CONTINUES = 255

# =============================================================================
# OPERATION MODES AND STATUS MAPPINGS
# =============================================================================
OPERATION_MODE_NAMES = {
    0: _STATE_OFF,
    1: "fire_up",
    2: "operation",
    3: "work",
    4: "supervision",
    5: _STATE_PAUSED,  # "halted",
    6: "stop",
    7: "burning_off",
    8: "manual",
    9: _STATE_PROBLEM,  # "alarm",
    10: "unsealing",
    11: "chimney",
    12: "stabilization",
    13: "no_transmission",
}

# =============================================================================
# MIXER CONFIGURATION CONSTANTS
# =============================================================================
NUMBER_OF_AVAILABLE_MIXERS = 6  # Supports up to 6 mixers (ecoMAX850R2-X has 5)
NUMBER_OF_AVAILABLE_ECOSTERS = 8  # Supports up to 8 ecoSTER thermostats
MIXER_AVAILABILITY_KEY = "mixerTemp"
MIXER_SET_AVAILABILITY_KEY = "mixerSetTemp"

# Dynamically generate SENSOR_MIXER_KEY
SENSOR_MIXER_KEY = {
    i: {f"{MIXER_AVAILABILITY_KEY}{i}", f"{MIXER_SET_AVAILABILITY_KEY}{i}"}
    for i in range(1, NUMBER_OF_AVAILABLE_MIXERS + 1)
}

# Mixer pump binary sensor keys
MIXER_PUMP_BINARY_SENSOR_KEYS = {
    f"mixerPumpWorks{i}" for i in range(1, NUMBER_OF_AVAILABLE_MIXERS + 1)
}

# Keywords that indicate mixer-related parameters for duplicate entity filtering
MIXER_RELATED_KEYWORDS: list[str] = [
    "mixer",
    "valve",
    "heating circuit",
    "actuator",
    "circuit",
]

