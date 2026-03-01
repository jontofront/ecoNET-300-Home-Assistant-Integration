"""Econet300 API class describing methods of getting and setting data."""

import asyncio
from datetime import datetime
from http import HTTPStatus
import json
import logging
import re
from typing import Any

import aiohttp
from aiohttp import BasicAuth, ClientSession, ClientTimeout
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .common_functions import generate_translation_key
from .const import (
    API_EDITABLE_PARAMS_LIMITS_DATA,
    API_EDITABLE_PARAMS_LIMITS_URI,
    API_REG_PARAMS_DATA_PARAM_DATA,
    API_REG_PARAMS_DATA_URI,
    API_REG_PARAMS_PARAM_DATA,
    API_REG_PARAMS_URI,
    API_RM_ACCESS_URI,
    API_RM_ALARMS_NAMES_URI,
    API_RM_CURRENT_DATA_PARAMS_EDITS_URI,
    API_RM_CURRENT_DATA_PARAMS_URI,
    API_RM_DATA_KEY,
    API_RM_EXISTING_LANGS_URI,
    API_RM_LANGS_URI,
    API_RM_LOCKS_NAMES_URI,
    API_RM_PARAMS_DATA_URI,
    API_RM_PARAMS_DESCS_URI,
    API_RM_PARAMS_ENUMS_URI,
    API_RM_PARAMS_NAMES_URI,
    API_RM_PARAMS_UNITS_NAMES_URI,
    API_RM_STRUCTURE_URI,
    API_SYS_PARAMS_PARAM_HW_VER,
    API_SYS_PARAMS_PARAM_MODEL_ID,
    API_SYS_PARAMS_PARAM_SW_REV,
    API_SYS_PARAMS_PARAM_UID,
    API_SYS_PARAMS_URI,
    CACHE_KEY_STATIC_METADATA,
    CACHE_STATIC_METADATA_TTL,
    CONTROL_PARAMS,
    NUMBER_MAP,
    RM_PROBE_TIMEOUT_SEC,
    RM_STRUCTURE_TYPE_CATEGORY,
    RM_STRUCTURE_TYPE_DATA_REF,
    RM_STRUCTURE_TYPE_MENU_GROUP,
    RM_STRUCTURE_TYPE_PARAMETER,
    RMNEWPARAM_PARAMS,
)
from .mem_cache import MemCache

_LOGGER = logging.getLogger(__name__)


def _sanitize_url_for_logging(url: str) -> str:
    """Remove sensitive parameters from URL before logging.

    Removes password parameter from URLs to prevent sensitive data exposure in logs.
    """
    # Remove password parameter from URL query string
    return re.sub(r"([&?])password=[^&]*", r"\1password=***REDACTED***", url)


class AuthError(Exception):
    """Raised when authentication fails."""


class ApiError(Exception):
    """Raised when an API error occurs."""


class DataError(Exception):
    """Raised when there is an error with the data."""


class Limits:
    """Class defining entity value set limits."""

    def __init__(self, min_v: int | None, max_v: int | None):
        """Construct the necessary attributes for the Limits object."""
        self.min = min_v
        self.max = max_v


class EconetClient:
    """Econet client class."""

    def __init__(
        self, host: str, username: str, password: str, session: ClientSession
    ) -> None:
        """Initialize the EconetClient."""

        proto = ["http://", "https://"]

        not_contains = all(p not in host for p in proto)

        if not_contains:
            _LOGGER.info("Manually adding 'http' to host")
            host = "http://" + host

        self._host = host
        self._session = session
        self._auth = BasicAuth(username, password)
        self._model_id = "default-model-id"
        self._sw_revision = "default-sw-revision"

    @property
    def host(self) -> str:
        """Get host address."""
        return self._host

    async def get(self, url):
        """Public method for fetching data."""
        attempt = 1
        max_attempts = 5

        while attempt <= max_attempts:
            try:
                _LOGGER.debug("Fetching data from URL: %s (Attempt %d)", _sanitize_url_for_logging(url), attempt)

                async with await self._session.get(
                    url, auth=self._auth, timeout=ClientTimeout(total=15)
                ) as resp:
                    _LOGGER.debug("Received response with status: %s", resp.status)
                    if resp.status == HTTPStatus.UNAUTHORIZED:
                        _LOGGER.error("Unauthorized access to URL: %s", _sanitize_url_for_logging(url))
                        raise AuthError

                    if resp.status != HTTPStatus.OK:
                        try:
                            error_message = await resp.text()
                        except (aiohttp.ClientError, aiohttp.ClientResponseError) as e:
                            error_message = f"Could not retrieve error message: {e}"

                        _LOGGER.error(
                            "Failed to fetch data from URL: %s (Status: %s) - Response: %s",
                            _sanitize_url_for_logging(url),
                            resp.status,
                            error_message,
                        )
                        return None

                    data = await resp.json()
                    # Log summary only to avoid flooding logs with large JSON
                    if isinstance(data, dict):
                        data_keys = list(data.keys())
                        data_size = len(data.get("data", [])) if "data" in data else 0
                        _LOGGER.debug(
                            "Fetched data: keys=%s, data_items=%d",
                            data_keys,
                            data_size,
                        )
                    else:
                        _LOGGER.debug("Fetched data: type=%s", type(data).__name__)
                    return data

            except TimeoutError:
                _LOGGER.warning("Timeout error, retry(%i/%i)", attempt, max_attempts)
                await asyncio.sleep(1)
            attempt += 1
        _LOGGER.error(
            "Failed to fetch data from %s after %d attempts", _sanitize_url_for_logging(url), max_attempts
        )
        return None

    async def get_with_short_timeout(self, url: str, timeout_sec: float = 2):
        """Fetch data with a short timeout (single attempt, no retries).

        Used to check if an endpoint is available; legacy-only modules return 404 or
        timeout. Caller can use this to skip full fetches when the endpoint is absent.
        """
        try:
            async with await self._session.get(
                url, auth=self._auth, timeout=ClientTimeout(total=timeout_sec)
            ) as resp:
                if resp.status in (HTTPStatus.UNAUTHORIZED, HTTPStatus.NOT_FOUND):
                    return None
                if resp.status != HTTPStatus.OK:
                    return None
                return await resp.json()
        except (aiohttp.ClientError, asyncio.TimeoutError, ValueError):
            return None

    async def get_with_fix_quotes(self, url):
        r"""Fetch data with preprocessing to fix malformed JSON quote escaping.

        The ecoNET device API sometimes returns JSON with double-double-quotes ("")
        instead of properly escaped quotes (\"). This method fetches raw text,
        fixes the escaping, and then parses JSON.

        Args:
            url: URL to fetch from

        Returns:
            Parsed JSON data, or None if request fails

        """
        attempt = 1
        max_attempts = 5

        while attempt <= max_attempts:
            try:
                _LOGGER.debug(
                    "Fetching data with quote fix from URL: %s (Attempt %d)",
                    url,
                    attempt,
                )

                async with await self._session.get(
                    url, auth=self._auth, timeout=ClientTimeout(total=15)
                ) as resp:
                    _LOGGER.debug("Received response with status: %s", resp.status)
                    if resp.status == HTTPStatus.UNAUTHORIZED:
                        _LOGGER.error("Unauthorized access to URL: %s", _sanitize_url_for_logging(url))
                        raise AuthError

                    if resp.status != HTTPStatus.OK:
                        try:
                            error_message = await resp.text()
                        except (aiohttp.ClientError, aiohttp.ClientResponseError) as e:
                            error_message = f"Could not retrieve error message: {e}"

                        _LOGGER.error(
                            "Failed to fetch data from URL: %s (Status: %s) - Response: %s",
                            _sanitize_url_for_logging(url),
                            resp.status,
                            error_message,
                        )
                        return None

                    # Get raw text and fix quote escaping
                    raw_text = await resp.text()

                    # Fix double-double-quotes ("") to normal quotes
                    # Pattern: look for "" that are inside strings (not at string boundaries)
                    fixed_text = re.sub(r'""([^"]+)""', r'"\1"', raw_text)

                    # Also fix curly/smart quotes to straight quotes
                    fixed_text = fixed_text.replace('"', '"').replace('"', '"')

                    try:
                        data = json.loads(fixed_text)
                    except json.JSONDecodeError as e:
                        _LOGGER.warning(
                            "JSON decode error after quote fix: %s, trying original",
                            e,
                        )
                        # Try original if fix made it worse
                        try:
                            return json.loads(raw_text)
                        except json.JSONDecodeError:
                            _LOGGER.error("Failed to parse JSON from URL: %s", _sanitize_url_for_logging(url))
                            return None
                    else:
                        _LOGGER.debug("Fetched and fixed data successfully")
                    return data

            except TimeoutError:
                _LOGGER.warning("Timeout error, retry(%i/%i)", attempt, max_attempts)
                await asyncio.sleep(1)
            attempt += 1
        _LOGGER.error(
            "Failed to fetch data from %s after %d attempts", _sanitize_url_for_logging(url), max_attempts
        )
        return None


