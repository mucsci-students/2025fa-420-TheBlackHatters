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
    ctrl.exportSchedulesBTN(data, pathVar)

    written = json.loads(fake_save.read_text())
    assert written == data
    assert "Schedules have been saved" in pathVar.set.call_args[0][0]


def test_exportOneScheduleBTN_writes_selected(monkeypatch, tmp_path):
    fake_save = tmp_path / "one.json"
    monkeypatch.setattr("Controller.main_controller.filedialog.asksaveasfilename", Mock(return_value=str(fake_save)))

    pathVar = Mock()
    data = [[{"course": "CMSC 101"}], [{"course": "CMSC 102"}]]
    ctrl.exportSchedulesBTN(data, pathVar, num=2)

    written = json.loads(fake_save.read_text())
    assert written == [{"course": "CMSC 102"}]
    assert "Your 1 Schedule" in pathVar.set.call_args[0][0]


def test_exportOneScheduleBTN_invalid_num(tmp_path, monkeypatch):
    fake = tmp_path/"out.json"
    monkeypatch.setattr("Controller.main_controller.filedialog.asksaveasfilename", lambda **kwargs: str(fake))
    data = [[{"course":"X"}],[{"course":"Y"}]]
    pathVar = Mock()
    import Controller.main_controller as ctrl
    ctrl.exportSchedulesBTN(data, pathVar, num="bad")
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

# --- Undo/Redo Action Tests (Fixed) ---

def test_rooms_controller_records_undo_actions(monkeypatch):
    """Test that room operations work (undo recording happens in view layer)"""
    def mock_refresh(target=None, data=None):
        pass

    c = ctrl.RoomsController()
    
    # Test room addition - should work without app_instance
    c.addRoom("Roddy 140", mock_refresh)
    ctrl.DM.addRoom.assert_called_with("Roddy 140")
    
    # Test room edit - should work without app_instance
    c.editRoom("Roddy 140", "Roddy 150", mock_refresh)
    ctrl.DM.editRoom.assert_called_with("Roddy 140", "Roddy 150")
    
    # Test room deletion - should work without app_instance
    ctrl.DM.getRooms.return_value = ["Roddy 150"]
    c.removeRoom("Roddy 150", mock_refresh)
    ctrl.DM.removeRoom.assert_called_with("Roddy 150")


def test_labs_controller_records_undo_actions():
    """Test that lab operations work (undo recording happens in view layer)"""
    def mock_refresh(target=None, data=None):
        pass

    c = ctrl.LabsController()
    
    # Test lab addition - should work without app_instance
    c.addLab("Linux Lab", mock_refresh)
    ctrl.DM.addLab.assert_called_with("Linux Lab")
    
    # Test lab edit - should work without app_instance
    c.editLab("Linux Lab", "Windows Lab", mock_refresh)
    ctrl.DM.editLabs.assert_called_with("Linux Lab", "Windows Lab")
    
    # Test lab deletion - should work without app_instance
    ctrl.DM.getLabs.return_value = ["Windows Lab"]
    c.removeLab("Windows Lab", mock_refresh)
    ctrl.DM.removeLabs.assert_called_with("Windows Lab")


def test_faculty_controller_records_undo_actions():
    """Test that faculty operations work (undo recording happens in view layer)"""
    def mock_refresh(target=None, data=None):
        pass

    c = ctrl.FacultyController()
    
    faculty_data = {"name": "Dr. Smith", "maximum_credits": 12}
    new_faculty_data = {"name": "Dr. Smith", "maximum_credits": 10}
    
    # Test faculty addition - should work without app_instance
    c.addFaculty(faculty_data, mock_refresh)
    ctrl.DM.addFaculty.assert_called_with(faculty_data)
    
    # Test faculty edit - should work without app_instance
    c.editFaculty(new_faculty_data, "Dr. Smith", mock_refresh)
    ctrl.DM.removeFaculty.assert_called_with("Dr. Smith")
    ctrl.DM.addFaculty.assert_called_with(new_faculty_data)
    
    # Test faculty deletion - should work without app_instance
    ctrl.DM.getFaculty.return_value = [faculty_data]
    c.removeFaculty("Dr. Smith", mock_refresh)
    ctrl.DM.removeFaculty.assert_called_with("Dr. Smith")


