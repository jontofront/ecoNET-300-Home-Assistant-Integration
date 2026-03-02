#!/usr/bin/env python3
"""List all API endpoints used in the ecoNET300 integration."""

from pathlib import Path
import sys

# Add the custom_components directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "custom_components"))

try:
    from econet300.const import (  # type: ignore[import-untyped]
        API_NEW_PARAM_URI,
        API_REG_PARAMS_DATA_URI,
        API_REG_PARAMS_URI,
        API_RM_ALARMS_NAMES_URI,
        API_RM_CURR_NEW_PARAM_URI,
        API_RM_CURRENT_DATA_PARAMS_EDITS_URI,
        API_RM_CURRENT_DATA_PARAMS_URI,
        API_RM_EXISTING_LANGS_URI,
        API_RM_LANGS_URI,
        API_RM_LOCKS_NAMES_URI,
        API_RM_NEW_PARAM_URI,
        API_RM_PARAMS_DATA_URI,
        API_RM_PARAMS_DESCS_URI,
        API_RM_PARAMS_ENUMS_URI,
        API_RM_PARAMS_NAMES_URI,
        API_RM_PARAMS_UNITS_NAMES_URI,
        API_RM_STRUCTURE_URI,
        API_SYS_PARAMS_URI,
    )
except ImportError as e:
    print(f"Error importing constants: {e}")
    print("Make sure you're running from the project root directory.")
    sys.exit(1)


def main():
    """List all API endpoints."""
    print("ecoNET300 API Endpoints")
    print("=" * 50)

    # Core endpoints
    print("\n[CORE ENDPOINTS]")
    endpoints = [
        ("System Parameters", API_SYS_PARAMS_URI),
        ("Register Parameters", API_REG_PARAMS_URI),
        ("Register Parameters Data", API_REG_PARAMS_DATA_URI),
    ]

    for name, endpoint in endpoints:
        print(f"  • {name}: {endpoint}")

    # Parameter editing endpoints
    print("\n[PARAMETER EDITING ENDPOINTS]")
    edit_endpoints = [
        ("Save Parameter by Key", API_RM_CURR_NEW_PARAM_URI),
        ("Save Parameter by Index", API_RM_NEW_PARAM_URI),
        ("Legacy Parameter Edit", API_NEW_PARAM_URI),
        ("Editable Parameters Limits", API_RM_CURRENT_DATA_PARAMS_EDITS_URI),
    ]

    for name, endpoint in edit_endpoints:
        print(f"  • {name}: {endpoint}")

    # RM API endpoints
    print("\n[REMOTE MENU (RM) API ENDPOINTS]")

    rm_endpoints = [
        ("Parameter Names", API_RM_PARAMS_NAMES_URI),
        ("Parameter Data", API_RM_PARAMS_DATA_URI),
        ("Parameter Descriptions", API_RM_PARAMS_DESCS_URI),
        ("Parameter Enumerations", API_RM_PARAMS_ENUMS_URI),
        ("Parameter Units", API_RM_PARAMS_UNITS_NAMES_URI),
        ("Menu Structure", API_RM_STRUCTURE_URI),
        ("Current Parameters", API_RM_CURRENT_DATA_PARAMS_URI),
        ("Editable Parameters", API_RM_CURRENT_DATA_PARAMS_EDITS_URI),
        ("Languages", API_RM_LANGS_URI),
        ("Existing Languages", API_RM_EXISTING_LANGS_URI),
        ("Lock Names", API_RM_LOCKS_NAMES_URI),
        ("Alarm Names", API_RM_ALARMS_NAMES_URI),
    ]

    for name, endpoint in rm_endpoints:
        print(f"  • {name}: {endpoint}")

    # Summary
    total_endpoints = len(endpoints) + len(edit_endpoints) + len(rm_endpoints)
    print(f"\n[TOTAL ENDPOINTS: {total_endpoints}]")

    print("\n[USAGE]")
    print("All endpoints are accessed via: {host}/econet/{endpoint}")
    print("Example: https://192.168.1.100/econet/sysParams")


if __name__ == "__main__":
    main()
