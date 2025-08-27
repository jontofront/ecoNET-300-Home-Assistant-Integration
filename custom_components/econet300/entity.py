"""Base econet entity class."""

import logging

from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api import Econet300Api
from .common import EconetDataCoordinator
from .const import (
    DEVICE_INFO_CONTROLLER_NAME,
    DEVICE_INFO_ECOSTER_NAME,
    DEVICE_INFO_LAMBDA_NAME,
    DEVICE_INFO_MANUFACTURER,
    DEVICE_INFO_MIXER_NAME,
    DEVICE_INFO_MODEL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class EconetEntity(CoordinatorEntity):
    """Represents EconetEntity."""

    api: Econet300Api
    entity_description: EntityDescription

    def __init__(self, coordinator: EconetDataCoordinator, api: Econet300Api):
        """Initialize the EconetEntity."""
        super().__init__(coordinator)
        self.api = api

    @property
    def has_entity_name(self):
        """Return if the name of the entity is describing only the entity itself."""
        return True

    @property
    def unique_id(self) -> str | None:
        """Return the unique_id of the entity."""
        return f"{self.api.uid}-{self.entity_description.key}"

    @property
    def device_info(self) -> DeviceInfo | None:
        """Return device info of the entity."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.api.uid)},
            name=DEVICE_INFO_CONTROLLER_NAME,
            manufacturer=DEVICE_INFO_MANUFACTURER,
            model=DEVICE_INFO_MODEL,
            model_id=self.api.model_id,
            configuration_url=self.api.host,
            sw_version=self.api.sw_rev,
            hw_version=self.api.hw_ver,
        )

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug(
            "Update EconetEntity, entity name: %s", self.entity_description.name
        )

        # Safety check: ensure coordinator data exists
        if self.coordinator.data is None:
            _LOGGER.info("Coordinator data is None, skipping update")
            return

        # Debug: Check what's available in each data source
        sys_params = self.coordinator.data.get("sysParams", {})
        reg_params = self.coordinator.data.get("regParams", {})
        params_edits = self.coordinator.data.get("paramsEdits", {})

        # Safety check: ensure all data sources are always dicts
        if sys_params is None:
            sys_params = {}
            _LOGGER.info("sysParams was None, defaulting to empty dict")
        if reg_params is None:
            reg_params = {}
            _LOGGER.info("regParams was None, defaulting to empty dict")
        if params_edits is None:
            params_edits = {}
            _LOGGER.info("paramsEdits was None, defaulting to empty dict")

        _LOGGER.debug(
            "DEBUG: Looking for key '%s' in data sources - sysParams: %s, regParams: %s, paramsEdits: %s",
            self.entity_description.key,
            self.entity_description.key in sys_params,
            self.entity_description.key in reg_params,
            self.entity_description.key in params_edits,
        )

        value = None
        if self.entity_description.key in sys_params:
            value = sys_params[self.entity_description.key]
            _LOGGER.debug("DEBUG: Found in sysParams: %s", value)
        elif self.entity_description.key in reg_params:
            value = reg_params[self.entity_description.key]
            _LOGGER.debug("DEBUG: Found in regParams: %s", value)
        elif self.entity_description.key in params_edits:
            value = params_edits[self.entity_description.key]
            _LOGGER.debug("DEBUG: Found in paramsEdits: %s", value)

        if value is None:
            _LOGGER.debug("Value for key %s is None", self.entity_description.key)
            return

        _LOGGER.debug(
            "Updating state for key: %s with value: %s",
            self.entity_description.key,
            value,
        )
        # Call _sync_state to update entity state
        self._sync_state(value)

    async def async_added_to_hass(self):
        """Handle added to hass."""
        _LOGGER.debug("Entering async_added_to_hass method")
        _LOGGER.debug("Added to HASS: %s", self.entity_description)
        _LOGGER.debug("Coordinator: %s", self.coordinator)

        # Check if the coordinator has a 'data' attributes
        if "data" not in dir(self.coordinator):
            _LOGGER.error("Coordinator object does not have a 'data' attribute")
            return

        # Safety check: ensure coordinator data exists
        if self.coordinator.data is None:
            _LOGGER.info("Coordinator data is None, skipping setup")
            return

        # Retrieve sysParams and regParams paramsEdits data
        sys_params = self.coordinator.data.get("sysParams", {})
        reg_params = self.coordinator.data.get("regParams", {})
        params_edits = self.coordinator.data.get("paramsEdits", {})

        # Safety check: ensure all data sources are always dicts
        if sys_params is None:
            sys_params = {}
            _LOGGER.info(
                "async_added_to_hass: sysParams was None, defaulting to empty dict"
            )
        if reg_params is None:
            reg_params = {}
            _LOGGER.info(
                "async_added_to_hass: regParams was None, defaulting to empty dict"
            )
        if params_edits is None:
            params_edits = {}
            _LOGGER.info(
                "async_added_to_hass: paramsEdits was None, defaulting to empty dict"
            )
        _LOGGER.debug("async_sysParams: %s", sys_params)
        _LOGGER.debug("async_regParams: %s", reg_params)
        _LOGGER.debug("async_paramsEdits: %s", params_edits)

        # Check the available keys in all sources
        sys_keys = sys_params.keys() if sys_params is not None else []
        reg_keys = reg_params.keys() if reg_params is not None else []
        edit_keys = params_edits.keys() if params_edits is not None else []
        _LOGGER.debug("Available keys in sysParams: %s", sys_keys)
        _LOGGER.debug("Available keys in regParams: %s", reg_keys)
        _LOGGER.debug("Available keys in paramsEdits: %s", edit_keys)

        # Expected key from entity_description
        expected_key = self.entity_description.key
        _LOGGER.debug("Expected key: %s", expected_key)

        # Retrieve the value from sysParams or regParams  or paramsEdits
        value = (
            sys_params.get(expected_key)
            if sys_params.get(expected_key) is not None
            else (
                reg_params.get(expected_key)
                if reg_params.get(expected_key) is not None
                else params_edits.get(expected_key)
            )
        )

        if value is not None:
            _LOGGER.debug("Found key '%s' with value: %s", expected_key, value)
        else:
            _LOGGER.info(
                "Data key: %s was expected to exist but it doesn't. Available sysParams keys: %s, regParams keys: %s, paramsEdits keys: %s",
                expected_key,
                sys_keys,
                reg_keys,
                edit_keys,
            )
            return

        # Synchronize with HASS
        await super().async_added_to_hass()
        # Call _sync_state to update entity state
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
        return DeviceInfo(
            identifiers={(DOMAIN, f"{self.api.uid}-mixer-{self._idx}")},
            name=f"{DEVICE_INFO_MIXER_NAME}{self._idx}",
            manufacturer=DEVICE_INFO_MANUFACTURER,
            model=DEVICE_INFO_MODEL,
            model_id=self.api.model_id,
            configuration_url=self.api.host,
            sw_version=self.api.sw_rev,
            via_device=(DOMAIN, self.api.uid),
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
        return DeviceInfo(
            identifiers={(DOMAIN, f"{self.api.uid}lambda")},
            name=f"{DEVICE_INFO_LAMBDA_NAME}",
            manufacturer=DEVICE_INFO_MANUFACTURER,
            model=DEVICE_INFO_MODEL,
            configuration_url=self.api.host,
            sw_version=self.api.sw_rev,
            via_device=(DOMAIN, self.api.uid),
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
        return DeviceInfo(
            identifiers={(DOMAIN, f"{self.api.uid}-ecoster-{self._idx}")},
            name=f"{DEVICE_INFO_ECOSTER_NAME} {self._idx}",
            manufacturer=DEVICE_INFO_MANUFACTURER,
            model=DEVICE_INFO_MODEL,
            model_id=self.api.model_id,
            configuration_url=self.api.host,
            sw_version=self.api.sw_rev,
            via_device=(DOMAIN, self.api.uid),
        )
