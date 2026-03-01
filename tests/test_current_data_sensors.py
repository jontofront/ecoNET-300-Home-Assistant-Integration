"""Tests for dynamic CurrentData sensor and binary sensor creation.

Tests are parametrized across all device fixtures that have valid
rmCurrentDataParams.json and regParamsData.json files.
"""

import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from custom_components.econet300.common_functions import (
    build_current_data_entity_key,
    classify_current_data_param,
    is_regparams_data_id_mapped,
)
from custom_components.econet300.const import (
    CDP_SPECIAL_SKIP,
    STATIC_REGPARAMS_DATA_IDS,
    UNIT_INDEX_TO_NAME,
)

FIXTURES_ROOT = Path(__file__).parent / "fixtures"


def _load_json(path: Path) -> dict:
    """Load a JSON fixture file."""
    with path.open() as f:
        return json.load(f)


def _has_valid_cdp(device_dir: Path) -> bool:
    """Check if device fixture has valid rmCurrentDataParams + regParamsData."""
    cdp_path = device_dir / "rmCurrentDataParams.json"
    rpd_path = device_dir / "regParamsData.json"

    if not cdp_path.exists() or not rpd_path.exists():
        return False

    cdp = _load_json(cdp_path)
    rpd = _load_json(rpd_path)

    # Must have "data" dict (not an error response)
    return isinstance(cdp.get("data"), dict) and isinstance(rpd.get("data"), dict)


def _build_merged(device_dir: Path) -> dict:
    """Build a currentDataMerged dict from a device fixture directory."""
    cdp_data = _load_json(device_dir / "rmCurrentDataParams.json").get("data", {})
    rpd_data = _load_json(device_dir / "regParamsData.json").get("data", {})

    merged: dict[str, dict] = {}
    for param_id, metadata in cdp_data.items():
        if not isinstance(metadata, dict):
            continue
        merged[param_id] = {
            "name": metadata.get("name", ""),
            "unit": metadata.get("unit", 0),
            "special": metadata.get("special", 0),
            "value": rpd_data.get(param_id),
        }
    return merged


# Discover all device fixtures that support CDP dynamic entities
CDP_DEVICES: list[str] = sorted(
    d.name
    for d in FIXTURES_ROOT.iterdir()
    if d.is_dir() and _has_valid_cdp(d)
)


def _make_coordinator(current_data_merged: dict) -> MagicMock:
    """Build a mock coordinator with currentDataMerged data."""
    coordinator = MagicMock()
    coordinator.data = {"currentDataMerged": current_data_merged}
    return coordinator


# =============================================================================
# Tests for classify_current_data_param() — unit tests (no fixture needed)
# =============================================================================


