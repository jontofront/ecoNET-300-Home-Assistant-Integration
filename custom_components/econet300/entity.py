"""Base econet entity class."""

import logging

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

        value = self.coordinator.data["sysParams"].get(self.entity_description.key)
        if value is None:
            _LOGGER.debug("Value for key %s is None", self.entity_description.key)
            return
        self._sync_state(value)

    async def async_added_to_hass(self):
        """Handle added to hass."""
        _LOGGER.debug("Entering async_added_to_hass method")
        _LOGGER.debug("Added to HASS: %s", self.entity_description)
        _LOGGER.debug("Coordinator: %s", self.coordinator)

        _LOGGER.debug("Added to HASS: %s", self.entity_description.name)

        if "data" not in dir(self.coordinator):
            _LOGGER.error("Coordinator object does not have a 'data' attribute")
            return

        if (
            not self.coordinator.has_sys_data(self.entity_description.key)
            or self.coordinator.data["sysParams"].get(self.entity_description.key)
            is None
        ):
            _LOGGER.warning(
                "Data key: %s was expected to exist but it doesn't",
                self.entity_description.key,
            )
            _LOGGER.debug(
                "Coordinator available data: %s", self.coordinator.data["sysParams"]
            )

            _LOGGER.debug("Exiting async_added_to_hass method")
            return

        value = self.coordinator.data["sysParams"].get(self.entity_description.key)

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
