"""Basic tests for ecoNET300 sensors."""

import json
from pathlib import Path
from unittest.mock import Mock

import pytest
from homeassistant.components.sensor import SensorStateClass

from custom_components.econet300.common_functions import (
    is_ecomax360i_controller,
    is_ecosol_controller,
)
from custom_components.econet300.const import (
    DEFAULT_SENSORS,
    ECOMAX360I_SENSORS,
    ECOSOL_CONTROLLER_MAP_REFERENCE_KEY,
    ECOSOL_SENSORS,
    EDIT_PARAMS_DATA_SENSOR_MAP,
    ENTITY_VALUE_PROCESSOR,
    INFORMATION_PARAMS_SENSOR_MAP,
    SENSITIVE_PARAM_KEYS,
    SENSOR_ENUM_OPTIONS,
    SENSOR_MAP_KEY,
    STATE_UNKNOWN,
)
from custom_components.econet300.entity import EconetEntity
from custom_components.econet300.sensor import (
    EconetSensorEntityDescription,
    _controller_sensor_key_candidates,
    can_add_mixer,
    create_controller_sensors,
    create_sensor_entity_description,
)


class TestEconetSensorBasic:
    """Test basic sensor functionality."""

    # ruff: noqa: PLR6301
    def test_create_sensor_entity_description(self):
        """Test creating a sensor entity description."""
        # Test with a simple key
        description = create_sensor_entity_description("tempCO")

        assert description.key == "tempCO"
        assert description.translation_key == "temp_co"
        assert description.process_val is not None

    # ruff: noqa: PLR6301
    @pytest.mark.parametrize(
        "key",
        [
            "tempCO",
            "boilerPower",
            "boilerPowerKW",
            "fuelLevel",
            "tempCWU",
            "tempFeeder",
            "fanPower",
            "tempFlueGas",
            "tempBack",
            "quality",
            "signal",
        ],
    )
    def test_core_numeric_sensors_default_to_measurement(self, key: str) -> None:
        """Core numeric sensors must keep MEASUREMENT for long-term statistics."""
        description = create_sensor_entity_description(key)
        assert description.state_class == SensorStateClass.MEASUREMENT

    # ruff: noqa: PLR6301
    @pytest.mark.parametrize("key", ["mode", "statusCO", "controllerID"])
    def test_suppressed_keys_have_no_state_class(self, key: str) -> None:
        """Enum/status/string keys stay suppressed to None (no bogus statistics)."""
        description = create_sensor_entity_description(key)
        assert description.state_class is None

    # ruff: noqa: PLR6301
    @pytest.mark.parametrize(
        "key",
        ["ActualFlowTemp", "ActualReturnTemp", "Circuit1DesiredLWT"],
    )
    def test_ecomax360i_temperature_sensors_ignore_off_state(
        self, key: str
    ) -> None:
        """ecoMAX360i temperature sensors should not publish off as numeric state."""
        description = create_sensor_entity_description(key)

        assert description.process_val("off") is None
        assert description.process_val("") is None
        assert description.process_val("34.5") == 34.5

    @pytest.mark.parametrize("key", ["mode", "transmission"])
    def test_enum_sensor_unknown_fallback_is_in_options(self, key: str) -> None:
        """Enum sensors must include STATE_UNKNOWN in options when processor can return it."""
        options = SENSOR_ENUM_OPTIONS.get(key)
        assert options is not None, f"Missing SENSOR_ENUM_OPTIONS for {key}"
        assert STATE_UNKNOWN in options, (
            f"STATE_UNKNOWN not in options for {key} — HA rejects the state"
        )

        processor = ENTITY_VALUE_PROCESSOR.get(key)
        assert processor is not None
        assert processor(9999) == STATE_UNKNOWN

    # ruff: noqa: PLR6301
    def test_can_add_mixer_with_valid_data(self):
        """Test can_add_mixer with valid data."""
        # Create a mock coordinator with valid data
        mock_coordinator = Mock()
        mock_coordinator.data = {"regParams": {"mixerTemp1": 25.5}}
        mock_coordinator.has_reg_data.return_value = True

        # Test with valid mixer data
        result = can_add_mixer("mixerTemp1", mock_coordinator)
        assert result is True

    # ruff: noqa: PLR6301
    def test_can_add_mixer_with_invalid_data(self):
        """Test can_add_mixer with invalid data."""
        # Create a mock coordinator with invalid data
        mock_coordinator = Mock()
        mock_coordinator.data = {"regParams": {"mixerTemp1": None}}
        mock_coordinator.has_reg_data.return_value = True

        # Test with None value
        result = can_add_mixer("mixerTemp1", mock_coordinator)
        assert result is False

    # ruff: noqa: PLR6301
    def test_can_add_mixer_with_missing_data(self):
        """Test can_add_mixer with missing data."""
        # Create a mock coordinator with missing data
        mock_coordinator = Mock()
        mock_coordinator.data = {"regParams": {}}
        mock_coordinator.has_reg_data.return_value = False

        # Test with missing data
        result = can_add_mixer("mixerTemp1", mock_coordinator)
        assert result is False


