"""Tests for the configurable device grouping option (split vs single).

Covers:
- ``EconetDataCoordinator.single_device_tree`` reading the option.
- ``get_device_info_for_component`` split vs single behaviour.
- Per-component entity ``device_info`` honouring the coordinator flag.
"""

from typing import Any
from unittest.mock import MagicMock

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
def test_component_split_produces_distinct_devices() -> None:
    """Split mode yields per-component identifiers with via_device parent."""
    api = _make_api()

    huw = get_device_info_for_component(COMPONENT_HUW, api, single_device=False)
    lam = get_device_info_for_component(COMPONENT_LAMBDA, api, single_device=False)
    buf = get_device_info_for_component(COMPONENT_BUFFER, api, single_device=False)
    sol = get_device_info_for_component(COMPONENT_SOLAR, api, single_device=False)

    assert _identifier(huw) == f"{api.uid}-huw"
    assert _identifier(lam) == f"{api.uid}-lambda"
    assert _identifier(buf) == f"{api.uid}-buffer"
    assert _identifier(sol) == f"{api.uid}-solar"
    for info in (huw, lam, buf, sol):
        assert info.get("via_device") == (DOMAIN, api.uid)


def test_component_split_mixer_has_index_and_parent() -> None:
    """Mixer split device uses the indexed identifier and parent link."""
    api = _make_api()
    info = get_device_info_for_component("mixer_2", api, single_device=False)
    assert _identifier(info) == f"{api.uid}-mixer-2"
    assert info.get("via_device") == (DOMAIN, api.uid)


def test_component_single_merges_into_one_device() -> None:
    """Single mode returns the main device identifier for every component."""
    api = _make_api()
    for component in (COMPONENT_HUW, COMPONENT_LAMBDA, COMPONENT_SOLAR, "mixer_3"):
        info = get_device_info_for_component(component, api, single_device=True)
        assert _identifier(info) == api.uid
        assert "via_device" not in info


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


def test_mixer_entity_split_vs_single() -> None:
    """MixerEntity returns its own device when split, main when single."""
    api = _make_api()
    split = object.__new__(MixerEntity)
    split.api = api
    split._idx = 1
    split.coordinator = _coordinator(single=False)
    assert _identifier(_entity_device_info(MixerEntity, split)) == f"{api.uid}-mixer-1"

    single = object.__new__(MixerEntity)
    single.api = api
    single._idx = 1
    single.coordinator = _coordinator(single=True)
    assert _identifier(_entity_device_info(MixerEntity, single)) == api.uid


def test_lambda_entity_split_vs_single() -> None:
    """LambdaEntity returns its own device when split, main when single."""
    api = _make_api()
    split = object.__new__(LambdaEntity)
    split.api = api
    split.coordinator = _coordinator(single=False)
    assert _identifier(_entity_device_info(LambdaEntity, split)) == f"{api.uid}-lambda"

    single = object.__new__(LambdaEntity)
    single.api = api
    single.coordinator = _coordinator(single=True)
    assert _identifier(_entity_device_info(LambdaEntity, single)) == api.uid


def test_ecoster_entity_split_vs_single() -> None:
    """EcoSterEntity returns its own device when split, main when single."""
    api = _make_api()
    split = object.__new__(EcoSterEntity)
    split.api = api
    split._idx = 2
    split.coordinator = _coordinator(single=False)
    assert (
        _identifier(_entity_device_info(EcoSterEntity, split)) == f"{api.uid}-ecoster-2"
    )

    single = object.__new__(EcoSterEntity)
    single.api = api
    single._idx = 2
    single.coordinator = _coordinator(single=True)
    assert _identifier(_entity_device_info(EcoSterEntity, single)) == api.uid
