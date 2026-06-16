"""Common code for econet300 integration."""

from __future__ import annotations

import asyncio
import copy
from datetime import timedelta
import logging
import time
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
from .common_functions import is_ecomax360i_controller, is_ecosol_controller
from .const import (
    CONF_DEVICE_GROUPING,
    CONF_POLL_EDIT_PARAMS,
    CONF_POLL_REG_PARAMS,
    CONF_POLL_SYS_PARAMS,
    CONSECUTIVE_FAILURES_THRESHOLD,
    DEFAULT_DEVICE_GROUPING,
    DEFAULT_POLL_EDIT_PARAMS,
    DEFAULT_POLL_REG_PARAMS,
    DEFAULT_POLL_SYS_PARAMS,
    DEVICE_GROUPING_SINGLE,
    DOMAIN,
    RM_ADDITIONAL_DATASET_KEYS,
    RM_CORE_DATASET_KEYS,
    STALE_AFTER_SECONDS,
    UPDATE_TIMEOUT_FIRST_SEC,
    UPDATE_TIMEOUT_SEC,
)

_LOGGER = logging.getLogger(__name__)


def skip_params_edits(sys_params: dict[str, Any] | None) -> bool:
    """Determine whether paramsEdits should be skipped based on controllerID."""
    if sys_params is None:
        return False
    controller_id = sys_params.get("controllerID")

    unsupported_controllers = {
        "ecoMAX360i",
        "ecoSter",
        "SControl MK1",
    }

    if is_ecosol_controller(controller_id) or controller_id in unsupported_controllers:
        _LOGGER.debug(
            "Skipping paramsEdits due to controllerID: %s (endpoint not supported)",
            controller_id,
        )
        return True

    return False


def skip_edit_params(sys_params: dict[str, Any] | None) -> bool:
    """Determine whether editParams should be skipped based on controllerID."""
    if sys_params is None:
        return True
    return not is_ecomax360i_controller(sys_params.get("controllerID"))


def build_edit_param_catalog(
    edit_params: dict[str, Any] | None,
) -> dict[str, dict[str, Any]]:
    """Build a normalized writable-parameter catalog from /econet/editParams."""
    data = (edit_params or {}).get("data", {}) or {}
    editable_params = (edit_params or {}).get("editableParams", {}) or {}
    catalog: dict[str, dict[str, Any]] = {}

    for pid, entry in data.items():
        try:
            if not isinstance(entry, dict):
                continue
            editable = bool(entry.get("edit"))
            name = entry.get("name") or f"Param {pid}"
            value = entry.get("value")

            if not editable:
                continue
            if not isinstance(value, (int, float)):
                continue

            unit_code = entry.get("unit", 0)
            unit = None
            lname = str(name).lower()
            if unit_code == 1 or "temp" in lname or "setpoint" in lname:
                unit = "°C"

            minv = entry.get("minv")
            maxv = entry.get("maxv")
            has_explicit_limits = False
            native_min = None
            native_max = None
            native_step = None

            if (
                isinstance(minv, (int, float))
                and isinstance(maxv, (int, float))
                and maxv > minv
            ):
                native_min = float(minv)
                native_max = float(maxv)
                has_explicit_limits = True

            ep = editable_params.get(str(pid)) or editable_params.get(pid)
            if (
                (native_min is None or native_max is None)
                and isinstance(ep, list)
                and len(ep) >= 6
            ):
                try:
                    native_min = float(ep[3])
                    native_max = float(ep[4])
                    native_step = float(ep[5])
                    has_explicit_limits = True
                except (TypeError, ValueError):
                    pass

            if native_step is None:
                is_intish = True
                for item in (value, native_min, native_max):
                    if item is None:
                        continue
                    try:
                        if not float(item).is_integer():
                            is_intish = False
                            break
                    except (TypeError, ValueError):
                        pass
                native_step = 1.0 if is_intish else 0.1

            if native_min is not None and native_max is not None:
                try:
                    fval = float(value)
                    native_min = min(native_min, fval)
                    native_max = max(native_max, fval)
                except (TypeError, ValueError):
                    pass

            kind = "number"
            options: list[str] | None = None
            expose_number = False
            if native_min is not None and native_max is not None:
                if (
                    has_explicit_limits
                    and native_min == 0
                    and native_max == 1
                    and native_step in (1, 1.0)
                ):
                    kind = "switch"
                elif (
                    has_explicit_limits
                    and native_step in (1, 1.0)
                    and native_max.is_integer()
                    and native_min.is_integer()
                ):
                    span = int(native_max) - int(native_min)
                    if 0 <= span <= 20:
                        kind = "select"
                        options = [
                            str(v) for v in range(int(native_min), int(native_max) + 1)
                        ]
            elif value in (0, 1):
                kind = "switch"
                expose_number = True
                native_min = 0.0
                native_max = max(10.0, float(value))
                native_step = 1.0

            catalog[str(pid)] = {
                "id": str(pid),
                "name": str(name),
                "value": float(value) if isinstance(value, float) else int(value),
                "editable": True,
                "unit": unit,
                "unit_code": unit_code,
                "min": native_min,
                "max": native_max,
                "step": native_step,
                "kind": kind,
                "options": options or [],
                "expose_number": expose_number,
            }
        except Exception:  # noqa: BLE001
            _LOGGER.debug("Skipping malformed editParam %s", pid, exc_info=True)
            continue

    return catalog


