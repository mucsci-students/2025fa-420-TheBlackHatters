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
    DM.load_file(filePath)
    refresh("ConfigPage")



# room controller 
class RoomsController:
    global DM
    def __init__(self):
        pass

    def listRooms(self):
        print(f"my rooms from controller: {DM.getRooms()}")
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

    