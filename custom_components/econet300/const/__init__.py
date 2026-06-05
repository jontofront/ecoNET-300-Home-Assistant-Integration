"""Constants for ecoNET300 integration.

Organized into thematic submodules and re-exported here so existing
``from .const import X`` imports keep working unchanged:

- ``core``            – core/coordinator/device/API/RM/mode/mixer constants
- ``controllers``     – controller-specific sensor & binary-sensor key sets
- ``params``          – number/select param maps, unit lookups, dedup sets
- ``custom_entities`` – options-flow custom-entity selector constants
- ``entity_maps``     – unit / state-class / device-class / precision maps
- ``value_maps``      – integer-keyed value mappings and enum options
- ``processors``      – sensor value processors and helpers
- ``schedule``        – ecomaxSchedules name/key maps
"""

# Backward-compatible re-exports previously exposed by monolithic const.py.
from homeassistant.components.binary_sensor import BinarySensorDeviceClass  # noqa: F401
from homeassistant.components.number import NumberDeviceClass  # noqa: F401
from homeassistant.components.sensor import (  # noqa: F401
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import (  # noqa: F401
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    STATE_OFF,
    STATE_PAUSED,
    STATE_PROBLEM,
    STATE_UNKNOWN,
    EntityCategory,
    UnitOfEnergy,
    UnitOfMass,
    UnitOfPower,
    UnitOfTemperature,
    UnitOfTime,
)

from .controllers import *  # noqa: F401,F403
from .core import *  # noqa: F401,F403

# Explicit re-export so static analyzers resolve this shared constant reliably
# (wildcard re-exports of newly added names are not always picked up).
from .core import SENSITIVE_PARAM_KEYS  # noqa: F401
from .custom_entities import *  # noqa: F401,F403
from .entity_maps import *  # noqa: F401,F403
from .params import *  # noqa: F401,F403
from .processors import *  # noqa: F401,F403

# Internal helpers kept importable for backwards-compatible namespace parity.
from .processors import (  # noqa: F401
    _int_enum_lookup,
    _numeric_div10_or_none,
    _numeric_or_none,
)
from .schedule import *  # noqa: F401,F403
from .value_maps import *  # noqa: F401,F403
