# File Name: test_lab_model.py
# Author: Fletcher Burton
# Created: October 11, 2025
#
# Unit tests for Labs_model.py using pytest.

import pytest
from Models.Labs_model import Lab


def test_add_lab_success():
    """Adding a new lab should store it in the labs list."""
    l = Lab()
    l.add("Linux")
    assert "Linux" in l.labs
    assert len(l.labs) == 1


def test_add_lab_duplicate_ignored():
    """Adding a duplicate lab should not create a second entry."""
    l = Lab(["Linux"])
    l.add("Linux")
    assert l.labs.count("Linux") == 1


def test_remove_existing_lab():
    """Removing an existing lab should succeed."""
    l = Lab(["Linux", "Windows"])
    l.remove("Linux")
    assert "Linux" not in l.labs
    assert "Windows" in l.labs


def test_remove_nonexistent_lab(capfd):
    """Removing a non-existent lab should print a warning but not raise an error."""
    l = Lab(["Linux"])
    l.remove("MacOS")
    out, _ = capfd.readouterr()
    assert "not in the system" in out
    assert len(l.labs) == 1  # unchanged


def test_modify_lab_success():
    """Modifying an existing lab should change its name."""
    l = Lab(["Linux", "Windows"])
    l.modify("Linux", "MacOS")
    assert "MacOS" in l.labs
    assert "Linux" not in l.labs


def test_modify_lab_not_found(capfd):
    """Trying to modify a non-existent lab should print a warning."""
    l = Lab(["Linux"])
    l.modify("MacOS", "Unix")
    out, _ = capfd.readouterr()
    assert "not in the system" in out
    assert "Linux" in l.labs
    assert "Unix" not in l.labs


def test_to_json_returns_list():
    """The toJson method should return a list of labs (copy or reference)."""
    labs_list = ["Linux", "Windows"]
    l = Lab(labs_list)
    json_out = l.toJson()
    assert isinstance(json_out, list)
    assert json_out == labs_list

def test_str_output():
    """String representation should include all lab names."""
    l = Lab(["Linux", "Windows"])
    text = str(l)
    assert "Linux" in text
    assert "Windows" in text
    assert "Labs in the system" in text

def test_init_empty():
    """Lab() should initialize with empty list when no args provided."""
    l = Lab()
    assert l.labs == []

def test_init_none():
    """Lab(None) should initialize with empty list."""
    l = Lab(None)
    assert l.labs == []

def test_init_preserves_list():
    """Lab should preserve the provided list without modification."""
    original = ["Linux", "Windows"]
    l = Lab(original)
    # Lab should preserve contents but use an internal copy (independent)
    assert l.labs == original
    assert l.labs is not original

def test_labs_list_independence():
    """Changes to the original list shouldn't affect the Lab instance."""
    original = ["Linux", "Windows"]
    l = Lab(original)
    original.append("MacOS")  # Modify original
    assert "MacOS" not in l.labs  # Lab.labs should be independent

def test_to_json_list_independence():
    """Changes to toJson output shouldn't affect internal labs list."""
    l = Lab(["Linux"])
    json_out = l.toJson()
    json_out.append("Windows")
    assert "Windows" not in l.labs

def test_add_empty_string():
    """Adding an empty string as lab name should work."""
    l = Lab()
    l.add("")
    assert "" in l.labs

def test_add_special_characters():
    """Adding lab names with special characters should work."""
    l = Lab()
    l.add("Lab-01")
    l.add("Lab#2")
    assert "Lab-01" in l.labs
    assert "Lab#2" in l.labs

def test_modify_to_existing_name(capfd):
    """Modifying a lab to a name that already exists."""
    l = Lab(["Linux", "Windows"])
    l.modify("Linux", "Windows")
    assert l.labs.count("Windows") == 2  # Current behavior allows duplicates in modify

def test_multiple_operations_sequence():
    """Test sequence of add/remove/modify operations."""
    l = Lab()
    l.add("Linux")
    l.add("Windows")
    l.modify("Linux", "Unix")
    l.remove("Windows")
    l.add("MacOS")
    assert set(l.labs) == {"Unix", "MacOS"}

def test_whitespace_handling():
    """Test handling of whitespace in lab names."""
    l = Lab()
    l.add("  Linux  ")  # Leading/trailing spaces
    l.add("\tWindows\n")  # Tabs and newlines
    assert "  Linux  " in l.labs  # Should preserve whitespace
    assert "\tWindows\n" in l.labs

def test_add_non_string():
    """Adding non-string values should work (current behavior) or raise TypeError."""
    l = Lab()
    l.add(123)  # Current implementation accepts this
    assert 123 in l.labs

def test_modify_with_non_string():
    """Modifying with non-string values."""
    l = Lab(["Linux"])
    l.modify("Linux", 123)
    assert 123 in l.labs

def test_str_special_characters():
    """String representation should handle special characters."""
    l = Lab(["Lab-01", "Lab#2", "  Lab  "])
    text = str(l)
    assert "Lab-01" in text
    assert "Lab#2" in text
    assert "  Lab  " in text

def test_empty_list_operations():
    """Operations on empty lab list."""
    l = Lab()
    assert str(l) == "Labs in the system: []."
    l.remove("NonExistent")  # Should just print warning
    l.modify("NonExistent", "Still NonExistent")  # Should just print warning
    assert l.labs == []