class TestEconetSensorEntityDescription:
    """Test sensor entity description."""

    # ruff: noqa: PLR6301
    def test_entity_description_creation(self):
        """Test creating an entity description."""
        description = EconetSensorEntityDescription(
            key="testSensor", name="Test Sensor", process_val=lambda x: x * 2
        )

        assert description.key == "testSensor"
        assert description.name == "Test Sensor"
        assert description.process_val(5) == 10

    # ruff: noqa: PLR6301
    def test_entity_description_default_process_val(self):
        """Test default process_val function."""
        description = EconetSensorEntityDescription(key="testSensor")

        # Default process_val should return the value as-is
        assert description.process_val(42) == 42
        assert description.process_val("test") == "test"


class TestIsEcosolController:
    """Pattern match for sysParams controllerID (ecoSOL [n] product line)."""

    @pytest.mark.parametrize(
        "cid",
        [
            "ecoSOL",
            "ecoSOL 301",
            "ecoSOL 400",
            "ecoSOL 500",
            "ecoSOL500",
            "  ecoSOL 301  ",
        ],
    )
    def test_matches_ecosol_models(self, cid: str) -> None:
        assert is_ecosol_controller(cid)

    @pytest.mark.parametrize(
        "cid",
        [
            None,
            "",
            "ecoMAX860P3-V",
            "ecoSOL not_a_model",
            "ecosol 301",
        ],
    )
    def test_rejects_non_ecosol(self, cid: str | None) -> None:
        assert not is_ecosol_controller(cid)


class TestIsEcomax360iController:
    """sysParams controllerID for schema-style regParams (ecoMAX360 / 360i line)."""

    def test_matches_ecoMAX360i(self) -> None:
        assert is_ecomax360i_controller("ecoMAX360i")
        assert is_ecomax360i_controller("  ecoMAX360i  ")

    @pytest.mark.parametrize(
        "cid",
        [
            None,
            "",
            "ecoMAX360",
            "ecoMAX360i TOUCH",
            "ecoMAX860P3-V",
        ],
    )
    def test_rejects_other(self, cid: str | None) -> None:
        assert not is_ecomax360i_controller(cid)


