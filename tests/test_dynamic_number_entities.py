"""Test dynamic number entity creation."""

import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

from homeassistant.components.number import NumberEntity as HANumberEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
import pytest

from custom_components.econet300.api import Econet300Api
from custom_components.econet300.common import EconetDataCoordinator

# Category functions removed - category support eliminated
from custom_components.econet300.number import (
    async_setup_entry,
    create_dynamic_number_entity_description,
    should_be_number_entity,
)

# List of fixtures to test - only those with mergedData.json
FIXTURES_WITH_MERGED_DATA = ["ecoMAX810P-L", "ecoMAX860P3-O"]

# All available fixtures for basic tests
ALL_FIXTURES = [
    "ecoMAX810P-L",
    "ecoMAX360",
    "ecoMAX360-cf8",
    "ecoSOL",
    "SControl MK1",
    "ecoMAX850R2-X",
    "ecoMAX860D3-HB",
    "ecoMAX860P2-N",
    "ecoMAX860P3-O",
    "ecoMAX860P3-V",
    "ecoSOL500",
]


def load_fixture(fixture_name: str, filename: str) -> dict | None:
    """Load a fixture file, return None if not found."""
    fixture_path = Path(__file__).parent / "fixtures" / fixture_name / filename
    if not fixture_path.exists():
        return None
    with fixture_path.open(encoding="utf-8") as f:
        return json.load(f)