class TestClassifyCurrentDataParam:
    """Tests for classify_current_data_param function."""

    def test_sensor_numeric_with_unit(self):
        """Numeric value with unit index 5 (%) → sensor."""
        param = {"name": "Valve mixer 1", "unit": 5, "special": 0, "value": 59}
        assert classify_current_data_param(param) == "sensor"

    def test_sensor_temperature(self):
        """Numeric value with unit index 1 (°C) → sensor."""
        param = {
            "name": "Feeder temperature",
            "unit": 1,
            "special": 1,
            "value": 24.0,
        }
        assert classify_current_data_param(param) == "sensor"

    def test_binary_sensor_boolean_unit31(self):
        """Boolean value with unit 31 → binary_sensor."""
        param = {"name": "Lighter", "unit": 31, "special": 1, "value": False}
        assert classify_current_data_param(param) == "binary_sensor"

    def test_binary_sensor_int_unit31(self):
        """Integer 0/1 value with unit 31 → binary_sensor."""
        param = {"name": "Unseal", "unit": 31, "special": 1, "value": 1}
        assert classify_current_data_param(param) == "binary_sensor"

    def test_skip_null_value(self):
        """None value → skip."""
        param = {"name": "Some param", "unit": 1, "special": 0, "value": None}
        assert classify_current_data_param(param) == "skip"

    def test_skip_empty_name(self):
        """Empty name → skip."""
        param = {"name": "", "unit": 1, "special": 0, "value": 42}
        assert classify_current_data_param(param) == "skip"

    def test_skip_whitespace_name(self):
        """Whitespace-only name → skip."""
        param = {"name": "   ", "unit": 1, "special": 0, "value": 42}
        assert classify_current_data_param(param) == "skip"

    def test_skip_special_7(self):
        """special=7 → skip (mode-like entries)."""
        param = {"name": "Some mode", "unit": 0, "special": 7, "value": 2}
        assert classify_current_data_param(param) == "skip"

    def test_skip_string_value(self):
        """String value → skip."""
        param = {"name": "Version", "unit": 0, "special": 0, "value": "1.2.3"}
        assert classify_current_data_param(param) == "skip"

    def test_sensor_zero_value(self):
        """Zero numeric value should still be a sensor (not skipped)."""
        param = {"name": "Fan power", "unit": 5, "special": 0, "value": 0}
        assert classify_current_data_param(param) == "sensor"

    def test_sensor_hours_unit(self):
        """Unit index 4 (hours) → sensor."""
        param = {"name": "Work at 100%", "unit": 4, "special": 0, "value": 1234}
        assert classify_current_data_param(param) == "sensor"


# =============================================================================
# Tests for is_regparams_data_id_mapped()
# =============================================================================


class TestIsRegparamsDataIdMapped:
    """Tests for is_regparams_data_id_mapped function."""

    def test_number_map_id_is_mapped(self):
        """IDs from NUMBER_MAP should be reported as mapped."""
        assert is_regparams_data_id_mapped("1280") is True
        assert is_regparams_data_id_mapped("1281") is True

    def test_select_post_index_is_mapped(self):
        """IDs from SELECT_KEY_POST_INDEX values should be mapped."""
        assert is_regparams_data_id_mapped("55") is True

    def test_select_get_index_is_mapped(self):
        """IDs from SELECT_KEY_GET_INDEX values should be mapped."""
        assert is_regparams_data_id_mapped("2049") is True

    def test_unknown_id_not_mapped(self):
        """Unknown IDs should not be mapped."""
        assert is_regparams_data_id_mapped("139") is False
        assert is_regparams_data_id_mapped("99999") is False

    def test_static_set_not_empty(self):
        """STATIC_REGPARAMS_DATA_IDS should contain entries."""
        assert len(STATIC_REGPARAMS_DATA_IDS) > 0


# =============================================================================
# Tests for build_current_data_entity_key()
# =============================================================================


class TestBuildCurrentDataEntityKey:
    """Tests for build_current_data_entity_key function."""

    def test_basic_key(self):
        """Basic name produces expected key."""
        key = build_current_data_entity_key("139", "Valve mixer 1")
        assert key == "cdp_139_valve_mixer_1"

    def test_special_characters(self):
        """Special characters are replaced."""
        key = build_current_data_entity_key("155", "Work at 100%")
        assert key == "cdp_155_work_at_100"

    def test_unicode_chars(self):
        """Non-ASCII chars should be stripped."""
        key = build_current_data_entity_key("26", "Feeder temperature")
        assert key == "cdp_26_feeder_temperature"

    def test_leading_trailing_spaces(self):
        """Leading/trailing spaces are stripped."""
        key = build_current_data_entity_key("1", " Lighter ")
        assert key == "cdp_1_lighter"


# =============================================================================
# Tests for UNIT_INDEX_TO_NAME mapping
# =============================================================================


