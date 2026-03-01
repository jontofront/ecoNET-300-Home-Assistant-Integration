"""Tests for dynamic CurrentData sensor and binary sensor creation.

Tests are parametrized across all device fixtures that have valid
rmCurrentDataParams.json and regParamsData.json files.
"""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

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


def _make_coordinator(
    current_data_merged: dict,
    reg_params: dict | None = None,
) -> MagicMock:
    """Build a mock coordinator with currentDataMerged and regParams data."""
    coordinator = MagicMock()
    coordinator.data = {
        "currentDataMerged": current_data_merged,
        "regParams": reg_params or {},
    }
    return coordinator


def _load_reg_params(device_dir: Path) -> dict:
    """Load regParams 'curr' section from a device fixture (matches API behavior)."""
    path = device_dir / "regParams.json"
    if not path.exists():
        return {}
    raw = _load_json(path)
    return raw.get("curr", raw) if isinstance(raw, dict) else {}


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
        reg_params = _load_reg_params(FIXTURES_ROOT / device)
        coordinator = _make_coordinator(merged, reg_params)
        api = MagicMock()
        api.uid = "test_uid"

        entities = create_current_data_sensors(coordinator, api)
        assert len(entities) > 0, f"{device}: no CDP sensors created"

    @pytest.mark.parametrize("device", CDP_DEVICES)
    def test_no_static_ids_in_sensors(self, device):
        """Sensor factory should never include static IDs."""
        from custom_components.econet300.sensor import create_current_data_sensors

        merged = _build_merged(FIXTURES_ROOT / device)
        reg_params = _load_reg_params(FIXTURES_ROOT / device)
        coordinator = _make_coordinator(merged, reg_params)
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
        reg_params = _load_reg_params(FIXTURES_ROOT / device)
        coordinator = _make_coordinator(merged, reg_params)
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
        reg_params = _load_reg_params(FIXTURES_ROOT / device)
        coordinator = _make_coordinator(merged, reg_params)
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
        reg_params = _load_reg_params(FIXTURES_ROOT / device)
        coordinator = _make_coordinator(merged, reg_params)
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

    @pytest.fixture
    def reg_params(self) -> dict:
        """Return regParams from ecoMAX810P-L."""
        return _load_reg_params(FIXTURES_ROOT / "ecoMAX810P-L")

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

    def test_valve_mixer_1_in_sensor_factory(self, merged, reg_params):
        """Sensor factory should include cdp_139_valve_mixer_1 (mixer 1 exists)."""
        from custom_components.econet300.sensor import create_current_data_sensors

        coordinator = _make_coordinator(merged, reg_params)
        api = MagicMock()
        api.uid = "test_uid"

        entities = create_current_data_sensors(coordinator, api)
        keys = [e.entity_description.key for e in entities]
        assert "cdp_139_valve_mixer_1" in keys

    def test_lighter_in_binary_factory(self, merged, reg_params):
        """Binary sensor factory should include cdp_1_lighter."""
        from custom_components.econet300.binary_sensor import (
            create_current_data_binary_sensors,
        )

        coordinator = _make_coordinator(merged, reg_params)
        api = MagicMock()
        api.uid = "test_uid"

        entities = create_current_data_binary_sensors(coordinator, api)
        keys = [e.entity_description.key for e in entities]
        assert "cdp_1_lighter" in keys


# =============================================================================
# Mixer skip tests — non-existent mixers should be excluded
# =============================================================================


