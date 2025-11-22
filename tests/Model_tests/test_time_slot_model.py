# test_time_slot_model.py
import pytest
from Models.time_slot_model import (
    parse_time_to_minutes,
    minutes_to_time_str,
    TimeInterval,
    TimeSlotConfig,
)


# ============================================================
# parse_time_to_minutes() tests
# ============================================================

class TestParseTimeToMinutes:
    # Valid inputs
    def test_midnight(self):
        assert parse_time_to_minutes("00:00") == 0

    def test_one_minute_before_midnight(self):
        assert parse_time_to_minutes("23:59") == 23 * 60 + 59

    def test_noon(self):
        assert parse_time_to_minutes("12:00") == 720

    def test_early_morning(self):
        assert parse_time_to_minutes("06:30") == 390

    def test_late_evening(self):
        assert parse_time_to_minutes("21:45") == 21 * 60 + 45

    # Invalid format edge cases
    def test_invalid_no_colon(self):
        with pytest.raises(ValueError, match="Invalid time format"):
            parse_time_to_minutes("1200")

    def test_invalid_single_digit_hour(self):
        with pytest.raises(ValueError, match="Invalid time format"):
            parse_time_to_minutes("9:00")

    def test_invalid_single_digit_minute(self):
        with pytest.raises(ValueError, match="Invalid time format"):
            parse_time_to_minutes("09:0")

    def test_invalid_hour_24(self):
        with pytest.raises(ValueError, match="Invalid time format"):
            parse_time_to_minutes("24:00")

    def test_invalid_hour_25(self):
        with pytest.raises(ValueError, match="Invalid time format"):
            parse_time_to_minutes("25:00")

    def test_invalid_minute_60(self):
        with pytest.raises(ValueError, match="Invalid time format"):
            parse_time_to_minutes("12:60")

    def test_invalid_negative_hour(self):
        with pytest.raises(ValueError, match="Invalid time format"):
            parse_time_to_minutes("-1:00")

    def test_invalid_empty_string(self):
        with pytest.raises(ValueError, match="Invalid time format"):
            parse_time_to_minutes("")

    def test_invalid_none(self):
        with pytest.raises(ValueError, match="Invalid time format"):
            parse_time_to_minutes(None)

    def test_invalid_integer_input(self):
        with pytest.raises(ValueError, match="Invalid time format"):
            parse_time_to_minutes(1200)

    def test_invalid_with_spaces(self):
        with pytest.raises(ValueError, match="Invalid time format"):
            parse_time_to_minutes(" 12:00")

    def test_invalid_with_trailing_spaces(self):
        with pytest.raises(ValueError, match="Invalid time format"):
            parse_time_to_minutes("12:00 ")

    def test_invalid_am_pm_format(self):
        with pytest.raises(ValueError, match="Invalid time format"):
            parse_time_to_minutes("12:00 PM")

    def test_invalid_three_digit_hour(self):
        with pytest.raises(ValueError, match="Invalid time format"):
            parse_time_to_minutes("012:00")

    def test_invalid_letters(self):
        with pytest.raises(ValueError, match="Invalid time format"):
            parse_time_to_minutes("ab:cd")

    def test_invalid_special_characters(self):
        with pytest.raises(ValueError, match="Invalid time format"):
            parse_time_to_minutes("12:00:00")


# ============================================================
# minutes_to_time_str() tests
# ============================================================

class TestMinutesToTimeStr:
    # Valid inputs
    def test_zero_minutes(self):
        assert minutes_to_time_str(0) == "00:00"

    def test_max_valid_minutes(self):
        assert minutes_to_time_str(1439) == "23:59"

    def test_noon(self):
        assert minutes_to_time_str(720) == "12:00"

    def test_single_digit_hour(self):
        assert minutes_to_time_str(90) == "01:30"

    def test_single_digit_minute(self):
        assert minutes_to_time_str(605) == "10:05"

    # Invalid inputs
    def test_negative_minutes(self):
        with pytest.raises(ValueError, match="minutes out of range"):
            minutes_to_time_str(-1)

    def test_large_negative_minutes(self):
        with pytest.raises(ValueError, match="minutes out of range"):
            minutes_to_time_str(-1000)

    def test_minutes_equals_1440(self):
        with pytest.raises(ValueError, match="minutes out of range"):
            minutes_to_time_str(1440)

    def test_minutes_exceeds_day(self):
        with pytest.raises(ValueError, match="minutes out of range"):
            minutes_to_time_str(2000)

    # Round-trip tests
    def test_roundtrip_midnight(self):
        assert minutes_to_time_str(parse_time_to_minutes("00:00")) == "00:00"

    def test_roundtrip_end_of_day(self):
        assert minutes_to_time_str(parse_time_to_minutes("23:59")) == "23:59"

    def test_roundtrip_arbitrary(self):
        assert minutes_to_time_str(parse_time_to_minutes("14:37")) == "14:37"


