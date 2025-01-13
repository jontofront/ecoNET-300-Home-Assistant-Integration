"""Common code for econet300 integration."""

from __future__ import annotations

import asyncio
from datetime import timedelta
import logging
from typing import Any

from aiohttp import ClientError
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import ApiError, AuthError, Econet300Api
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


def should_skip_params_edits(sys_params: dict[str, Any]) -> bool:
    """Determine whether paramsEdits should be skipped based on controllerID."""
    controller_id = sys_params.get("controllerID")
    if controller_id == "ecoMAX360i":
        _LOGGER.info("Skipping paramsEdits due to controllerID: %s", controller_id)
        return True
    return False


class EconetDataCoordinator(DataUpdateCoordinator):
    """Econet data coordinator to handle data updates."""

    def __init__(self, hass, api: Econet300Api) -> None:
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_data_coordinator",
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=30),
        )
        self._api = api

    def has_sys_data(self, key: str) -> bool:
        """Check if data key is present in sysParams."""
        if self.data is None:
            return False
        return key in self.data["sysParams"]

    def has_reg_data(self, key: str) -> bool:
        """Check if data key is present in regParams."""
        if self.data is None:
            return False

        return key in self.data["regParams"]

    def has_param_edit_data(self, key: str) -> bool:
        """Check if ."""
        if self.data is None:
            return False

        return key in self.data["paramsEdits"]

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API endpoint."""

        _LOGGER.debug("Fetching data from API")

        try:
            async with asyncio.timeout(10):
                # Fetch system parameters from ../econet/sysParams
                sys_params = await self._api.fetch_sys_params()

                # Determine whether to fetch paramsEdits from ../econet/rmCurrentDataParamsEdits
                if should_skip_params_edits(sys_params):
                    params_edits = {}
                else:
                    params_edits = await self._api.fetch_param_edit_data()

                # Fetch regular parameters from ../econet/regParams
                reg_params = await self._api.fetch_reg_params()

                return {
                    "sysParams": sys_params,
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
