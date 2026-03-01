"""Common utility functions for the ecoNET-300 integration.

This module contains helper functions for:
- Name conversion (camelCase to snake_case)
- Translation key generation
- Parameter type detection (number, switch, select, sensor)
- Parameter validation and locking

For detailed documentation on the validation layer and entity type detection,
see: docs/DYNAMIC_ENTITY_VALIDATION.md
"""

import logging
import re

from .const import (
    AVAILABLE_NUMBER_OF_MIXERS,
    CDP_SPECIAL_SKIP,
    CDP_UNIT_BINARY_STATE,
    COMPONENT_BOILER,
    COMPONENT_BUFFER,
    COMPONENT_HUW,
    COMPONENT_LAMBDA,
    COMPONENT_MIXER_1,
    COMPONENT_MIXER_2,
    COMPONENT_MIXER_3,
    COMPONENT_MIXER_4,
    COMPONENT_SOLAR,
    DEFAULT_COMPONENT_STATUS,
    STATIC_REGPARAMS_DATA_IDS,
)

_LOGGER = logging.getLogger(__name__)


def camel_to_snake(key: str) -> str:
    """Convert camel case return from API to snake case to match translations keys structure."""
    # Handle special cases first
    special_mappings = {
        "ecoSter": "ecoster",
        "ecoSOL": "ecosol",
        "ecoMAX": "ecomax",
        "ecoNET": "econet",
    }

    # Apply special mappings
    for camel_case, snake_case in special_mappings.items():
        if camel_case in key:
            key = key.replace(camel_case, snake_case)

    # Now apply the standard camel to snake conversion
    key = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", key)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", key).lower()


def generate_translation_key(name: str) -> str:
    """Convert parameter name to Home Assistant translation key."""
    # Replace common characters
    key = name.replace(" ", "_")
    key = key.replace("%", "percent")
    key = key.replace(".", "")
    key = key.replace("-", "_")
    key = key.replace("(", "")
    key = key.replace(")", "")
    key = key.replace(":", "")
    key = key.replace("'", "")
    key = key.replace('"', "")

    # Convert to lowercase
    key = key.lower()

    # Handle specific patterns: mixer 3 room therm -> mixer3_room_therm
    # Pattern: word + space + number + space + word -> word + number + underscore + word
    key = re.sub(r"(\w+)_(\d+)_(\w+)", r"\1\2_\3", key)

    # Handle other similar patterns: word + number + space + word -> word + number + underscore + word
    return re.sub(r"(\w+)(\d+)_(\w+)", r"\1\2_\3", key)


def extract_device_group_from_name(
    name: str | None, for_information: bool = False
) -> tuple[int | None, str | None]:
    """Extract device group from parameter name using heuristics.

    Analyzes parameter names to determine the most appropriate device grouping
    based on keywords like "mixer 1", "lambda", "boiler", "HUW", etc.

    This helps correctly group parameters that may be miscategorized in the
    ecoNET rmStructure data (e.g., mixer parameters under "Chimney sweep mode").

    Args:
        name: Parameter name (e.g., "Heating curve. mixer 2", "Lambda sensor")
        for_information: If True, returns Information-type categories for sensors
                        If False, returns Settings-type categories for numbers

    Returns:
        Tuple of (category_index, category_name) for the matched device group,
        or (None, None) if no specific device pattern is found.

    Category indices (from rmCatsNames):
        - Settings: 2=Boiler, 3=HUW, 5-8=Mixer 1-4, 32=Buffer, 43=Lambda
        - Information: 16-19=Information mixer 1-4

    """
    if not name:
        return None, None

    name_lower = name.lower()

    # Check for mixer patterns (highest priority for mixer-specific params)
    # Matches: "mixer 1", "mixer1", "Mixer 2", etc.
    mixer_match = re.search(r"mixer\s*(\d+)", name_lower)
    if mixer_match:
        mixer_num = int(mixer_match.group(1))
        if 1 <= mixer_num <= AVAILABLE_NUMBER_OF_MIXERS:
            if for_information:
                # Information mixer devices use formula: 15 + mixer_num
                return 15 + mixer_num, f"Information mixer {mixer_num}"
            # Mixer settings use formula: 4 + mixer_num
            return 4 + mixer_num, f"Mixer {mixer_num} settings"

    # Check for lambda sensor
    if "lambda" in name_lower:
        return 43, "Lambda sensor"

    # Check for HUW (Hot Utility Water / DHW)
    # Case-insensitive check for "huw" or "dhw"
    if "huw" in name_lower or "dhw" in name_lower:
        return 3, "HUW settings"

    # Check for buffer
    if "buffer" in name_lower:
        return 32, "Buffer settings"

    # Check for boiler/burner/feed/feeder/fan/blow-in/air/fuel/oxygen (all part of boiler system)
    if any(
        keyword in name_lower
        for keyword in [
            "boiler",
            "burner",
            "feed",
            "feeder",
            "fan",
            "blow",
            "air",
            "fuel",
            "oxygen",
        ]
    ):
        return 2, "Boiler settings"

    # Check for alarm-related parameters (system-wide)
    if "alarm" in name_lower:
        return 1, "Information"

    return None, None