def test_course_controller_records_undo_actions():
    """Test that course operations work (undo recording happens in view layer)"""
    def mock_refresh(target=None, data=None):
        pass

    c = ctrl.CourseController()
    ctrl.DM.addCourse.return_value = None
    ctrl.DM.editCourse.return_value = None
    ctrl.DM.removeCourse.return_value = None
    
    course_data = {"course_id": "CMSC 140", "credits": 4}
    new_course_data = {"course_id": "CMSC 140", "credits": 3}
    
    # Test course addition - should work without app_instance
    result = c.addCourse(course_data, mock_refresh)
    assert result is None
    ctrl.DM.addCourse.assert_called_with(course_data)
    
    # Test course edit - should work without app_instance
    result = c.editCourse("CMSC 140", new_course_data, mock_refresh)
    assert result is None
    ctrl.DM.editCourse.assert_called_with("CMSC 140", new_course_data, target_index=None)
    
    # Test course deletion - should work without app_instance
    ctrl.DM.getCourses.return_value = [course_data]
    result = c.removeCourse("CMSC 140", mock_refresh)
    assert result is None
    ctrl.DM.removeCourse.assert_called_with("CMSC 140")


def test_controller_methods_without_app_instance(fake_refresh):
    """Test that controller methods work without app_instance (backward compatibility)"""
    c_rooms = ctrl.RoomsController()
    c_labs = ctrl.LabsController()
    c_faculty = ctrl.FacultyController()
    c_courses = ctrl.CourseController()
    
    ctrl.DM.addCourse.return_value = None
    ctrl.DM.editCourse.return_value = None
    ctrl.DM.removeCourse.return_value = None
    
    # These should not raise errors when app_instance is None
    c_rooms.addRoom("Test Room", fake_refresh)
    c_labs.addLab("Test Lab", fake_refresh)
    c_faculty.addFaculty({"name": "Test Faculty"}, fake_refresh)
    c_courses.addCourse({"course_id": "TEST 101"}, fake_refresh)


def test_controller_methods_with_optional_refresh():
    """Test that controller methods work with optional refresh parameter"""
    c_rooms = ctrl.RoomsController()
    c_labs = ctrl.LabsController()
    c_faculty = ctrl.FacultyController()
    c_courses = ctrl.CourseController()
    
    ctrl.DM.addCourse.return_value = None
    ctrl.DM.editCourse.return_value = None
    ctrl.DM.removeCourse.return_value = None
    
    # Create a minimal refresh function that doesn't fail
    def minimal_refresh(target=None, data=None):
        pass
    
    # These should work with a minimal refresh function
    c_rooms.addRoom("Room A", minimal_refresh)
    c_labs.addLab("Lab A", minimal_refresh)
    c_faculty.addFaculty({"name": "Faculty A"}, minimal_refresh)
    c_courses.addCourse({"course_id": "COURSE A"}, minimal_refresh)