class TestUnitIndexToName:
    """Tests for UNIT_INDEX_TO_NAME constant."""

    def test_temperature_unit(self):
        """Unit index 1 maps to °C."""
        assert UNIT_INDEX_TO_NAME[1] == "°C"

    def test_percentage_unit(self):
        """Unit index 5 maps to %."""
        assert UNIT_INDEX_TO_NAME[5] == "%"

    def test_power_unit(self):
        """Unit index 7 maps to kW."""
        assert UNIT_INDEX_TO_NAME[7] == "kW"

    def test_boolean_unit(self):
        """Unit index 31 maps to empty string (state indicator)."""
        assert UNIT_INDEX_TO_NAME[31] == ""

    def test_hours_unit(self):
        """Unit index 4 maps to h."""
        assert UNIT_INDEX_TO_NAME[4] == "h."


# =============================================================================
# Tests for CDP_SPECIAL_SKIP
# =============================================================================


class TestCdpSpecialSkip:
    """Tests for CDP_SPECIAL_SKIP constant."""

    def test_special_7_is_skipped(self):
        """special=7 should be in the skip set."""
        assert 7 in CDP_SPECIAL_SKIP

    def test_special_0_not_skipped(self):
        """special=0 should not be skipped."""
        assert 0 not in CDP_SPECIAL_SKIP

    def test_special_1_not_skipped(self):
        """special=1 should not be skipped."""
        assert 1 not in CDP_SPECIAL_SKIP


# =============================================================================
# Multi-device parametrized tests — merged data integrity
# =============================================================================


class TestCurrentDataMergedMultiDevice:
    """Integration tests parametrized across all devices with valid CDP fixtures."""

    @pytest.mark.parametrize("device", CDP_DEVICES)
    def test_merged_not_empty(self, device):
        """Merged dict should contain parameters for each device."""
        merged = _build_merged(FIXTURES_ROOT / device)
        assert len(merged) > 0, f"{device}: currentDataMerged is empty"

    @pytest.mark.parametrize("device", CDP_DEVICES)
    def test_all_params_have_required_keys(self, device):
        """Every merged param should have name, unit, special, value keys."""
        merged = _build_merged(FIXTURES_ROOT / device)
        for param_id, param in merged.items():
            for required in ("name", "unit", "special", "value"):
                assert required in param, (
                    f"{device} param {param_id}: missing '{required}'"
                )

    @pytest.mark.parametrize("device", CDP_DEVICES)
    def test_classification_returns_valid_type(self, device):
        """classify_current_data_param should return sensor/binary_sensor/skip."""
        valid_types = {"sensor", "binary_sensor", "skip"}
        merged = _build_merged(FIXTURES_ROOT / device)
        for param_id, param in merged.items():
            result = classify_current_data_param(param)
            assert result in valid_types, (
                f"{device} param {param_id}: got '{result}'"
            )

    @pytest.mark.parametrize("device", CDP_DEVICES)
    def test_no_duplicate_entity_keys(self, device):
        """All generated entity keys should be unique per device."""
        merged = _build_merged(FIXTURES_ROOT / device)
        keys: set[str] = set()
        for param_id, param in merged.items():
            if classify_current_data_param(param) == "skip":
                continue
            if is_regparams_data_id_mapped(param_id):
                continue
            name = param.get("name", "").strip()
            key = build_current_data_entity_key(param_id, name)
            assert key not in keys, f"{device}: duplicate key '{key}'"
            keys.add(key)

    @pytest.mark.parametrize("device", CDP_DEVICES)
    def test_static_ids_excluded_from_dynamic(self, device):
        """Static IDs should be filtered out by is_regparams_data_id_mapped."""
        merged = _build_merged(FIXTURES_ROOT / device)
        for param_id in merged:
            if is_regparams_data_id_mapped(param_id):
                assert param_id in STATIC_REGPARAMS_DATA_IDS


# =============================================================================
# Multi-device parametrized tests — sensor factory
# =============================================================================


