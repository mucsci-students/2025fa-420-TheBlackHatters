# File Name: test_timeslots_model.py
# Author: Nicholas DiPace
# Created: November 23, 2025
#
# Unit tests for Rooms_model.py using pytest.

import pytest
from Models.Timeslots_model import validate_time, TimeSlotModel


# Validate Time Tests:
def test_validate_time_valid():
    """Valid HH:MM formats should return True."""
    assert validate_time("00:00") is True
    assert validate_time("23:59") is True
    assert validate_time("09:30") is True


def test_validate_time_invalid_format():
    """Invalid formats should return False."""
    assert validate_time("9:00") is False
    assert validate_time("123:00") is False
    assert validate_time("aa:bb") is False
    assert validate_time("12-00") is False


def test_validate_time_invalid_values():
    """Invalid numeric ranges should return False."""
    assert validate_time("24:00") is False
    assert validate_time("12:60") is False
    assert validate_time("99:99") is False


# Test TimeSlotModel methods:
def test_list_slots():
    """list_slots should return saved slots or empty list."""
    model = TimeSlotModel(
        {"times": {"MON": [{"start": "08:00", "spacing": 60, "end": "12:00"}]}}
    )
    assert len(model.list_slots("MON")) == 1
    assert model.list_slots("TUE") == []


def test_add_slot_success():
    """A valid slot should be added to the model."""
    model = TimeSlotModel({"times": {}})
    model.add_slot("TUE", "09:00", 30, "10:00")
    slots = model.list_slots("TUE")
    assert len(slots) == 1
    assert slots[0]["start"] == "09:00"
    assert slots[0]["spacing"] == 30
    assert slots[0]["end"] == "10:00"


def test_add_slot_invalid_times():
    """Invalid time formats should raise ValueError."""
    model = TimeSlotModel({"times": {}})
    with pytest.raises(ValueError):
        model.add_slot("WED", "99:00", 30, "10:00")
    with pytest.raises(ValueError):
        model.add_slot("WED", "09:00", 30, "25:00")


def test_edit_slot_success():
    """Editing a slot should update its values."""
    model = TimeSlotModel(
        {"times": {"MON": [{"start": "08:00", "spacing": 60, "end": "12:00"}]}}
    )
    model.edit_slot("MON", 0, start="09:00", end="11:00", spacing=45)
    slot = model.list_slots("MON")[0]
    assert slot["start"] == "09:00"
    assert slot["end"] == "11:00"
    assert slot["spacing"] == 45


def test_edit_slot_invalid_index():
    """Invalid index or day should raise IndexError."""
    model = TimeSlotModel(
        {"times": {"MON": [{"start": "08:00", "spacing": 60, "end": "12:00"}]}}
    )
    with pytest.raises(IndexError):
        model.edit_slot("MON", 5, start="10:00")
    with pytest.raises(IndexError):
        model.edit_slot("FRI", 0, start="10:00")


def test_edit_slot_invalid_time():
    """Invalid times during edit should raise ValueError."""
    model = TimeSlotModel(
        {"times": {"MON": [{"start": "08:00", "spacing": 60, "end": "12:00"}]}}
    )
    with pytest.raises(ValueError):
        model.edit_slot("MON", 0, start="99:00")
    with pytest.raises(ValueError):
        model.edit_slot("MON", 0, end="99:00")


def test_delete_slot_success():
    """A valid delete should remove the slot and return it."""
    model = TimeSlotModel(
        {"times": {"MON": [{"start": "08:00", "spacing": 60, "end": "12:00"}]}}
    )
    deleted = model.delete_slot("MON", 0)
    assert deleted["start"] == "08:00"
    assert model.list_slots("MON") == []


def test_delete_slot_invalid_index():
    """Deleting with invalid index/day should raise IndexError."""
    model = TimeSlotModel(
        {"times": {"MON": [{"start": "08:00", "spacing": 60, "end": "12:00"}]}}
    )
    with pytest.raises(IndexError):
        model.delete_slot("MON", 5)
    with pytest.raises(IndexError):
        model.delete_slot("FRI", 0)