class EconetDataCoordinator(DataUpdateCoordinator):
    """Econet data coordinator to handle data updates."""

    def __init__(
        self,
        hass,
        api: Econet300Api,
        config_entry: ConfigEntry,
        options: dict[str, Any] | None = None,
    ) -> None:
        """Initialize coordinator."""
        options = options or {}
        self._poll_reg_params = int(
            options.get(CONF_POLL_REG_PARAMS, DEFAULT_POLL_REG_PARAMS)
        )
        self._poll_sys_params = int(
            options.get(CONF_POLL_SYS_PARAMS, DEFAULT_POLL_SYS_PARAMS)
        )
        self._poll_edit_params = int(
            options.get(CONF_POLL_EDIT_PARAMS, DEFAULT_POLL_EDIT_PARAMS)
        )
        self._device_grouping = options.get(
            CONF_DEVICE_GROUPING, DEFAULT_DEVICE_GROUPING
        )

        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_data_coordinator",
            update_interval=timedelta(seconds=max(5, self._poll_reg_params)),
        )
        self._api = api
        self._config_entry = config_entry
        self._options = options
        self._consecutive_failures = 0
        self._rm_supported: bool | None = None
        self._last_success_ts: float = 0.0
        self._last_failure_ts: float = 0.0
        self._last_error: str = ""
        self._sys_params_last_fetch: float = 0.0
        self._edit_params_last_fetch: float = 0.0
        self._edit_params_force_refresh = True
        self._edit_params_failures = 0

    def has_sys_data(self, key: str) -> bool:
        """Check if data key is present in sysParams."""
        if self.data is None:
            return False
        return key in (self.data.get("sysParams") or {})

    def has_reg_data(self, key: str) -> bool:
        """Check if data key is present in regParams."""
        if self.data is None:
            return False
        return key in (self.data.get("regParams") or {})

    def has_param_edit_data(self, key: str) -> bool:
        """Check if parameter edit data key is present in paramsEdits."""
        if self.data is None:
            return False
        return key in (self.data.get("paramsEdits") or {})

    @property
    def single_device_tree(self) -> bool:
        """Return True when all entities should share one device."""
        return self._device_grouping == DEVICE_GROUPING_SINGLE

    def force_edit_params_refresh(self) -> None:
        """Force editParams refresh on the next coordinator update."""
        self._edit_params_force_refresh = True

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from API endpoint."""
        _LOGGER.debug("Fetching data from API")

        last_data: dict[str, Any] = self.data or {}
        first_update = self._rm_supported is None
        timeout = UPDATE_TIMEOUT_FIRST_SEC if first_update else UPDATE_TIMEOUT_SEC

        try:
            async with asyncio.timeout(timeout):
                now = time.time()

                sys_params = last_data.get("sysParams") or {}
                if (
                    not sys_params
                    or (now - self._sys_params_last_fetch) >= self._poll_sys_params
                ):
                    sys_params = await self._api.fetch_sys_params()
                    if not isinstance(sys_params, dict) or not sys_params:
                        raise ApiError("sysParams endpoint returned no usable data")  # noqa: TRY301 — reuse the ApiError keep-last-data path
                    self._sys_params_last_fetch = now

                if sys_params is None or skip_params_edits(sys_params):
                    params_edits = {}
                else:
                    params_edits = await self._api.fetch_param_edit_data()
                    if not isinstance(params_edits, dict):
                        params_edits = {}

                reg_params = await self._api.fetch_reg_params()
                if not isinstance(reg_params, dict) or not reg_params:
                    raise ApiError("regParams endpoint returned no usable data")  # noqa: TRY301 — reuse the ApiError keep-last-data path

                reg_params_data = await self._api.fetch_reg_params_data()
                if not isinstance(reg_params_data, dict):
                    reg_params_data = last_data.get("regParamsData") or {}

                edit_params_full = last_data.get("editParamsFull") or {}
                edit_params_data = last_data.get("editParams") or {}
                information_params = last_data.get("informationParams") or {}

                if skip_edit_params(sys_params):
                    edit_params_full = {}
                    edit_params_data = {}
                    information_params = {}
                else:
                    # poll_edit_params <= 0 disables interval polling: only fetch
                    # on an explicit force-refresh or once to populate an empty
                    # catalog (never unconditionally on every cycle).
                    interval_due = (
                        self._poll_edit_params > 0
                        and (now - self._edit_params_last_fetch)
                        >= self._poll_edit_params
                    )
                    should_fetch_edit = (
                        self._edit_params_force_refresh
                        or not edit_params_full
                        or interval_due
                    )
                    if should_fetch_edit:
                        try:
                            raw = await self._api.fetch_edit_params()
                            if isinstance(raw, dict) and raw:
                                edit_params_full = copy.deepcopy(raw)
                                edit_params_data = edit_params_full.get("data") or {}
                                information_params = (
                                    edit_params_full.get("informationParams") or {}
                                )
                                self._edit_params_last_fetch = now
                                self._edit_params_failures = 0
                            else:
                                self._edit_params_failures += 1
                        except (ApiError, asyncio.TimeoutError, ClientError) as err:
                            self._edit_params_failures += 1
                            _LOGGER.warning(
                                "Failed to refresh editParams, keeping last data: %s",
                                err,
                            )
                        self._edit_params_force_refresh = False

                edit_catalog = build_edit_param_catalog(edit_params_full)
                if not params_edits:
                    params_edits = {
                        pid: info.get("value") for pid, info in edit_catalog.items()
                    }

                if self._rm_supported is None:
                    self._rm_supported = await self._api.probe_rm_support()
                    if not self._rm_supported:
                        _LOGGER.info("RM endpoint not available, skipping merged data")

                if self._rm_supported:
                    rm_data = await self._fetch_rm_endpoint_data()
                    merged_data = None
                    try:
                        merged_data = await self._api.fetch_merged_rm_data(
                            sys_params=sys_params,
                        )
                    except (aiohttp.ClientError, asyncio.TimeoutError, ValueError) as e:
                        _LOGGER.warning(
                            "Failed to fetch merged parameter data in coordinator: %s",
                            e,
                        )
                else:
                    rm_data = {}
                    merged_data = None

                self._last_success_ts = now
                self._last_error = ""
                self._on_successful_update()

                result = {
                    "sysParams": copy.deepcopy(sys_params),
                    "regParams": copy.deepcopy(reg_params),
                    "regParamsData": copy.deepcopy(reg_params_data),
                    "paramsEdits": copy.deepcopy(params_edits),
                    "editParams": copy.deepcopy(edit_params_data),
                    "editParamsFull": copy.deepcopy(edit_params_full),
                    "editParamCatalog": copy.deepcopy(edit_catalog),
                    "informationParams": copy.deepcopy(information_params),
                    "rmData": rm_data,
                    "mergedData": merged_data,
                }

                # result is freshly allocated (each value already deep-copied
                # above), so _with_health can mutate it in place without copying.
                return self._with_health(result, online=True, copy_payload=False)
        except AuthError as err:
            _LOGGER.error("Authentication error: %s", err)
            raise ConfigEntryAuthFailed from err
        except ApiError as err:
            _LOGGER.error("API error: %s", err)
            self._on_failed_update(err)
            if last_data:
                return self._with_health(last_data, online=False)
            raise UpdateFailed(f"Error communicating with API: {err}") from err
        except asyncio.TimeoutError as err:
            _LOGGER.warning(
                "Update timed out after %ds (device slow or overloaded?): %s",
                timeout,
                err,
            )
            self._on_failed_update(err)
            if last_data:
                return self._with_health(last_data, online=False)
            raise UpdateFailed(f"Update timed out after {timeout}s: {err}") from err
        except ClientError as err:
            _LOGGER.warning("Connection failed (device offline?): %s", err)
            self._on_failed_update(err)
            if last_data:
                return self._with_health(last_data, online=False)
            raise UpdateFailed(f"Connection failed: {err}") from err

    def _with_health(
        self, payload: dict[str, Any], *, online: bool, copy_payload: bool = True
    ) -> dict[str, Any]:
        """Add health metadata used by watchdog entities.

        ``copy_payload`` deep-copies the payload to avoid mutating live data
        (needed on the failure path, where ``payload`` is the live ``self.data``).
        The success path passes an already-fresh dict and can skip the copy.
        """
        data = copy.deepcopy(payload) if copy_payload else payload
        now = time.time()
        last_success_ts = self._last_success_ts or float(
            (data.get("_health") or {}).get("last_success_ts") or 0
        )
        stale_seconds = max(0, int(now - last_success_ts)) if last_success_ts else 0
        stale = bool(last_success_ts) and stale_seconds >= STALE_AFTER_SECONDS
        data["_health"] = {
            "online": bool(online),
            "stale": bool(stale),
            "stale_after_seconds": STALE_AFTER_SECONDS,
            "stale_seconds": stale_seconds,
            "last_success_ts": last_success_ts,
            "last_failure_ts": self._last_failure_ts,
            "consecutive_failures": self._consecutive_failures,
            "last_error": self._last_error,
            "poll_reg_params": self._poll_reg_params,
            "poll_sys_params": self._poll_sys_params,
            "poll_edit_params": self._poll_edit_params,
            "edit_params_failures": self._edit_params_failures,
        }
        data["_ts"] = now
        return data

    def _on_successful_update(self) -> None:
        """Handle successful data update."""
        if self._consecutive_failures > 0:
            _LOGGER.debug(
                "Connection restored after %d failures", self._consecutive_failures
            )
            self._consecutive_failures = 0
            async_delete_issue(
                self.hass, DOMAIN, f"connection_failed_{self._config_entry.entry_id}"
            )

    def _on_failed_update(self, err: Exception | None = None) -> None:
        """Handle failed data update."""
        self._consecutive_failures += 1
        self._last_failure_ts = time.time()
        if err is not None:
            self._last_error = str(err) or err.__class__.__name__
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
            core_tasks = [
                self._api.fetch_rm_current_data_params(),
                self._api.fetch_rm_params_names(),
                self._api.fetch_rm_params_data(),
                self._api.fetch_rm_langs(),
            ]
            core_results = await asyncio.gather(*core_tasks, return_exceptions=True)

            for index, key in enumerate(RM_CORE_DATASET_KEYS):
                result = core_results[index]
                rm_data[key] = (
                    {} if isinstance(result, Exception) or result is None else result
                )
                if isinstance(result, Exception):
                    _LOGGER.warning("Failed to fetch %s: %s", key, result)

            if rm_data.get("currentDataParams"):
                additional_tasks = [
                    self._api.fetch_rm_params_descs(),
                    self._api.fetch_rm_params_enums(),
                    self._api.fetch_rm_alarms_names(),
                ]
                additional_results = await asyncio.gather(
                    *additional_tasks, return_exceptions=True
                )

                for index, key in enumerate(RM_ADDITIONAL_DATASET_KEYS):
                    result = additional_results[index]
                    rm_data[key] = (
                        {}
                        if isinstance(result, Exception) or result is None
                        else result
                    )
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