class TestSensorMappingLogic:
    """Test sensor mapping logic for different controllerIDs."""

    # ruff: noqa: PLR6301
    @pytest.mark.parametrize(
        "cid",
        [
            "ecoSOL",
            "ecoSOL 301",
            "ecoSOL 400",
            "ecoSOL 500",
            "ecoSOL500",
        ],
    )
    def test_ecosol_models_use_ecosol_sensors(self, cid: str):
        """All ecoSOL [n] controllerIDs use ECOSOL_SENSORS (issues #219, #220)."""
        keys = _controller_sensor_key_candidates(cid)
        ecoSTER_stripped = keys - SENSOR_MAP_KEY.get("ecoSter", set())
        assert keys == ECOSOL_SENSORS
        assert ecoSTER_stripped == ECOSOL_SENSORS
        assert is_ecosol_controller(cid)

    # ruff: noqa: PLR6301
    def test_non_ecosol_controllers_use_default_sensors(self):
        """Boiler and other controllers use DEFAULT_SENSORS."""
        for controller_id in (
            "ecoMAX860P3-V",
            "SControl MK1",
            None,
        ):
            keys = _controller_sensor_key_candidates(controller_id)
            assert keys == DEFAULT_SENSORS

    def test_ecomax360i_uses_ecomax360i_sensors(self) -> None:
        """ecoMAX360i uses ``curr`` register keys, not boiler DEFAULT_SENSORS."""
        keys = _controller_sensor_key_candidates("ecoMAX360i")
        assert keys == ECOMAX360I_SENSORS
        assert "tempCO" not in keys
        assert "TempCircuit3" in keys

    # ruff: noqa: PLR6301
    def test_reference_mappings_exist_for_documentation(self):
        """SENSOR_MAP_KEY holds per-device sets; ecoSOL [n] reference matches runtime."""
        assert SENSOR_MAP_KEY[ECOSOL_CONTROLLER_MAP_REFERENCE_KEY] == ECOSOL_SENSORS
        assert SENSOR_MAP_KEY["ecoMAX360i"] == ECOMAX360I_SENSORS
        for cid in ("ecoSter", "lambda"):
            assert cid in SENSOR_MAP_KEY
            assert SENSOR_MAP_KEY[cid] != DEFAULT_SENSORS

    # ruff: noqa: PLR6301
    def test_unknown_controllers_use_default_sensors(self):
        """Unknown controllerID values use DEFAULT_SENSORS."""
        unknown_controllers = [
            "ecoMAX860D3-HB",
            "ecoMAX860P4-O MINI MATIC",
            "ecoMAX850R2-X",
            "ecoMAX810P-L TOUCH",
            "ecoMAX860P2-N TOUCH",
            "UnknownController",
        ]

        for controller_id in unknown_controllers:
            assert _controller_sensor_key_candidates(controller_id) == DEFAULT_SENSORS

    # ruff: noqa: PLR6301
    def test_default_sensors_comprehensive(self):
        """Test that DEFAULT_SENSORS contains comprehensive sensor set."""
        # Verify DEFAULT_SENSORS contains expected sensor types
        expected_sensors = {
            "tempCO",  # Boiler temperature
            "tempCWU",  # Hot water temperature
            "boilerPower",  # Boiler power
            "mode",  # Operation mode
            "statusCO",  # Boiler status
        }

        # All expected sensors should be in DEFAULT_SENSORS
        for sensor in expected_sensors:
            assert sensor in DEFAULT_SENSORS, (
                f"Expected sensor {sensor} not in DEFAULT_SENSORS"
            )

    # ruff: noqa: PLR6301
    def test_create_controller_sensors_ecosol301_fixture(self):
        """EcoSOL 301 regParams produce T1/P1 sensors, not boiler tempCO (issue #219)."""
        fixture_dir = Path(__file__).parent / "fixtures" / "ecoSOL301"
        reg_params = json.loads(
            (fixture_dir / "regParams.json").read_text(encoding="utf-8")
        )
        sys_params = json.loads(
            (fixture_dir / "sysParams.json").read_text(encoding="utf-8")
        )
        mock_coordinator = Mock()
        mock_coordinator.data = {"regParams": reg_params, "sysParams": sys_params}
        mock_api = Mock()

        entities = create_controller_sensors(mock_coordinator, mock_api)
        keys = {e.entity_description.key for e in entities}

        assert "T1" in keys
        assert "P1" in keys
        assert "tempCO" not in keys

    def test_create_controller_sensors_ecomax360_fixture(self) -> None:
        """ecoMAX360i ``curr`` keys produce circuit sensors, not boiler tempCO."""
        fixture_dir = Path(__file__).parent / "fixtures" / "ecoMAX360"
        reg_raw = json.loads(
            (fixture_dir / "regParams.json").read_text(encoding="utf-8")
        )
        reg_params = reg_raw.get("curr") or reg_raw
        sys_params = json.loads(
            (fixture_dir / "sysParams.json").read_text(encoding="utf-8")
        )
        mock_coordinator = Mock()
        mock_coordinator.data = {"regParams": reg_params, "sysParams": sys_params}
        mock_api = Mock()

        entities = create_controller_sensors(mock_coordinator, mock_api)
        keys = {e.entity_description.key for e in entities}

        assert "TempCircuit3" in keys
        assert "quality" in keys
        assert "tempCO" not in keys
        # editParams / informationParams-only keys (not in regParams/sysParams)
        assert "TargetFlowTemp" in keys
        assert "COP" in keys
        assert "AXENREGISTER64" in keys

    def test_sensitive_sysparams_keys_are_not_exposed(self) -> None:
        """Credentials/network keys in sysParams must never become sensors."""
        fixture_dir = Path(__file__).parent / "fixtures" / "ecoMAX810P-L"
        reg_params = json.loads(
            (fixture_dir / "regParams.json").read_text(encoding="utf-8")
        )
        sys_params = json.loads(
            (fixture_dir / "sysParams.json").read_text(encoding="utf-8")
        )
        # Guard: the fixture must actually contain the sensitive keys we filter,
        # otherwise this test would pass vacuously.
        present_sensitive = SENSITIVE_PARAM_KEYS & set(sys_params)
        assert present_sensitive, "fixture lacks sensitive keys to validate filtering"

        mock_coordinator = Mock()
        mock_coordinator.data = {"regParams": reg_params, "sysParams": sys_params}
        mock_api = Mock()

        entities = create_controller_sensors(mock_coordinator, mock_api)
        keys = {e.entity_description.key for e in entities}

        assert keys.isdisjoint(SENSITIVE_PARAM_KEYS)


