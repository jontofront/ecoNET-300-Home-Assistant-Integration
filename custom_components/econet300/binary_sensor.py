"""Econet binary sensor."""

from dataclasses import dataclass
import logging

from homeassistant.components.binary_sensor import (
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .common import Econet300Api, EconetDataCoordinator
from .common_functions import camel_to_snake, get_entity_component
from .const import (
    API_REG_PARAMS_URI,
    BINARY_SENSOR_MAP_KEY,
    CONF_CUSTOM_ENTITIES,
    DOMAIN,
    ECOSOL_BINARY_SENSORS,
    ECOSOL_CONTROLLER_IDS,
    ENTITY_BINARY_DEVICE_CLASS_MAP,
    ENTITY_CATEGORY,
    MIXER_PUMP_BINARY_SENSOR_KEYS,
    NUMBER_OF_AVAILABLE_ECOSTERS,
    SENSOR_MIXER_KEY,
    SERVICE_API,
    SERVICE_COORDINATOR,
)
from .entity import (
    EconetEntity,
    EcoSterEntity,
    MixerEntity,
    get_device_info_for_component,
)

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class EconetBinarySensorEntityDescription(BinarySensorEntityDescription):
    """Describes Econet binary sensor entity."""

    availability_key: str = ""
    component: str | None = None  # Component for device grouping (huw, mixer_1, etc.)


class EconetBinarySensor(EconetEntity, BinarySensorEntity):
    """Econet Binary Sensor."""

    entity_description: EconetBinarySensorEntityDescription

    def __init__(
        self,
        entity_description: EconetBinarySensorEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
    ):
        """Initialize a new ecoNET binary sensor."""
        self.entity_description = entity_description
        self.api = api
        self._attr_is_on: bool | None = None
        super().__init__(coordinator, api)
        _LOGGER.debug(
            "EconetBinarySensor initialized with unique_id: %s, entity_description: %s",
            self.unique_id,
            self.entity_description,
        )

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device info based on entity component."""
        component = getattr(self.entity_description, "component", None)
        if component:
            return get_device_info_for_component(component, self.api)
        # Fall back to parent class device_info (main boiler device)
        return super().device_info

    def _sync_state(self, value: bool):
        """Sync state."""
        value = bool(value)
        _LOGGER.debug("EconetBinarySensor _sync_state: %s", value)
        self._attr_is_on = value
        _LOGGER.debug(
            "Updated EconetBinarySensor _attr_is_on for %s: %s",
            self.entity_description.key,
            self._attr_is_on,
        )
        self.async_write_ha_state()

    @property
    def entity_category(self) -> EntityCategory | None:
        """Return the entity category."""
        return self.entity_description.entity_category


class MixerBinarySensor(MixerEntity, BinarySensorEntity):
    """Mixer Binary Sensor."""

    entity_description: EconetBinarySensorEntityDescription

    def __init__(
        self,
        entity_description: EconetBinarySensorEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
        idx: int,
    ):
        """Initialize a new mixer binary sensor."""
        super().__init__(entity_description, coordinator, api, idx)
        self._attr_is_on: bool | None = None
        _LOGGER.debug(
            "MixerBinarySensor initialized with unique_id: %s, entity_description: %s",
            self.unique_id,
            self.entity_description,
        )

    def _sync_state(self, value: bool):
        """Sync state."""
        value = bool(value)
        _LOGGER.debug("MixerBinarySensor _sync_state: %s", value)
        self._attr_is_on = value
        _LOGGER.debug(
            "Updated MixerBinarySensor _attr_is_on for %s: %s",
            self.entity_description.key,
            self._attr_is_on,
        )
        self.async_write_ha_state()


class EcoSterBinarySensor(EcoSterEntity, BinarySensorEntity):
    """EcoSter Binary Sensor."""

    entity_description: EconetBinarySensorEntityDescription

    def __init__(
        self,
        entity_description: EconetBinarySensorEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
        idx: int,
    ):
        """Initialize the EcoSter binary sensor."""
        super().__init__(entity_description, coordinator, api, idx)

    def _sync_state(self, value: bool):
        """Sync state."""
        _LOGGER.debug("EcoSter binary sensor sync state: %s", value)
        self._attr_is_on = value
        self.async_write_ha_state()


def create_binary_entity_description(key: str) -> EconetBinarySensorEntityDescription:
    """Create Econet300 binary entity description."""
    _LOGGER.debug("create_binary_entity_description: %s", key)
    entity_category = ENTITY_CATEGORY.get(key, None)
    _LOGGER.debug("Entity category for %s: %s", key, entity_category)

    # Determine component for device grouping based on key patterns
    component = get_entity_component(key, key)

    # All binary sensors now use icon translations
    # The translation_key will automatically link to icons.json
    entity_description = EconetBinarySensorEntityDescription(
        key=key,
        translation_key=camel_to_snake(key),
        device_class=ENTITY_BINARY_DEVICE_CLASS_MAP.get(key, None),
        entity_category=entity_category,
        component=component,
        # No icon or icon_off - Home Assistant will use icons.json automatically
    )
    _LOGGER.debug(
        "create_binary_entity_description: %s (component=%s)",
        entity_description,
        component,
    )
    return entity_description


def create_binary_sensors(coordinator: EconetDataCoordinator, api: Econet300Api):
    """Create binary sensors."""
    entities: list[EconetBinarySensor] = []
    if coordinator.data is None:
        _LOGGER.info("Coordinator data is None, no binary sensors will be created")
        return entities

    data_regParams = coordinator.data.get("regParams") or {}
    data_sysParams = coordinator.data.get("sysParams") or {}

    # Get controller ID to determine which binary sensors to create
    controller_id = data_sysParams.get("controllerID", None)

    # Always use default binary sensor mapping for all controllers
    binary_sensor_keys = BINARY_SENSOR_MAP_KEY["_default"].copy()
    if controller_id and controller_id in BINARY_SENSOR_MAP_KEY:
        _LOGGER.info(
            "ControllerID '%s' found in mapping, but using default binary sensor mapping",
            controller_id,
        )
    else:
        _LOGGER.info(
            "ControllerID '%s' not found in mapping, using default binary sensor mapping",
            controller_id if controller_id else "None",
        )

    # Always filter out ecoSTER binary sensors from controller binary sensors since they are created as separate devices
    ecoSTER_binary_sensors = BINARY_SENSOR_MAP_KEY.get("ecoSter", set())
    binary_sensor_keys = binary_sensor_keys - ecoSTER_binary_sensors

    _LOGGER.info(
        "Using binary sensor keys for controllerID '%s': %s",
        controller_id if controller_id else "None (default)",
        binary_sensor_keys,
    )

    for data_key in binary_sensor_keys:
        _LOGGER.debug(
            "Processing binary sensor data_key: %s from regParams & sysParams", data_key
        )
        if data_key in data_regParams:
            entity = EconetBinarySensor(
                create_binary_entity_description(data_key), coordinator, api
            )
            entities.append(entity)
            _LOGGER.debug("Created and appended entity from regParams: %s", entity)
        elif data_key in data_sysParams:
            entity = EconetBinarySensor(
                create_binary_entity_description(data_key), coordinator, api
            )
            entities.append(entity)
            _LOGGER.debug("Created and appended entity from sysParams: %s", entity)
        else:
            _LOGGER.debug(
                "key: %s is not mapped in regParams, binary sensor entity will not be added",
                data_key,
            )
    _LOGGER.info("Total entities created: %d", len(entities))
    return entities


def create_mixer_binary_sensors(coordinator: EconetDataCoordinator, api: Econet300Api):
    """Create mixer binary sensors."""
    entities: list[MixerBinarySensor] = []
    if coordinator.data is None:
        _LOGGER.info(
            "Coordinator data is None, no mixer binary sensors will be created"
        )
        return entities

    data_regParams = coordinator.data.get("regParams") or {}

    # Create mixer pump status sensors using the dynamic keys
    for mixer_pump_key in MIXER_PUMP_BINARY_SENSOR_KEYS:
        if (
            mixer_pump_key in data_regParams
            and data_regParams[mixer_pump_key] is not None
        ):
            # Extract mixer number from key (e.g., "mixerPumpWorks1" -> 1)
            mixer_number = int(mixer_pump_key.replace("mixerPumpWorks", ""))

            # Check if this mixer has valid temperature data (same logic as sensor creation)
            mixer_keys = SENSOR_MIXER_KEY.get(mixer_number, set())
            if any(data_regParams.get(mixer_key) is None for mixer_key in mixer_keys):
                _LOGGER.info(
                    "Mixer %d binary sensor will not be created due to invalid temperature data.",
                    mixer_number,
                )
                continue

            entity = MixerBinarySensor(
                create_binary_entity_description(mixer_pump_key),
                coordinator,
                api,
                mixer_number,
            )
            entities.append(entity)
            _LOGGER.debug("Created mixer binary sensor: %s", mixer_pump_key)

    _LOGGER.info("Total mixer binary sensor entities created: %d", len(entities))
    return entities


def create_ecoster_binary_sensors(
    coordinator: EconetDataCoordinator, api: Econet300Api
):
    """Create ecoSTER binary sensor entities."""
    entities: list[EcoSterBinarySensor] = []
    if coordinator.data is None:
        _LOGGER.info(
            "Coordinator data is None, no ecoSTER binary sensors will be created"
        )
        return entities

    sys_params = coordinator.data.get("sysParams", {})
    if sys_params is None:
        sys_params = {}

    # Check if moduleEcoSTERSoftVer is None
    if sys_params.get("moduleEcoSTERSoftVer") is None:
        _LOGGER.info(
            "moduleEcoSTERSoftVer is None, no ecoSTER binary sensors will be created"
        )
        return entities

    coordinator_data = coordinator.data.get("regParams", {})

    # Create ecoSTER binary sensors for each thermostat (1-8)
    for thermostat_idx in range(1, NUMBER_OF_AVAILABLE_ECOSTERS + 1):
        # Create contacts sensor
        contacts_key = f"ecoSterContacts{thermostat_idx}"
        if (
            contacts_key in coordinator_data
            and coordinator_data.get(contacts_key) is not None
        ):
            entities.append(
                EcoSterBinarySensor(
                    create_binary_entity_description(contacts_key),
                    coordinator,
                    api,
                    thermostat_idx,
                )
            )
            _LOGGER.debug("Created ecoSTER contacts sensor: %s", contacts_key)

        # Create day schedule sensor
        day_sched_key = f"ecoSterDaySched{thermostat_idx}"
        if (
            day_sched_key in coordinator_data
            and coordinator_data.get(day_sched_key) is not None
        ):
            entities.append(
                EcoSterBinarySensor(
                    create_binary_entity_description(day_sched_key),
                    coordinator,
                    api,
                    thermostat_idx,
                )
            )
            _LOGGER.debug("Created ecoSTER day schedule sensor: %s", day_sched_key)

    _LOGGER.info("Created %d ecoSTER binary sensors", len(entities))
    return entities


def create_ecosol_binary_sensors(coordinator: EconetDataCoordinator, api: Econet300Api):
    """Create ecoSOL-specific binary sensor entities (ecoSOL 500, ecoSOL 301, etc.)."""
    entities: list[EconetBinarySensor] = []
    sys_params = coordinator.data.get("sysParams", {})

    # Check if this is an ecoSOL controller
    controller_id = sys_params.get("controllerID", "")
    if controller_id not in ECOSOL_CONTROLLER_IDS:
        _LOGGER.debug("Not an ecoSOL controller, skipping ecoSOL binary sensors")
        return entities

    _LOGGER.info("Creating ecoSOL binary sensors for controller: %s", controller_id)

    # Get ecoSOL binary sensor keys (same for all ecoSOL models)
    ecoSOL_keys = ECOSOL_BINARY_SENSORS

    # Check data availability in both regParams and sysParams
    data_regParams = coordinator.data.get("regParams", {})
    data_sysParams = coordinator.data.get("sysParams", {})

    for data_key in ecoSOL_keys:
        _LOGGER.debug("Processing ecoSOL binary sensor: %s", data_key)

        # Check if data exists and is not None
        if data_key in data_regParams and data_regParams.get(data_key) is not None:
            entity = EconetBinarySensor(
                create_binary_entity_description(data_key), coordinator, api
            )
            entities.append(entity)
            _LOGGER.debug("Created ecoSOL binary sensor from regParams: %s", data_key)
        elif data_key in data_sysParams and data_sysParams.get(data_key) is not None:
            entity = EconetBinarySensor(
                create_binary_entity_description(data_key), coordinator, api
            )
            entities.append(entity)
            _LOGGER.debug("Created ecoSOL binary sensor from sysParams: %s", data_key)
        else:
            _LOGGER.info(
                "ecoSOL binary sensor %s not found or has no data, skipping",
                data_key,
            )

    _LOGGER.info("Created %d ecoSOL binary sensors", len(entities))
    return entities


# =============================================================================
# Unified custom binary sensors (user-selected via Options Flow)
# =============================================================================


class CustomBinarySensor(EconetEntity, BinarySensorEntity):
    """Binary sensor created from a user-selected parameter across any endpoint."""

    entity_description: EconetBinarySensorEntityDescription

    def __init__(
        self,
        entity_description: EconetBinarySensorEntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
        source: str,
        param_key: str,
    ):
        """Initialize a custom binary sensor."""
        self.entity_description = entity_description
        self.api = api
        self._source = source
        self._param_key = param_key
        self._attr_is_on: bool | None = None
        super().__init__(coordinator, api)

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device info based on entity component."""
        component = getattr(self.entity_description, "component", None)
        if component:
            return get_device_info_for_component(component, self.api)
        return super().device_info

    def _lookup_value(self):
        """Look up value from the configured data source."""
        if self.coordinator.data is None:
            return None
        if self._source == API_REG_PARAMS_URI:
            return self.coordinator.data.get("regParams", {}).get(self._param_key)
        # Both regParamsData and rmCurrentDataParams share the same numeric
        # ID space.  Try regParamsData first, then rmCurrentDataParams metadata.
        rpd = self.coordinator.data.get("regParamsData", {}) or {}
        rpd_value = rpd.get(self._param_key)
        if rpd_value is not None:
            return rpd_value
        cdp = self.coordinator.data.get("rmData", {}).get("currentDataParams", {})
        param = cdp.get(self._param_key)
        return param.get("value") if isinstance(param, dict) else param

    def _sync_state(self, value) -> None:
        """Synchronize the binary sensor state."""
        self._attr_is_on = bool(value)
        self.async_write_ha_state()


def create_custom_binary_sensors(
    coordinator: EconetDataCoordinator,
    api: Econet300Api,
    custom_entities: dict[str, dict[str, str]],
) -> list[CustomBinarySensor]:
    """Create binary sensor entities from user-selected parameters.

    Args:
        coordinator: The data coordinator.
        api: The device API.
        custom_entities: Dict from entry.options[CONF_CUSTOM_ENTITIES],
            shaped as {unique_id: {"source": str, "key": str, "name": str,
            "entity_type": str, "component": str, "entity_category": str|None}}.

    """
    entities: list[CustomBinarySensor] = []

    for _uid, cfg in custom_entities.items():
        if cfg.get("entity_type") != "binary_sensor":
            continue

        name = cfg.get("name", f"Parameter {cfg.get('key', _uid)}")
        source = cfg.get("source", "regParamsData")
        param_key = cfg.get("key", _uid)
        component = cfg.get("component")
        entity_key = f"custom_{source}_{param_key}"

        cat_str = cfg.get("entity_category")
        entity_category = EntityCategory.DIAGNOSTIC if cat_str == "diagnostic" else None

        description = EconetBinarySensorEntityDescription(
            key=entity_key,
            name=name,
            entity_category=entity_category,
            component=component,
            has_entity_name=True,
        )

        entities.append(
            CustomBinarySensor(description, coordinator, api, source, param_key)
        )

    _LOGGER.info("Created %d custom binary sensors", len(entities))
    return entities


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> bool:
    """Set up the binary sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id][SERVICE_COORDINATOR]
    api = hass.data[DOMAIN][entry.entry_id][SERVICE_API]

    entities: list[
        EconetBinarySensor
        | MixerBinarySensor
        | EcoSterBinarySensor
        | CustomBinarySensor
    ] = []

    # Create standard binary sensors (including controller-specific ones)
    entities.extend(create_binary_sensors(coordinator, api))

    # Create mixer binary sensors
    entities.extend(create_mixer_binary_sensors(coordinator, api))

    # Create ecoSTER binary sensors
    entities.extend(create_ecoster_binary_sensors(coordinator, api))

    # Create ecoSOL-specific binary sensors (ecoSOL 500, ecoSOL 301, etc.)
    entities.extend(create_ecosol_binary_sensors(coordinator, api))

    # Create user-defined custom binary sensors from Options Flow
    custom_cfg = entry.options.get(CONF_CUSTOM_ENTITIES, {})
    if custom_cfg:
        entities.extend(create_custom_binary_sensors(coordinator, api, custom_cfg))

    _LOGGER.info("Total binary sensor entities: %d", len(entities))
    async_add_entities(entities)
    return True