# ============================================================
# TimeInterval tests
# ============================================================

class TestTimeIntervalValidation:
    def test_valid_interval(self):
        iv = TimeInterval(start="08:00", end="17:00", spacing=60)
        iv.validate()  # Should not raise

    def test_end_before_start(self):
        iv = TimeInterval(start="17:00", end="08:00", spacing=60)
        with pytest.raises(ValueError, match="end must be after start"):
            iv.validate()

    def test_end_equals_start(self):
        iv = TimeInterval(start="12:00", end="12:00", spacing=30)
        with pytest.raises(ValueError, match="end must be after start"):
            iv.validate()

    def test_zero_spacing(self):
        iv = TimeInterval(start="08:00", end="17:00", spacing=0)
        with pytest.raises(ValueError, match="spacing must be a positive"):
            iv.validate()

    def test_negative_spacing(self):
        iv = TimeInterval(start="08:00", end="17:00", spacing=-30)
        with pytest.raises(ValueError, match="spacing must be a positive"):
            iv.validate()

    def test_invalid_start_format(self):
        iv = TimeInterval(start="8:00", end="17:00", spacing=60)
        with pytest.raises(ValueError, match="Invalid time format"):
            iv.validate()

    def test_invalid_end_format(self):
        iv = TimeInterval(start="08:00", end="5:00 PM", spacing=60)
        with pytest.raises(ValueError, match="Invalid time format"):
            iv.validate()


class TestTimeIntervalGenerateSlots:
    def test_hourly_slots(self):
        iv = TimeInterval(start="08:00", end="12:00", spacing=60)
        assert iv.generate_slots() == ["08:00", "09:00", "10:00", "11:00"]

    def test_30_minute_slots(self):
        iv = TimeInterval(start="09:00", end="11:00", spacing=30)
        assert iv.generate_slots() == ["09:00", "09:30", "10:00", "10:30"]

    def test_15_minute_slots(self):
        iv = TimeInterval(start="14:00", end="15:00", spacing=15)
        assert iv.generate_slots() == ["14:00", "14:15", "14:30", "14:45"]

    def test_slot_at_exact_end_excluded(self):
        iv = TimeInterval(start="10:00", end="11:00", spacing=30)
        slots = iv.generate_slots()
        assert "11:00" not in slots
        assert slots == ["10:00", "10:30"]

    def test_single_slot_when_spacing_exceeds_duration(self):
        iv = TimeInterval(start="10:00", end="10:30", spacing=60)
        assert iv.generate_slots() == ["10:00"]

    def test_one_minute_spacing(self):
        iv = TimeInterval(start="23:55", end="23:59", spacing=1)
        assert iv.generate_slots() == ["23:55", "23:56", "23:57", "23:58"]

    def test_spacing_larger_than_interval(self):
        iv = TimeInterval(start="08:00", end="08:15", spacing=60)
        assert iv.generate_slots() == ["08:00"]

    def test_exact_fit_slots(self):
        iv = TimeInterval(start="08:00", end="10:00", spacing=30)
        slots = iv.generate_slots()
        assert len(slots) == 4
        assert slots[-1] == "09:30"

    def test_midnight_crossing_not_supported(self):
        # end before start should fail validation
        iv = TimeInterval(start="23:00", end="01:00", spacing=30)
        with pytest.raises(ValueError):
            iv.generate_slots()

    def test_very_small_interval(self):
        iv = TimeInterval(start="12:00", end="12:01", spacing=1)
        assert iv.generate_slots() == ["12:00"]

    def test_large_spacing_value(self):
        iv = TimeInterval(start="00:00", end="23:59", spacing=480)  # 8 hours
        assert iv.generate_slots() == ["00:00", "08:00", "16:00"]


