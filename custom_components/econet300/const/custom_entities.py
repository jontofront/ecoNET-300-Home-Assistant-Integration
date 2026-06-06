"""Custom-entity selector constants and options-flow choice maps."""

from homeassistant.components.sensor import SensorDeviceClass as _SensorDeviceClass

from .core import DEFAULT_COMPONENT_STATUS
from .params import UNIT_NAME_TO_HA_UNIT

# =============================================================================
# CUSTOM ENTITY SELECTOR (Options Flow)
# =============================================================================
# Key used inside entry.options to store user-defined custom entities.
CONF_CUSTOM_ENTITIES = "custom_entities"

# Entity type constants for custom entity classification.
CUSTOM_ENTITY_TYPE_SENSOR = "sensor"
CUSTOM_ENTITY_TYPE_BINARY_SENSOR = "binary_sensor"

# Component choices for the Options Flow dropdown, built from DEFAULT_COMPONENT_STATUS.
CUSTOM_ENTITY_COMPONENTS: dict[str, str] = {
    key: key.replace("_", " ").title() for key in DEFAULT_COMPONENT_STATUS
}

# Sensor-specific options for the Options Flow configure_sensor step.
CUSTOM_SENSOR_UNIT_OPTIONS: dict[str | None, str] = {
    None: "None (auto)",
    **{unit: unit for unit in UNIT_NAME_TO_HA_UNIT},
}

CUSTOM_SENSOR_DEVICE_CLASS_OPTIONS: dict[str | None, str] = {
    None: "None (auto)",
    _SensorDeviceClass.TEMPERATURE: "Temperature",
    _SensorDeviceClass.POWER: "Power",
    _SensorDeviceClass.POWER_FACTOR: "Power factor",
    _SensorDeviceClass.ENERGY: "Energy",
    _SensorDeviceClass.HUMIDITY: "Humidity",
    _SensorDeviceClass.PRESSURE: "Pressure",
    _SensorDeviceClass.DURATION: "Duration",
    _SensorDeviceClass.SIGNAL_STRENGTH: "Signal strength",
    _SensorDeviceClass.WEIGHT: "Weight",
}

CUSTOM_SENSOR_PRECISION_OPTIONS: dict[int | None, str] = {
    None: "Auto",
    0: "0 (integer)",
    1: "0.0",
    2: "0.00",
    3: "0.000",
}

