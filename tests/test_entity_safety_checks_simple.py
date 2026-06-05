"""Simple tests for ecoNET300 entity safety checks to prevent crashes."""

from unittest.mock import Mock, patch

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import UnitOfTemperature

from custom_components.econet300.entity import EconetEntity
from custom_components.econet300.sensor import (
    EconetSensor,
    EconetSensorEntityDescription,
)


def test_handle_coordinator_update_with_none_data():
    """Test that _handle_coordinator_update handles None coordinator data gracefully."""
    # Create a mock coordinator with None data
    mock_coordinator = Mock()
    mock_coordinator.data = None

    # Create entity instance
    mock_api = Mock()
    entity = EconetEntity(mock_coordinator, mock_api)
    entity.entity_description = EconetSensorEntityDescription(
        key="tempCO", name="Boiler Temperature", process_val=lambda x: x
    )
    entity.api = Mock()

    # Should not crash; returns early without calling _lookup_value
    with patch.object(entity, "_lookup_value") as mock_lookup:
        # ruff: noqa: SLF001
        entity._handle_coordinator_update()
        mock_lookup.assert_not_called()


def test_handle_coordinator_update_with_none_reg_params():
    """Test that _handle_coordinator_update handles None regParams gracefully."""
    # Create a mock coordinator with None regParams
    mock_coordinator = Mock()
    mock_coordinator.data = {
        "sysParams": {"controllerID": "ecoMAX360"},
        "regParams": None,
        "paramsEdits": {},
    }

    # Create entity instance
    mock_api = Mock()
    entity = EconetEntity(mock_coordinator, mock_api)
    entity.entity_description = EconetSensorEntityDescription(
        key="tempCO", name="Boiler Temperature", process_val=lambda x: x
    )
    entity.api = Mock()

    # This should not crash - it should handle None regParams gracefully
    # ruff: noqa: SLF001
    entity._handle_coordinator_update()

    # Entity should still be functional after handling None regParams
    # The implementation now logs a debug message about the value being None


def test_handle_coordinator_update_with_valid_data():
    """Test that _handle_coordinator_update works correctly with valid data."""
    # Create a mock coordinator with valid data
    mock_coordinator = Mock()
    mock_coordinator.data = {
        "sysParams": {"controllerID": "ecoMAX360"},
        "regParams": {"tempCO": 65.5},
        "paramsEdits": {},
    }

    # Create entity instance
    mock_api = Mock()
    entity = EconetEntity(mock_coordinator, mock_api)
    entity.entity_description = EconetSensorEntityDescription(
        key="tempCO", name="Boiler Temperature", process_val=lambda x: x
    )
    entity.api = Mock()

    # Mock the _sync_state method to avoid crashes
    with patch.object(entity, "_sync_state") as mock_sync:
        # ruff: noqa: SLF001
        entity._handle_coordinator_update()

        # Verify _sync_state was called with the correct value
        mock_sync.assert_called_with(65.5)


def test_handle_coordinator_update_with_missing_key():
    """Test that _handle_coordinator_update handles missing keys gracefully."""
    # Create a mock coordinator with data but missing the expected key
    mock_coordinator = Mock()
    mock_coordinator.data = {
        "sysParams": {"controllerID": "ecoMAX360"},
        "regParams": {"otherTemp": 45.0},  # Missing tempCO
        "paramsEdits": {},
    }

    # Create entity instance
    mock_api = Mock()
    entity = EconetEntity(mock_coordinator, mock_api)
    entity.entity_description = EconetSensorEntityDescription(
        key="tempCO", name="Boiler Temperature", process_val=lambda x: x
    )
    entity.api = Mock()

    # Mock the _sync_state method to avoid crashes
    with patch.object(entity, "_sync_state") as mock_sync:
        # ruff: noqa: SLF001
        entity._handle_coordinator_update()

        # Verify _sync_state was NOT called (because key was missing)
        mock_sync.assert_not_called()


def test_entity_does_not_crash_with_none_data():
    """Test that entity methods don't crash when data is None."""
    # Create a mock coordinator with None data
    mock_coordinator = Mock()
    mock_coordinator.data = None

    # Create entity instance
    mock_api = Mock()
    entity = EconetEntity(mock_coordinator, mock_api)
    entity.entity_description = EconetSensorEntityDescription(
        key="tempCO", name="Boiler Temperature", process_val=lambda x: x
    )
    entity.api = Mock()

    # This should not raise any exceptions
    # ruff: noqa: SLF001
    entity._handle_coordinator_update()
    # If we get here, no crash occurred - test passes


