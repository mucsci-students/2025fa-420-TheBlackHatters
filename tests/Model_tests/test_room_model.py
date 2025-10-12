# File Name: test_room_model.py
# Author: Fletcher Burton
# Created: October 11, 2025
#
# Unit tests for Rooms_model.py using pytest.

import pytest
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