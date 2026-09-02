"""Integer-keyed sensor value mappings and enum sensor option lists."""

from homeassistant.const import STATE_UNKNOWN as _STATE_UNKNOWN

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
    0: "off",  # modeTurnOff - TURNED OFF
    1: "stop",  # modeStop - STOP
    2: "fire_up",  # modeKindle - FIRE UP / KINDLING
    3: "operation",  # modeWork - OPERATION / WORK
    4: "supervision",  # modeSupervision - SUPERVISION
    5: "paused",  # modeHalt - HALTED / PAUSED
    6: "cleaning",  # modeCleaning - CLEANING
    7: "burning_off",  # modeExtinction - BURNING OFF / EXTINCTION
    8: "alarm",  # modeAlarm - ALARM
    9: "manual",  # modeManual - MANUAL
    10: "unsealing",  # modeUnsealing - UNSEALING
    11: "other",  # modeOther - OTHER
    12: "stabilization",  # modeStabilization - STABILIZATION
    13: "purge",  # modePurge - PURGE
    14: "check_flame",  # modeCheckFlame - CHECK FLAME
    15: "flame_losing",  # modeFlameLosing - FLAME LOSING
    16: "prevention",  # modePrevention - PREVENTION
    17: "work_grate",  # modeWorkGrate - WORK GRATE
    18: "supervision_grate",  # modeSupervisionGrate - SUPERVISION GRATE
    19: "calibration",  # modeCalibration - CALIBRATION
    20: "maintain",  # modeMaintain - MAINTAIN / MAINTENANCE
    21: "afterburning",  # modeAfterburning - AFTERBURNING
    22: "chimney_sweep",  # modeChimneySwep - CHIMNEY SWEEP
    23: "heating",  # modeHeats - HEATING
    24: "open_door",  # modeOpenDoor - OPEN DOOR
    25: "cooling",  # modeCooling - COOLING
    26: "safe",  # modeSafe - SAFE MODE
}

# Official ecoNET Mode{} table (cloud JS). mode, transmission, and statusCO share it.
SENSOR_MODE_MAPPING: dict[int, str] = SENSOR_STATUS_CO_MAPPING
OPERATION_MODE_NAMES: dict[int, str] = SENSOR_STATUS_CO_MAPPING

SENSOR_THERMOSTAT_MAPPING: dict[int, str] = {
    0: "off",
    1: "on",
}

# ecoMAX360i-specific value mappings
SENSOR_FLAP_VALVE_STATES_MAPPING: dict[int, str] = {
    0: "central_heating",
    3: "domestic_hot_water",
}

SENSOR_HEAT_DEMANDED_MAPPING: dict[int, str] = {
    0: "heat",
    1: "off",
}

SENSOR_WATER_PUMP_RUNNING_MAPPING: dict[int, str] = {
    0: "on",
    1: "unknown",
    2: "off",
}

# =============================================================================
# ENUM SENSOR OPTIONS
# =============================================================================
# Options for SensorDeviceClass.ENUM sensors - displayed in HA Developer Tools
SENSOR_ENUM_OPTIONS: dict[str, list[str]] = {
    "mode": [*SENSOR_STATUS_CO_MAPPING.values(), _STATE_UNKNOWN],
    "transmission": [*SENSOR_STATUS_CO_MAPPING.values(), _STATE_UNKNOWN],
    "statusCO": [*SENSOR_STATUS_CO_MAPPING.values(), _STATE_UNKNOWN],
    # ecoMAX360i enum options
    "flapValveStates": [*SENSOR_FLAP_VALVE_STATES_MAPPING.values(), _STATE_UNKNOWN],
    "HeatDemanded": [*SENSOR_HEAT_DEMANDED_MAPPING.values(), _STATE_UNKNOWN],
    "WaterPumpRunning": list(
        dict.fromkeys([*SENSOR_WATER_PUMP_RUNNING_MAPPING.values(), _STATE_UNKNOWN])
    ),
}