class TestTimeIntervalToDict:
    def test_basic_to_dict(self):
        iv = TimeInterval(start="08:00", end="17:00", spacing=60)
        d = iv.to_dict()
        assert d == {"start": "08:00", "end": "17:00", "spacing": 60}

    def test_with_professors(self):
        iv = TimeInterval(start="08:00", end="12:00", spacing=60, 
                         professors=["Dr. Smith", "Dr. Jones"])
        d = iv.to_dict()
        assert d["professors"] == ["Dr. Smith", "Dr. Jones"]

    def test_with_labs(self):
        iv = TimeInterval(start="08:00", end="12:00", spacing=60,
                         labs=["Lab A", "Lab B"])
        d = iv.to_dict()
        assert d["labs"] == ["Lab A", "Lab B"]

    def test_with_courses(self):
        iv = TimeInterval(start="08:00", end="12:00", spacing=60,
                         courses=["CS101", "CS102"])
        d = iv.to_dict()
        assert d["courses"] == ["CS101", "CS102"]

    def test_empty_lists_not_included(self):
        iv = TimeInterval(start="08:00", end="12:00", spacing=60,
                         professors=[], labs=[], courses=[])
        d = iv.to_dict()
        assert "professors" not in d
        assert "labs" not in d
        assert "courses" not in d

    def test_all_fields(self):
        iv = TimeInterval(
            start="09:00", end="17:00", spacing=30,
            professors=["Prof A"], labs=["Lab 1"], courses=["Course X"]
        )
        d = iv.to_dict()
        assert d == {
            "start": "09:00", "end": "17:00", "spacing": 30,
            "professors": ["Prof A"], "labs": ["Lab 1"], "courses": ["Course X"]
        }


class TestTimeIntervalFromDict:
    def test_basic_from_dict(self):
        d = {"start": "08:00", "end": "17:00", "spacing": 60}
        iv = TimeInterval.from_dict(d)
        assert iv.start == "08:00"
        assert iv.end == "17:00"
        assert iv.spacing == 60

    def test_with_optional_fields(self):
        d = {
            "start": "08:00", "end": "12:00", "spacing": 30,
            "professors": ["Dr. A"], "labs": ["Lab 1"], "courses": ["CS101"]
        }
        iv = TimeInterval.from_dict(d)
        assert iv.professors == ["Dr. A"]
        assert iv.labs == ["Lab 1"]
        assert iv.courses == ["CS101"]

    def test_missing_optional_fields(self):
        d = {"start": "08:00", "end": "12:00", "spacing": 30}
        iv = TimeInterval.from_dict(d)
        assert iv.professors == []
        assert iv.labs == []
        assert iv.courses == []

    def test_strips_whitespace_from_professors(self):
        d = {"start": "08:00", "end": "12:00", "spacing": 30,
             "professors": ["  Dr. Smith  ", "Dr. Jones  "]}
        iv = TimeInterval.from_dict(d)
        assert iv.professors == ["Dr. Smith", "Dr. Jones"]

    def test_filters_empty_strings(self):
        d = {"start": "08:00", "end": "12:00", "spacing": 30,
             "professors": ["Dr. A", "", "  ", "Dr. B"]}
        iv = TimeInterval.from_dict(d)
        assert iv.professors == ["Dr. A", "Dr. B"]

    def test_spacing_converted_to_int(self):
        d = {"start": "08:00", "end": "12:00", "spacing": "30"}
        iv = TimeInterval.from_dict(d)
        assert iv.spacing == 30
        assert isinstance(iv.spacing, int)

    def test_roundtrip(self):
        original = TimeInterval(
            start="09:00", end="18:00", spacing=45,
            professors=["Prof X"], labs=["Lab Y"], courses=["Course Z"]
        )
        restored = TimeInterval.from_dict(original.to_dict())
        assert restored.start == original.start
        assert restored.end == original.end
        assert restored.spacing == original.spacing
        assert restored.professors == original.professors
        assert restored.labs == original.labs
        assert restored.courses == original.courses


# ============================================================
# TimeSlotConfig tests
# ============================================================