def is_binary_enum(enum_values: list[str] | None) -> bool:
    """Check if enum represents a binary ON/OFF type switch.

    Binary enums have exactly 2 values representing ON/OFF states.
    Note: Only checks the first 2 values since enum.values may have
    incorrect mappings from the API.

    Args:
        enum_values: List of enum option strings (e.g., ["OFF", "ON"])

    Returns:
        True if first 2 enum values represent binary state patterns

    """
    if not enum_values or len(enum_values) < 2:
        return False

    # Take only first 2 values (min/max determines actual option count)
    check_values = enum_values[:2]
    values_lower = [v.lower() for v in check_values]

    # Common binary patterns
    binary_patterns = [
        {"off", "on"},
        {"no", "yes"},
        {"disable", "enable"},
        {"disabled", "enabled"},
        {"inactive", "active"},
        {"false", "true"},
        {"0", "1"},
    ]

    return set(values_lower) in binary_patterns


def get_on_off_values(
    enum_values: list[str], enum_first: int = 0
) -> tuple[int, int] | None:
    """Get the API values for OFF and ON states from enum.

    Analyzes enum values to determine which index represents OFF and ON,
    then returns the corresponding API values (enum_first + index).

    Args:
        enum_values: List of enum option strings (e.g., ["OFF", "ON"])
        enum_first: First value offset from enum data (default 0)

    Returns:
        Tuple of (off_value, on_value) for API calls, or None if not binary

    """
    if not enum_values:
        return None

    # Take only first 2 values (min/max determines actual option count)
    check_values = enum_values[:2] if len(enum_values) >= 2 else enum_values

    if len(check_values) != 2:
        return None

    values_lower = [v.lower() for v in check_values]

    # Patterns where first value is OFF
    off_first_patterns = ["off", "no", "disable", "disabled", "inactive", "false", "0"]

    # Patterns where first value is ON
    on_first_patterns = ["on", "yes", "enable", "enabled", "active", "true", "1"]

    # Determine which index is OFF and which is ON
    if values_lower[0] in off_first_patterns:
        # First value is OFF (index 0), second is ON (index 1)
        return enum_first, enum_first + 1

    if values_lower[0] in on_first_patterns:
        # First value is ON (index 0), second is OFF (index 1)
        return enum_first + 1, enum_first

    # Default: assume first is OFF, second is ON
    return enum_first, enum_first + 1


def _get_num_options(param: dict) -> int | None:
    """Calculate number of options from min/max values.

    Args:
        param: Parameter dictionary from mergedData

    Returns:
        Number of options if calculable, None otherwise

    """
    minv = param.get("minv")
    maxv = param.get("maxv")

    if minv is None or maxv is None:
        return None

    try:
        return int(maxv) - int(minv) + 1
    except (ValueError, TypeError):
        return None