class Econet300Api:
    """Client for interacting with the ecoNET-300 API."""

    def __init__(self, client: EconetClient, cache: MemCache) -> None:
        """Initialize the Econet300Api object with a client, cache, and default values for uid, sw_revision, and hw_version."""
        self._client = client
        self._cache = cache
        self._uid = "default-uid"
        self._model_id = "default-model-id"
        self._sw_revision = "default-sw-revision"
        self._hw_version = "default-hw-version"

    @classmethod
    async def create(cls, client: EconetClient, cache: MemCache):
        """Create and return initial object."""
        c = cls(client, cache)
        await c.init()

        return c

    @property
    def host(self) -> str:
        """Get clients host address."""
        return self._client.host

    @property
    def uid(self) -> str:
        """Get uid."""
        return self._uid

    @property
    def model_id(self) -> str:
        """Get model name."""
        return self._model_id

    @property
    def sw_rev(self) -> str:
        """Get software version."""
        return self._sw_revision

    @property
    def hw_ver(self) -> str:
        """Get hardware version."""
        return self._hw_version

    async def init(self):
        """Econet300 API initialization.

        Raises:
            ConnectionError: If sysParams cannot be fetched (device offline/unreachable).
            ValueError: If uid is missing from sysParams (critical for device identity).

        """
        sys_params = await self.fetch_sys_params()

        if sys_params is None:
            raise ConnectionError(
                "Failed to fetch system parameters - device offline or unreachable"
            )

        # UID is mandatory - without it, entities register under a ghost device
        if API_SYS_PARAMS_PARAM_UID not in sys_params:
            raise ValueError(
                "System parameters missing 'uid' - cannot establish device identity"
            )

        # Set system parameters by HA device properties
        self._set_device_property(sys_params, API_SYS_PARAMS_PARAM_UID, "_uid", "UUID")
        self._set_device_property(
            sys_params,
            API_SYS_PARAMS_PARAM_MODEL_ID,
            "_model_id",
            "controller model name",
        )
        self._set_device_property(
            sys_params, API_SYS_PARAMS_PARAM_SW_REV, "_sw_revision", "software revision"
        )
        self._set_device_property(
            sys_params, API_SYS_PARAMS_PARAM_HW_VER, "_hw_version", "hardware version"
        )

    def _set_device_property(self, sys_params, param_key, attr_name, param_desc):
        """Set an attribute from system parameters with logging if unavailable."""
        if param_key not in sys_params:
            _LOGGER.info(
                "%s not in sys_params - cannot set proper %s", param_key, param_desc
            )
            setattr(self, attr_name, None)
        else:
            setattr(self, attr_name, sys_params[param_key])

    async def set_param(self, param, value) -> bool:
        """Set param value in Econet300 API."""
        if param is None:
            _LOGGER.info(
                "Requested param set for: '%s' but mapping for this param does not exist",
                param,
            )
            return False

        # Get the appropriate endpoint URL
        # Use rmCurrNewParam for temperature setpoints (parameter keys like 1280)
        # Use newParam for control parameters (parameter names like BOILER_CONTROL)
        # Use rmNewParam for special parameters that need newParamIndex (like heater mode 55)
        if param in RMNEWPARAM_PARAMS:
            url = f"{self.host}/econet/rmNewParam?newParamIndex={param}&newParamValue={value}"
            _LOGGER.debug(
                "Using rmNewParam endpoint for special parameter %s: %s",
                param,
                url,
            )
        elif param in NUMBER_MAP:
            # param is a key like "1287"
            url = f"{self.host}/econet/rmCurrNewParam?newParamKey={param}&newParamValue={value}"
            _LOGGER.debug(
                "Using rmCurrNewParam endpoint for temperature setpoint %s: %s",
                param,
                url,
            )
        elif param in NUMBER_MAP.values():
            # param is a value like "mixerSetTemp1" - find the key
            param_key = next(k for k, v in NUMBER_MAP.items() if v == param)
            url = f"{self.host}/econet/rmCurrNewParam?newParamKey={param_key}&newParamValue={value}"
            _LOGGER.debug(
                "Using rmCurrNewParam endpoint for %s (key=%s): %s",
                param,
                param_key,
                url,
            )
        elif param in CONTROL_PARAMS:
            url = f"{self.host}/econet/newParam?newParamName={param}&newParamValue={value}"
            _LOGGER.debug(
                "Using newParam endpoint for control parameter %s: %s", param, url
            )
        else:
            # Default to newParam for unknown parameters
            url = f"{self.host}/econet/newParam?newParamName={param}&newParamValue={value}"
            _LOGGER.debug(
                "Using default newParam endpoint for parameter %s: %s", param, url
            )

        # Make the API call
        data = await self._client.get(url)
        if data is None or "result" not in data:
            return False
        if data["result"] != "OK":
            return False

        # Cache the value locally
        self._cache.set(param, value)

        # Force immediate refresh of paramsEdits data
        await self._force_refresh_params_edits()

        return True

    async def set_param_by_index(self, param_index: str | int, value: float) -> bool:
        """Set parameter value using rmNewParam endpoint with parameter index.

        This is used for dynamic entities from mergedData that use parameter numbers
        (like heating curve with index 83) instead of parameter keys.

        Args:
            param_index: The parameter index/number from mergedData (e.g., "83" or 83)
            value: The value to set (already scaled if needed)

        Returns:
            True if successful, False otherwise

        """
        if param_index is None:
            _LOGGER.warning("Cannot set param with None index")
            return False

        # Format value - use integer format for whole numbers to match API expectations
        # API may silently ignore values like "56.0" for integer parameters (mult=1)
        formatted_value: int | float = int(value) if value == int(value) else value

        url = f"{self.host}/econet/rmNewParam?newParamIndex={param_index}&newParamValue={formatted_value}"
        _LOGGER.debug(
            "Setting parameter by index %s to value %s: %s",
            param_index,
            formatted_value,
            url,
        )

        data = await self._client.get(url)
        if data is None or "result" not in data:
            _LOGGER.warning(
                "Failed to set param by index %s: no result in response", param_index
            )
            return False
        if data["result"] != "OK":
            _LOGGER.warning(
                "Failed to set param by index %s: result=%s",
                param_index,
                data.get("result"),
            )
            return False

        _LOGGER.debug("Successfully set param %s to %s", param_index, formatted_value)
        return True

    async def _force_refresh_params_edits(self):
        """Force refresh paramsEdits data by fetching fresh data and updating cache."""
        try:
            _LOGGER.debug("Force refreshing paramsEdits data")
            fresh_data = await self._fetch_api_data_by_key(
                API_EDITABLE_PARAMS_LIMITS_URI, API_EDITABLE_PARAMS_LIMITS_DATA
            )
            if fresh_data:
                self._cache.set(API_EDITABLE_PARAMS_LIMITS_DATA, fresh_data)
                _LOGGER.debug(
                    "Successfully refreshed paramsEdits data: %d params",
                    len(fresh_data) if isinstance(fresh_data, dict) else 0,
                )
            else:
                _LOGGER.info("Failed to refresh paramsEdits data")
        except (aiohttp.ClientError, asyncio.TimeoutError, ValueError) as e:
            _LOGGER.error("Error refreshing paramsEdits data: %s", e)

    async def get_param_limits(self, param: str):
        """Fetch and return the limits for a particular parameter from the Econet 300 API, using a cache for efficient retrieval if available."""
        if not self._cache.exists(API_EDITABLE_PARAMS_LIMITS_DATA):
            try:
                # Attempt to fetch the API data
                limits = await self._fetch_api_data_by_key(
                    API_EDITABLE_PARAMS_LIMITS_URI, API_EDITABLE_PARAMS_LIMITS_DATA
                )
                # Cache the fetched data
                self._cache.set(API_EDITABLE_PARAMS_LIMITS_DATA, limits)
            except (
                aiohttp.ClientError,
                asyncio.TimeoutError,
                ValueError,
                DataError,
            ) as e:
                _LOGGER.error(
                    "API error while fetching data from %s: %s",
                    API_EDITABLE_PARAMS_LIMITS_URI,
                    e,
                )
                return None
            except (TypeError, AttributeError) as e:
                _LOGGER.error(
                    "Data structure error while processing API data from %s: %s",
                    API_EDITABLE_PARAMS_LIMITS_URI,
                    e,
                )
                return None

        # Retrieve limits from the cache
        limits = self._cache.get(API_EDITABLE_PARAMS_LIMITS_DATA)

        if not param:
            _LOGGER.info("Parameter name is None. Unable to fetch limits.")
            return None

        if limits is None or param not in limits:
            _LOGGER.info(
                "Limits for parameter '%s' do not exist. Available limits: %s",
                param,
                limits,
            )
            return None

        # Extract and log the limits
        curr_limits = limits[param]
        # Remove sensitive data from debug logging to prevent information disclosure
        _LOGGER.debug("Limits for edit param '%s' retrieved successfully", param)
        return Limits(curr_limits["min"], curr_limits["max"])

    async def fetch_reg_params_data(self) -> dict[str, Any] | None:
        """Fetch data from econet/regParamsData."""
        try:
            regParamsData = await self._fetch_api_data_by_key(
                API_REG_PARAMS_DATA_URI, API_REG_PARAMS_DATA_PARAM_DATA
            )
        except (aiohttp.ClientError, asyncio.TimeoutError, ValueError, DataError) as e:
            _LOGGER.error("API error occurred while fetching regParamsData: %s", e)
            return {}
        except (TypeError, AttributeError) as e:
            _LOGGER.error(
                "Data structure error occurred while processing regParamsData: %s", e
            )
            return {}
        else:
            _LOGGER.debug(
                "Fetched regParamsData: %d params",
                len(regParamsData) if isinstance(regParamsData, dict) else 0,
            )
            return regParamsData

    async def fetch_param_edit_data(self):
        """Fetch and return the limits for a particular parameter from the Econet 300 API, using a cache for efficient retrieval if available.

        Note: This endpoint is only supported by certain controllers (e.g., ecoMAX series).
        Controllers like ecoSOL500, ecoSter, SControl MK1 don't support this endpoint.
        The common.py skip_params_edits() function handles controller-specific endpoint support.
        """
        if not self._cache.exists(API_EDITABLE_PARAMS_LIMITS_DATA):
            limits = await self._fetch_api_data_by_key(
                API_EDITABLE_PARAMS_LIMITS_URI, API_EDITABLE_PARAMS_LIMITS_DATA
            )
            # Ensure we always return a dict, not None
            if limits is None:
                limits = {}
            self._cache.set(API_EDITABLE_PARAMS_LIMITS_DATA, limits)

        result = self._cache.get(API_EDITABLE_PARAMS_LIMITS_DATA)
        # Ensure we always return a dict, not None
        return result if result is not None else {}

    async def fetch_reg_params(self) -> dict[str, Any] | None:
        """Fetch and return the regParams data from ip/econet/regParams endpoint."""
        _LOGGER.debug("Calling fetch_reg_params method")
        regParams = await self._fetch_api_data_by_key(
            API_REG_PARAMS_URI, API_REG_PARAMS_PARAM_DATA
        )
        _LOGGER.debug(
            "Fetched regParams: type=%s, count=%d",
            type(regParams).__name__,
            len(regParams) if isinstance(regParams, dict) else 0,
        )
        return regParams

    async def fetch_sys_params(self) -> dict[str, Any] | None:
        """Fetch and return the regParam data from ip/econet/sysParams endpoint."""
        _LOGGER.debug(
            "fetch_sys_params called: Fetching parameters from host '%s'",
            self.host,
        )
        sysParams = await self._fetch_api_data_by_key(API_SYS_PARAMS_URI)
        _LOGGER.debug(
            "Fetched sysParams: %d params",
            len(sysParams) if isinstance(sysParams, dict) else 0,
        )
        return sysParams

    async def _fetch_api_data_by_key(self, endpoint: str, data_key: str | None = None):
        """Fetch a key from the json-encoded data returned by the API for a given registry If key is None, then return whole data."""
        try:
            data = await self._client.get(f"{self.host}/econet/{endpoint}")

            if data is None:
                _LOGGER.info("Data fetched by API for endpoint: %s is None", endpoint)
                return None

            if data_key is None:
                return data

            if data_key not in data:
                _LOGGER.info(
                    "Data for key: %s does not exist in endpoint: %s",
                    data_key,
                    endpoint,
                )
                return None

            return data[data_key]
        except aiohttp.ClientError as e:
            _LOGGER.warning(
                "Client error while fetching %s (device offline?): %s",
                endpoint,
                e,
            )
        except asyncio.TimeoutError as e:
            _LOGGER.warning(
                "Timeout while fetching %s (device offline?): %s",
                endpoint,
                e,
            )
        except ValueError as e:
            _LOGGER.error(
                "A value error occurred while processing data from endpoint: %s, error: %s",
                endpoint,
                e,
            )
        except (TypeError, AttributeError) as e:
            _LOGGER.error(
                "Data structure error occurred while processing response from endpoint: %s, error: %s",
                endpoint,
                e,
            )
        return None

    # =============================================================================
    # RM... ENDPOINT METHODS (Remote Menu API)
    # =============================================================================
    # These methods provide access to the structured data endpoints used by
    # the ecoNET24 web interface. Based on analysis of dev_set1.js and test fixtures.

    async def fetch_rm_params_names(self, lang: str = "en") -> dict[str, Any] | None:
        """Fetch parameter names with translations from rmParamsNames endpoint.

        This endpoint provides human-readable parameter names in the specified language.
        Used by the ecoNET24 web interface to display parameter labels.

        Args:
            lang: Language code (e.g., 'en', 'pl', 'fr'). Defaults to 'en'.

        Returns:
            Dictionary containing parameter names mapped to their translations.
            None if the request fails.

        Example:
            {
                "remoteMenuParamsNamesVer": "61477_1",  # Version of parameter names
                "data": [                               # Array of parameter names (index matches rmParamsData)
                    "100% Blow-in output",             # Human-readable name for parameter 0
                    "100% Feeder operation",            # Human-readable name for parameter 1
                    "Boiler hysteresis",               # Human-readable name for parameter 2
                    "FL airfl. correction",            # Human-readable name for parameter 3
                    "Minimum boiler output FL"         # Human-readable name for parameter 4
                ]
            }

        """
        try:
            url = f"{self.host}/econet/{API_RM_PARAMS_NAMES_URI}?uid={self.uid}&lang={lang}"
            _LOGGER.debug("Fetching parameter names from: %s", url)

            data = await self._client.get(url)
            if data is None:
                _LOGGER.warning("Failed to fetch parameter names from rmParamsNames")
                return None

            return data.get(API_RM_DATA_KEY, {})

        except (aiohttp.ClientError, asyncio.TimeoutError, ValueError) as e:
            _LOGGER.error("Error fetching parameter names: %s", e)
            return None

    async def _authenticate_service(self, password: str) -> bool:
        """Authenticate with service password via rmAccess endpoint.

        This method authenticates with the device using the service password.
        Successful authentication unlocks the ability to modify service parameters
        (those with pass_index > 0) in subsequent API calls.

        Based on dev_set1.js: rmAccess?password=<password>

        Args:
            password: The service password (or password hash from sysParams)

        Returns:
            True if authentication successful, False otherwise

        """
        try:
            url = f"{self.host}/econet/{API_RM_ACCESS_URI}"
            _LOGGER.debug("Authenticating with service password via rmAccess")

            async with asyncio.timeout(10):
                async with self._client._session.get(  # noqa: SLF001  # Accessing private member for service auth
                    url,
                    params={"password": password},
                    auth=self._client._auth,  # noqa: SLF001  # Accessing private member for service auth
                ) as response:
                    if response.status == HTTPStatus.OK:
                        data = await response.json()
                        access = data.get("access", False)
                        if access:
                            _LOGGER.info(
                                "Service authentication successful (access level: %s)",
                                data.get("index", data.get("level", "unknown")),
                            )
                            return True
                        _LOGGER.debug(
                            "Service authentication denied: access=%s", access
                        )
                    else:
                        _LOGGER.debug(
                            "Service authentication failed: HTTP %s", response.status
                        )
        except asyncio.TimeoutError:
            _LOGGER.debug("Service authentication timed out")
        except (aiohttp.ClientError, ValueError) as e:
            _LOGGER.debug("Service authentication error: %s", e)
        except (OSError, RuntimeError) as e:
            _LOGGER.debug("Service authentication unexpected error: %s", e)
        return False

    async def fetch_rm_params_data(
        self, password: str | None = None
    ) -> dict[str, Any] | None:
        """Fetch parameter metadata from rmParamsData endpoint.

        This endpoint provides parameter metadata including min/max values, units,
        and other configuration information for each parameter.

        Args:
            password: Optional service password hash for authenticated access

        Returns:
            Dictionary containing parameter metadata.
            None if the request fails.

        Example:
            {
                "remoteMenuValuesKonfVer": 14264,  # Configuration version number
                "remoteMenuValuesVer": 43253,      # Data version number
                "data": [
                    {
                        "value": 60,    # Current parameter value
                        "maxv": 100,    # Maximum allowed value
                        "minv": 15,     # Minimum allowed value
                        "edit": true,   # Whether parameter can be edited
                        "unit": 5,      # Unit index (maps to rmParamsUnitsNames)
                        "mult": 1,      # Multiplier for value conversion
                        "offset": 0     # Offset for value conversion
                    }
                ]
            }

        """
        try:
            url = f"{self.host}/econet/{API_RM_PARAMS_DATA_URI}?uid={self.uid}"
            log_url = url  # Safe URL for logging (without password)
            if password:
                url = f"{url}&password={password}"
            _LOGGER.debug("Fetching parameter data from: %s", log_url)

            data = await self._client.get(url)
            if data is None:
                _LOGGER.warning("Failed to fetch parameter data from rmParamsData")
                return None

            return data.get(API_RM_DATA_KEY, {})

        except (aiohttp.ClientError, asyncio.TimeoutError, ValueError) as e:
            _LOGGER.error("Error fetching parameter data: %s", e)
            return None

    async def probe_rm_support(self) -> bool:
        """Probe rmParamsData with short timeout to detect legacy-only modules (no RM API).

        Returns True if the endpoint responds with valid data, False on 404/timeout/error.
        Used to skip RM and mergedData fetches on devices that do not support them.
        """
        url = f"{self.host}/econet/{API_RM_PARAMS_DATA_URI}?uid={self.uid}"
        data = await self._client.get_with_short_timeout(
            url, timeout_sec=RM_PROBE_TIMEOUT_SEC
        )
        if data is None:
            return False
        if not isinstance(data, dict) or API_RM_DATA_KEY not in data:
            return False
        return True

    async def fetch_rm_params_descs(self, lang: str = "en") -> dict[str, Any] | None:
        """Fetch parameter descriptions from rmParamsDescs endpoint.

        This endpoint provides detailed descriptions of parameters in the specified language.
        Used for help text and parameter explanations in the web interface.

        Note: The API sometimes returns malformed JSON with double-double-quotes ("")
        instead of properly escaped quotes. This method uses get_with_fix_quotes()
        to handle this automatically.

        Args:
            lang: Language code (e.g., 'en', 'pl', 'fr'). Defaults to 'en'.

        Returns:
            Dictionary containing parameter descriptions.
            None if the request fails.

        Example:
            {
                "remoteMenuParamsDescsVer": "16688_1",  # Version of parameter descriptions
                "data": [                               # Array of parameter descriptions (index matches rmParamsData)
                    "Blow-in output when the burner runs at maximum output.",                    # Description for parameter 0
                    "Feeder operation time when the burner runs at maximum output.",              # Description for parameter 1
                    "If the boiler temperature drops below the present boiler temperature by the boiler hysteresis value, then the automatic burner firing up will take place."  # Description for parameter 2
                ]
            }

        """
        try:
            url = f"{self.host}/econet/{API_RM_PARAMS_DESCS_URI}?uid={self.uid}&lang={lang}"
            _LOGGER.debug("Fetching parameter descriptions from: %s", url)

            # Use get_with_fix_quotes to handle malformed JSON escaping from device
            data = await self._client.get_with_fix_quotes(url)
            if data is None:
                _LOGGER.warning(
                    "Failed to fetch parameter descriptions from rmParamsDescs"
                )
                return None

            return data.get(API_RM_DATA_KEY, {})

        except (aiohttp.ClientError, asyncio.TimeoutError, ValueError) as e:
            _LOGGER.error("Error fetching parameter descriptions: %s", e)
            return None

    async def fetch_rm_params_enums(self, lang: str = "en") -> dict[str, Any] | None:
        """Fetch parameter enumeration values from rmParamsEnums endpoint.

        This endpoint provides enumeration values for parameters that have
        predefined options (like operation modes, status values, etc.).

        Args:
            lang: Language code (e.g., 'en', 'pl', 'fr'). Defaults to 'en'.

        Returns:
            Dictionary containing parameter enumeration values.
            None if the request fails.

        Example:
            {
                "remoteMenuParamsEnumsVer": "22746_1",  # Version of parameter enums
                "data": [                              # Array of enum objects
                    {
                        "0": [                         # Enum type 0
                            "off",                     # Value 0 = "off"
                            "on"                       # Value 1 = "on"
                        ]
                    },
                    {
                        "1": [                         # Enum type 1
                            "off",                     # Value 0 = "off"
                            "priority",                # Value 1 = "priority"
                            "no_priority",             # Value 2 = "no_priority"
                            "summer_mode"              # Value 3 = "summer_mode"
                        ]
                    }
                ]
            }

        """
        try:
            url = f"{self.host}/econet/{API_RM_PARAMS_ENUMS_URI}?uid={self.uid}&lang={lang}"
            _LOGGER.debug("Fetching parameter enums from: %s", url)

            data = await self._client.get(url)
            if data is None:
                _LOGGER.warning("Failed to fetch parameter enums from rmParamsEnums")
                return None

            return data.get(API_RM_DATA_KEY, {})

        except (aiohttp.ClientError, asyncio.TimeoutError, ValueError) as e:
            _LOGGER.error("Error fetching parameter enums: %s", e)
            return None

    async def fetch_rm_params_units_names(
        self, lang: str = "en"
    ) -> dict[str, Any] | None:
        """Fetch parameter unit names from rmParamsUnitsNames endpoint.

        This endpoint provides unit names and symbols for parameters.

        Args:
            lang: Language code (e.g., 'en', 'pl', 'fr'). Defaults to 'en'.

        Returns:
            Dictionary containing parameter unit names.
            None if the request fails.

        Example:
            {
                "remoteMenuParamsUnitsNamesVer": "22746_1",  # Version of unit names
                "data": [                                   # Array of unit symbols (index matches unit field in rmParamsData)
                    "",                                     # Index 0: No unit (empty string)
                    "°C",                                   # Index 1: Celsius temperature
                    "sek.",                                 # Index 2: Seconds
                    "min.",                                 # Index 3: Minutes
                    "h.",                                   # Index 4: Hours
                    "%",                                    # Index 5: Percentage
                    "kg",                                   # Index 6: Kilograms
                    "kW",                                   # Index 7: Kilowatts
                    "r/min"                                 # Index 8: Revolutions per minute
                ]
            }

        """
        try:
            url = f"{self.host}/econet/{API_RM_PARAMS_UNITS_NAMES_URI}?uid={self.uid}&lang={lang}"
            _LOGGER.debug("Fetching parameter units from: %s", url)

            data = await self._client.get(url)
            if data is None:
                _LOGGER.warning(
                    "Failed to fetch parameter units from rmParamsUnitsNames"
                )
                return None

            return data.get(API_RM_DATA_KEY, {})

        except (aiohttp.ClientError, asyncio.TimeoutError, ValueError) as e:
            _LOGGER.error("Error fetching parameter units: %s", e)
            return None

    async def fetch_rm_structure(
        self, lang: str = "en", password: str | None = None
    ) -> dict[str, Any] | None:
        """Fetch menu structure from rmStructure endpoint.

        This endpoint provides the hierarchical menu structure for the web interface,
        showing how parameters are organized and grouped.

        Args:
            lang: Language code (e.g., 'en', 'pl', 'fr'). Defaults to 'en'.
            password: Optional service password hash for authenticated access

        Returns:
            Dictionary containing menu structure.
            None if the request fails.

        Example:
            {
                "remoteMenuStructureVer": "22746_1",  # Version of menu structure
                "data": [                             # Array of menu structure entries
                    {
                        "pass_index": 0,              # Menu level/pass index
                        "index": 1,                   # Unique identifier for this entry
                        "type": 7,                    # Entry type (7=menu group, 1=parameter, etc.)
                        "lock": false                 # Whether this entry is locked
                    },
                    {
                        "pass_index": 0,              # Same menu level
                        "index": 46,                  # Parameter ID (matches number field in merged data)
                        "type": 1,                    # Type 1 = parameter entry
                        "lock": false                 # Not locked
                    }
                ]
            }

        """
        try:
            url = (
                f"{self.host}/econet/{API_RM_STRUCTURE_URI}?uid={self.uid}&lang={lang}"
            )
            log_url = url  # Safe URL for logging (without password)
            if password:
                url = f"{url}&password={password}"
            _LOGGER.debug("Fetching menu structure from: %s", log_url)

            data = await self._client.get(url)
            if data is None:
                _LOGGER.warning("Failed to fetch menu structure from rmStructure")
                return None

            return data.get(API_RM_DATA_KEY, {})

        except (aiohttp.ClientError, asyncio.TimeoutError, ValueError) as e:
            _LOGGER.error("Error fetching menu structure: %s", e)
            return None

    async def fetch_rm_current_data_params(
        self, lang: str = "en"
    ) -> dict[str, Any] | None:
        """Fetch current parameter values from rmCurrentDataParams endpoint.

        This endpoint provides the current values of all parameters.
        This is the main data source for sensor values in Home Assistant.

        Args:
            lang: Language code (e.g., 'en', 'pl', 'fr'). Defaults to 'en'.

        Returns:
            Dictionary containing current parameter values.
            None if the request fails.

        Example:
            {
                "remoteMenuCurrDataParamsVer": "17127_1",  # Version of current data
                "data": {                                  # Dictionary of current parameter values
                    "1": {                                # Parameter ID 1
                        "unit": 31,                       # Unit index (maps to rmParamsUnitsNames)
                        "name": "Lighter",                # Parameter name
                        "special": 1                      # Special flag/status
                    },
                    "26": {                               # Parameter ID 26
                        "unit": 1,                        # Unit index (1 = "°C")
                        "name": "Feeder temperature",     # Parameter name
                        "special": 1                      # Special flag/status
                    }
                }
            }

        """
        try:
            url = f"{self.host}/econet/{API_RM_CURRENT_DATA_PARAMS_URI}?uid={self.uid}&lang={lang}"
            _LOGGER.debug("Fetching current data params from: %s", url)

            data = await self._client.get(url)
            if data is None:
                _LOGGER.warning(
                    "Failed to fetch current data params from rmCurrentDataParams"
                )
                return None

            return data.get(API_RM_DATA_KEY, {})

        except (aiohttp.ClientError, asyncio.TimeoutError, ValueError) as e:
            _LOGGER.error("Error fetching current data params: %s", e)
            return None

    async def fetch_rm_current_data_params_edits(self) -> dict[str, Any] | None:
        """Fetch editable parameter data from rmCurrentDataParamsEdits endpoint.

        This endpoint provides information about which parameters can be edited
        and their current values. Used for number entities and controls.

        Returns:
            Dictionary containing editable parameter data.
            None if the request fails.

        Example:
            {
                "currentDataParamsEditsVer": 1,
                "data": {
                    "1280": {
                        "max": 68,
                        "type": 4,
                        "value": 40,
                        "min": 27
                    },
                    "2048": {
                        "max": 2,
                        "type": 4,
                        "value": 0,
                        "min": 0
                    }
                }
            }

        """
        try:
            url = f"{self.host}/econet/{API_RM_CURRENT_DATA_PARAMS_EDITS_URI}?uid={self.uid}"
            _LOGGER.debug("Fetching current data params edits from: %s", url)

            data = await self._client.get(url)
            if data is None:
                _LOGGER.warning(
                    "Failed to fetch current data params edits from rmCurrentDataParamsEdits"
                )
                return None

            return data.get(API_RM_DATA_KEY, {})

        except (aiohttp.ClientError, asyncio.TimeoutError, ValueError) as e:
            _LOGGER.error("Error fetching current data params edits: %s", e)
            return None

    async def fetch_rm_langs(self) -> dict[str, Any] | None:
        """Fetch available languages from rmLangs endpoint.

        This endpoint provides information about available languages for translations.

        Returns:
            Dictionary containing available languages.
            None if the request fails.

        Example:
            {
                "remoteMenuLangsVer": "20028",
                "defaultLang": "default",
                "data": [
                    {
                        "code": "pl",
                        "name": "Polski",
                        "version": "3EDBB76"
                    },
                    {
                        "default": true,
                        "code": "en",
                        "name": "English",
                        "version": "3ACA62B1"
                    }
                ]
            }

        """
        try:
            url = f"{self.host}/econet/{API_RM_LANGS_URI}?uid={self.uid}"
            _LOGGER.debug("Fetching available languages from: %s", url)

            data = await self._client.get(url)
            if data is None:
                _LOGGER.warning("Failed to fetch available languages from rmLangs")
                return None

            return data.get(API_RM_DATA_KEY, {})

        except (aiohttp.ClientError, asyncio.TimeoutError, ValueError) as e:
            _LOGGER.error("Error fetching available languages: %s", e)
            return None

    async def fetch_rm_existing_langs(self) -> dict[str, Any] | None:
        """Fetch existing language list from rmExistingLangs endpoint.

        This endpoint provides a list of languages that are actually available
        on the controller (as opposed to all possible languages).

        Returns:
            Dictionary containing existing language list.
            None if the request fails.

        """
        try:
            url = f"{self.host}/econet/{API_RM_EXISTING_LANGS_URI}?uid={self.uid}"
            _LOGGER.debug("Fetching existing languages from: %s", url)

            data = await self._client.get(url)
            if data is None:
                _LOGGER.warning(
                    "Failed to fetch existing languages from rmExistingLangs"
                )
                return None

            return data.get(API_RM_DATA_KEY, {})

        except (aiohttp.ClientError, asyncio.TimeoutError, ValueError) as e:
            _LOGGER.error("Error fetching existing languages: %s", e)
            return None

    async def fetch_rm_locks_names(self, lang: str = "en") -> dict[str, Any] | None:
        """Fetch lock/restriction messages from rmLocksNames endpoint.

        This endpoint provides messages about parameter locks and restrictions.

        Args:
            lang: Language code (e.g., 'en', 'pl', 'fr'). Defaults to 'en'.

        Returns:
            Dictionary containing lock/restriction messages.
            None if the request fails.

        """
        try:
            url = f"{self.host}/econet/{API_RM_LOCKS_NAMES_URI}?uid={self.uid}&lang={lang}"
            _LOGGER.debug("Fetching lock names from: %s", url)

            data = await self._client.get(url)
            if data is None:
                _LOGGER.warning("Failed to fetch lock names from rmLocksNames")
                return None

            return data.get(API_RM_DATA_KEY, {})

        except (aiohttp.ClientError, asyncio.TimeoutError, ValueError) as e:
            _LOGGER.error("Error fetching lock names: %s", e)
            return None

    async def fetch_rm_alarms_names(self, lang: str = "en") -> dict[str, Any] | None:
        """Fetch alarm descriptions from rmAlarmsNames endpoint.

        This endpoint provides descriptions of alarm conditions and messages.

        Args:
            lang: Language code (e.g., 'en', 'pl', 'fr'). Defaults to 'en'.

        Returns:
            Dictionary containing alarm descriptions.
            None if the request fails.

        """
        try:
            url = f"{self.host}/econet/{API_RM_ALARMS_NAMES_URI}?uid={self.uid}&lang={lang}"
            _LOGGER.debug("Fetching alarm names from: %s", url)

            data = await self._client.get(url)
            if data is None:
                _LOGGER.warning("Failed to fetch alarm names from rmAlarmsNames")
                return None

            return data.get(API_RM_DATA_KEY, {})

        except (aiohttp.ClientError, asyncio.TimeoutError, ValueError) as e:
            _LOGGER.error("Error fetching alarm names: %s", e)
            return None

    # =============================================================================
    # STEP-BY-STEP UNIFIED RM DATA METHODS
    # =============================================================================
    # These methods demonstrate how to merge rm... endpoint data step by step,
    # starting with the most fundamental endpoint (rmParamsData) as the foundation.

    async def fetch_merged_rm_data_with_names(
        self, lang: str = "en", password: str | None = None
    ) -> dict[str, Any] | None:
        """Merge rmParamsData with rmParamsNames.

        This is the first step in creating a unified data structure.
        We start with rmParamsData as the foundation and merge in parameter names.

        Args:
            lang: Language code (e.g., 'en', 'pl', 'fr'). Defaults to 'en'.
            password: Optional service password hash for authenticated access.

        Returns:
            Dictionary containing merged parameter data with names.
            None if the request fails.

        Example:
            {
                "version": "1.0-names",                    # Merged data version
                "timestamp": "2024-01-15T10:30:00Z",       # Generation timestamp
                "device": {                                # Device information
                    "uid": "ecoMAX810P-L-device",         # Device unique identifier
                    "controllerId": "ecoMAX810P-L",        # Controller type
                    "language": "en"                       # Language used
                },
                "parameters": [                            # Merged parameter array
                    {
                        "value": 60,                       # Current parameter value
                        "maxv": 100,                       # Maximum allowed value
                        "minv": 15,                        # Minimum allowed value
                        "edit": true,                      # Whether parameter can be edited
                        "unit": 5,                         # Unit index (maps to rmParamsUnitsNames)
                        "mult": 1,                          # Multiplier for value conversion
                        "offset": 0,                        # Offset for value conversion
                        "name": "100% Blow-in output",     # Human-readable name (from rmParamsNames)
                        "index": 0                          # Array index position
                    }
                ],
                "metadata": {                              # Data statistics
                    "totalParameters": 1,                   # Total number of parameters
                    "namedParameters": 1,                   # Parameters with names
                    "editableParameters": 1                 # Parameters that can be edited
                },
                "sourceEndpoints": {                        # Source endpoint information
                    "rmParamsData": "Parameter metadata (values, min/max, units, edit flags)",
                    "rmParamsNames": "Human-readable parameter names"
                }
            }

        """
        try:
            # Fetch core data in parallel
            # Pass password to rmParamsData for potential service params
            tasks = [
                self.fetch_rm_params_data(password=password),
                self.fetch_rm_params_names(lang),
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            params_data: list[dict[str, Any]] = []
            params_names: list[str] = []

            if (
                not isinstance(results[0], Exception)
                and results[0] is not None
                and isinstance(results[0], list)
            ):
                params_data = results[0]  # type: ignore[assignment]
            if (
                not isinstance(results[1], Exception)
                and results[1] is not None
                and isinstance(results[1], list)
            ):
                params_names = results[1]  # type: ignore[assignment]

            if not params_data:
                _LOGGER.warning("No parameter data available")
                return None

            # Merge parameter data with names
            merged_params: list[dict[str, Any]] = []
            for i, param in enumerate(params_data):
                if isinstance(param, dict):
                    merged_param = param.copy()  # Start with original parameter data

                    # Add name if available
                    if i < len(params_names) and isinstance(params_names, list):
                        merged_param["name"] = params_names[i]  # type: ignore[index]
                    else:
                        merged_param["name"] = f"Parameter {i}"

                    # Add index for reference
                    merged_param["index"] = i

                    merged_params.append(merged_param)

            unified_data = {
                "version": "1.0-names",
                "timestamp": datetime.now().isoformat(),
                "device": {
                    "uid": self.uid,
                    "controllerId": self.model_id,
                    "language": lang,
                },
                "parameters": merged_params,
                "metadata": {
                    "totalParameters": len(merged_params),
                    "namedParameters": len([p for p in merged_params if "name" in p]),
                    "editableParameters": len(
                        [p for p in merged_params if p.get("edit", False)]
                    ),
                },
            }

            _LOGGER.debug(
                "Merged %d parameters with names from rmParamsData + rmParamsNames",
                len(merged_params),
            )
        except (aiohttp.ClientError, asyncio.TimeoutError, ValueError) as e:
            _LOGGER.error("Error merging rmParamsData with rmParamsNames: %s", e)
            return None
        else:
            return unified_data

    async def fetch_merged_rm_data_with_names_and_descs(
        self, lang: str = "en", password: str | None = None
    ) -> dict[str, Any] | None:
        """Merge rmParamsData with rmParamsNames and rmParamsDescs.

        This step adds parameter descriptions to the existing merged structure.

        Args:
            lang: Language code (e.g., 'en', 'pl', 'fr'). Defaults to 'en'.
            password: Optional service password hash for authenticated access.

        Returns:
            Dictionary containing merged parameter data with names and descriptions.
            None if the request fails.

        """
        try:
            # Get step 1 data (pass password for service authentication)
            step1_data = await self.fetch_merged_rm_data_with_names(
                lang, password=password
            )
            if not step1_data:
                return None

            # Fetch descriptions
            params_descs = await self.fetch_rm_params_descs(lang)
            if isinstance(params_descs, Exception):
                params_descs = []

            # Merge descriptions
            for i, param in enumerate(step1_data["parameters"]):
                if isinstance(params_descs, list) and i < len(params_descs):
                    param["description"] = params_descs[i]
                else:
                    param["description"] = ""

            # Update metadata
            step1_data["version"] = "1.0-names-descs"
            step1_data["metadata"]["describedParameters"] = len(
                [p for p in step1_data["parameters"] if p.get("description")]
            )

            _LOGGER.debug(
                "Added descriptions to %d parameters from rmParamsDescs",
                len(step1_data["parameters"]),
            )
        except (aiohttp.ClientError, asyncio.TimeoutError, ValueError) as e:
            _LOGGER.error(
                "Error merging rmParamsData with rmParamsNames and rmParamsDescs: %s", e
            )
            return None
        else:
            return step1_data

    async def _get_or_fetch_static_metadata(
        self, lang: str, service_password: str | None
    ) -> dict[str, list[Any]]:
        """Get static metadata from cache or fetch and cache it.

        Static metadata rarely changes and is cached for 24 hours to reduce API load.

        Returns:
            Dict with keys: names, descs, structure, enums, units, locks

        """
        cached = self._cache.get(CACHE_KEY_STATIC_METADATA)
        if cached is not None:
            _LOGGER.debug("Using cached static metadata")
            return cached  # type: ignore[return-value]

        _LOGGER.info("Static metadata cache miss - fetching from API")

        # Fetch all static metadata in parallel
        results = await asyncio.gather(
            self.fetch_rm_params_names(lang),
            self.fetch_rm_params_descs(lang),
            self.fetch_rm_structure(lang, password=service_password),
            self.fetch_rm_params_enums(lang),
            self.fetch_rm_params_units_names(lang),
            self.fetch_rm_locks_names(lang),
            return_exceptions=True,
        )

        # Process results - use empty list for errors/None
        keys = ["names", "descs", "structure", "enums", "units", "locks"]
        metadata: dict[str, list[Any]] = {}
        for key, result in zip(keys, results, strict=True):
            if isinstance(result, Exception):
                _LOGGER.warning("Failed to fetch static metadata %s: %s", key, result)
                metadata[key] = []
            else:
                metadata[key] = result if isinstance(result, list) else []

        # Cache all together with 24 hour TTL
        self._cache.set(CACHE_KEY_STATIC_METADATA, metadata, CACHE_STATIC_METADATA_TTL)
        _LOGGER.debug(
            "Cached static metadata: %s",
            {k: len(v) for k, v in metadata.items()},
        )

        return metadata

    async def fetch_merged_rm_data(
        self,
        lang: str = "en",
        sys_params: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        """Merge rmParamsData with rmParamsNames, rmParamsDescs, rmStructure, and rmParamsEnums.

        This step adds parameter numbers, units, and enumeration data to individual parameters.
        Returns a cleaned structure with only essential data (structure, enums, metadata sections removed).

        If sys_params contains a servicePassword, authenticates with rmAccess endpoint
        before fetching data to potentially unlock service parameters.

        OPTIMIZATION: Static metadata (names, descs, structure, enums, units, locks) is cached
        for 24 hours. Only dynamic values (rmParamsData) are fetched fresh each poll.
        This reduces API calls from ~7 to ~1 per poll cycle (85% reduction).

        Args:
            lang: Language code (e.g., 'en', 'pl', 'fr'). Defaults to 'en'.
            sys_params: Optional sysParams data containing servicePassword for authentication.

        Returns:
            Dictionary containing fully merged parameter data.
            None if the request fails.

        Example:
            {
                "version": "1.0-names-descs-structure-units-indexed-enums-cleaned",  # Cleaned merged data version
                "timestamp": "2024-01-15T10:30:00Z",           # Generation timestamp
                "device": {                                    # Device information
                    "uid": "ecoMAX810P-L-device",             # Device unique identifier
                    "controllerId": "ecoMAX810P-L",            # Controller type
                    "language": "en"                           # Language used
                },
                "parameters": {                                # Indexed parameter object
                    "0": {                                     # Parameter index as key
                        "value": 60,                           # Current parameter value
                        "maxv": 100,                           # Maximum allowed value
                        "minv": 15,                            # Minimum allowed value
                        "edit": true,                          # Whether parameter can be edited
                        "unit": 5,                             # Unit index (maps to rmParamsUnitsNames)
                        "mult": 1,                              # Multiplier for value conversion
                        "offset": 0,                           # Offset for value conversion
                        "name": "100% Blow-in output",         # Human-readable name (from rmParamsNames)
                        "key": "100percent_blow_in_output",    # Generated key using generate_translation_key
                        "description": "Blow-in output when...", # Parameter description (from rmParamsDescs)
                        "index": 0,                             # Array index position
                        "number": 46,                           # Parameter ID from structure (from rmStructure)
                        "unit_name": "%"                        # Resolved unit symbol (from rmParamsUnitsNames)
                    },
                    "69": {                                     # Another parameter example
                        "value": 25,
                        "maxv": 85,
                        "minv": 20,
                        "edit": true,
                        "unit": 1,
                        "mult": 1,
                        "offset": 0,
                        "name": "Min. mixer 3 temp.",
                        "key": "min_mixer3_temp",
                        "description": "Param. allows for limiting...",
                        "index": 69,
                        "number": 67,
                        "unit_name": "°C"
                    },
                    "1": {                                      # Parameter with enum example
                        "value": 1,
                        "maxv": 1,
                        "minv": 0,
                        "edit": true,
                        "unit": 2,
                        "mult": 1,
                        "offset": 0,
                        "name": "100% Feeder operation",
                        "key": "100percent_feeder_operation",
                        "description": "Feeder operation setting...",
                        "index": 1,
                        "number": 111,
                        "unit_name": "sek.",
                        "enum": {                               # Enum data (if available)
                            "id": 1,
                            "values": ["OFF", "ON"],
                            "first": 0
                        },
                        "enum_value": "ON"                      # Current enum value (if applicable)
                    }
                }
            }

        """
        try:
            # Try service authentication if password available in sysParams
            service_password: str | None = None
            if sys_params:
                service_password = sys_params.get("servicePassword")
                if service_password:
                    auth_success = await self._authenticate_service(service_password)
                    if not auth_success:
                        _LOGGER.debug(
                            "Service authentication failed, continuing with user-level access"
                        )

            # Get static metadata from cache or fetch once (cached for 24 hours)
            meta = await self._get_or_fetch_static_metadata(lang, service_password)

            # Fetch only dynamic data fresh each poll
            params_data = await self.fetch_rm_params_data(password=service_password)
            if not params_data:
                _LOGGER.warning("No parameter data available from rmParamsData")
                return None

            # Merge parameter data with cached static metadata
            names: list[str] = meta["names"]  # type: ignore[assignment]
            descs: list[str] = meta["descs"]  # type: ignore[assignment]
            merged_params: list[dict[str, Any]] = []
            for i, param in enumerate(params_data):
                if isinstance(param, dict):
                    merged_param = param.copy()
                    merged_param["name"] = (
                        names[i] if i < len(names) else f"Parameter {i}"
                    )
                    merged_param["description"] = descs[i] if i < len(descs) else ""
                    merged_param["index"] = i
                    merged_params.append(merged_param)

            # Build unified data structure
            step2_data = {
                "version": "1.0-names-descs",
                "timestamp": datetime.now().isoformat(),
                "device": {
                    "uid": self.uid,
                    "controllerId": self.model_id,
                    "language": lang,
                },
                "parameters": merged_params,
                "metadata": {
                    "totalParameters": len(merged_params),
                    "namedParameters": len([p for p in merged_params if "name" in p]),
                    "editableParameters": len(
                        [p for p in merged_params if p.get("edit", False)]
                    ),
                    "describedParameters": len(
                        [p for p in merged_params if p.get("description")]
                    ),
                },
            }

            _LOGGER.debug(
                "Merged %d parameters with cached names/descs from rmParamsData",
                len(merged_params),
            )

            # Add parameter numbers, units, and keys using cached metadata
            structure: list[dict[str, Any]] = meta["structure"]  # type: ignore[assignment]
            enums: list[dict[str, Any]] = meta["enums"]  # type: ignore[assignment]
            units: list[str] = meta["units"]  # type: ignore[assignment]
            locks: list[str] = meta["locks"]  # type: ignore[assignment]

            self._add_parameter_numbers(merged_params, structure)
            self._add_unit_names(merged_params, units)

            # Add keys using generate_translation_key
            for merged_param in merged_params:
                if "name" in merged_param:
                    merged_param["key"] = generate_translation_key(merged_param["name"])

            # Convert parameters array to indexed dict
            parameters_dict: dict[str, dict[str, Any]] = {
                str(p.get("index", 0)): p for p in merged_params
            }
            step2_data["parameters"] = parameters_dict

            # Add enum data (priority: unit/offset > structure > smart detection)
            unit_enum_count = self._add_enum_data_from_unit_offset(
                parameters_dict, enums
            )
            struct_enum_count = self._add_enum_data_from_structure(
                parameters_dict, structure, enums
            )
            smart_enum_count = self._add_smart_enum_detection(parameters_dict, enums)

            # Add lock status to parameters
            lock_count = self._add_parameter_locks(parameters_dict, structure, locks)

            step2_data["version"] = (
                "1.0-names-descs-structure-units-indexed-enums-locks-cleaned"
            )

            _LOGGER.debug(
                "Merged %d params: enums(unit=%d, struct=%d, smart=%d), locks=%d",
                len(parameters_dict),
                unit_enum_count,
                struct_enum_count,
                smart_enum_count,
                lock_count,
            )
        except (aiohttp.ClientError, asyncio.TimeoutError, ValueError) as e:
            _LOGGER.error(
                "Error merging rmParamsData with names, descriptions, and structure: %s",
                e,
            )
            return None
        else:
            return step2_data

    def _should_detect_enum_smart(self, param: dict[str, Any]) -> bool:
        """Determine if a parameter should have smart enum detection applied.

        Args:
            param: Parameter dictionary

        Returns:
            True if parameter should have smart enum detection

        """
        # Check for empty unit_name (indicates enum-type parameter)
        unit_name = param.get("unit_name", "")
        if unit_name != "":
            return False

        # Check for special unit indices that typically indicate enums
        unit_index = param.get("unit")
        if unit_index in [31]:  # Known enum unit indices
            return True

        # Check for decimal multiplier - indicates numeric parameter, not enum
        # Parameters with mult < 1 (like 0.1) are definitely numeric values
        mult = param.get("mult", 1)
        if isinstance(mult, (int, float)) and mult < 1:
            return False

        # Check if min/max are fractional - indicates numeric parameter, not enum
        minv = param.get("minv", 0)
        maxv = param.get("maxv", 0)
        if isinstance(minv, (int, float)) and isinstance(maxv, (int, float)):
            # Fractional min or max means it's a numeric value, not enum
            if minv != int(minv) or maxv != int(maxv):
                return False

        # Check if description contains enum-like patterns
        description = param.get("description", "").lower()
        enum_patterns = [
            "off",
            "on",
            "auto",
            "manual",
            "enabled",
            "disabled",
            "start",
            "stop",
            "open",
            "close",
            "connected",
            "disconnected",
        ]

        pattern_matches = sum(1 for pattern in enum_patterns if pattern in description)
        if pattern_matches >= 2:  # At least 2 enum-like patterns
            return True

        # Check if min/max values suggest discrete states (only for integers)
        if isinstance(minv, (int, float)) and isinstance(maxv, (int, float)):
            # Only consider as enum if values are integers and range is small
            if minv == int(minv) and maxv == int(maxv):
                if 0 <= minv <= maxv <= 10 and maxv - minv <= 5:
                    return True

        return False

    def _find_best_matching_enum(
        self, param: dict[str, Any], enums: list[dict[str, Any]]
    ) -> int | None:
        """Find the best matching enum for a parameter based on description analysis.

        Args:
            param: Parameter dictionary
            enums: List of enum data from rmParamsEnums

        Returns:
            Best matching enum ID or None if no good match found

        """
        description = param.get("description", "").lower()
        name = param.get("name", "").lower()

        best_enum_id = None
        best_score = 0

        for enum_id, enum_data in enumerate(enums):
            if not isinstance(enum_data, dict) or not enum_data.get("values"):
                continue

            values = enum_data["values"]
            if not values:
                continue

            # Calculate match score
            score = 0

            # Count exact matches in description
            for value in values:
                if value and value.lower() in description:
                    score += 2  # Exact match in description

            # Count partial matches in description
            for value in values:
                if value:
                    value_words = value.lower().split()
                    for word in value_words:
                        if len(word) > 2 and word in description:
                            score += 1  # Partial match

            # Count matches in parameter name
            for value in values:
                if value and value.lower() in name:
                    score += 3  # Match in name (higher weight)

            # Bonus for perfect enum size match
            param_value = param.get("value", 0)
            minv = param.get("minv", 0)
            maxv = param.get("maxv", 0)

            if (
                isinstance(param_value, (int, float))
                and isinstance(minv, (int, float))
                and isinstance(maxv, (int, float))
            ):
                expected_range = maxv - minv + 1
                if expected_range == len(values):
                    score += 5  # Perfect size match

            # Require minimum score threshold
            if score >= 3 and score > best_score:
                best_score = score
                best_enum_id = enum_id

        return best_enum_id

    def _add_parameter_numbers(
        self, parameters: list[dict[str, Any]], structure: list[dict[str, Any]]
    ) -> None:
        """Add parameter numbers, pass_index, and data_id based on structure data.

        The pass_index field indicates access level:
        - 0 = User accessible (no password required)
        - 1, 2, 3, 4 = Requires service password (should be disabled by default)

        The structure is hierarchical:
        - type 0 = category entry (can have pass_index > 0)
        - type 1 = parameter entry (inherits pass_index from parent category)
        - type 3 = data reference entry (has data_id for sysParams mapping)
        - type 7 = menu group (resets pass_index tracking)

        Parameters inherit pass_index from their parent category.
        Note: category_index is handled separately by _add_parameter_categories().

        IMPORTANT: The structure type=1 entry's "index" field refers to the param's
        position in rmParamsData. We use a dictionary keyed by this index to look up
        the correct pass_index for each param.

        Args:
            parameters: List of parameter dictionaries to update
            structure: Structure data from rmStructure endpoint

        """
        # Build dictionary mapping param index -> pass_index
        # The structure type=1 "index" field is the param's position in rmParamsData
        param_structure_map: dict[int, int] = {}
        # Also build mapping of param index -> data_id from type 3 entries
        data_id_map: dict[int, str] = {}
        current_pass_index = 0

        for entry in structure:
            if not isinstance(entry, dict):
                continue

            entry_type = entry.get("type")
            entry_pass_index = entry.get("pass_index", 0)

            if entry_type == RM_STRUCTURE_TYPE_MENU_GROUP:
                # Menu group - reset pass_index tracking
                current_pass_index = 0
            elif entry_type == RM_STRUCTURE_TYPE_CATEGORY:
                # Category entry (type 0) - update pass_index
                current_pass_index = entry_pass_index
            elif entry_type == RM_STRUCTURE_TYPE_PARAMETER:
                # Parameter entry - map by param index (structure's index field)
                param_index = entry.get("index")
                if param_index is not None:
                    param_structure_map[param_index] = current_pass_index
            elif entry_type == RM_STRUCTURE_TYPE_DATA_REF:
                # Data reference entry - has data_id for sysParams mapping
                param_index = entry.get("index")
                data_id = entry.get("data_id")
                if param_index is not None and data_id is not None:
                    data_id_map[param_index] = data_id

        # Add numbers, pass_index, and data_id to parameters
        # Use the param's index to look up in the structure map
        for param in parameters:
            param_index = param.get("index", 0)

            if param_index in param_structure_map:
                param["number"] = param_index  # Number is same as index
                param["pass_index"] = param_structure_map[param_index]
            else:
                # Fallback for params not in structure
                param["number"] = param_index
                param["pass_index"] = 0  # Default to user-accessible

            # Add data_id if available from type 3 entries
            if param_index in data_id_map:
                param["data_id"] = data_id_map[param_index]

    def _add_unit_names(
        self, parameters: list[dict[str, Any]], units: list[str]
    ) -> None:
        """Add unit names to parameters based on unit indices.

        Args:
            parameters: List of parameter dictionaries to update
            units: List of unit names from rmParamsUnitsNames endpoint


        """
        for param in parameters:
            # Add unit name if available
            unit_index = param.get("unit")
            if (
                unit_index is not None
                and isinstance(unit_index, int)
                and 0 <= unit_index < len(units)
                and isinstance(units[unit_index], str)
            ):
                param["unit_name"] = units[unit_index]
            else:
                param["unit_name"] = ""

    def _add_parameter_locks(
        self,
        parameters_dict: dict[str, dict[str, Any]],
        structure: list[dict[str, Any]],
        lock_names: list[str] | None = None,
    ) -> int:
        """Add lock status to parameters based on structure data.

        Adds lock information including:
        - locked: bool - Whether the parameter is currently locked
        - lock_index: int | None - Index into rmLocksNames for lock reason
        - lock_reason: str | None - Human-readable lock reason message

        Args:
            parameters_dict: Dictionary of parameters indexed by string keys
            structure: Structure data from rmStructure endpoint
            lock_names: Lock reason messages from rmLocksNames endpoint

        Returns:
            Number of parameters with lock status added

        """
        # Build mapping: parameter_number -> (lock_status, lock_index)
        param_to_lock: dict[int, tuple[bool, int | None]] = {}

        for entry in structure:
            if not isinstance(entry, dict):
                continue

            entry_type = entry.get("type")
            entry_index = entry.get("index")
            entry_lock = entry.get("lock", False)
            entry_lock_index = entry.get("lock_index")

            if entry_type == RM_STRUCTURE_TYPE_PARAMETER:
                if entry_index is not None:
                    param_to_lock[entry_index] = (entry_lock, entry_lock_index)

        # Add lock status to parameters based on their number
        lock_count = 0
        for param in parameters_dict.values():
            param_number = param.get("number")
            if isinstance(param_number, int) and param_number in param_to_lock:
                locked, lock_index = param_to_lock[param_number]
                param["locked"] = locked
                param["lock_index"] = lock_index

                # Add lock reason from rmLocksNames if available
                if locked and lock_index is not None and lock_names:
                    if 0 <= lock_index < len(lock_names):
                        param["lock_reason"] = lock_names[lock_index]
                    else:
                        param["lock_reason"] = "Parameter locked"
                else:
                    param["lock_reason"] = None

                if locked:
                    lock_count += 1
            else:
                param["locked"] = False
                param["lock_index"] = None
                param["lock_reason"] = None

        return lock_count

    def _add_enum_data_from_unit_offset(
        self,
        parameters_dict: dict[str, dict[str, Any]],
        enums: list[dict[str, Any]],
    ) -> int:
        """Add enum data to parameters based on unit=31 and offset field.

        According to ecoNET24 web interface JS code (dev_set3.js):
        - When unit == 31 (ENUM_UNIT), the offset field contains the enum index
        - This is the authoritative source for enum type parameters

        Args:
            parameters_dict: Dictionary of parameters indexed by string keys
            enums: List of enum data from rmParamsEnums endpoint

        Returns:
            Number of enums added from unit/offset references

        """
        # ENUM_UNIT constant from ecoNET24 JS code
        ENUM_UNIT = 31

        enum_count = 0
        for param in parameters_dict.values():
            # Check if this parameter has unit=31 (ENUM_UNIT)
            if param.get("unit") == ENUM_UNIT:
                # The offset field contains the enum index
                enum_id = param.get("offset", 0)

                # Get enum data if available
                if isinstance(enum_id, int) and 0 <= enum_id < len(enums):
                    enum_data = enums[enum_id]
                    # Validate enum_data is a dict before accessing
                    if not isinstance(enum_data, dict):
                        continue

                    param["enum"] = {
                        "id": enum_id,
                        "values": enum_data.get("values", []),
                        "first": enum_data.get("first", 0),
                        "detection_method": "unit_offset",
                    }

                    # Add current enum value if parameter has a value and it's within enum range
                    if "value" in param and param["value"] is not None:
                        param_value = param["value"]
                        enum_values = enum_data.get("values", [])
                        first_value = enum_data.get("first", 0)

                        # Calculate the actual enum index
                        enum_index = param_value - first_value
                        if 0 <= enum_index < len(enum_values):
                            param["enum_value"] = enum_values[enum_index]

                    enum_count += 1
                    _LOGGER.debug(
                        "Enum from unit/offset: param=%s, enum_id=%d, values=%s",
                        param.get("name", "unknown"),
                        enum_id,
                        enum_data.get("values", [])[:4],  # First 4 values for logging
                    )

        return enum_count

    def _add_enum_data_from_structure(
        self,
        parameters_dict: dict[str, dict[str, Any]],
        structure: list[dict[str, Any]],
        enums: list[dict[str, Any]],
    ) -> int:
        """Add enum data to parameters based on structure data_id references.

        This is a fallback method for parameters that don't have unit=31.

        Args:
            parameters_dict: Dictionary of parameters indexed by string keys
            structure: Structure data from rmStructure endpoint
            enums: List of enum data from rmParamsEnums endpoint

        Returns:
            Number of enums added from structure references

        """
        # Create structure enum map
        structure_enum_map = {}
        for entry in structure:
            if isinstance(entry, dict) and "data_id" in entry:
                param_index = entry.get("index")
                enum_id = int(entry.get("data_id", 0))
                if param_index is not None:
                    structure_enum_map[param_index] = enum_id

        # Add enum data to parameters
        enum_count = 0
        for param_index_str, param in parameters_dict.items():
            # Skip if already has enum data (from unit/offset method)
            if "enum" in param:
                continue

            param_index = int(param_index_str)

            # Check if this parameter has an enum reference AND no unit_name (enum-type parameter)
            if param_index in structure_enum_map and param.get("unit_name") == "":
                enum_id = structure_enum_map[param_index]

                # Get enum data if available
                if isinstance(enum_id, int) and 0 <= enum_id < len(enums):
                    enum_data = enums[enum_id]
                    # Validate enum_data is a dict before accessing
                    if not isinstance(enum_data, dict):
                        continue

                    param["enum"] = {
                        "id": enum_id,
                        "values": enum_data.get("values", []),
                        "first": enum_data.get("first", 0),
                        "detection_method": "structure_data_id",
                    }

                    # Add current enum value if parameter has a value and it's within enum range
                    if "value" in param and param["value"] is not None:
                        param_value = param["value"]
                        enum_values = enum_data.get("values", [])
                        first_value = enum_data.get("first", 0)

                        # Calculate the actual enum index
                        enum_index = param_value - first_value
                        if 0 <= enum_index < len(enum_values):
                            param["enum_value"] = enum_values[enum_index]

                    enum_count += 1

        return enum_count

    def _add_smart_enum_detection(
        self, parameters_dict: dict[str, dict[str, Any]], enums: list[dict[str, Any]]
    ) -> int:
        """Add enum data using smart detection for parameters without structure enum references.

        Args:
            parameters_dict: Dictionary of parameters indexed by string keys
            enums: List of enum data from rmParamsEnums endpoint

        Returns:
            Number of enums added via smart detection

        """
        smart_enum_count = 0
        for param in parameters_dict.values():
            # Skip if already has enum data
            if "enum" in param:
                continue

            # Check if this parameter needs smart enum detection
            if self._should_detect_enum_smart(param):
                best_enum_id = self._find_best_matching_enum(param, enums)
                if (
                    best_enum_id is not None
                    and isinstance(best_enum_id, int)
                    and 0 <= best_enum_id < len(enums)
                ):
                    enum_data = enums[best_enum_id]
                    # Validate enum_data is a dict before accessing
                    if not isinstance(enum_data, dict):
                        continue

                    param["enum"] = {
                        "id": best_enum_id,
                        "values": enum_data.get("values", []),
                        "first": enum_data.get("first", 0),
                        "detection_method": "smart_detection",
                    }

                    # Add current enum value if parameter has a value and it's within enum range
                    if "value" in param and param["value"] is not None:
                        param_value = param["value"]
                        enum_values = enum_data.get("values", [])
                        first_value = enum_data.get("first", 0)

                        # Calculate the actual enum index
                        enum_index = param_value - first_value
                        if 0 <= enum_index < len(enum_values):
                            param["enum_value"] = enum_values[enum_index]

                    smart_enum_count += 1

        return smart_enum_count


async def make_api(hass: HomeAssistant, cache: MemCache, data: dict):
    """Create api object."""
    return await Econet300Api.create(
        EconetClient(
            data["host"],
            data["username"],
            data["password"],
            async_get_clientsession(hass),
        ),
        cache,
    )
