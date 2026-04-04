#!/usr/bin/env python3
"""Parse Home Assistant diagnostic file and create fixture folders.

This script extracts data from a Home Assistant ecoNET300 diagnostic file
and creates a fixture folder structure matching the project's test fixtures.

Usage:
    python scripts/create_fixture_from_diagnostics.py [diagnostic_file] [--device-name <name>]

    If no file is specified, the script will scan scripts/ad_diagnostic_file/
    for JSON files and process them automatically.

Arguments:
    diagnostic_file     Path to the diagnostic JSON file (optional)
    --device-name       Optional device name override (auto-detected from controllerId otherwise)
    --output-dir        Output directory (default: tests/fixtures/)
    --dry-run           Show what would be created without writing files
    --keep-file         Don't delete the diagnostic file after processing

Examples:
    # Auto-scan scripts/ad_diagnostic_file/ folder
    python scripts/create_fixture_from_diagnostics.py

    # Process specific file
    python scripts/create_fixture_from_diagnostics.py diagnostics.json

    # With device name override
    python scripts/create_fixture_from_diagnostics.py diagnostics.json --device-name ecoMAX920i2

    # Dry run (preview only)
    python scripts/create_fixture_from_diagnostics.py --dry-run

"""

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any

# api_endpoint_data.extended_endpoints keys → tests/fixtures/<device>/ filenames
EXTENDED_ENDPOINT_FIXTURE_MAP: dict[str, str] = {
    "edit_params": "editParams.json",
    "rm_params_names": "rmParamsNames.json",
    "rm_params_data": "rmParamsData.json",
    "rm_params_descs": "rmParamsDescs.json",
    "rm_params_enums": "rmParamsEnums.json",
    "rm_params_units_names": "rmParamsUnitsNames.json",
    "rm_structure": "rmStructure.json",
    "rm_current_data_params": "rmCurrentDataParams.json",
    "rm_langs": "rmLangs.json",
    "rm_existing_langs": "rmExistingLangs.json",
    "rm_locks_names": "rmLocksNames.json",
    "rm_alarms_names": "rmAlarmsNames.json",
}


def _extended_fixture_payload_usable(payload: Any) -> bool:
    """Skip HA diagnostics placeholders (failed or unsupported endpoint)."""
    if isinstance(payload, dict) and (
        "_ha_diagnostics_unavailable" in payload
        or "_ha_diagnostics_fetch_failed" in payload
    ):
        return False
    return True


def sanitize_folder_name(name: str) -> str:
    """Sanitize the device name for use as a folder name.

    Args:
        name: Original device name from controllerId

    Returns:
        Sanitized folder name safe for filesystem use

    """
    # Remove or replace problematic characters, collapse underscores
    sanitized = name.replace(" ", "_")
    sanitized = re.sub(r"[<>:\"/\\|?*]", "", sanitized)
    sanitized = sanitized.strip("._")
    return re.sub(r"_+", "_", sanitized)


def unwrap_data(data: dict) -> dict:
    """Unwrap the 'data' wrapper if present in diagnostic files.

    Home Assistant diagnostic files can have different structures:
    - Direct structure: {"api_info": {...}, "coordinator_data": {...}}
    - Wrapped structure: {"data": {"api_info": {...}, "coordinator_data": {...}}}

    Args:
        data: The parsed diagnostic JSON data

    Returns:
        Unwrapped data dictionary

    """
    # Check if this is a wrapped structure (has 'data' key with nested dicts)
    if "data" in data and isinstance(data["data"], dict):
        inner_data = data["data"]
        # Check if the inner data has expected keys
        if any(
            key in inner_data
            for key in ["api_info", "coordinator_data", "api_endpoint_data"]
        ):
            return inner_data
    return data


def extract_device_name(data: dict) -> str | None:
    """Extract device/controller name from diagnostic data.

    Args:
        data: The parsed diagnostic JSON data

    Returns:
        Device name or None if not found

    """
    # Unwrap if needed
    data = unwrap_data(data)

    # Try coordinator_data.data.mergedData.device.controllerId
    try:
        controller_id = (
            data.get("coordinator_data", {})
            .get("data", {})
            .get("mergedData", {})
            .get("device", {})
            .get("controllerId")
        )
        if controller_id:
            return controller_id
    except (AttributeError, TypeError):
        pass

    # Try api_info.model_id
    try:
        model_id = data.get("api_info", {}).get("model_id")
        if model_id:
            return model_id
    except (AttributeError, TypeError):
        pass

    # Try coordinator_data.data.sysParams for any identifier
    try:
        sys_params = (
            data.get("coordinator_data", {}).get("data", {}).get("sysParams", {})
        )
        # Try to construct from version info
        module_ver = sys_params.get("moduleASoftVer", "")
        if module_ver:
            # Extract model hint from version (e.g., "8.30.176.R1" doesn't help)
            pass
    except (AttributeError, TypeError):
        pass

    return None


