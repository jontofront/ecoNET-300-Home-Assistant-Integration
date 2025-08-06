#!/usr/bin/env python3
"""API Endpoint Testing Script for ecoNET-300.

This script systematically tests all discovered API endpoints and documents
their response structures to understand the complete API.

Usage:
    python test_api_endpoints.py --host 10.10.1.77 --username admin --password password
"""

import argparse
from datetime import datetime
import json
import logging
from pathlib import Path
import sys
import time
from typing import Any, Dict, List

import requests
from requests.auth import HTTPBasicAuth

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
_LOGGER = logging.getLogger(__name__)


class ApiEndpointTester:
    """Test all discovered API endpoints and document their responses."""

    def __init__(self, host: str, username: str, password: str):
        """Initialize the API tester."""
        self.host = (
            host if host.startswith(("http://", "https://")) else f"http://{host}"
        )
        self.username = username
        self.password = password
        self.auth = HTTPBasicAuth(username, password)
        self.session = requests.Session()
        self.session.auth = self.auth
        self.timeout = 30

        # Test results
        self.test_results: Dict[str, Any] = {}
        self.endpoint_responses: Dict[str, Any] = {}

    def test_endpoint(self, endpoint: str) -> Dict[str, Any]:
        """Test a single endpoint and return the result."""
        url = f"{self.host}/econet/{endpoint}"

        result = {
            "endpoint": endpoint,
            "url": url,
            "status_code": None,
            "response_time": None,
            "response_size": None,
            "content_type": None,
            "is_json": False,
            "data": None,
            "error": None,
            "structure": None,
        }

        try:
            _LOGGER.info("Testing endpoint: %s", endpoint)

            # Make request and measure time
            start_time = time.time()
            response = self.session.get(url, timeout=self.timeout)
            end_time = time.time()

            result["status_code"] = response.status_code
            result["response_time"] = round(end_time - start_time, 3)
            result["response_size"] = len(response.content)
            result["content_type"] = response.headers.get("content-type", "unknown")

            if response.status_code == 200:
                # Try to parse as JSON
                try:
                    data = response.json()
                    result["is_json"] = True
                    result["data"] = data
                    result["structure"] = self.analyze_json_structure(data)
                    _LOGGER.info("✅ %s: JSON response (%d items)", endpoint, len(data))
                except json.JSONDecodeError:
                    result["data"] = response.text[:1000]  # First 1000 chars
                    result["structure"] = "text"
                    _LOGGER.info(
                        "✅ %s: Text response (%d chars)", endpoint, len(response.text)
                    )
            else:
                result["error"] = f"HTTP {response.status_code}"
                _LOGGER.warning("❌ %s: %s", endpoint, result["error"])

        except Exception as e:
            result["error"] = str(e)
            _LOGGER.error("❌ %s: %s", endpoint, e)

        return result

    def analyze_json_structure(
        self, data: Any, max_depth: int = 3, current_depth: int = 0
    ) -> Any:
        """Analyze JSON structure recursively."""
        if current_depth >= max_depth:
            return "..."

        if isinstance(data, dict):
            structure = {}
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    structure[key] = self.analyze_json_structure(
                        value, max_depth, current_depth + 1
                    )
                else:
                    structure[key] = type(value).__name__
            return structure
        elif isinstance(data, list):
            if len(data) == 0:
                return "[]"
            if len(data) == 1:
                return [
                    self.analyze_json_structure(data[0], max_depth, current_depth + 1)
                ]
            return [
                self.analyze_json_structure(data[0], max_depth, current_depth + 1),
                f"... ({len(data)} items)",
            ]
        else:
            return type(data).__name__

    def get_all_endpoints(self) -> List[str]:
        """Get list of all endpoints to test (safe endpoints only)."""
        # Core endpoints
        core_endpoints = [
            "sysParams",
            "regParams",
            "regParamsData",
            "rmCurrentDataParamsEdits",
        ]

        # Discovered endpoints (safe for testing)
        discovered_endpoints = [
            "rmCurrentDataParams",
            "rmParamsData",
            "rmParamsNames",
            "rmParamsEnums",
            "rmStructure",
            "rmAlarmsNames",
            "rmAlarms",
            "rmStatus",
            "rmDiagnostics",
            "rmLogs",
            "rmConfig",
            "rmFirmware",
            "rmUsers",
            "rmSchedule",
            "rmStatistics",
            "rmMaintenance",
            "rmService",
            "rmTest",
        ]

        # Additional endpoints to try (safe for testing)
        additional_endpoints = [
            "rmParamsDescs",
            "rmCatsNames",
            "rmExistingLangs",
            "rmParamsStructure",
            "rmParamsLimits",
            "rmParamsUnits",
            "rmParamsTypes",
            "rmParamsAccess",
            "rmParamsEdit",
            "rmParamsRead",
            "rmParamsWrite",
            "rmParamsValidate",
            "rmParamsDefault",
            "rmParamsCurrent",
            "rmParamsHistory",
            "rmParamsTrends",
            "rmParamsAlarms",
            "rmParamsEvents",
            "rmParamsLogs",
            "rmParamsDebug",
        ]

        return core_endpoints + discovered_endpoints + additional_endpoints

    def test_all_endpoints(self) -> Dict[str, Any]:
        """Test all endpoints and collect results."""
        _LOGGER.info("Starting comprehensive API endpoint testing...")

        endpoints = self.get_all_endpoints()
        results = {
            "test_info": {
                "host": self.host,
                "tested_at": datetime.now().isoformat(),
                "total_endpoints": len(endpoints),
                "successful_tests": 0,
                "failed_tests": 0,
            },
            "endpoints": {},
        }

        for endpoint in endpoints:
            result = self.test_endpoint(endpoint)
            results["endpoints"][endpoint] = result

            if result["status_code"] == 200:
                results["test_info"]["successful_tests"] += 1
            else:
                results["test_info"]["failed_tests"] += 1

        return results

    def save_results(
        self, results: Dict[str, Any], output_dir: str = "api_test_results"
    ):
        """Save test results to files."""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        # Save complete results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = output_path / f"api_test_results_{timestamp}.json"
        with results_file.open("w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        _LOGGER.info("Saved complete results to: %s", results_file)

        # Create summary report
        summary_file = output_path / f"api_test_summary_{timestamp}.md"
        self.create_summary_report(results, summary_file)
        _LOGGER.info("Saved summary report to: %s", summary_file)

        # Create endpoint documentation
        docs_file = output_path / f"api_endpoint_documentation_{timestamp}.md"
        self.create_endpoint_documentation(results, docs_file)
        _LOGGER.info("Saved endpoint documentation to: %s", docs_file)

    def create_summary_report(self, results: Dict[str, Any], file_path: Path):
        """Create a summary report of the test results."""
        with file_path.open("w", encoding="utf-8") as f:
            f.write("# ecoNET-300 API Endpoint Test Results\n\n")

            # Test info
            test_info = results["test_info"]
            f.write(f"**Test Date:** {test_info['tested_at']}\n")
            f.write(f"**Host:** {test_info['host']}\n")
            f.write(f"**Total Endpoints Tested:** {test_info['total_endpoints']}\n")
            f.write(f"**Successful:** {test_info['successful_tests']}\n")
            f.write(f"**Failed:** {test_info['failed_tests']}\n\n")

            # Successful endpoints
            f.write("## ✅ Successful Endpoints\n\n")
            successful = [
                ep
                for ep, result in results["endpoints"].items()
                if result["status_code"] == 200
            ]
            for endpoint in successful:
                result = results["endpoints"][endpoint]
                f.write(
                    f"- **{endpoint}** ({result['response_time']}s, {result['response_size']} bytes)\n"
                )
            f.write("\n")

            # Failed endpoints
            f.write("## ❌ Failed Endpoints\n\n")
            failed = [
                ep
                for ep, result in results["endpoints"].items()
                if result["status_code"] != 200
            ]
            for endpoint in failed:
                result = results["endpoints"][endpoint]
                error_msg = result.get(
                    "error", f'HTTP {result.get("status_code", "Unknown")}'
                )
                f.write(f"- **{endpoint}**: {error_msg}\n")
            f.write("\n")

            # Response types
            f.write("## 📊 Response Types\n\n")
            json_responses = [
                ep
                for ep, result in results["endpoints"].items()
                if result.get("is_json", False)
            ]
            text_responses = [
                ep
                for ep, result in results["endpoints"].items()
                if result["status_code"] == 200 and not result.get("is_json", False)
            ]

            f.write(f"**JSON Responses:** {len(json_responses)}\n")
            f.write(f"**Text Responses:** {len(text_responses)}\n")
            f.write(f"**Failed Requests:** {len(failed)}\n\n")

    def create_endpoint_documentation(self, results: Dict[str, Any], file_path: Path):
        """Create detailed endpoint documentation."""
        with file_path.open("w", encoding="utf-8") as f:
            f.write("# ecoNET-300 API Endpoint Documentation\n\n")
            f.write(f"**Generated:** {results['test_info']['tested_at']}\n\n")

            # Group endpoints by status
            successful = {
                ep: result
                for ep, result in results["endpoints"].items()
                if result["status_code"] == 200
            }

            for endpoint, result in successful.items():
                f.write(f"## {endpoint}\n\n")
                f.write(f"- **URL:** `{result['url']}`\n")
                f.write("- **Method:** GET\n")
                f.write(f"- **Response Time:** {result['response_time']}s\n")
                f.write(f"- **Response Size:** {result['response_size']} bytes\n")
                f.write(f"- **Content Type:** {result['content_type']}\n")
                f.write(
                    f"- **Response Type:** {'JSON' if result['is_json'] else 'Text'}\n\n"
                )

                if result.get("structure"):
                    f.write("### Response Structure\n\n")
                    f.write("```json\n")
                    f.write(json.dumps(result["structure"], indent=2))
                    f.write("\n```\n\n")

                if (
                    result.get("data")
                    and isinstance(result["data"], dict)
                    and len(result["data"]) < 10
                ):
                    f.write("### Sample Response\n\n")
                    f.write("```json\n")
                    f.write(json.dumps(result["data"], indent=2, ensure_ascii=False))
                    f.write("\n```\n\n")

                f.write("---\n\n")

    def run_tests(self) -> bool:
        """Run all API endpoint tests."""
        try:
            _LOGGER.info("Starting ecoNET-300 API endpoint testing...")

            # Test all endpoints
            results = self.test_all_endpoints()

            # Save results
            self.save_results(results)

            # Print summary
            test_info = results["test_info"]
            _LOGGER.info("Testing completed!")
            _LOGGER.info("Total endpoints: %d", test_info["total_endpoints"])
            _LOGGER.info("Successful: %d", test_info["successful_tests"])
            _LOGGER.info("Failed: %d", test_info["failed_tests"])

            return True

        except Exception as e:
            _LOGGER.error("Testing failed: %s", e)
            return False


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Test ecoNET-300 API Endpoints")
    parser.add_argument("--host", required=True, help="Device IP address or hostname")
    parser.add_argument("--username", required=True, help="Username for authentication")
    parser.add_argument("--password", required=True, help="Password for authentication")
    parser.add_argument(
        "--output-dir", default="api_test_results", help="Output directory for results"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    tester = ApiEndpointTester(args.host, args.username, args.password)

    # Test safe endpoints only
    results = tester.test_all_endpoints()

    # Save results
    tester.save_results(results, args.output_dir)

    # Print summary
    test_info = results["test_info"]
    _LOGGER.info("Testing completed!")
    _LOGGER.info("Total endpoints: %d", test_info["total_endpoints"])
    _LOGGER.info("Successful: %d", test_info["successful_tests"])
    _LOGGER.info("Failed: %d", test_info["failed_tests"])

    sys.exit(0)


if __name__ == "__main__":
    main()