class TestTimeSlotConfigBasic:
    def test_empty_config(self):
        cfg = TimeSlotConfig()
        assert cfg.times == {}

    def test_from_empty_dict(self):
        cfg = TimeSlotConfig.from_dict({})
        assert cfg.times == {}

    def test_from_dict_with_times(self):
        d = {
            "times": {
                "MON": [{"start": "08:00", "end": "12:00", "spacing": 60}],
                "TUE": [{"start": "09:00", "end": "11:00", "spacing": 30}]
            }
        }
        cfg = TimeSlotConfig.from_dict(d)
        assert "MON" in cfg.times
        assert "TUE" in cfg.times
        assert len(cfg.times["MON"]) == 1
        assert cfg.times["MON"][0].start == "08:00"

    def test_to_dict(self):
        cfg = TimeSlotConfig()
        cfg.add_interval("MON", {"start": "08:00", "end": "12:00", "spacing": 60})
        d = cfg.to_dict()
        assert "times" in d
        assert "MON" in d["times"]

    def test_roundtrip(self):
        original = TimeSlotConfig()
        original.add_interval("MON", {
            "start": "08:00", "end": "17:00", "spacing": 60,
            "professors": ["Dr. A"], "labs": ["Lab 1"]
        })
        original.add_interval("WED", {"start": "10:00", "end": "14:00", "spacing": 30})
        
        restored = TimeSlotConfig.from_dict(original.to_dict())
        assert len(restored.times) == 2
        assert restored.times["MON"][0].professors == ["Dr. A"]


class TestTimeSlotConfigAddInterval:
    def test_add_to_empty_day(self):
        cfg = TimeSlotConfig()
        cfg.add_interval("MON", {"start": "08:00", "end": "12:00", "spacing": 60})
        assert len(cfg.times["MON"]) == 1

    def test_add_multiple_to_same_day(self):
        cfg = TimeSlotConfig()
        cfg.add_interval("MON", {"start": "08:00", "end": "12:00", "spacing": 60})
        cfg.add_interval("MON", {"start": "13:00", "end": "17:00", "spacing": 60})
        assert len(cfg.times["MON"]) == 2

    def test_add_to_different_days(self):
        cfg = TimeSlotConfig()
        cfg.add_interval("MON", {"start": "08:00", "end": "12:00", "spacing": 60})
        cfg.add_interval("TUE", {"start": "09:00", "end": "11:00", "spacing": 30})
        assert "MON" in cfg.times
        assert "TUE" in cfg.times

    def test_add_invalid_interval_raises(self):
        cfg = TimeSlotConfig()
        with pytest.raises(ValueError):
            cfg.add_interval("MON", {"start": "12:00", "end": "08:00", "spacing": 60})

    def test_add_with_zero_spacing_raises(self):
        cfg = TimeSlotConfig()
        with pytest.raises(ValueError):
            cfg.add_interval("MON", {"start": "08:00", "end": "12:00", "spacing": 0})

    def test_add_overlapping_intervals_allowed(self):
        # Model doesn't prevent overlapping intervals
        cfg = TimeSlotConfig()
        cfg.add_interval("MON", {"start": "08:00", "end": "12:00", "spacing": 60})
        cfg.add_interval("MON", {"start": "10:00", "end": "14:00", "spacing": 60})
        assert len(cfg.times["MON"]) == 2


class TestTimeSlotConfigRemoveInterval:
    def test_remove_only_interval(self):
        cfg = TimeSlotConfig()
        cfg.add_interval("MON", {"start": "08:00", "end": "12:00", "spacing": 60})
        cfg.remove_interval("MON", 0)
        assert "MON" not in cfg.times

    def test_remove_first_of_multiple(self):
        cfg = TimeSlotConfig()
        cfg.add_interval("MON", {"start": "08:00", "end": "12:00", "spacing": 60})
        cfg.add_interval("MON", {"start": "13:00", "end": "17:00", "spacing": 60})
        cfg.remove_interval("MON", 0)
        assert len(cfg.times["MON"]) == 1
        assert cfg.times["MON"][0].start == "13:00"

    def test_remove_last_of_multiple(self):
        cfg = TimeSlotConfig()
        cfg.add_interval("MON", {"start": "08:00", "end": "12:00", "spacing": 60})
        cfg.add_interval("MON", {"start": "13:00", "end": "17:00", "spacing": 60})
        cfg.remove_interval("MON", 1)
        assert len(cfg.times["MON"]) == 1
        assert cfg.times["MON"][0].start == "08:00"

    def test_remove_from_nonexistent_day(self):
        cfg = TimeSlotConfig()
        with pytest.raises(KeyError, match="No intervals for day"):
            cfg.remove_interval("MON", 0)

    def test_remove_invalid_index(self):
        cfg = TimeSlotConfig()
        cfg.add_interval("MON", {"start": "08:00", "end": "12:00", "spacing": 60})
        with pytest.raises(IndexError):
            cfg.remove_interval("MON", 5)

    def test_remove_negative_index(self):
        cfg = TimeSlotConfig()
        cfg.add_interval("MON", {"start": "08:00", "end": "12:00", "spacing": 60})
        cfg.add_interval("MON", {"start": "13:00", "end": "17:00", "spacing": 60})
        # Python allows negative indexing
        cfg.remove_interval("MON", -1)
        assert len(cfg.times["MON"]) == 1
        assert cfg.times["MON"][0].start == "08:00"

    def test_day_removed_when_empty(self):
        cfg = TimeSlotConfig()
        cfg.add_interval("MON", {"start": "08:00", "end": "12:00", "spacing": 60})
        cfg.remove_interval("MON", 0)
        assert "MON" not in cfg.times