class TestCreateCurrentDataSensorsMultiDevice:
    """Sensor factory tests across all devices."""

    @pytest.mark.parametrize("device", CDP_DEVICES)
    def test_creates_sensors(self, device):
        """Factory should create at least one sensor for each device."""
        from custom_components.econet300.sensor import create_current_data_sensors

        merged = _build_merged(FIXTURES_ROOT / device)
        coordinator = _make_coordinator(merged)
        api = MagicMock()
        api.uid = "test_uid"

        entities = create_current_data_sensors(coordinator, api)
        assert len(entities) > 0, f"{device}: no CDP sensors created"

    @pytest.mark.parametrize("device", CDP_DEVICES)
    def test_no_static_ids_in_sensors(self, device):
        """Sensor factory should never include static IDs."""
        from custom_components.econet300.sensor import create_current_data_sensors

        merged = _build_merged(FIXTURES_ROOT / device)
        coordinator = _make_coordinator(merged)
        api = MagicMock()
        api.uid = "test_uid"

        entities = create_current_data_sensors(coordinator, api)
        entity_keys = {e.entity_description.key for e in entities}
        for static_id in STATIC_REGPARAMS_DATA_IDS:
            for key in entity_keys:
                assert not key.startswith(f"cdp_{static_id}_"), (
                    f"{device}: static ID {static_id} found in key '{key}'"
                )

    @pytest.mark.parametrize("device", CDP_DEVICES)
    def test_no_binary_sensor_params_in_sensors(self, device):
        """Sensor factory should not include binary_sensor classified params."""
        from custom_components.econet300.sensor import create_current_data_sensors

        merged = _build_merged(FIXTURES_ROOT / device)
        coordinator = _make_coordinator(merged)
        api = MagicMock()
        api.uid = "test_uid"

        entities = create_current_data_sensors(coordinator, api)
        entity_keys = {e.entity_description.key for e in entities}

        for param_id, param in merged.items():
            if classify_current_data_param(param) == "binary_sensor":
                name = param.get("name", "").strip()
                bkey = build_current_data_entity_key(param_id, name)
                assert bkey not in entity_keys, (
                    f"{device}: binary param '{bkey}' in sensors"
                )


# =============================================================================
# Multi-device parametrized tests — binary sensor factory
# =============================================================================


class TestCreateCurrentDataBinarySensorsMultiDevice:
    """Binary sensor factory tests across all devices."""

    @pytest.mark.parametrize("device", CDP_DEVICES)
    def test_creates_binary_sensors(self, device):
        """Factory should create at least one binary sensor for each device."""
        from custom_components.econet300.binary_sensor import (
            create_current_data_binary_sensors,
        )

        merged = _build_merged(FIXTURES_ROOT / device)
        coordinator = _make_coordinator(merged)
        api = MagicMock()
        api.uid = "test_uid"

        entities = create_current_data_binary_sensors(coordinator, api)
        assert len(entities) > 0, f"{device}: no CDP binary sensors created"

    @pytest.mark.parametrize("device", CDP_DEVICES)
    def test_no_sensor_params_in_binary(self, device):
        """Binary factory should not include sensor classified params."""
        from custom_components.econet300.binary_sensor import (
            create_current_data_binary_sensors,
        )

        merged = _build_merged(FIXTURES_ROOT / device)
        coordinator = _make_coordinator(merged)
        api = MagicMock()
        api.uid = "test_uid"

        entities = create_current_data_binary_sensors(coordinator, api)
        entity_keys = {e.entity_description.key for e in entities}

        for param_id, param in merged.items():
            if classify_current_data_param(param) == "sensor":
                name = param.get("name", "").strip()
                skey = build_current_data_entity_key(param_id, name)
                assert skey not in entity_keys, (
                    f"{device}: sensor param '{skey}' in binary sensors"
                )


# =============================================================================
# Edge case tests (empty / None data)
# =============================================================================