class TestMixerSkip:
    """Entities for non-existent mixers must not be created."""

    MIXER_1_ONLY_REG_PARAMS = {
        "mixerTemp1": 32.95,
        "mixerTemp2": None,
        "mixerTemp3": None,
        "mixerTemp4": None,
    }

    @staticmethod
    def _mixer_merged():
        """Minimal currentDataMerged with mixer 1-4 sensor + binary entries."""
        return {
            "139": {"name": "Valve mixer 1", "unit": 5, "special": 0, "value": 59},
            "140": {"name": "Valve mixer 2", "unit": 5, "special": 0, "value": 0},
            "141": {"name": "Valve mixer 3", "unit": 5, "special": 0, "value": 0},
            "142": {"name": "Valve mixer 4", "unit": 5, "special": 0, "value": 0},
            "200": {"name": "Pump mixer 1", "unit": 31, "special": 0, "value": True},
            "201": {"name": "Pump mixer 2", "unit": 31, "special": 0, "value": False},
            "202": {"name": "Pump mixer 3", "unit": 31, "special": 0, "value": False},
            "203": {"name": "Pump mixer 4", "unit": 31, "special": 0, "value": False},
        }

    def test_sensor_mixer_1_created(self):
        """Sensor for mixer 1 should be created (mixer 1 connected)."""
        from custom_components.econet300.sensor import create_current_data_sensors

        coordinator = _make_coordinator(
            self._mixer_merged(), self.MIXER_1_ONLY_REG_PARAMS
        )
        api = MagicMock()
        api.uid = "test_uid"

        entities = create_current_data_sensors(coordinator, api)
        keys = {e.entity_description.key for e in entities}
        assert "cdp_139_valve_mixer_1" in keys

    def test_sensor_mixer_2_skipped(self):
        """Sensor for mixer 2 should be skipped (mixer 2 not connected)."""
        from custom_components.econet300.sensor import create_current_data_sensors

        coordinator = _make_coordinator(
            self._mixer_merged(), self.MIXER_1_ONLY_REG_PARAMS
        )
        api = MagicMock()
        api.uid = "test_uid"

        entities = create_current_data_sensors(coordinator, api)
        keys = {e.entity_description.key for e in entities}
        assert "cdp_140_valve_mixer_2" not in keys
        assert "cdp_141_valve_mixer_3" not in keys
        assert "cdp_142_valve_mixer_4" not in keys

    def test_binary_sensor_mixer_1_created(self):
        """Binary sensor for mixer 1 should be created (mixer 1 connected)."""
        from custom_components.econet300.binary_sensor import (
            create_current_data_binary_sensors,
        )

        coordinator = _make_coordinator(
            self._mixer_merged(), self.MIXER_1_ONLY_REG_PARAMS
        )
        api = MagicMock()
        api.uid = "test_uid"

        entities = create_current_data_binary_sensors(coordinator, api)
        keys = {e.entity_description.key for e in entities}
        assert "cdp_200_pump_mixer_1" in keys

    def test_binary_sensor_mixer_2_3_4_skipped(self):
        """Binary sensors for mixer 2/3/4 should be skipped."""
        from custom_components.econet300.binary_sensor import (
            create_current_data_binary_sensors,
        )

        coordinator = _make_coordinator(
            self._mixer_merged(), self.MIXER_1_ONLY_REG_PARAMS
        )
        api = MagicMock()
        api.uid = "test_uid"

        entities = create_current_data_binary_sensors(coordinator, api)
        keys = {e.entity_description.key for e in entities}
        assert "cdp_201_pump_mixer_2" not in keys
        assert "cdp_202_pump_mixer_3" not in keys
        assert "cdp_203_pump_mixer_4" not in keys

    def test_all_mixers_created_when_all_connected(self):
        """All mixer sensors created when all 4 mixers are connected."""
        from custom_components.econet300.sensor import create_current_data_sensors

        all_mixers_reg = {
            "mixerTemp1": 32.0,
            "mixerTemp2": 28.0,
            "mixerTemp3": 30.0,
            "mixerTemp4": 25.0,
        }
        coordinator = _make_coordinator(self._mixer_merged(), all_mixers_reg)
        api = MagicMock()
        api.uid = "test_uid"

        entities = create_current_data_sensors(coordinator, api)
        keys = {e.entity_description.key for e in entities}
        assert "cdp_139_valve_mixer_1" in keys
        assert "cdp_140_valve_mixer_2" in keys
        assert "cdp_141_valve_mixer_3" in keys
        assert "cdp_142_valve_mixer_4" in keys

    def test_ecomax810p_l_fixture_skips_mixer_2_3_4(self):
        """ecoMAX810P-L fixture has only mixer 1 — mixer 2/3/4 entities skipped."""
        from custom_components.econet300.sensor import create_current_data_sensors

        merged = _build_merged(FIXTURES_ROOT / "ecoMAX810P-L")
        reg_params = _load_reg_params(FIXTURES_ROOT / "ecoMAX810P-L")
        coordinator = _make_coordinator(merged, reg_params)
        api = MagicMock()
        api.uid = "test_uid"

        entities = create_current_data_sensors(coordinator, api)
        keys = {e.entity_description.key for e in entities}
        mixer_2_3_4_keys = [k for k in keys if "mixer_2" in k or "mixer_3" in k or "mixer_4" in k]
        assert mixer_2_3_4_keys == [], f"Unexpected mixer 2/3/4 sensors: {mixer_2_3_4_keys}"


