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
        expected_fields = ["password", "username", "host"]

        for field in expected_fields:
            assert field in TO_REDACT, (
                f"Expected field '{field}' not found in TO_REDACT"
            )

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
        assert result["uid"] == "ecoNET300_001"
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
        assert result["data"]["sysParams"]["uid"] == "ecoNET300_001"
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

        # Verify no sensitive data is present (should be unchanged)
        assert result["device_id"] == "test_device_id"
        assert result["name"] == "ecoNET300 Test Device"
        assert result["manufacturer"] == "PLUM"
        assert result["model"] == "ecoNET300"
        assert result["sw_version"] == "1.0.0"
        assert result["hw_version"] == "1.0"
        assert result["identifiers"] == [("econet300", "test_uid")]
        assert result["connections"] == []
        assert result["suggested_area"] == "Boiler Room"
        assert result["disabled_by"] is None
