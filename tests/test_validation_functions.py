"""Tests for parameter validation functions in common_functions.py."""

import pytest

from custom_components.econet300.common_functions import (
    get_lock_reason,
    is_binary_enum,
    is_parameter_locked,
    should_be_select_entity,
    should_be_switch_entity,
    validate_parameter_data,
)


class TestValidateParameterData:
    """Tests for validate_parameter_data function."""

    def test_valid_parameter_with_all_fields(self):
        """Test validation passes for a complete valid parameter."""
        param = {
            "key": "tempCOSet",
            "name": "Boiler Temperature Setpoint",
            "edit": True,
            "unit_name": "°C",
            "minv": 30,
            "maxv": 80,
        }
        is_valid, error = validate_parameter_data(param)
        assert is_valid is True
        assert error == ""

    def test_missing_key(self):
        """Test validation fails when key is missing."""
        param = {
            "name": "Test Parameter",
            "edit": True,
        }
        is_valid, error = validate_parameter_data(param)
        assert is_valid is False
        assert "Missing parameter key" in error

    def test_missing_name(self):
        """Test validation fails when name is missing."""
        param = {
            "key": "test_key",
            "edit": True,
        }
        is_valid, error = validate_parameter_data(param)
        assert is_valid is False
        assert "Missing parameter name" in error

    def test_editable_number_missing_min_max(self):
        """Test validation fails for editable number without min/max."""
        param = {
            "key": "test_key",
            "name": "Test Parameter",
            "edit": True,
            "unit_name": "°C",
            # Missing minv and maxv
        }
        is_valid, error = validate_parameter_data(param)
        assert is_valid is False
        assert "Missing min/max" in error

    def test_editable_number_invalid_range(self):
        """Test validation fails when min >= max."""
        param = {
            "key": "test_key",
            "name": "Test Parameter",
            "edit": True,
            "unit_name": "°C",
            "minv": 80,
            "maxv": 30,  # Invalid: max < min
        }
        is_valid, error = validate_parameter_data(param)
        assert is_valid is False
        assert "Invalid min/max range" in error

    def test_editable_number_equal_range(self):
        """Test validation fails when min == max."""
        param = {
            "key": "test_key",
            "name": "Test Parameter",
            "edit": True,
            "unit_name": "°C",
            "minv": 50,
            "maxv": 50,  # Invalid: max == min
        }
        is_valid, error = validate_parameter_data(param)
        assert is_valid is False
        assert "Invalid min/max range" in error

    def test_non_editable_parameter_no_range_check(self):
        """Test validation passes for non-editable params without min/max."""
        param = {
            "key": "test_key",
            "name": "Test Parameter",
            "edit": False,  # Not editable, so no range check needed
            "unit_name": "°C",
        }
        is_valid, error = validate_parameter_data(param)
        assert is_valid is True
        assert error == ""

    def test_valid_enum_parameter(self):
        """Test validation passes for valid enum parameter."""
        param = {
            "key": "test_key",
            "name": "Test Parameter",
            "edit": True,
            "enum": {
                "values": ["OFF", "ON"],
                "first": 0,
            },
        }
        is_valid, error = validate_parameter_data(param)
        assert is_valid is True
        assert error == ""

    def test_invalid_enum_structure(self):
        """Test validation fails for invalid enum structure."""
        param = {
            "key": "test_key",
            "name": "Test Parameter",
            "edit": True,
            "enum": "not_a_dict",  # Invalid enum structure
        }
        is_valid, error = validate_parameter_data(param)
        assert is_valid is False
        assert "Invalid enum structure" in error

    def test_empty_enum_values(self):
        """Test validation fails for empty enum values."""
        param = {
            "key": "test_key",
            "name": "Test Parameter",
            "edit": True,
            "enum": {
                "values": [],  # Empty values
                "first": 0,
            },
        }
        is_valid, error = validate_parameter_data(param)
        assert is_valid is False
        assert "Empty enum values" in error


class TestIsParameterLocked:
    """Tests for is_parameter_locked function."""

    def test_locked_parameter(self):
        """Test returns True for locked parameter."""
        param = {"locked": True}
        assert is_parameter_locked(param) is True

    def test_unlocked_parameter(self):
        """Test returns False for unlocked parameter."""
        param = {"locked": False}
        assert is_parameter_locked(param) is False

    def test_missing_locked_field(self):
        """Test returns False when locked field is missing."""
        param = {}
        assert is_parameter_locked(param) is False

    def test_locked_with_reason(self):
        """Test returns True for locked parameter with reason."""
        param = {
            "locked": True,
            "lock_reason": "Weather control enabled.",
        }
        assert is_parameter_locked(param) is True


