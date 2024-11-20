"""Common code for econet300 integration."""

import asyncio
from datetime import timedelta
import logging

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import ApiError, AuthError, Econet300Api
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class EconetDataCoordinator(DataUpdateCoordinator):
    """Econet data coordinator."""

    def __init__(self, hass, api: Econet300Api):
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=30),
        )
        self._api = api

    def has_data(self, key: str):
        """Check if datakey is present in data."""
        if self.data is None:
            return False

        has_key = key in self.data["sysParams"] or self.data["regParams"]
        _LOGGER.debug("has_data: %s=%s", key, has_key)
        return has_key

    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """

        _LOGGER.debug("Fetching data from API")

        try:
            # Note: asyncio.TimeoutError and aiohttp.ClientError are already
            # handled by the data update coordinator.
            async with asyncio.timeout(10):
                data = (
                    await self._api.fetch_sys_params()
                    if self._api.model_id == "MAX810P-L TOUCH"
                    else {}
                )
                reg_params = await self._api.fetch_reg_params()
                return {"sysParams": data, "regParams": reg_params}
        except AuthError as err:
            raise ConfigEntryAuthFailed from err
        except ApiError as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
