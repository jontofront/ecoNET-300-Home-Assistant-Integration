"""Tests for ecoMAX schedule bitmask decoder functions."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from custom_components.econet300.common_functions import (
    decode_ecomax_schedule_day,
    decode_ecomax_schedule_metadata,
    summarize_schedule_slots,
)


class TestDecodeEcomaxScheduleDay:
    """Test decode_ecomax_schedule_day bitmask decoding."""

    def test_all_on(self):
        """All bits set means every half-hour slot is active."""
        slots = decode_ecomax_schedule_day([255, 255, 255, 255, 255, 255])
        assert len(slots) == 48
        assert all(s["active"] for s in slots)
        assert slots[0] == {"start": "00:00", "end": "00:30", "active": True}
        assert slots[47] == {"start": "23:30", "end": "24:00", "active": True}

    def test_all_off(self):
        """All bits clear means no slot is active."""
        slots = decode_ecomax_schedule_day([0, 0, 0, 0, 0, 0])
        assert len(slots) == 48
        assert not any(s["active"] for s in slots)

    def test_single_byte_pattern(self):
        """Byte 192 = 0b11000000 -> first 2 slots active, next 6 off."""
        slots = decode_ecomax_schedule_day([192, 0, 0, 0, 0, 0])
        assert slots[0]["active"] is True
        assert slots[1]["active"] is True
        assert slots[2]["active"] is False
        assert slots[7]["active"] is False
        assert slots[8]["active"] is False

    def test_real_cwu_sunday_fixture(self):
        """Decode real cwuTZ Sunday data from ecoMAX810P-L fixture.

        [192, 15, 255, 0, 1, 255]
        byte 0: 192 = 11000000 -> 00:00-01:00 ON
        byte 1:  15 = 00001111 -> 06:00-08:00 ON
        byte 2: 255 = 11111111 -> 08:00-12:00 ON
        byte 3:   0 = 00000000 -> 12:00-16:00 OFF
        byte 4:   1 = 00000001 -> 19:30-20:00 ON
        byte 5: 255 = 11111111 -> 20:00-00:00 ON
        """
        slots = decode_ecomax_schedule_day([192, 15, 255, 0, 1, 255])
        assert len(slots) == 48

        # 00:00-01:00 ON (slots 0,1)
        assert slots[0]["active"] is True
        assert slots[1]["active"] is True
        assert slots[2]["active"] is False

        # 06:00-08:00 ON (slots 12-15, byte 1 low nibble)
        assert slots[11]["active"] is False
        assert slots[12]["active"] is True
        assert slots[13]["active"] is True
        assert slots[14]["active"] is True
        assert slots[15]["active"] is True

        # 08:00-12:00 ON (slots 16-23, byte 2 all ones)
        assert all(slots[i]["active"] for i in range(16, 24))

        # 12:00-16:00 OFF (slots 24-31, byte 3 all zeroes)
        assert not any(slots[i]["active"] for i in range(24, 32))

        # 19:30-20:00 ON (slot 39, byte 4 = 00000001)
        assert slots[38]["active"] is False
        assert slots[39]["active"] is True

        # 20:00-00:00 ON (slots 40-47, byte 5 all ones)
        assert all(slots[i]["active"] for i in range(40, 48))

    def test_slot_time_boundaries(self):
        """Verify start/end times cover 24 hours without gaps."""
        slots = decode_ecomax_schedule_day([0, 0, 0, 0, 0, 0])
        assert slots[0]["start"] == "00:00"
        assert slots[0]["end"] == "00:30"
        assert slots[1]["start"] == "00:30"
        assert slots[1]["end"] == "01:00"
        assert slots[46]["start"] == "23:00"
        assert slots[46]["end"] == "23:30"
        assert slots[47]["start"] == "23:30"
        assert slots[47]["end"] == "24:00"

    def test_real_boiler_work_fixture(self):
        """Decode real boilerWorkTZ Monday from ecoMAX810P-L fixture.

        [255, 252, 0, 0, 7, 255]
        byte 0: 255 = 11111111 -> 00:00-04:00 ON
        byte 1: 252 = 11111100 -> 04:00-07:00 ON, 07:00-08:00 OFF
        byte 2:   0 = 00000000 -> 08:00-12:00 OFF
        byte 3:   0 = 00000000 -> 12:00-16:00 OFF
        byte 4:   7 = 00000111 -> 18:30-20:00 ON
        byte 5: 255 = 11111111 -> 20:00-00:00 ON
        """
        slots = decode_ecomax_schedule_day([255, 252, 0, 0, 7, 255])

        # 00:00-04:00 ON
        assert all(slots[i]["active"] for i in range(8))

        # 04:00-07:00 ON (byte 1 high 6 bits)
        assert all(slots[i]["active"] for i in range(8, 14))

        # 07:00-08:00 OFF (byte 1 low 2 bits)
        assert slots[14]["active"] is False
        assert slots[15]["active"] is False

        # 08:00-16:00 OFF
        assert not any(slots[i]["active"] for i in range(16, 32))

        # 18:30-20:00 ON (byte 4 low 3 bits: slots 37,38,39)
        assert slots[36]["active"] is False
        assert slots[37]["active"] is True
        assert slots[38]["active"] is True
        assert slots[39]["active"] is True

        # 20:00-00:00 ON
        assert all(slots[i]["active"] for i in range(40, 48))


class TestDecodeEcomaxScheduleMetadata:
    """Test decode_ecomax_schedule_metadata extraction."""

    def test_cwu_metadata(self):
        """Decode cwuTZ metadata: [0, 10, 0, 20]."""
        meta = decode_ecomax_schedule_metadata([0, 10, 0, 20])
        assert meta == {
            "on_off_mode": 0,
            "decrease_value": 10,
            "min_decrease": 0,
            "max_decrease": 20,
        }

    def test_boiler_work_metadata(self):
        """Decode boilerWorkTZ metadata: [0, 0, 0, 20]."""
        meta = decode_ecomax_schedule_metadata([0, 0, 0, 20])
        assert meta == {
            "on_off_mode": 0,
            "decrease_value": 0,
            "min_decrease": 0,
            "max_decrease": 20,
        }

    def test_empty_metadata(self):
        """Empty or short metadata returns empty dict."""
        assert decode_ecomax_schedule_metadata([]) == {}  # noqa: PLC1901
        assert decode_ecomax_schedule_metadata([1, 2]) == {}  # noqa: PLC1901

    def test_none_metadata(self):
        """None metadata returns empty dict."""
        assert decode_ecomax_schedule_metadata(None) == {}  # noqa: PLC1901


class TestSummarizeScheduleSlots:
    """Test summarize_schedule_slots summary generation."""

    def test_all_on(self):
        """All active slots produce 'all_on'."""
        slots = decode_ecomax_schedule_day([255, 255, 255, 255, 255, 255])
        assert summarize_schedule_slots(slots) == "all_on"

    def test_all_off(self):
        """No active slots produce 'all_off'."""
        slots = decode_ecomax_schedule_day([0, 0, 0, 0, 0, 0])
        assert summarize_schedule_slots(slots) == "all_off"

    def test_empty_slots(self):
        """Empty slot list produces 'all_off'."""
        assert summarize_schedule_slots([]) == "all_off"

    def test_real_cwu_sunday_summary(self):
        """Real cwuTZ Sunday should produce merged active ranges."""
        slots = decode_ecomax_schedule_day([192, 15, 255, 0, 1, 255])
        summary = summarize_schedule_slots(slots)
        assert "00:00-01:00" in summary
        assert "06:00-12:00" in summary
        assert "19:30-00:00" in summary

    def test_real_boiler_work_summary(self):
        """Real boilerWorkTZ should produce merged active ranges."""
        slots = decode_ecomax_schedule_day([255, 252, 0, 0, 7, 255])
        summary = summarize_schedule_slots(slots)
        assert "00:00-07:00" in summary
        assert "18:30-00:00" in summary


class TestScheduleWithFixture:
    """Integration-style test using the real ecoMAX810P-L sysParams fixture."""

    @pytest.fixture
    def sys_params(self) -> dict:
        """Load the ecoMAX810P-L sysParams fixture."""
        fixture_path = (
            Path(__file__).parent / "fixtures" / "ecoMAX810P-L" / "sysParams.json"
        )
        with fixture_path.open() as f:
            return json.load(f)

    def test_fixture_has_ecomax_schedules(self, sys_params):
        """Fixture contains ecomaxSchedules with expected keys."""
        schedules = sys_params["schedules"]["ecomaxSchedules"]
        assert "cwuTZ" in schedules
        assert "boilerWorkTZ" in schedules
        assert "boilerTZ" in schedules
        assert "mixer1TZ" in schedules

    def test_fixture_schedule_structure(self, sys_params):
        """Each schedule has 8 entries: 7 days + 1 metadata."""
        for key, data in sys_params["schedules"]["ecomaxSchedules"].items():
            assert len(data) == 8, f"{key} should have 8 entries (7 days + metadata)"
            for day_idx in range(7):
                assert len(data[day_idx]) == 6, (
                    f"{key} day {day_idx} should have 6 bytes"
                )
            assert len(data[7]) == 4, f"{key} metadata should have 4 values"

    def test_decode_all_fixture_schedules(self, sys_params):
        """Decode every schedule in the fixture without errors."""
        for key, data in sys_params["schedules"]["ecomaxSchedules"].items():
            for day_idx in range(7):
                slots = decode_ecomax_schedule_day(data[day_idx])
                assert len(slots) == 48, f"{key} day {day_idx} should yield 48 slots"
                summary = summarize_schedule_slots(slots)
                assert isinstance(summary, str)

            meta = decode_ecomax_schedule_metadata(data[7])
            assert "on_off_mode" in meta
