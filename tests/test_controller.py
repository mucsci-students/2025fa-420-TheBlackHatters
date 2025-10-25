# File Name: test_main_controller.py
# Author: Fletcher Burton
# Created: October 11, 2025
#
# Tests for main_controller.py functions and controller classes.
# Uses pytest + unittest.mock to isolate Tkinter and DataManager behavior.

import json
import pytest
from unittest.mock import Mock, patch, mock_open

with patch("Controller.main_controller.DataManager", Mock(return_value=Mock())):
    import Controller.main_controller as ctrl


# --- Fixtures ---

@pytest.fixture(autouse=True)
def reset_dm(monkeypatch):
    """Provide a mock DataManager for each test run."""
    dm = Mock()
    dm.data = {"config": {"rooms": [], "labs": [], "courses": [], "faculty": []}}
    monkeypatch.setattr(ctrl, "DM", dm)
    return dm


@pytest.fixture
def fake_refresh():
    """Simple refresh mock to assert it was called."""
    return Mock()


# --- File Import / Export ---

def test_configImportBTN_loads_json_and_refreshes(monkeypatch, fake_refresh, tmp_path):
    fake_path = tmp_path / "config.json"
    fake_path.write_text("{}")
    monkeypatch.setattr("Controller.main_controller.filedialog.askopenfilename", Mock(return_value=str(fake_path)))

    pathVar = Mock()
    ctrl.configImportBTN(pathVar, refresh=fake_refresh)

    ctrl.DM.loadFile.assert_called_once_with(str(fake_path))
    fake_refresh.assert_called_once_with("ConfigPage")
    pathVar.set.assert_called_once_with(str(fake_path))


def test_configExportBTN_saves(monkeypatch, tmp_path):
    fake_save_path = tmp_path / "out.json"
    monkeypatch.setattr("Controller.main_controller.filedialog.asksaveasfilename", Mock(return_value=str(fake_save_path)))

    pathVar = Mock()
    ctrl.configExportBTN(pathVar)

    ctrl.DM.saveData.assert_called_once_with(str(fake_save_path))
    assert "Config File saved" in pathVar.set.call_args[0][0]


def test_importSchedulesBTN_reads_valid_json(monkeypatch, tmp_path):
    data = {"schedules": [1, 2]}
    file_path = tmp_path / "sch.json"
    file_path.write_text(json.dumps(data))

    monkeypatch.setattr("Controller.main_controller.filedialog.askopenfilename", Mock(return_value=str(file_path)))

    pathVar = Mock()
    result = ctrl.importSchedulesBTN(pathVar)
    assert result == data
    assert pathVar.set.call_args[0][0] == str(file_path)


def test_importSchedulesBTN_invalid_path(monkeypatch):
    monkeypatch.setattr("Controller.main_controller.filedialog.askopenfilename", Mock(return_value="nonexistent.json"))
    pathVar = Mock()
    result = ctrl.importSchedulesBTN(pathVar)
    assert result is None
    assert "Unable to open" in pathVar.set.call_args[0][0]


def test_exportAllSchedulesBTN_writes_json(monkeypatch, tmp_path):
    fake_save = tmp_path / "all.json"
    monkeypatch.setattr("Controller.main_controller.filedialog.asksaveasfilename", Mock(return_value=str(fake_save)))

    pathVar = Mock()
    data = [{"course": "CMSC 101"}]
    ctrl.exportAllSchedulesBTN(data, pathVar)

    written = json.loads(fake_save.read_text())
    assert written == data
    assert "Schedules have been saved" in pathVar.set.call_args[0][0]


def test_exportOneScheduleBTN_writes_selected(monkeypatch, tmp_path):
    fake_save = tmp_path / "one.json"
    monkeypatch.setattr("Controller.main_controller.filedialog.asksaveasfilename", Mock(return_value=str(fake_save)))

    pathVar = Mock()
    data = [[{"course": "CMSC 101"}], [{"course": "CMSC 102"}]]
    ctrl.exportOneScheduleBTN(data, pathVar, num=2)

    written = json.loads(fake_save.read_text())
    assert written == [{"course": "CMSC 102"}]
    assert "Your 1 Schedule" in pathVar.set.call_args[0][0]


