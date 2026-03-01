"""Tests for Custom Entity Selector (Options Flow + custom entity factories).

Covers:
- Helper functions (_classify_regparam_value, _get_unmapped_regparams, _build_multiselect_options)
- CustomRegParamSensor factory
- CustomRegParamBinarySensor factory
- Options flow steps (menu, connection_settings, custom_entities, select_params, name_entities)
"""

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from custom_components.econet300.binary_sensor import (
    CustomRegParamBinarySensor,
    create_custom_regparam_binary_sensors,
)
from custom_components.econet300.config_flow import (
    _build_multiselect_options,
    _classify_regparam_value,
    _get_unmapped_regparams,
)
from custom_components.econet300.const import (
    CUSTOM_ENTITY_TYPE_BINARY_SENSOR,
    CUSTOM_ENTITY_TYPE_SENSOR,
    STATIC_REGPARAMS_DATA_IDS,
)
from custom_components.econet300.sensor import (
    CustomRegParamSensor,
    create_custom_regparam_sensors,
)

FIXTURES_ROOT = Path(__file__).parent / "fixtures"


def _load_fixture(device: str, filename: str) -> dict:
    """Load a JSON fixture file for a device."""
    path = FIXTURES_ROOT / device / filename
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as f:
        return json.load(f)


# ============================================================================
# _classify_regparam_value tests
# ============================================================================


class TestClassifyRegparamValue:
    """Test value type classification for custom entities."""

    def test_bool_true_is_binary_sensor(self):
        assert _classify_regparam_value(True) == CUSTOM_ENTITY_TYPE_BINARY_SENSOR

    def test_bool_false_is_binary_sensor(self):
        assert _classify_regparam_value(False) == CUSTOM_ENTITY_TYPE_BINARY_SENSOR

    def test_int_is_sensor(self):
        assert _classify_regparam_value(42) == CUSTOM_ENTITY_TYPE_SENSOR

    def test_float_is_sensor(self):
        assert _classify_regparam_value(3.14) == CUSTOM_ENTITY_TYPE_SENSOR

    def test_string_is_sensor(self):
        assert _classify_regparam_value("some_text") == CUSTOM_ENTITY_TYPE_SENSOR

    def test_zero_is_sensor(self):
        """Zero is an int, not a bool -- should be sensor."""
        assert _classify_regparam_value(0) == CUSTOM_ENTITY_TYPE_SENSOR


# ============================================================================
# _get_unmapped_regparams tests
# ============================================================================


class TestGetUnmappedRegparams:
    """Test filtering of unmapped regParamsData IDs."""

    def test_returns_empty_for_none_data(self):
        assert _get_unmapped_regparams(None) == {}

    def test_returns_empty_for_missing_regparams_data(self):
        assert _get_unmapped_regparams({"regParams": {}}) == {}

    def test_filters_out_static_ids(self):
        """IDs in STATIC_REGPARAMS_DATA_IDS should be excluded."""
        if not STATIC_REGPARAMS_DATA_IDS:
            pytest.skip("No static IDs defined")
        static_id = next(iter(STATIC_REGPARAMS_DATA_IDS))
        data = {
            "regParamsData": {static_id: 42, "99999": 100},
            "currentDataMerged": {},
        }
        result = _get_unmapped_regparams(data)
        assert static_id not in result
        assert "99999" in result

    def test_filters_out_cdm_ids(self):
        """IDs already in currentDataMerged should be excluded."""
        data = {
            "regParamsData": {"10": 42, "20": 100},
            "currentDataMerged": {"10": {"name": "test", "value": 42}},
        }
        result = _get_unmapped_regparams(data)
        assert "10" not in result
        assert "20" in result

    def test_filters_out_null_values(self):
        """IDs with None values should be excluded."""
        data = {
            "regParamsData": {"10": None, "20": 42},
            "currentDataMerged": {},
        }
        result = _get_unmapped_regparams(data)
        assert "10" not in result
        assert "20" in result

    def test_returns_all_unmapped_with_values(self):
        """All non-null, non-static, non-CDM IDs should be returned."""
        data = {
            "regParamsData": {"10": 42, "20": True, "30": "text"},
            "currentDataMerged": {},
        }
        result = _get_unmapped_regparams(data)
        assert len(result) == 3
        assert result["10"] == 42
        assert result["20"] is True
        assert result["30"] == "text"

    def test_with_real_fixture(self):
        """Test with actual ecoMAX810P-L fixture data."""
        rpd = _load_fixture("ecoMAX810P-L", "regParamsData.json")
        if not rpd:
            pytest.skip("No ecoMAX810P-L regParamsData fixture")

        cdm_fixture = _load_fixture("ecoMAX810P-L", "currentDataMerged.json")
        cdm = cdm_fixture if cdm_fixture else {}

        data = {
            "regParamsData": rpd.get("data", rpd),
            "currentDataMerged": cdm,
        }
        result = _get_unmapped_regparams(data)

        # Should have some unmapped IDs
        assert isinstance(result, dict)
        # None of the returned IDs should be in static or CDM sets
        for pid in result:
            assert pid not in STATIC_REGPARAMS_DATA_IDS
            assert pid not in cdm


