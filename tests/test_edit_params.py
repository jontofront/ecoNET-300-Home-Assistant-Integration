"""Tests for the editParams catalog and editable-parameter entities.

Covers PR #234:
- ``build_edit_param_catalog`` (number/switch/select detection, skips, limits)
- ``_create_edit_param_numbers`` / ``_create_edit_param_selects`` /
  ``_create_edit_param_switches`` entity factories.

Covers issue #236:
- ``create_ecoster_number_entities`` / ``EcoSterNumber`` (ecoSTER setpoints
  ``STER_*_{N}`` read from editParams and written via newParam).
"""

from typing import cast
from unittest.mock import AsyncMock, MagicMock, patch

from homeassistant.components.number import NumberDeviceClass
from homeassistant.const import UnitOfTemperature
from homeassistant.exceptions import HomeAssistantError
import pytest

from custom_components.econet300.common import build_edit_param_catalog
from custom_components.econet300.const import DOMAIN
from custom_components.econet300.number import (
    EcoSterNumber,
    EditParamNumber,
    _create_edit_param_numbers,
    create_ecoster_number_entities,
)
from custom_components.econet300.select import (
    EditParamSelect,
    _create_edit_param_selects,
)
from custom_components.econet300.switch import (
    EditParamSwitch,
    _create_edit_param_switches,
)


def _make_api() -> MagicMock:
    """Create a mock API with the attributes editParams entities read."""
    api = MagicMock()
    api.uid = "test-uid"
    api.model_id = "ecoMAX360i"
    api.host = "http://test"
    api.sw_rev = "1.0"
    api.hw_ver = "hw1"
    return api


# ============================================================================
# build_edit_param_catalog
# ============================================================================


class TestBuildEditParamCatalog:
    """Test normalization of /econet/editParams into a writable catalog."""

    def test_empty_input(self):
        assert build_edit_param_catalog({}) == {}
        assert build_edit_param_catalog(None) == {}

    def test_number_with_explicit_limits(self):
        raw = {
            "data": {
                "1280": {
                    "edit": True,
                    "name": "Boiler temp",
                    "value": 55,
                    "unit": 1,
                    "minv": 40,
                    "maxv": 80,
                }
            }
        }
        item = build_edit_param_catalog(raw)["1280"]
        assert item["kind"] == "number"
        assert item["unit"] == "°C"
        assert item["min"] == 40
        assert item["max"] == 80
        assert item["step"] == 1.0
        assert item["value"] == 55

    def test_binary_zero_one_becomes_switch(self):
        raw = {
            "data": {
                "10": {
                    "edit": True,
                    "name": "Pump enable",
                    "value": 1,
                    "minv": 0,
                    "maxv": 1,
                }
            }
        }
        item = build_edit_param_catalog(raw)["10"]
        assert item["kind"] == "switch"
        assert item["unit"] is None

    def test_small_integer_range_becomes_select(self):
        raw = {
            "data": {
                "20": {
                    "edit": True,
                    "name": "Mode",
                    "value": 2,
                    "minv": 0,
                    "maxv": 5,
                }
            }
        }
        item = build_edit_param_catalog(raw)["20"]
        assert item["kind"] == "select"
        assert item["options"] == ["0", "1", "2", "3", "4", "5"]

    def test_limits_from_editable_params_list(self):
        raw = {
            "data": {"30": {"edit": True, "name": "Setting", "value": 50}},
            "editableParams": {"30": [0, 0, 0, 10, 90, 5]},
        }
        item = build_edit_param_catalog(raw)["30"]
        assert item["min"] == 10
        assert item["max"] == 90
        assert item["step"] == 5
        assert item["kind"] == "number"

    def test_zero_one_without_limits_exposes_number(self):
        raw = {"data": {"40": {"edit": True, "name": "Flag", "value": 0}}}
        item = build_edit_param_catalog(raw)["40"]
        assert item["kind"] == "switch"
        assert item["expose_number"] is True

    def test_skips_non_editable(self):
        raw = {"data": {"50": {"edit": False, "name": "RO", "value": 5}}}
        assert "50" not in build_edit_param_catalog(raw)

    def test_skips_non_numeric_value(self):
        raw = {"data": {"60": {"edit": True, "name": "Text", "value": "abc"}}}
        assert "60" not in build_edit_param_catalog(raw)

    def test_skips_malformed_entry(self):
        raw = {"data": {"70": "not-a-dict"}}
        assert build_edit_param_catalog(raw) == {}


# ============================================================================
# entity factories
# ============================================================================


def _catalog() -> dict:
    """Build a representative catalog covering all entity kinds."""
    raw = {
        "data": {
            "n1": {
                "edit": True,
                "name": "Boiler temp",
                "value": 55,
                "unit": 1,
                "minv": 40,
                "maxv": 80,
            },
            "s1": {
                "edit": True,
                "name": "Pump",
                "value": 1,
                "minv": 0,
                "maxv": 1,
            },
            "sel1": {
                "edit": True,
                "name": "Mode",
                "value": 2,
                "minv": 0,
                "maxv": 5,
            },
            "e1": {"edit": True, "name": "Flag", "value": 0},
            "ro": {"edit": False, "name": "RO", "value": 9},
        }
    }
    return build_edit_param_catalog(raw)


