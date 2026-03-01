"""Common code for econet300 integration."""

from __future__ import annotations

import asyncio
from datetime import timedelta
import logging
from typing import Any

import aiohttp
from aiohttp import ClientError
from homeassistant.config_entries import ConfigEntry
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.issue_registry import (
    IssueSeverity,
    async_create_issue,
    async_delete_issue,
)
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import ApiError, AuthError, Econet300Api
from .const import (
    CONSECUTIVE_FAILURES_THRESHOLD,
    DOMAIN,
    ECOSOL_CONTROLLER_IDS,
    RM_ADDITIONAL_DATASET_KEYS,
    RM_CORE_DATASET_KEYS,
)

_LOGGER = logging.getLogger(__name__)


def skip_params_edits(sys_params: dict[str, Any] | None) -> bool:
    """Determine whether paramsEdits should be skipped based on controllerID."""
    if sys_params is None:
        return False
    controller_id = sys_params.get("controllerID")

    # Controllers that don't support rmCurrentDataParamsEdits endpoint
    unsupported_controllers = {
        "ecoMAX360i",  # Known to not support the endpoint
        *ECOSOL_CONTROLLER_IDS,  # All ecoSOL controllers don't support this endpoint
        "ecoSter",  # ecoSter controllers
        "SControl MK1",  # SControl controllers
    }

    if controller_id in unsupported_controllers:
        _LOGGER.info(
            "Skipping paramsEdits due to controllerID: %s (endpoint not supported)",
            controller_id,
        )
        return True

    # Log which controllers do support the endpoint
    _LOGGER.debug("Controller %s supports paramsEdits endpoint", controller_id)
    return False