# ============================================================================
# _build_multiselect_options tests
# ============================================================================


class TestBuildMultiselectOptions:
    """Test building multi-select options for the UI."""

    def test_empty_input(self):
        assert _build_multiselect_options({}) == {}

    def test_basic_options(self):
        unmapped = {"10": 42, "20": True}
        result = _build_multiselect_options(unmapped)
        assert "10" in result
        assert "20" in result
        assert "42" in result["10"]
        assert "int" in result["10"]

    def test_sorted_by_numeric_id(self):
        unmapped = {"20": 1, "5": 2, "100": 3}
        result = _build_multiselect_options(unmapped)
        keys = list(result.keys())
        assert keys == ["5", "20", "100"]

    def test_type_filter_sensor(self):
        unmapped = {"10": 42, "20": True}
        result = _build_multiselect_options(unmapped, CUSTOM_ENTITY_TYPE_SENSOR)
        assert "10" in result
        assert "20" not in result

    def test_type_filter_binary_sensor(self):
        unmapped = {"10": 42, "20": True}
        result = _build_multiselect_options(unmapped, CUSTOM_ENTITY_TYPE_BINARY_SENSOR)
        assert "10" not in result
        assert "20" in result

    def test_long_value_truncated(self):
        unmapped = {"1": "a" * 50}
        result = _build_multiselect_options(unmapped)
        assert "..." in result["1"]


# ============================================================================
# CustomRegParamSensor factory tests
# ============================================================================


class TestCreateCustomRegparamSensors:
    """Test sensor factory for user-selected regParamsData IDs."""

    def _make_coordinator(self, reg_params_data: dict) -> MagicMock:
        coordinator = MagicMock()
        coordinator.data = {"regParamsData": reg_params_data}
        return coordinator

    def _make_api(self) -> MagicMock:
        api = MagicMock()
        api.uid = "test-uid"
        api.model_id = "ecoMAX810P-L"
        api.host = "http://test"
        api.sw_rev = "1.0"
        return api

    def test_empty_config_returns_empty(self):
        coordinator = self._make_coordinator({"10": 42})
        api = self._make_api()
        result = create_custom_regparam_sensors(coordinator, api, {})
        assert result == []

    def test_only_sensor_type_created(self):
        coordinator = self._make_coordinator({"10": 42, "20": True})
        api = self._make_api()
        config = {
            "10": {"name": "My Sensor", "entity_type": "sensor"},
            "20": {"name": "My Switch", "entity_type": "binary_sensor"},
        }
        result = create_custom_regparam_sensors(coordinator, api, config)
        assert len(result) == 1
        assert isinstance(result[0], CustomRegParamSensor)
        assert result[0].entity_description.key == "custom_10"
        assert result[0].entity_description.name == "My Sensor"

    def test_default_name_used(self):
        coordinator = self._make_coordinator({"10": 42})
        api = self._make_api()
        config = {"10": {"entity_type": "sensor"}}
        result = create_custom_regparam_sensors(coordinator, api, config)
        assert len(result) == 1
        assert result[0].entity_description.name == "Parameter 10"

    def test_lookup_value(self):
        coordinator = self._make_coordinator({"10": 42})
        api = self._make_api()
        config = {"10": {"name": "Test", "entity_type": "sensor"}}
        entities = create_custom_regparam_sensors(coordinator, api, config)
        sensor = entities[0]
        assert sensor._lookup_value() == 42

    def test_lookup_value_missing_id(self):
        coordinator = self._make_coordinator({"10": 42})
        api = self._make_api()
        config = {"99": {"name": "Missing", "entity_type": "sensor"}}
        entities = create_custom_regparam_sensors(coordinator, api, config)
        sensor = entities[0]
        assert sensor._lookup_value() is None


