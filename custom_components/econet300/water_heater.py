"""DHW water heater for ecoMAX360i controllers with explicit setpoint metadata."""

import math
from typing import Any

from homeassistant.components.button import ButtonEntity
from homeassistant.components.water_heater import (
    WaterHeaterEntity,
    WaterHeaterEntityFeature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api import Econet300Api
from .common import EconetDataCoordinator
from .common_functions import is_ecomax360i_controller
from .const import DOMAIN, SERVICE_API, SERVICE_COORDINATOR, _numeric_or_none
from .const.processors import TEMP_NOT_CONNECTED_VALUE
from .entity import _main_device_info

DHW_SETPOINT_PARAM = "103"
DHW_MODE_PARAM = "119"
DHW_BOOST_PARAM = "115"  # HDWStartOneLoading, momentary one-shot trigger
# ecoMAX360i mapping: 0=off, 1=on, 2=schedule. 0 and 2 observed live; 1=on
# confirmed by the user against the controller. Also corroborated by the
# vendor enum 101:['off','on','schedule'] in
# docs/cloud_translations/js_files/dev_set3.js and by LeeNuss'
# sensors-inputs-ecomax360i branch (DHW_WORK_MODE_VALUES).
DHW_MODES = {0: "off", 1: "on", 2: "schedule"}


def _finite_number(value: Any) -> float | None:
    numeric = _numeric_or_none(value)
    return numeric if numeric is not None and math.isfinite(numeric) else None


def _valid_setpoint(data: dict[str, Any]) -> bool:
    entry = (data.get("editParams") or {}).get(DHW_SETPOINT_PARAM)
    if not isinstance(entry, dict):
        return False
    minimum = _finite_number(entry.get("minv"))
    maximum = _finite_number(entry.get("maxv"))
    return (
        entry.get("name") == "HDWTSetPoint"
        and entry.get("unit") == 1
        and entry.get("mult") == 1
        and entry.get("edit") is True
        and not entry.get("locked", False)
        and minimum is not None
        and maximum is not None
        and minimum < maximum
    )


def _valid_boost_param(data: dict[str, Any]) -> bool:
    """Return True when the momentary boost trigger is present and writable."""
    entry = (data.get("editParams") or {}).get(DHW_BOOST_PARAM)
    return (
        isinstance(entry, dict)
        and entry.get("name") == "HDWStartOneLoading"
        and entry.get("edit") is True
        and not entry.get("locked", False)
        and entry.get("mult") == 1
    )


def _dhw_platform_supported(data: dict[str, Any]) -> bool:
    """Return True when this controller is a supported DHW platform target."""
    sys_params = data.get("sysParams") or {}
    return (
        is_ecomax360i_controller(sys_params.get("controllerID"))
        and sys_params.get("protocolType") == "gm3_pomp"
        and _valid_setpoint(data)
    )


class EconetWaterHeater(CoordinatorEntity[EconetDataCoordinator], WaterHeaterEntity):
    """Combine controller-owned DHW temperature and setpoint data."""

    _attr_has_entity_name = True
    _attr_translation_key = "dhw"
    _attr_supported_features = (
        WaterHeaterEntityFeature.TARGET_TEMPERATURE
        | WaterHeaterEntityFeature.OPERATION_MODE
    )
    _attr_operation_list = ["off", "on", "schedule"]
    _attr_native_temperature_unit = UnitOfTemperature.CELSIUS
    _attr_target_temperature_step = 1.0

    def __init__(self, coordinator: EconetDataCoordinator, api: Econet300Api) -> None:
        """Initialize without device I/O."""
        super().__init__(coordinator)
        self._api = api
        self._initial_min = self._setpoint.get("minv", 35)
        self._initial_max = self._setpoint.get("maxv", 65)
        self._attr_unique_id = f"{api.uid}-dhw"
        self._attr_device_info = _main_device_info(api)

    @property
    def native_current_temperature(self) -> float | None:
        """Return the cylinder temperature from registers."""
        value = _finite_number(
            (self.coordinator.data or {}).get("regParams", {}).get("TempCWU")
        )
        return None if value == TEMP_NOT_CONNECTED_VALUE else value

    @property
    def native_target_temperature(self) -> float | None:
        """Return the controller's DHW setpoint."""
        return _finite_number(self._setpoint.get("value"))

    @property
    def _setpoint(self) -> dict[str, Any]:
        return (
            (self.coordinator.data or {})
            .get("editParams", {})
            .get(DHW_SETPOINT_PARAM, {})
        )

    @property
    def current_operation(self) -> str | None:
        """Return DHW policy, not compressor activity."""
        entry = (
            (self.coordinator.data or {}).get("editParams", {}).get(DHW_MODE_PARAM, {})
        )
        value = entry.get("value")
        if type(value) is not int:
            return None
        return DHW_MODES.get(value)

    async def async_set_operation_mode(self, operation_mode: str) -> None:
        """Change only the controller's DHW user mode."""
        entry = (
            (self.coordinator.data or {}).get("editParams", {}).get(DHW_MODE_PARAM, {})
        )
        if (
            not self.available
            or entry.get("name") != "HDWusermode"
            or entry.get("edit") is not True
            or entry.get("locked", False)
            or entry.get("mult") != 1
            or operation_mode not in DHW_MODES.values()
        ):
            raise HomeAssistantError("DHW mode is unavailable or unsupported")
        value = next(
            value for value, name in DHW_MODES.items() if name == operation_mode
        )
        if not await self._api.set_param(DHW_MODE_PARAM, value):
            raise HomeAssistantError("Controller rejected the DHW mode")
        self.coordinator.force_edit_params_refresh()
        await self.coordinator.async_request_refresh()

    @property
    def min_temp(self) -> float:
        """Return the controller's minimum setpoint."""
        return self._setpoint.get("minv", self._initial_min)

    @property
    def max_temp(self) -> float:
        """Return the controller's maximum setpoint."""
        return self._setpoint.get("maxv", self._initial_max)

    @property
    def available(self) -> bool:
        """Block control when the controller or writable metadata is unavailable."""
        data = self.coordinator.data or {}
        health = data.get("_health") or {}
        return bool(
            super().available
            and not health.get("stale", False)
            and health.get("online", True)
            and _valid_setpoint(data)
        )

    async def async_set_temperature(self, **kwargs: Any) -> None:
        """Change only the DHW target, respecting current controller limits."""
        raw = kwargs.get(ATTR_TEMPERATURE)
        value = _finite_number(raw)
        if (
            not self.available
            or kwargs.get("operation_mode") is not None
            or not isinstance(raw, (int, float))
            or isinstance(raw, bool)
            or value is None
            or not value.is_integer()
            or not self.min_temp <= value <= self.max_temp
        ):
            raise HomeAssistantError(
                "DHW target is unavailable or outside controller limits"
            )
        if not await self._api.set_param(DHW_SETPOINT_PARAM, int(value)):
            raise HomeAssistantError("Controller rejected the DHW target")
        self.coordinator.force_edit_params_refresh()
        await self.coordinator.async_request_refresh()


# Older HA releases consume the legacy names; do not override deprecated
# members on HA 2026.11+, where native temperature properties are supported.
if not hasattr(WaterHeaterEntity, "native_current_temperature"):
    setattr(
        EconetWaterHeater,
        "current_temperature",
        EconetWaterHeater.native_current_temperature,
    )
    setattr(
        EconetWaterHeater,
        "target_temperature",
        EconetWaterHeater.native_target_temperature,
    )
    setattr(
        EconetWaterHeater,
        "temperature_unit",
        property(lambda self: self._attr_native_temperature_unit),
    )


class EconetDhwBoostButton(CoordinatorEntity[EconetDataCoordinator], ButtonEntity):
    """One-shot DHW loading trigger (param HDWStartOneLoading)."""

    _attr_has_entity_name = True
    _attr_translation_key = "dhw_boost"

    def __init__(self, coordinator: EconetDataCoordinator, api: Econet300Api) -> None:
        """Initialize the momentary boost trigger without device I/O."""
        super().__init__(coordinator)
        self._api = api
        self._attr_unique_id = f"{api.uid}-dhw-boost"
        self._attr_device_info = _main_device_info(api)

    @property
    def available(self) -> bool:
        """Block the trigger when controller data or boost metadata is unsafe."""
        data = self.coordinator.data or {}
        health = data.get("_health") or {}
        return bool(
            super().available
            and not health.get("stale", False)
            and health.get("online", True)
            and _valid_boost_param(data)
        )

    async def async_press(self) -> None:
        """Trigger a single DHW loading cycle on the controller."""
        if not self.available:
            raise HomeAssistantError("DHW boost is unavailable or unsupported")
        if not await self._api.set_param(DHW_BOOST_PARAM, 1):
            raise HomeAssistantError("Controller rejected the DHW boost")
        self.coordinator.force_edit_params_refresh()
        await self.coordinator.async_request_refresh()


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the DHW platform for supported controllers."""
    services = hass.data[DOMAIN][entry.entry_id]
    coordinator = services[SERVICE_COORDINATOR]
    data = coordinator.data or {}
    if _dhw_platform_supported(data):
        async_add_entities([EconetWaterHeater(coordinator, services[SERVICE_API])])
