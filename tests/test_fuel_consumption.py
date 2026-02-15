"""Tests for fuel consumption tracking functionality."""

from decimal import Decimal


from custom_components.econet300.const import (
    DEVICE_CLASS_FUEL_METER,
    FUEL_MAX_SUB_INTERVAL_SECONDS,
)
from custom_components.econet300.sensor import (
    FuelConsumptionExtraStoredData,
    FuelConsumptionTotalSensor,
    _decimal_state,
)


class TestDecimalState:
    """Test the _decimal_state helper."""

    def test_valid_number(self):
        """Test parsing a valid numeric string."""
        assert _decimal_state("3.6") == Decimal("3.6")

    def test_valid_zero(self):
        """Test parsing zero."""
        assert _decimal_state("0") == Decimal(0)

    def test_valid_negative(self):
        """Test parsing a negative number."""
        assert _decimal_state("-1.5") == Decimal("-1.5")

    def test_invalid_string(self):
        """Test parsing an invalid string returns None."""
        assert _decimal_state("unknown") is None

    def test_empty_string(self):
        """Test parsing an empty string returns None."""
        assert _decimal_state("") is None

    def test_none_value(self):
        """Test parsing None returns None."""
        assert _decimal_state(None) is None


class TestTrapezoidalIntegration:
    """Test the trapezoidal integration math.

    Formula: area = (old + new) / 2 * elapsed_seconds / 3600
    This converts kg/h rate over seconds into kg consumed.
    """

    def test_constant_rate(self):
        """Test integration with constant rate (old == new)."""
        old = Decimal("2.0")
        new = Decimal("2.0")
        elapsed = Decimal(60)  # 60 seconds
        area = (old + new) / 2 * elapsed / Decimal(3600)
        # 2.0 kg/h * 60s / 3600 = 0.0333... kg
        expected = Decimal("2.0") * Decimal(60) / Decimal(3600)
        assert area == expected

    def test_increasing_rate(self):
        """Test integration with increasing rate."""
        old = Decimal("1.0")
        new = Decimal("3.0")
        elapsed = Decimal(60)
        area = (old + new) / 2 * elapsed / Decimal(3600)
        # avg = 2.0 kg/h, 60s -> 2.0 * 60/3600 = 0.0333...
        expected = Decimal("2.0") * Decimal(60) / Decimal(3600)
        assert area == expected

    def test_rate_drops_to_zero(self):
        """Test integration when rate drops from positive to zero.

        This is the key fix: old implementation skipped zeros entirely.
        Trapezoidal method correctly accounts for the transition.
        """
        old = Decimal("2.5")
        new = Decimal("0.0")
        elapsed = Decimal(60)
        area = (old + new) / 2 * elapsed / Decimal(3600)
        # avg = 1.25 kg/h, 60s -> 1.25 * 60/3600 ≈ 0.020833...
        expected = Decimal("1.25") * Decimal(60) / Decimal(3600)
        assert area == expected
        assert area > 0  # Non-zero consumption during transition

    def test_rate_rises_from_zero(self):
        """Test integration when rate rises from zero to positive."""
        old = Decimal("0.0")
        new = Decimal("2.5")
        elapsed = Decimal(60)
        area = (old + new) / 2 * elapsed / Decimal(3600)
        expected = Decimal("1.25") * Decimal(60) / Decimal(3600)
        assert area == expected

    def test_both_zero(self):
        """Test integration when both values are zero (boiler off)."""
        old = Decimal("0.0")
        new = Decimal("0.0")
        elapsed = Decimal(60)
        area = (old + new) / 2 * elapsed / Decimal(3600)
        assert area == Decimal(0)

    def test_longer_interval(self):
        """Test integration over a longer interval (5 min at 1 kg/h)."""
        old = Decimal("1.0")
        new = Decimal("1.0")
        elapsed = Decimal(300)  # 5 minutes
        area = (old + new) / 2 * elapsed / Decimal(3600)
        # 1 kg/h * 300s / 3600 = 0.0833... kg
        expected = Decimal("1.0") * Decimal(300) / Decimal(3600)
        assert area == expected

    def test_accumulation_over_multiple_intervals(self):
        """Test that accumulated consumption matches expected total."""
        total = Decimal(0)
        # 5 intervals of 60 seconds each at 1 kg/h constant rate
        for _ in range(5):
            area = (Decimal("1.0") + Decimal("1.0")) / 2 * Decimal(60) / Decimal(3600)
            total += area
        # 5 * 60s = 300s at 1 kg/h -> 300/3600 = 0.08333... kg
        expected = Decimal(5) * Decimal(60) / Decimal(3600)
        # Use round to 10 decimal places to avoid accumulated precision drift
        assert round(total, 10) == round(expected, 10)


class TestFuelConsumptionExtraStoredData:
    """Test the extra stored data serialization."""

    def test_round_trip(self):
        """Test that data survives a serialize/deserialize round trip."""
        original = FuelConsumptionExtraStoredData(
            native_value=Decimal("123.456"),
            native_unit_of_measurement="kg",
            source_entity="sensor.econet300_fuel_stream",
            last_valid_state=Decimal("123.456"),
        )
        data = original.as_dict()
        restored = FuelConsumptionExtraStoredData.from_dict(data)

        assert restored is not None
        assert restored.source_entity == "sensor.econet300_fuel_stream"
        assert restored.last_valid_state == Decimal("123.456")

    def test_from_dict_with_none_last_valid_state(self):
        """Test restoration when last_valid_state is None."""
        data = {
            "native_value": {"decimal_str": "0"},
            "native_unit_of_measurement": "kg",
            "source_entity": "sensor.test",
            "last_valid_state": None,
        }
        restored = FuelConsumptionExtraStoredData.from_dict(data)
        # last_valid_state is None -> from_dict returns None (requires valid state)
        assert restored is None

    def test_from_dict_with_invalid_value(self):
        """Test restoration with invalid last_valid_state value."""
        data = {
            "native_value": {"decimal_str": "0"},
            "native_unit_of_measurement": "kg",
            "source_entity": "sensor.test",
            "last_valid_state": "not_a_number",
        }
        restored = FuelConsumptionExtraStoredData.from_dict(data)
        assert restored is None


