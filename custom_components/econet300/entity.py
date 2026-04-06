"""Base econet entity class."""

import logging
from typing import Any

from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api import Econet300Api
from .common import EconetDataCoordinator
from .const import (
    COMPONENT_BOILER,
    COMPONENT_BUFFER,
    COMPONENT_HUW,
    COMPONENT_LAMBDA,
    COMPONENT_SOLAR,
    DEVICE_INFO_BUFFER_NAME,
    DEVICE_INFO_CONTROLLER_NAME,
    DEVICE_INFO_ECOSTER_NAME,
    DEVICE_INFO_HUW_NAME,
    DEVICE_INFO_LAMBDA_NAME,
    DEVICE_INFO_MANUFACTURER,
    DEVICE_INFO_MIXER_NAME,
    DEVICE_INFO_MODEL,
    DEVICE_INFO_SOLAR_NAME,
    DOMAIN,
    EDIT_PARAMS_DATA_SENSOR_MAP,
    INFORMATION_PARAMS_SENSOR_MAP,
)

_LOGGER = logging.getLogger(__name__)


def _create_base_device_info(
    api: Econet300Api,
    identifier: str,
    name: str,
    parent_device_id: str | None = None,
    include_model_id: bool = False,
    include_hw_version: bool = False,
) -> DeviceInfo:
    """Create base DeviceInfo with common fields.

    Args:
        api: Econet300Api instance
        identifier: Unique device identifier
        name: Device display name
        parent_device_id: Parent device identifier for via_device
        include_model_id: Whether to include model_id
        include_hw_version: Whether to include hw_version

    Returns:
        DeviceInfo with common fields populated

    """
    # Build base device info - always present fields
    info = DeviceInfo(
        identifiers={(DOMAIN, identifier)},
        name=name,
        manufacturer=DEVICE_INFO_MANUFACTURER,
        model=DEVICE_INFO_MODEL,
        configuration_url=api.host,
        sw_version=api.sw_rev,
    )
    # Add optional fields only when they have values
    if parent_device_id:
        info["via_device"] = (DOMAIN, parent_device_id)
    if include_model_id:
        info["model_id"] = api.model_id
    if include_hw_version:
        info["hw_version"] = api.hw_ver
    return info


