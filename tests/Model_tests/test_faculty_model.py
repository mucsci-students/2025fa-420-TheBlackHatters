# File Name: test_faculty_model.py
# Author: Fletcher Burton
# Created: October 11, 2025
#
# Unit tests for Faculty_model.py using pytest.
# These tests validate core behaviors of the current Faculty implementation.

import pytest
from Models.Faculty_model import Faculty


def sample_faculty_entry():
    """Return a representative faculty dictionary for use in list-based operations."""
    return {
        "name": "Dr. Smith",
        "maximum_credits": 12,
        "minimum_credits": 6,
        "unique_course_limit": 3,
        "time_available": ["MWF 9-10", "TTh 1-3"],
        "course_preferences": ["CMSC 101", "CMSC 201"],
        "room_preferences": ["Roddy 136"],
        "lab_preferences": ["Linux"],
    }


def test_faculty_init_attributes():
    """Faculty object should store initialization arguments as attributes."""
    f = Faculty(
        "Dr. Jones",
        12,
        6,
        3,
        ["MWF 9-10", "TTh 1-3"],
        ["CMSC 101"],
        ["Roddy 136"],
        ["Linux"],
    )
    assert f.name == "Dr. Jones"
    assert f.maximum_credits == 12
    assert f.minimum_credits == 6
    assert f.unique_course_limit == 3
    assert f.times == ["MWF 9-10", "TTh 1-3"]
    assert f.course_preferences == ["CMSC 101"]
    assert f.room_preferences == ["Roddy 136"]
    assert f.lab_preferences == ["Linux"]


def test_facCheck_true_when_name_found(monkeypatch):
    """facCheck() should return True if the name matches any faculty entry in self."""
    # We'll fake 'self' as a list of dicts and bind facCheck to it
    fake_faculty = [sample_faculty_entry()]
    Faculty.facCheck.__qualname__  # ensure exists
    result = Faculty.facCheck(fake_faculty, "Dr. Smith")
    assert result is True


def test_facCheck_false_when_not_found():
    """facCheck() should return False when the name is not in any entry."""
    fake_faculty = [sample_faculty_entry()]
    result = Faculty.facCheck(fake_faculty, "Dr. Zoppetti")
    assert result is False


def test_addFaculty_appends_entry():
    """addFaculty() should append a new faculty entry to the list."""
    fake_faculty = []
    new_entry = sample_faculty_entry()
    Faculty.addFaculty(fake_faculty, new_entry)
    assert new_entry in fake_faculty


def test_removeFaculty_found_entry():
    """removeFaculty() should remove and return the matching faculty entry."""
    fake_faculty = [sample_faculty_entry()]
    removed = Faculty.removeFaculty(fake_faculty, "Dr. Smith")
    assert removed["name"] == "Dr. Smith"
    assert fake_faculty == []


def test_removeFaculty_not_found_returns_none():
    """removeFaculty() should return None and leave list unchanged if not found."""
    fake_faculty = [sample_faculty_entry()]
    removed = Faculty.removeFaculty(fake_faculty, "Dr. Nonexistent")
    assert removed is None
    assert len(fake_faculty) == 1


def test_viewFaculty_prints_all_entries(capfd):
    """viewFaculty() should print each faculty entry with a newline."""
    fake_faculty = [sample_faculty_entry(), {**sample_faculty_entry(), "name": "Dr. Jones"}]
    Faculty.viewFaculty(fake_faculty)
    out, _ = capfd.readouterr()
    assert "Dr. Smith" in out
    assert "Dr. Jones" in out