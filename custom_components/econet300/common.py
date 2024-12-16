"""Common code for econet300 integration."""

import asyncio
from datetime import timedelta
import logging

from aiohttp import ClientError
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

    def has_sys_data(self, key: str):
        """Check if data key is present in sysParams."""
        if self.data is None:
            return False
        return key in self.data["sysParams"]

    def has_reg_data(self, key: str):
        """Check if data key is present in regParams."""
        if self.data is None:
            return False

        return key in self.data["regParams"]

    def has_param_edit_data(self, key: str):
        """Check if ."""
        if self.data is None:
            return False

        return key in self.data["paramsEdits"]

    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """

        _LOGGER.debug("Fetching data from API")

        try:
            # Note: asyncio.TimeoutError and aiohttp.ClientError are already
            # handled by the data update coordinator.
            async with asyncio.timeout(20):
                data = await self._api.fetch_sys_params()
                reg_params = await self._api.fetch_reg_params()
                params_edits = await self._api.fetch_param_edit_data()
                return {
                    "sysParams": data,
                    "regParams": reg_params,
                    "paramsEdits": params_edits,
                }
        except AuthError as err:
            _LOGGER.error("Authentication error: %s", err)
            raise ConfigEntryAuthFailed from err
        except ApiError as err:
            _LOGGER.error("API error: %s", err)
            raise UpdateFailed(f"Error communicating with API: {err}") from err
        except (asyncio.TimeoutError, ClientError) as err:
            _LOGGER.error("Timeout or client error: %s", err)
            raise UpdateFailed(f"Timeout or client error: {err}") from err