class EconetEntity(CoordinatorEntity):
    """Represents EconetEntity."""

    api: Econet300Api
    _attr_has_entity_name = True  # Required for icon translations from icons.json
    # Note: entity_description type is defined by child classes (NumberEntity, SensorEntity, etc.)
    # to avoid MRO conflicts when multiple inheritance is used

    def __init__(self, coordinator: EconetDataCoordinator, api: Econet300Api):
        """Initialize the EconetEntity."""
        super().__init__(coordinator)
        self.api = api

    @property
    def unique_id(self) -> str | None:
        """Return the unique_id of the entity."""
        return f"{self.api.uid}-{self.entity_description.key}"

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device info of the entity."""
        return _create_base_device_info(
            api=self.api,
            identifier=self.api.uid,
            name=DEVICE_INFO_CONTROLLER_NAME,
            include_model_id=True,
            include_hw_version=True,
        )

    def _get_param_data(self) -> dict | None:
        """Get parameter data from mergedData for this entity.

        Looks up parameter data using either self._param_id (instance attribute)
        or self.entity_description.param_id, handling both string and int keys.

        Returns:
            Parameter data dict if found, None otherwise

        """
        if self.coordinator.data is None:
            return None
        merged_data = self.coordinator.data.get("mergedData", {})
        if not merged_data:
            return None
        merged_parameters = merged_data.get("parameters", {})
        if not merged_parameters:
            return None

        # Try instance _param_id first, then entity_description.param_id
        param_id = getattr(self, "_param_id", None) or getattr(
            self.entity_description, "param_id", None
        )
        if not param_id:
            return None

        # Try direct lookup, then string/int conversion
        if param_id in merged_parameters:
            return merged_parameters[param_id]
        if str(param_id).isdigit():
            return merged_parameters.get(str(param_id)) or merged_parameters.get(
                int(param_id)
            )
        return None

    def _is_parameter_locked(self) -> bool:
        """Check if the parameter is locked."""
        param_data = self._get_param_data()
        return param_data.get("locked", False) if param_data else False

    def _get_lock_reason(self) -> str | None:
        """Get the lock reason for the parameter."""
        param_data = self._get_param_data()
        return param_data.get("lock_reason") if param_data else None

    def _get_description(self) -> str | None:
        """Get the description for the parameter."""
        param_data = self._get_param_data()
        return param_data.get("description") if param_data else None

    def _get_data_sources(self) -> tuple[dict, dict, dict, dict, dict, dict]:
        """Get all data sources with safe defaults."""
        data = self.coordinator.data or {}
        return (
            data.get("sysParams") or {},
            data.get("regParams") or {},
            data.get("paramsEdits") or {},
            data.get("mergedData") or {},
            data.get("editParams") or {},
            data.get("informationParams") or {},
        )

    def _lookup_value(self) -> Any:
        """Look up value from appropriate data source.

        For dynamic entities (with param_id), looks up in mergedData.
        For legacy entities, looks up in sysParams, regParams, paramsEdits,
        then editParams.data and informationParams (ecoMAX360i).

        Returns:
            The value if found, None otherwise.

        """
        (
            sys_params,
            reg_params,
            params_edits,
            merged_data,
            edit_params,
            information_params,
        ) = self._get_data_sources()
        param_id = getattr(self.entity_description, "param_id", None)

        if param_id:
            # Dynamic entity lookup in mergedData
            params = merged_data.get("parameters", {})
            param_data = params.get(param_id) or params.get(str(param_id))
            return param_data.get("value") if param_data else None

        # Legacy entity lookup - check each source in order
        key = self.entity_description.key
        if key in sys_params:
            return sys_params[key]
        if key in reg_params:
            return reg_params[key]
        if key in params_edits:
            return params_edits[key]

        # editParams.data lookup (ecoMAX360i sensors by parameter ID)
        edit_param_id = EDIT_PARAMS_DATA_SENSOR_MAP.get(key)
        if edit_param_id and edit_param_id in edit_params:
            entry = edit_params[edit_param_id]
            return entry.get("value") if isinstance(entry, dict) else entry

        # informationParams lookup (ecoMAX360i read-only status sensors)
        info_param_id = INFORMATION_PARAMS_SENSOR_MAP.get(key)
        if info_param_id and info_param_id in information_params:
            info_data = information_params[info_param_id]
            if isinstance(info_data, list) and len(info_data) > 1:
                inner = info_data[1]
                if isinstance(inner, list) and len(inner) > 0:
                    return inner[0][0]

        return None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        if self.coordinator.data is None:
            return

        value = self._lookup_value()
        if value is None:
            _LOGGER.debug(
                "No value for key %s, skipping update", self.entity_description.key
            )
            return

        self._sync_state(value)

    async def async_added_to_hass(self) -> None:
        """Handle entity added to Home Assistant."""
        # Always register for coordinator updates first
        await super().async_added_to_hass()

        # Skip initial sync if no data available yet
        if self.coordinator.data is None:
            _LOGGER.debug(
                "No coordinator data for %s, will update on next refresh",
                self.entity_description.key,
            )
            return

        # Sync initial value if available
        value = self._lookup_value()
        if value is not None:
            self._sync_state(value)

    def _sync_state(self, value) -> None:
        """Update entity state with the provided value.

        This method is called when the coordinator provides new data.
        Child classes should override this to handle entity-specific state updates.
        """
        # Base implementation does nothing - child classes handle state updates


class MixerEntity(EconetEntity):
    """Represents MixerEntity."""

    def __init__(
        self,
        description: EntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
        idx: int,
    ):
        """Initialize the MixerEntity."""
        self.entity_description = description
        self.api = api
        self._idx = idx
        super().__init__(coordinator, api)

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device info of the entity."""
        return _create_base_device_info(
            api=self.api,
            identifier=f"{self.api.uid}-mixer-{self._idx}",
            name=f"{DEVICE_INFO_MIXER_NAME}{self._idx}",
            parent_device_id=self.api.uid,
            include_model_id=True,
        )


