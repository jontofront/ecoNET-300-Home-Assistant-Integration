"""Tests for Unified Custom Entity Selector (Options Flow + custom entity factories).

Covers:
- Helper functions (_get_unmapped_keys, _build_multiselect_options)
- CustomSensor factory and _lookup_value for all 3 sources
- CustomBinarySensor factory and _lookup_value for all 3 sources
- Device grouping via component in entity descriptions
"""

import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest

from custom_components.econet300.binary_sensor import (
    CustomBinarySensor,
    create_custom_binary_sensors,
)
from custom_components.econet300.config_flow import (
    _build_multiselect_options,
    _get_unmapped_keys,
)
from custom_components.econet300.const import (
    API_REG_PARAMS_DATA_URI,
    API_REG_PARAMS_URI,
    API_RM_CURRENT_DATA_PARAMS_URI,
    STATIC_REGPARAMS_DATA_IDS,
    STATIC_REGPARAMS_KEYS,
)
from custom_components.econet300.sensor import (
    CustomSensor,
    create_custom_sensors,
)

FIXTURES_ROOT = Path(__file__).parent / "fixtures"


def _load_fixture(device: str, filename: str) -> dict[str, Any]:
    """Load a JSON fixture file for a device."""
    path = FIXTURES_ROOT / device / filename
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def _make_coordinator(
    reg_params: dict[str, Any] | None = None,
    reg_params_data: dict[str, Any] | None = None,
    rm_data: dict[str, Any] | None = None,
) -> MagicMock:
    """Create a mock coordinator with the given data."""
    coordinator = MagicMock()
    coordinator.data = {
        "regParams": reg_params or {},
        "regParamsData": reg_params_data or {},
        "rmData": rm_data or {},
    }
    return coordinator


def _make_api() -> MagicMock:
    """Create a mock API instance."""
    api = MagicMock()
    api.uid = "test-uid"
    api.model_id = "ecoMAX810P-L"
    api.host = "http://test"
    api.sw_rev = "1.0"
    return api


# ============================================================================
# _get_unmapped_keys tests — regParams
# ============================================================================


class TestGetUnmappedKeysRegParams:
    """Test filtering of unmapped regParams keys."""

    def test_returns_empty_for_none_data(self):
        assert _get_unmapped_keys(None, API_REG_PARAMS_URI) == {}

    def test_returns_empty_for_missing_regparams(self):
        assert _get_unmapped_keys({"sysParams": {}}, API_REG_PARAMS_URI) == {}

    def test_filters_out_static_keys(self):
        """Keys in STATIC_REGPARAMS_KEYS should be excluded."""
        if not STATIC_REGPARAMS_KEYS:
            pytest.skip("No static keys defined")
        static_key = next(iter(STATIC_REGPARAMS_KEYS))
        data = {"regParams": {static_key: 42, "customNewKey": 100}}
        result = _get_unmapped_keys(data, API_REG_PARAMS_URI)
        assert static_key not in result
        assert "customNewKey" in result

    def test_filters_out_null_values(self):
        data = {"regParams": {"keyA": None, "keyB": 42}}
        result = _get_unmapped_keys(data, API_REG_PARAMS_URI)
        assert "keyA" not in result
        assert "keyB" in result


# ============================================================================
# _get_unmapped_keys tests — regParamsData
# ============================================================================


class TestGetUnmappedKeysRegParamsData:
    """Test filtering of unmapped regParamsData IDs."""

    def test_returns_empty_for_none_data(self):
        assert _get_unmapped_keys(None, API_REG_PARAMS_DATA_URI) == {}

    def test_filters_out_static_ids(self):
        if not STATIC_REGPARAMS_DATA_IDS:
            pytest.skip("No static IDs defined")
        static_id = next(iter(STATIC_REGPARAMS_DATA_IDS))
        data = {
            "regParamsData": {static_id: 42, "99999": 100},
            "rmData": {},
        }
        result = _get_unmapped_keys(data, API_REG_PARAMS_DATA_URI)
        assert static_id not in result
        assert "99999" in result

    def test_filters_out_cdp_ids(self):
        """IDs already in rmData.currentDataParams should be excluded."""
        data = {
            "regParamsData": {"10": 42, "20": 100},
            "rmData": {"currentDataParams": {"10": {"name": "test"}}},
        }
        result = _get_unmapped_keys(data, API_REG_PARAMS_DATA_URI)
        assert "10" not in result
        assert "20" in result

    def test_filters_out_null_values(self):
        data = {
            "regParamsData": {"10": None, "20": 42},
            "rmData": {},
        }
        result = _get_unmapped_keys(data, API_REG_PARAMS_DATA_URI)
        assert "10" not in result
        assert "20" in result


