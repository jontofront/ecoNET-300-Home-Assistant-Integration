"""Basic tests for ecoNET300 sensors."""

import json
from pathlib import Path
from unittest.mock import Mock

import pytest

from custom_components.econet300.common_functions import (
    is_ecomax360i_controller,
    is_ecosol_controller,
)
from custom_components.econet300.const import (
    DEFAULT_SENSORS,
    ECOMAX360I_SENSORS,
    ECOSOL_CONTROLLER_MAP_REFERENCE_KEY,
    ECOSOL_SENSORS,
    SENSOR_MAP_KEY,
)
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