class LambdaEntity(EconetEntity):
    """Initialize the LambdaEntity."""

    def __init__(
        self,
        description: EntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
    ):
        """Initialize the LambdaEntity."""
        self.entity_description = description
        self.api = api
        super().__init__(coordinator, api)

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device info of the entity."""
        return _create_base_device_info(
            api=self.api,
            identifier=f"{self.api.uid}-lambda",
            name=DEVICE_INFO_LAMBDA_NAME,
            parent_device_id=self.api.uid,
        )


class EcoSterEntity(EconetEntity):
    """Represents EcoSterEntity."""

    def __init__(
        self,
        description: EntityDescription,
        coordinator: EconetDataCoordinator,
        api: Econet300Api,
        idx: int,
    ):
        """Initialize the EcoSterEntity."""
        self.entity_description = description
        self.api = api
        self._idx = idx
        super().__init__(coordinator, api)

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device info of the entity."""
        return _create_base_device_info(
            api=self.api,
            identifier=f"{self.api.uid}-ecoster-{self._idx}",
            name=f"{DEVICE_INFO_ECOSTER_NAME} {self._idx}",
            parent_device_id=self.api.uid,
            include_model_id=True,
        )


# Component configuration for device info creation
_COMPONENT_CONFIG: dict[str, dict[str, Any]] = {
    COMPONENT_BOILER: {
        "suffix": "",
        "name": DEVICE_INFO_CONTROLLER_NAME,
        "include_model_id": True,
        "include_hw_version": True,
    },
    COMPONENT_HUW: {
        "suffix": "-huw",
        "name": DEVICE_INFO_HUW_NAME,
    },
    COMPONENT_LAMBDA: {
        "suffix": "-lambda",
        "name": DEVICE_INFO_LAMBDA_NAME,
    },
    COMPONENT_BUFFER: {
        "suffix": "-buffer",
        "name": DEVICE_INFO_BUFFER_NAME,
    },
    COMPONENT_SOLAR: {
        "suffix": "-solar",
        "name": DEVICE_INFO_SOLAR_NAME,
    },
}


def get_device_info_for_component(
    component: str, api: Econet300Api, mixer_idx: int | None = None
) -> DeviceInfo:
    """Return DeviceInfo for a specific component.

    Args:
        component: Component identifier (COMPONENT_BOILER, COMPONENT_HUW, etc.)
        api: Econet300Api instance for device information
        mixer_idx: Optional mixer index (1-4) for mixer components

    Returns:
        DeviceInfo for the specified component

    """
    # Handle mixer special case
    if component.startswith("mixer_"):
        idx = mixer_idx or int(component.split("_")[1])
        return _create_base_device_info(
            api,
            f"{api.uid}-mixer-{idx}",
            f"{DEVICE_INFO_MIXER_NAME}{idx}",
            parent_device_id=api.uid,
            include_model_id=True,
        )

    # Use mapping for standard components, default to boiler config
    config = _COMPONENT_CONFIG.get(component, _COMPONENT_CONFIG[COMPONENT_BOILER])
    suffix = config.get("suffix", "")
    identifier = f"{api.uid}{suffix}" if suffix else api.uid
    parent = api.uid if suffix else None

    return _create_base_device_info(
        api,
        identifier,
        config["name"],
        parent_device_id=parent,
        include_model_id=config.get("include_model_id", False),
        include_hw_version=config.get("include_hw_version", False),
    )
