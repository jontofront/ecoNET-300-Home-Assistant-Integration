"""Tests for Unified Custom Entity Selector (Options Flow + custom entity factories).

Covers:
- Helper functions (_get_unmapped_keys, _build_multiselect_options)
- CustomSensor factory and _lookup_value for all sources
- CustomBinarySensor factory and _lookup_value for all sources
- Device grouping via component in entity descriptions
- Backwards compatibility with legacy rmCurrentDataParams source
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
    STATIC_CDP_IDS,
    STATIC_REGPARAMS_DATA_IDS,
    STATIC_REGPARAMS_KEYS,
)
from custom_components.econet300.sensor import (
    CustomSensor,
    create_custom_sensors,
)
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import UnitOfTemperature

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
    params_edits: dict[str, Any] | None = None,
    merged_data: dict[str, Any] | None = None,
) -> MagicMock:
    """Create a mock coordinator with the given data."""
    coordinator = MagicMock()
    coordinator.data = {
        "regParams": reg_params or {},
        "regParamsData": reg_params_data or {},
        "rmData": rm_data or {},
        "paramsEdits": params_edits or {},
        "mergedData": merged_data,
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
# _get_unmapped_keys tests — regParamsData (merged with rmCurrentDataParams)
# ============================================================================


class TestGetUnmappedKeysRegParamsData:
    """Test filtering of merged regParamsData + rmCurrentDataParams IDs."""

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

    def test_merges_cdp_metadata_with_rpd_values(self):
        """IDs present in both rpd and cdp should be merged with metadata."""
        data = {
            "regParamsData": {"10": 42, "20": 100},
            "rmData": {"currentDataParams": {"10": {"name": "Temperature"}}},
        }
        result = _get_unmapped_keys(data, API_REG_PARAMS_DATA_URI)
        assert "10" in result
        assert "20" in result
        assert isinstance(result["10"], dict)
        assert result["10"]["name"] == "Temperature"
        assert result["10"]["_rpd_value"] == 42

    def test_cdp_only_ids_included(self):
        """IDs present only in cdp (not in rpd) should be included."""
        data = {
            "regParamsData": {},
            "rmData": {"currentDataParams": {"50": {"name": "CDP only"}}},
        }
        result = _get_unmapped_keys(data, API_REG_PARAMS_DATA_URI)
        assert "50" in result
        assert result["50"]["name"] == "CDP only"

    def test_rpd_only_ids_included(self):
        """IDs present only in rpd (no cdp metadata) should be included."""
        data = {
            "regParamsData": {"77": 99},
            "rmData": {},
        }
        result = _get_unmapped_keys(data, API_REG_PARAMS_DATA_URI)
        assert "77" in result
        assert result["77"] == 99

    def test_filters_out_static_cdp_ids(self):
        """IDs in STATIC_CDP_IDS should be excluded."""
        if not STATIC_CDP_IDS:
            pytest.skip("No static CDP IDs defined")
        static_id = next(iter(STATIC_CDP_IDS))
        data = {
            "regParamsData": {},
            "rmData": {
                "currentDataParams": {
                    static_id: {"name": "Static"},
                    "99999": {"name": "Dynamic"},
                }
            },
        }
        result = _get_unmapped_keys(data, API_REG_PARAMS_DATA_URI)
        assert static_id not in result
        assert "99999" in result

    def test_filters_null_rpd_without_cdp_metadata(self):
        """rpd-only entries with None value and no cdp metadata are excluded."""
        data = {
            "regParamsData": {"10": None, "20": 42},
            "rmData": {},
        }
        result = _get_unmapped_keys(data, API_REG_PARAMS_DATA_URI)
        assert "10" not in result
        assert "20" in result


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

    def test_regparamsdata_plain_value_shows_type(self):
        """Plain rpd entries (no cdp metadata) show value and type."""
        unmapped = {"10": 42}
        result = _build_multiselect_options(unmapped, API_REG_PARAMS_DATA_URI)
        assert "int" in result["10"]
        assert "42" in result["10"]

    def test_regparamsdata_with_metadata_shows_name(self):
        """Merged entries with cdp metadata show friendly name."""
        unmapped = {"10": {"name": "Temperature", "unit": 1, "_rpd_value": 42}}
        result = _build_multiselect_options(unmapped, API_REG_PARAMS_DATA_URI)
        assert "Temperature" in result["10"]
        assert "°C" in result["10"]
        assert "42" in result["10"]

    def test_regparamsdata_metadata_no_unit(self):
        """Merged entries without unit omit the unit part."""
        unmapped = {"10": {"name": "Counter", "unit": 0, "_rpd_value": None}}
        result = _build_multiselect_options(unmapped, API_REG_PARAMS_DATA_URI)
        assert "Counter" in result["10"]

    def test_regparamsdata_metadata_no_rpd_value(self):
        """Merged entries without rpd value still show the name."""
        unmapped = {"10": {"name": "CDP Only Param", "unit": 0, "_rpd_value": None}}
        result = _build_multiselect_options(unmapped, API_REG_PARAMS_DATA_URI)
        assert "CDP Only Param" in result["10"]


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
        """Value from regParamsData source resolves via the fallback chain."""
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

    def test_lookup_value_cdp_via_id_mapping(self):
        """CDP lookup resolves via CDP_ID_TO_REGPARAMS mapping to regParams."""
        coordinator = _make_coordinator(
            reg_params={"tempCO": 82.5},
            rm_data={"currentDataParams": {"1024": {"name": "Boiler temperature"}}},
        )
        api = _make_api()
        config = {
            "rmCurrentDataParams:1024": {
                "source": "rmCurrentDataParams",
                "key": "1024",
                "name": "Boiler temperature",
                "entity_type": "sensor",
            }
        }
        entities = create_custom_sensors(coordinator, api, config)
        assert entities[0]._lookup_value() == 82.5  # noqa: SLF001

    def test_lookup_value_cdp_via_name_heuristic(self):
        """CDP lookup falls back to name-to-camelCase heuristic for unmapped IDs."""
        coordinator = _make_coordinator(
            reg_params={"valveMixer1": 45.0},
            rm_data={"currentDataParams": {"139": {"name": "Valve mixer 1"}}},
        )
        api = _make_api()
        config = {
            "rmCurrentDataParams:139": {
                "source": "rmCurrentDataParams",
                "key": "139",
                "name": "Valve mixer 1",
                "entity_type": "sensor",
            }
        }
        entities = create_custom_sensors(coordinator, api, config)
        assert entities[0]._lookup_value() == 45.0  # noqa: SLF001

    def test_lookup_value_via_regparamsdata_direct(self):
        """Fallback step 3: value resolved from regParamsData by numeric ID."""
        coordinator = _make_coordinator(
            reg_params_data={"139": 59},
            rm_data={"currentDataParams": {"139": {"name": "Valve mixer 1"}}},
        )
        api = _make_api()
        config = {
            "regParamsData:139": {
                "source": "regParamsData",
                "key": "139",
                "name": "Valve mixer 1",
                "entity_type": "sensor",
            }
        }
        entities = create_custom_sensors(coordinator, api, config)
        assert entities[0]._lookup_value() == 59  # noqa: SLF001

    def test_lookup_value_cdp_via_params_edits(self):
        """CDP lookup falls back to paramsEdits when regParams has no match."""
        coordinator = _make_coordinator(
            rm_data={"currentDataParams": {"9999": {"name": "Unknown param"}}},
            params_edits={"9999": {"value": 12.3, "min": 0, "max": 100}},
        )
        api = _make_api()
        config = {
            "rmCurrentDataParams:9999": {
                "source": "rmCurrentDataParams",
                "key": "9999",
                "name": "Unknown param",
                "entity_type": "sensor",
            }
        }
        entities = create_custom_sensors(coordinator, api, config)
        assert entities[0]._lookup_value() == 12.3  # noqa: SLF001

    def test_lookup_value_cdp_via_merged_data_name(self):
        """CDP lookup falls back to mergedData name search when other sources fail."""
        coordinator = _make_coordinator(
            rm_data={"currentDataParams": {"9999": {"name": "Alarm level"}}},
            merged_data={
                "parameters": {
                    "139": {"name": "Alarm level", "value": 10},
                    "140": {"name": "Other param", "value": 99},
                }
            },
        )
        api = _make_api()
        config = {
            "rmCurrentDataParams:9999": {
                "source": "rmCurrentDataParams",
                "key": "9999",
                "name": "Alarm level",
                "entity_type": "sensor",
            }
        }
        entities = create_custom_sensors(coordinator, api, config)
        assert entities[0]._lookup_value() == 10  # noqa: SLF001

    def test_lookup_value_cdp_returns_none_when_unavailable(self):
        """CDP lookup returns None when no source has the value."""
        coordinator = _make_coordinator(
            rm_data={"currentDataParams": {"9999": {"name": "Unknown param"}}},
            merged_data={"parameters": {"0": {"name": "Other", "value": 5}}},
        )
        api = _make_api()
        config = {
            "rmCurrentDataParams:9999": {
                "source": "rmCurrentDataParams",
                "key": "9999",
                "name": "Unknown param",
                "entity_type": "sensor",
            }
        }
        entities = create_custom_sensors(coordinator, api, config)
        assert entities[0]._lookup_value() is None  # noqa: SLF001

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

    def test_native_unit_applied(self):
        """Sensor with native_unit set should have native_unit_of_measurement."""
        coordinator = _make_coordinator(reg_params={"tempCustom": 55.5})
        api = _make_api()
        config = {
            "regParams:tempCustom": {
                "source": "regParams",
                "key": "tempCustom",
                "name": "Custom Temp",
                "entity_type": "sensor",
                "native_unit": "°C",
            }
        }
        entities = create_custom_sensors(coordinator, api, config)
        assert (
            entities[0].entity_description.native_unit_of_measurement
            == UnitOfTemperature.CELSIUS
        )

    def test_device_class_applied(self):
        """Sensor with device_class set should have correct device_class."""
        coordinator = _make_coordinator(reg_params={"tempCustom": 55.5})
        api = _make_api()
        config = {
            "regParams:tempCustom": {
                "source": "regParams",
                "key": "tempCustom",
                "name": "Custom Temp",
                "entity_type": "sensor",
                "device_class": "temperature",
            }
        }
        entities = create_custom_sensors(coordinator, api, config)
        assert (
            entities[0].entity_description.device_class == SensorDeviceClass.TEMPERATURE
        )

    def test_precision_applied(self):
        """Sensor with precision set should have suggested_display_precision."""
        coordinator = _make_coordinator(reg_params={"tempCustom": 55.5})
        api = _make_api()
        config = {
            "regParams:tempCustom": {
                "source": "regParams",
                "key": "tempCustom",
                "name": "Custom Temp",
                "entity_type": "sensor",
                "precision": 1,
            }
        }
        entities = create_custom_sensors(coordinator, api, config)
        assert entities[0].entity_description.suggested_display_precision == 1

    def test_all_sensor_properties_applied(self):
        """Sensor with all three properties set."""
        coordinator = _make_coordinator(reg_params={"tempCustom": 55.5})
        api = _make_api()
        config = {
            "regParams:tempCustom": {
                "source": "regParams",
                "key": "tempCustom",
                "name": "Custom Temp",
                "entity_type": "sensor",
                "native_unit": "°C",
                "device_class": "temperature",
                "precision": 2,
            }
        }
        entities = create_custom_sensors(coordinator, api, config)
        desc = entities[0].entity_description
        assert desc.native_unit_of_measurement == UnitOfTemperature.CELSIUS
        assert desc.device_class == SensorDeviceClass.TEMPERATURE
        assert desc.suggested_display_precision == 2

    def test_none_sensor_properties_default(self):
        """Sensor without sensor-specific properties should have None defaults."""
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
        desc = entities[0].entity_description
        assert desc.native_unit_of_measurement is None
        assert desc.device_class is None
        assert desc.suggested_display_precision is None


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

    def test_lookup_value_binary_cdp_fallback(self):
        """Binary sensor with rmCurrentDataParams source falls back to rpd."""
        coordinator = _make_coordinator(
            reg_params_data={"20": True},
            rm_data={"currentDataParams": {"20": {"name": "Pump"}}},
        )
        api = _make_api()
        config = {
            "rmCurrentDataParams:20": {
                "source": "rmCurrentDataParams",
                "key": "20",
                "name": "Pump",
                "entity_type": "binary_sensor",
            }
        }
        entities = create_custom_binary_sensors(coordinator, api, config)
        assert entities[0]._lookup_value() is True  # noqa: SLF001

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