class TestGetDataSourcesTuple:
    """Test _get_data_sources returns the correct 6-tuple structure."""

    @staticmethod
    def _build_entity(coordinator_data: dict | None) -> EconetEntity:
        """Create a minimal entity wired to coordinator data."""
        entity = object.__new__(EconetEntity)
        entity.coordinator = Mock()
        entity.coordinator.data = coordinator_data
        return entity

    def test_returns_six_element_tuple(self) -> None:
        """_get_data_sources returns a 6-tuple with all data sources."""
        coord_data = {
            "sysParams": {"controllerID": "ecoMAX360i"},
            "regParams": {"tempCO": 65.5},
            "paramsEdits": {"k": 1},
            "mergedData": {"parameters": {}},
            "editParams": {"1211": {"value": 0}},
            "informationParams": {"221": [True, [[0, 1, 0]]]},
        }
        entity = self._build_entity(coord_data)
        sources = entity._get_data_sources()
        assert len(sources) == 6
        assert sources[0] == coord_data["sysParams"]
        assert sources[1] == coord_data["regParams"]
        assert sources[2] == coord_data["paramsEdits"]
        assert sources[3] == coord_data["mergedData"]
        assert sources[4] == coord_data["editParams"]
        assert sources[5] == coord_data["informationParams"]

    def test_defaults_missing_keys_to_empty_dict(self) -> None:
        """Missing data keys default to empty dicts (backward compatibility)."""
        coord_data = {
            "sysParams": {"controllerID": "ecoMAX860P3-V"},
            "regParams": {"tempCO": 65.5},
            "paramsEdits": {},
        }
        entity = self._build_entity(coord_data)
        sources = entity._get_data_sources()
        assert len(sources) == 6
        assert sources[4] == {}  # editParams
        assert sources[5] == {}  # informationParams

    def test_none_coordinator_data(self) -> None:
        """None coordinator data yields all empty dicts."""
        entity = self._build_entity(None)
        sources = entity._get_data_sources()
        assert len(sources) == 6
        assert all(s == {} for s in sources)


class TestEditParamsSensorMaps:
    """Validate INFORMATION_PARAMS_SENSOR_MAP and EDIT_PARAMS_DATA_SENSOR_MAP."""

    def test_info_params_keys_in_ecomax360i_sensors(self) -> None:
        """All informationParams sensor keys should be in ECOMAX360I_SENSORS."""
        for key in INFORMATION_PARAMS_SENSOR_MAP:
            assert key in ECOMAX360I_SENSORS, (
                f"{key} in INFORMATION_PARAMS_SENSOR_MAP but missing from ECOMAX360I_SENSORS"
            )

    def test_edit_params_keys_in_ecomax360i_sensors(self) -> None:
        """All editParams.data sensor keys should be in ECOMAX360I_SENSORS."""
        for key in EDIT_PARAMS_DATA_SENSOR_MAP:
            assert key in ECOMAX360I_SENSORS, (
                f"{key} in EDIT_PARAMS_DATA_SENSOR_MAP but missing from ECOMAX360I_SENSORS"
            )

    def test_info_params_ids_in_cf8_fixture(self) -> None:
        """IDs in INFORMATION_PARAMS_SENSOR_MAP must exist in ecoMAX360-cf8 fixture."""
        fixture = (
            Path(__file__).parent / "fixtures" / "ecoMAX360-cf8" / "editParams.json"
        )
        edit_params = json.loads(fixture.read_text(encoding="utf-8"))
        info_params = edit_params.get("informationParams", {})
        for key, param_id in INFORMATION_PARAMS_SENSOR_MAP.items():
            assert param_id in info_params, (
                f"INFORMATION_PARAMS_SENSOR_MAP['{key}'] = '{param_id}' "
                f"not found in ecoMAX360-cf8 informationParams"
            )

    def test_edit_params_ids_in_cf8_fixture(self) -> None:
        """IDs in EDIT_PARAMS_DATA_SENSOR_MAP must exist in ecoMAX360-cf8 fixture."""
        fixture = (
            Path(__file__).parent / "fixtures" / "ecoMAX360-cf8" / "editParams.json"
        )
        edit_params = json.loads(fixture.read_text(encoding="utf-8"))
        data_section = edit_params.get("data", {})
        for key, param_id in EDIT_PARAMS_DATA_SENSOR_MAP.items():
            assert param_id in data_section, (
                f"EDIT_PARAMS_DATA_SENSOR_MAP['{key}'] = '{param_id}' "
                f"not found in ecoMAX360-cf8 editParams.data"
            )