def should_be_select_entity(param: dict) -> bool:
    """Check if parameter should be a Select entity.

    Select entities are for editable parameters with enum having 3+ values.
    Uses min/max range to determine option count, as enum.values may have
    incorrect mappings.

    Args:
        param: Parameter dictionary from mergedData

    Returns:
        True if parameter should be a Select entity

    """
    if not param.get("edit", False):
        return False

    # Locked parameters should not be editable selects
    if is_parameter_locked(param):
        return False

    enum_data = param.get("enum")
    if not enum_data:
        return False

    # Use min/max to determine actual number of options (more reliable)
    num_options = _get_num_options(param)
    if num_options is not None:
        return num_options >= 3

    # Fallback to enum.values length when min/max unavailable
    # Simply check if there are 3+ options - the binary pattern check is not
    # relevant for length-based detection since is_binary_enum only examines
    # the first 2 values and would incorrectly filter enums like ["off", "on", "auto"]
    enum_values = enum_data.get("values", [])
    return len(enum_values) >= 3


def should_be_switch_entity(param: dict) -> bool:
    """Check if parameter should be a Switch entity.

    Switch entities are for editable parameters with binary enum (2 values).
    Uses min/max range to determine option count, as enum.values may have
    incorrect mappings.

    Args:
        param: Parameter dictionary from mergedData

    Returns:
        True if parameter should be a Switch entity

    """
    if not param.get("edit", False):
        return False

    # Locked parameters should not be editable switches
    if is_parameter_locked(param):
        return False

    enum_data = param.get("enum")
    if not enum_data:
        return False

    enum_values = enum_data.get("values", [])

    # Use min/max to determine actual number of options (more reliable)
    num_options = _get_num_options(param)
    if num_options is not None:
        # Must have exactly 2 options
        if num_options != 2:
            return False
    # Fallback: require exactly 2 enum values when min/max unavailable or invalid
    # This prevents 3+ option enums (e.g., ["off", "on", "auto"]) from being
    # misclassified as switches just because their first 2 values match a binary pattern
    elif len(enum_values) != 2:
        return False

    # Check if enum values represent binary pattern
    return is_binary_enum(enum_values)


def mixer_exists(coordinator_data: dict | None, mixer_num: int) -> bool:
    """Check if a mixer exists by verifying regParams data.

    Mixers that don't exist in the boiler will have None values for their
    temperature sensors. This function checks if the mixer temperature
    data is available.

    Args:
        coordinator_data: Coordinator data dict containing regParams
        mixer_num: Mixer number (1-6)

    Returns:
        True if mixer has valid temperature data, False otherwise

    """
    if not coordinator_data:
        return False

    reg_params = coordinator_data.get("regParams", {})
    if not reg_params:
        return False

    mixer_temp_key = f"mixerTemp{mixer_num}"
    return reg_params.get(mixer_temp_key) is not None


def ecoster_exists(coordinator_data: dict | None) -> bool:
    """Check if ecoSTER panel is connected by verifying moduleEcoSTERSoftVer.

    If moduleEcoSTERSoftVer is None, no ecoSTER panel is connected
    and ecoSTER-related entities should not be created.

    Args:
        coordinator_data: Coordinator data dict containing sysParams

    Returns:
        True if ecoSTER is connected, False otherwise

    """
    if not coordinator_data:
        return False

    sys_params = coordinator_data.get("sysParams", {})
    if not sys_params:
        return False

    return sys_params.get("moduleEcoSTERSoftVer") is not None


def is_ecoster_related(param: dict) -> bool:
    """Check if a parameter is related to ecoSTER panel.

    Checks if the parameter description mentions ecoSTER.

    Args:
        param: Parameter dictionary from mergedData

    Returns:
        True if parameter is ecoSTER-related, False otherwise

    """
    description = param.get("description", "")
    return "ecoster" in description.lower()