class TestGetLockReason:
    """Tests for get_lock_reason function."""

    def test_get_lock_reason_present(self):
        """Test returns lock reason when present."""
        param = {"lock_reason": "Requires turn off the controller."}
        assert get_lock_reason(param) == "Requires turn off the controller."

    def test_get_lock_reason_missing(self):
        """Test returns None when lock_reason is missing."""
        param = {}
        assert get_lock_reason(param) is None

    def test_get_lock_reason_none(self):
        """Test returns None when lock_reason is None."""
        param = {"lock_reason": None}
        assert get_lock_reason(param) is None

    def test_get_lock_reason_empty_string(self):
        """Test returns empty string when lock_reason is empty."""
        param = {"lock_reason": ""}
        assert get_lock_reason(param) == ""


class TestLockReasonsFromFixture:
    """Tests using lock reasons from fixture data."""

    @pytest.fixture
    def lock_reasons(self):
        """Load lock reasons from fixture."""
        return [
            "",
            "Requires turn off the controller.",
            "Weather control enabled.",
            "HUW mode off.",
            "Function unavailable.",
            "Lambda sensor calibration in progress",
            "",
        ]

    def test_lock_reason_weather_control(self, lock_reasons):
        """Test weather control lock reason."""
        param = {"lock_reason": lock_reasons[2]}
        assert get_lock_reason(param) == "Weather control enabled."

    def test_lock_reason_controller_off(self, lock_reasons):
        """Test controller off lock reason."""
        param = {"lock_reason": lock_reasons[1]}
        assert get_lock_reason(param) == "Requires turn off the controller."

    def test_lock_reason_huw_mode(self, lock_reasons):
        """Test HUW mode lock reason."""
        param = {"lock_reason": lock_reasons[3]}
        assert get_lock_reason(param) == "HUW mode off."

    def test_lock_reason_lambda_calibration(self, lock_reasons):
        """Test lambda calibration lock reason."""
        param = {"lock_reason": lock_reasons[5]}
        assert get_lock_reason(param) == "Lambda sensor calibration in progress"


class TestIsBinaryEnum:
    """Tests for is_binary_enum function."""

    def test_binary_on_off(self):
        """Test binary enum with OFF/ON values."""
        assert is_binary_enum(["OFF", "ON"]) is True

    def test_binary_yes_no(self):
        """Test binary enum with NO/YES values."""
        assert is_binary_enum(["NO", "YES"]) is True

    def test_binary_enabled_disabled(self):
        """Test binary enum with DISABLED/ENABLED values."""
        assert is_binary_enum(["DISABLED", "ENABLED"]) is True

    def test_non_binary_three_options(self):
        """Test non-binary enum with 3 options - only checks first 2."""
        # Note: is_binary_enum only checks first 2 values by design
        # This returns True because first 2 match binary pattern
        assert is_binary_enum(["OFF", "ON", "AUTO"]) is True

    def test_non_binary_pattern(self):
        """Test non-binary enum that doesn't match patterns."""
        assert is_binary_enum(["LOW", "MEDIUM", "HIGH"]) is False

    def test_empty_enum(self):
        """Test empty enum."""
        assert is_binary_enum([]) is False

    def test_single_value(self):
        """Test single value enum."""
        assert is_binary_enum(["ON"]) is False


class TestShouldBeSwitchEntity:
    """Tests for should_be_switch_entity function."""

    def test_binary_switch_with_min_max(self):
        """Test binary enum with min/max indicating 2 options."""
        param = {
            "edit": True,
            "enum": {"values": ["OFF", "ON"]},
            "minv": 0,
            "maxv": 1,
        }
        assert should_be_switch_entity(param) is True

    def test_three_option_enum_with_min_max_not_switch(self):
        """Test 3-option enum with min/max should NOT be switch."""
        param = {
            "edit": True,
            "enum": {"values": ["OFF", "ON", "AUTO"]},
            "minv": 0,
            "maxv": 2,
        }
        assert should_be_switch_entity(param) is False

    def test_three_option_enum_no_min_max_not_switch(self):
        """Test 3-option enum without min/max should NOT be switch.

        This is the key bug fix test - previously this would incorrectly
        return True because is_binary_enum only checks first 2 values.
        """
        param = {
            "edit": True,
            "enum": {"values": ["OFF", "ON", "AUTO"]},
            # No minv/maxv
        }
        assert should_be_switch_entity(param) is False

    def test_binary_switch_no_min_max(self):
        """Test binary enum without min/max still works as switch."""
        param = {
            "edit": True,
            "enum": {"values": ["OFF", "ON"]},
            # No minv/maxv - fallback to enum length check
        }
        assert should_be_switch_entity(param) is True

    def test_non_editable_not_switch(self):
        """Test non-editable param is not a switch."""
        param = {
            "edit": False,
            "enum": {"values": ["OFF", "ON"]},
            "minv": 0,
            "maxv": 1,
        }
        assert should_be_switch_entity(param) is False

    def test_locked_param_not_switch(self):
        """Test locked param is not a switch."""
        param = {
            "edit": True,
            "locked": True,
            "enum": {"values": ["OFF", "ON"]},
            "minv": 0,
            "maxv": 1,
        }
        assert should_be_switch_entity(param) is False

    def test_no_enum_not_switch(self):
        """Test param without enum is not a switch."""
        param = {
            "edit": True,
            "minv": 0,
            "maxv": 100,
        }
        assert should_be_switch_entity(param) is False