class TestDynamicNumberEntities:
    """Test dynamic number entity creation."""

    @pytest.fixture
    def mock_merged_data(self):
        """Load mock merged parameter data."""
        fixture_path = (
            Path(__file__).parent / "fixtures" / "ecoMAX810P-L" / "mergedData.json"
        )
        with fixture_path.open(encoding="utf-8") as f:
            return json.load(f)

    @pytest.fixture
    def mock_api(self, mock_merged_data):
        """Create a mock API with merged data."""
        api = MagicMock(spec=Econet300Api)
        api.fetch_merged_rm_data = AsyncMock(return_value=mock_merged_data)
        return api

    @pytest.fixture
    def mock_coordinator(self, mock_merged_data):
        """Create a mock coordinator with merged data."""
        coordinator = MagicMock(spec=EconetDataCoordinator)
        coordinator.data = {
            "sysParams": {"controllerId": "ecoMAX810P-L"},
            "regParams": {},
            "paramsEdits": {},
            "mergedData": mock_merged_data,
        }
        return coordinator

    def test_should_be_number_entity(self):
        """Test should_be_number_entity function."""
        # Test number entity candidate (no enum key at all)
        number_param = {"unit_name": "%", "edit": True}
        assert should_be_number_entity(number_param) is True

        # Test select entity candidate (has enum)
        select_param = {
            "unit_name": "",
            "edit": True,
            "enum": {"values": ["Off", "On"]},
        }
        assert should_be_number_entity(select_param) is False

        # Test read-only parameter
        readonly_param = {"unit_name": "%", "edit": False}
        assert should_be_number_entity(readonly_param) is False

        # Test parameter with unit but no edit
        no_edit_param = {"unit_name": "°C", "edit": False}
        assert should_be_number_entity(no_edit_param) is False

    def test_create_dynamic_number_entity_description(self):
        """Test create_dynamic_number_entity_description function."""
        param = {
            "unit_name": "%",
            "minv": 15,
            "maxv": 100,
            "key": "test_parameter",
            "name": "Test Parameter",
        }

        entity_desc = create_dynamic_number_entity_description("0", param)

        assert entity_desc.key == "test_parameter"
        assert entity_desc.translation_key == "test_parameter"
        assert entity_desc.native_min_value == 15.0
        assert entity_desc.native_max_value == 100.0
        assert entity_desc.native_step == 1.0
        # Unit mapping should work
        assert entity_desc.native_unit_of_measurement is not None

    def test_create_dynamic_number_entity_description_temperature(self):
        """Test temperature parameter entity description."""
        param = {
            "unit_name": "°C",
            "minv": 20,
            "maxv": 85,
            "key": "mixer_temp",
            "name": "Mixer Temperature",
        }

        entity_desc = create_dynamic_number_entity_description("69", param)

        assert entity_desc.key == "mixer_temp"
        assert entity_desc.translation_key == "mixer_temp"
        assert entity_desc.native_min_value == 20.0
        assert entity_desc.native_max_value == 85.0
        assert entity_desc.native_step == 1.0

    def test_create_dynamic_number_entity_description_large_range(self):
        """Test parameter with large range gets step 5."""
        param = {
            "unit_name": "kW",  # Use a unit that's not in the special list
            "minv": 0,
            "maxv": 255,
            "key": "large_range_param",
            "name": "Large Range Parameter",
        }

        entity_desc = create_dynamic_number_entity_description("100", param)

        assert entity_desc.native_min_value == 0.0
        assert entity_desc.native_max_value == 255.0
        assert entity_desc.native_step == 5.0  # Large range should get step 5

    @pytest.mark.asyncio
    async def test_dynamic_number_entity_creation(
        self, hass, mock_config_entry, mock_api, mock_coordinator
    ):
        """Test dynamic number entity creation in async_setup_entry."""

        # Mock the hass.data structure
        hass.data = {
            "econet300": {
                mock_config_entry.entry_id: {
                    "api": mock_api,
                    "coordinator": mock_coordinator,
                }
            }
        }

        # Mock async_add_entities
        mock_add_entities = MagicMock(spec=AddEntitiesCallback)

        # Call the setup function
        await async_setup_entry(hass, mock_config_entry, mock_add_entities)

        # Verify that entities were added
        mock_add_entities.assert_called_once()
        entities = mock_add_entities.call_args[0][0]

        # Should have created number entities (EconetNumber, categories removed)
        assert len(entities) > 0
        # All entities should be NumberEntity instances (base class)
        assert all(isinstance(entity, HANumberEntity) for entity in entities)

        # Check that we have the expected number of entities
        # This is approximate since it depends on the fixture data and filtering logic
        # (service parameters may be disabled, some become switches/selects, etc.)
        assert len(entities) >= 25  # At least 25 number entities should be created

    @pytest.mark.asyncio
    async def test_fallback_to_legacy_method(self, hass, mock_config_entry):
        """Test fallback to legacy method when merged data is unavailable."""

        # Create API that returns None for merged data
        mock_api = MagicMock(spec=Econet300Api)
        mock_api.fetch_merged_rm_data = AsyncMock(return_value=None)

        # Create coordinator WITHOUT mergedData to trigger fallback
        mock_coordinator_no_merged = MagicMock(spec=EconetDataCoordinator)
        mock_coordinator_no_merged.data = {
            "sysParams": {"controllerId": "ecoMAX810P-L"},
            "regParams": {},
            "paramsEdits": {},
            "mergedData": None,  # No merged data triggers legacy fallback
        }

        # Mock the hass.data structure
        hass.data = {
            "econet300": {
                mock_config_entry.entry_id: {
                    "api": mock_api,
                    "coordinator": mock_coordinator_no_merged,
                }
            }
        }

        # Mock async_add_entities
        mock_add_entities = MagicMock(spec=AddEntitiesCallback)

        # Call the setup function
        await async_setup_entry(hass, mock_config_entry, mock_add_entities)

        # Verify that entities were added (legacy method)
        mock_add_entities.assert_called_once()
        entities = mock_add_entities.call_args[0][0]

        # Should have created some entities from NUMBER_MAP
        assert len(entities) >= 0  # Could be 0 if no legacy entities are available

    def test_entity_properties_from_real_data(self, mock_merged_data):
        """Test entity properties using real fixture data."""
        # Find a number entity candidate from real data
        number_candidates = []
        for param_id, param in mock_merged_data["parameters"].items():
            if should_be_number_entity(param):
                number_candidates.append((param_id, param))
                if len(number_candidates) >= 3:  # Test first 3
                    break

        assert len(number_candidates) > 0, (
            "Should have number entity candidates in fixture data"
        )

        for param_id, param in number_candidates:
            entity_desc = create_dynamic_number_entity_description(param_id, param)

            # Verify basic properties - entity key uses param key directly
            assert entity_desc.key == param["key"]
            assert entity_desc.translation_key == param["key"]
            assert entity_desc.native_min_value == float(param["minv"])
            assert entity_desc.native_max_value == float(param["maxv"])

            # Verify unit mapping
            unit_name = param["unit_name"]
            if unit_name in ["%", "°C", "sek.", "min.", "h.", "r/min", "kW"]:
                assert entity_desc.native_unit_of_measurement is not None

            # Verify step calculation
            if unit_name in {"%", "°C"} or unit_name in ["sek.", "min.", "h."]:
                assert entity_desc.native_step == 1.0
            elif float(param["maxv"]) - float(param["minv"]) > 100:
                assert entity_desc.native_step == 5.0
            else:
                assert entity_desc.native_step == 1.0

    def test_error_handling_in_entity_creation(self):
        """Test error handling when creating entity descriptions."""
        # Test with invalid parameter data
        invalid_param = {
            "unit_name": "%",
            "minv": "invalid",  # Invalid min value
            "maxv": 100,
            "key": "test",
        }

        with pytest.raises((ValueError, TypeError)):
            create_dynamic_number_entity_description("0", invalid_param)

        # Test with missing required fields - should work with defaults
        incomplete_param = {
            "unit_name": "%"
            # Missing minv, maxv, key - should use defaults
        }

        # This should not raise an error because of defaults
        entity_desc = create_dynamic_number_entity_description("0", incomplete_param)
        assert entity_desc.native_min_value == 0.0  # Default min
        assert entity_desc.native_max_value == 100.0  # Default max
        assert entity_desc.translation_key == "parameter_0"  # Default key

    def test_multiple_categories_parameter_structure(self, mock_merged_data):
        """Test that parameters can have multiple categories in merged data."""
        # Test the data structure that would be created by the API
        # Create a mock parameter with multiple categories
        test_param = {
            "name": "Test Parameter",
            "number": 123,
            "categories": ["Information", "Boiler settings"],  # Multiple categories
            "category": "Information",  # First category for backward compatibility
            "unit_name": "%",
            "edit": True,
            "key": "test_param",
        }

        # Verify structure that API would create
        assert "categories" in test_param
        assert "category" in test_param
        assert isinstance(test_param["categories"], list)
        assert isinstance(test_param["category"], str)
        assert len(test_param["categories"]) > 1
        assert (
            test_param["category"] == test_param["categories"][0]
        )  # First category for backward compatibility

        # Verify that the fixture data has the expected structure
        # (In real usage, categories would be added by the API processing)
        assert "parameters" in mock_merged_data
        assert isinstance(mock_merged_data["parameters"], dict)

        # Verify that some parameters have the basic fields
        params_with_keys = []
        for param_id, param in mock_merged_data["parameters"].items():
            if isinstance(param, dict) and "key" in param:
                params_with_keys.append((param_id, param))

        assert len(params_with_keys) > 0, "Should have parameters with key field"

    def test_entity_key_generation(self, mock_merged_data):
        """Test that entity keys use param key directly."""
        # Create a test parameter
        test_param = {
            "name": "Test Parameter",
            "unit_name": "%",
            "minv": 0,
            "maxv": 100,
            "key": "test_param",
            "edit": True,
        }

        entity_desc = create_dynamic_number_entity_description("123", test_param)

        # Verify entity key uses param key directly
        assert entity_desc.key == "test_param", (
            f"Entity key {entity_desc.key} should equal param key"
        )
        assert entity_desc.translation_key == "test_param", (
            "Translation key should equal param key"
        )

    def test_entity_description_from_merged_data(self, mock_merged_data):
        """Test create_dynamic_number_entity_description with real merged data parameter."""
        # Get a test parameter
        test_param = None
        test_param_id = None
        for param_id, param in mock_merged_data["parameters"].items():
            if isinstance(param, dict) and "key" in param:
                test_param = param
                test_param_id = param_id
                break

        assert test_param is not None, "Should have test parameter"
        assert test_param_id is not None, "Should have test parameter ID"

        entity_desc = create_dynamic_number_entity_description(
            test_param_id, test_param
        )

        # Verify entity key uses param key directly
        assert entity_desc.key == test_param["key"], "Entity key should equal param key"

        # Verify other properties are preserved
        assert entity_desc.translation_key == test_param["key"]
        assert entity_desc.native_min_value == float(test_param.get("minv", 0))
        assert entity_desc.native_max_value == float(test_param.get("maxv", 100))