class EconetDataCoordinator(DataUpdateCoordinator):
    """Econet data coordinator to handle data updates."""

    def __init__(
        self,
        hass,
        api: Econet300Api,
        config_entry: ConfigEntry,
        options: dict[str, Any] | None = None,
    ) -> None:
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_data_coordinator",
            # Polling interval. Will only be polled if there are subscribers.
            # 60 seconds is reasonable for heating systems - reduces API load by 50%
            update_interval=timedelta(seconds=60),
        )
        self._api = api
        self._config_entry = config_entry
        self._options = options or {}
        self._consecutive_failures = 0
        self._rm_supported: bool | None = None

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
        """Check if parameter edit data key is present in paramsEdits."""
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
                if sys_params is None or skip_params_edits(sys_params):
                    params_edits = {}
                else:
                    params_edits = await self._api.fetch_param_edit_data()

                # Fetch regular parameters from ../econet/regParams
                reg_params = await self._api.fetch_reg_params()

                # Fetch regParamsData from ../econet/regParamsData
                reg_params_data = await self._api.fetch_reg_params_data()

                # Probe once whether RM API is supported (legacy-only modules return 404/timeout)
                if self._rm_supported is None:
                    self._rm_supported = await self._api.probe_rm_support()
                    if not self._rm_supported:
                        _LOGGER.info(
                            "RM endpoint not available (legacy-only module), skipping merged data"
                        )

                if self._rm_supported:
                    # Fetch RM... endpoint data for enhanced functionality
                    rm_data = await self._fetch_rm_endpoint_data()
                    # Fetch merged parameter data for dynamic entities
                    merged_data = None
                    try:
                        merged_data = await self._api.fetch_merged_rm_data(
                            sys_params=sys_params,
                        )
                        _LOGGER.info(
                            "Coordinator fetched merged data: %s parameters",
                            len(merged_data.get("parameters", {})) if merged_data else 0,
                        )
                    except (aiohttp.ClientError, asyncio.TimeoutError, ValueError) as e:
                        _LOGGER.warning(
                            "Failed to fetch merged parameter data in coordinator: %s", e
                        )
                else:
                    rm_data = {}
                    merged_data = None

                # Build currentDataMerged: join rmCurrentDataParams metadata
                # with live values from regParamsData (same numeric ID space).
                current_data_merged: dict[str, dict] = {}
                current_data_params = (
                    rm_data.get("currentDataParams", {}) if rm_data else {}
                )
                if current_data_params and reg_params_data:
                    for param_id, metadata in current_data_params.items():
                        if not isinstance(metadata, dict):
                            continue
                        current_data_merged[param_id] = {
                            "name": metadata.get("name", ""),
                            "unit": metadata.get("unit", 0),
                            "special": metadata.get("special", 0),
                            "value": reg_params_data.get(param_id),
                        }
                    _LOGGER.debug(
                        "Built currentDataMerged with %d parameters",
                        len(current_data_merged),
                    )

                result = {
                    "sysParams": sys_params,
                    "regParams": reg_params,
                    "regParamsData": reg_params_data,
                    "paramsEdits": params_edits,
                    "rmData": rm_data,
                    "mergedData": merged_data,
                    "currentDataMerged": current_data_merged,
                }

                # Debug: Log merged data structure
                if merged_data and "parameters" in merged_data:
                    param_keys = list(merged_data["parameters"].keys())[
                        :5
                    ]  # First 5 keys
                    _LOGGER.debug(
                        "Coordinator merged data keys (first 5): %s", param_keys
                    )

                # Success - reset failure counter and remove any repair issue
                self._on_successful_update()

                return result
        except AuthError as err:
            _LOGGER.error("Authentication error: %s", err)
            raise ConfigEntryAuthFailed from err
        except ApiError as err:
            _LOGGER.error("API error: %s", err)
            self._on_failed_update()
            raise UpdateFailed(f"Error communicating with API: {err}") from err
        except (asyncio.TimeoutError, ClientError) as err:
            _LOGGER.warning("Connection failed (device offline?): %s", err)
            self._on_failed_update()
            raise UpdateFailed(f"Connection failed: {err}") from err

    def _on_successful_update(self) -> None:
        """Handle successful data update - reset failure counter and remove repair issue."""
        if self._consecutive_failures > 0:
            _LOGGER.debug(
                "Connection restored after %d failures", self._consecutive_failures
            )
            self._consecutive_failures = 0
            # Remove the repair issue if it exists
            async_delete_issue(
                self.hass, DOMAIN, f"connection_failed_{self._config_entry.entry_id}"
            )

    def _on_failed_update(self) -> None:
        """Handle failed data update - increment counter and create repair issue if threshold reached."""
        self._consecutive_failures += 1
        _LOGGER.debug("Consecutive connection failures: %d", self._consecutive_failures)

        if self._consecutive_failures >= CONSECUTIVE_FAILURES_THRESHOLD:
            host = self._config_entry.data.get("host", "unknown")
            async_create_issue(
                self.hass,
                DOMAIN,
                f"connection_failed_{self._config_entry.entry_id}",
                is_fixable=True,
                is_persistent=True,
                severity=IssueSeverity.ERROR,
                translation_key="connection_failed",
                translation_placeholders={
                    "host": host,
                    "failures": str(self._consecutive_failures),
                },
            )

    async def _fetch_rm_endpoint_data(self) -> dict[str, Any]:
        """Fetch data from RM... endpoints for enhanced functionality."""
        rm_data: dict[str, Any] = {}

        try:
            # Fetch core RM data in parallel
            core_tasks = [
                self._api.fetch_rm_current_data_params(),
                self._api.fetch_rm_params_names(),
                self._api.fetch_rm_params_data(),
                self._api.fetch_rm_langs(),
            ]
            core_results = await asyncio.gather(*core_tasks, return_exceptions=True)

            # Process core results using mapping
            for index, key in enumerate(RM_CORE_DATASET_KEYS):
                result = core_results[index]
                rm_data[key] = {} if isinstance(result, Exception) else result
                if isinstance(result, Exception):
                    _LOGGER.warning("Failed to fetch %s: %s", key, result)

            # Only fetch additional data if core data was successful
            if rm_data["currentDataParams"]:
                additional_tasks = [
                    self._api.fetch_rm_params_descs(),
                    self._api.fetch_rm_params_enums(),
                    self._api.fetch_rm_alarms_names(),
                ]
                additional_results = await asyncio.gather(
                    *additional_tasks, return_exceptions=True
                )

                # Process additional results using mapping
                for index, key in enumerate(RM_ADDITIONAL_DATASET_KEYS):
                    result = additional_results[index]
                    rm_data[key] = {} if isinstance(result, Exception) else result
                    if isinstance(result, Exception):
                        _LOGGER.warning("Failed to fetch %s: %s", key, result)

            _LOGGER.debug(
                "Successfully fetched RM endpoint data: %s", list(rm_data.keys())
            )

        except (aiohttp.ClientError, asyncio.TimeoutError, ValueError) as e:
            _LOGGER.warning("Error fetching RM endpoint data: %s", e)

        return rm_data

    def has_rm_data(self, key: str) -> bool:
        """Check if RM data key is present in rmData."""
        if self.data is None or "rmData" not in self.data:
            return False
        return key in self.data["rmData"]

    def get_rm_data(self, key: str) -> dict[str, Any] | None:
        """Get RM data by key."""
        if not self.has_rm_data(key):
            return None
        return self.data["rmData"][key]