# ============================================================================
# _get_unmapped_keys tests — rmCurrentDataParams
# ============================================================================


class TestGetUnmappedKeysRmCurrentData:
    """Test filtering of unmapped rmCurrentDataParams keys."""

    def test_returns_empty_for_none_data(self):
        assert _get_unmapped_keys(None, API_RM_CURRENT_DATA_PARAMS_URI) == {}

    def test_returns_empty_for_missing_rm_data(self):
        assert _get_unmapped_keys({"rmData": {}}, API_RM_CURRENT_DATA_PARAMS_URI) == {}

    def test_filters_out_static_ids(self):
        if not STATIC_REGPARAMS_DATA_IDS:
            pytest.skip("No static IDs defined")
        static_id = next(iter(STATIC_REGPARAMS_DATA_IDS))
        data = {
            "rmData": {
                "currentDataParams": {
                    static_id: {"name": "Static Param"},
                    "99999": {"name": "Dynamic Param"},
                }
            }
        }
        result = _get_unmapped_keys(data, API_RM_CURRENT_DATA_PARAMS_URI)
        assert static_id not in result
        assert "99999" in result

    def test_only_dict_values_included(self):
        data = {
            "rmData": {
                "currentDataParams": {
                    "10": {"name": "Good"},
                    "20": "not_a_dict",
                }
            }
        }
        result = _get_unmapped_keys(data, API_RM_CURRENT_DATA_PARAMS_URI)
        assert "10" in result
        assert "20" not in result


# ============================================================================
# _build_multiselect_options tests
# ============================================================================


class TestBuildMultiselectOptions:
    """Test building multi-select options for the UI."""

    def test_empty_input(self):
        assert _build_multiselect_options({}, API_REG_PARAMS_URI) == {}

    def test_regparams_options(self):
        unmapped = {"tempSomeKey": 42.5, "anotherKey": True}
        result = _build_multiselect_options(unmapped, API_REG_PARAMS_URI)
        assert "tempSomeKey" in result
        assert "42.5" in result["tempSomeKey"]

    def test_regparams_sorted_alphabetically(self):
        unmapped = {"zKey": 1, "aKey": 2, "mKey": 3}
        result = _build_multiselect_options(unmapped, API_REG_PARAMS_URI)
        keys = list(result.keys())
        assert keys == ["aKey", "mKey", "zKey"]

    def test_regparamsdata_sorted_by_numeric_id(self):
        unmapped = {"20": 1, "5": 2, "100": 3}
        result = _build_multiselect_options(unmapped, API_REG_PARAMS_DATA_URI)
        keys = list(result.keys())
        assert keys == ["5", "20", "100"]

    def test_regparamsdata_shows_type(self):
        unmapped = {"10": 42}
        result = _build_multiselect_options(unmapped, API_REG_PARAMS_DATA_URI)
        assert "int" in result["10"]
        assert "42" in result["10"]

    def test_rmcurrentdata_shows_name_and_unit(self):
        unmapped = {"10": {"name": "Temperature", "unit": 1}}
        result = _build_multiselect_options(unmapped, API_RM_CURRENT_DATA_PARAMS_URI)
        assert "Temperature" in result["10"]
        assert "°C" in result["10"]

    def test_rmcurrentdata_no_unit(self):
        unmapped = {"10": {"name": "Counter", "unit": 0}}
        result = _build_multiselect_options(unmapped, API_RM_CURRENT_DATA_PARAMS_URI)
        assert "Counter" in result["10"]


# ============================================================================
# CustomSensor factory tests
# ============================================================================