def extract_and_save_files(
    data: dict, output_dir: Path, dry_run: bool = False
) -> dict[str, bool]:
    """Extract data from diagnostic file and save to fixture files.

    Args:
        data: The parsed diagnostic JSON data
        output_dir: Directory where files should be saved
        dry_run: If True, don't write files, just report what would be done

    Returns:
        Dictionary mapping filename to success status

    """
    # Unwrap if needed
    data = unwrap_data(data)

    results: dict[str, bool] = {}

    # Define extraction mappings: (target_filename, extraction_paths)
    # Each extraction path is tried in order until one succeeds
    file_mappings: list[tuple[str, list[tuple[str, ...]]]] = [
        (
            "sysParams.json",
            [
                ("api_endpoint_data", "sys_params"),
                ("coordinator_data", "data", "sysParams"),
            ],
        ),
        (
            "regParams.json",
            [
                ("api_endpoint_data", "reg_params"),
                ("coordinator_data", "data", "regParams"),
            ],
        ),
        (
            "regParamsData.json",
            [
                ("api_endpoint_data", "reg_params_data"),
            ],
        ),
        (
            "rmCurrentDataParamsEdits.json",
            [
                ("api_endpoint_data", "param_edit_data"),
            ],
        ),
        (
            "mergedData.json",
            [
                ("coordinator_data", "data", "mergedData"),
            ],
        ),
    ]

    # Also check for any rm* data in coordinator_data.data
    coordinator_data_keys = list(
        data.get("coordinator_data", {}).get("data", {}).keys()
    )
    rm_keys = [
        k for k in coordinator_data_keys if k.startswith("rm") and k != "mergedData"
    ]

    # Add rm* files if found
    file_mappings.extend(
        (f"{rm_key}.json", [("coordinator_data", "data", rm_key)]) for rm_key in rm_keys
    )

    # Also try to extract from regParamsData the rmCurrentDataParams if present
    reg_params_data = None
    for path in [
        ("api_endpoint_data", "reg_params_data"),
        ("coordinator_data", "data", "regParamsData"),
    ]:
        try:
            current = data
            for key in path:
                current = current[key]
            reg_params_data = current
            break
        except (KeyError, TypeError):
            pass

    # If regParamsData has a specific structure, extract rmCurrentDataParams
    if isinstance(reg_params_data, dict) and "curr" in reg_params_data:
        file_mappings.append(
            (
                "rmCurrentDataParams.json",
                [("api_endpoint_data", "reg_params_data")],
            )
        )

    # Extract and save each file
    for filename, paths in file_mappings:
        extracted_data = None

        for path in paths:
            try:
                current = data
                for key in path:
                    current = current[key]
                extracted_data = current
                break
            except (KeyError, TypeError):
                continue

        if extracted_data is not None:
            file_path = output_dir / filename
            if dry_run:
                print(f"  [DRY-RUN] Would create: {file_path}")
                # Check size
                json_str = json.dumps(extracted_data, indent=2, ensure_ascii=False)
                print(f"            Size: {len(json_str):,} bytes")
                results[filename] = True
            else:
                try:
                    file_path.write_text(
                        json.dumps(extracted_data, indent=2, ensure_ascii=False),
                        encoding="utf-8",
                    )
                    print(f"  [OK] Created: {file_path}")
                    results[filename] = True
                except OSError as e:
                    print(f"  [ERROR] Failed to write {file_path}: {e}")
                    results[filename] = False
        else:
            print(f"  [SKIP] {filename}: Data not found in diagnostic file")
            results[filename] = False

    unwrapped = unwrap_data(data)
    api_ep = unwrapped.get("api_endpoint_data")
    if isinstance(api_ep, dict) and not api_ep.get("error"):
        extended = api_ep.get("extended_endpoints")
        if isinstance(extended, dict):
            for ep_key, fname in EXTENDED_ENDPOINT_FIXTURE_MAP.items():
                payload = extended.get(ep_key)
                if payload is None or not _extended_fixture_payload_usable(payload):
                    continue
                file_path = output_dir / fname
                if dry_run:
                    print(f"  [DRY-RUN] Would create (extended): {file_path}")
                    results[fname] = True
                else:
                    try:
                        file_path.write_text(
                            json.dumps(payload, indent=2, ensure_ascii=False),
                            encoding="utf-8",
                        )
                        print(f"  [OK] Created (extended): {file_path}")
                        results[fname] = True
                    except OSError as e:
                        print(f"  [ERROR] Failed to write {file_path}: {e}")
                        results[fname] = False

    return results


