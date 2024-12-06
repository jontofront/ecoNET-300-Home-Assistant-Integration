"""Functions used in Econet300 integration,."""

import re


def camel_to_snake(key: str) -> str:
    """Convert camel case return from API to snake case to match translations keys structure."""
    key = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", key)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", key).lower()


def get_key_by_value(search_dict: dict, search_value: str) -> str | None:
    """Get a key from a dict by passing its value."""
    for key, value in search_dict.items():
        if value == search_value:
            return key
    return None