def _coordinator(catalog: dict) -> MagicMock:
    coordinator = MagicMock()
    coordinator.data = {"editParamCatalog": catalog}
    return coordinator


class TestCreateEditParamEntities:
    """Test the per-platform editParams entity factories."""

    def test_numbers_include_number_and_expose_number(self):
        catalog = _catalog()
        entities = _create_edit_param_numbers(_coordinator(catalog), _make_api())

        assert all(isinstance(e, EditParamNumber) for e in entities)
        numbers = cast("list[EditParamNumber]", entities)
        assert {e._pid for e in numbers} == {"n1", "e1"}

    def test_switches_match_switch_kind(self):
        catalog = _catalog()
        entities = _create_edit_param_switches(_coordinator(catalog), _make_api())

        assert all(isinstance(e, EditParamSwitch) for e in entities)
        switches = cast("list[EditParamSwitch]", entities)
        assert {e._pid for e in switches} == {"s1", "e1"}

    def test_selects_match_select_kind(self):
        catalog = _catalog()
        entities = _create_edit_param_selects(_coordinator(catalog), _make_api())

        assert len(entities) == 1
        assert isinstance(entities[0], EditParamSelect)
        select = cast("EditParamSelect", entities[0])
        assert select._pid == "sel1"

    def test_expose_number_uses_value_suffix_unique_id(self):
        catalog = _catalog()
        entities = _create_edit_param_numbers(_coordinator(catalog), _make_api())
        numbers = cast("list[EditParamNumber]", entities)
        by_pid = {e._pid: e for e in numbers}

        assert by_pid["n1"].unique_id == "test-uid-edit_n1"
        assert by_pid["e1"].unique_id == "test-uid-edit_e1_value"

    def test_number_native_value_and_limits(self):
        catalog = _catalog()
        entities = _create_edit_param_numbers(_coordinator(catalog), _make_api())
        numbers = cast("list[EditParamNumber]", entities)
        number = next(e for e in numbers if e._pid == "n1")

        assert number.native_value == 55
        assert number.native_min_value == 40
        assert number.native_max_value == 80

    def test_select_current_option_for_value_in_options(self):
        catalog = _catalog()
        select = _create_edit_param_selects(_coordinator(catalog), _make_api())[0]
        select = cast("EditParamSelect", select)

        assert select.options == ["0", "1", "2", "3", "4", "5"]
        assert select.current_option == "2"

    def test_select_current_option_none_when_value_not_in_options(self):
        """HA contract: current_option must be one of options or None."""
        catalog = _catalog()
        # Device reports a value outside the declared options list.
        catalog["sel1"]["value"] = 9
        select = _create_edit_param_selects(_coordinator(catalog), _make_api())[0]
        select = cast("EditParamSelect", select)

        assert "9" not in select.options
        assert select.current_option is None

    def test_select_current_option_none_when_value_missing(self):
        catalog = _catalog()
        catalog["sel1"]["value"] = None
        select = _create_edit_param_selects(_coordinator(catalog), _make_api())[0]
        select = cast("EditParamSelect", select)

        assert select.current_option is None


# ============================================================================
# ecoSTER setpoint numbers (issue #236)
# ============================================================================


def _ecoster_coordinator(load_fixture, controller: str = "ecoMAX860D3-HB"):
    """Build a coordinator mock with sysParams and editParams.data from fixtures."""
    coordinator = MagicMock()
    coordinator.single_device_tree = False
    coordinator.async_request_refresh = AsyncMock()
    coordinator.data = {
        "sysParams": load_fixture(controller, "sysParams.json"),
        "editParams": load_fixture(controller, "editParams.json").get("data", {}),
    }
    return coordinator


def _ecoster_numbers(coordinator, api=None) -> dict[str, EcoSterNumber]:
    """Create ecoSTER numbers and index them by entity key."""
    entities = create_ecoster_number_entities(coordinator, api or _make_api())
    return {e.entity_description.key: e for e in entities}


