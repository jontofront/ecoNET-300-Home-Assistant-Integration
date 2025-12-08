"""Econet300 API class describing methods of getting and setting data."""

import asyncio
from datetime import datetime
from http import HTTPStatus
import logging
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
    API_RM_ALARMS_NAMES_URI,
    API_RM_CATS_DESCS_URI,
    API_RM_CATS_NAMES_URI,
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
    CONTROL_PARAMS,
    NUMBER_MAP,
)
from .mem_cache import MemCache

_LOGGER = logging.getLogger(__name__)


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
                _LOGGER.debug("Fetching data from URL: %s (Attempt %d)", url, attempt)

                async with await self._session.get(
                    url, auth=self._auth, timeout=ClientTimeout(total=15)
                ) as resp:
                    _LOGGER.debug("Received response with status: %s", resp.status)
                    if resp.status == HTTPStatus.UNAUTHORIZED:
                        _LOGGER.error("Unauthorized access to URL: %s", url)
                        raise AuthError

                    if resp.status != HTTPStatus.OK:
                        try:
                            error_message = await resp.text()
                        except (aiohttp.ClientError, aiohttp.ClientResponseError) as e:
                            error_message = f"Could not retrieve error message: {e}"

                        _LOGGER.error(
                            "Failed to fetch data from URL: %s (Status: %s) - Response: %s",
                            url,
                            resp.status,
                            error_message,
                        )
                        return None

                    data = await resp.json()
                    _LOGGER.debug("Fetched data: %s", data)
                    return data

            except TimeoutError:
                _LOGGER.warning("Timeout error, retry(%i/%i)", attempt, max_attempts)
                await asyncio.sleep(1)
            attempt += 1
        _LOGGER.error(
            "Failed to fetch data from %s after %d attempts", url, max_attempts
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
        """Econet300 API initialization."""
        sys_params = await self.fetch_sys_params()

        if sys_params is None:
            _LOGGER.error("Failed to fetch system parameters.")
            return

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
        """Set param value in Econet300 API.

        Dynamically determines the correct endpoint based on parameter type:
        - Numeric string (e.g., "49", "55") -> rmNewParam?newParamIndex={param}
        - Legacy setpoints in NUMBER_MAP (e.g., "1280") -> rmCurrNewParam?newParamKey={param}
        - Control parameters (e.g., "BOILER_CONTROL") -> newParam?newParamName={param}
        - Default -> newParam?newParamName={param}
        """
        if param is None:
            _LOGGER.info(
                "Requested param set for: '%s' but mapping for this param does not exist",
                param,
            )
            return False

        # Determine endpoint dynamically based on parameter format
        # Check if param is a numeric string (from merged data parameters)
        if isinstance(param, str) and param.isdigit():
            # Numeric parameter ID from merged data -> use rmNewParam
            url = f"{self.host}/econet/rmNewParam?newParamIndex={param}&newParamValue={value}"
            _LOGGER.debug(
                "Using rmNewParam endpoint for parameter ID %s: %s",
                param,
                url,
            )
        elif param in NUMBER_MAP:
            # Legacy setpoint parameters (1280, 1281, etc.) -> use rmCurrNewParam
            url = f"{self.host}/econet/rmCurrNewParam?newParamKey={param}&newParamValue={value}"
            _LOGGER.debug(
                "Using rmCurrNewParam endpoint for setpoint parameter %s: %s",
                param,
                url,
            )
        elif param in CONTROL_PARAMS:
            # Control parameters (BOILER_CONTROL, etc.) -> use newParam with name
            url = f"{self.host}/econet/newParam?newParamName={param}&newParamValue={value}"
            _LOGGER.debug(
                "Using newParam endpoint for control parameter %s: %s", param, url
            )
        else:
            # Default: assume it's a parameter name -> use newParam with name
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

    async def _force_refresh_params_edits(self):
        """Force refresh paramsEdits data by fetching fresh data and updating cache."""
        try:
            _LOGGER.debug("Force refreshing paramsEdits data")
            fresh_data = await self._fetch_api_data_by_key(
                API_EDITABLE_PARAMS_LIMITS_URI, API_EDITABLE_PARAMS_LIMITS_DATA
            )
            if fresh_data:
                self._cache.set(API_EDITABLE_PARAMS_LIMITS_DATA, fresh_data)
                _LOGGER.debug("Successfully refreshed paramsEdits data: %s", fresh_data)
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
            _LOGGER.debug("Fetched regParamsData: %s", regParamsData)
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
        _LOGGER.info("Calling fetch_reg_params method")
        regParams = await self._fetch_api_data_by_key(
            API_REG_PARAMS_URI, API_REG_PARAMS_PARAM_DATA
        )
        _LOGGER.debug("Fetched regParams data: %s", regParams)
        _LOGGER.debug("Type of regParams: %s", type(regParams))
        return regParams

    async def fetch_sys_params(self) -> dict[str, Any] | None:
        """Fetch and return the regParam data from ip/econet/sysParams endpoint."""
        _LOGGER.debug(
            "fetch_sys_params called: Fetching parameters for registry '%s' from host '%s'",
            self.host,
            API_SYS_PARAMS_URI,
        )
        sysParams = await self._fetch_api_data_by_key(API_SYS_PARAMS_URI)
        _LOGGER.debug("Fetched sysParams data: %s", sysParams)
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
            _LOGGER.error(
                "Client error occurred while fetching data from endpoint: %s, error: %s",
                endpoint,
                e,
            )
        except asyncio.TimeoutError as e:
            _LOGGER.error(
                "A timeout error occurred while fetching data from endpoint: %s, error: %s",
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

    async def fetch_rm_params_data(self) -> dict[str, Any] | None:
        """Fetch parameter metadata from rmParamsData endpoint.

        This endpoint provides parameter metadata including min/max values, units,
        and other configuration information for each parameter.

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
            _LOGGER.debug("Fetching parameter data from: %s", url)

            data = await self._client.get(url)
            if data is None:
                _LOGGER.warning("Failed to fetch parameter data from rmParamsData")
                return None

            return data.get(API_RM_DATA_KEY, {})

        except (aiohttp.ClientError, asyncio.TimeoutError, ValueError) as e:
            _LOGGER.error("Error fetching parameter data: %s", e)
            return None

    async def fetch_rm_params_descs(self, lang: str = "en") -> dict[str, Any] | None:
        """Fetch parameter descriptions from rmParamsDescs endpoint.

        This endpoint provides detailed descriptions of parameters in the specified language.
        Used for help text and parameter explanations in the web interface.

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

            data = await self._client.get(url)
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

    async def fetch_rm_cats_names(self, lang: str = "en") -> dict[str, Any] | None:
        """Fetch category names from rmCatsNames endpoint.

        This endpoint provides category names for organizing parameters in the web interface.

        Args:
            lang: Language code (e.g., 'en', 'pl', 'fr'). Defaults to 'en'.

        Returns:
            Dictionary containing category names.
            None if the request fails.

        """
        try:
            url = (
                f"{self.host}/econet/{API_RM_CATS_NAMES_URI}?uid={self.uid}&lang={lang}"
            )
            _LOGGER.debug("Fetching category names from: %s", url)

            data = await self._client.get(url)
            if data is None:
                _LOGGER.warning("Failed to fetch category names from rmCatsNames")
                return None

            return data.get(API_RM_DATA_KEY, {})

        except (aiohttp.ClientError, asyncio.TimeoutError, ValueError) as e:
            _LOGGER.error("Error fetching category names: %s", e)
            return None

    async def fetch_rm_cats_descs(self, lang: str = "en") -> dict[str, Any] | None:
        """Fetch category descriptions from rmCatsDescs endpoint.

        This endpoint provides detailed descriptions of parameter categories.

        Args:
            lang: Language code (e.g., 'en', 'pl', 'fr'). Defaults to 'en'.

        Returns:
            Dictionary containing category descriptions.
            None if the request fails.

        """
        try:
            url = (
                f"{self.host}/econet/{API_RM_CATS_DESCS_URI}?uid={self.uid}&lang={lang}"
            )
            _LOGGER.debug("Fetching category descriptions from: %s", url)

            data = await self._client.get(url)
            if data is None:
                _LOGGER.warning(
                    "Failed to fetch category descriptions from rmCatsDescs"
                )
                return None

            return data.get(API_RM_DATA_KEY, {})

        except (aiohttp.ClientError, asyncio.TimeoutError, ValueError) as e:
            _LOGGER.error("Error fetching category descriptions: %s", e)
            return None

    async def fetch_rm_structure(self, lang: str = "en") -> dict[str, Any] | None:
        """Fetch menu structure from rmStructure endpoint.

        This endpoint provides the hierarchical menu structure for the web interface,
        showing how parameters are organized and grouped.

        Args:
            lang: Language code (e.g., 'en', 'pl', 'fr'). Defaults to 'en'.

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
            _LOGGER.debug("Fetching menu structure from: %s", url)

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
        self, lang: str = "en"
    ) -> dict[str, Any] | None:
        """Merge rmParamsData with rmParamsNames.

        This is the first step in creating a unified data structure.
        We start with rmParamsData as the foundation and merge in parameter names.

        Args:
            lang: Language code (e.g., 'en', 'pl', 'fr'). Defaults to 'en'.

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
            tasks = [
                self.fetch_rm_params_data(),
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
            merged_params = []
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
        self, lang: str = "en"
    ) -> dict[str, Any] | None:
        """Merge rmParamsData with rmParamsNames and rmParamsDescs.

        This step adds parameter descriptions to the existing merged structure.

        Args:
            lang: Language code (e.g., 'en', 'pl', 'fr'). Defaults to 'en'.

        Returns:
            Dictionary containing merged parameter data with names and descriptions.
            None if the request fails.

        """
        try:
            # Get step 1 data
            step1_data = await self.fetch_merged_rm_data_with_names(lang)
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

    async def fetch_merged_rm_data_with_names_descs_and_structure(
        self, lang: str = "en"
    ) -> dict[str, Any] | None:
        """Merge rmParamsData with rmParamsNames, rmParamsDescs, rmStructure, and rmParamsEnums.

        This step adds parameter numbers, units, and enumeration data to individual parameters.
        Returns a cleaned structure with only essential data (structure, enums, metadata sections removed).

        Args:
            lang: Language code (e.g., 'en', 'pl', 'fr'). Defaults to 'en'.

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
            # Get step 2 data
            step2_data = await self.fetch_merged_rm_data_with_names_and_descs(lang)
            if not step2_data:
                return None

            # Fetch additional data in parallel (always include categories for dynamic entities)
            tasks = [
                self.fetch_rm_structure(lang),
                self.fetch_rm_params_enums(lang),
                self.fetch_rm_params_units_names(lang),
                self.fetch_rm_cats_names(lang),
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            structure: list[dict[str, Any]] = []
            enums: list[dict[str, Any]] = []
            units: list[str] = []
            categories: list[str] = []

            if (
                not isinstance(results[0], Exception)
                and results[0] is not None
                and isinstance(results[0], list)
            ):
                structure = results[0]  # type: ignore[assignment]
            if (
                not isinstance(results[1], Exception)
                and results[1] is not None
                and isinstance(results[1], list)
            ):
                enums = results[1]  # type: ignore[assignment]
            if (
                not isinstance(results[2], Exception)
                and results[2] is not None
                and isinstance(results[2], list)
            ):
                units = results[2]  # type: ignore[assignment]
            if (
                not isinstance(results[3], Exception)
                and results[3] is not None
                and isinstance(results[3], list)
            ):
                categories = results[3]  # type: ignore[assignment]

            # Add parameter numbers, units, and keys using helper methods
            self._add_parameter_numbers(step2_data["parameters"], structure)
            self._add_unit_names(step2_data["parameters"], units)

            # Add keys using generate_translation_key
            for param in step2_data["parameters"]:
                if "name" in param:
                    param["key"] = generate_translation_key(param["name"])

            # Convert parameters array to object with index keys
            parameters_dict = {}
            for param in step2_data["parameters"]:
                param_index = param.get("index", 0)
                parameters_dict[param_index] = param

            # Replace parameters array with indexed object
            step2_data["parameters"] = parameters_dict

            # Add enum data using helper methods
            enum_count = self._add_enum_data_from_structure(
                parameters_dict, structure, enums
            )
            smart_enum_count = self._add_smart_enum_detection(parameters_dict, enums)

            # Always add category information (for dynamic entity generation)
            category_count = 0
            if categories:
                category_count = self._add_parameter_categories(
                    parameters_dict, structure, categories
                )
                _LOGGER.debug(
                    "Added category information to %d parameters", category_count
                )

            # Add lock status to parameters
            lock_count = self._add_parameter_locks(parameters_dict, structure)
            _LOGGER.debug("Added lock status to %d locked parameters", lock_count)

            # Update version to include categories and locks
            step2_data["version"] = (
                "1.0-names-descs-structure-units-indexed-enums-categories-locks-cleaned"
            )

            # Extract parameter entries from structure for logging
            param_structure_entries = [
                item
                for item in structure
                if isinstance(item, dict) and item.get("type") == 1
            ]

            _LOGGER.debug(
                "Added parameter numbers (%d), units (%d types), enum mappings (%d structure + %d smart), categories (%d) from rmStructure + rmParamsEnums + rmParamsUnitsNames + rmCatsNames. Converted to indexed format with cleaned structure.",
                len(param_structure_entries),
                len(units),
                enum_count,
                smart_enum_count,
                category_count,
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

        # Check if min/max values suggest discrete states
        minv = param.get("minv", 0)
        maxv = param.get("maxv", 0)
        if isinstance(minv, (int, float)) and isinstance(maxv, (int, float)):
            # If range is small and discrete, likely an enum
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
        """Add parameter numbers based on structure data.

        Args:
            parameters: List of parameter dictionaries to update
            structure: Structure data from rmStructure endpoint

        """
        # Extract parameter entries from structure (type == 1)
        param_structure_entries = [
            item
            for item in structure
            if isinstance(item, dict) and item.get("type") == 1
        ]

        # Add numbers to parameters based on structure mapping
        for param in parameters:
            param_index = param.get("index", 0)

            # Use the structure entry index if available
            if param_index < len(param_structure_entries):
                structure_entry = param_structure_entries[param_index]
                param["number"] = structure_entry.get("index", param_index)
            else:
                # Fallback to parameter index if no structure entry
                param["number"] = param_index

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
                and unit_index < len(units)
                and isinstance(units[unit_index], str)
            ):
                param["unit_name"] = units[unit_index]
            else:
                param["unit_name"] = ""

    def _add_parameter_categories(
        self,
        parameters_dict: dict[str, dict[str, Any]],
        structure: list[dict[str, Any]],
        categories: list[str],
    ) -> int:
        """Add category information to parameters based on structure data.

        Maps parameters to their categories by parsing the structure:
        - type 7 = category/menu group (index maps to rmCatsNames array)
        - type 1 = parameter (index is the parameter number)
        - Parameters follow their category in the structure

        Args:
            parameters_dict: Dictionary of parameters indexed by string keys
            structure: Structure data from rmStructure endpoint
            categories: Category names from rmCatsNames endpoint

        Returns:
            Number of parameters with category information added

        """
        if not categories:
            return 0

        # Map parameter numbers to their categories
        # Structure: type 7 = category, type 1 = parameter
        # Parameters follow their category in the structure
        param_to_category: dict[int, str] = {}
        current_category_index: int | None = None

        for entry in structure:
            if not isinstance(entry, dict):
                continue

            entry_type = entry.get("type")
            entry_index = entry.get("index")

            if entry_type == 7:  # Category/menu group
                # This is a category - store it
                if isinstance(entry_index, int) and entry_index < len(categories):
                    current_category_index = entry_index
            elif entry_type == 1:  # Parameter
                # This is a parameter - map it to current category
                if isinstance(entry_index, int) and current_category_index is not None:
                    category_name = categories[current_category_index]
                    param_to_category[entry_index] = category_name

        # Add category to parameters
        category_count = 0
        for param in parameters_dict.values():
            param_number = param.get("number")
            if isinstance(param_number, int) and param_number in param_to_category:
                param["category"] = param_to_category[param_number]
                category_count += 1

        return category_count

    def _add_parameter_locks(
        self,
        parameters_dict: dict[str, dict[str, Any]],
        structure: list[dict[str, Any]],
    ) -> int:
        """Add lock status to parameters based on structure data.

        Args:
            parameters_dict: Dictionary of parameters indexed by string keys
            structure: Structure data from rmStructure endpoint

        Returns:
            Number of parameters with lock status added

        """
        # Build mapping: parameter_number -> lock_status
        param_to_lock: dict[int, bool] = {}

        for entry in structure:
            if not isinstance(entry, dict):
                continue

            entry_type = entry.get("type")
            entry_index = entry.get("index")
            entry_lock = entry.get("lock", False)

            if entry_type == 1:  # Parameter
                if entry_index is not None:
                    param_to_lock[entry_index] = entry_lock

        # Add lock status to parameters based on their number
        lock_count = 0
        for param in parameters_dict.values():
            param_number = param.get("number")
            if isinstance(param_number, int) and param_number in param_to_lock:
                param["locked"] = param_to_lock[param_number]
                if param_to_lock[param_number]:
                    lock_count += 1
            else:
                param["locked"] = False

        return lock_count

    def _add_enum_data_from_structure(
        self,
        parameters_dict: dict[str, dict[str, Any]],
        structure: list[dict[str, Any]],
        enums: list[dict[str, Any]],
    ) -> int:
        """Add enum data to parameters based on structure data_id references.

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
            param_index = int(param_index_str)

            # Check if this parameter has an enum reference AND no unit_name (enum-type parameter)
            if param_index in structure_enum_map and param.get("unit_name") == "":
                enum_id = structure_enum_map[param_index]

                # Get enum data if available
                if isinstance(enum_id, int) and 0 <= enum_id < len(enums):
                    enum_data = enums[enum_id]
                    param["enum"] = {
                        "id": enum_id,
                        "values": enum_data.get("values", []),
                        "first": enum_data.get("first", 0),
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
