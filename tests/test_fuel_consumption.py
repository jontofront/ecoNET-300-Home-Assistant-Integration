"""Tests for fuel consumption tracking functionality."""

from datetime import datetime, timezone
from unittest.mock import patch

import pytest

from custom_components.econet300.sensor import (
    DEVICE_CLASS_FUEL_METER,
    FuelConsumptionTracker,
    FuelConsumptionTotalSensor,
    MAX_TIME_DELTA_SECONDS,
)


class TestFuelConsumptionTracker:
    """Test the FuelConsumptionTracker class."""

    def test_initial_state(self):
        """Test tracker initializes with zero values."""
        tracker = FuelConsumptionTracker()

        assert tracker.total == 0.0
        assert tracker.last_reset is None
        assert tracker.last_update is None

    def test_update_with_none_value(self):
        """Test update with None fuel stream does not change total."""
        tracker = FuelConsumptionTracker()

        result = tracker.update(None)

        assert result == 0.0
        assert tracker.total == 0.0
        assert tracker.last_update is not None  # Should still update timestamp

    def test_update_with_zero_value(self):
        """Test update with zero fuel stream does not change total."""
        tracker = FuelConsumptionTracker()

        result = tracker.update(0.0)

        assert result == 0.0
        assert tracker.total == 0.0

    def test_update_with_negative_value(self):
        """Test update with negative fuel stream does not change total."""
        tracker = FuelConsumptionTracker()

        result = tracker.update(-1.5)

        assert result == 0.0
        assert tracker.total == 0.0

    def test_first_update_with_positive_value(self):
        """Test first update does not add consumption (no previous timestamp)."""
        tracker = FuelConsumptionTracker()

        result = tracker.update(2.0)  # 2 kg/h

        # First update should not add anything (no time delta)
        assert result == 0.0
        assert tracker.total == 0.0
        assert tracker.last_update is not None

    def test_consecutive_updates_accumulate(self):
        """Test consecutive updates accumulate consumption correctly."""
        tracker = FuelConsumptionTracker()

        # Set initial timestamp (simulating first update already happened)
        start_time = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        tracker._last_update = start_time

        # Mock time to be exactly 60 seconds later
        with patch("custom_components.econet300.sensor.datetime") as mock_datetime:
            future_time = datetime(2025, 1, 1, 12, 1, 0, tzinfo=timezone.utc)
            mock_datetime.now.return_value = future_time

            # Update with 3.6 kg/h for 60 seconds = 0.06 kg
            result = tracker.update(3.6)

            # Should accumulate 3.6 kg/h * (60/3600) h = 0.06 kg
            expected = 3.6 * (60 / 3600)
            assert result == pytest.approx(expected, rel=0.01)

    def test_reset(self):
        """Test reset clears total and sets last_reset."""
        tracker = FuelConsumptionTracker()
        tracker._total = 100.0

        tracker.reset()

        assert tracker.total == 0.0
        assert tracker.last_reset is not None
        assert tracker.last_update is not None
        assert tracker.last_reset == tracker.last_update

    def test_calibrate(self):
        """Test calibrate sets total to specific value."""
        tracker = FuelConsumptionTracker()
        tracker._total = 50.0

        tracker.calibrate(150.5)

        assert tracker.total == 150.5
        assert tracker.last_update is not None

    def test_restore(self):
        """Test restore sets values from storage."""
        tracker = FuelConsumptionTracker()
        reset_time = datetime.now(timezone.utc)

        tracker.restore(total=123.456, last_reset=reset_time)

        assert tracker.total == 123.456
        assert tracker.last_reset == reset_time

    def test_restore_with_none_values(self):
        """Test restore handles None values gracefully."""
        tracker = FuelConsumptionTracker()
        tracker._total = 50.0

        tracker.restore(total=None, last_reset=None)

        # Original values should remain
        assert tracker.total == 50.0
        assert tracker.last_reset is None

    def test_total_rounds_to_three_decimals(self):
        """Test total property rounds to 3 decimal places."""
        tracker = FuelConsumptionTracker()
        tracker._total = 1.23456789

        assert tracker.total == 1.235

    def test_max_time_delta_cap(self):
        """Test that time delta is capped to prevent spikes."""
        tracker = FuelConsumptionTracker()

        # Set last update to long ago
        tracker._last_update = datetime(2020, 1, 1, tzinfo=timezone.utc)

        # Update now - should cap delta to MAX_TIME_DELTA_SECONDS
        result = tracker.update(3.6)  # 3.6 kg/h

        # Maximum consumption = 3.6 kg/h * (MAX_TIME_DELTA_SECONDS / 3600) hours
        max_expected = 3.6 * (MAX_TIME_DELTA_SECONDS / 3600)
        assert result <= max_expected + 0.001  # Allow small tolerance


