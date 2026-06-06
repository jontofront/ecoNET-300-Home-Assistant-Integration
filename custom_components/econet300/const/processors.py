"""Sensor value processors (raw API value -> display value) and their helper functions."""

from typing import Any, Final

from homeassistant.const import STATE_UNKNOWN as _STATE_UNKNOWN

from .core import OPERATION_MODE_NAMES
from .value_maps import (
    SENSOR_FLAP_VALVE_STATES_MAPPING,
    SENSOR_HEAT_DEMANDED_MAPPING,
    SENSOR_LAMBDA_STATUS_MAPPING,
    SENSOR_MODE_MAPPING,
    SENSOR_STATUS_CO_MAPPING,
    SENSOR_STATUS_CWU_MAPPING,
    SENSOR_THERMOSTAT_MAPPING,
    SENSOR_WATER_PUMP_RUNNING_MAPPING,
)

NO_CWU_TEMP_SET_STATUS_CODE = 128

ECOMAX360I_NUMERIC_SENSOR_PROCESSOR_KEYS: Final[tuple[str, ...]] = (
    "ActualDHWTemp",
    "ActualFlowTemp",
    "ActualReturnTemp",
    "AXENREGISTER64",
    "AXENREGISTER65",
    "Circuit1DesiredLWT",
    "COP",
    "ElectricalPower",
    "FanSpeed",
    "FlowRate",
    "HeatPumpAmbient",
    "HeatSourceCalcPresetTemp",
    "HPStatusPresetTemp",
    "SCOP",
    "TargetFlowTemp",
    "ThermalPower",
    "afterCompressorTemp",
    "beforeCompressorTemp",
    "exhaustGasTemp",
    "outdoorTemp",
    "ssaCorr",
    "ssaPrevTemp",
)


def _int_enum_lookup(mapping: dict[int, str], value: Any) -> str:
    """Look up an integer-keyed enum mapping, coercing string values from informationParams."""
    try:
        return mapping.get(int(value), _STATE_UNKNOWN)
    except (TypeError, ValueError):
        return _STATE_UNKNOWN


# scale-phnxreg2045-2046
def _numeric_div10_or_none(value: Any) -> float | None:
    """Return numeric value divided by 10, or None when unavailable."""
    numeric = _numeric_or_none(value)
    return None if numeric is None else numeric / 10


def _numeric_or_none(value: Any) -> float | None:
    """Return a numeric sensor value, or None when the controller reports a state."""
    if isinstance(value, bool) or value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


ENTITY_VALUE_PROCESSOR = {
    **dict.fromkeys(ECOMAX360I_NUMERIC_SENSOR_PROCESSOR_KEYS, _numeric_or_none),
    "mode": lambda x: SENSOR_MODE_MAPPING.get(x, _STATE_UNKNOWN),
    "lambdaStatus": lambda x: SENSOR_LAMBDA_STATUS_MAPPING.get(x, _STATE_UNKNOWN),
    "statusCWU": lambda x: SENSOR_STATUS_CWU_MAPPING.get(x, _STATE_UNKNOWN),
    "statusCO": lambda x: SENSOR_STATUS_CO_MAPPING.get(x, _STATE_UNKNOWN),
    "thermostat": lambda x: SENSOR_THERMOSTAT_MAPPING.get(x, _STATE_UNKNOWN),
    "transmission": lambda x: OPERATION_MODE_NAMES.get(x, _STATE_UNKNOWN),
    "PHNXreg2045": _numeric_div10_or_none,
    "PHNXreg2046": _numeric_div10_or_none,
    # ecoMAX360i-specific processors (informationParams yields string values)
    "flapValveStates": lambda x: _int_enum_lookup(SENSOR_FLAP_VALVE_STATES_MAPPING, x),
    "HeatDemanded": lambda x: _int_enum_lookup(SENSOR_HEAT_DEMANDED_MAPPING, x),
    "WaterPumpRunning": lambda x: _int_enum_lookup(
        SENSOR_WATER_PUMP_RUNNING_MAPPING, x
    ),
}