class TestTimeSlotConfigEditInterval:
    def test_edit_basic(self):
        cfg = TimeSlotConfig()
        cfg.add_interval("MON", {"start": "08:00", "end": "12:00", "spacing": 60})
        cfg.edit_interval("MON", 0, {"start": "09:00", "end": "13:00", "spacing": 30})
        assert cfg.times["MON"][0].start == "09:00"
        assert cfg.times["MON"][0].end == "13:00"
        assert cfg.times["MON"][0].spacing == 30

    def test_edit_preserves_other_intervals(self):
        cfg = TimeSlotConfig()
        cfg.add_interval("MON", {"start": "08:00", "end": "12:00", "spacing": 60})
        cfg.add_interval("MON", {"start": "13:00", "end": "17:00", "spacing": 60})
        cfg.edit_interval("MON", 0, {"start": "07:00", "end": "11:00", "spacing": 30})
        assert cfg.times["MON"][0].start == "07:00"
        assert cfg.times["MON"][1].start == "13:00"

    def test_edit_nonexistent_day(self):
        cfg = TimeSlotConfig()
        with pytest.raises(KeyError, match="No intervals for day"):
            cfg.edit_interval("MON", 0, {"start": "08:00", "end": "12:00", "spacing": 60})

    def test_edit_invalid_index(self):
        cfg = TimeSlotConfig()
        cfg.add_interval("MON", {"start": "08:00", "end": "12:00", "spacing": 60})
        with pytest.raises(IndexError):
            cfg.edit_interval("MON", 5, {"start": "09:00", "end": "13:00", "spacing": 30})

    def test_edit_with_invalid_interval_raises(self):
        cfg = TimeSlotConfig()
        cfg.add_interval("MON", {"start": "08:00", "end": "12:00", "spacing": 60})
        with pytest.raises(ValueError):
            cfg.edit_interval("MON", 0, {"start": "12:00", "end": "08:00", "spacing": 60})

    def test_edit_negative_index(self):
        cfg = TimeSlotConfig()
        cfg.add_interval("MON", {"start": "08:00", "end": "12:00", "spacing": 60})
        cfg.add_interval("MON", {"start": "13:00", "end": "17:00", "spacing": 60})
        cfg.edit_interval("MON", -1, {"start": "14:00", "end": "18:00", "spacing": 45})
        assert cfg.times["MON"][-1].start == "14:00"


class TestTimeSlotConfigGetIntervals:
    def test_get_existing_day(self):
        cfg = TimeSlotConfig()
        cfg.add_interval("MON", {"start": "08:00", "end": "12:00", "spacing": 60})
        intervals = cfg.get_intervals("MON")
        assert len(intervals) == 1
        assert intervals[0].start == "08:00"

    def test_get_nonexistent_day(self):
        cfg = TimeSlotConfig()
        intervals = cfg.get_intervals("MON")
        assert intervals == []

    def test_get_returns_copy(self):
        cfg = TimeSlotConfig()
        cfg.add_interval("MON", {"start": "08:00", "end": "12:00", "spacing": 60})
        intervals = cfg.get_intervals("MON")
        intervals.append(TimeInterval(start="13:00", end="17:00", spacing=60))
        # Original should be unchanged
        assert len(cfg.times["MON"]) == 1