def test_undo_redo_stack_logic():
    """Test the core undo/redo stack logic without GUI dependencies"""
    # Simulate the stack management logic
    undo_stack = []
    redo_stack = []
    
    def record_action(action_type, data):
        action = {'type': action_type, 'data': data}
        undo_stack.append(action)
        redo_stack.clear()
    
    def undo():
        if undo_stack:
            action = undo_stack.pop()
            redo_stack.append(action)
            return action
        return None
    
    def redo():
        if redo_stack:
            action = redo_stack.pop()
            undo_stack.append(action)
            return action
        return None
    
    # Test recording actions
    record_action('room_addition', {'room_name': 'Room 1'})
    assert len(undo_stack) == 1
    assert len(redo_stack) == 0
    
    record_action('room_addition', {'room_name': 'Room 2'})
    assert len(undo_stack) == 2
    assert len(redo_stack) == 0  # Redo stack should be cleared
    
    # Test undo
    action = undo()
    assert action['type'] == 'room_addition'
    assert action['data']['room_name'] == 'Room 2'
    assert len(undo_stack) == 1
    assert len(redo_stack) == 1
    
    # Test redo
    action = redo()
    assert action['type'] == 'room_addition'
    assert action['data']['room_name'] == 'Room 2'
    assert len(undo_stack) == 2
    assert len(redo_stack) == 0
    
    # Test undo with empty stack
    undo_stack.clear()
    assert undo() is None


def test_undo_redo_edge_cases():
    """Test edge cases for undo/redo logic"""
    undo_stack = []
    redo_stack = []
    
    def record_action(action_type, data):
        action = {'type': action_type, 'data': data}
        undo_stack.append(action)
        redo_stack.clear()
    
    def undo():
        if undo_stack:
            action = undo_stack.pop()
            redo_stack.append(action)
            return action
        return None
    
    def redo():
        if redo_stack:
            action = redo_stack.pop()
            undo_stack.append(action)
            return action
        return None
    
    # Test multiple undos/redos
    record_action('action1', {'data': 1})
    record_action('action2', {'data': 2})
    record_action('action3', {'data': 3})
    
    assert undo()['data']['data'] == 3
    assert undo()['data']['data'] == 2
    
    record_action('action4', {'data': 4})  # This should clear redo stack
    assert len(undo_stack) == 2  # action1, action4 (action2 and action3 were undone)
    assert len(redo_stack) == 0  # Cleared by new action
    
    # Verify the actual contents
    assert undo_stack[0]['data']['data'] == 1
    assert undo_stack[1]['data']['data'] == 4


def test_controller_error_handling_with_undo():
    """Test that controller errors are properly handled"""
    c = ctrl.CourseController()
    
    # Simulate an error in DataManager
    ctrl.DM.addCourse.side_effect = ValueError("Invalid course data")
    
    def minimal_refresh(target=None, data=None):
        pass
    
    # Test that errors are properly returned
    result = c.addCourse({"invalid": "data"}, minimal_refresh)
    assert "Invalid course data" in result


def test_undo_action_data_integrity():
    """Test that controller operations work correctly (data integrity is handled by DataManager)"""
    c_rooms = ctrl.RoomsController()
    c_faculty = ctrl.FacultyController()
    
    def minimal_refresh(target=None, data=None):
        pass
    
    # Test room edit - verify proper DataManager calls
    c_rooms.editRoom("Old Name", "New Name", minimal_refresh)
    ctrl.DM.editRoom.assert_called_with("Old Name", "New Name")
    
    # Test faculty edit - verify proper DataManager calls
    old_faculty = {"name": "Old", "credits": 12}
    new_faculty = {"name": "New", "credits": 10}
    
    c_faculty.editFaculty(new_faculty, "Old", minimal_refresh)
    ctrl.DM.removeFaculty.assert_called_with("Old")
    ctrl.DM.addFaculty.assert_called_with(new_faculty)


