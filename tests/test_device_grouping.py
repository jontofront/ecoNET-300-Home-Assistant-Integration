"""Tests for the configurable device grouping option (split vs single).

Covers:
- ``EconetDataCoordinator.single_device_tree`` reading the option.
- ``get_device_info_for_component`` split vs single behaviour.
- Per-component entity ``device_info`` honouring the coordinator flag.
- Component devices connected through the controller device, with
  ``via_device_id`` (Home Assistant 2026.8+) and ``via_device`` (older).
"""

from collections.abc import Iterator
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from custom_components.econet300.common import EconetDataCoordinator
from custom_components.econet300.const import (
    COMPONENT_BUFFER,
    COMPONENT_HUW,
    COMPONENT_LAMBDA,
    COMPONENT_SOLAR,
    CONF_DEVICE_GROUPING,
    DEVICE_GROUPING_SINGLE,
    DEVICE_GROUPING_SPLIT,
    DOMAIN,
)
from custom_components.econet300.entity import (
    EconetEntity,
    EcoSterEntity,
    LambdaEntity,
    MixerEntity,
    get_device_info_for_component,
)
from custom_components.econet300.calendar import EconetScheduleCalendar
from custom_components.econet300.common_functions import schedule_component
from custom_components.econet300.number import (
    AdvancedParameterNumber,
    ServiceParameterNumber,
)

CONTROLLER_DEVICE_ID = "controller-device-id"


@pytest.fixture(params=[True, False], ids=["via_device_id", "via_device"])
def supports_via_device_id(request: pytest.FixtureRequest) -> Iterator[bool]:
    """Run the test as on Home Assistant 2026.8+ and as on an older version."""
    with patch(
        "custom_components.econet300.entity.HA_SUPPORTS_VIA_DEVICE_ID", request.param
    ):
        yield request.param


def _assert_connected_via_controller(
    info: Any, api: MagicMock, supports_via_device_id: bool
) -> None:
    """Assert the device links to the controller device."""
    if supports_via_device_id:
        assert info.get("via_device_id") == CONTROLLER_DEVICE_ID
        assert "via_device" not in info
    else:
        assert info.get("via_device") == (DOMAIN, api.uid)
        assert "via_device_id" not in info


def _make_api() -> MagicMock:
    """Create a mock API with the attributes device_info reads."""
    api = MagicMock()
    api.uid = "test-uid"
    api.model_id = "ecoMAX360i"
    api.host = "http://test"
    api.sw_rev = "1.0"
    api.hw_ver = "hw1"
    return api


def _coordinator(single: bool) -> MagicMock:
    """Mock coordinator exposing the single_device_tree flag."""
    coord = MagicMock(spec=EconetDataCoordinator)
    coord.single_device_tree = single
    coord.controller_device_id = CONTROLLER_DEVICE_ID
    return coord


def _identifier(device_info: Any) -> str:
    """Extract the single identifier string from a DeviceInfo object."""
    return next(iter(device_info["identifiers"]))[1]


def _entity_device_info(cls: type, entity: Any) -> Any:
    """Invoke the device_info property defined on the given class."""
    return cls.device_info.fget(entity)


# ---------------------------------------------------------------------------
# Coordinator option reading
# ---------------------------------------------------------------------------
def test_single_device_tree_default_is_split() -> None:
    """Default (no option) keeps split devices."""
    coord = object.__new__(EconetDataCoordinator)
    coord._device_grouping = DEVICE_GROUPING_SPLIT
    assert coord.single_device_tree is False


def test_single_device_tree_true_when_single() -> None:
    """Single option enables the merged device tree."""
    coord = object.__new__(EconetDataCoordinator)
    coord._device_grouping = DEVICE_GROUPING_SINGLE
    assert coord.single_device_tree is True


def test_coordinator_reads_option_from_options() -> None:
    """__init__ should read CONF_DEVICE_GROUPING from options."""
    coord = object.__new__(EconetDataCoordinator)
    options = {CONF_DEVICE_GROUPING: DEVICE_GROUPING_SINGLE}
    coord._device_grouping = options.get(CONF_DEVICE_GROUPING, DEVICE_GROUPING_SPLIT)
    assert coord.single_device_tree is True


# ---------------------------------------------------------------------------
# get_device_info_for_component
# ---------------------------------------------------------------------------
def test_component_split_produces_distinct_devices(
    supports_via_device_id: bool,
) -> None:
    """Split mode yields per-component devices connected via the controller."""
    api = _make_api()
    expected_identifiers = {
        COMPONENT_HUW: f"{api.uid}-huw",
        COMPONENT_LAMBDA: f"{api.uid}-lambda",
        COMPONENT_BUFFER: f"{api.uid}-buffer",
        COMPONENT_SOLAR: f"{api.uid}-solar",
    }

    for component, identifier in expected_identifiers.items():
        info = get_device_info_for_component(
            component, api, via_device_id=CONTROLLER_DEVICE_ID
        )
        assert _identifier(info) == identifier
        _assert_connected_via_controller(info, api, supports_via_device_id)


def test_component_split_mixer_has_index_and_parent(
    supports_via_device_id: bool,
) -> None:
    """Mixer split device uses the indexed identifier and the controller link."""
    api = _make_api()
    info = get_device_info_for_component(
        "mixer_2", api, via_device_id=CONTROLLER_DEVICE_ID
    )
    assert _identifier(info) == f"{api.uid}-mixer-2"
    _assert_connected_via_controller(info, api, supports_via_device_id)


