from tkinter import filedialog
from Models.Data_manager import DataManager


# Lets Create 1 DataManager for all the classes
# this should make things easier
DM = DataManager()

# Import button form the tabs view rooms and others. 
def configImportBTN(pathVar, refresh):
    global DM

    # this just opens the file manager and accepts only .json files
    filePath = filedialog.askopenfilename(title="Select a JSON file",
        filetypes=[("JSON files", "*.json")])
    pathVar.set(filePath)
    DM.loadFile(filePath)
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