class TestCreateCustomSensors:
    """Test unified sensor factory for user-selected parameters."""

    def test_empty_config_returns_empty(self):
        coordinator = _make_coordinator(reg_params_data={"10": 42})
        api = _make_api()
        result = create_custom_sensors(coordinator, api, {})
        assert result == []

    def test_only_sensor_type_created(self):
        coordinator = _make_coordinator(reg_params_data={"10": 42})
        api = _make_api()
        config = {
            "regParamsData:10": {
                "source": "regParamsData",
                "key": "10",
                "name": "My Sensor",
                "entity_type": "sensor",
                "component": "boiler",
            },
            "regParamsData:20": {
                "source": "regParamsData",
                "key": "20",
                "name": "My Bool",
                "entity_type": "binary_sensor",
                "component": "boiler",
            },
        }
        result = create_custom_sensors(coordinator, api, config)
        assert len(result) == 1
        assert isinstance(result[0], CustomSensor)
        assert result[0].entity_description.name == "My Sensor"

    def test_lookup_value_regparams(self):
        coordinator = _make_coordinator(reg_params={"tempCustom": 55.5})
        api = _make_api()
        config = {
            "regParams:tempCustom": {
                "source": "regParams",
                "key": "tempCustom",
                "name": "Custom Temp",
                "entity_type": "sensor",
            }
        }
        entities = create_custom_sensors(coordinator, api, config)
        assert entities[0]._lookup_value() == 55.5  # noqa: SLF001

    def test_lookup_value_regparamsdata(self):
        coordinator = _make_coordinator(reg_params_data={"10": 42})
        api = _make_api()
        config = {
            "regParamsData:10": {
                "source": "regParamsData",
                "key": "10",
                "name": "Param 10",
                "entity_type": "sensor",
            }
        }
        entities = create_custom_sensors(coordinator, api, config)
        assert entities[0]._lookup_value() == 42  # noqa: SLF001

    def test_lookup_value_rmcurrentdata(self):
        """RmCurrentDataParams shares ID space with regParamsData."""
        coordinator = _make_coordinator(reg_params_data={"139": 7.3})
        api = _make_api()
        config = {
            "rmCurrentDataParams:139": {
                "source": "rmCurrentDataParams",
                "key": "139",
                "name": "Weather Temp",
                "entity_type": "sensor",
            }
        }
        entities = create_custom_sensors(coordinator, api, config)
        assert entities[0]._lookup_value() == 7.3  # noqa: SLF001

    def test_lookup_value_missing(self):
        coordinator = _make_coordinator(reg_params_data={"10": 42})
        api = _make_api()
        config = {
            "regParamsData:99": {
                "source": "regParamsData",
                "key": "99",
                "name": "Missing",
                "entity_type": "sensor",
            }
        }
        entities = create_custom_sensors(coordinator, api, config)
        assert entities[0]._lookup_value() is None  # noqa: SLF001

    def test_entity_category_diagnostic(self):
        coordinator = _make_coordinator(reg_params_data={"10": 42})
        api = _make_api()
        config = {
            "regParamsData:10": {
                "source": "regParamsData",
                "key": "10",
                "name": "Diag Param",
                "entity_type": "sensor",
                "entity_category": "diagnostic",
            }
        }
        entities = create_custom_sensors(coordinator, api, config)
        from homeassistant.const import EntityCategory

        assert (
            entities[0].entity_description.entity_category == EntityCategory.DIAGNOSTIC
        )

    def test_entity_category_none(self):
        coordinator = _make_coordinator(reg_params_data={"10": 42})
        api = _make_api()
        config = {
            "regParamsData:10": {
                "source": "regParamsData",
                "key": "10",
                "name": "Normal Param",
                "entity_type": "sensor",
                "entity_category": None,
            }
        }
        entities = create_custom_sensors(coordinator, api, config)
        assert entities[0].entity_description.entity_category is None

    def test_component_stored_in_description(self):
        coordinator = _make_coordinator(reg_params_data={"10": 42})
        api = _make_api()
        config = {
            "regParamsData:10": {
                "source": "regParamsData",
                "key": "10",
                "name": "Mixer Param",
                "entity_type": "sensor",
                "component": "mixer_1",
            }
        }
        entities = create_custom_sensors(coordinator, api, config)
        assert entities[0].entity_description.component == "mixer_1"


# ============================================================================
# CustomBinarySensor factory tests
# ============================================================================