def create_readme(
    device_name: str,
    output_dir: Path,
    files_created: list[str],
    dry_run: bool = False,
) -> None:
    """Create a README.md file for the fixture folder.

    Args:
        device_name: Name of the device
        output_dir: Directory where README should be saved
        files_created: List of files that were created
        dry_run: If True, don't write files

    """
    files_list = "\n".join(
        f"- `{f}` - Extracted from diagnostic file" for f in sorted(files_created)
    )
    readme_content = f"""# {device_name} Test Fixtures

## Overview

This directory contains test fixtures for the **{device_name}** ecoNET device.

## Files

### Data Files

{files_list}

## Source

These fixtures were automatically generated from a Home Assistant diagnostic file
using the `scripts/create_fixture_from_diagnostics.py` script.

## Usage

These fixtures are used by the integration's test suite to verify correct behavior
without requiring a live ecoNET device connection.

```python
# Example: Load fixture data in tests
import json
from pathlib import Path

fixture_path = Path(__file__).parent / "fixtures" / "{device_name}"
sys_params = json.loads((fixture_path / "sysParams.json").read_text())
```
"""

    readme_path = output_dir / "README.md"
    if dry_run:
        print(f"  [DRY-RUN] Would create: {readme_path}")
    else:
        readme_path.write_text(readme_content, encoding="utf-8")
        print(f"  [OK] Created: {readme_path}")


def is_econet_diagnostic(data: dict) -> bool:
    """Check if the diagnostic file is from ecoNET300 integration.

    Args:
        data: The parsed diagnostic JSON data

    Returns:
        True if this appears to be an ecoNET300 diagnostic file

    """
    unwrapped = unwrap_data(data)

    # Check for ecoNET300 specific data structures
    if unwrapped.get("api_endpoint_data"):
        return True
    if unwrapped.get("coordinator_data", {}).get("data", {}).get("sysParams"):
        return True
    if unwrapped.get("coordinator_data", {}).get("data", {}).get("regParams"):
        return True

    return False


def process_diagnostic_file(
    file_path: Path,
    output_base: Path,
    device_name: str | None = None,
    dry_run: bool = False,
    delete_after: bool = True,
) -> bool:
    """Process a single diagnostic file.

    Args:
        file_path: Path to the diagnostic file
        output_base: Base directory for output fixtures
        device_name: Optional device name override
        dry_run: If True, don't write files
        delete_after: If True, delete the source file after success

    Returns:
        True if processing was successful

    """
    print(f"\nProcessing: {file_path.name}")
    print("-" * 40)

    # Load diagnostic file
    try:
        raw_text = file_path.read_text(encoding="utf-8")
        data = json.loads(raw_text)
    except json.JSONDecodeError as e:
        print(f"  [ERROR] Invalid JSON: {e}")
        return False
    except OSError as e:
        print(f"  [ERROR] Failed to read file: {e}")
        return False

    print(f"  File size: {len(raw_text):,} bytes")

    # Check if this is an ecoNET300 diagnostic
    if not is_econet_diagnostic(data):
        print("  [SKIP] Not an ecoNET300 diagnostic file (missing required data)")
        print("         Make sure to download diagnostics from ecoNET300 integration,")
        print("         not from HACS or other integrations.")
        return False

    # Determine device name
    detected_name = device_name
    if not detected_name:
        detected_name = extract_device_name(data)
        if detected_name:
            print(f"  Auto-detected device: {detected_name}")
        else:
            print("  [ERROR] Could not auto-detect device name.")
            print("          Use --device-name to specify.")
            return False
    else:
        print(f"  Using specified device name: {detected_name}")

    # Sanitize folder name
    folder_name = sanitize_folder_name(detected_name)
    print(f"  Folder name: {folder_name}")

    # Create output directory
    output_dir = output_base / folder_name

    if not dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)

    # Extract and save files
    results = extract_and_save_files(data, output_dir, dry_run=dry_run)

    # Create README
    files_created = [f for f, success in results.items() if success]
    if files_created:
        create_readme(folder_name, output_dir, files_created, dry_run=dry_run)

    # Summary for this file
    success_count = sum(1 for v in results.values() if v)
    skip_count = sum(1 for v in results.values() if not v)

    if success_count > 0:
        print(f"  [OK] Created {success_count} files, skipped {skip_count}")
        if not dry_run:
            print(f"  Fixture folder: {output_dir}")

        # Delete source file after successful processing
        if delete_after and not dry_run:
            try:
                file_path.unlink()
                print(f"  [CLEANUP] Deleted source file: {file_path.name}")
            except OSError as e:
                print(f"  [WARN] Could not delete source file: {e}")

        return True
    print(f"  [WARN] No files created (skipped {skip_count})")
    return False