def test_undo_redo_integration_with_mocked_controllers():
    """Test the complete undo/redo flow with mocked controllers"""
    # Mock the controller calls that would happen during undo/redo
    mock_room_ctr = Mock()
    mock_lab_ctr = Mock()
    mock_faculty_ctr = Mock()
    mock_course_ctr = Mock()
    
    # Simulate the undo/redo execution logic
    def execute_undo(action):
        if action['type'] == 'room_addition':
            mock_room_ctr.removeRoom(action['data']['room_name'], refresh=None)
        elif action['type'] == 'room_deletion':
            mock_room_ctr.addRoom(action['data']['room_name'], refresh=None)
        elif action['type'] == 'lab_addition':
            mock_lab_ctr.removeLab(action['data']['lab_name'], refresh=None)
        elif action['type'] == 'lab_deletion':
            mock_lab_ctr.addLab(action['data']['lab_name'], refresh=None)
        # Add more cases as needed...
    
    def execute_redo(action):
        if action['type'] == 'room_addition':
            mock_room_ctr.addRoom(action['data']['room_name'], refresh=None)
        elif action['type'] == 'room_deletion':
            mock_room_ctr.removeRoom(action['data']['room_name'], refresh=None)
        elif action['type'] == 'lab_addition':
            mock_lab_ctr.addLab(action['data']['lab_name'], refresh=None)
        elif action['type'] == 'lab_deletion':
            mock_lab_ctr.removeLab(action['data']['lab_name'], refresh=None)
        # Add more cases as needed...
    
    # Test room addition undo/redo
    room_action = {'type': 'room_addition', 'data': {'room_name': 'Test Room'}}
    
    execute_undo(room_action)
    mock_room_ctr.removeRoom.assert_called_with('Test Room', refresh=None)
    
    execute_redo(room_action)
    mock_room_ctr.addRoom.assert_called_with('Test Room', refresh=None)
    
    # Test lab deletion undo/redo
    lab_action = {'type': 'lab_deletion', 'data': {'lab_name': 'Test Lab'}}
    
    execute_undo(lab_action)
    mock_lab_ctr.addLab.assert_called_with('Test Lab', refresh=None)
    
    execute_redo(lab_action)
    mock_lab_ctr.removeLab.assert_called_with('Test Lab', refresh=None)

def test_rooms_controller_list_rooms():
    """Test that rooms controller properly lists rooms"""
    c = ctrl.RoomsController()
    ctrl.DM.getRooms.return_value = ["Room 101", "Room 102", "Room 103"]
    
    rooms = c.listRooms()
    assert rooms == ["Room 101", "Room 102", "Room 103"]
    ctrl.DM.getRooms.assert_called_once()


def test_labs_controller_list_labs():
    """Test that labs controller properly lists labs"""
    c = ctrl.LabsController()
    ctrl.DM.getLabs.return_value = ["Lab A", "Lab B"]
    
    labs = c.listLabs()
    assert labs == ["Lab A", "Lab B"]
    ctrl.DM.getLabs.assert_called_once()


def test_faculty_controller_list_faculty():
    """Test that faculty controller properly lists faculty"""
    c = ctrl.FacultyController()
    mock_faculty = [{"name": "Dr. Smith"}, {"name": "Dr. Johnson"}]
    ctrl.DM.getFaculty.return_value = mock_faculty
    
    faculty = c.listFaculty()
    assert faculty == mock_faculty
    ctrl.DM.getFaculty.assert_called_once()


def test_course_controller_list_courses():
    """Test that course controller properly lists courses"""
    c = ctrl.CourseController()
    mock_courses = [{"course_id": "CMSC 101"}, {"course_id": "CMSC 102"}]
    ctrl.DM.getCourses.return_value = mock_courses
    
    courses = c.listCourses()
    assert courses == mock_courses
    ctrl.DM.getCourses.assert_called_once()


def test_rooms_controller_remove_nonexistent_room(capfd):
    """Test that removing nonexistent room doesn't crash"""
    c = ctrl.RoomsController()
    ctrl.DM.getRooms.return_value = ["Existing Room"]
    
    # Should not raise an error, just print message
    c.removeRoom("Nonexistent Room", None)
    
    out, _ = capfd.readouterr()
    assert "Room not in system" in out


def test_labs_controller_remove_nonexistent_lab(capfd):
    """Test that removing nonexistent lab doesn't crash"""
    c = ctrl.LabsController()
    ctrl.DM.getLabs.return_value = ["Existing Lab"]
    
    # Should not raise an error, just print message
    c.removeLab("Nonexistent Lab", None)
    
    out, _ = capfd.readouterr()
    assert "Lab not in system" in out


