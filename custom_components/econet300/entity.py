"""Base econet entity class."""

import logging
from typing import Any

from homeassistant.core import callback
from homeassistant.helpers.entity import DeviceInfo, EntityDescription
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api import Econet300Api
from .common import EconetDataCoordinator
from .const import (
    DEVICE_INFO_CONTROLLER_NAME,
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

    @property
    def has_entity_name(self):
        """Return if the name of the entity is describing only the entity itself."""
        return True

    @property
    def unique_id(self) -> str | None:
        """Return the unique_id of the entity."""
        if not self.api.uid:
            _LOGGER.error(
                "API UID is missing for entity: %s", self.entity_description.key
            )
            return None
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

    def _get_value(self, expected_key: str) -> Any:
        """Retrieve the value for the expected key from sysParams or regParams."""
        sys_params = self.coordinator.data.get("sysParams", {})
        reg_params = self.coordinator.data.get("regParams", {})
        if expected_key in sys_params:
            return sys_params[expected_key]
        if expected_key in reg_params:
            return reg_params[expected_key]
        return None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        _LOGGER.debug(
            "Update EconetEntity, entity name: %s", self.entity_description.name
        )

        value = self._get_value(self.entity_description.key)
        if value is None:
            _LOGGER.debug("Value for key %s is None", self.entity_description.key)
            return
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

        # # Check the expected key and retrieve the value entity_description
        expected_key = self.entity_description.key
        _LOGGER.debug("Expected key: %s", expected_key)

        # Retrieve the value from sysParams or regParams
        value = self._get_value(expected_key)
        if value is None:
            sys_keys = self.coordinator.data.get("sysParams", {}).keys()
            reg_keys = self.coordinator.data.get("regParams", {}).keys()
            _LOGGER.warning(
                "Data key: %s was expected to exist but it doesn't. Available sysParams keys: %s, regParams keys: %s",
                expected_key,
                list(sys_keys),
                list(reg_keys),
            )
            return

        _LOGGER.debug("Retrieved value for key %s: %s", expected_key, value)

        # Synchronize with HASS
        await super().async_added_to_hass()
        self._sync_state(value)


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
        super().__init__(description, coordinator, api)

        self._idx = idx

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
