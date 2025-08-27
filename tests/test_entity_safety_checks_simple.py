"""Simple tests for ecoNET300 entity safety checks to prevent crashes."""

from unittest.mock import Mock, patch

from custom_components.econet300.entity import EconetEntity
from custom_components.econet300.sensor import EconetSensorEntityDescription


def test_handle_coordinator_update_with_none_data():
    """Test that _handle_coordinator_update handles None coordinator data gracefully."""
    # Create a mock coordinator with None data
    mock_coordinator = Mock()
    mock_coordinator.data = None

    # Create entity instance
    entity = EconetEntity(mock_coordinator)
    entity.entity_description = EconetSensorEntityDescription(
        key="tempCO", name="Boiler Temperature", process_val=lambda x: x
    )
    entity.api = Mock()

    # This should not crash - it should log info and return early
    with patch("custom_components.econet300.entity._LOGGER") as mock_logger:
        # ruff: noqa: SLF001
        entity._handle_coordinator_update()

        # Verify info log was called
        mock_logger.info.assert_called_with("Coordinator data is None, skipping update")


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
    entity = EconetEntity(mock_coordinator)
    entity.entity_description = EconetSensorEntityDescription(
        key="tempCO", name="Boiler Temperature", process_val=lambda x: x
    )
    entity.api = Mock()

    # This should not crash - it should log info and continue
    with patch("custom_components.econet300.entity._LOGGER") as mock_logger:
        # ruff: noqa: SLF001
        entity._handle_coordinator_update()

        # Verify info log was called for regParams
        mock_logger.info.assert_called_with(
            "regParams was None, defaulting to empty dict"
        )


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
    entity = EconetEntity(mock_coordinator)
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
    entity = EconetEntity(mock_coordinator)
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
    entity = EconetEntity(mock_coordinator)
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
    entity = EconetEntity(mock_coordinator)
    entity.entity_description = EconetSensorEntityDescription(
        key="tempCO", name="Boiler Temperature", process_val=lambda x: x
    )
    entity.api = Mock()

    # This should not raise any exceptions
    # ruff: noqa: SLF001
    entity._handle_coordinator_update()
    # If we get here, no crash occurred - test passes


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
    ]

    for test_case in test_cases:
        mock_coordinator = Mock()
        mock_coordinator.data = test_case["data"]

        entity = EconetEntity(mock_coordinator)
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

    entity = EconetEntity(mock_coordinator)
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
