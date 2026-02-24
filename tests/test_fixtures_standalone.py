"""Standalone fixture tests - can run without Home Assistant dependencies.

This script is designed to be run directly for debugging and validation.
"""
# ruff: noqa: T201

import json
from pathlib import Path
import sys

# List of all fixtures
ALL_FIXTURES = [
    "ecoMAX810P-L",
    "ecoMAX360",
    "ecoMAX360-cf8",
    "ecoSOL",
    "SControl MK1",
    "ecoMAX850R2-X",
    "ecoMAX860D3-HB",
    "ecoMAX860P2-N",
    "ecoMAX860P3-O",
    "ecoMAX860P3-V",
    "ecoSOL500",
]

FIXTURES_WITH_MERGED_DATA = ["ecoMAX810P-L", "ecoMAX860P3-O"]


def load_fixture(fixture_name: str, filename: str) -> dict | None:
    """Load a fixture file, return None if not found."""
    fixture_path = Path(__file__).parent / "fixtures" / fixture_name / filename
    if not fixture_path.exists():
        return None
    with fixture_path.open(encoding="utf-8") as f:
        return json.load(f)


def should_be_number_entity(param: dict) -> bool:
    """Check if parameter should be a number entity (simplified)."""
    if not param.get("edit", False):
        return False
    if "enum" in param:
        return False
    if param.get("unit_name"):
        return True
    return False


def test_all_fixtures_exist():
    """Test that all fixture directories exist."""
    print("\n=== Testing fixture directories ===")
    fixtures_dir = Path(__file__).parent / "fixtures"
    for fixture_name in ALL_FIXTURES:
        fixture_path = fixtures_dir / fixture_name
        exists = fixture_path.exists()
        status = "OK" if exists else "MISSING"
        print(f"  {fixture_name}: {status}")
        assert exists, f"Fixture directory {fixture_name} does not exist"
    print("All fixture directories exist!")


def test_sys_params_for_all_fixtures():
    """Test sysParams.json exists and is valid for all fixtures."""
    print("\n=== Testing sysParams.json ===")
    for fixture_name in ALL_FIXTURES:
        sys_params = load_fixture(fixture_name, "sysParams.json")
        assert sys_params is not None, f"sysParams.json missing for {fixture_name}"
        assert isinstance(sys_params, dict), (
            f"sysParams should be dict for {fixture_name}"
        )

        # Check for controllerID
        controller_id = sys_params.get("controllerID") or sys_params.get("controllerId")
        assert controller_id is not None, f"controllerID missing for {fixture_name}"
        print(f"  {fixture_name}: controllerID = {controller_id}")
    print("All sysParams.json files valid!")


def test_reg_params_for_all_fixtures():
    """Test regParams.json exists and is valid for all fixtures."""
    print("\n=== Testing regParams.json ===")
    for fixture_name in ALL_FIXTURES:
        reg_params = load_fixture(fixture_name, "regParams.json")
        assert reg_params is not None, f"regParams.json missing for {fixture_name}"
        assert isinstance(reg_params, dict), (
            f"regParams should be dict for {fixture_name}"
        )
        print(f"  {fixture_name}: {len(reg_params)} parameters")
    print("All regParams.json files valid!")


def test_merged_data_structure():
    """Test mergedData.json structure for fixtures that have it."""
    print("\n=== Testing mergedData.json ===")
    for fixture_name in FIXTURES_WITH_MERGED_DATA:
        merged_data = load_fixture(fixture_name, "mergedData.json")
        assert merged_data is not None, f"mergedData.json missing for {fixture_name}"
        assert "parameters" in merged_data, "mergedData should have parameters"
        assert isinstance(merged_data["parameters"], dict)

        num_params = len(merged_data["parameters"])
        print(f"  {fixture_name}: {num_params} parameters")

        # Count entity types
        number_count = 0
        for param in merged_data["parameters"].values():
            if should_be_number_entity(param):
                number_count += 1
        print(f"    - Number entity candidates: {number_count}")
    print("All mergedData.json files valid!")


def test_device_type_detection():
    """Test that device type can be detected from controllerID."""
    print("\n=== Testing device type detection ===")
    device_types = {
        "ecoMAX810P-L": "ecoMAX",
        "ecoMAX360": "ecoMAX",
        "ecoMAX850R2-X": "ecoMAX",
        "ecoMAX860P2-N": "ecoMAX",
        "ecoMAX860P3-V": "ecoMAX",
        "ecoSOL": "ecoSOL",
        "ecoSOL500": "ecoSOL",
        "SControl MK1": "SControl",
    }

    for fixture_name, expected_type in device_types.items():
        sys_params = load_fixture(fixture_name, "sysParams.json")
        if sys_params is None:
            print(f"  {fixture_name}: SKIPPED (no sysParams)")
            continue

        controller_id = sys_params.get("controllerID") or sys_params.get("controllerId")
        if controller_id is None:
            print(f"  {fixture_name}: SKIPPED (no controllerID)")
            continue

        detected = (
            expected_type in controller_id
            or expected_type.lower() in controller_id.lower()
        )
        status = "OK" if detected else "FAIL"
        print(f"  {fixture_name}: {controller_id} -> {expected_type} [{status}]")
        assert detected, f"Device type {expected_type} not detected in {controller_id}"
    print("All device types detected correctly!")


def test_fixture_summary():
    """Print a summary of all fixtures."""
    print("\n=== Fixture Summary ===")
    print(f"{'Fixture':<20} {'sysParams':<12} {'regParams':<12} {'mergedData':<12}")
    print("-" * 56)

    for fixture_name in ALL_FIXTURES:
        sys_ok = "OK" if load_fixture(fixture_name, "sysParams.json") else "MISSING"
        reg_ok = "OK" if load_fixture(fixture_name, "regParams.json") else "MISSING"
        merged_ok = "OK" if load_fixture(fixture_name, "mergedData.json") else "-"
        print(f"{fixture_name:<20} {sys_ok:<12} {reg_ok:<12} {merged_ok:<12}")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("RUNNING STANDALONE FIXTURE TESTS")
    print("=" * 60)

    try:
        test_all_fixtures_exist()
        test_sys_params_for_all_fixtures()
        test_reg_params_for_all_fixtures()
        test_merged_data_structure()
        test_device_type_detection()
        test_fixture_summary()
    except AssertionError as e:
        print(f"\nTEST FAILED: {e}")
        return 1
    else:
        print("\n" + "=" * 60)
        print("ALL TESTS PASSED!")
        print("=" * 60)
        return 0


if __name__ == "__main__":
    sys.exit(run_all_tests())
