# File Name: test_room_model.py
# Author: Fletcher Burton
# Created: October 11, 2025
#
# Unit tests for Rooms_model.py using pytest.

from Models.Room_model import Room


def test_add_room_success():
    """Adding a new room should store it in the rooms list."""
    r = Room()
    r.add("Roddy 101")
    assert "Roddy 101" in r.rooms
    assert len(r.rooms) == 1


def test_add_room_duplicate_ignored():
    """Adding a duplicate room should not create a second entry."""
    r = Room(["Roddy 101"])
    r.add("Roddy 101")
    assert r.rooms.count("Roddy 101") == 1


def test_remove_existing_room():
    """Removing an existing room should succeed."""
    r = Room(["Roddy 101", "Roddy 102"])
    r.remove("Roddy 101")
    assert "Roddy 101" not in r.rooms
    assert "Roddy 102" in r.rooms


def test_remove_nonexistent_room(capfd):
    """Removing a non-existent room should print a warning but not raise an error."""
    r = Room(["Roddy 101"])
    r.remove("Roddy 999")
    out, _ = capfd.readouterr()
    assert "not in the system" in out
    assert len(r.rooms) == 1  # unchanged


def test_modify_room_success():
    """Modifying an existing room should change its name."""
    r = Room(["Roddy 101", "Roddy 102"])
    r.modify("Roddy 101", "Roddy 105")
    assert "Roddy 105" in r.rooms
    assert "Roddy 101" not in r.rooms


def test_modify_room_not_found(capfd):
    """Trying to modify a non-existent room should print a warning."""
    r = Room(["Roddy 101"])
    r.modify("Roddy 999", "Roddy 105")
    out, _ = capfd.readouterr()
    assert "not in the system" in out
    assert "Roddy 101" in r.rooms
    assert "Roddy 105" not in r.rooms


def test_modify_to_existing_name():
    """Modifying a room to an existing name should be allowed (current behavior)."""
    r = Room(["Roddy 101", "Roddy 102"])
    r.modify("Roddy 101", "Roddy 102")
    assert r.rooms.count("Roddy 102") == 2
    assert "Roddy 101" not in r.rooms


def test_modify_case_sensitivity():
    """Room names should be case-sensitive in modifications."""
    r = Room(["Roddy 101"])
    r.modify("Roddy 101", "RODDY 101")
    assert "RODDY 101" in r.rooms
    assert "Roddy 101" not in r.rooms


def test_to_json_returns_list():
    rooms_list = ["Roddy 101", "Roddy 102"]
    r = Room(rooms_list)
    json_out = r.toJson()
    assert isinstance(json_out, list)
    assert json_out == rooms_list
    # no need to require a new list reference


def test_str_output():
    """String representation should include all room names."""
    r = Room(["Roddy 101", "Roddy 102"])
    text = str(r)
    assert "Roddy 101" in text
    assert "Roddy 102" in text
    assert "Rooms in the system" in text


def test_init_empty():
    """Room() should initialize with empty list when no args provided."""
    r = Room()
    assert r.rooms == []


def test_init_none():
    """Room(None) should initialize with empty list."""
    r = Room(None)
    assert r.rooms == []


def test_init_with_list():
    """Room should accept and store a list of room names."""
    rooms = ["Roddy 101", "Caputo 210"]
    r = Room(rooms)
    assert r.rooms == rooms


def test_add_room_with_special_chars():
    """Room names with special characters should be handled."""
    r = Room()
    r.add("Roddy-101")
    r.add("Caputo/210")
    r.add("Room #123")
    assert "Roddy-101" in r.rooms
    assert "Caputo/210" in r.rooms
    assert "Room #123" in r.rooms


def test_add_empty_room_name():
    """Empty string as room name should be handled."""
    r = Room()
    r.add("")
    assert "" in r.rooms


def test_add_whitespace_room_name():
    """Room names with only whitespace should be handled."""
    r = Room()
    r.add("   ")
    r.add("\t\n")
    assert "   " in r.rooms
    assert "\t\n" in r.rooms


def test_add_non_string_room():
    """Adding non-string values should work (current behavior)."""
    r = Room()
    r.add(123)
    assert 123 in r.rooms


def test_modify_with_non_string():
    """Modifying with non-string values should work (current behavior)."""
    r = Room(["Roddy 101"])
    r.modify("Roddy 101", 123)
    assert 123 in r.rooms


def test_multiple_operations():
    """Test a sequence of add/remove/modify operations."""
    r = Room()
    r.add("Roddy 101")
    r.add("Roddy 102")
    r.modify("Roddy 101", "Caputo 210")
    r.remove("Roddy 102")
    r.add("Wickersham 100")
    assert set(r.rooms) == {"Caputo 210", "Wickersham 100"}


def test_modify_after_remove():
    """Attempting to modify a removed room should fail appropriately."""
    r = Room(["Roddy 101"])
    r.remove("Roddy 101")
    r.modify("Roddy 101", "Caputo 210")  # Should print warning
    assert "Roddy 101" not in r.rooms
    assert "Caputo 210" not in r.rooms


def test_rooms_list_independence():
    """Changes to the input list shouldn't affect Room instance."""
    original = ["Roddy 101", "Roddy 102"]
    r = Room(original)
    original.append("Caputo 210")
    assert "Caputo 210" not in r.rooms


def test_to_json_list_independence():
    """Changes to toJson output shouldn't affect internal list."""
    r = Room(["Roddy 101"])
    json_out = r.toJson()
    json_out.append("Roddy 102")
    assert "Roddy 102" not in r.rooms


def test_remove_error_message_format(capfd):
    """Error message for remove should include the room name."""
    r = Room()
    r.remove("Nonexistent")
    out, _ = capfd.readouterr()
    assert "Nonexistent" in out
    assert "not in the system" in out


def test_modify_error_message_format(capfd):
    """Error message for modify should include both old and new names."""
    r = Room()
    r.modify("Old Room", "New Room")
    out, _ = capfd.readouterr()
    assert "Old Room" in out
    assert "New Room" in out
    assert "not in the system" in out


def test_empty_room_string_representation():
    """String representation of empty room list should be well-formatted."""
    r = Room()
    assert str(r) == "Rooms in the system: []."


def test_operations_on_empty_room():
    """Operations on empty room list should handle gracefully."""
    r = Room()
    r.remove("Any Room")  # Should just print warning
    r.modify("Any Room", "New Room")  # Should just print warning
    assert r.rooms == []