class TestTimeSlotConfigGenerateSlots:
    def test_generate_for_single_interval(self):
        cfg = TimeSlotConfig()
        cfg.add_interval("MON", {"start": "08:00", "end": "10:00", "spacing": 60})
        slots = cfg.generate_slots_for_day("MON")
        assert slots == ["08:00", "09:00"]

    def test_generate_for_multiple_intervals(self):
        cfg = TimeSlotConfig()
        cfg.add_interval("MON", {"start": "08:00", "end": "10:00", "spacing": 60})
        cfg.add_interval("MON", {"start": "14:00", "end": "16:00", "spacing": 60})
        slots = cfg.generate_slots_for_day("MON")
        assert slots == ["08:00", "09:00", "14:00", "15:00"]

    def test_generate_for_nonexistent_day(self):
        cfg = TimeSlotConfig()
        slots = cfg.generate_slots_for_day("MON")
        assert slots == []

    def test_generate_all_slots_empty(self):
        cfg = TimeSlotConfig()
        all_slots = cfg.generate_all_slots()
        assert all_slots == {}

    def test_generate_all_slots_multiple_days(self):
        cfg = TimeSlotConfig()
        cfg.add_interval("MON", {"start": "08:00", "end": "10:00", "spacing": 60})
        cfg.add_interval("WED", {"start": "14:00", "end": "16:00", "spacing": 30})
        all_slots = cfg.generate_all_slots()
        assert "MON" in all_slots
        assert "WED" in all_slots
        assert all_slots["MON"] == ["08:00", "09:00"]
        assert all_slots["WED"] == ["14:00", "14:30", "15:00", "15:30"]

    def test_generate_preserves_interval_order(self):
        cfg = TimeSlotConfig()
        # Add afternoon first, then morning
        cfg.add_interval("MON", {"start": "14:00", "end": "16:00", "spacing": 60})
        cfg.add_interval("MON", {"start": "08:00", "end": "10:00", "spacing": 60})
        slots = cfg.generate_slots_for_day("MON")
        # Should be in order of addition, not chronological
        assert slots == ["14:00", "15:00", "08:00", "09:00"]


# ============================================================
# Edge cases for day names
# ============================================================

class TestDayNameEdgeCases:
    def test_lowercase_day(self):
        cfg = TimeSlotConfig()
        cfg.add_interval("mon", {"start": "08:00", "end": "12:00", "spacing": 60})
        assert "mon" in cfg.times
        # Note: "MON" and "mon" are treated as different days

    def test_mixed_case_day(self):
        cfg = TimeSlotConfig()
        cfg.add_interval("Mon", {"start": "08:00", "end": "12:00", "spacing": 60})
        assert "Mon" in cfg.times

    def test_numeric_day(self):
        cfg = TimeSlotConfig()
        cfg.add_interval("1", {"start": "08:00", "end": "12:00", "spacing": 60})
        assert "1" in cfg.times

    def test_empty_string_day(self):
        cfg = TimeSlotConfig()
        cfg.add_interval("", {"start": "08:00", "end": "12:00", "spacing": 60})
        assert "" in cfg.times

    def test_special_characters_in_day(self):
        cfg = TimeSlotConfig()
        cfg.add_interval("MON-AM", {"start": "08:00", "end": "12:00", "spacing": 60})
        assert "MON-AM" in cfg.times


# ============================================================
# Stress / boundary tests
# ============================================================

class TestBoundaryConditions:
    def test_full_day_hourly(self):
        cfg = TimeSlotConfig()
        cfg.add_interval("MON", {"start": "00:00", "end": "23:59", "spacing": 60})
        slots = cfg.generate_slots_for_day("MON")
        assert len(slots) == 24
        assert slots[0] == "00:00"
        assert slots[-1] == "23:00"

    def test_full_day_minute_by_minute(self):
        cfg = TimeSlotConfig()
        cfg.add_interval("MON", {"start": "00:00", "end": "23:59", "spacing": 1})
        slots = cfg.generate_slots_for_day("MON")
        assert len(slots) == 1439

    def test_many_intervals_same_day(self):
        cfg = TimeSlotConfig()
        for hour in range(0, 24, 2):
            start = f"{hour:02d}:00"
            end = f"{hour+1:02d}:00"
            cfg.add_interval("MON", {"start": start, "end": end, "spacing": 15})
        assert len(cfg.times["MON"]) == 12

    def test_many_days(self):
        cfg = TimeSlotConfig()
        days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
        for day in days:
            cfg.add_interval(day, {"start": "09:00", "end": "17:00", "spacing": 60})
        assert len(cfg.times) == 7
        all_slots = cfg.generate_all_slots()
        for day in days:
            assert len(all_slots[day]) == 8


# ============================================================
# Type coercion and edge cases in from_dict
# ============================================================

