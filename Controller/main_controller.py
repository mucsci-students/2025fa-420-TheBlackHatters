from tkinter import filedialog
from Models.Data_manager import DataManager
from scheduler import Scheduler, CombinedConfig
import os, json,io,csv
# from scheduler.config import CombinedConfig

# Lets Create 1 DataManager for all the classes
# this should make things easier
DM = DataManager()

# Import button form the tabs view rooms and others. 
def configImportBTN(pathVar, refresh = None):
    global DM

    # this just opens the file manager and accepts only .json files
    filePath = filedialog.askopenfilename(title="Select a JSON file",
        filetypes=[("JSON files", "*.json")])
    pathVar.set(filePath)
    DM.loadFile(filePath)

    if refresh:
        refresh("ConfigPage")
    

def configExportBTN(pathVar):
    global DM

    file_path = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("Text files", "*.json")]
    )
    if file_path != "":
        DM.saveData(file_path)
        pathVar.set(f"Config File saved to Path: {file_path}.")
    
def generateSchedulesBtn(limit, optimize):
    global DM

    # TODO: Not sure how to update the limit, optimize gotten form user. 
    config = CombinedConfig(**DM.data)
    # print(config)

    scheduler = Scheduler(config)
    all_schedules = []
    for schedule in scheduler.get_models():
        # print(schedule)
        schedule_list = []
        for course in schedule:
            csv_line = course.as_csv()
            # print(csv_line)

            schedule_list.append(csv_line.split(','))
                    
            all_schedules.append(schedule_list)

    print(all_schedules)
    

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
                pathEntaryVar.set(f"Invalid: row {ridx} in schedule {ridx} is not a list.")
                return False

            # to check if we have atleat 5 things in the row
            # at least calss, facult, room, lab ,1 time
            if len(row) < 5: 
                pathEntaryVar.set(f"Invalid: row {ridx} in schedule {ridx} has too few elements.")
                return False
            
    return True

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
    filePath = filedialog.askopenfilename(title="Select a JSON file",
        filetypes=[("JSON files", "*.json"), ("CSV files", "*.csv")])
    
    if filePath and os.path.exists(filePath):
        sch = None
        ext = os.path.splitext(filePath)[1].lower()
        if ext == ".json":
            with open(filePath, 'r') as file:
                sch = json.load(file)
                if not checkFileContent(sch, pathEntaryVar):
                    return None
        elif ext == ".csv":
            with open(filePath, 'r') as file:
                reader = csv.reader(file)
                sch = list(reader)
                sch = csvToJson(sch)
                # print(sch)
                if not checkFileContent(sch,  pathEntaryVar):
                    return None      
    else:
        pathEntaryVar.set(f"Please open a valid file, Unable to open: {filePath}.")
        return None
    
    pathEntaryVar.set(filePath)
    return sch

def exportAllSchedulesBTN(data, pathEntaryVar):
    # exports all schedules :)

    filePath = filedialog.asksaveasfilename(defaultextension=".json",
        filetypes=[("Text files", "*.json")])
    
    if filePath != "":
        with open(filePath , "w") as f:
            json.dump(data, f, indent= 4)

        pathEntaryVar.set(f"Schedules have been saved to File saved to Path: {filePath}.")

def exportOneScheduleBTN(data, pathEntaryVar, num):
    # exports selected schedule :)
    selectedSch = data[num-1]

    filePath = filedialog.asksaveasfilename(defaultextension=".json",
        filetypes=[("Text files", "*.json")])
    
    if filePath != "":
        with open(filePath , "w") as f:
            json.dump(selectedSch, f, indent= 4)

        pathEntaryVar.set(f"Your 1 Schedule have been saved to File saved to Path: {filePath}.")

# room controller 
class RoomsController:
    global DM
    def __init__(self):
        pass

    def listRooms(self):
        return DM.getRooms()

    def addRoom(self, roomName, refresh):
        DM.addRoom(roomName)
        refresh("ConfigPage")

    def editRoom(self,oldname, roomName, refresh):
        DM.editRoom(oldname,roomName)
        refresh(target = "ConfigPage", data = roomName)

    def removeRoom(self, roomName, refresh):
        if roomName in self.listRooms():
            DM.removeRoom(roomName)
            refresh("ConfigPage")
        else: 
            print('Room not in system')


# Lab controller 
class LabsController:
    global DM
    def __init__(self):
        pass

    def listLabs(self):
        return DM.getLabs()

    def addLab(self, labName, refresh):
        DM.addLab(labName)
        refresh("ConfigPage")

    def editLab(self,oldname, labName, refresh):
        DM.editLabs(oldname,labName)
        refresh(target = "ConfigPage", data = labName)

    def removeLab(self, labName, refresh):
        if labName in self.listLabs():
            DM.removeLabs(labName)
            refresh("ConfigPage")
        else: 
            print('Lab not in system')

# Faculty controller           
class FacultyController:
    global DM
    def __init__(self):
        pass
    
    def listFaculty(self):
        return DM.getFaculty()
    
    def addFaculty(self, newFaculty, refresh):
        DM.addFaculty(newFaculty)
        refresh("ConfigPage")

    def editFaculty(self, newFaculty, facultyName, refresh):
        DM.removeFaculty(newFaculty)
        DM.addFaculty(newFaculty)
        refresh("ConfigPage")

    def removeFaculty(self, faculty, refresh):
        DM.removeFaculty(faculty)
        refresh("ConfigPage")
        
# Course Controller
class CourseController:
    global DM
    def __init__(self):
        pass
    def listCourses(self):
        return DM.getCourses()

    def addCourse(self, courseData, refresh):
        try:
            DM.addCourse(courseData)
            refresh("ConfigPage")
            return None
        except Exception as e:
            return str(e)

    def editCourse(self, oldName, newData, refresh, target_index=None):
        try:
            DM.editCourse(oldName, newData, target_index=target_index)
            refresh(target="ConfigPage", data=newData)
            return None
        except Exception as e:
            return str(e)

    def removeCourse(self, courseName, refresh):
        try:
            DM.removeCourse(courseName)
            refresh("ConfigPage")
            return None
        except Exception as e:
            return str(e)
