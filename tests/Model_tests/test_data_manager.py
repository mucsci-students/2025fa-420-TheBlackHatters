# File Name: test_data_manager.py
# Author: Fletcher Burton
# Created: October 11, 2025
#
# Unit tests for Data_manager.py using pytest and mock JSON data.

import json
import pytest
from unittest.mock import mock_open, patch

from Models.Data_manager import DataManager



@pytest.fixture
def sample_config():
    """Minimal but valid configuration matching what DataManager expects."""
    return {
        "config": {
            "rooms": ["Roddy 101", "Roddy 102"],
            "labs": ["Linux", "Windows"],
            "faculty": [{"name": "Zoppetti"}, {"name": "Jones"}],
            "courses": [
                {
                    "course_id": "CMSC 140",
                    "credits": 4,
                    "room": ["Roddy 101"],
                    "lab": ["Linux"],
                    "faculty": ["Zoppetti"],
                    "conflicts": [],
                }
            ],
        }
    }


# ---- Basic loading / saving ----

def test_default_data_loads_from_template(tmp_path):
    """Should call deafultData() when no file path is given."""
    template_path = tmp_path / "ConfigTemplate.json"
    fake_data = {"config": {"rooms": []}}
    template_path.write_text(json.dumps(fake_data))

    with patch("builtins.open", mock_open(read_data=json.dumps(fake_data))) as m:
        dm = DataManager()
        dm.deafultData()  # exercise explicitly
        assert "config" in dm.deafultData()
        m.assert_called()


def test_loadFile_reads_json(tmp_path, sample_config):
    """loadFile should read and populate data."""
    data_str = json.dumps(sample_config)
    m = mock_open(read_data=data_str)
    with patch("builtins.open", m):
        dm = DataManager()
        dm.loadFile("dummy.json")
    assert dm.data == sample_config


def test_saveData_writes_json(tmp_path, sample_config):
    """saveData should write the current data as JSON."""
    file_path = tmp_path / "out.json"
    dm = DataManager()
    dm.data = sample_config
    dm.filePath = str(file_path)
    dm.saveData()
    written = json.loads(file_path.read_text())
    assert written == sample_config


# ---- CRUD: Rooms ----

def test_add_edit_remove_room(sample_config):
    dm = DataManager()
    dm.data = sample_config
    dm.addRoom("Roddy 103")
    assert "Roddy 103" in dm.getRooms()
    dm.editRoom("Roddy 103", "Roddy 105")
    assert "Roddy 105" in dm.getRooms()
    dm.removeRoom("Roddy 105")
    assert "Roddy 105" not in dm.getRooms()


# ---- CRUD: Labs ----

def test_add_edit_remove_lab(sample_config):
    dm = DataManager()
    dm.data = sample_config
    dm.addLab("MacOS")
    assert "MacOS" in dm.getLabs()
    dm.editLabs("MacOS", "Unix")
    assert "Unix" in dm.getLabs()
    dm.removeLabs("Unix")
    assert "Unix" not in dm.getLabs()


# ---- CRUD: Faculty ----

def test_add_faculty(sample_config):
    dm = DataManager()
    dm.data = sample_config
    new_faculty = {"name": "Delaney"}
    dm.addFaculty(new_faculty)
    assert new_faculty in dm.getFaculty()


# ---- Courses ----

def test_add_and_remove_course_success(sample_config):
    dm = DataManager()
    dm.data = sample_config
    new_course = {
        "course_id": "CMSC 150",
        "credits": 4,
        "room": ["Roddy 101"],
        "lab": ["Linux"],
        "faculty": ["Jones"],
        "conflicts": ["CMSC 140"],
    }
    dm.addCourse(new_course)
    ids = [c["course_id"] for c in dm.getCourses()]
    assert "CMSC 150" in ids
    dm.removeCourse("CMSC 150")
    ids = [c["course_id"] for c in dm.getCourses()]
    assert "CMSC 150" not in ids


def test_editCourse_updates_fields(sample_config):
    dm = DataManager()
    dm.data = sample_config
    old_id = "CMSC 140"
    updates = {"credits": 5, "room": ["Roddy 102"], "lab": ["Windows"], "faculty": ["Jones"]}
    dm.editCourse(old_id, updates)
    edited = [c for c in dm.getCourses() if c["course_id"] == old_id][0]
    assert edited["credits"] == 5
    assert edited["room"] == ["Roddy 102"]
    assert edited["lab"] == ["Windows"]
    assert edited["faculty"] == ["Jones"]


def test_editCourse_invalid_id_raises(sample_config):
    dm = DataManager()
    dm.data = sample_config
    with pytest.raises(ValueError):
        dm.editCourse("INVALID", {"credits": 5})


# ---- Cleaning references ----

def test_clean_invalid_references_removes_bad_links(sample_config):
    dm = DataManager()
    dm.data = sample_config
    # corrupt a course
    c = dm.data["config"]["courses"][0]
    c["room"].append("MissingRoom")
    c["lab"].append("GhostLab")
    c["faculty"].append("GhostFaculty")
    c["conflicts"].append("GhostCourse")

    changed = dm._clean_invalid_references()
    assert changed is True

    # all invalid references should now be gone
    c = dm.getCourses()[0]
    assert "MissingRoom" not in c["room"]
    assert "GhostLab" not in c["lab"]
    assert "GhostFaculty" not in c["faculty"]
    assert "GhostCourse" not in c["conflicts"]