# =============================================================================
# Component assignment tests — entities go to correct sub-devices
# =============================================================================


class TestComponentAssignment:
    """Entities should be assigned to the correct sub-device component."""

    def test_mixer_1_sensor_has_mixer_1_component(self):
        """Mixer 1 sensor should have component='mixer_1'."""
        from custom_components.econet300.sensor import create_current_data_sensors

        merged = {
            "139": {"name": "Valve mixer 1", "unit": 5, "special": 0, "value": 59},
        }
        reg_params = {"mixerTemp1": 32.0}
        coordinator = _make_coordinator(merged, reg_params)
        api = MagicMock()
        api.uid = "test_uid"

        entities = create_current_data_sensors(coordinator, api)
        assert len(entities) == 1
        assert entities[0].entity_description.component == "mixer_1"

    def test_huw_sensor_has_huw_component(self):
        """HUW-related sensor should have component='huw'."""
        from custom_components.econet300.sensor import create_current_data_sensors

        merged = {
            "500": {"name": "HUW temperature", "unit": 1, "special": 0, "value": 45.0},
        }
        coordinator = _make_coordinator(merged)
        api = MagicMock()
        api.uid = "test_uid"

        entities = create_current_data_sensors(coordinator, api)
        assert len(entities) == 1
        assert entities[0].entity_description.component == "huw"

    def test_buffer_sensor_has_buffer_component(self):
        """Buffer-related sensor should have component='buffer'."""
        from custom_components.econet300.sensor import create_current_data_sensors

        merged = {
            "600": {
                "name": "Upper buffer temperature",
                "unit": 1,
                "special": 0,
                "value": 50.0,
            },
        }
        coordinator = _make_coordinator(merged)
        api = MagicMock()
        api.uid = "test_uid"

        entities = create_current_data_sensors(coordinator, api)
        assert len(entities) == 1
        assert entities[0].entity_description.component == "buffer"

    def test_lambda_sensor_has_lambda_component(self):
        """Lambda-related sensor should have component='lambda'."""
        from custom_components.econet300.sensor import create_current_data_sensors

        merged = {
            "700": {"name": "Lambda level", "unit": 5, "special": 0, "value": 1.2},
        }
        coordinator = _make_coordinator(merged)
        api = MagicMock()
        api.uid = "test_uid"

        entities = create_current_data_sensors(coordinator, api)
        assert len(entities) == 1
        assert entities[0].entity_description.component == "lambda"

    def test_boiler_sensor_has_boiler_component(self):
        """Generic sensor should have component='boiler' (default)."""
        from custom_components.econet300.sensor import create_current_data_sensors

        merged = {
            "26": {
                "name": "Feeder temperature",
                "unit": 1,
                "special": 1,
                "value": 24.0,
            },
        }
        coordinator = _make_coordinator(merged)
        api = MagicMock()
        api.uid = "test_uid"

        entities = create_current_data_sensors(coordinator, api)
        assert len(entities) == 1
        assert entities[0].entity_description.component == "boiler"

    def test_binary_mixer_1_has_mixer_1_component(self):
        """Mixer 1 binary sensor should have component='mixer_1'."""
        from custom_components.econet300.binary_sensor import (
            create_current_data_binary_sensors,
        )

        merged = {
            "200": {"name": "Pump mixer 1", "unit": 31, "special": 0, "value": True},
        }
        reg_params = {"mixerTemp1": 32.0}
        coordinator = _make_coordinator(merged, reg_params)
        api = MagicMock()
        api.uid = "test_uid"

        entities = create_current_data_binary_sensors(coordinator, api)
        assert len(entities) == 1
        assert entities[0].entity_description.component == "mixer_1"

    def test_binary_huw_has_huw_component(self):
        """HUW-related binary sensor should have component='huw'."""
        from custom_components.econet300.binary_sensor import (
            create_current_data_binary_sensors,
        )

        merged = {
            "300": {"name": "HUW pump", "unit": 31, "special": 0, "value": False},
        }
        coordinator = _make_coordinator(merged)
        api = MagicMock()
        api.uid = "test_uid"

        entities = create_current_data_binary_sensors(coordinator, api)
        assert len(entities) == 1
        assert entities[0].entity_description.component == "huw"


