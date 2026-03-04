"""Config flow for ecoNET300 integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry, ConfigFlowResult, OptionsFlow
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from .api import make_api
from .common import AuthError
from .const import (
    API_REG_PARAMS_DATA_URI,
    API_REG_PARAMS_URI,
    API_RM_CURRENT_DATA_PARAMS_URI,
    CONF_CUSTOM_ENTITIES,
    CONF_ENTRY_DESCRIPTION,
    CONF_ENTRY_TITLE,
    CUSTOM_ENTITY_COMPONENTS,
    CUSTOM_ENTITY_TYPE_BINARY_SENSOR,
    CUSTOM_ENTITY_TYPE_SENSOR,
    CUSTOM_SENSOR_DEVICE_CLASS_OPTIONS,
    CUSTOM_SENSOR_PRECISION_OPTIONS,
    CUSTOM_SENSOR_UNIT_OPTIONS,
    DOMAIN,
    SERVICE_COORDINATOR,
    STATIC_REGPARAMS_DATA_IDS,
    STATIC_REGPARAMS_KEYS,
    UNIT_INDEX_TO_NAME,
)
from .mem_cache import MemCache

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("host"): str,
        vol.Required("username"): str,
        vol.Required("password"): str,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""
    cache = MemCache()
    info = {}

    try:
        api = await make_api(hass, cache, data)
        info["uid"] = api.uid
    except AuthError as auth_error:
        raise InvalidAuth from auth_error
    except TimeoutError as timeout_error:
        raise CannotConnect from timeout_error

    return info


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ecoNET300 integration."""

    VERSION = 1

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow:
        """Get the options flow for this handler."""
        return EconetOptionsFlowHandler()

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}

        try:
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except InvalidAuth:
            errors["base"] = "invalid_auth"
        except Exception:
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            user_input["uid"] = info["uid"]

            await self.async_set_unique_id(user_input["uid"])
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=CONF_ENTRY_TITLE,
                description=CONF_ENTRY_DESCRIPTION,
                data=user_input,
            )

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle reconfiguration of the integration."""
        entry_id = self.context.get("entry_id")
        if entry_id is None:
            return self.async_abort(reason="reconfigure_failed")
        entry = self.hass.config_entries.async_get_entry(entry_id)
        if entry is None:
            return self.async_abort(reason="reconfigure_failed")

        if user_input is None:
            # Pre-fill the form with current values (password not shown for security)
            return self.async_show_form(
                step_id="reconfigure",
                data_schema=vol.Schema(
                    {
                        vol.Required("host", default=entry.data.get("host", "")): str,
                        vol.Required(
                            "username", default=entry.data.get("username", "")
                        ): str,
                        vol.Required("password"): str,
                    }
                ),
                description_placeholders={"device_name": entry.title},
            )

        errors = {}

        try:
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except InvalidAuth:
            errors["base"] = "invalid_auth"
        except Exception:
            _LOGGER.exception("Unexpected exception during reconfigure")
            errors["base"] = "unknown"
        else:
            # Update the config entry with new data
            return self.async_update_reload_and_abort(
                entry,
                data={
                    **entry.data,
                    "host": user_input["host"],
                    "username": user_input["username"],
                    "password": user_input["password"],
                    "uid": info["uid"],
                },
            )

        # Show form again with errors
        return self.async_show_form(
            step_id="reconfigure",
            data_schema=vol.Schema(
                {
                    vol.Required("host", default=user_input.get("host", "")): str,
                    vol.Required(
                        "username", default=user_input.get("username", "")
                    ): str,
                    vol.Required("password"): str,
                }
            ),
            errors=errors,
            description_placeholders={"device_name": entry.title},
        )


def _get_unmapped_keys(
    coordinator_data: dict[str, Any] | None,
    source: str,
) -> dict[str, Any]:
    """Return keys from the given endpoint not already covered by static entities.

    Args:
        coordinator_data: Full coordinator data dict.
        source: One of API_REG_PARAMS_URI, API_REG_PARAMS_DATA_URI,
                or API_RM_CURRENT_DATA_PARAMS_URI.

    Returns:
        Dict of {key: display_info} for keys available for custom selection.

    """
    if coordinator_data is None:
        return {}

    if source == API_REG_PARAMS_URI:
        reg_params = coordinator_data.get("regParams")
        if not reg_params or not isinstance(reg_params, dict):
            return {}
        return {
            k: v
            for k, v in reg_params.items()
            if k not in STATIC_REGPARAMS_KEYS and v is not None
        }

    if source == API_REG_PARAMS_DATA_URI:
        rpd = coordinator_data.get("regParamsData")
        if not rpd or not isinstance(rpd, dict):
            return {}
        rm_data = coordinator_data.get("rmData") or {}
        cdp_ids = set((rm_data.get("currentDataParams") or {}).keys())
        return {
            k: v
            for k, v in rpd.items()
            if k not in STATIC_REGPARAMS_DATA_IDS and k not in cdp_ids and v is not None
        }

    if source == API_RM_CURRENT_DATA_PARAMS_URI:
        rm_data = coordinator_data.get("rmData") or {}
        cdp = rm_data.get("currentDataParams")
        if not cdp or not isinstance(cdp, dict):
            return {}
        return {
            k: v
            for k, v in cdp.items()
            if k not in STATIC_REGPARAMS_DATA_IDS and isinstance(v, dict)
        }

    return {}


def _build_multiselect_options(
    unmapped: dict[str, Any],
    source: str,
) -> dict[str, str]:
    """Build {key: label} dict for the multi-select UI.

    Args:
        unmapped: Output of _get_unmapped_keys.
        source: Endpoint source identifier.

    """
    options: dict[str, str] = {}

    if source == API_REG_PARAMS_URI:
        for key in sorted(unmapped):
            val = unmapped[key]
            display_val = str(val)[:30]
            options[key] = f"{key}: {display_val}"
        return options

    if source == API_REG_PARAMS_DATA_URI:
        for key in sorted(unmapped, key=int):
            val = unmapped[key]
            type_hint = type(val).__name__
            display_val = str(val)[:30]
            options[key] = f"ID {key}: {display_val} ({type_hint})"
        return options

    if source == API_RM_CURRENT_DATA_PARAMS_URI:
        for key in sorted(unmapped, key=int):
            meta = unmapped[key]
            name = meta.get("name", "?")
            unit_idx = meta.get("unit", 0)
            unit_name = UNIT_INDEX_TO_NAME.get(unit_idx, "")
            options[key] = (
                f"ID {key}: {name} ({unit_name})" if unit_name else f"ID {key}: {name}"
            )
        return options

    return options


class EconetOptionsFlowHandler(OptionsFlow):
    """Handle options flow for ecoNET300."""

    def __init__(self) -> None:
        """Initialize the options flow."""
        self._selected_source: str = API_REG_PARAMS_URI
        self._selected_keys: list[str] = []
        self._configure_index: int = 0
        self._entity_configs: dict[str, dict[str, Any]] = {}

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Show the options menu."""
        return self.async_show_menu(
            step_id="init",
            menu_options=["connection_settings", "custom_entities"],
        )

    # ------------------------------------------------------------------
    # Connection settings
    # ------------------------------------------------------------------
    async def async_step_connection_settings(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage connection settings."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:
                _LOGGER.exception("Unexpected exception during reconfiguration")
                errors["base"] = "unknown"
            else:
                new_data = {
                    **self.config_entry.data,
                    "host": user_input["host"],
                    "username": user_input["username"],
                    "password": user_input["password"],
                }
                self.hass.config_entries.async_update_entry(
                    self.config_entry,
                    data=new_data,
                )
                self.hass.async_create_task(
                    self.hass.config_entries.async_reload(self.config_entry.entry_id)
                )
                return self.async_create_entry(
                    title="", data=dict(self.config_entry.options)
                )

        options_schema = vol.Schema(
            {
                vol.Required(
                    "host", default=self.config_entry.data.get("host", "")
                ): str,
                vol.Required(
                    "username", default=self.config_entry.data.get("username", "")
                ): str,
                vol.Required("password"): str,
            }
        )

        return self.async_show_form(
            step_id="connection_settings",
            data_schema=options_schema,
            errors=errors,
        )

    # ------------------------------------------------------------------
    # Custom entities: Step 1 – select endpoint
    # ------------------------------------------------------------------
    async def async_step_custom_entities(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Let user choose which API endpoint to browse."""
        if user_input is not None:
            self._selected_source = user_input.get("endpoint", API_REG_PARAMS_URI)
            return await self._show_key_selection()

        schema = vol.Schema(
            {
                vol.Required("endpoint", default=API_REG_PARAMS_URI): vol.In(
                    {
                        API_REG_PARAMS_URI: "regParams (named parameters)",
                        API_REG_PARAMS_DATA_URI: "regParamsData (numeric IDs)",
                        API_RM_CURRENT_DATA_PARAMS_URI: "rmCurrentDataParams (with metadata)",
                    }
                ),
            }
        )

        return self.async_show_form(
            step_id="custom_entities",
            data_schema=schema,
        )

    # ------------------------------------------------------------------
    # Custom entities: Step 2 – select keys
    # ------------------------------------------------------------------
    async def _show_key_selection(self) -> ConfigFlowResult:
        """Show multi-select of available keys from the chosen endpoint."""
        coordinator = self.hass.data[DOMAIN][self.config_entry.entry_id][
            SERVICE_COORDINATOR
        ]
        unmapped = _get_unmapped_keys(coordinator.data, self._selected_source)
        available = _build_multiselect_options(unmapped, self._selected_source)

        if not available:
            return self.async_abort(reason="no_unmapped_params")

        existing = self.config_entry.options.get(CONF_CUSTOM_ENTITIES, {})
        already_selected = [
            cfg["key"]
            for cfg in existing.values()
            if cfg.get("source") == self._selected_source
            and cfg.get("key") in available
        ]

        schema = vol.Schema(
            {
                vol.Optional(
                    "selected_params", default=already_selected
                ): cv.multi_select(available),
            }
        )

        return self.async_show_form(
            step_id="select_params",
            data_schema=schema,
        )

    async def async_step_select_params(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle selected parameter keys."""
        if user_input is None:
            return await self._show_key_selection()

        self._selected_keys = user_input.get("selected_params", [])

        if not self._selected_keys:
            # Remove all custom entities for this source, keep others
            existing = self.config_entry.options.get(CONF_CUSTOM_ENTITIES, {})
            kept = {
                uid: cfg
                for uid, cfg in existing.items()
                if cfg.get("source") != self._selected_source
            }
            new_options = {**self.config_entry.options, CONF_CUSTOM_ENTITIES: kept}
            self.hass.async_create_task(
                self.hass.config_entries.async_reload(self.config_entry.entry_id)
            )
            return self.async_create_entry(title="", data=new_options)

        self._configure_index = 0
        self._entity_configs = {}
        return await self.async_step_configure_entity()

    # ------------------------------------------------------------------
    # Custom entities: Step 3 – per-key configuration
    # ------------------------------------------------------------------
    async def async_step_configure_entity(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Configure each selected key: name, component, type, category."""
        if user_input is not None:
            key = self._selected_keys[self._configure_index]
            uid = f"{self._selected_source}:{key}"
            self._entity_configs[uid] = {
                "source": self._selected_source,
                "key": key,
                "name": user_input.get("name", f"Parameter {key}").strip()
                or f"Parameter {key}",
                "component": user_input.get("component", "boiler"),
                "entity_type": user_input.get("entity_type", CUSTOM_ENTITY_TYPE_SENSOR),
                "entity_category": user_input.get("entity_category"),
            }

            if user_input.get("entity_type") == CUSTOM_ENTITY_TYPE_SENSOR:
                return await self.async_step_configure_sensor()

            return await self._advance_or_save()

        key = self._selected_keys[self._configure_index]
        default_name = self._get_default_name(key)
        existing = self.config_entry.options.get(CONF_CUSTOM_ENTITIES, {})
        uid = f"{self._selected_source}:{key}"
        old_cfg = existing.get(uid, {})

        schema = vol.Schema(
            {
                vol.Required("name", default=old_cfg.get("name", default_name)): str,
                vol.Required(
                    "component", default=old_cfg.get("component", "boiler")
                ): vol.In(CUSTOM_ENTITY_COMPONENTS),
                vol.Required(
                    "entity_type",
                    default=old_cfg.get("entity_type", CUSTOM_ENTITY_TYPE_SENSOR),
                ): vol.In(
                    {
                        CUSTOM_ENTITY_TYPE_SENSOR: "Sensor",
                        CUSTOM_ENTITY_TYPE_BINARY_SENSOR: "Binary sensor",
                    }
                ),
                vol.Optional(
                    "entity_category",
                    default=old_cfg.get("entity_category"),
                ): vol.In(
                    {
                        None: "Default (no category)",
                        "diagnostic": "Diagnostic",
                    }
                ),
            }
        )

        return self.async_show_form(
            step_id="configure_entity",
            data_schema=schema,
            description_placeholders={"key": key, "source": self._selected_source},
        )

    # ------------------------------------------------------------------
    # Custom entities: Step 3b – sensor-specific configuration
    # ------------------------------------------------------------------
    async def async_step_configure_sensor(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Configure sensor-specific properties: unit, device class, precision."""
        if user_input is not None:
            key = self._selected_keys[self._configure_index]
            uid = f"{self._selected_source}:{key}"
            self._entity_configs[uid].update(
                {
                    "native_unit": user_input.get("native_unit"),
                    "device_class": user_input.get("device_class"),
                    "precision": user_input.get("precision"),
                }
            )
            return await self._advance_or_save()

        key = self._selected_keys[self._configure_index]
        uid = f"{self._selected_source}:{key}"
        existing = self.config_entry.options.get(CONF_CUSTOM_ENTITIES, {})
        old_cfg = existing.get(uid, {})

        schema = vol.Schema(
            {
                vol.Optional(
                    "native_unit",
                    default=old_cfg.get("native_unit"),
                ): vol.In(CUSTOM_SENSOR_UNIT_OPTIONS),
                vol.Optional(
                    "device_class",
                    default=old_cfg.get("device_class"),
                ): vol.In(CUSTOM_SENSOR_DEVICE_CLASS_OPTIONS),
                vol.Optional(
                    "precision",
                    default=old_cfg.get("precision"),
                ): vol.In(CUSTOM_SENSOR_PRECISION_OPTIONS),
            }
        )

        entity_name = self._entity_configs.get(uid, {}).get("name", key)
        return self.async_show_form(
            step_id="configure_sensor",
            data_schema=schema,
            description_placeholders={"name": entity_name},
        )

    async def _advance_or_save(self) -> ConfigFlowResult:
        """Advance to the next key or save if all keys are configured."""
        self._configure_index += 1
        if self._configure_index >= len(self._selected_keys):
            return await self._save_custom_entities()
        return await self.async_step_configure_entity()

    def _get_default_name(self, key: str) -> str:
        """Determine default display name for a key based on source."""
        if self._selected_source == API_RM_CURRENT_DATA_PARAMS_URI:
            coordinator = self.hass.data[DOMAIN][self.config_entry.entry_id][
                SERVICE_COORDINATOR
            ]
            rm_data = (coordinator.data or {}).get("rmData") or {}
            cdp = rm_data.get("currentDataParams") or {}
            meta = cdp.get(key)
            if isinstance(meta, dict) and meta.get("name"):
                return meta["name"]
        if self._selected_source == API_REG_PARAMS_URI:
            return key
        return f"Parameter {key}"

    async def _save_custom_entities(self) -> ConfigFlowResult:
        """Persist configured entities and reload integration."""
        existing = self.config_entry.options.get(CONF_CUSTOM_ENTITIES, {})

        # Keep entities from other sources, replace entities for current source
        kept = {
            uid: cfg
            for uid, cfg in existing.items()
            if cfg.get("source") != self._selected_source
        }
        kept.update(self._entity_configs)

        new_options = {**self.config_entry.options, CONF_CUSTOM_ENTITIES: kept}
        self.hass.async_create_task(
            self.hass.config_entries.async_reload(self.config_entry.entry_id)
        )
        return self.async_create_entry(title="", data=new_options)


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