class TestEdgeCases:
    """Edge case tests for empty and None data."""

    def test_sensor_factory_empty_merged(self):
        """Sensor factory returns empty list for empty merged data."""
        from custom_components.econet300.sensor import create_current_data_sensors

        coordinator = _make_coordinator({})
        api = MagicMock()
        api.uid = "test_uid"
        assert create_current_data_sensors(coordinator, api) == []

    def test_sensor_factory_none_data(self):
        """Sensor factory returns empty list when coordinator data is None."""
        from custom_components.econet300.sensor import create_current_data_sensors

        coordinator = MagicMock()
        coordinator.data = None
        api = MagicMock()
        api.uid = "test_uid"
        assert create_current_data_sensors(coordinator, api) == []

    def test_binary_factory_empty_merged(self):
        """Binary sensor factory returns empty list for empty merged data."""
        from custom_components.econet300.binary_sensor import (
            create_current_data_binary_sensors,
        )

        coordinator = _make_coordinator({})
        api = MagicMock()
        api.uid = "test_uid"
        assert create_current_data_binary_sensors(coordinator, api) == []


# =============================================================================
# ecoMAX810P-L specific tests (known param IDs)
# =============================================================================


class TestEcomax810PLSpecific:
    """Tests using known param IDs from ecoMAX810P-L fixture."""

    @pytest.fixture
    def merged(self) -> dict:
        """Return currentDataMerged from ecoMAX810P-L."""
        return _build_merged(FIXTURES_ROOT / "ecoMAX810P-L")

    def test_valve_mixer_1_is_sensor(self, merged):
        """ID 139 (Valve mixer 1, unit=5, value=59) → sensor."""
        param = merged["139"]
        assert param["name"] == "Valve mixer 1"
        assert param["value"] == 59
        assert classify_current_data_param(param) == "sensor"

    def test_lighter_is_binary_sensor(self, merged):
        """ID 1 (Lighter, unit=31, value=false) → binary_sensor."""
        param = merged["1"]
        assert param["name"] == "Lighter"
        assert classify_current_data_param(param) == "binary_sensor"

    def test_feeder_temp_is_sensor(self, merged):
        """ID 26 (Feeder temperature, unit=1, value=24.0) → sensor."""
        param = merged["26"]
        assert param["name"] == "Feeder temperature"
        assert classify_current_data_param(param) == "sensor"

    def test_valve_mixer_1_in_sensor_factory(self, merged):
        """Sensor factory should include cdp_139_valve_mixer_1."""
        from custom_components.econet300.sensor import create_current_data_sensors

        coordinator = _make_coordinator(merged)
        api = MagicMock()
        api.uid = "test_uid"

        entities = create_current_data_sensors(coordinator, api)
        keys = [e.entity_description.key for e in entities]
        assert "cdp_139_valve_mixer_1" in keys

    def test_lighter_in_binary_factory(self, merged):
        """Binary sensor factory should include cdp_1_lighter."""
        from custom_components.econet300.binary_sensor import (
            create_current_data_binary_sensors,
        )

        coordinator = _make_coordinator(merged)
        api = MagicMock()
        api.uid = "test_uid"

        entities = create_current_data_binary_sensors(coordinator, api)
        keys = [e.entity_description.key for e in entities]
        assert "cdp_1_lighter" in keys


# =============================================================================
# Discovery test — ensure CDP_DEVICES is populated
# =============================================================================


class TestDeviceDiscovery:
    """Ensure test parametrization found the expected devices."""

    def test_at_least_one_device_found(self):
        """At least one device fixture should support CDP."""
        assert len(CDP_DEVICES) >= 1

    def test_ecomax810p_l_in_devices(self):
        """ecoMAX810P-L should be in discovered devices."""
        assert "ecoMAX810P-L" in CDP_DEVICES

    def test_devices_with_error_responses_excluded(self):
        """Devices with error rmCurrentDataParams should be excluded."""
        assert "ecoMAX360" not in CDP_DEVICES
        assert "ecoSOL" not in CDP_DEVICES