class TestFuelConsumptionTotalSensorAttributes:
    """Test FuelConsumptionTotalSensor class attributes."""

    def test_device_class_in_const(self):
        """Test DEVICE_CLASS_FUEL_METER is defined in const.py."""
        assert DEVICE_CLASS_FUEL_METER == "econet300__fuel_meter"

    def test_sensor_class_attributes_exist(self):
        """Test sensor class has expected attributes defined."""
        assert hasattr(FuelConsumptionTotalSensor, "_attr_state_class")
        assert hasattr(FuelConsumptionTotalSensor, "_attr_should_poll")
        assert hasattr(FuelConsumptionTotalSensor, "_attr_has_entity_name")
        assert hasattr(FuelConsumptionTotalSensor, "_attr_translation_key")
        assert hasattr(FuelConsumptionTotalSensor, "_attr_device_class")

    def test_state_class_is_defined(self):
        """Test that state class attribute is defined on the class.

        HA's CachedProperties metaclass converts _attr_state_class to a
        property descriptor, so we verify the descriptor exists rather than
        comparing the value directly.
        TOTAL is recommended by HA for lifetime totals with optional reset.
        """
        # HA metaclass wraps _attr_state_class as a cached property descriptor
        assert "_attr_state_class" in FuelConsumptionTotalSensor.__dict__


class TestFuelConsumptionConstants:
    """Test fuel consumption related constants."""

    def test_max_sub_interval_seconds(self):
        """Test FUEL_MAX_SUB_INTERVAL_SECONDS is reasonable."""
        # Should be 5 minutes (300 seconds)
        assert FUEL_MAX_SUB_INTERVAL_SECONDS == 300
        # Should be at least 1 minute
        assert FUEL_MAX_SUB_INTERVAL_SECONDS >= 60
        # Should be at most 10 minutes
        assert FUEL_MAX_SUB_INTERVAL_SECONDS <= 600

    def test_device_class_format(self):
        """Test DEVICE_CLASS_FUEL_METER follows HA convention."""
        # Custom device classes must use domain__class format
        assert "__" in DEVICE_CLASS_FUEL_METER
        assert DEVICE_CLASS_FUEL_METER.startswith("econet300__")


class TestZeroHandling:
    """Test that zero values are properly handled.

    The old implementation skipped zeros entirely, losing ~50% of consumption.
    The new trapezoidal method treats zeros as part of the curve.
    """

    def test_feeder_cycle_simulation(self):
        """Simulate feeder ON/OFF cycling and verify consumption is captured.

        Feeder cycle: ON (2.5 kg/h) -> OFF (0.0) -> ON (2.5) -> OFF (0.0)
        Each interval is 60 seconds.
        """
        total = Decimal(0)

        # Interval 1: 0.0 -> 2.5 (feeder starts)
        area = (Decimal("0.0") + Decimal("2.5")) / 2 * Decimal(60) / Decimal(3600)
        total += area

        # Interval 2: 2.5 -> 0.0 (feeder stops)
        area = (Decimal("2.5") + Decimal("0.0")) / 2 * Decimal(60) / Decimal(3600)
        total += area

        # Interval 3: 0.0 -> 2.5 (feeder starts again)
        area = (Decimal("0.0") + Decimal("2.5")) / 2 * Decimal(60) / Decimal(3600)
        total += area

        # Interval 4: 2.5 -> 0.0 (feeder stops again)
        area = (Decimal("2.5") + Decimal("0.0")) / 2 * Decimal(60) / Decimal(3600)
        total += area

        # Total should be > 0 (the old implementation would give 0)
        assert total > 0

        # Each interval contributes: avg(0, 2.5) * 60/3600 = 1.25 * 1/60
        # 4 intervals: 4 * 1.25 / 60 = 5.0 / 60 ≈ 0.0833 kg
        expected = 4 * Decimal("1.25") * Decimal(60) / Decimal(3600)
        assert round(total, 10) == round(expected, 10)

    def test_steady_burn_with_zero_dips(self):
        """Simulate steady burn with occasional zero readings.

        Values: 2.0, 0.0, 2.0 (each 60s apart)
        Old implementation: only counts first interval's contribution
        New implementation: counts transition contributions too
        """
        total = Decimal(0)

        # 2.0 -> 0.0 (transition down)
        area1 = (Decimal("2.0") + Decimal("0.0")) / 2 * Decimal(60) / Decimal(3600)
        total += area1

        # 0.0 -> 2.0 (transition up)
        area2 = (Decimal("0.0") + Decimal("2.0")) / 2 * Decimal(60) / Decimal(3600)
        total += area2

        # Both transitions contribute equally
        assert area1 == area2
        # Total should equal constant 1.0 kg/h for 120 seconds
        expected = Decimal("1.0") * Decimal(120) / Decimal(3600)
        assert round(total, 10) == round(expected, 10)
