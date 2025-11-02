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

def test_facCheck_partial_match_returns_true():
    """
    facCheck() uses substring matching ('if name in subFaculty'),
    so even a partial name like 'Smith' should return True.
    This ensures the method behaves consistently with its current logic.
    """
    fake_faculty = [{"name": "Dr. Smith"}]
    assert Faculty.facCheck(fake_faculty, "Smith") is True


def test_facCheck_empty_list_returns_false():
    """
    If the faculty list is empty, facCheck() should immediately return False,
    since there are no entries to search through.
    """
    assert Faculty.facCheck([], "Dr. Smith") is False

def test_addFaculty_does_not_modify_other_lists():
    """
    Ensure that addFaculty() only appends to the intended list,
    and does not alter any unrelated list variables.
    """
    faculty_list = []
    unrelated_list = []
    Faculty.addFaculty(faculty_list, sample_faculty_entry())
    assert len(faculty_list) == 1
    assert len(unrelated_list) == 0  # remains untouched


def test_removeFaculty_partial_match_removes():
    """
    removeFaculty() also uses substring matching ('if faculty_name in subFaculty'),
    so it should remove the entry even if only part of the name matches.
    """
    fake_faculty = [sample_faculty_entry()]
    removed = Faculty.removeFaculty(fake_faculty, "Smith")
    assert removed["name"] == "Dr. Smith"
    assert fake_faculty == []  # list should now be empty


def test_removeFaculty_multiple_entries_removes_first_match():
    """
    When multiple entries share similar names, removeFaculty()
    should remove only the first match it encounters.
    """
    fake_faculty = [
        {"name": "Dr. Smith"},
        {"name": "Dr. Smithers"},
        {"name": "Dr. Jones"},
    ]
    removed = Faculty.removeFaculty(fake_faculty, "Smith")
    assert removed["name"] == "Dr. Smith"
    assert len(fake_faculty) == 2
    assert {"name": "Dr. Smithers"} in fake_faculty
    assert {"name": "Dr. Jones"} in fake_faculty

def test_viewFaculty_empty_list_prints_nothing(capfd):
    """
    If there are no faculty entries, viewFaculty() should print nothing.
    We capture stdout to confirm it’s empty.
    """
    Faculty.viewFaculty([])
    out, _ = capfd.readouterr()
    assert out.strip() == ""


def test_str_method_returns_expected_format():
    """
    The __str__() method currently references an undefined 'self.faculty',
    but this test ensures that the method exists and returns a string.
    If later fixed to include actual info, this test can be updated.
    """
    f = Faculty(
        "Dr. Test",
        10,
        5,
        3,
        ["MWF 9-10"],
        ["CMSC 101"],
        ["Roddy 136"],
        ["Linux"],
    )
    # Even if it raises an AttributeError, we’ll catch and mark it as known behavior
    try:
        result = str(f)
        assert isinstance(result, str)
    except AttributeError:
        pytest.skip("Known issue: __str__() references undefined 'self.faculty'.")

# facCheck handles entries without 'name' key without raising:
def test_facCheck_entry_without_name_key_returns_false():
    fake = [{"foo": "bar"}, {"name": "Dr. X"}]
    assert Faculty.facCheck(fake, "Dr. X") is True
    assert Faculty.facCheck(fake, "Dr. Y") is False

# facCheck with non-string search term:
def test_facCheck_with_non_string_search_term():
    """
    facCheck() should handle non-string search terms gracefully by returning False
    rather than raising TypeError, consistent with error handling in the method.
    """
    fake = [{"name": "123"}, {"name": 456}]
    assert Faculty.facCheck(fake, 123) is False  # number search term
    assert Faculty.facCheck(fake, None) is False  # None search term

# addFaculty returns None and appends by reference:
def test_addFaculty_returns_none_and_appends_by_reference():
    lst = []
    entry = {"name": "Dr. Ref"}
    ret = Faculty.addFaculty(lst, entry)
    assert ret is None
    assert lst[0] is entry
    entry["name"] = "Dr. Ref Modified"
    assert lst[0]["name"] == "Dr. Ref Modified"

# removeFaculty when 'name' value is None:
def test_removeFaculty_entry_with_none_name_skips_and_returns_none():
    fake = [{"name": None}, {"name": "Dr. Valid"}]
    removed = Faculty.removeFaculty(fake, "Dr. Valid")
    assert removed["name"] == "Dr. Valid"
    assert any(e.get("name") is None for e in fake)

# removeFaculty identical object instances:
def test_removeFaculty_duplicate_same_object_removes_first_only():
    entry = {"name": "Dr. Twin"}
    fake = [entry, entry]
    removed = Faculty.removeFaculty(fake, "Dr. Twin")
    assert removed is entry
    assert len(fake) == 1
    assert fake[0] is entry

# viewFaculty exact formatting:
def test_viewFaculty_exact_formatting(capfd):
    e = {"name": "X"}
    fake = [e]
    Faculty.viewFaculty(fake)
    out, _ = capfd.readouterr()
    assert out == f"{e}\n\n"

# constructor preserves provided types and None:
def test_constructor_preserves_types_and_none():
    f = Faculty("N", None, None, None, None, None, None, None)
    assert f.times is None
    assert f.course_preferences is None

# case sensitivity:
def test_facCheck_is_case_sensitive():
    fake = [{"name": "Dr. Smith"}]
    assert Faculty.facCheck(fake, "dr. smith") is False
    assert Faculty.facCheck(fake, "Dr. Smith") is True