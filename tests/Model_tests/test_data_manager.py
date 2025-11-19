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


def test_saveData_no_path():
    """saveData should handle missing path gracefully."""
    dm = DataManager()
    dm.filePath = None
    with patch("builtins.print") as mock_print:
        dm.saveData()
        mock_print.assert_called_with("No path specified for saveData()")


def test_saveData_permission_error(tmp_path):
    """Should handle permission errors when saving."""
    dm = DataManager()
    dm.data = {"config": {}}
    with patch("builtins.open", side_effect=PermissionError):
        with pytest.raises(PermissionError):
            dm.saveData("invalid/path/file.json")


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


def test_editRoom_nonexistent():
    """Should handle editing non-existent room."""
    dm = DataManager()
    dm.data = {"config": {"rooms": []}}
    with pytest.raises(ValueError):
        dm.editRoom("NonExistent", "NewName")


def test_removeRoom_nonexistent():
    """Should handle removing non-existent room."""
    dm = DataManager()
    dm.data = {"config": {"rooms": []}}
    with pytest.raises(ValueError):
        dm.removeRoom("NonExistent")


def test_duplicate_room_names(sample_config):
    """Should handle adding duplicate room names."""
    dm = DataManager()
    dm.data = sample_config
    existing_room = dm.getRooms()[0]
    dm.addRoom(existing_room)  # Current behavior allows duplicates
    assert dm.getRooms().count(existing_room) == 2


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


def test_editLab_nonexistent():
    """Should handle editing non-existent lab."""
    dm = DataManager()
    dm.data = {"config": {"labs": []}}
    with pytest.raises(ValueError):
        dm.editLabs("NonExistent", "NewName")


def test_removeLab_nonexistent():
    """Should handle removing non-existent lab."""
    dm = DataManager()
    dm.data = {"config": {"labs": []}}
    with pytest.raises(ValueError):
        dm.removeLabs("NonExistent")


def test_duplicate_lab_names(sample_config):
    """Should handle adding duplicate lab names."""
    dm = DataManager()
    dm.data = sample_config
    existing_lab = dm.getLabs()[0]
    dm.addLab(existing_lab)  # Current behavior allows duplicates
    assert dm.getLabs().count(existing_lab) == 2


# ---- CRUD: Faculty ----


def test_remove_nonexistent_faculty():
    """Should handle removing non-existent faculty."""
    dm = DataManager()
    dm.data = {"config": {"faculty": []}}
    with pytest.raises(ValueError):
        dm.removeFaculty("NonExistent")


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
    updates = {
        "credits": 5,
        "room": ["Roddy 102"],
        "lab": ["Windows"],
        "faculty": ["Jones"],
    }
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


def test_course_with_circular_conflicts(sample_config):
    """Should handle courses with circular conflicts."""
    dm = DataManager()
    dm.data = sample_config

    # Create two courses that conflict with each other
    course1 = {"course_id": "CMSC 150", "credits": 3, "conflicts": ["CMSC 160"]}
    course2 = {"course_id": "CMSC 160", "credits": 3, "conflicts": ["CMSC 150"]}

    dm.addCourse(course1)
    dm.addCourse(course2)

    # Verify both courses exist with their conflicts
    courses = dm.getCourses()
    c150 = next(c for c in courses if c["course_id"] == "CMSC 150")
    c160 = next(c for c in courses if c["course_id"] == "CMSC 160")
    assert "CMSC 160" in c150["conflicts"]
    assert "CMSC 150" in c160["conflicts"]


def test_course_edit_with_cascade_updates(sample_config):
    """Should handle updating course ID that's referenced in conflicts."""
    dm = DataManager()
    dm.data = sample_config

    # Add a course that conflicts with CMSC 140
    dm.addCourse({"course_id": "CMSC 150", "credits": 3, "conflicts": ["CMSC 140"]})

    # Rename CMSC 140 and verify the conflict is updated
    dm.editCourse("CMSC 140", {"course_id": "CMSC 141"})
    courses = dm.getCourses()
    c150 = next(c for c in courses if c["course_id"] == "CMSC 150")
    assert "CMSC 141" in c150["conflicts"]  # Should be updated


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


def test_clean_invalid_references_empty_lists():
    """Should handle empty reference lists."""
    dm = DataManager()
    dm.data = {
        "config": {
            "rooms": [],
            "labs": [],
            "faculty": [],
            "courses": [
                {
                    "course_id": "TEST101",
                    "credits": 3,
                    "room": [],
                    "lab": [],
                    "faculty": [],
                    "conflicts": [],
                }
            ],
        }
    }
    changed = dm._clean_invalid_references()
    assert changed is False  # No changes needed for empty lists


def test_clean_invalid_references_missing_fields():
    """Should handle courses missing optional fields."""
    dm = DataManager()
    dm.data = {
        "config": {
            "rooms": ["Room1"],
            "labs": ["Lab1"],
            "faculty": [{"name": "Faculty1"}],
            "courses": [
                {
                    "course_id": "TEST101",
                    "credits": 3,
                    # Missing room, lab, faculty, conflicts fields
                }
            ],
        }
    }
    changed = dm._clean_invalid_references()
    assert changed is False  # No changes needed for missing fields


def test_default_data_missing_template():
    """Should handle missing template file gracefully."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            DataManager()


def test_default_data_invalid_json():
    """Should handle corrupted template file."""
    with patch("builtins.open", mock_open(read_data="invalid json")):
        with pytest.raises(json.JSONDecodeError):
            DataManager()


def test_updateLimit():
    """Should update limit value correctly."""
    dm = DataManager()
    dm.data = {"limit": 5}
    dm.updateLimit(10)
    assert dm.data["limit"] == 10


def test_updateOptimizerFlags():
    """Should update optimizer flags correctly."""
    dm = DataManager()
    dm.data = {"optimizer_flags": []}
    new_flags = ["flag1", "flag2"]
    dm.updateOptimizerFlags(new_flags)
    assert dm.data["optimizer_flags"] == new_flags


def test_data_consistency_after_operations(sample_config):
    """Should maintain data consistency through multiple operations."""
    dm = DataManager()
    dm.data = sample_config

    # Perform a series of operations
    dm.addRoom("NewRoom")
    dm.addLab("NewLab")
    dm.addFaculty({"name": "NewFaculty"})

    # Add a course using all new resources
    dm.addCourse(
        {
            "course_id": "NEW101",
            "credits": 3,
            "room": ["NewRoom"],
            "lab": ["NewLab"],
            "faculty": ["NewFaculty"],
        }
    )

    # Remove resources in use
    with pytest.raises(ValueError):
        dm.removeRoom("NewRoom")  # Should fail - in use
    with pytest.raises(ValueError):
        dm.removeLabs("NewLab")  # Should fail - in use
    with pytest.raises(ValueError):
        dm.removeFaculty("NewFaculty")  # Should fail - in use

    # Remove course first, then resources
    dm.removeCourse("NEW101")
    dm.removeRoom("NewRoom")  # Should succeed
    dm.removeLabs("NewLab")  # Should succeed
    dm.removeFaculty("NewFaculty")  # Should succeed
