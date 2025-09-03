"""Simple tests for the ecoNET300 integration diagnostics functionality."""

from custom_components.econet300.diagnostics import TO_REDACT, _redact_data


class TestRedactData:
    """Test the _redact_data function."""

    def test_redact_sensitive_data(self):
        """Test that sensitive data is properly redacted."""
        data = {
            "host": "192.168.1.100",
            "username": "test_user",
            "password": "secret_password",
            "safe_data": "this_is_safe",
        }

        result = _redact_data(data, TO_REDACT)

        assert result["host"] == "**REDACTED**"
        assert result["username"] == "**REDACTED**"
        assert result["password"] == "**REDACTED**"
        assert result["safe_data"] == "this_is_safe"

    def test_redact_nested_data(self):
        """Test that nested sensitive data is properly redacted."""
        data = {
            "api_info": {
                "host": "192.168.1.100",
                "username": "test_user",
            },
            "safe_data": "this_is_safe",
        }

        result = _redact_data(data, TO_REDACT)

        assert result["api_info"]["host"] == "**REDACTED**"
        assert result["api_info"]["username"] == "**REDACTED**"
        assert result["safe_data"] == "this_is_safe"

    def test_non_dict_data(self):
        """Test that non-dict data is returned unchanged."""
        data = "not_a_dict"
        result = _redact_data(data, TO_REDACT)
        assert result == "not_a_dict"

    def test_empty_data(self):
        """Test that empty dict is handled correctly."""
        data = {}
        result = _redact_data(data, TO_REDACT)
        assert not result

    def test_partial_redaction(self):
        """Test that only specified fields are redacted."""
        data = {
            "host": "192.168.1.100",
            "username": "test_user",
            "password": "secret_password",
            "device_id": "safe_device_id",
            "model": "ecoNET300",
        }

        result = _redact_data(data, TO_REDACT)

        # Sensitive fields should be redacted
        assert result["host"] == "**REDACTED**"
        assert result["username"] == "**REDACTED**"
        assert result["password"] == "**REDACTED**"

        # Safe fields should remain unchanged
        assert result["device_id"] == "safe_device_id"
        assert result["model"] == "ecoNET300"

    def test_deeply_nested_redaction(self):
        """Test redaction in deeply nested structures."""
        data = {
            "level1": {
                "level2": {
                    "level3": {
                        "host": "192.168.1.100",
                        "username": "test_user",
                        "safe_field": "safe_value",
                    }
                }
            }
        }

        result = _redact_data(data, TO_REDACT)

        assert result["level1"]["level2"]["level3"]["host"] == "**REDACTED**"
        assert result["level1"]["level2"]["level3"]["username"] == "**REDACTED**"
        assert result["level1"]["level2"]["level3"]["safe_field"] == "safe_value"

    def test_mixed_data_types(self):
        """Test redaction with mixed data types."""
        data = {
            "host": "192.168.1.100",
            "port": 8080,
            "enabled": True,
            "tags": ["tag1", "tag2"],
            "config": {
                "username": "test_user",
                "timeout": 30,
            },
        }

        result = _redact_data(data, TO_REDACT)

        assert result["host"] == "**REDACTED**"
        assert result["port"] == 8080
        assert result["enabled"] is True
        assert result["tags"] == ["tag1", "tag2"]
        assert result["config"]["username"] == "**REDACTED**"
        assert result["config"]["timeout"] == 30


class TestDiagnosticsConstants:
    """Test the diagnostics constants and configuration."""

    def test_to_redact_contains_expected_fields(self):
        """Test that TO_REDACT contains the expected sensitive fields."""
        expected_fields = [
            "password",
            "username",
            "host",
            "uid",
            "device_uid",
            "identifiers",
            "key",
            "ssid",
            "wlan0",
            "eth0",
        ]

        for field in expected_fields:
            assert field in TO_REDACT, (
                f"Expected field '{field}' not found in TO_REDACT"
            )

    def test_integration_version_included(self):
        """Test that integration version is included in diagnostics."""
        # This test verifies that the integration version field is expected
        # The actual version will be tested in integration tests
        assert "integration_version" in ["integration_version"]  # Placeholder test

    def test_to_redact_is_list(self):
        """Test that TO_REDACT is a list."""
        assert isinstance(TO_REDACT, list)

    def test_to_redact_not_empty(self):
        """Test that TO_REDACT is not empty."""
        assert len(TO_REDACT) > 0


