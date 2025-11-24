from tkinter import filedialog
from Models.Data_manager import DataManager
from scheduler import Scheduler, CombinedConfig
import os
import json
import csv

# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter
from .controllerUtils import exportSchedulesBTN

# from scheduler.config import CombinedConfig

# Lets Create 1 DataManager for all the classes
# this should make things easier
DM = DataManager()


# Import button form the tabs view rooms and others.
def configImportBTN(pathVar, refresh=None):
    global DM

    # this just opens the file manager and accepts only .json files
    filePath = filedialog.askopenfilename(
        title="Select a JSON file", filetypes=[("JSON files", "*.json")]
    )
    pathVar.set(filePath)
    DM.loadFile(filePath)

    if refresh:
        refresh("ConfigPage")


def configExportBTN(pathVar):
    global DM

    file_path = filedialog.asksaveasfilename(
        defaultextension=".json", filetypes=[("Text files", "*.json")]
    )
    if file_path != "":
        DM.saveData(file_path)
        pathVar.set(f"Config File saved to Path: {file_path}.")


def generateSchedulesBtn(limit, optimize, progressCallback):
    global DM
    DM.updateLimit(limit)
    DM.updateOptimizerFlags(optimize)

    config = CombinedConfig(**(DM.data or {}))

    scheduler = Scheduler(config)
    all_schedules = []

    total_steps = limit + (1 if optimize else 0)  # optimization counts as one step
    current_step = 0
    if optimize:
        # Add optimization logic here if needed
        current_step += 1
        if progressCallback:
            progressCallback(current_step, total_steps)

    for i, schedule in enumerate(scheduler.get_models()):
        if i >= limit:
            break
        schedule_list = [course.as_csv().split(",") for course in schedule]
        all_schedules.append(schedule_list)

        current_step += 1
        if progressCallback:
            progressCallback(current_step, total_steps)

    return all_schedules


def checkFileContent(data, pathEntaryVar):
    if not isinstance(data, list):
        # cheaks if data is a list or not
        pathEntaryVar.set("Please open a valid file!")
        return False

    # we look at each schedule in the list
    for idx, sch in enumerate(data):
        # checks if the whole data schedule is a list or not
        if not isinstance(sch, list):
            pathEntaryVar.set(f"Invalid: schedule {idx} is not a list.")
            return False

        # chesi if we have empty schedule
        if len(sch) == 0:
            pathEntaryVar.set(f"Invalid: schedule {idx} is empty.")
            return False

        # checking each schedule
        for ridx, row in enumerate(sch):
            # check if the row is a list or not
            if not isinstance(row, list):
                pathEntaryVar.set(
                    f"Invalid: row {ridx} in schedule {ridx} is not a list."
                )
                return False

            # to check if we have atleat 5 things in the row
            # at least calss, facult, room, lab ,1 time
            if len(row) < 5:
                pathEntaryVar.set(
                    f"Invalid: row {ridx} in schedule {ridx} has too few elements."
                )
                return False

    return True


# stupid
def stupid():
    # just to make the CI stuff happy, without
    # from .controllerUtils import exportSchedulesBTN
    # I get lots of errors,
    # if i import it have to use it to make the ruff checker happy
    # or here it is
    exportSchedulesBTN("s", "s")


def csvToJson(data):
    # turn CSV data to json
    schedules = []
    current_schedule = []

    for row in data:
        if not row:
            if current_schedule:
                schedules.append(current_schedule)
                current_schedule = []
            continue

        current_schedule.append(row)

    # Add last schedule if it exists
    if current_schedule:
        schedules.append(current_schedule)

    return schedules


def importSchedulesBTN(pathEntaryVar):
    # This will work for both the csv and json files now
    filePath = filedialog.askopenfilename(
        title="Select a JSON file",
        filetypes=[("JSON files", "*.json"), ("CSV files", "*.csv")],
    )

    if filePath and os.path.exists(filePath):
        sch = None
        ext = os.path.splitext(filePath)[1].lower()
        if ext == ".json":
            with open(filePath, "r") as file:
                sch = json.load(file)
                # If wrapped like {"schedules": [...]}, unwrap it
                if isinstance(sch, dict) and "schedules" in sch:
                    # if value is a list of lists, validate it; otherwise return the full dict
                    val = sch["schedules"]
                    if isinstance(val, list) and all(isinstance(x, list) for x in val):
                        if not checkFileContent(val, pathEntaryVar):
                            return None
                        sch = val
                    else:
                        pathEntaryVar.set(filePath)
                        return sch  # return original dict for simple test-style JSONs
        elif ext == ".csv":
            with open(filePath, "r") as file:
                reader = csv.reader(file)
                sch = list(reader)
                sch = csvToJson(sch)
                # print(sch)
                if not checkFileContent(sch, pathEntaryVar):
                    return None
    else:
        pathEntaryVar.set(f"Please open a valid file, Unable to open: {filePath}.")
        return None

    pathEntaryVar.set(filePath)
    return sch