def main() -> int:
    """Run the fixture generator from diagnostics."""
    parser = argparse.ArgumentParser(
        description="Parse Home Assistant diagnostic file and create fixture folders",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Auto-scan scripts/ad_diagnostic_file/ folder
    python scripts/create_fixture_from_diagnostics.py

    # Process specific file
    python scripts/create_fixture_from_diagnostics.py diagnostics.json

    # With device name override
    python scripts/create_fixture_from_diagnostics.py --device-name ecoMAX920i2

    # Dry run (preview only)
    python scripts/create_fixture_from_diagnostics.py --dry-run
        """,
    )
    parser.add_argument(
        "diagnostic_file",
        type=Path,
        nargs="?",
        default=None,
        help="Path to the diagnostic JSON file (optional - scans ad_diagnostic_file/ if not provided)",
    )
    parser.add_argument(
        "--device-name",
        type=str,
        help="Override device name (auto-detected from controllerId otherwise)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Output directory (default: tests/fixtures/)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created without writing files",
    )
    parser.add_argument(
        "--keep-file",
        action="store_true",
        help="Don't delete the diagnostic file after successful processing",
    )

    args = parser.parse_args()

    # Find project root and default output directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    output_base = args.output_dir or (project_root / "tests" / "fixtures")
    ad_diagnostic_dir = script_dir / "ad_diagnostic_file"

    print("[FIXTURE GENERATOR FROM DIAGNOSTICS]")
    print("=" * 60)

    # Collect files to process
    files_to_process: list[Path] = []

    if args.diagnostic_file:
        # Specific file provided
        if not args.diagnostic_file.exists():
            print(f"Error: Diagnostic file not found: {args.diagnostic_file}")
            return 1
        files_to_process.append(args.diagnostic_file)
    else:
        # Scan ad_diagnostic_file folder
        print(f"Scanning: {ad_diagnostic_dir}")
        if not ad_diagnostic_dir.exists():
            print(f"  Creating folder: {ad_diagnostic_dir}")
            ad_diagnostic_dir.mkdir(parents=True, exist_ok=True)

        json_files = list(ad_diagnostic_dir.glob("*.json"))
        if json_files:
            print(f"  Found {len(json_files)} JSON file(s)")
            files_to_process.extend(json_files)
        else:
            print("  No JSON files found in ad_diagnostic_file/")
            print("\n  To use this script:")
            print("  1. Download diagnostics from Home Assistant:")
            print(
                "     Settings > Devices & Services > ecoNET300 > Menu > Download diagnostics"
            )
            print(f"  2. Copy the JSON file to: {ad_diagnostic_dir}")
            print("  3. Run this script again")
            return 0

    if args.dry_run:
        print("\n[DRY-RUN MODE - No files will be written or deleted]")

    # Process each file
    success_count = 0
    fail_count = 0

    for file_path in files_to_process:
        delete_after = not args.keep_file and not args.dry_run
        if process_diagnostic_file(
            file_path,
            output_base,
            device_name=args.device_name,
            dry_run=args.dry_run,
            delete_after=delete_after,
        ):
            success_count += 1
        else:
            fail_count += 1

    # Final summary
    print("\n" + "=" * 60)
    print("[FINAL SUMMARY]")
    print(f"  Successful: {success_count}")
    print(f"  Failed/Skipped: {fail_count}")

    if args.dry_run:
        print("\n[DRY-RUN MODE - No files were actually written or deleted]")

    return 0 if success_count > 0 or fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
