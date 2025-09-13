#!/usr/bin/env python3
"""Integrated diagnostic tests for ecoNET300 integration.

This test combines both simple and complex diagnostic functionality:
1. Simple data redaction tests (standalone)
2. Complex diagnostic integration tests (with Home Assistant)
3. Edge case handling
4. Error scenarios

Part of the test integration strategy for better organization.
"""

import logging
from pathlib import Path
import sys
from typing import Any

# Import diagnostics module components at top level
DIAGNOSTICS_AVAILABLE = False
TO_REDACT: list[str] = []
_redact_data = None
async_get_config_entry_diagnostics = None
async_get_device_diagnostics = None

try:
    from custom_components.econet300.diagnostics import (  # type: ignore[import,assignment]
        TO_REDACT,
        _redact_data,
        async_get_config_entry_diagnostics,
        async_get_device_diagnostics,
    )

    DIAGNOSTICS_AVAILABLE = True
except ImportError:
    # Use dummy values already set above
    pass


# Set up logging
_LOGGER = logging.getLogger(__name__)

# Add the custom_components directory to the path
custom_components_path = str(
    Path(__file__).parent.parent / "custom_components" / "econet300"
)
if custom_components_path not in sys.path:
    sys.path.insert(0, custom_components_path)

# Also add the parent directory for the custom_components module
parent_path = str(Path(__file__).parent.parent)
if parent_path not in sys.path:
    sys.path.insert(0, parent_path)

# Test configuration
TEST_CONFIG: dict[str, Any] = {
    "sensitive_keys": ["host", "username", "password", "token", "key"],
    "safe_keys": ["name", "version", "status", "data"],
    "test_data": {
        "simple": {
            "host": "192.168.1.100",
            "username": "test_user",
            "password": "secret_password",
            "safe_data": "this_is_safe",
        },
        "nested": {
            "api_info": {
                "host": "192.168.1.100",
                "username": "test_user",
            },
            "safe_data": "this_is_safe",
        },
        "complex": {
            "config": {
                "host": "192.168.1.100",
                "credentials": {
                    "username": "admin",
                    "password": "admin123",
                },
            },
            "data": {
                "temperature": 25.5,
                "status": "online",
            },
        },
    },
}


class TestResult:
    """Container for test results."""

    def __init__(self, name: str):
        """Initialize a TestResult container.

        Args:
            name: The name of the test result.

        """
        self.name = name
        self.passed = 0
        self.failed = 0
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def add_success(self, message: str = ""):
        """Add a successful test."""
        self.passed += 1
        if message:
            _LOGGER.info("✅ %s", message)

    def add_failure(self, message: str):
        """Add a failed test."""
        self.failed += 1
        self.errors.append(message)
        _LOGGER.error("❌ %s", message)

    def add_warning(self, message: str):
        """Add a warning."""
        self.warnings.append(message)
        _LOGGER.warning("⚠️  %s", message)

    def is_success(self) -> bool:
        """Check if all tests passed."""
        return self.failed == 0

    def summary(self) -> str:
        """Get test summary."""
        return f"{self.name}: {self.passed} passed, {self.failed} failed, {len(self.warnings)} warnings"


