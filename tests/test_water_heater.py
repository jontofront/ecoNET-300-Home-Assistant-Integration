"""Tests for the capability-gated ecoMAX360i DHW entity."""

import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

from homeassistant.const import Platform
import pytest

from custom_components.econet300 import PLATFORMS


def make_coordinator():
    """Build coordinator data from an existing controller fixture."""
    path = Path(__file__).parent / "fixtures" / "ecoMAX360-cf8" / "editParams.json"
    raw = json.loads(path.read_text())
    coordinator = MagicMock()
    coordinator.data = {
        "sysParams": {"controllerID": "ecoMAX360i", "protocolType": "gm3_pomp"},
        "regParams": {"TempCWU": 42.4},
        "editParams": raw["data"],
        "informationParams": raw["informationParams"],
        "_health": {"stale": False},
    }
    coordinator.single_device_tree = False
    coordinator.controller_device_id = None
    coordinator.async_request_refresh = AsyncMock()
    return coordinator


def test_water_heater_platform_registered():
    """Home Assistant must load the new platform."""
    assert Platform.WATER_HEATER in PLATFORMS


@pytest.mark.asyncio
async def test_setup_exposes_existing_dhw_data():
    """The platform combines existing data without fetching or writing."""
    import importlib.util

    assert (
        importlib.util.find_spec("custom_components.econet300.water_heater") is not None
    )
    from custom_components.econet300.water_heater import async_setup_entry

    coordinator = make_coordinator()
    api = MagicMock(uid="test-controller")
    api.set_param = AsyncMock()
    hass = MagicMock()
    hass.data = {"econet300": {"entry": {"api": api, "coordinator": coordinator}}}
    add = MagicMock()
    await async_setup_entry(hass, MagicMock(entry_id="entry"), add)
    entity = add.call_args.args[0][0]
    assert entity.native_current_temperature == 42.4
    assert entity.native_target_temperature == 50
    assert entity.min_temp == 35
    assert entity.max_temp == 60
    assert entity.unique_id == "test-controller-dhw"
    api.set_param.assert_not_awaited()
    coordinator.async_request_refresh.assert_not_awaited()


@pytest.mark.asyncio
async def test_valid_target_writes_only_setpoint():
    """A target write must not alter the DHW mode or other settings."""
    from custom_components.econet300.water_heater import EconetWaterHeater

    coordinator = make_coordinator()
    api = MagicMock(uid="test-controller", set_param=AsyncMock(return_value=True))
    entity = EconetWaterHeater(coordinator, api)
    await entity.async_set_temperature(temperature=55)
    api.set_param.assert_awaited_once_with("103", 55)
    coordinator.force_edit_params_refresh.assert_called_once()
    coordinator.async_request_refresh.assert_awaited_once()
    assert entity.native_target_temperature == 50


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "value", [34, 61, 50.5, float("nan"), float("inf"), True, "55"]
)
async def test_invalid_targets_never_write(value):
    """Reject out-of-range, malformed and fractional targets."""
    from homeassistant.exceptions import HomeAssistantError
    from custom_components.econet300.water_heater import EconetWaterHeater

    api = MagicMock(uid="test-controller", set_param=AsyncMock(return_value=True))
    entity = EconetWaterHeater(make_coordinator(), api)
    with pytest.raises(HomeAssistantError):
        await entity.async_set_temperature(temperature=value)
    api.set_param.assert_not_awaited()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "change", ["stale", "readonly", "locked", "missing", "offline"]
)
async def test_unsafe_state_never_writes(change):
    """Revalidate current metadata before every write."""
    from homeassistant.exceptions import HomeAssistantError
    from custom_components.econet300.water_heater import EconetWaterHeater

    c = make_coordinator()
    if change == "stale":
        c.data["_health"]["stale"] = True
    elif change == "offline":
        c.data["_health"]["online"] = False
    elif change == "readonly":
        c.data["editParams"]["103"]["edit"] = False
    elif change == "locked":
        c.data["editParams"]["103"]["locked"] = True
    else:
        c.data["editParams"].pop("103")
    api = MagicMock(uid="test-controller", set_param=AsyncMock())
    e = EconetWaterHeater(c, api)
    assert not e.available
    with pytest.raises(HomeAssistantError):
        await e.async_set_temperature(temperature=50)
    api.set_param.assert_not_awaited()


@pytest.mark.asyncio
async def test_rejected_write_raises():
    """Do not report a failed controller command as success."""
    from homeassistant.exceptions import HomeAssistantError
    from custom_components.econet300.water_heater import EconetWaterHeater

    api = MagicMock(uid="test-controller", set_param=AsyncMock(return_value=False))
    e = EconetWaterHeater(make_coordinator(), api)
    with pytest.raises(HomeAssistantError):
        await e.async_set_temperature(temperature=50)


@pytest.mark.parametrize("value", [None, "off", True, float("nan"), float("inf"), 999])
def test_invalid_measured_temperature_is_unknown(value):
    """Do not expose disconnected or nonnumeric measurements as temperature."""
    from custom_components.econet300.water_heater import EconetWaterHeater

    c = make_coordinator()
    c.data["regParams"]["TempCWU"] = value
    assert EconetWaterHeater(c, MagicMock()).native_current_temperature is None