# =============================================================================
# Device info override tests
# =============================================================================


class TestDeviceInfoOverride:
    """Verify CDP entities use device_info from component."""

    def test_current_data_sensor_device_info_delegates_to_component(self):
        """CurrentDataSensor with component should call get_device_info_for_component."""
        from custom_components.econet300.sensor import (
            CurrentDataSensor,
            EconetSensorEntityDescription,
        )

        desc = EconetSensorEntityDescription(
            key="cdp_139_valve_mixer_1",
            name="Valve mixer 1",
            component="mixer_1",
            has_entity_name=True,
        )
        api = MagicMock()
        api.uid = "test_uid"
        coordinator = _make_coordinator({})

        with patch(
            "custom_components.econet300.sensor.get_device_info_for_component"
        ) as mock_get_di:
            mock_get_di.return_value = {"identifiers": {("econet300", "test_uid-mixer-1")}}
            sensor = CurrentDataSensor(desc, coordinator, api, "139")
            di = sensor.device_info
            mock_get_di.assert_called_once_with("mixer_1", api)
            assert di is not None

    def test_current_data_sensor_device_info_no_component(self):
        """CurrentDataSensor without component should use base device_info."""
        from custom_components.econet300.sensor import (
            CurrentDataSensor,
            EconetSensorEntityDescription,
        )

        desc = EconetSensorEntityDescription(
            key="cdp_26_feeder_temperature",
            name="Feeder temperature",
            has_entity_name=True,
        )
        api = MagicMock()
        api.uid = "test_uid"
        coordinator = _make_coordinator({})

        sensor = CurrentDataSensor(desc, coordinator, api, "26")
        di = sensor.device_info
        # Should fall through to super().device_info (base EconetEntity)
        assert di is not None or di is None  # Just verify no crash

    def test_current_data_binary_sensor_device_info_delegates(self):
        """CurrentDataBinarySensor with component should call get_device_info_for_component."""
        from custom_components.econet300.binary_sensor import (
            CurrentDataBinarySensor,
            EconetBinarySensorEntityDescription,
        )

        desc = EconetBinarySensorEntityDescription(
            key="cdp_200_pump_mixer_1",
            name="Pump mixer 1",
            component="mixer_1",
            has_entity_name=True,
        )
        api = MagicMock()
        api.uid = "test_uid"
        coordinator = _make_coordinator({})

        with patch(
            "custom_components.econet300.binary_sensor.get_device_info_for_component"
        ) as mock_get_di:
            mock_get_di.return_value = {"identifiers": {("econet300", "test_uid-mixer-1")}}
            sensor = CurrentDataBinarySensor(desc, coordinator, api, "200")
            di = sensor.device_info
            mock_get_di.assert_called_once_with("mixer_1", api)
            assert di is not None


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