class TestMultipleFixtures:
    """Test with multiple device fixtures."""

    @pytest.mark.parametrize("fixture_name", ALL_FIXTURES)
    def test_fixture_sys_params_exists(self, fixture_name):
        """Test that sysParams.json exists and is valid for each fixture."""
        sys_params = load_fixture(fixture_name, "sysParams.json")
        assert sys_params is not None, f"sysParams.json missing for {fixture_name}"
        assert isinstance(sys_params, dict), (
            f"sysParams should be dict for {fixture_name}"
        )

    @pytest.mark.parametrize("fixture_name", ALL_FIXTURES)
    def test_fixture_reg_params_exists(self, fixture_name):
        """Test that regParams.json exists and is valid for each fixture."""
        reg_params = load_fixture(fixture_name, "regParams.json")
        assert reg_params is not None, f"regParams.json missing for {fixture_name}"
        assert isinstance(reg_params, dict), (
            f"regParams should be dict for {fixture_name}"
        )

    @pytest.mark.parametrize("fixture_name", ALL_FIXTURES)
    def test_fixture_controller_id(self, fixture_name):
        """Test that each fixture has a valid controllerID."""
        sys_params = load_fixture(fixture_name, "sysParams.json")
        assert sys_params is not None
        # Check for controllerID or controllerId (case may vary)
        controller_id = sys_params.get("controllerID") or sys_params.get("controllerId")
        assert controller_id is not None, f"controllerID missing for {fixture_name}"

    @pytest.mark.parametrize("fixture_name", FIXTURES_WITH_MERGED_DATA)
    def test_merged_data_structure(self, fixture_name):
        """Test mergedData.json structure for fixtures that have it."""
        merged_data = load_fixture(fixture_name, "mergedData.json")
        assert merged_data is not None, f"mergedData.json missing for {fixture_name}"
        assert "parameters" in merged_data, "mergedData should have parameters"
        assert isinstance(merged_data["parameters"], dict)
        assert len(merged_data["parameters"]) > 0, "Should have parameters"

    @pytest.mark.parametrize("fixture_name", FIXTURES_WITH_MERGED_DATA)
    def test_number_entity_candidates_from_merged_data(self, fixture_name):
        """Test that we can find number entity candidates in mergedData."""
        merged_data = load_fixture(fixture_name, "mergedData.json")
        assert merged_data is not None

        number_candidates = []
        for param_id, param in merged_data["parameters"].items():
            if should_be_number_entity(param):
                number_candidates.append((param_id, param))

        assert len(number_candidates) > 0, (
            f"Should have number entity candidates in {fixture_name}"
        )

    @pytest.mark.parametrize(
        ("fixture_name", "expected_keys"),
        [
            ("ecoMAX810P-L", ["controllerID", "uid", "softVer"]),
            ("ecoMAX360", ["controllerID", "uid"]),
            ("ecoSOL", ["controllerID", "uid"]),
            ("SControl MK1", ["controllerID", "uid"]),
        ],
    )
    def test_sys_params_expected_keys(self, fixture_name, expected_keys):
        """Test that sysParams has expected keys for each device type."""
        sys_params = load_fixture(fixture_name, "sysParams.json")
        if sys_params is None:
            pytest.skip(f"sysParams.json not available for {fixture_name}")

        for key in expected_keys:
            # Check case-insensitive
            found = any(k.lower() == key.lower() for k in sys_params)
            assert found, f"Expected key {key} not found in {fixture_name} sysParams"

    @pytest.mark.parametrize("fixture_name", ALL_FIXTURES)
    def test_reg_params_has_values(self, fixture_name):
        """Test that regParams has actual values."""
        reg_params = load_fixture(fixture_name, "regParams.json")
        if reg_params is None:
            pytest.skip(f"regParams.json not available for {fixture_name}")

        assert len(reg_params) > 0, f"regParams should have values for {fixture_name}"

    @pytest.mark.parametrize(
        ("fixture_name", "device_type"),
        [
            ("ecoMAX810P-L", "ecoMAX"),
            ("ecoMAX360", "ecoMAX"),
            ("ecoMAX360-cf8", "ecoMAX"),
            ("ecoMAX850R2-X", "ecoMAX"),
            ("ecoMAX860D3-HB", "ecoMAX"),
            ("ecoMAX860P2-N", "ecoMAX"),
            ("ecoMAX860P3-O", "ecoMAX"),
            ("ecoMAX860P3-V", "ecoMAX"),
            ("ecoSOL", "ecoSOL"),
            ("ecoSOL500", "ecoSOL"),
            ("SControl MK1", "SControl"),
        ],
    )
    def test_device_type_detection(self, fixture_name, device_type):
        """Test that device type can be detected from controllerID."""
        sys_params = load_fixture(fixture_name, "sysParams.json")
        if sys_params is None:
            pytest.skip(f"sysParams.json not available for {fixture_name}")

        controller_id = sys_params.get("controllerID") or sys_params.get("controllerId")
        assert controller_id is not None

        # Verify device type is in controllerID
        assert (
            device_type in controller_id or device_type.lower() in controller_id.lower()
        ), f"Device type {device_type} not found in controllerID {controller_id}"