def test_exportOneScheduleBTN_invalid_num(tmp_path, monkeypatch):
    fake = tmp_path/"out.json"
    monkeypatch.setattr("Controller.main_controller.filedialog.asksaveasfilename", lambda **kwargs: str(fake))
    data = [[{"course":"X"}],[{"course":"Y"}]]
    pathVar = Mock()
    import Controller.main_controller as ctrl
    ctrl.exportOneScheduleBTN(data, pathVar, num="bad")
    assert json.loads(fake.read_text()) == []


# --- RoomsController ---

def test_roomscontroller_add_edit_remove(fake_refresh):
    c = ctrl.RoomsController()
    c.addRoom("Roddy 136", fake_refresh)
    ctrl.DM.addRoom.assert_called_with("Roddy 136")

    c.editRoom("Roddy 136", "Roddy 140", fake_refresh)
    ctrl.DM.editRoom.assert_called_with("Roddy 136", "Roddy 140")

    ctrl.DM.getRooms.return_value = ["Roddy 140"]
    c.removeRoom("Roddy 140", fake_refresh)
    ctrl.DM.removeRoom.assert_called_with("Roddy 140")


def test_roomscontroller_remove_nonexistent(capfd, fake_refresh):
    c = ctrl.RoomsController()
    ctrl.DM.getRooms.return_value = ["Roddy 136"]
    c.removeRoom("Missing", fake_refresh)
    out, _ = capfd.readouterr()
    assert "Room not in system" in out


# --- LabsController ---

def test_labscontroller_add_edit_remove(fake_refresh):
    c = ctrl.LabsController()
    c.addLab("Linux", fake_refresh)
    ctrl.DM.addLab.assert_called_with("Linux")

    c.editLab("Linux", "Windows", fake_refresh)
    ctrl.DM.editLabs.assert_called_with("Linux", "Windows")

    ctrl.DM.getLabs.return_value = ["Windows"]
    c.removeLab("Windows", fake_refresh)
    ctrl.DM.removeLabs.assert_called_with("Windows")


def test_labscontroller_remove_nonexistent(capfd, fake_refresh):
    c = ctrl.LabsController()
    ctrl.DM.getLabs.return_value = ["Linux"]
    c.removeLab("Ghost", fake_refresh)
    out, _ = capfd.readouterr()
    assert "Lab not in system" in out


# --- CourseController ---

def test_coursecontroller_add_edit_remove_success(fake_refresh):
    c = ctrl.CourseController()
    ctrl.DM.addCourse.return_value = None
    ctrl.DM.editCourse.return_value = None
    ctrl.DM.removeCourse.return_value = None

    assert c.addCourse({"id": "CMSC 150"}, fake_refresh) is None
    assert c.editCourse("CMSC 140", {"credits": 5}, fake_refresh) is None
    assert c.removeCourse("CMSC 140", fake_refresh) is None


def test_coursecontroller_add_raises(fake_refresh):
    c = ctrl.CourseController()
    ctrl.DM.addCourse.side_effect = ValueError("invalid data")
    err = c.addCourse({"bad": "x"}, fake_refresh)
    assert "invalid" in err


def test_coursecontroller_edit_raises(fake_refresh):
    c = ctrl.CourseController()
    ctrl.DM.editCourse.side_effect = ValueError("bad edit")
    err = c.editCourse("CMSC 140", {}, fake_refresh)
    assert "bad edit" in err


def test_coursecontroller_remove_raises(fake_refresh):
    c = ctrl.CourseController()
    ctrl.DM.removeCourse.side_effect = ValueError("not found")
    err = c.removeCourse("CMSC 999", fake_refresh)
    assert "not found" in err


def test_editCourse_cascade_conflict_update():
    from Models.Data_manager import DataManager
    dm = DataManager()
    dm.data = {"config": {"rooms": [], "labs": [], "courses": [], "faculty": []}}
    dm.addCourse({"course_id": "B", "credits": 3, "conflicts": []})
    dm.addCourse({"course_id": "A", "credits": 3, "conflicts": ["B"]})
    dm.editCourse("B", {"course_id": "B2"})
    courses = dm.getCourses()
    a = next(c for c in courses if c["course_id"] == "A")
    assert "B2" in a["conflicts"]
    assert "B" not in a["conflicts"]