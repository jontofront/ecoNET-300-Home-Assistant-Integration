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
    CONF_CUSTOM_ENTITIES,
    CONF_ENTRY_DESCRIPTION,
    CONF_ENTRY_TITLE,
    CUSTOM_ENTITY_TYPE_BINARY_SENSOR,
    CUSTOM_ENTITY_TYPE_SENSOR,
    DOMAIN,
    SERVICE_COORDINATOR,
    STATIC_REGPARAMS_DATA_IDS,
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


def _classify_regparam_value(value: Any) -> str:
    """Classify a regParamsData value as sensor or binary_sensor."""
    if isinstance(value, bool):
        return CUSTOM_ENTITY_TYPE_BINARY_SENSOR
    return CUSTOM_ENTITY_TYPE_SENSOR


def _get_unmapped_regparams(
    coordinator_data: dict[str, Any] | None,
) -> dict[str, Any]:
    """Return regParamsData entries not covered by static or CDP entities.

    Returns a dict of {param_id: raw_value} for IDs that have no
    RM metadata (not in currentDataMerged) and no static mapping.
    """
    if coordinator_data is None:
        return {}

    reg_params_data = coordinator_data.get("regParamsData")
    if not reg_params_data or not isinstance(reg_params_data, dict):
        return {}

    cdm_ids = set(coordinator_data.get("currentDataMerged", {}).keys())

    unmapped: dict[str, Any] = {}
    for param_id, value in reg_params_data.items():
        if param_id in STATIC_REGPARAMS_DATA_IDS:
            continue
        if param_id in cdm_ids:
            continue
        if value is None:
            continue
        unmapped[param_id] = value

    return unmapped


def _build_multiselect_options(
    unmapped: dict[str, Any],
    type_filter: str | None = None,
) -> dict[str, str]:
    """Build {param_id: label} dict for the multi-select UI.

    Args:
        unmapped: Output of _get_unmapped_regparams.
        type_filter: If set, only include IDs matching this entity type.

    """
    options: dict[str, str] = {}
    for param_id, value in sorted(unmapped.items(), key=lambda x: int(x[0])):
        detected_type = _classify_regparam_value(value)
        if type_filter and detected_type != type_filter:
            continue
        type_hint = type(value).__name__
        display_val = str(value)
        if len(display_val) > 30:
            display_val = display_val[:27] + "..."
        options[param_id] = f"ID {param_id}: {display_val} ({type_hint})"
    return options


class EconetOptionsFlowHandler(OptionsFlow):
    """Handle options flow for ecoNET300."""

    def __init__(self) -> None:
        """Initialize the options flow."""
        self._selected_ids: list[str] = []

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Show the options menu."""
        return self.async_show_menu(
            step_id="init",
            menu_options=["connection_settings", "custom_entities"],
        )

    # ------------------------------------------------------------------
    # Connection settings (moved from old async_step_init)
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
    # Custom entities: type filter
    # ------------------------------------------------------------------
    async def async_step_custom_entities(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Let user choose parameter type filter before browsing IDs."""
        if user_input is not None:
            type_filter = user_input.get("type_filter", "all")
            return await self._show_param_selection(type_filter)

        schema = vol.Schema(
            {
                vol.Required("type_filter", default="all"): vol.In(
                    {
                        "all": "All parameters",
                        CUSTOM_ENTITY_TYPE_SENSOR: "Numeric only (sensor)",
                        CUSTOM_ENTITY_TYPE_BINARY_SENSOR: "Boolean only (binary sensor)",
                    }
                ),
            }
        )

        return self.async_show_form(
            step_id="custom_entities",
            data_schema=schema,
        )

    async def _show_param_selection(self, type_filter: str) -> ConfigFlowResult:
        """Show multi-select of available regParamsData IDs."""
        coordinator = self.hass.data[DOMAIN][self.config_entry.entry_id][
            SERVICE_COORDINATOR
        ]
        unmapped = _get_unmapped_regparams(coordinator.data)
        filter_val = type_filter if type_filter != "all" else None
        available = _build_multiselect_options(unmapped, filter_val)

        if not available:
            return self.async_abort(reason="no_unmapped_params")

        existing = self.config_entry.options.get(CONF_CUSTOM_ENTITIES, {})
        already_selected = [pid for pid in existing if pid in available]

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

    # ------------------------------------------------------------------
    # Custom entities: ID selection
    # ------------------------------------------------------------------
    async def async_step_select_params(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle selected parameter IDs."""
        if user_input is None:
            return await self._show_param_selection("all")

        self._selected_ids = user_input.get("selected_params", [])

        if not self._selected_ids:
            new_options = {**self.config_entry.options, CONF_CUSTOM_ENTITIES: {}}
            self.hass.async_create_task(
                self.hass.config_entries.async_reload(self.config_entry.entry_id)
            )
            return self.async_create_entry(title="", data=new_options)

        return await self.async_step_name_entities()

    # ------------------------------------------------------------------
    # Custom entities: naming step
    # ------------------------------------------------------------------
    async def async_step_name_entities(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Let user assign custom names to selected IDs."""
        coordinator = self.hass.data[DOMAIN][self.config_entry.entry_id][
            SERVICE_COORDINATOR
        ]
        unmapped = _get_unmapped_regparams(coordinator.data)
        existing = self.config_entry.options.get(CONF_CUSTOM_ENTITIES, {})

        if user_input is not None:
            custom_entities: dict[str, dict[str, str]] = {}
            for param_id in self._selected_ids:
                name_key = f"name_{param_id}"
                name = user_input.get(name_key, f"Parameter {param_id}").strip()
                if not name:
                    name = f"Parameter {param_id}"
                raw_value = unmapped.get(param_id)
                entity_type = _classify_regparam_value(raw_value)
                custom_entities[param_id] = {
                    "name": name,
                    "entity_type": entity_type,
                }

            new_options = {
                **self.config_entry.options,
                CONF_CUSTOM_ENTITIES: custom_entities,
            }
            self.hass.async_create_task(
                self.hass.config_entries.async_reload(self.config_entry.entry_id)
            )
            return self.async_create_entry(title="", data=new_options)

        # Build schema with a text field per selected ID
        schema_dict: dict[vol.Marker, Any] = {}
        for param_id in self._selected_ids:
            old_name = existing.get(param_id, {}).get("name", f"Parameter {param_id}")
            schema_dict[
                vol.Optional(
                    f"name_{param_id}",
                    default=old_name,
                    description={"suggested_value": old_name},
                )
            ] = str

        return self.async_show_form(
            step_id="name_entities",
            data_schema=vol.Schema(schema_dict),
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
