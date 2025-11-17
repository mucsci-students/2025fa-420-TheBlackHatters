# File Name: test_lab_model.py
# Author: Fletcher Burton
# Created: October 11, 2025
#
# Unit tests for Labs_model.py using pytest.

from Models.Labs_model import Lab


def test_add_lab_success():
    """Adding a new lab should store it in the labs list."""
    lab = Lab()
    lab.add("Linux")
    assert "Linux" in lab.labs
    assert len(lab.labs) == 1


def test_add_lab_duplicate_ignored():
    """Adding a duplicate lab should not create a second entry."""
    lab = Lab(["Linux"])
    lab.add("Linux")
    assert lab.labs.count("Linux") == 1


def test_remove_existing_lab():
    """Removing an existing lab should succeed."""
    lab = Lab(["Linux", "Windows"])
    lab.remove("Linux")
    assert "Linux" not in lab.labs
    assert "Windows" in lab.labs


def test_remove_nonexistent_lab(capfd):
    """Removing a non-existent lab should print a warning but not raise an error."""
    lab = Lab(["Linux"])
    lab.remove("MacOS")
    out, _ = capfd.readouterr()
    assert "not in the system" in out
    assert len(lab.labs) == 1  # unchanged


def test_modify_lab_success():
    """Modifying an existing lab should change its name."""
    lab = Lab(["Linux", "Windows"])
    lab.modify("Linux", "MacOS")
    assert "MacOS" in lab.labs
    assert "Linux" not in lab.labs


def test_modify_lab_not_found(capfd):
    """Trying to modify a non-existent lab should print a warning."""
    lab = Lab(["Linux"])
    lab.modify("MacOS", "Unix")
    out, _ = capfd.readouterr()
    assert "not in the system" in out
    assert "Linux" in lab.labs
    assert "Unix" not in lab.labs


def test_to_json_returns_list():
    """The toJson method should return a list of labs (copy or reference)."""
    labs_list = ["Linux", "Windows"]
    lab = Lab(labs_list)
    json_out = lab.toJson()
    assert isinstance(json_out, list)
    assert json_out == labs_list


def test_str_output():
    """String representation should include all lab names."""
    lab = Lab(["Linux", "Windows"])
    text = str(lab)
    assert "Linux" in text
    assert "Windows" in text
    assert "Labs in the system" in text


def test_init_empty():
    """Lab() should initialize with empty list when no args provided."""
    lab = Lab()
    assert lab.labs == []


def test_init_none():
    """Lab(None) should initialize with empty list."""
    lab = Lab(None)
    assert lab.labs == []


def test_init_preserves_list():
    """Lab should preserve the provided list without modification."""
    original = ["Linux", "Windows"]
    lab = Lab(original)
    # Lab should preserve contents but use an internal copy (independent)
    assert lab.labs == original
    assert lab.labs is not original


def test_labs_list_independence():
    """Changes to the original list shouldn't affect the Lab instance."""
    original = ["Linux", "Windows"]
    lab = Lab(original)
    original.append("MacOS")  # Modify original
    assert "MacOS" not in lab.labs  # Lab.labs should be independent


def test_to_json_list_independence():
    """Changes to toJson output shouldn't affect internal labs list."""
    lab = Lab(["Linux"])
    json_out = lab.toJson()
    json_out.append("Windows")
    assert "Windows" not in lab.labs


def test_add_empty_string():
    """Adding an empty string as lab name should work."""
    lab = Lab()
    lab.add("")
    assert "" in lab.labs


def test_add_special_characters():
    """Adding lab names with special characters should work."""
    lab = Lab()
    lab.add("Lab-01")
    lab.add("Lab#2")
    assert "Lab-01" in lab.labs
    assert "Lab#2" in lab.labs


def test_modify_to_existing_name(capfd):
    """Modifying a lab to a name that already exists."""
    lab = Lab(["Linux", "Windows"])
    lab.modify("Linux", "Windows")
    assert lab.labs.count("Windows") == 2  # Current behavior allows duplicates in modify


def test_multiple_operations_sequence():
    """Test sequence of add/remove/modify operations."""
    lab = Lab()
    lab.add("Linux")
    lab.add("Windows")
    lab.modify("Linux", "Unix")
    lab.remove("Windows")
    lab.add("MacOS")
    assert set(lab.labs) == {"Unix", "MacOS"}


def test_whitespace_handling():
    """Test handling of whitespace in lab names."""
    lab = Lab()
    lab.add("  Linux  ")  # Leading/trailing spaces
    lab.add("\tWindows\n")  # Tabs and newlines
    assert "  Linux  " in lab.labs  # Should preserve whitespace
    assert "\tWindows\n" in lab.labs


def test_add_non_string():
    """Adding non-string values should work (current behavior) or raise TypeError."""
    lab = Lab()
    lab.add(123)  # Current implementation accepts this
    assert 123 in lab.labs


def test_modify_with_non_string():
    """Modifying with non-string values."""
    lab = Lab(["Linux"])
    lab.modify("Linux", 123)
    assert 123 in lab.labs


def test_str_special_characters():
    """String representation should handle special characters."""
    lab = Lab(["Lab-01", "Lab#2", "  Lab  "])
    text = str(lab)
    assert "Lab-01" in text
    assert "Lab#2" in text
    assert "  Lab  " in text


def test_empty_list_operations():
    """Operations on empty lab list."""
    lab = Lab()
    assert str(lab) == "Labs in the system: []."
    lab.remove("NonExistent")  # Should just print warning
    lab.modify("NonExistent", "Still NonExistent")  # Should just print warning
    assert lab.labs == []