class TestCreateCustomBinarySensors:
    """Test unified binary sensor factory for user-selected parameters."""

    def test_empty_config_returns_empty(self):
        coordinator = _make_coordinator(reg_params_data={"20": True})
        api = _make_api()
        result = create_custom_binary_sensors(coordinator, api, {})
        assert result == []

    def test_only_binary_sensor_type_created(self):
        coordinator = _make_coordinator(reg_params_data={"10": 42, "20": True})
        api = _make_api()
        config = {
            "regParamsData:10": {
                "source": "regParamsData",
                "key": "10",
                "name": "My Sensor",
                "entity_type": "sensor",
            },
            "regParamsData:20": {
                "source": "regParamsData",
                "key": "20",
                "name": "My Bool",
                "entity_type": "binary_sensor",
            },
        }
        result = create_custom_binary_sensors(coordinator, api, config)
        assert len(result) == 1
        assert isinstance(result[0], CustomBinarySensor)
        assert result[0].entity_description.name == "My Bool"

    def test_lookup_value_regparams(self):
        coordinator = _make_coordinator(reg_params={"customBool": True})
        api = _make_api()
        config = {
            "regParams:customBool": {
                "source": "regParams",
                "key": "customBool",
                "name": "Custom Bool",
                "entity_type": "binary_sensor",
            }
        }
        entities = create_custom_binary_sensors(coordinator, api, config)
        assert entities[0]._lookup_value() is True  # noqa: SLF001

    def test_lookup_value_regparamsdata(self):
        coordinator = _make_coordinator(reg_params_data={"20": False})
        api = _make_api()
        config = {
            "regParamsData:20": {
                "source": "regParamsData",
                "key": "20",
                "name": "Off Bool",
                "entity_type": "binary_sensor",
            }
        }
        entities = create_custom_binary_sensors(coordinator, api, config)
        assert entities[0]._lookup_value() is False  # noqa: SLF001

    def test_component_stored_in_description(self):
        coordinator = _make_coordinator(reg_params_data={"20": True})
        api = _make_api()
        config = {
            "regParamsData:20": {
                "source": "regParamsData",
                "key": "20",
                "name": "HUW Param",
                "entity_type": "binary_sensor",
                "component": "huw",
            }
        }
        entities = create_custom_binary_sensors(coordinator, api, config)
        assert entities[0].entity_description.component == "huw"


# ============================================================================
# Fixture-based tests for all devices
# ============================================================================


@pytest.fixture(
    params=[
        d.name
        for d in FIXTURES_ROOT.iterdir()
        if d.is_dir() and (d / "regParamsData.json").exists()
    ]
)
def device_name(request: pytest.FixtureRequest) -> str:
    """Parametrize over all device fixtures that have regParamsData."""
    return request.param


class TestUnmappedKeysWithFixtures:
    """Test _get_unmapped_keys with real fixture data for all devices."""

    def test_regparamsdata_unmapped_is_subset(self, device_name):
        rpd_raw = _load_fixture(device_name, "regParamsData.json")
        rpd = rpd_raw.get("data", rpd_raw)
        if not isinstance(rpd, dict):
            pytest.skip(f"{device_name}: regParamsData not a dict")

        data = {"regParamsData": rpd, "rmData": {}}
        unmapped = _get_unmapped_keys(data, API_REG_PARAMS_DATA_URI)

        for pid in unmapped:
            assert pid in rpd, f"Unmapped ID {pid} not in regParamsData"

    def test_no_static_ids_in_regparamsdata_unmapped(self, device_name):
        rpd_raw = _load_fixture(device_name, "regParamsData.json")
        rpd = rpd_raw.get("data", rpd_raw)
        if not isinstance(rpd, dict):
            pytest.skip(f"{device_name}: regParamsData not a dict")

        data = {"regParamsData": rpd, "rmData": {}}
        unmapped = _get_unmapped_keys(data, API_REG_PARAMS_DATA_URI)

        for pid in unmapped:
            assert pid not in STATIC_REGPARAMS_DATA_IDS, (
                f"Static ID {pid} found in unmapped for {device_name}"
            )

    def test_no_null_values_in_regparamsdata_unmapped(self, device_name):
        rpd_raw = _load_fixture(device_name, "regParamsData.json")
        rpd = rpd_raw.get("data", rpd_raw)
        if not isinstance(rpd, dict):
            pytest.skip(f"{device_name}: regParamsData not a dict")

        data = {"regParamsData": rpd, "rmData": {}}
        unmapped = _get_unmapped_keys(data, API_REG_PARAMS_DATA_URI)

        for pid, value in unmapped.items():
            assert value is not None, (
                f"Null value for ID {pid} in unmapped for {device_name}"
            )