class TestCreateEcoSterNumbers:
    """Test which ecoSTER setpoint numbers are created from editParams."""

    def test_two_panels_from_ecomax860d3_fixture(self, load_fixture):
        numbers = _ecoster_numbers(_ecoster_coordinator(load_fixture))

        params = (
            "STER_TEMP_ANTIFREEZ",
            "STER_TEMP_DAY",
            "STER_TEMP_NIGHT",
            "STER_TEMP_SET_PARTY",
            "STER_TEMP_SET_SUMMER",
        )
        expected = {f"{param}_{idx}" for param in params for idx in (1, 2)}
        assert set(numbers) == expected

    def test_single_panel_from_ecomax850p_fixture(self, load_fixture):
        coordinator = _ecoster_coordinator(load_fixture, "ecoMAX850P-R")
        numbers = _ecoster_numbers(coordinator)

        assert "STER_TEMP_DAY_1" in numbers
        assert not any(key.endswith("_2") for key in numbers)

    def test_no_numbers_without_ecoster_panel(self, load_fixture):
        coordinator = _ecoster_coordinator(load_fixture)
        coordinator.data["sysParams"]["moduleEcoSTERSoftVer"] = None

        assert _ecoster_numbers(coordinator) == {}

    def test_no_numbers_without_coordinator_data(self):
        coordinator = MagicMock()
        coordinator.data = None

        assert _ecoster_numbers(coordinator) == {}

    def test_skips_invalid_entries(self, load_fixture):
        coordinator = _ecoster_coordinator(load_fixture)
        edit_params = coordinator.data["editParams"]
        edit_params["STER_TEMP_DAY_1"]["edit"] = False
        del edit_params["STER_TEMP_NIGHT_1"]["maxv"]
        edit_params["STER_TEMP_DAY_2"]["value"] = None

        numbers = _ecoster_numbers(coordinator)

        assert "STER_TEMP_DAY_1" not in numbers
        assert "STER_TEMP_NIGHT_1" not in numbers
        assert "STER_TEMP_DAY_2" not in numbers
        assert "STER_TEMP_NIGHT_2" in numbers

    def test_only_day_and_night_enabled_by_default(self, load_fixture):
        numbers = _ecoster_numbers(_ecoster_coordinator(load_fixture))

        enabled = {k for k, e in numbers.items() if e.entity_registry_enabled_default}
        assert enabled == {
            "STER_TEMP_DAY_1",
            "STER_TEMP_DAY_2",
            "STER_TEMP_NIGHT_1",
            "STER_TEMP_NIGHT_2",
        }


class TestEcoSterNumber:
    """Test EcoSterNumber state, metadata and writes."""

    def test_description_from_editparams_entry(self, load_fixture):
        number = _ecoster_numbers(_ecoster_coordinator(load_fixture))["STER_TEMP_DAY_2"]

        assert number.native_min_value == 10.0
        assert number.native_max_value == 35.0
        assert number.native_step == 0.1
        assert number.device_class == NumberDeviceClass.TEMPERATURE
        assert number.native_unit_of_measurement == UnitOfTemperature.CELSIUS
        assert number.translation_key == "ster_temp_day"
        assert number.translation_placeholders == {"index": "2"}

    def test_unique_id_and_ecoster_device(self, load_fixture):
        number = _ecoster_numbers(_ecoster_coordinator(load_fixture))["STER_TEMP_DAY_2"]

        assert number.unique_id == "test-uid-STER_TEMP_DAY_2"
        device_info = number.device_info
        assert device_info is not None
        assert device_info.get("identifiers") == {(DOMAIN, "test-uid-ecoster-2")}

    def test_value_synced_from_editparams(self, load_fixture):
        number = _ecoster_numbers(_ecoster_coordinator(load_fixture))["STER_TEMP_DAY_1"]

        with patch.object(number, "async_write_ha_state"):
            number._sync_state(number._lookup_value())

        assert number.native_value == 23.1

    def test_unavailable_when_entry_disappears(self, load_fixture):
        coordinator = _ecoster_coordinator(load_fixture)
        number = _ecoster_numbers(coordinator)["STER_TEMP_DAY_1"]
        assert number.available is True

        del coordinator.data["editParams"]["STER_TEMP_DAY_1"]

        assert number.available is False

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("requested", "sent"),
        [(22.6, 22.6), (22.0, 22), (22.649999999, 22.6)],
    )
    async def test_set_value_writes_via_set_param(self, load_fixture, requested, sent):
        coordinator = _ecoster_coordinator(load_fixture)
        api = _make_api()
        api.set_param = AsyncMock(return_value=True)
        number = _ecoster_numbers(coordinator, api)["STER_TEMP_DAY_2"]

        with patch.object(number, "async_write_ha_state"):
            await number.async_set_native_value(requested)

        api.set_param.assert_awaited_once_with("STER_TEMP_DAY_2", sent)
        assert type(api.set_param.await_args.args[1]) is type(sent)
        assert number.native_value == float(sent)
        coordinator.force_edit_params_refresh.assert_called_once()
        coordinator.async_request_refresh.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_set_value_failure_raises(self, load_fixture):
        coordinator = _ecoster_coordinator(load_fixture)
        api = _make_api()
        api.set_param = AsyncMock(return_value=False)
        number = _ecoster_numbers(coordinator, api)["STER_TEMP_DAY_1"]

        with pytest.raises(HomeAssistantError):
            await number.async_set_native_value(21.5)

        coordinator.async_request_refresh.assert_not_awaited()