def validate_parameter_data(param: dict) -> tuple[bool, str]:
    """Validate parameter from mergedData before entity creation.

    Performs comprehensive validation of parameter data to ensure
    it has all required fields and valid values before creating entities.

    Args:
        param: Parameter dictionary from mergedData

    Returns:
        Tuple of (is_valid, error_message). If valid, error_message is empty.

    """
    # Check required fields
    if not param.get("key"):
        return False, "Missing parameter key"

    if not param.get("name"):
        return False, "Missing parameter name"

    # Validate numeric range if editable number (has unit_name, no enum)
    is_editable = param.get("edit", False)
    has_unit = bool(param.get("unit_name"))
    has_enum = "enum" in param and param.get("enum") is not None

    if is_editable and has_unit and not has_enum:
        minv = param.get("minv")
        maxv = param.get("maxv")

        if minv is None or maxv is None:
            return False, "Missing min/max for editable number parameter"

        try:
            min_float = float(minv)
            max_float = float(maxv)
            if min_float >= max_float:
                return False, f"Invalid min/max range: {minv} >= {maxv}"
        except (ValueError, TypeError):
            return False, f"Non-numeric min/max values: {minv}, {maxv}"

    # Validate enum if present
    enum_data = param.get("enum")
    if enum_data is not None:
        if not isinstance(enum_data, dict):
            return False, "Invalid enum structure (not a dict)"

        enum_values = enum_data.get("values")
        if enum_values is not None and not isinstance(enum_values, list):
            return False, "Invalid enum values (not a list)"

        if enum_values is not None and len(enum_values) == 0:
            return False, "Empty enum values list"

    return True, ""


def is_parameter_locked(param: dict) -> bool:
    """Check if parameter is locked using existing mergedData field.

    The lock status is determined by the rmStructure endpoint and
    added to parameters during the merge process in api.py.

    Args:
        param: Parameter dictionary from mergedData

    Returns:
        True if parameter is locked and cannot be modified

    """
    return param.get("locked", False)


def get_lock_reason(param: dict) -> str | None:
    """Get human-readable lock reason from mergedData.

    Lock reasons come from the rmLocksNames endpoint and provide
    user-friendly explanations for why a parameter is locked.

    Examples of lock reasons:
        - "Requires turn off the controller."
        - "Weather control enabled."
        - "HUW mode off."
        - "Function unavailable."
        - "Lambda sensor calibration in progress"

    Args:
        param: Parameter dictionary from mergedData

    Returns:
        Lock reason string if available, None otherwise

    """
    return param.get("lock_reason")


def detect_connected_components(reg_params: dict | None) -> dict[str, bool]:
    """Detect which physical components are connected based on regParams data.

    Checks temperature sensors and status values to determine if each
    component is physically connected to the boiler system.

    Args:
        reg_params: regParams data from coordinator containing sensor readings

    Returns:
        Dictionary mapping component names to connection status

    """
    if not reg_params:
        return DEFAULT_COMPONENT_STATUS.copy()

    def is_connected(key: str) -> bool:
        """Check if a sensor value indicates component is connected."""
        val = reg_params.get(key)
        return (
            val is not None
            and val != -1
            and (not isinstance(val, (int, float)) or val > 0)
        )

    return {
        COMPONENT_BOILER: True,  # Boiler is always present
        COMPONENT_HUW: is_connected("tempCWU"),
        COMPONENT_MIXER_1: is_connected("mixerTemp1"),
        COMPONENT_MIXER_2: is_connected("mixerTemp2"),
        COMPONENT_MIXER_3: is_connected("mixerTemp3"),
        COMPONENT_MIXER_4: is_connected("mixerTemp4"),
        COMPONENT_LAMBDA: reg_params.get("lambdaStatus") is not None,
        COMPONENT_BUFFER: is_connected("tempUpperBuffer")
        or is_connected("tempLowerBuffer"),
        COMPONENT_SOLAR: is_connected("tempSolarCollector"),
    }