# ============================================================================
# CustomRegParamBinarySensor factory tests
# ============================================================================


class TestCreateCustomRegparamBinarySensors:
    """Test binary sensor factory for user-selected regParamsData IDs."""

    def _make_coordinator(self, reg_params_data: dict) -> MagicMock:
        coordinator = MagicMock()
        coordinator.data = {"regParamsData": reg_params_data}
        return coordinator

    def _make_api(self) -> MagicMock:
        api = MagicMock()
        api.uid = "test-uid"
        api.model_id = "ecoMAX810P-L"
        api.host = "http://test"
        api.sw_rev = "1.0"
        return api

    def test_empty_config_returns_empty(self):
        coordinator = self._make_coordinator({"20": True})
        api = self._make_api()
        result = create_custom_regparam_binary_sensors(coordinator, api, {})
        assert result == []

    def test_only_binary_sensor_type_created(self):
        coordinator = self._make_coordinator({"10": 42, "20": True})
        api = self._make_api()
        config = {
            "10": {"name": "My Sensor", "entity_type": "sensor"},
            "20": {"name": "My Bool", "entity_type": "binary_sensor"},
        }
        result = create_custom_regparam_binary_sensors(coordinator, api, config)
        assert len(result) == 1
        assert isinstance(result[0], CustomRegParamBinarySensor)
        assert result[0].entity_description.key == "custom_20"
        assert result[0].entity_description.name == "My Bool"

    def test_lookup_value(self):
        coordinator = self._make_coordinator({"20": True})
        api = self._make_api()
        config = {"20": {"name": "Test Bool", "entity_type": "binary_sensor"}}
        entities = create_custom_regparam_binary_sensors(coordinator, api, config)
        sensor = entities[0]
        assert sensor._lookup_value() is True

    def test_lookup_value_false(self):
        coordinator = self._make_coordinator({"20": False})
        api = self._make_api()
        config = {"20": {"name": "Off Bool", "entity_type": "binary_sensor"}}
        entities = create_custom_regparam_binary_sensors(coordinator, api, config)
        sensor = entities[0]
        assert sensor._lookup_value() is False


# ============================================================================
# Options flow helper tests with real fixture data
# ============================================================================


@pytest.fixture(
    params=[
        d.name
        for d in FIXTURES_ROOT.iterdir()
        if d.is_dir() and (d / "regParamsData.json").exists()
    ]
)
def device_name(request):
    """Parametrize over all device fixtures that have regParamsData."""
    return request.param


class TestUnmappedRegparamsWithFixtures:
    """Test _get_unmapped_regparams with real fixture data for all devices."""

    def test_unmapped_is_subset_of_regparams_data(self, device_name):
        rpd_raw = _load_fixture(device_name, "regParamsData.json")
        rpd = rpd_raw.get("data", rpd_raw)
        if not isinstance(rpd, dict):
            pytest.skip(f"{device_name}: regParamsData not a dict")

        cdm = _load_fixture(device_name, "currentDataMerged.json") or {}

        data = {
            "regParamsData": rpd,
            "currentDataMerged": cdm,
        }
        unmapped = _get_unmapped_regparams(data)

        for pid in unmapped:
            assert pid in rpd, f"Unmapped ID {pid} not in regParamsData"

    def test_no_static_ids_in_unmapped(self, device_name):
        rpd_raw = _load_fixture(device_name, "regParamsData.json")
        rpd = rpd_raw.get("data", rpd_raw)
        if not isinstance(rpd, dict):
            pytest.skip(f"{device_name}: regParamsData not a dict")

        data = {
            "regParamsData": rpd,
            "currentDataMerged": {},
        }
        unmapped = _get_unmapped_regparams(data)

        for pid in unmapped:
            assert pid not in STATIC_REGPARAMS_DATA_IDS, (
                f"Static ID {pid} found in unmapped for {device_name}"
            )

    def test_no_null_values_in_unmapped(self, device_name):
        rpd_raw = _load_fixture(device_name, "regParamsData.json")
        rpd = rpd_raw.get("data", rpd_raw)
        if not isinstance(rpd, dict):
            pytest.skip(f"{device_name}: regParamsData not a dict")

        data = {
            "regParamsData": rpd,
            "currentDataMerged": {},
        }
        unmapped = _get_unmapped_regparams(data)

        for pid, value in unmapped.items():
            assert value is not None, (
                f"Null value for ID {pid} in unmapped for {device_name}"
            )
