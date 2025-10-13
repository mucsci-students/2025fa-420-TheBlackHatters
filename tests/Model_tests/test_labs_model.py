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