class TestFromDictTypeCoercion:
    def test_spacing_as_float(self):
        d = {"start": "08:00", "end": "12:00", "spacing": 30.5}
        iv = TimeInterval.from_dict(d)
        assert iv.spacing == 30
        assert isinstance(iv.spacing, int)

    def test_professors_with_non_string_values(self):
        d = {"start": "08:00", "end": "12:00", "spacing": 30,
             "professors": [123, "Dr. A", None, 45.6]}
        iv = TimeInterval.from_dict(d)
        # All should be converted to strings, None becomes "None" then stripped
        assert "123" in iv.professors
        assert "Dr. A" in iv.professors

    def test_labs_with_integers(self):
        d = {"start": "08:00", "end": "12:00", "spacing": 30,
             "labs": [1, 2, 3]}
        iv = TimeInterval.from_dict(d)
        assert iv.labs == ["1", "2", "3"]

    def test_courses_mixed_types(self):
        d = {"start": "08:00", "end": "12:00", "spacing": 30,
             "courses": ["CS101", 102, "  ", "MATH201"]}
        iv = TimeInterval.from_dict(d)
        assert "CS101" in iv.courses
        assert "102" in iv.courses
        assert "MATH201" in iv.courses
        assert "" not in iv.courses


# ============================================================
# Config serialization edge cases
# ============================================================

class TestConfigSerializationEdgeCases:
    def test_to_dict_empty_times(self):
        cfg = TimeSlotConfig(times={})
        d = cfg.to_dict()
        assert d == {"times": {}}

    def test_from_dict_ignores_extra_keys(self):
        d = {
            "times": {"MON": [{"start": "08:00", "end": "12:00", "spacing": 60}]},
            "extra_key": "should be ignored",
            "another": 123
        }
        cfg = TimeSlotConfig.from_dict(d)
        assert "MON" in cfg.times
        # No error raised for extra keys

    def test_from_dict_with_empty_day_list(self):
        d = {"times": {"MON": []}}
        cfg = TimeSlotConfig.from_dict(d)
        assert cfg.times["MON"] == []

    def test_complex_roundtrip(self):
        cfg = TimeSlotConfig()
        # Add various intervals across days
        cfg.add_interval("MON", {
            "start": "08:00", "end": "12:00", "spacing": 60,
            "professors": ["Dr. Smith", "Dr. Jones"],
            "labs": ["Lab A"],
            "courses": ["CS101", "CS102"]
        })
        cfg.add_interval("MON", {
            "start": "13:00", "end": "17:00", "spacing": 30
        })
        cfg.add_interval("TUE", {
            "start": "09:00", "end": "11:00", "spacing": 15,
            "courses": ["MATH201"]
        })
        
        # Roundtrip
        d = cfg.to_dict()
        restored = TimeSlotConfig.from_dict(d)
        
        # Verify
        assert len(restored.times["MON"]) == 2
        assert len(restored.times["TUE"]) == 1
        assert restored.times["MON"][0].professors == ["Dr. Smith", "Dr. Jones"]
        assert restored.times["MON"][1].spacing == 30
        assert restored.times["TUE"][0].courses == ["MATH201"]


# ============================================================
# Interval mutation tests
# ============================================================

class TestIntervalMutation:
    def test_direct_times_mutation(self):
        cfg = TimeSlotConfig()
        cfg.add_interval("MON", {"start": "08:00", "end": "12:00", "spacing": 60})
        # Directly mutate the internal structure
        cfg.times["MON"][0].start = "07:00"
        assert cfg.times["MON"][0].start == "07:00"

    def test_add_interval_after_direct_mutation(self):
        cfg = TimeSlotConfig()
        cfg.times["MON"] = []
        cfg.add_interval("MON", {"start": "08:00", "end": "12:00", "spacing": 60})
        assert len(cfg.times["MON"]) == 1


# ============================================================
# Unicode and special string handling
# ============================================================

class TestUnicodeHandling:
    def test_unicode_professor_names(self):
        d = {"start": "08:00", "end": "12:00", "spacing": 30,
             "professors": ["Dr. Müller", "Prof. 田中", "Señor García"]}
        iv = TimeInterval.from_dict(d)
        assert "Dr. Müller" in iv.professors
        assert "Prof. 田中" in iv.professors
        assert "Señor García" in iv.professors

    def test_unicode_in_day_name(self):
        cfg = TimeSlotConfig()
        cfg.add_interval("月曜日", {"start": "08:00", "end": "12:00", "spacing": 60})
        assert "月曜日" in cfg.times

    def test_emoji_in_lab_name(self):
        d = {"start": "08:00", "end": "12:00", "spacing": 30,
             "labs": ["Lab 🔬", "Room 💻"]}
        iv = TimeInterval.from_dict(d)
        assert "Lab 🔬" in iv.labs


# ============================================================
# Error message verification
# ============================================================

