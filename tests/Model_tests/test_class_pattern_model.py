# File Name: test_class_pattern_model.py
# Author: Fletcher Burton
# Created: November 2025
#
# Unit tests for ClassPattern model and helper functions.

import pytest
from Models.ClassPattern_model import (
    ClassPattern,
    add_class_pattern_to_config,
    modify_class_pattern_in_config,
    delete_class_pattern_from_config,
)


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------


def sample_time_slot_config():
    return {
        "times": {
            "MON": [{"start": "08:00", "end": "19:00", "spacing": 60}],
            "TUE": [{"start": "08:00", "end": "17:00", "spacing": 60}],
            "WED": [{"start": "08:00", "end": "19:00", "spacing": 60}],
            "THU": [{"start": "08:00", "end": "17:00", "spacing": 60}],
            "FRI": [{"start": "08:00", "end": "17:00", "spacing": 60}],
        },
        "classes": [
            {
                "credits": 3,
                "meetings": [
                    {"day": "MON", "duration": 50},
                    {"day": "WED", "duration": 50},
                    {"day": "FRI", "duration": 50},
                ],
            }
        ],
    }


# ------------------------------------------------------------
# Basic construction tests
# ------------------------------------------------------------


def test_minimal_pattern():
    p = ClassPattern(credits=3, meetings=[{"day": "MON", "duration": 50}])
    assert p.credits == 3
    assert len(p.meetings) == 1
    assert p.meetings[0]["day"] == "MON"
    assert p.meetings[0]["duration"] == 50
    assert p.start_time is None
    assert p.disabled is False


def test_full_pattern():
    meetings = [
        {"day": "TUE", "duration": 110, "lab": True},
        {"day": "THU", "duration": 110},
    ]
    p = ClassPattern(
        credits=4,
        meetings=meetings,
        start_time="16:00",
        disabled=True,
    )
    assert p.credits == 4
    assert p.meetings == meetings
    assert p.start_time == "16:00"
    assert p.disabled is True


# ------------------------------------------------------------
# Validation tests
# ------------------------------------------------------------


def test_invalid_credits():
    with pytest.raises(ValueError):
        ClassPattern(credits="abc", meetings=[])
    with pytest.raises(ValueError):
        ClassPattern(credits=-1, meetings=[])


def test_invalid_meetings_structure():
    # Missing duration
    with pytest.raises(ValueError):
        ClassPattern(credits=3, meetings=[{"day": "MON"}])
    # Invalid day
    with pytest.raises(ValueError):
        ClassPattern(credits=3, meetings=[{"day": "SAT", "duration": 50}])


def test_start_time_validation():
    p = ClassPattern(3, [{"day": "MON", "duration": 50}], start_time="09:00")
    assert p.start_time == "09:00"

    with pytest.raises(ValueError):
        ClassPattern(3, [{"day": "MON", "duration": 50}], start_time="bad")


def test_meeting_duration_rules():
    # Zero or negative durations rejected
    with pytest.raises(ValueError):
        ClassPattern(3, [{"day": "MON", "duration": 0}])

    with pytest.raises(ValueError):
        ClassPattern(3, [{"day": "MON", "duration": -1}])


# ------------------------------------------------------------
# Config-level helper tests
# ------------------------------------------------------------


def test_add_class_pattern_success():
    cfg = sample_time_slot_config()
    new_pattern = {
        "credits": 3,
        "meetings": [{"day": "TUE", "duration": 75}],
    }
    stored = add_class_pattern_to_config(cfg, new_pattern)
    assert stored["credits"] == 3
    assert stored in cfg["classes"]


def test_add_class_pattern_duplicate_reference():
    """Adding identical structure is allowed (no unique IDs)."""
    cfg = sample_time_slot_config()
    p = cfg["classes"][0]
    stored = add_class_pattern_to_config(cfg, p)
    assert stored in cfg["classes"]
    assert cfg["classes"].count(p) == 2  # duplicate allowed


def test_modify_class_pattern_success():
    cfg = sample_time_slot_config()
    updated = modify_class_pattern_in_config(
        cfg,
        index=0,
        updates={
            "credits": 4,
            "disabled": True,
            "meetings": [{"day": "MON", "duration": 110, "lab": True}],
        },
    )

    assert updated["credits"] == 4
    assert updated["disabled"] is True
    assert updated["meetings"][0]["duration"] == 110
    assert updated["meetings"][0]["lab"] is True


def test_modify_invalid_index():
    cfg = sample_time_slot_config()
    with pytest.raises(IndexError):
        modify_class_pattern_in_config(cfg, index=999, updates={"credits": 4})


def test_modify_keeps_existing_if_none():
    cfg = sample_time_slot_config()
    existing = cfg["classes"][0]

    updated = modify_class_pattern_in_config(
        cfg, index=0, updates={"credits": None, "start_time": None}
    )

    assert updated["credits"] == existing["credits"]
    assert updated.get("start_time") is None


def test_delete_class_pattern():
    cfg = sample_time_slot_config()
    removed = delete_class_pattern_from_config(cfg, index=0)
    assert removed["credits"] == 3
    assert len(cfg["classes"]) == 0

    with pytest.raises(IndexError):
        delete_class_pattern_from_config(cfg, index=0)


# ------------------------------------------------------------
# Edge case tests
# ------------------------------------------------------------


def test_class_pattern_type_safety():
    # meetings types converted to expected forms
    p = ClassPattern(
        credits="3",
        meetings=[
            {"day": "MON", "duration": "50"},
            {"day": "WED", "duration": 50.0},
        ],
    )
    assert p.credits == 3
    assert p.meetings[0]["duration"] == 50
    assert p.meetings[1]["duration"] == 50


def test_meetings_with_extra_fields_ignored():
    """If your model ignores unknown fields, confirm here."""
    p = ClassPattern(
        credits=3,
        meetings=[{"day": "MON", "duration": 50, "something_else": "ignored"}],
    )
    assert "something_else" not in p.meetings[0]


def test_disable_flag_default_behavior():
    p = ClassPattern(3, [{"day": "MON", "duration": 50}])
    assert p.disabled is False
    p = ClassPattern(3, [{"day": "MON", "duration": 50}], disabled=True)
    assert p.disabled is True


def test_start_time_optional_behavior():
    p = ClassPattern(3, [{"day": "MON", "duration": 50}], start_time="08:00")
    assert p.start_time == "08:00"

    # Valid HH:MM formats only
    with pytest.raises(ValueError):
        ClassPattern(3, [{"day": "MON", "duration": 50}], start_time="8am")