def test_entity_does_not_crash_with_none_reg_params():
    """Test that entity methods don't crash when regParams is None."""
    # Create a mock coordinator with None regParams
    mock_coordinator = Mock()
    mock_coordinator.data = {
        "sysParams": {"controllerID": "ecoMAX360"},
        "regParams": None,
        "paramsEdits": {},
    }

    # Create entity instance
    mock_api = Mock()
    entity = EconetEntity(mock_coordinator, mock_api)
    entity.entity_description = EconetSensorEntityDescription(
        key="tempCO", name="Boiler Temperature", process_val=lambda x: x
    )
    entity.api = Mock()

    # This should not raise any exceptions
    # ruff: noqa: SLF001
    entity._handle_coordinator_update()
    # If we get here, no crash occurred - test passes


def test_entity_handles_edit_params_in_data():
    """Test that entity handles editParams and informationParams in coordinator data."""
    mock_coordinator = Mock()
    mock_coordinator.data = {
        "sysParams": {"controllerID": "ecoMAX360i"},
        "regParams": {},
        "paramsEdits": {},
        "mergedData": {},
        "editParams": {"1211": {"value": 0, "minv": -1000, "maxv": 1000}},
        "informationParams": {"221": [True, [[0, 1, 0]]]},
    }

    mock_api = Mock()
    entity = EconetEntity(mock_coordinator, mock_api)
    entity.entity_description = EconetSensorEntityDescription(
        key="tempCO", name="Boiler Temperature", process_val=lambda x: x
    )
    entity.api = Mock()

    entity._handle_coordinator_update()


def test_entity_handles_missing_edit_params_keys():
    """Test that entity handles missing editParams/informationParams keys gracefully."""
    mock_coordinator = Mock()
    mock_coordinator.data = {
        "sysParams": {"controllerID": "ecoMAX360"},
        "regParams": {"tempCO": 65.5},
        "paramsEdits": {},
    }

    mock_api = Mock()
    entity = EconetEntity(mock_coordinator, mock_api)
    entity.entity_description = EconetSensorEntityDescription(
        key="tempCO", name="Boiler Temperature", process_val=lambda x: x
    )
    entity.api = Mock()

    with patch.object(entity, "_sync_state") as mock_sync:
        entity._handle_coordinator_update()
        mock_sync.assert_called_with(65.5)


def test_edge_cases():
    """Test various edge cases to ensure robustness."""
    test_cases = [
        {
            "name": "Empty data structure",
            "data": {"sysParams": {}, "regParams": {}, "paramsEdits": {}},
        },
        {
            "name": "Mixed None and valid data",
            "data": {
                "sysParams": None,
                "regParams": {"tempCO": 70.0},
                "paramsEdits": {},
            },
        },
        {
            "name": "All None data",
            "data": {"sysParams": None, "regParams": None, "paramsEdits": None},
        },
        {
            "name": "Full data with editParams and informationParams",
            "data": {
                "sysParams": {"controllerID": "ecoMAX360i"},
                "regParams": {},
                "paramsEdits": {},
                "mergedData": {},
                "editParams": {"1211": {"value": 0}},
                "informationParams": {"221": [True, [[0, 1, 0]]]},
            },
        },
    ]

    for test_case in test_cases:
        mock_coordinator = Mock()
        mock_coordinator.data = test_case["data"]

        mock_api = Mock()
        entity = EconetEntity(mock_coordinator, mock_api)
        entity.entity_description = EconetSensorEntityDescription(
            key="tempCO", name="Boiler Temperature", process_val=lambda x: x
        )
        entity.api = Mock()

        # This should not raise any exceptions
        # ruff: noqa: SLF001
        entity._handle_coordinator_update()
        # If we get here, no crash occurred - test passes