class TestErrorMessages:
    def test_invalid_time_format_message(self):
        with pytest.raises(ValueError) as exc_info:
            parse_time_to_minutes("bad")
        assert "Invalid time format" in str(exc_info.value)
        assert "'bad'" in str(exc_info.value)

    def test_interval_end_before_start_message(self):
        iv = TimeInterval(start="17:00", end="08:00", spacing=60)
        with pytest.raises(ValueError) as exc_info:
            iv.validate()
        assert "end must be after start" in str(exc_info.value)
        assert "17:00" in str(exc_info.value)
        assert "08:00" in str(exc_info.value)

    def test_spacing_error_message(self):
        iv = TimeInterval(start="08:00", end="12:00", spacing=-5)
        with pytest.raises(ValueError) as exc_info:
            iv.validate()
        assert "spacing must be a positive" in str(exc_info.value)

    def test_no_intervals_for_day_message(self):
        cfg = TimeSlotConfig()
        with pytest.raises(KeyError) as exc_info:
            cfg.remove_interval("NONEXISTENT", 0)
        assert "No intervals for day" in str(exc_info.value)


# ============================================================
# Concurrent-style operations (sequential but testing state)
# ============================================================

class TestSequentialOperations:
    def test_add_remove_add_same_day(self):
        cfg = TimeSlotConfig()
        cfg.add_interval("MON", {"start": "08:00", "end": "12:00", "spacing": 60})
        cfg.remove_interval("MON", 0)
        cfg.add_interval("MON", {"start": "09:00", "end": "13:00", "spacing": 30})
        assert len(cfg.times["MON"]) == 1
        assert cfg.times["MON"][0].start == "09:00"

    def test_multiple_edits_same_interval(self):
        cfg = TimeSlotConfig()
        cfg.add_interval("MON", {"start": "08:00", "end": "12:00", "spacing": 60})
        cfg.edit_interval("MON", 0, {"start": "09:00", "end": "13:00", "spacing": 30})
        cfg.edit_interval("MON", 0, {"start": "10:00", "end": "14:00", "spacing": 15})
        cfg.edit_interval("MON", 0, {"start": "11:00", "end": "15:00", "spacing": 45})
        assert cfg.times["MON"][0].start == "11:00"
        assert cfg.times["MON"][0].spacing == 45

    def test_interleaved_operations_multiple_days(self):
        cfg = TimeSlotConfig()
        cfg.add_interval("MON", {"start": "08:00", "end": "12:00", "spacing": 60})
        cfg.add_interval("TUE", {"start": "09:00", "end": "13:00", "spacing": 30})
        cfg.add_interval("MON", {"start": "13:00", "end": "17:00", "spacing": 60})
        cfg.remove_interval("TUE", 0)
        cfg.add_interval("WED", {"start": "10:00", "end": "14:00", "spacing": 15})
        cfg.edit_interval("MON", 1, {"start": "14:00", "end": "18:00", "spacing": 30})
        
        assert len(cfg.times["MON"]) == 2
        assert "TUE" not in cfg.times
        assert len(cfg.times["WED"]) == 1
        assert cfg.times["MON"][1].start == "14:00"


# ============================================================
# Dataclass behavior tests
# ============================================================

class TestDataclassBehavior:
    def test_interval_equality(self):
        iv1 = TimeInterval(start="08:00", end="12:00", spacing=60)
        iv2 = TimeInterval(start="08:00", end="12:00", spacing=60)
        assert iv1 == iv2

    def test_interval_inequality_start(self):
        iv1 = TimeInterval(start="08:00", end="12:00", spacing=60)
        iv2 = TimeInterval(start="09:00", end="12:00", spacing=60)
        assert iv1 != iv2

    def test_interval_inequality_lists(self):
        iv1 = TimeInterval(start="08:00", end="12:00", spacing=60, professors=["A"])
        iv2 = TimeInterval(start="08:00", end="12:00", spacing=60, professors=["B"])
        assert iv1 != iv2

    def test_interval_default_factory_isolation(self):
        iv1 = TimeInterval(start="08:00", end="12:00", spacing=60)
        iv2 = TimeInterval(start="08:00", end="12:00", spacing=60)
        iv1.professors.append("Dr. A")
        assert iv2.professors == []  # Should not be affected

    def test_config_default_factory_isolation(self):
        cfg1 = TimeSlotConfig()
        cfg2 = TimeSlotConfig()
        cfg1.add_interval("MON", {"start": "08:00", "end": "12:00", "spacing": 60})
        assert cfg2.times == {}  # Should not be affected