@pytest.mark.asyncio
@pytest.mark.parametrize("change", ["controller", "protocol", "name", "limits", "mult"])
async def test_discovery_requires_verified_capabilities(change):
    """Do not attach this controller-specific mapping to incompatible data."""
    from custom_components.econet300.water_heater import async_setup_entry

    c = make_coordinator()
    if change == "controller":
        c.data["sysParams"]["controllerID"] = "ecoSOL"
    elif change == "protocol":
        c.data["sysParams"]["protocolType"] = "em"
    elif change == "name":
        c.data["editParams"]["103"]["name"] = "Other"
    elif change == "mult":
        c.data["editParams"]["103"]["mult"] = 10
    else:
        c.data["editParams"]["103"]["minv"] = 100
    hass = MagicMock()
    hass.data = {"econet300": {"entry": {"api": MagicMock(), "coordinator": c}}}
    add = MagicMock()
    await async_setup_entry(hass, MagicMock(entry_id="entry"), add)
    assert not add.called or add.call_args.args[0] == []


@pytest.mark.parametrize(
    ("raw", "expected"),
    [(0, "off"), (1, "on"), (2, "schedule"), (3, None), (True, None), (1.5, None)],
)
def test_dhw_mode_mapping(raw, expected):
    """Preserve controller mode semantics rather than infer heating activity."""
    from custom_components.econet300.water_heater import EconetWaterHeater

    c = make_coordinator()
    c.data["editParams"]["119"]["value"] = raw
    e = EconetWaterHeater(c, MagicMock())
    assert e.current_operation == expected
    assert e.operation_list == ["off", "on", "schedule"]


@pytest.mark.asyncio
@pytest.mark.parametrize(("mode", "value"), [("off", 0), ("on", 1), ("schedule", 2)])
async def test_mode_write_is_dhw_only(mode, value):
    """Mode changes must never write the global heat pump control."""
    from custom_components.econet300.water_heater import EconetWaterHeater

    c = make_coordinator()
    api = MagicMock(uid="test-controller", set_param=AsyncMock(return_value=True))
    e = EconetWaterHeater(c, api)
    await e.async_set_operation_mode(mode)
    api.set_param.assert_awaited_once_with("119", value)
    c.force_edit_params_refresh.assert_called_once()
    c.async_request_refresh.assert_awaited_once()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "change", ["unknown", "readonly", "locked", "renamed", "stale"]
)
async def test_unsafe_mode_write_is_rejected(change):
    """Unknown modes or incompatible metadata must never reach the device."""
    from homeassistant.exceptions import HomeAssistantError
    from custom_components.econet300.water_heater import EconetWaterHeater

    c = make_coordinator()
    mode = "schedule"
    if change == "unknown":
        mode = "boost"
    elif change == "readonly":
        c.data["editParams"]["119"]["edit"] = False
    elif change == "locked":
        c.data["editParams"]["119"]["locked"] = True
    elif change == "renamed":
        c.data["editParams"]["119"]["name"] = "Other"
    else:
        c.data["_health"]["stale"] = True
    api = MagicMock(uid="test-controller", set_param=AsyncMock())
    e = EconetWaterHeater(c, api)
    with pytest.raises(HomeAssistantError):
        await e.async_set_operation_mode(mode)
    api.set_param.assert_not_awaited()


@pytest.mark.asyncio
async def test_combined_temperature_and_mode_is_rejected_before_writing():
    """Reject non-atomic multi-command requests instead of partially applying them."""
    from homeassistant.exceptions import HomeAssistantError
    from custom_components.econet300.water_heater import EconetWaterHeater

    api = MagicMock(uid="test-controller", set_param=AsyncMock())
    e = EconetWaterHeater(make_coordinator(), api)
    with pytest.raises(HomeAssistantError):
        await e.async_set_temperature(temperature=50, operation_mode="off")
    api.set_param.assert_not_awaited()


def test_button_platform_registered():
    """HA must load the button platform for the DHW boost trigger."""
    assert Platform.BUTTON in PLATFORMS


@pytest.mark.asyncio
async def test_dhw_boost_button_created():
    """The DHW boost trigger appears as a button on the same device."""
    from custom_components.econet300.button import async_setup_entry

    coordinator = make_coordinator()
    api = MagicMock(uid="test-controller")
    hass = MagicMock()
    hass.data = {"econet300": {"entry": {"api": api, "coordinator": coordinator}}}
    add = MagicMock()
    await async_setup_entry(hass, MagicMock(entry_id="entry"), add)
    entities = add.call_args.args[0]
    assert len(entities) == 1
    assert entities[0].unique_id == "test-controller-dhw-boost"


@pytest.mark.asyncio
async def test_dhw_boost_press_writes_param_115():
    """Pressing boost triggers one-shot loading without touching other params."""
    from custom_components.econet300.button import EconetDhwBoostButton

    c = make_coordinator()
    api = MagicMock(uid="test-controller", set_param=AsyncMock(return_value=True))
    e = EconetDhwBoostButton(c, api)
    await e.async_press()
    api.set_param.assert_awaited_once_with("115", 1)
    c.force_edit_params_refresh.assert_called_once()
    c.async_request_refresh.assert_awaited_once()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "change", ["stale", "offline", "readonly", "locked", "missing"]
)
async def test_unsafe_boost_press_rejected(change):
    """Boost never writes when metadata is unsafe."""
    from homeassistant.exceptions import HomeAssistantError
    from custom_components.econet300.button import EconetDhwBoostButton

    c = make_coordinator()
    if change == "stale":
        c.data["_health"]["stale"] = True
    elif change == "offline":
        c.data["_health"]["online"] = False
    elif change == "readonly":
        c.data["editParams"]["115"]["edit"] = False
    elif change == "locked":
        c.data["editParams"]["115"]["locked"] = True
    else:
        c.data["editParams"].pop("115")
    api = MagicMock(uid="test-controller", set_param=AsyncMock())
    e = EconetDhwBoostButton(c, api)
    with pytest.raises(HomeAssistantError):
        await e.async_press()
    api.set_param.assert_not_awaited()
