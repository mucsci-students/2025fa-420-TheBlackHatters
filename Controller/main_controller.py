from tkinter import filedialog
from Models.Data_manager import DataManager
from scheduler import Scheduler, CombinedConfig
import os, json
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


class FacultyController:
    global DM
    print("TODO")

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
    

def importSchedulesBTN(pathEntaryVar):
    # this just opens the file manager and accepts only .json files
    filePath = filedialog.askopenfilename(title="Select a JSON file",
        filetypes=[("JSON files", "*.json")])
    
    if filePath and os.path.exists(filePath):
        with open(filePath, 'r') as file:
            sch = json.load(file)
            #print(sch)
        
            pathEntaryVar.set(filePath)
        return sch
    else:
        pathEntaryVar.set(f"Please open a valid file, Unable to open: {filePath}.")
        return None


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