class TestShouldBeSelectEntity:
    """Tests for should_be_select_entity function."""

    def test_three_option_select_with_min_max(self):
        """Test 3-option enum with min/max is select."""
        param = {
            "edit": True,
            "enum": {"values": ["OFF", "ON", "AUTO"]},
            "minv": 0,
            "maxv": 2,
        }
        assert should_be_select_entity(param) is True

    def test_three_option_select_no_min_max(self):
        """Test 3-option enum without min/max is select.

        This is the key bug fix test - previously this would incorrectly
        return False because is_binary_enum returns True for first 2 values.
        """
        param = {
            "edit": True,
            "enum": {"values": ["OFF", "ON", "AUTO"]},
            # No minv/maxv
        }
        assert should_be_select_entity(param) is True

    def test_binary_enum_not_select(self):
        """Test binary enum with min/max indicating 2 options is not select."""
        param = {
            "edit": True,
            "enum": {"values": ["OFF", "ON"]},
            "minv": 0,
            "maxv": 1,
        }
        assert should_be_select_entity(param) is False

    def test_binary_enum_no_min_max_not_select(self):
        """Test binary enum without min/max is not select."""
        param = {
            "edit": True,
            "enum": {"values": ["OFF", "ON"]},
            # No minv/maxv
        }
        assert should_be_select_entity(param) is False

    def test_non_editable_not_select(self):
        """Test non-editable param is not a select."""
        param = {
            "edit": False,
            "enum": {"values": ["OFF", "ON", "AUTO"]},
            "minv": 0,
            "maxv": 2,
        }
        assert should_be_select_entity(param) is False

    def test_locked_param_not_select(self):
        """Test locked param is not a select."""
        param = {
            "edit": True,
            "locked": True,
            "enum": {"values": ["OFF", "ON", "AUTO"]},
            "minv": 0,
            "maxv": 2,
        }
        assert should_be_select_entity(param) is False

    def test_no_enum_not_select(self):
        """Test param without enum is not a select."""
        param = {
            "edit": True,
            "minv": 0,
            "maxv": 100,
        }
        assert should_be_select_entity(param) is False

    def test_many_options_select(self):
        """Test enum with many options is select."""
        param = {
            "edit": True,
            "enum": {"values": ["A", "B", "C", "D", "E"]},
            "minv": 0,
            "maxv": 4,
        }
        assert should_be_select_entity(param) is True


class TestSwitchSelectMutualExclusion:
    """Tests to ensure switch and select detection are mutually exclusive."""

    def test_binary_enum_switch_not_select(self):
        """Test binary enum is switch, not select."""
        param = {
            "edit": True,
            "enum": {"values": ["OFF", "ON"]},
            "minv": 0,
            "maxv": 1,
        }
        assert should_be_switch_entity(param) is True
        assert should_be_select_entity(param) is False

    def test_three_option_select_not_switch(self):
        """Test 3-option enum is select, not switch."""
        param = {
            "edit": True,
            "enum": {"values": ["OFF", "ON", "AUTO"]},
            "minv": 0,
            "maxv": 2,
        }
        assert should_be_switch_entity(param) is False
        assert should_be_select_entity(param) is True

    def test_three_option_no_min_max_select_not_switch(self):
        """Test 3-option enum without min/max is select, not switch.

        Critical test for the bug fix - ensures mutual exclusion
        when min/max are unavailable.
        """
        param = {
            "edit": True,
            "enum": {"values": ["OFF", "ON", "AUTO"]},
            # No minv/maxv
        }
        assert should_be_switch_entity(param) is False
        assert should_be_select_entity(param) is True

    def test_binary_no_min_max_switch_not_select(self):
        """Test binary enum without min/max is switch, not select."""
        param = {
            "edit": True,
            "enum": {"values": ["OFF", "ON"]},
            # No minv/maxv
        }
        assert should_be_switch_entity(param) is True
        assert should_be_select_entity(param) is False