class TestLookupValueEditParams:
    """Test _lookup_value() resolves from editParams and informationParams."""

    @staticmethod
    def _build_entity(key: str, coordinator_data: dict) -> EconetEntity:
        """Create a minimal entity wired to coordinator data."""
        entity = object.__new__(EconetEntity)
        entity.coordinator = Mock()
        entity.coordinator.data = coordinator_data
        entity.entity_description = Mock()
        entity.entity_description.key = key
        entity.entity_description.param_id = None
        return entity

    def test_lookup_from_information_params(self) -> None:
        """_lookup_value() extracts value from informationParams for mapped sensors."""
        fixture = (
            Path(__file__).parent / "fixtures" / "ecoMAX360-cf8" / "editParams.json"
        )
        edit_params = json.loads(fixture.read_text(encoding="utf-8"))
        coord_data = {
            "sysParams": {},
            "regParams": {},
            "paramsEdits": {},
            "mergedData": {},
            "editParams": edit_params.get("data", {}),
            "informationParams": edit_params.get("informationParams", {}),
        }
        entity = self._build_entity("ActualDHWTemp", coord_data)
        val = entity._lookup_value()
        assert val == "42.4"

    def test_lookup_from_edit_params_data(self) -> None:
        """_lookup_value() extracts value from editParams.data for mapped sensors."""
        fixture = (
            Path(__file__).parent / "fixtures" / "ecoMAX360-cf8" / "editParams.json"
        )
        edit_params = json.loads(fixture.read_text(encoding="utf-8"))
        coord_data = {
            "sysParams": {},
            "regParams": {},
            "paramsEdits": {},
            "mergedData": {},
            "editParams": edit_params.get("data", {}),
            "informationParams": edit_params.get("informationParams", {}),
        }
        entity = self._build_entity("AXENREGISTER64", coord_data)
        val = entity._lookup_value()
        assert val == 0

    def test_regparams_takes_precedence(self) -> None:
        """RegParams values should be returned before editParams for shared keys."""
        coord_data = {
            "sysParams": {},
            "regParams": {"TempCWU": 43.5},
            "paramsEdits": {},
            "mergedData": {},
            "editParams": {},
            "informationParams": {"61": [True, [["42.4", 1, 0]]]},
        }
        entity = self._build_entity("TempCWU", coord_data)
        val = entity._lookup_value()
        assert val == 43.5

    def test_cop_from_information_params(self) -> None:
        """COP sensor resolves from informationParams ID 221."""
        fixture = (
            Path(__file__).parent / "fixtures" / "ecoMAX360-cf8" / "editParams.json"
        )
        edit_params = json.loads(fixture.read_text(encoding="utf-8"))
        coord_data = {
            "sysParams": {},
            "regParams": {},
            "paramsEdits": {},
            "mergedData": {},
            "editParams": edit_params.get("data", {}),
            "informationParams": edit_params.get("informationParams", {}),
        }
        entity = self._build_entity("COP", coord_data)
        val = entity._lookup_value()
        assert val == 0

    def test_scop_from_information_params(self) -> None:
        """SCOP sensor resolves from informationParams ID 222."""
        fixture = (
            Path(__file__).parent / "fixtures" / "ecoMAX360-cf8" / "editParams.json"
        )
        edit_params = json.loads(fixture.read_text(encoding="utf-8"))
        coord_data = {
            "sysParams": {},
            "regParams": {},
            "paramsEdits": {},
            "mergedData": {},
            "editParams": edit_params.get("data", {}),
            "informationParams": edit_params.get("informationParams", {}),
        }
        entity = self._build_entity("SCOP", coord_data)
        val = entity._lookup_value()
        assert val == 4.67