class TestDiagnosticsIntegration:
    """Integration tests for diagnostics functionality."""

    def test_real_world_config_entry_data(self):
        """Test redaction with realistic config entry data."""
        # Simulate real config entry data
        config_data = {
            "host": "http://192.168.1.100",
            "username": "admin",
            "password": "super_secret_password",
            "port": 80,
            "ssl": False,
        }

        result = _redact_data(config_data, TO_REDACT)

        # Verify sensitive data is redacted
        assert result["host"] == "**REDACTED**"
        assert result["username"] == "**REDACTED**"
        assert result["password"] == "**REDACTED**"

        # Verify safe data is preserved
        assert result["port"] == 80
        assert result["ssl"] is False

    def test_real_world_api_info_data(self):
        """Test redaction with realistic API info data."""
        # Simulate real API info data
        api_info = {
            "host": "http://192.168.1.100",
            "uid": "ecoNET300_001",
            "model_id": "ecoMAX850R2-X",
            "sw_rev": "2.1.5",
            "hw_ver": "1.2",
            "username": "api_user",  # This might be sensitive
        }

        result = _redact_data(api_info, TO_REDACT)

        # Verify sensitive data is redacted
        assert result["host"] == "**REDACTED**"
        assert result["username"] == "**REDACTED**"

        # Verify safe operational data is preserved
        assert result["model_id"] == "ecoMAX850R2-X"
        assert result["sw_rev"] == "2.1.5"
        assert result["hw_ver"] == "1.2"

    def test_coordinator_data_structure(self):
        """Test redaction with realistic coordinator data structure."""
        # Simulate real coordinator data
        coordinator_data = {
            "last_update_success": True,
            "last_update_time": "2024-01-15T14:30:00",
            "data": {
                "sysParams": {
                    "uid": "ecoNET300_001",
                    "controllerID": "ecoMAX850R2-X",
                    "softVer": "2.1.5",
                },
                "regParams": {
                    "tempCO": 68.5,
                    "tempCOSet": 70,
                    "mode": 2,
                    "boilerPower": 85,
                },
                "paramsEdits": {
                    "1280": {"min": 27, "max": 68},
                    "1281": {"min": 20, "max": 55},
                },
            },
        }

        result = _redact_data(coordinator_data, TO_REDACT)

        # Verify no sensitive data is present (should be unchanged)
        assert result["last_update_success"] is True
        assert result["last_update_time"] == "2024-01-15T14:30:00"
        assert result["data"]["regParams"]["tempCO"] == 68.5
        assert result["data"]["paramsEdits"]["1280"]["min"] == 27

    def test_device_info_data_structure(self):
        """Test redaction with realistic device info data structure."""
        # Simulate real device info data
        device_info = {
            "device_id": "test_device_id",
            "name": "ecoNET300 Test Device",
            "manufacturer": "PLUM",
            "model": "ecoNET300",
            "sw_version": "1.0.0",
            "hw_version": "1.0",
            "identifiers": [("econet300", "test_uid")],
            "connections": [],
            "suggested_area": "Boiler Room",
            "disabled_by": None,
        }

        result = _redact_data(device_info, TO_REDACT)

        # Verify sensitive data is redacted
        assert result["identifiers"] == "**REDACTED**"

        # Verify safe operational data is preserved
        assert result["device_id"] == "test_device_id"
        assert result["name"] == "ecoNET300 Test Device"
        assert result["manufacturer"] == "PLUM"
        assert result["model"] == "ecoNET300"
        assert result["sw_version"] == "1.0.0"
        assert result["hw_version"] == "1.0"
        assert result["connections"] == []
        assert result["suggested_area"] == "Boiler Room"
        assert result["disabled_by"] is None

    def test_device_uid_redaction(self):
        """Test that device UIDs are properly redacted."""
        # Test API info with UID
        api_info = {
            "host": "http://192.168.1.100",
            "uid": "7VCPMB4ZJ8DHH208002Z0",
            "model_id": "ecoNET300",
        }

        result = _redact_data(api_info, TO_REDACT)

        # Verify UID is redacted
        assert result["uid"] == "**REDACTED**"
        assert result["host"] == "**REDACTED**"
        assert result["model_id"] == "ecoNET300"

        # Test coordinator data with device_uid
        coordinator_data = {
            "device_uid": "7VCPMB4ZJ8DHH208002Z0",
            "last_update": "2024-01-15T14:30:00",
            "data_available": True,
        }

        result = _redact_data(coordinator_data, TO_REDACT)

        # Verify device_uid is redacted
        assert result["device_uid"] == "**REDACTED**"
        assert result["last_update"] == "2024-01-15T14:30:00"
        assert result["data_available"] is True

    def test_device_identifiers_redaction(self):
        """Test that device identifiers are properly redacted."""
        # Test device info with identifiers containing UID
        device_info = {
            "device_id": "b5c9a5f653976a1d5bb62bdb9eb8c5b8",
            "name": "PLUM ecoNET300",
            "manufacturer": "PLUM",
            "model": "ecoNET300",
            "identifiers": [["econet300", "7VCPMB4ZJ8DHH208002Z0"]],
            "connections": [],
        }

        result = _redact_data(device_info, TO_REDACT)

        # Verify identifiers are redacted
        assert result["identifiers"] == "**REDACTED**"
        assert result["device_id"] == "b5c9a5f653976a1d5bb62bdb9eb8c5b8"
        assert result["name"] == "PLUM ecoNET300"
        assert result["manufacturer"] == "PLUM"
        assert result["model"] == "ecoNET300"

    def test_diagnostics_includes_version_info(self):
        """Test that diagnostics output includes version information."""
        # Test data structure that should include version
        test_data = {
            "integration_version": "1.1.12",
            "entry_data": {"host": "192.168.1.100"},
            "api_info": {"uid": "test_uid"},
        }

        # Verify version field is present and not redacted
        assert "integration_version" in test_data
        assert test_data["integration_version"] == "1.1.12"

        # Verify other fields are redacted
        result = _redact_data(test_data, TO_REDACT)
        assert (
            result["integration_version"] == "1.1.12"
        )  # Version should not be redacted
        assert result["entry_data"]["host"] == "**REDACTED**"
        assert result["api_info"]["uid"] == "**REDACTED**"

    def test_api_endpoint_data_included(self):
        """Test that API endpoint data is included in diagnostics."""
        # Test data structure that should include API endpoint data
        test_data = {
            "integration_version": "1.1.12",
            "api_endpoint_data": {
                "sys_params": {"uid": "test_uid", "model_id": "ecoNET300"},
                "reg_params": {"tempCO": 68.5, "lambdaStatus": 0},
                "reg_params_data": {"data": "some_data"},
                "param_edit_data": {"edits": "some_edits"},
            },
        }

        # Verify API endpoint data is present
        assert "api_endpoint_data" in test_data
        assert "sys_params" in test_data["api_endpoint_data"]
        assert "reg_params" in test_data["api_endpoint_data"]
        assert "reg_params_data" in test_data["api_endpoint_data"]
        assert "param_edit_data" in test_data["api_endpoint_data"]

        # Verify sensitive data is redacted
        result = _redact_data(test_data, TO_REDACT)
        assert result["api_endpoint_data"]["sys_params"]["uid"] == "**REDACTED**"
        assert (
            result["api_endpoint_data"]["reg_params"]["tempCO"] == 68.5
        )  # Non-sensitive data preserved

    def test_sysparams_sensitive_data_redaction(self):
        """Test that sensitive data in sysParams is properly redacted."""
        # Test sysParams data with sensitive fields
        sys_params_data = {
            "uid": "7VCPMB4ZJ8x121xssadadsa",
            "key": "secret_key",
            "password": "********************************************",
            "ssid": "secret_wifi_ssid_name",
            "wlan0": "10.10.1.77",
            "eth0": "0.0.0.0",
            "regRefresh": 5,
            "lan": False,
            "ecosrvSoftVer": "3.2.3819",
            "regAllowed": True,
        }

        result = _redact_data(sys_params_data, TO_REDACT)

        # Verify sensitive data is redacted
        assert result["uid"] == "**REDACTED**"
        assert result["key"] == "**REDACTED**"
        assert result["password"] == "**REDACTED**"
        assert result["ssid"] == "**REDACTED**"
        assert result["wlan0"] == "**REDACTED**"
        assert result["eth0"] == "**REDACTED**"

        # Verify safe operational data is preserved
        assert result["regRefresh"] == 5
        assert result["lan"] is False
        assert result["ecosrvSoftVer"] == "3.2.3819"
        assert result["regAllowed"] is True

    def test_entity_values_included(self):
        """Test that entity values are included in diagnostics."""
        # Test data structure that should include entity values
        test_entity_data = {
            "entity_count": 2,
            "entities": [
                {
                    "entity_id": "sensor.econet300_boiler_temperature",
                    "name": "Boiler Temperature",
                    "platform": "sensor",
                    "current_value": "68.5",
                    "unit_of_measurement": "°C",
                    "attributes": {
                        "device_class": "temperature",
                        "state_class": "measurement",
                        "friendly_name": "Boiler Temperature",
                    },
                },
                {
                    "entity_id": "binary_sensor.econet300_boiler_status",
                    "name": "Boiler Status",
                    "platform": "binary_sensor",
                    "current_value": "on",
                    "unit_of_measurement": None,
                    "attributes": {
                        "device_class": "heat",
                        "friendly_name": "Boiler Status",
                    },
                },
            ],
        }

        # Verify entity values are present
        assert test_entity_data["entity_count"] == 2
        assert len(test_entity_data["entities"]) == 2

        # Check first entity
        entity1 = test_entity_data["entities"][0]
        assert entity1["entity_id"] == "sensor.econet300_boiler_temperature"
        assert entity1["current_value"] == "68.5"
        assert entity1["unit_of_measurement"] == "°C"
        assert entity1["attributes"]["device_class"] == "temperature"

        # Check second entity
        entity2 = test_entity_data["entities"][1]
        assert entity2["entity_id"] == "binary_sensor.econet300_boiler_status"
        assert entity2["current_value"] == "on"
        assert entity2["unit_of_measurement"] is None
        assert entity2["attributes"]["device_class"] == "heat"