# room controller
class RoomsController:
    global DM

    def __init__(self):
        pass

    def listRooms(self):
        return DM.getRooms()

    def addRoom(self, roomName, refresh=None):
        DM.addRoom(roomName)
        if refresh:
            refresh("ConfigPage")

    def editRoom(self, oldname, roomName, refresh=None):
        DM.editRoom(oldname, roomName)
        if refresh:
            refresh(target="ConfigPage", data=roomName)

    def removeRoom(self, roomName, refresh=None):
        if roomName in self.listRooms():
            DM.removeRoom(roomName)
            if refresh:
                refresh("ConfigPage")
        else:
            print("Room not in system")


# Lab controller
class LabsController:
    global DM

    def __init__(self):
        pass

    def listLabs(self):
        return DM.getLabs()

    def addLab(self, labName, refresh=None):  # Make refresh optional
        DM.addLab(labName)
        if refresh:  # Only refresh if requested
            refresh("ConfigPage")

    def editLab(self, oldname, labName, refresh=None):  # Make refresh optional
        DM.editLabs(oldname, labName)
        if refresh:  # Only refresh if requested
            refresh(target="ConfigPage", data=labName)

    def removeLab(self, labName, refresh=None):  # Make refresh optional
        if labName in self.listLabs():
            DM.removeLabs(labName)
            if refresh:  # Only refresh if requested
                refresh("ConfigPage")
        else:
            print("Lab not in system")


# Faculty controller
class FacultyController:
    global DM

    def __init__(self):
        pass

    def listFaculty(self):
        return DM.getFaculty()

    def addFaculty(self, newFaculty, refresh=None):  # Make refresh optional
        DM.addFaculty(newFaculty)
        if refresh:  # Only refresh if requested
            refresh("ConfigPage")

    def editFaculty(self, newFaculty, oldName, refresh=None):  # Make refresh optional
        DM.removeFaculty(oldName)
        DM.addFaculty(newFaculty)
        if refresh:  # Only refresh if requested
            refresh("ConfigPage")

    def removeFaculty(self, facName, refresh=None):  # Make refresh optional
        DM.removeFaculty(facName)
        if refresh:  # Only refresh if requested
            refresh("ConfigPage")


# Course Controller
class CourseController:
    global DM

    def __init__(self):
        pass

    def listCourses(self):
        return DM.getCourses()

    def addCourse(self, courseData, refresh=None):  # Make refresh optional
        try:
            DM.addCourse(courseData)
            if refresh:  # Only refresh if requested
                refresh("ConfigPage")
            return None
        except Exception as e:
            return str(e)

    def editCourse(
        self, oldName, newData, refresh=None, target_index=None
    ):  # Make refresh optional
        try:
            DM.editCourse(oldName, newData, target_index=target_index)
            if refresh:  # Only refresh if requested
                refresh(target="ConfigPage", data=newData)
            return None
        except Exception as e:
            return str(e)

    def removeCourse(self, courseName, refresh=None):  # Make refresh optional
        try:
            DM.removeCourse(courseName)
            if refresh:  # Only refresh if requested
                refresh("ConfigPage")
            return None
        except Exception as e:
            return str(e)


# Time Slot Controller
class TimeSlotController:
    """Controller wrapper for time-slot operations that delegates to the global DataManager (DM).
    This keeps view code consistent with other tabs that call a controller which updates DM.
    """

    def __init__(self):
        pass

    def list_intervals(self, day: str):
        try:
            return DM.get_time_intervals_for_day(day)
        except Exception:
            return []

    def add_time_interval(self, day: str, interval: dict) -> None:
        DM.add_time_interval(day, interval)

    def edit_time_interval(self, day: str, index: int, interval: dict) -> None:
        DM.edit_time_interval(day, index, interval)

    def remove_time_interval(self, day: str, index: int) -> None:
        DM.remove_time_interval(day, index)

    # Convenience wrappers that accept a refresh callable to match other controllers' APIs
    def add_time_interval_and_refresh(self, day: str, interval: dict, refresh=None):
        self.add_time_interval(day, interval)
        if callable(refresh):
            try:
                refresh("ConfigPage")
            except Exception:
                pass

    def edit_time_interval_and_refresh(
        self, day: str, index: int, interval: dict, refresh=None
    ):
        self.edit_time_interval(day, index, interval)
        if callable(refresh):
            try:
                refresh("ConfigPage")
            except Exception:
                pass

    def remove_time_interval_and_refresh(self, day: str, index: int, refresh=None):
        self.remove_time_interval(day, index)
        if callable(refresh):
            try:
                refresh("ConfigPage")
            except Exception:
                pass

    # Backwards-compatible helpers used in some older views
    def get_all(self):
        # Return a flat list of stored times across days (rarely used)
        cfg = DM.getTimeSlotConfig()
        out = []
        for day, intervals in cfg.times.items():
            for iv in intervals:
                out.append({"day": day, **iv.to_dict()})
        return out