def test_component_single_merges_into_one_device(
    supports_via_device_id: bool,
) -> None:
    """Single mode returns the main device identifier for every component."""
    api = _make_api()
    for component in (COMPONENT_HUW, COMPONENT_LAMBDA, COMPONENT_SOLAR, "mixer_3"):
        info = get_device_info_for_component(
            component, api, single_device=True, via_device_id=CONTROLLER_DEVICE_ID
        )
        assert _identifier(info) == api.uid
        assert "via_device" not in info
        assert "via_device_id" not in info


# ---------------------------------------------------------------------------
# Entity-level device_info
# ---------------------------------------------------------------------------
def test_econet_entity_split_uses_controller_device() -> None:
    """EconetEntity split device uses the bare controller uid."""
    api = _make_api()
    entity = object.__new__(EconetEntity)
    entity.api = api
    entity.coordinator = _coordinator(single=False)
    assert _identifier(_entity_device_info(EconetEntity, entity)) == api.uid


def test_mixer_entity_split_vs_single(supports_via_device_id: bool) -> None:
    """MixerEntity returns its own device when split, main when single."""
    api = _make_api()
    split = object.__new__(MixerEntity)
    split.api = api
    split._idx = 1
    split.coordinator = _coordinator(single=False)
    split_info = _entity_device_info(MixerEntity, split)
    assert _identifier(split_info) == f"{api.uid}-mixer-1"
    _assert_connected_via_controller(split_info, api, supports_via_device_id)

    single = object.__new__(MixerEntity)
    single.api = api
    single._idx = 1
    single.coordinator = _coordinator(single=True)
    assert _identifier(_entity_device_info(MixerEntity, single)) == api.uid


def test_lambda_entity_split_vs_single(supports_via_device_id: bool) -> None:
    """LambdaEntity returns its own device when split, main when single."""
    api = _make_api()
    split = object.__new__(LambdaEntity)
    split.api = api
    split.coordinator = _coordinator(single=False)
    split_info = _entity_device_info(LambdaEntity, split)
    assert _identifier(split_info) == f"{api.uid}-lambda"
    _assert_connected_via_controller(split_info, api, supports_via_device_id)

    single = object.__new__(LambdaEntity)
    single.api = api
    single.coordinator = _coordinator(single=True)
    assert _identifier(_entity_device_info(LambdaEntity, single)) == api.uid


def test_ecoster_entity_split_vs_single(supports_via_device_id: bool) -> None:
    """EcoSterEntity returns its own device when split, main when single."""
    api = _make_api()
    split = object.__new__(EcoSterEntity)
    split.api = api
    split._idx = 2
    split.coordinator = _coordinator(single=False)
    split_info = _entity_device_info(EcoSterEntity, split)
    assert _identifier(split_info) == f"{api.uid}-ecoster-2"
    _assert_connected_via_controller(split_info, api, supports_via_device_id)

    single = object.__new__(EcoSterEntity)
    single.api = api
    single._idx = 2
    single.coordinator = _coordinator(single=True)
    assert _identifier(_entity_device_info(EcoSterEntity, single)) == api.uid


@pytest.mark.parametrize(
    ("entity_class", "suffix"),
    [
        (ServiceParameterNumber, "service-parameters"),
        (AdvancedParameterNumber, "advanced-parameters"),
    ],
)
def test_parameter_device_connects_via_controller(
    supports_via_device_id: bool, entity_class: type, suffix: str
) -> None:
    """Service and advanced parameter devices share the controller details."""
    api = _make_api()
    entity = object.__new__(entity_class)
    entity.api = api
    entity.coordinator = _coordinator(single=False)
    info = _entity_device_info(entity_class, entity)
    assert _identifier(info) == f"{api.uid}-{suffix}"
    assert info["configuration_url"] == api.host
    assert info["sw_version"] == api.sw_rev
    _assert_connected_via_controller(info, api, supports_via_device_id)


# ---------------------------------------------------------------------------
# Schedule sensor device routing
# ---------------------------------------------------------------------------
def test_schedule_component_mapping() -> None:
    """Mixer/water-heater schedules map to their device component."""
    assert schedule_component("mixer_1") == "mixer_1"
    assert schedule_component("mixer_4") == "mixer_4"
    assert schedule_component("water_heater") == COMPONENT_HUW
    assert schedule_component("water_heater_2") == COMPONENT_HUW
    assert schedule_component("boiler") is None
    assert schedule_component("circulation_pump") is None


def test_schedule_calendar_routes_to_mixer_device() -> None:
    """A mixer schedule calendar is grouped under its mixer device when split."""
    api = _make_api()
    entity = object.__new__(EconetScheduleCalendar)
    entity.api = api
    entity._component = "mixer_1"
    entity.coordinator = _coordinator(single=False)
    assert (
        _identifier(_entity_device_info(EconetScheduleCalendar, entity))
        == f"{api.uid}-mixer-1"
    )


def test_schedule_calendar_without_component_uses_main_device() -> None:
    """A boiler-level schedule calendar stays on the controller device."""
    api = _make_api()
    entity = object.__new__(EconetScheduleCalendar)
    entity.api = api
    entity._component = None
    entity.coordinator = _coordinator(single=False)
    assert _identifier(_entity_device_info(EconetScheduleCalendar, entity)) == api.uid
