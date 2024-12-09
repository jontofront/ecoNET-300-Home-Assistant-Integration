"""Econet300 API class describing methods of getting and setting data."""

import asyncio
from http import HTTPStatus
import logging
from typing import Any

import aiohttp
from aiohttp import BasicAuth, ClientSession
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    API_EDITABLE_PARAMS_LIMITS_DATA,
    API_EDITABLE_PARAMS_LIMITS_URI,
    API_REG_PARAMS_DATA_PARAM_DATA,
    API_REG_PARAMS_DATA_URI,
    API_REG_PARAMS_PARAM_DATA,
    API_REG_PARAMS_URI,
    API_SYS_PARAMS_PARAM_HW_VER,
    API_SYS_PARAMS_PARAM_MODEL_ID,
    API_SYS_PARAMS_PARAM_SW_REV,
    API_SYS_PARAMS_PARAM_UID,
    API_SYS_PARAMS_URI,
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

    class AuthError(Exception):
        """Raised when authentication fails."""


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
                    url, auth=self._auth, timeout=10
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

    def _set_device_property(
        self, sys_params, param_key, attr_name, param_desc, default=None
    ):
        """Set an attribute from system parameters with logging if unavailable."""
        if param_key not in sys_params:
            _LOGGER.warning(
                "%s not in sys_params - cannot set proper %s", param_key, param_desc
            )
            setattr(self, attr_name, default)
        else:
            setattr(self, attr_name, sys_params[param_key])

    async def set_param(self, param, value) -> bool:
        """Set param value in Econet300 API."""
        if param is None:
            _LOGGER.warning(
                "Requested param set for: '%s' but mapping for this param does not exist",
                param,
            )
            return False

        data = await self._client.get(
            f"{self.host}/econet/rmCurrNewParam?newParamKey={param}&newParamValue={value}"
        )
        if data is None or "result" not in data:
            return False
        if data["result"] != "OK":
            return False
        self._cache.set(param, value)

        return True

    async def get_param_limits(self, param: str):
        """Fetch and return the limits for a particular parameter from the Econet 300 API, using a cache for efficient retrieval if available."""
        if not self._cache.exists(API_EDITABLE_PARAMS_LIMITS_DATA):
            limits = await self._fetch_reg_key(
                API_EDITABLE_PARAMS_LIMITS_URI, API_EDITABLE_PARAMS_LIMITS_DATA
            )
            self._cache.set(API_EDITABLE_PARAMS_LIMITS_DATA, limits)

        # Retrieve limits from the cache
        limits = self._cache.get(API_EDITABLE_PARAMS_LIMITS_DATA)

        if not param:
            _LOGGER.warning("Parameter name is None. Unable to fetch limits.")
            return None

        if param not in limits:
            _LOGGER.warning(
                "Limits for parameter '%s' do not exist. Available limits: %s",
                param,
                limits,
            )
            return None

        # Extract and log the limits
        curr_limits = limits[param]
        _LOGGER.debug("Limits '%s'", limits)
        _LOGGER.debug("Limits for edit param '%s': %s", param, curr_limits)
        return Limits(curr_limits["min"], curr_limits["max"])

    async def fetch_reg_params_data(self) -> dict[str, Any]:
        """Fetch data from econet/regParamsData."""
        try:
            regParamsData = await self._fetch_reg_key(
                API_REG_PARAMS_DATA_URI, API_REG_PARAMS_DATA_PARAM_DATA
            )
        except DataError as e:
            _LOGGER.error("Error fetching regParamsData: %s", e)
            return {}
        else:
            _LOGGER.debug("Fetched regParamsData: %s", regParamsData)
            return regParamsData

    async def fetch_param_edit_data(self):
        """Fetch and return the limits for a particular parameter from the Econet 300 API, using a cache for efficient retrieval if available."""
        if not self._cache.exists(API_EDITABLE_PARAMS_LIMITS_DATA):
            limits = await self._fetch_reg_key(
                API_EDITABLE_PARAMS_LIMITS_URI, API_EDITABLE_PARAMS_LIMITS_DATA
            )
            self._cache.set(API_EDITABLE_PARAMS_LIMITS_DATA, limits)

        return self._cache.get(API_EDITABLE_PARAMS_LIMITS_DATA)

    async def _fetch_reg_key(self, reg, data_key: str | None = None):
        """Fetch a key from the json-encoded data returned by the API for a given registry If key is None, then return whole data."""
        data = await self.fetch_sys_params()

        if data is None:
            raise DataError(f"Data fetched by API for reg: {reg} is None")

        if data_key is None:
            return data

        if data_key not in data:
            _LOGGER.debug(data)
            raise DataError(f"Data for key: {data_key} does not exist")

        return data[data_key]

    async def fetch_sys_params(self) -> dict[str, Any]:
        """Fetch and return the regParam data from ip/econet/sysParams endpoint."""
        _LOGGER.debug(
            "fetch_sys_params called: Fetching parameters for registry '%s' from host '%s'",
            self.host,
            API_SYS_PARAMS_URI,
        )

        return await self._client.get(f"{self.host}/econet/{API_SYS_PARAMS_URI}")

    async def fetch_reg_params(self) -> dict[str, Any]:
        """Fetch and return the regParams data from ip/econet/regParams endpoint."""
        _LOGGER.info("Calling fetch_reg_params method")
        regParams = await self._fetch_reg_names(
            API_REG_PARAMS_URI, API_REG_PARAMS_PARAM_DATA
        )
        _LOGGER.debug("Fetched regParams data: %s", regParams)
        return regParams

    async def _fetch_reg_names(self, reg, data_key: str | None = None):
        """Fetch a key from the json-encoded data returned by the API for a given registry If key is None, then return whole data."""
        data = await self._client.get(f"{self.host}/econet/{reg}")

        if data is None:
            raise DataError(f"Data fetched by API for reg: {reg} is None")

        if data_key is None:
            return data

        if data_key not in data:
            _LOGGER.debug(data)
            raise DataError(f"Data for key: {data_key} does not exist")
        value = data[data_key]
        _LOGGER.debug("Processed value for key '%s': %s", data_key, value)
        return value


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