class TestDuplicateNaming:
    """Tests for get_duplicate_display_name and get_duplicate_entity_key functions."""

    def test_mixer_description_display_name(self):
        """Test that mixer description produces (Mixer X) format."""
        from custom_components.econet300.common_functions import (
            get_duplicate_display_name,
        )

        description = "Setting parameter on YES value closes the mixer actuator"
        result = get_duplicate_display_name("Off by thermostat", 1, description)
        assert result == "Off by thermostat (Mixer 1)"

        result = get_duplicate_display_name("Off by thermostat", 2, description)
        assert result == "Off by thermostat (Mixer 2)"

    def test_mixer_description_entity_key(self):
        """Test that mixer description produces _mixer_X format."""
        from custom_components.econet300.common_functions import (
            get_duplicate_entity_key,
        )

        description = "The higher the value, the faster the mixer reaches"
        result = get_duplicate_entity_key("proportional_range", 1, description)
        assert result == "proportional_range_mixer_1"

        result = get_duplicate_entity_key("proportional_range", 3, description)
        assert result == "proportional_range_mixer_3"

    def test_huw_description_display_name(self):
        """Test that HUW/hot water description produces (HUW X) format."""
        from custom_components.econet300.common_functions import (
            get_duplicate_display_name,
        )

        description = "Temperature to which the hot water tank will be heated"
        result = get_duplicate_display_name("HUW preset", 1, description)
        assert result == "HUW preset"  # First one doesn't need suffix

        result = get_duplicate_display_name("HUW preset", 2, description)
        assert result == "HUW preset (HUW 2)"

    def test_fallback_numbering(self):
        """Test that unknown descriptions fall back to simple numbering."""
        from custom_components.econet300.common_functions import (
            get_duplicate_display_name,
            get_duplicate_entity_key,
        )

        description = "Some unknown parameter description"
        result = get_duplicate_display_name("Parameter", 3, description)
        assert result == "Parameter 3"

        result = get_duplicate_entity_key("parameter", 3, description)
        assert result == "parameter_3"

    def test_no_description_fallback(self):
        """Test that missing description falls back to simple numbering."""
        from custom_components.econet300.common_functions import (
            get_duplicate_display_name,
            get_duplicate_entity_key,
        )

        result = get_duplicate_display_name("Parameter", 2, None)
        assert result == "Parameter 2"

        result = get_duplicate_entity_key("parameter", 2, None)
        assert result == "parameter_2"

    def test_thermostat_circuit_naming(self):
        """Test that room thermostat description produces (Circuit X) format."""
        from custom_components.econet300.common_functions import (
            get_duplicate_display_name,
        )

        description = "Controls the room thermostat connection"
        result = get_duplicate_display_name("Thermostat control", 1, description)
        assert result == "Thermostat control (Circuit 1)"


# =============================================================================
# Alarm helper tests
# =============================================================================


class TestParseAlarmEntry:
    """Tests for parse_alarm_entry function."""

    def test_basic_alarm_with_names(self):
        """Test parsing an alarm with a name mapping."""
        from custom_components.econet300.common_functions import parse_alarm_entry

        alarm = {
            "code": 0,
            "fromDate": "2025-12-14 19:04:16",
            "toDate": "2025-12-14 19:08:27",
            "service": False,
        }
        names = {"0": "Power outage", "7": "Unsuccessful boiler firing-up attempt."}

        result = parse_alarm_entry(alarm, names)
        assert result["alarm_code"] == 0
        assert result["description"] == "Power outage"
        assert result["from_date"] == "2025-12-14 19:04:16"
        assert result["to_date"] == "2025-12-14 19:08:27"
        assert result["is_active"] is False
        assert result["service"] is False

    def test_alarm_with_string_code(self):
        """Test parsing alarm where code is a string (older API format)."""
        from custom_components.econet300.common_functions import parse_alarm_entry

        alarm = {
            "code": "7",
            "fromDate": "2024-10-15 23:18:10",
            "toDate": "2024-10-15 23:37:05",
        }
        names = {"7": "Unsuccessful boiler firing-up attempt.\\nEmpty the ashtray."}

        result = parse_alarm_entry(alarm, names)
        assert result["alarm_code"] == "7"
        assert "Unsuccessful" in result["description"]
        assert "\\n" not in result["description"]

    def test_active_alarm_to_date_none(self):
        """Test that toDate=None is detected as active alarm."""
        from custom_components.econet300.common_functions import parse_alarm_entry

        alarm = {
            "code": 1,
            "fromDate": "2131-07-15 00:42:35",
            "toDate": None,
            "service": False,
        }
        result = parse_alarm_entry(alarm, {"1": "Boiler temperature sensor damage."})
        assert result["is_active"] is True
        assert result["to_date"] is None

    def test_alarm_without_name_mapping(self):
        """Test fallback description when no name mapping is provided."""
        from custom_components.econet300.common_functions import parse_alarm_entry

        alarm = {"code": 42, "fromDate": "2025-01-01", "toDate": "2025-01-02"}
        result = parse_alarm_entry(alarm, None)
        assert result["description"] == "Alarm 42"

    def test_alarm_unknown_code(self):
        """Test fallback when code is not in the name mapping."""
        from custom_components.econet300.common_functions import parse_alarm_entry

        alarm = {"code": 99, "fromDate": "2025-01-01", "toDate": "2025-01-02"}
        result = parse_alarm_entry(alarm, {"0": "Power outage"})
        assert result["description"] == "Alarm 99"

    def test_alarm_missing_service_defaults_false(self):
        """Test that missing service field defaults to False."""
        from custom_components.econet300.common_functions import parse_alarm_entry

        alarm = {"code": 0, "fromDate": "2025-01-01", "toDate": "2025-01-02"}
        result = parse_alarm_entry(alarm, None)
        assert result["service"] is False