def get_entity_component(
    name: str | None,
    key: str | None,
    description: str | None = None,
    sequence_num: int | None = None,
) -> str:
    """Determine which component an entity belongs to based on name/key/description.

    Analyzes parameter name, key, and description to assign it to the appropriate
    physical component device.

    Args:
        name: Parameter name (e.g., "HUW preset temperature")
        key: Parameter key (e.g., "huw_preset_temperature")
        description: Parameter description for additional context
        sequence_num: Sequence number for duplicate parameters (1-4 for mixers)

    Returns:
        Component identifier: "boiler", "huw", "mixer_1" through "mixer_4",
        "lambda", "buffer", or "solar"

    """
    if not name and not key:
        return COMPONENT_BOILER

    # Combine name, key, and description for pattern matching
    text = f"{name or ''} {key or ''} {description or ''}".lower()

    # Check for specific mixer (numbered patterns have highest priority)
    mixer_components = [
        COMPONENT_MIXER_1,
        COMPONENT_MIXER_2,
        COMPONENT_MIXER_3,
        COMPONENT_MIXER_4,
    ]
    for i in range(1, 5):
        if f"mixer{i}" in text or f"mixer {i}" in text or f"mixer_{i}" in text:
            return mixer_components[i - 1]

    # Check for HUW/CWU (hot utility water / hot tap water)
    if "huw" in text or "cwu" in text:
        return COMPONENT_HUW

    # Check for Lambda sensor
    if "lambda" in text:
        return COMPONENT_LAMBDA

    # Check for Buffer
    if "buffer" in text:
        return COMPONENT_BUFFER

    # Check for Solar
    if "solar" in text:
        return COMPONENT_SOLAR

    # If description mentions "mixer" generically and we have a sequence number,
    # use the sequence number to assign to the correct mixer
    if sequence_num and 1 <= sequence_num <= 4:
        if "mixer" in text:
            return mixer_components[sequence_num - 1]

    # Default to boiler
    return COMPONENT_BOILER


def get_validated_entity_component(
    name: str | None,
    key: str | None,
    description: str | None = None,
    sequence_num: int | None = None,
    coordinator_data: dict | None = None,
) -> str:
    """Determine and validate component assignment for an entity.

    Determines which component an entity belongs to, and validates
    that the component actually exists (e.g., mixer is connected).
    Falls back to COMPONENT_BOILER if the target component doesn't exist.

    This is the primary function to use for device assignment - it combines
    pattern detection from get_entity_component() with hardware validation.

    Args:
        name: Parameter name (e.g., "HUW preset temperature")
        key: Parameter key (e.g., "huw_preset_temperature")
        description: Parameter description for additional context
        sequence_num: Sequence number for duplicate parameters (1-4 for mixers)
        coordinator_data: Coordinator data for validation (regParams, etc.)

    Returns:
        Component identifier: COMPONENT_BOILER, COMPONENT_HUW, COMPONENT_MIXER_1 through
        COMPONENT_MIXER_4, COMPONENT_LAMBDA, COMPONENT_BUFFER, or COMPONENT_SOLAR

    """
    # First, determine the ideal component based on patterns
    component = get_entity_component(name, key, description, sequence_num)

    # Validate mixer exists before assigning
    if component.startswith("mixer_") and coordinator_data:
        mixer_num = int(component.split("_")[1])
        if not mixer_exists(coordinator_data, mixer_num):
            _LOGGER.debug(
                "Mixer %d doesn't exist, entity '%s' assigned to boiler instead",
                mixer_num,
                name or key,
            )
            return COMPONENT_BOILER

    # Add validation for other components (lambda, buffer, solar, huw)
    # when hardware detection is available

    return component


def _detect_param_context(description: str | None) -> str | None:
    """Detect parameter context from description.

    Args:
        description: Parameter description text

    Returns:
        Context type: "mixer", "huw", "circuit", "buffer", or None

    """
    if not description:
        return None

    desc_lower = description.lower()

    if "mixer" in desc_lower:
        return "mixer"
    if any(kw in desc_lower for kw in ["hot water", "huw", "dhw", "tap water"]):
        return "huw"
    if "thermostat" in desc_lower and "room" in desc_lower:
        return "circuit"
    if "buffer" in desc_lower:
        return "buffer"

    return None