def test_comprehensive_safety_checks():
    """Test comprehensive safety checks for all scenarios."""
    # Test 1: None coordinator data
    mock_coordinator = Mock()
    mock_coordinator.data = None

    mock_api = Mock()
    entity = EconetEntity(mock_coordinator, mock_api)
    entity.entity_description = EconetSensorEntityDescription(
        key="tempCO", name="Boiler Temperature", process_val=lambda x: x
    )
    entity.api = Mock()

    # Should not crash
    # ruff: noqa: SLF001
    entity._handle_coordinator_update()

    # Test 2: None regParams
    mock_coordinator.data = {
        "sysParams": {"controllerID": "ecoMAX360"},
        "regParams": None,
        "paramsEdits": {},
    }

    # Should not crash
    # ruff: noqa: SLF001
    entity._handle_coordinator_update()

    # Test 3: Valid data
    mock_coordinator.data = {
        "sysParams": {"controllerID": "ecoMAX360"},
        "regParams": {"tempCO": 65.5},
        "paramsEdits": {},
    }

    with patch.object(entity, "_sync_state") as mock_sync:
        # ruff: noqa: SLF001
        entity._handle_coordinator_update()
        mock_sync.assert_called_with(65.5)

    # Test 4: Missing key
    mock_coordinator.data = {
        "sysParams": {"controllerID": "ecoMAX360"},
        "regParams": {"otherTemp": 45.0},
        "paramsEdits": {},
    }

    with patch.object(entity, "_sync_state") as mock_sync:
        # ruff: noqa: SLF001
        entity._handle_coordinator_update()
        mock_sync.assert_not_called()

    # If we get here, all tests passed
    assert True


def test_sync_state_restores_state_class_after_non_numeric_value():
    """Regression: a transient non-numeric value must not permanently disable stats.

    HA resolves ``_attr_*`` before ``entity_description.*``. A non-numeric update
    (e.g. ``None`` from a transient "off" string) nulls ``_attr_state_class``; a
    later numeric value must restore it so long-term statistics keep working.
    """
    description = EconetSensorEntityDescription(
        key="tempCO",
        name="Boiler Temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        state_class=SensorStateClass.MEASUREMENT,
        suggested_display_precision=1,
        process_val=lambda x: x,
    )

    sensor = object.__new__(EconetSensor)
    sensor.entity_description = description
    sensor._raw_value = None
    sensor.async_write_ha_state = Mock()

    # 1) Valid numeric value: metadata reflects the description.
    sensor._sync_state(65.5)
    assert sensor._attr_native_value == 65.5
    assert sensor._attr_state_class == SensorStateClass.MEASUREMENT
    assert sensor._attr_device_class == SensorDeviceClass.TEMPERATURE
    assert sensor._attr_native_unit_of_measurement == UnitOfTemperature.CELSIUS
    assert sensor._attr_suggested_display_precision == 1

    # 2) Transient non-numeric value: stats metadata cleared for safety.
    sensor._sync_state(None)
    assert sensor._attr_native_value is None
    assert sensor._attr_state_class is None
    assert sensor._attr_suggested_display_precision is None

    # 3) Numeric value returns: metadata must be restored, not stuck at None.
    sensor._sync_state(70.0)
    assert sensor._attr_native_value == 70.0
    assert sensor._attr_state_class == SensorStateClass.MEASUREMENT
    assert sensor._attr_device_class == SensorDeviceClass.TEMPERATURE
    assert sensor._attr_native_unit_of_measurement == UnitOfTemperature.CELSIUS
    assert sensor._attr_suggested_display_precision == 1


def test_select_entity_handles_none_reg_params_data():
    """Regression test: select extra_state_attributes must not crash when regParamsData is None.

    Issue #227 - ecoMAX360i controllers have reg_params_data=null which causes
    AttributeError: 'NoneType' object has no attribute 'get' in select.py.
    """
    from custom_components.econet300.select import EconetSelect

    mock_coordinator = Mock()
    mock_coordinator.data = {
        "sysParams": {"controllerID": "ecoMAX360i"},
        "regParams": {},
        "paramsEdits": {},
        "regParamsData": None,
    }

    mock_api = Mock()
    mock_api.uid = "test-uid"

    from homeassistant.components.select import SelectEntityDescription

    description = SelectEntityDescription(
        key="heater_mode",
        name="Heater Mode",
        translation_key="heater_mode",
    )

    entity = EconetSelect(description, mock_coordinator, mock_api, "heaterMode")
    attrs = entity.extra_state_attributes
    assert attrs["current_state_value"] is None