class TestFuelConsumptionTotalSensorAttributes:
    """Test FuelConsumptionTotalSensor class attributes."""

    def test_device_class(self):
        """Test sensor has correct device class for service targeting."""
        assert DEVICE_CLASS_FUEL_METER == "econet300__fuel_meter"

    def test_sensor_class_attributes(self):
        """Test sensor class has expected attributes defined."""
        # Check that the class defines expected attributes
        # Note: These are defined as class attributes, not properties
        assert hasattr(FuelConsumptionTotalSensor, "_attr_state_class")
        assert hasattr(FuelConsumptionTotalSensor, "_attr_native_unit_of_measurement")
        assert hasattr(FuelConsumptionTotalSensor, "_attr_device_class")
        assert hasattr(FuelConsumptionTotalSensor, "_attr_translation_key")
        assert hasattr(FuelConsumptionTotalSensor, "_attr_icon")


class TestFuelConsumptionConstants:
    """Test fuel consumption related constants."""

    def test_max_time_delta_seconds(self):
        """Test MAX_TIME_DELTA_SECONDS is reasonable."""
        # Should be 5 minutes (300 seconds)
        assert MAX_TIME_DELTA_SECONDS == 300
        # Should be at least 1 minute
        assert MAX_TIME_DELTA_SECONDS >= 60
        # Should be at most 10 minutes
        assert MAX_TIME_DELTA_SECONDS <= 600


class TestFuelConsumptionTrackerCalculation:
    """Test the mathematical calculation of fuel consumption."""

    def test_calculation_formula(self):
        """Test the consumption calculation formula is correct."""
        tracker = FuelConsumptionTracker()

        # Set initial state
        initial_time = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
        tracker._last_update = initial_time

        # Calculate expected consumption for 60 seconds at 3.6 kg/h
        # 3.6 kg/h * (60/3600) h = 0.06 kg
        fuel_rate = 3.6  # kg/h
        time_delta = 60  # seconds
        expected = fuel_rate * (time_delta / 3600)

        # Mock the current time to be 60 seconds later
        with patch("custom_components.econet300.sensor.datetime") as mock_datetime:
            mock_datetime.now.return_value = datetime(
                2025, 1, 1, 12, 1, 0, tzinfo=timezone.utc
            )

            result = tracker.update(fuel_rate)

        assert result == pytest.approx(expected, rel=0.01)

    def test_accumulated_consumption_over_multiple_updates(self):
        """Test consumption accumulates correctly over multiple updates."""
        tracker = FuelConsumptionTracker()

        # Simulate 5 updates, each 60 seconds apart at 1.0 kg/h
        # Set initial timestamp
        tracker._last_update = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

        # Perform 5 updates
        for i in range(5):
            with patch("custom_components.econet300.sensor.datetime") as mock_datetime:
                mock_datetime.now.return_value = datetime(
                    2025, 1, 1, 12, i + 1, 0, tzinfo=timezone.utc
                )
                tracker.update(1.0)  # 1 kg/h
                # Update the last_update for next iteration
                tracker._last_update = datetime(
                    2025, 1, 1, 12, i + 1, 0, tzinfo=timezone.utc
                )

        # 5 updates * 60 seconds each at 1 kg/h = 5 * (60/3600) = 5/60 ≈ 0.083 kg
        expected_total = 5 * (1.0 * 60 / 3600)
        assert tracker.total == pytest.approx(expected_total, rel=0.01)