class DiagnosticsValidator:
    """Main validator class for diagnostic functionality."""

    def __init__(self):
        """Initialize the DiagnosticsValidator.

        Sets up the validator with empty results and checks diagnostics availability.
        """
        self.results: dict[str, TestResult] = {}
        self.diagnostics_available = DIAGNOSTICS_AVAILABLE

    def load_diagnostics(self) -> bool:
        """Load diagnostics module."""
        _LOGGER.info("📁 Loading diagnostics module...")

        if DIAGNOSTICS_AVAILABLE:
            self.diagnostics_available = True
            _LOGGER.info("✅ Diagnostics module loaded successfully")
            return True

        _LOGGER.error("Failed to load diagnostics module: ImportError")
        self.diagnostics_available = False
        return False

    def test_simple_data_redaction(self) -> TestResult:
        """Test 1: Simple data redaction functionality."""
        result = TestResult("Simple Data Redaction")

        if not self.diagnostics_available:
            result.add_failure("Diagnostics module not available")
            return result

        try:
            # Test simple data redaction
            if _redact_data is None:
                result.add_failure("_redact_data function not available")
                return result
            test_data = TEST_CONFIG["test_data"]["simple"]
            redacted_data = _redact_data(test_data, TO_REDACT)  # type: ignore[misc]

            # Check sensitive data is redacted
            if redacted_data["host"] == "**REDACTED**":
                result.add_success("Host data redacted correctly")
            else:
                result.add_failure(f"Host data not redacted: {redacted_data['host']}")

            if redacted_data["username"] == "**REDACTED**":
                result.add_success("Username data redacted correctly")
            else:
                result.add_failure(
                    f"Username data not redacted: {redacted_data['username']}"
                )

            if redacted_data["password"] == "**REDACTED**":
                result.add_success("Password data redacted correctly")
            else:
                result.add_failure(
                    f"Password data not redacted: {redacted_data['password']}"
                )

            # Check safe data is preserved
            if redacted_data["safe_data"] == "this_is_safe":
                result.add_success("Safe data preserved correctly")
            else:
                result.add_failure(
                    f"Safe data not preserved: {redacted_data['safe_data']}"
                )

        except (ImportError, KeyError, TypeError) as e:
            result.add_failure(f"Simple data redaction test failed: {e}")

        return result

    def test_nested_data_redaction(self) -> TestResult:
        """Test 2: Nested data redaction functionality."""
        result = TestResult("Nested Data Redaction")

        if not self.diagnostics_available:
            result.add_failure("Diagnostics module not available")
            return result

        try:
            # Test nested data redaction
            if _redact_data is None:
                result.add_failure("_redact_data function not available")
                return result
            test_data = TEST_CONFIG["test_data"]["nested"]
            redacted_data = _redact_data(test_data, TO_REDACT)  # type: ignore[misc]

            # Check nested sensitive data is redacted
            if redacted_data["api_info"]["host"] == "**REDACTED**":
                result.add_success("Nested host data redacted correctly")
            else:
                result.add_failure(
                    f"Nested host data not redacted: {redacted_data['api_info']['host']}"
                )

            if redacted_data["api_info"]["username"] == "**REDACTED**":
                result.add_success("Nested username data redacted correctly")
            else:
                result.add_failure(
                    f"Nested username data not redacted: {redacted_data['api_info']['username']}"
                )

            # Check safe data is preserved
            if redacted_data["safe_data"] == "this_is_safe":
                result.add_success("Nested safe data preserved correctly")
            else:
                result.add_failure(
                    f"Nested safe data not preserved: {redacted_data['safe_data']}"
                )

        except (ImportError, KeyError, TypeError) as e:
            result.add_failure(f"Nested data redaction test failed: {e}")

        return result

    def test_complex_data_redaction(self) -> TestResult:
        """Test 3: Complex nested data redaction functionality."""
        result = TestResult("Complex Data Redaction")

        if not self.diagnostics_available:
            result.add_failure("Diagnostics module not available")
            return result

        try:
            # Test complex nested data redaction
            if _redact_data is None:
                result.add_failure("_redact_data function not available")
                return result
            test_data = TEST_CONFIG["test_data"]["complex"]
            redacted_data = _redact_data(test_data, TO_REDACT)  # type: ignore[misc]

            # Check deeply nested sensitive data is redacted
            if redacted_data["config"]["host"] == "**REDACTED**":
                result.add_success("Deeply nested host data redacted correctly")
            else:
                result.add_failure(
                    f"Deeply nested host data not redacted: {redacted_data['config']['host']}"
                )

            if redacted_data["config"]["credentials"]["username"] == "**REDACTED**":
                result.add_success("Deeply nested username data redacted correctly")
            else:
                result.add_failure(
                    f"Deeply nested username data not redacted: {redacted_data['config']['credentials']['username']}"
                )

            if redacted_data["config"]["credentials"]["password"] == "**REDACTED**":
                result.add_success("Deeply nested password data redacted correctly")
            else:
                result.add_failure(
                    f"Deeply nested password data not redacted: {redacted_data['config']['credentials']['password']}"
                )

            # Check safe data is preserved
            if redacted_data["data"]["temperature"] == 25.5:
                result.add_success("Complex safe data preserved correctly")
            else:
                result.add_failure(
                    f"Complex safe data not preserved: {redacted_data['data']['temperature']}"
                )

            if redacted_data["data"]["status"] == "online":
                result.add_success("Complex status data preserved correctly")
            else:
                result.add_failure(
                    f"Complex status data not preserved: {redacted_data['data']['status']}"
                )

        except (ImportError, KeyError, TypeError) as e:
            result.add_failure(f"Complex data redaction test failed: {e}")

        return result

    def test_edge_cases(self) -> TestResult:
        """Test 4: Edge cases and error handling."""
        result = TestResult("Edge Cases")

        if not self.diagnostics_available:
            result.add_failure("Diagnostics module not available")
            return result

        try:
            # Test non-dict data
            if _redact_data is None:
                result.add_failure("_redact_data function not available")
                return result
            non_dict_data = "not_a_dict"
            redacted_non_dict = _redact_data(non_dict_data, TO_REDACT)  # type: ignore[misc]
            if redacted_non_dict == "not_a_dict":
                result.add_success("Non-dict data returned unchanged")
            else:
                result.add_failure(f"Non-dict data changed: {redacted_non_dict}")

            # Test empty dict
            empty_dict: dict[str, Any] = {}
            redacted_empty = _redact_data(empty_dict, TO_REDACT)
            if not redacted_empty:
                result.add_success("Empty dict handled correctly")
            else:
                result.add_failure(
                    f"Empty dict not handled correctly: {redacted_empty}"
                )

            # Test None data
            none_data = None
            redacted_none = _redact_data(none_data, TO_REDACT)
            if redacted_none is None:
                result.add_success("None data handled correctly")
            else:
                result.add_failure(f"None data not handled correctly: {redacted_none}")

            # Test list data
            list_data = ["item1", "item2"]
            redacted_list = _redact_data(list_data, TO_REDACT)
            if redacted_list == ["item1", "item2"]:
                result.add_success("List data returned unchanged")
            else:
                result.add_failure(f"List data changed: {redacted_list}")

        except (ImportError, KeyError, TypeError) as e:
            result.add_failure(f"Edge cases test failed: {e}")

        return result

    def test_to_redact_list(self) -> TestResult:
        """Test 5: TO_REDACT list validation."""
        result = TestResult("TO_REDACT List")

        if not self.diagnostics_available:
            result.add_failure("Diagnostics module not available")
            return result

        try:
            # Check TO_REDACT is a list
            if isinstance(TO_REDACT, list):
                result.add_success("TO_REDACT is a list")
            else:
                result.add_failure(f"TO_REDACT should be a list, got {type(TO_REDACT)}")

            # Check expected sensitive keys are in TO_REDACT
            expected_keys = ["host", "username", "password", "token", "key"]
            for key in expected_keys:
                if key in TO_REDACT:
                    result.add_success(f"Expected key '{key}' found in TO_REDACT")
                else:
                    result.add_warning(f"Expected key '{key}' not found in TO_REDACT")

            # Check TO_REDACT is not empty
            if len(TO_REDACT) > 0:
                result.add_success(f"TO_REDACT contains {len(TO_REDACT)} keys")
            else:
                result.add_failure("TO_REDACT is empty")

        except (ImportError, KeyError, TypeError) as e:
            result.add_failure(f"TO_REDACT list test failed: {e}")

        return result

    def test_diagnostic_functions_availability(self) -> TestResult:
        """Test 6: Diagnostic functions availability."""
        result = TestResult("Diagnostic Functions")

        if not self.diagnostics_available:
            result.add_failure("Diagnostics module not available")
            return result

        try:
            # Check functions are callable
            if callable(async_get_config_entry_diagnostics):
                result.add_success("async_get_config_entry_diagnostics is callable")
            else:
                result.add_failure("async_get_config_entry_diagnostics is not callable")

            if callable(async_get_device_diagnostics):
                result.add_success("async_get_device_diagnostics is callable")
            else:
                result.add_failure("async_get_device_diagnostics is not callable")

        except (ImportError, AttributeError) as e:
            result.add_failure(f"Diagnostic functions test failed: {e}")

        return result

    def test_mock_diagnostic_integration(self) -> TestResult:
        """Test 7: Mock diagnostic integration (without HA dependencies)."""
        result = TestResult("Mock Diagnostic Integration")

        if not self.diagnostics_available:
            result.add_failure("Diagnostics module not available")
            return result

        try:
            # Create mock data that would come from Home Assistant
            mock_config_entry_data = {
                "host": "192.168.1.100",
                "username": "test_user",
                "password": "test_password",
                "polling_interval": 30,
            }

            mock_device_data = {
                "device_id": "test_device_id",
                "name": "ecoNET300 Test Device",
                "manufacturer": "PLUM",
                "model": "ecoNET300",
                "sw_version": "1.0.0",
            }

            mock_entity_data = {
                "entity_id": "sensor.econet300_temperature",
                "name": "Temperature",
                "state": "25.5",
                "attributes": {
                    "unit_of_measurement": "°C",
                    "device_class": "temperature",
                },
            }

            # Test that our redaction function works with mock HA data
            # Test config entry data redaction
            if _redact_data is None:
                result.add_failure("_redact_data function not available")
                return result
            redacted_config = _redact_data(mock_config_entry_data, TO_REDACT)  # type: ignore[misc]
            if redacted_config["host"] == "**REDACTED**":
                result.add_success("Mock config entry data redacted correctly")
            else:
                result.add_failure("Mock config entry data not redacted correctly")

            # Test device data redaction
            redacted_device = _redact_data(mock_device_data, TO_REDACT)  # type: ignore[misc]
            if redacted_device["name"] == "ecoNET300 Test Device":
                result.add_success("Mock device data preserved correctly")
            else:
                result.add_failure("Mock device data not preserved correctly")

            # Test entity data redaction
            redacted_entity = _redact_data(mock_entity_data, TO_REDACT)  # type: ignore[misc]
            if redacted_entity["state"] == "25.5":
                result.add_success("Mock entity data preserved correctly")
            else:
                result.add_failure("Mock entity data not preserved correctly")

        except (ImportError, KeyError, TypeError) as e:
            result.add_failure(f"Mock diagnostic integration test failed: {e}")

        return result

    def run_all_tests(self) -> dict[str, TestResult]:
        """Run all diagnostic validation tests."""
        _LOGGER.info("🔍 Running Integrated Diagnostic Tests")
        _LOGGER.info("=" * 60)

        # Load diagnostics module first
        if not self.load_diagnostics():
            _LOGGER.error("Failed to load diagnostics module, aborting tests")
            return {}

        # Run all test categories
        test_methods = [
            self.test_simple_data_redaction,
            self.test_nested_data_redaction,
            self.test_complex_data_redaction,
            self.test_edge_cases,
            self.test_to_redact_list,
            self.test_diagnostic_functions_availability,
            self.test_mock_diagnostic_integration,
        ]

        # Run tests and collect results
        test_results = []

        def run_single_test(test_method):
            """Run a single test method and return result or error."""
            try:
                return test_method(), None
            except (ImportError, KeyError, TypeError, AttributeError) as e:
                return None, e

        for test_method in test_methods:
            result, error = run_single_test(test_method)
            if error is None:
                test_results.append(result)
            else:
                _LOGGER.error("Test %s crashed: %s", test_method.__name__, error)
                error_result = TestResult(test_method.__name__)
                error_result.add_failure(f"Test crashed: {error}")
                test_results.append(error_result)

        # Store results
        for result in test_results:
            self.results[result.name] = result

        return self.results

    def generate_report(self) -> str:
        """Generate comprehensive test report."""
        report_lines = []
        report_lines.append("ecoNET300 Integrated Diagnostic Tests Report")
        report_lines.append("=" * 60)
        report_lines.append("")

        # Summary
        total_passed = sum(r.passed for r in self.results.values())
        total_failed = sum(r.failed for r in self.results.values())
        total_warnings = sum(len(r.warnings) for r in self.results.values())

        report_lines.append("📊 SUMMARY")
        report_lines.append("-" * 20)
        report_lines.append(f"Total tests passed: {total_passed}")
        report_lines.append(f"Total tests failed: {total_failed}")
        report_lines.append(f"Total warnings: {total_warnings}")
        report_lines.append("")

        # Individual test results
        for test_name, result in self.results.items():
            report_lines.append(f"🔧 {test_name}")
            report_lines.append("-" * 30)
            report_lines.append(
                f"Status: {'✅ PASSED' if result.is_success() else '❌ FAILED'}"
            )
            report_lines.append(
                f"Results: {result.passed} passed, {result.failed} failed"
            )

            if result.errors:
                report_lines.append("Errors:")
                report_lines.extend(f"  - {error}" for error in result.errors)

            if result.warnings:
                report_lines.append("Warnings:")
                report_lines.extend(f"  - {warning}" for warning in result.warnings)

            report_lines.append("")

        # Overall status
        report_lines.append("=" * 60)
        if total_failed == 0:
            report_lines.append("🎉 ALL TESTS PASSED!")
        else:
            report_lines.append(f"⚠️  {total_failed} TESTS FAILED")
        report_lines.append("=" * 60)

        return "\n".join(report_lines)


def main():
    """Run integrated diagnostic tests."""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO, format="%(message)s", handlers=[logging.StreamHandler()]
    )

    # Run tests
    validator = DiagnosticsValidator()
    results = validator.run_all_tests()

    # Generate and display report
    report = validator.generate_report()
    _LOGGER.info(report)

    # Save report to file
    report_file = (
        Path(__file__).parent / "test_reports" / "diagnostics_integrated_report.txt"
    )
    report_file.parent.mkdir(exist_ok=True)  # Ensure the directory exists
    with report_file.open("w", encoding="utf-8") as f:
        f.write(report)

    _LOGGER.info("📄 Detailed report saved to: %s", report_file)

    # Return success status
    total_failed = sum(r.failed for r in results.values())
    return total_failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