def get_duplicate_display_name(
    param_name: str,
    sequence_num: int,
    description: str | None = None,
) -> str:
    """Generate display name for duplicate parameters with meaningful suffix.

    For parameters that appear multiple times (e.g., same name for Mixer 1-4),
    this function determines the appropriate suffix based on the description.

    Args:
        param_name: Original parameter name (e.g., "Off by thermostat")
        sequence_num: Sequence number (1, 2, 3, 4) for the duplicate
        description: Parameter description for component detection

    Returns:
        Display name with appropriate suffix:
        - "Off by thermostat (Mixer 1)" for mixer-related params
        - "Parameter Name (HUW)" for HUW-related params
        - "Parameter Name 1" as fallback for unknown params

    """
    context = _detect_param_context(description)

    if context == "mixer":
        return f"{param_name} (Mixer {sequence_num})"
    if context == "huw":
        return f"{param_name} (HUW {sequence_num})" if sequence_num > 1 else param_name
    if context == "circuit":
        return f"{param_name} (Circuit {sequence_num})"
    if context == "buffer":
        return (
            f"{param_name} (Buffer {sequence_num})" if sequence_num > 1 else param_name
        )

    # Fallback: use simple numbering
    return f"{param_name} {sequence_num}"


def get_duplicate_entity_key(
    base_key: str,
    sequence_num: int,
    description: str | None = None,
) -> str:
    """Generate entity key for duplicate parameters with meaningful suffix.

    Args:
        base_key: Base entity key (e.g., "off_by_thermostat")
        sequence_num: Sequence number (1, 2, 3, 4) for the duplicate
        description: Parameter description for component detection

    Returns:
        Entity key with appropriate suffix:
        - "off_by_thermostat_mixer_1" for mixer-related params
        - "param_name_1" as fallback

    """
    context = _detect_param_context(description)

    if context == "mixer":
        return f"{base_key}_mixer_{sequence_num}"
    if context == "huw":
        return f"{base_key}_huw_{sequence_num}" if sequence_num > 1 else base_key
    if context == "circuit":
        return f"{base_key}_circuit_{sequence_num}"
    if context == "buffer":
        return f"{base_key}_buffer_{sequence_num}" if sequence_num > 1 else base_key

    # Fallback: use simple numbering
    return f"{base_key}_{sequence_num}"


# =============================================================================
# CURRENT DATA PARAMS (CDP) DYNAMIC ENTITY HELPERS
# =============================================================================


def classify_current_data_param(param: dict) -> str:
    """Classify a currentDataMerged parameter as sensor, binary_sensor, or skip.

    Args:
        param: Dictionary with keys: name, unit, special, value

    Returns:
        "sensor", "binary_sensor", or "skip"

    """
    name = param.get("name", "")
    value = param.get("value")
    unit = param.get("unit", 0)
    special = param.get("special", 0)

    # Skip entries with no name or special values that should be skipped
    if not name or not name.strip():
        return "skip"

    if special in CDP_SPECIAL_SKIP:
        return "skip"

    # Skip null/None values (parameter not available on this device)
    if value is None:
        return "skip"

    # Skip string values (not numeric data)
    if isinstance(value, str):
        return "skip"

    # Boolean/state unit with boolean-like value → binary sensor
    if unit == CDP_UNIT_BINARY_STATE and isinstance(value, (bool, int)):
        return "binary_sensor"

    # Numeric values with a real unit → sensor
    if isinstance(value, (int, float)):
        return "sensor"

    return "skip"


def is_regparams_data_id_mapped(param_id: str) -> bool:
    """Check if a regParamsData ID is already handled by a static entity.

    Args:
        param_id: The string ID from regParamsData / currentDataMerged

    Returns:
        True if the ID is in NUMBER_MAP, SELECT_KEY_POST_INDEX, or SELECT_KEY_GET_INDEX

    """
    return param_id in STATIC_REGPARAMS_DATA_IDS


def build_current_data_entity_key(param_id: str, name: str) -> str:
    """Build a unique entity key for a currentDataMerged parameter.

    Format: cdp_{param_id}_{snake_name}
    The cdp prefix avoids collisions with existing static entities.

    Args:
        param_id: The numeric ID as a string (e.g., "139")
        name: Human-readable parameter name (e.g., "Valve mixer 1")

    Returns:
        Entity key like "cdp_139_valve_mixer_1"

    """
    snake = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    return f"cdp_{param_id}_{snake}"
