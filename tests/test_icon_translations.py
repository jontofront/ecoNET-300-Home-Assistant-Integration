"""Test icon translations for ecoNET300 integration.

This test file verifies icon translation functionality.
Currently focused on switch entity, but designed to be expanded
for all entity types (sensor, binary_sensor, number, etc.).
"""

from unittest.mock import Mock

from custom_components.econet300.api import Econet300Api
from custom_components.econet300.common import EconetDataCoordinator
from custom_components.econet300.switch import EconetSwitch, create_boiler_switch


def test_switch_has_translation_key():
    """Test that the switch has the correct translation key for icon translations."""
    # Create a mock coordinator and API
    mock_coordinator = Mock(spec=EconetDataCoordinator)
    mock_api = Mock(spec=Econet300Api)

    # Create the boiler switch
    switch = create_boiler_switch(mock_coordinator, mock_api)

    # Verify the translation key is set correctly
    assert switch.entity_description.translation_key == "boiler_control"

    # Verify no icon is set (should use icon translations instead)
    assert (
        not hasattr(switch.entity_description, "icon")
        or switch.entity_description.icon is None
    )


def test_switch_entity_creation():
    """Test that the switch entity is created correctly."""
    # Create a mock coordinator and API
    mock_coordinator = Mock(spec=EconetDataCoordinator)
    mock_api = Mock(spec=Econet300Api)

    # Create the boiler switch
    switch = create_boiler_switch(mock_coordinator, mock_api)

    # Verify the switch is created correctly
    assert isinstance(switch, EconetSwitch)
    assert switch.entity_description.key == "boiler_control"
    assert switch.entity_description.translation_key == "boiler_control"


def test_switch_icon_translation_structure():
    """Test that the switch icon translation structure is correct."""
    # Create a mock coordinator and API
    mock_coordinator = Mock(spec=EconetDataCoordinator)
    mock_api = Mock(spec=Econet300Api)

    # Create the boiler switch
    switch = create_boiler_switch(mock_coordinator, mock_api)

    # Verify the entity description has the required fields for icon translations
    assert switch.entity_description.key == "boiler_control"
    assert switch.entity_description.translation_key == "boiler_control"

    # Verify that the translation_key matches the key (this is the lookup path)
    # Home Assistant will look for: entity.switch.boiler_control in icons.json
    assert switch.entity_description.translation_key == "boiler_control"
