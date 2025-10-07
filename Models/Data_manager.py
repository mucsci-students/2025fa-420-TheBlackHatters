import json

# This will manage all of the data for the whole config file. 
# We will need to give a config filePath or it will start will an empty file
# note: empty file only inclues, 
class DataManager():
    def __init__(self, filePath = None):

        self.new = True
        self.filePath = filePath
        self.data = None
        if filePath:
            self.loadFile(filePath)
        else:
            self.data = self.deafultData()

    # we want to load if we have a file path
    def loadFile(self, filePath):
        self.filePath = filePath
        if filePath:
            # Use scheduler loader
            with open(filePath, 'r') as file:
                self.data = json.load(file)



    def deafultData(self):
        # deafult data if the file path is empty. 
        # all the defult data will come from a templateFile I created
        # Without other stuff form the config file the scheduler won't run to generate schedules
        with open("template/ConfigTemplate.json", 'r') as file:
            config = json.load(file)
        
        return config
    
    def saveData(self, outPath = None, data = None):
        if data: 
            # updates data with new data
            self.data = data

        #TODO: Not sure where to do this but, need way to save/export to difrent file, 
        # not sure weather to make this here or in the contorler. 

        # writes the file to the given FilePath
        with open(outPath , "w") as f:
            json.dump(self.data, f, indent= 4)

    # each method below will get the data from file: 
    # Rooms CRUD(Create, Read, Update, Delete)
    def getRooms(self):
        return self.data["config"]["rooms"]
    
    def addRoom(self, newRoom):
        self.data["config"]["rooms"].append(newRoom)
        # actally saves the data in file
        #self.saveData(outPath = self.filePath)
    
    def editRoom(self, oldName, newName):
        rooms = self.data["config"]["rooms"]
        idx = rooms.index(oldName)
        rooms[idx] = newName
        #self.saveData(outPath = self.filePath)

    def removeRoom(self, roomName):
        rooms = self.data["config"]["rooms"]
        rooms.remove(roomName)
        #self.saveData(outPath = self.filePath)


    # Labs CRUD
    def getLabs(self):
        return self.data["config"]['labs']
    
    def addLab(self, newLab):
        self.data["config"]["labs"].append(newLab)
        #self.saveData(outPath = self.filePath)

    def editLabs(self, oldName, newName):
        labs = self.data["config"]["labs"]
        idx = labs.index(oldName)
        labs[idx] = newName
        #self.saveData(outPath = self.filePath)

    def removeLabs(self, labName):
        labs = self.data["config"]["labs"]
        labs.remove(labName)
        #self.saveData(outPath = self.filePath)

    # Course CRUD
    def getCourses(self):
        return self.data["config"]["courses"]

    def addCourse(self, newCourse):
        self.data["config"]["courses"].append(newCourse)
        #self.saveData(outPath = self.filePath)


    # Faculty CRUD
    def getFaculty(self):
        return self.data["config"]["faculty"]

    def addFaculty(self, newFaculty):
        self.data["config"]["faculty"].append(newFaculty)
        #self.saveData(outPath = self.filePath)



