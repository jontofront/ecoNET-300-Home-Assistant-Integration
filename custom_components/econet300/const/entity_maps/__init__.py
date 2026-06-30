"""Per-entity attribute maps: units, state classes, device classes, precision, category and value limits.

Organized into thematic submodules:

- ``units``          – unit-of-measurement mappings
- ``state_classes``  – sensor state-class mappings
- ``device_classes`` – sensor / number / binary-sensor device-class mappings
- ``precision``      – suggested display precision mappings
- ``categories``     – entity category mappings
- ``value_limits``   – min / max / step for number entities
"""

from .categories import *  # noqa: F401,F403
from .device_classes import *  # noqa: F401,F403
from .precision import *  # noqa: F401,F403
from .state_classes import *  # noqa: F401,F403
from .state_classes import (
    DEFAULT_SENSOR_STATE_CLASS as DEFAULT_SENSOR_STATE_CLASS,  # noqa: F401,PLC0414
)
from .units import *  # noqa: F401,F403
from .value_limits import *  # noqa: F401,F403