class TestGetLatestAlarm:
    """Tests for get_latest_alarm function."""

    def test_returns_first_alarm(self):
        """Test that the first alarm (most recent) is returned."""
        from custom_components.econet300.common_functions import get_latest_alarm

        alarms = [
            {"code": 0, "fromDate": "2025-12-14", "toDate": "2025-12-14"},
            {"code": 7, "fromDate": "2025-11-29", "toDate": "2025-11-29"},
        ]
        result = get_latest_alarm(alarms, {"0": "Power outage"})
        assert result is not None
        assert result["alarm_code"] == 0
        assert result["description"] == "Power outage"

    def test_empty_alarms_returns_none(self):
        """Test that empty list returns None."""
        from custom_components.econet300.common_functions import get_latest_alarm

        assert get_latest_alarm([], None) is None

    def test_none_alarms_returns_none(self):
        """Test that None-like input returns None."""
        from custom_components.econet300.common_functions import get_latest_alarm

        assert get_latest_alarm([], {}) is None


class TestGetActiveAlarm:
    """Tests for get_active_alarm function."""

    def test_detects_active_alarm(self):
        """Test detection of an active alarm (toDate is None)."""
        from custom_components.econet300.common_functions import get_active_alarm

        alarms = [
            {"code": 0, "fromDate": "2025-12-14", "toDate": "2025-12-14"},
            {"code": 1, "fromDate": "2025-11-29", "toDate": None},
        ]
        result = get_active_alarm(alarms, {"1": "Boiler temperature sensor damage."})
        assert result is not None
        assert result["is_active"] is True
        assert result["alarm_code"] == 1

    def test_no_active_alarm(self):
        """Test that no active alarm returns None."""
        from custom_components.econet300.common_functions import get_active_alarm

        alarms = [
            {"code": 0, "fromDate": "2025-12-14", "toDate": "2025-12-14"},
            {"code": 7, "fromDate": "2025-11-29", "toDate": "2025-11-29"},
        ]
        assert get_active_alarm(alarms, {}) is None

    def test_empty_alarms(self):
        """Test empty alarms list returns None."""
        from custom_components.econet300.common_functions import get_active_alarm

        assert get_active_alarm([], {}) is None


class TestHasActiveAlarm:
    """Tests for has_active_alarm function."""

    def test_has_active_alarm_true(self):
        """Test returns True when an active alarm exists."""
        from custom_components.econet300.common_functions import has_active_alarm

        alarms = [
            {"code": 0, "fromDate": "2025-12-14", "toDate": "2025-12-14"},
            {"code": 1, "fromDate": "2025-11-29", "toDate": None},
        ]
        assert has_active_alarm(alarms) is True

    def test_has_active_alarm_false(self):
        """Test returns False when no active alarm exists."""
        from custom_components.econet300.common_functions import has_active_alarm

        alarms = [
            {"code": 0, "fromDate": "2025-12-14", "toDate": "2025-12-14"},
        ]
        assert has_active_alarm(alarms) is False

    def test_empty_alarms(self):
        """Test returns False for empty alarms list."""
        from custom_components.econet300.common_functions import has_active_alarm

        assert has_active_alarm([]) is False