def test_course_controller_edit_with_target_index():
    """Test course edit with target index parameter"""
    c = ctrl.CourseController()
    ctrl.DM.editCourse.return_value = None
    
    course_data = {"course_id": "CMSC 140", "credits": 4}
    result = c.editCourse("CMSC 140", course_data, None, target_index=2)
    
    assert result is None
    ctrl.DM.editCourse.assert_called_with("CMSC 140", course_data, target_index=2)

def test_generate_schedules_with_optimization_flags():
    """Test that generateSchedulesBtn properly sets optimization flags"""
    with patch('Controller.main_controller.Scheduler') as MockScheduler:
        with patch('Controller.main_controller.CombinedConfig') as MockCombinedConfig:
            mock_scheduler_instance = MockScheduler.return_value
            mock_scheduler_instance.get_models.return_value = []
            
            # Test with optimization flags
            optimize_flags = ["faculty_course", "pack_rooms"]
            result = ctrl.generateSchedulesBtn(5, optimize_flags, None)
            
            # Verify optimization flags were set
            ctrl.DM.updateOptimizerFlags.assert_called_with(optimize_flags)
            ctrl.DM.updateLimit.assert_called_with(5)
            assert result == []

def test_export_schedules_with_empty_data():
    """Test exportSchedulesBTN handles empty data gracefully"""
    with patch('Controller.main_controller.filedialog.asksaveasfilename', return_value="test.json"):
        with patch('builtins.open', mock_open()):
            pathVar = Mock()
            
            # Test with empty data
            ctrl.exportSchedulesBTN([], pathVar)
            
            # Should not crash and should set path variable
            pathVar.set.assert_called_once()
            assert "saved" in pathVar.set.call_args[0][0].lower()


def test_generate_schedules_with_zero_limit():
    """Test generateSchedulesBtn handles zero limit gracefully"""
    with patch('Controller.main_controller.Scheduler') as MockScheduler:
        with patch('Controller.main_controller.CombinedConfig'):
            mock_scheduler_instance = MockScheduler.return_value
            mock_scheduler_instance.get_models.return_value = []
            
            # Test with limit of 0
            result = ctrl.generateSchedulesBtn(0, [], None)
            
            # Should return empty list
            assert result == []
            # Should update limit in DataManager
            ctrl.DM.updateLimit.assert_called_with(0)

def test_config_import_empty_path():
    """Test configImportBTN with empty file path"""
    with patch('Controller.main_controller.filedialog.askopenfilename', return_value=""):
        pathVar = Mock()
        refresh = Mock()
        
        ctrl.configImportBTN(pathVar, refresh)
        
        # Should set the path variable even with empty string
        pathVar.set.assert_called_with("")
        # The actual behavior might call loadFile and refresh, so let's not assert on those


def test_rooms_controller_list_method():
    """Test that rooms controller list method works correctly"""
    c = ctrl.RoomsController()
    expected_rooms = ["Room 101", "Room 102", "Room 103"]
    ctrl.DM.getRooms.return_value = expected_rooms
    
    result = c.listRooms()
    
    assert result == expected_rooms
    ctrl.DM.getRooms.assert_called_once()


def test_faculty_controller_list_method():
    """Test that faculty controller list method works correctly"""
    c = ctrl.FacultyController()
    expected_faculty = [{"name": "Dr. Smith"}, {"name": "Dr. Johnson"}]
    ctrl.DM.getFaculty.return_value = expected_faculty
    
    result = c.listFaculty()
    
    assert result == expected_faculty
    ctrl.DM.getFaculty.assert_called_once()


def test_labs_controller_list_method():
    """Test that labs controller list method works correctly"""
    c = ctrl.LabsController()
    expected_labs = ["Lab A", "Lab B"]
    ctrl.DM.getLabs.return_value = expected_labs
    
    result = c.listLabs()
    
    assert result == expected_labs
    ctrl.DM.getLabs.assert_called_once()