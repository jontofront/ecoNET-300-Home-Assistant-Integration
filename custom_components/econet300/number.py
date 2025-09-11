"""Base entity number for Econet300."""

from dataclasses import dataclass
import logging

from homeassistant.components.number import (
    NumberEntity,
    NumberEntityDescription,
    NumberMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import Limits
from .common import Econet300Api, EconetDataCoordinator, skip_params_edits
from .common_functions import camel_to_snake
from .const import (
    DOMAIN,
    ENTITY_MAX_VALUE,
    ENTITY_MIN_VALUE,
    ENTITY_NUMBER_SENSOR_DEVICE_CLASS_MAP,
    ENTITY_NUMBER_SENSOR_MODE_MAP,
    ENTITY_STEP,
    ENTITY_UNIT_MAP,
    MIXER_HEATING_CURVE_PARAMS,
    NUMBER_MAP,
    RMNEWPARAM_PARAMS,
    SENSOR_MIXER_KEY,
    SERVICE_API,
    SERVICE_COORDINATOR,
)
from .entity import EconetEntity, MixerEntity

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class EconetNumberEntityDescription(NumberEntityDescription):
    """Describes ecoNET number entity."""


class EconetNumber(EconetEntity, NumberEntity):
    """Describes ecoNET number sensor entity."""

    entity_description: EconetNumberEntityDescription

    def __init__(
        self,
        entity_description: EconetNumberEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
    ):
        """Initialize a new ecoNET number entity."""
        self.entity_description = entity_description
        self.api = api
        super().__init__(coordinator, api)

    def _sync_state(self, value):
        """Sync the state of the ecoNET number entity."""
        _LOGGER.debug("ecoNETNumber _sync_state: %s", value)
        _LOGGER.debug(
            "DEBUG: Value type: %s, Value keys: %s",
            type(value),
            value.keys() if isinstance(value, dict) else "Not a dict",
        )

        # Handle both dict and direct value
        if isinstance(value, dict) and "value" in value:
            val = value.get("value")
            self._attr_native_value = float(val) if val is not None else None
            _LOGGER.debug(
                "DEBUG: Extracted value from dict: %s", self._attr_native_value
            )
        elif isinstance(value, (int, float, str)) and value is not None:
            self._attr_native_value = float(value)
            _LOGGER.debug("DEBUG: Using direct value: %s", self._attr_native_value)
        else:
            self._attr_native_value = None
            _LOGGER.debug("DEBUG: Invalid value type, setting to None: %s", value)

        map_key = NUMBER_MAP.get(self.entity_description.key)

        if map_key:
            self._set_value_limits(value)
        else:
            _LOGGER.error(
                "ecoNETNumber _sync_state: map_key %s not found in NUMBER_MAP",
                self.entity_description.key,
            )
        # Ensure the state is updated in Home Assistant.
        self.async_write_ha_state()
        # Create an asynchronous task for setting the limits.
        self.hass.async_create_task(self.async_set_limits_values())

    def _set_value_limits(self, value):
        """Set native min and max values for the entity."""
        if isinstance(value, dict):
            min_val = value.get("min")
            max_val = value.get("max")
            # Only update if we have valid values, otherwise keep existing values
            if min_val is not None:
                self._attr_native_min_value = float(min_val)
            if max_val is not None:
                self._attr_native_max_value = float(max_val)
        _LOGGER.debug(
            "ecoNETNumber _set_value_limits: min=%s, max=%s",
            self._attr_native_min_value,
            self._attr_native_max_value,
        )

    async def async_set_limits_values(self):
        """Async Sync number limits."""
        number_limits = await self.api.get_param_limits(self.entity_description.key)
        _LOGGER.debug("Number limits retrieved: %s", number_limits)

        if not number_limits:
            _LOGGER.info(
                "Cannot add number entity: %s, numeric limits for this entity is None",
                self.entity_description.key,
            )
            return

        # Directly set min and max values based on fetched limits.
        self._attr_native_min_value = (
            float(number_limits.min)
            if number_limits.min is not None
            else self._attr_native_min_value
        )
        self._attr_native_max_value = (
            float(number_limits.max)
            if number_limits.max is not None
            else self._attr_native_max_value
        )
        _LOGGER.debug("Apply number limits: %s", self)
        self.async_write_ha_state()

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        _LOGGER.debug("Set value: %s", value)

        # Skip processing if the value is unchanged.
        if value == self._attr_native_value:
            return

        if value > self._attr_native_max_value:
            _LOGGER.warning(
                "Requested value: '%s' exceeds maximum allowed value: '%s'",
                value,
                self._attr_max_value,
            )

        if value < self._attr_native_min_value:
            _LOGGER.warning(
                "Requested value: '%s' is below allowed value: '%s'",
                value,
                self._attr_min_value,
            )
            return

        if not await self.api.set_param(self.entity_description.key, int(value)):
            _LOGGER.warning("Setting value failed")
            return

        self._attr_native_value = value
        self.async_write_ha_state()


def can_add(key: str, coordinator: EconetDataCoordinator) -> bool:
    """Check if a given entity can be added based on the availability of data in the coordinator."""
    # For RMNEWPARAM_PARAMS, always allow creation (they're write-only parameters)
    if key in RMNEWPARAM_PARAMS:
        return True

    try:
        return (
            coordinator.has_param_edit_data(key)
            and coordinator.data["paramsEdits"][key]
        )
    except KeyError as e:
        _LOGGER.error("KeyError in can_add: %s", e)
        return False


def create_number_entity_description(
    key: str, limits: Limits | None = None
) -> EconetNumberEntityDescription:
    """Create ecoNET300 number entity description."""
    map_key = NUMBER_MAP.get(str(key), str(key))
    _LOGGER.debug("Creating number entity for key: %s", map_key)

    # Use limits if provided, otherwise use default values
    min_value = (
        float(limits.min)
        if limits and limits.min is not None
        else float(ENTITY_MIN_VALUE.get(map_key, 0))
    )
    max_value = (
        float(limits.max)
        if limits and limits.max is not None
        else float(ENTITY_MAX_VALUE.get(map_key, 100))
    )

    return EconetNumberEntityDescription(
        key=key,
        translation_key=camel_to_snake(map_key),
        device_class=ENTITY_NUMBER_SENSOR_DEVICE_CLASS_MAP.get(map_key),
        mode=ENTITY_NUMBER_SENSOR_MODE_MAP.get(map_key, NumberMode.BOX),  # type: ignore[arg-type]
        native_unit_of_measurement=ENTITY_UNIT_MAP.get(map_key),
        native_min_value=min_value,
        native_max_value=max_value,
        native_step=ENTITY_STEP.get(map_key, 1),
    )


def create_mixer_heating_curve_entities(
    coordinator: EconetDataCoordinator, api: Econet300Api
) -> list[MixerEntity]:
    """Create mixer heating curve number entities based on available mixers."""
    entities: list[MixerEntity] = []
    data_regParams = coordinator.data.get("regParams") or {}

    # Mixer heating curve parameter IDs (83-88)
    mixer_heating_curve_params = MIXER_HEATING_CURVE_PARAMS

    for mixer_number, mixer_keys in SENSOR_MIXER_KEY.items():
        # Check if this mixer has valid temperature data (same logic as other mixer entities)
        if any(data_regParams.get(mixer_key) is None for mixer_key in mixer_keys):
            _LOGGER.info(
                "Mixer %d heating curve will not be created due to invalid temperature data.",
                mixer_number,
            )
            continue

        # Create heating curve entity for this mixer
        param_id = str(82 + mixer_number)  # 83, 84, 85, 86, 87, 88
        if int(param_id) not in mixer_heating_curve_params:
            continue

        # Add this parameter to RMNEWPARAM_PARAMS for proper handling
        RMNEWPARAM_PARAMS.add(param_id)

        map_key = f"mixHeatCurve{mixer_number}"

        # Create entity description
        entity_description = EconetNumberEntityDescription(
            key=param_id,
            translation_key=camel_to_snake(map_key),
            native_unit_of_measurement=ENTITY_UNIT_MAP.get(map_key),
            device_class=ENTITY_NUMBER_SENSOR_DEVICE_CLASS_MAP.get(map_key),
            mode=ENTITY_NUMBER_SENSOR_MODE_MAP.get(map_key, NumberMode.BOX),  # type: ignore[arg-type]
            native_min_value=float(ENTITY_MIN_VALUE.get(map_key, 0.1)),
            native_max_value=float(ENTITY_MAX_VALUE.get(map_key, 4.0)),
            native_step=float(ENTITY_STEP.get(map_key, 0.1)),
        )

        # Create MixerEntity for this heating curve
        entity = MixerEntity(entity_description, coordinator, api, mixer_number)
        entities.append(entity)
        _LOGGER.debug(
            "Created mixer heating curve entity: %s for mixer %d", map_key, mixer_number
        )

    _LOGGER.info("Created %d mixer heating curve entities", len(entities))
    return entities


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""

    coordinator = hass.data[DOMAIN][entry.entry_id][SERVICE_COORDINATOR]
    api = hass.data[DOMAIN][entry.entry_id][SERVICE_API]

    entities: list[EconetNumber | MixerEntity] = []

    # Create mixer heating curve entities dynamically
    mixer_heating_curve_entities = create_mixer_heating_curve_entities(coordinator, api)
    entities.extend(mixer_heating_curve_entities)

    for key, map_key in NUMBER_MAP.items():
        sys_params = coordinator.data.get("sysParams", {})
        if skip_params_edits(sys_params):
            _LOGGER.info("Skipping number entity setup for controllerID: ecoMAX360i")
            continue

        # For RMNEWPARAM_PARAMS, use default limits instead of API limits
        if key in RMNEWPARAM_PARAMS:
            number_limits = None  # Will use ENTITY_MIN_VALUE/ENTITY_MAX_VALUE in create_number_entity_description
            _LOGGER.info(
                "Using default limits for RMNEWPARAM parameter %s: min=%s, max=%s, step=%s",
                key,
                ENTITY_MIN_VALUE.get(map_key, 0),
                ENTITY_MAX_VALUE.get(map_key, 80),
                ENTITY_STEP.get(map_key, 1),
            )
        else:
            number_limits = await api.get_param_limits(key)
            if number_limits is None:
                _LOGGER.info(
                    "Cannot add number entity: %s, numeric limits for this entity is None",
                    key,
                )
                continue

        if can_add(key, coordinator):
            entity_description = create_number_entity_description(key, number_limits)
            entities.append(EconetNumber(entity_description, coordinator, api))
        else:
            _LOGGER.info(
                "Cannot add number entity - availability key: %s does not exist",
                key,
            )

    return async_add_entities(entities)
