import json

# This will manage all of the data for the whole config file. 
# We will need to give a config filePath or it will start will an empty file
# note: empty file only inclues, 
class DataManager():
    def __init__(self, filePath = None):

        self.filePath = filePath
        self.data = None
        if filePath:
            self.load_file(filePath)
        else:
            self.data = self.deafultData()

    # we want to load if we have a file path
    def load_file(self, filePath):
        self.filePath = filePath
        if filePath:
            # Use scheduler loader
            with open(filePath, 'r') as file:
                self.data = json.load(file)

            print(self.data["config"]["rooms"])


    def deafultData(self):
        # deafult data if the file path is empty. 
        # all the defult data will come from a templateFile I created
        # Without other stuff form the config file the scheduler won't run to generate schedules
        with open("template/ConfigTemplate.json", 'r') as file:
            config = json.load(file)
        
        print(config)
        return config
    
    def saveData(self, outPath = None, data = None):
        if data: 
            # updates data with new data
            self.data = data

        #TODO: Not sure where to do this but, need way to save/export to difrent file, 
        # not sure weather to make this here or in the contorler. 

        # writes the file to the given FilePath
        with open(self.filePath , "w") as f:
            json.dump(self.data, f, indent= 4)

    # each method below will get the data from file: 

    def getRooms(self):
        print(f"Data form m: {self.data["config"]["rooms"]}")
        return self.data["config"]["rooms"]
    
    def getLabs(self):
        return self.data["config"]['labs']
    
    def getCourses(self):
        return self.data["config"]["courses"]

    def getFaculty(self):
        return self.data["config"]["faculty"]


    # these methods will add rooms, labs, courses, faculty to the file it self
    def addRoom(self, newRoom):
        self.data["config"]["rooms"].append(newRoom)

        # actally saves the data in file
        self.saveData()
    
    def editRoom(self, oldName, newName):
        rooms = self.data["config"]["rooms"]
        idx = rooms.index(oldName)
        rooms[idx] = newName
        self.saveData()


    def removeRoom(self, roomName):
        rooms = self.data["config"]["rooms"]
        rooms.remove(roomName)
        self.saveData()

    def addLab(self, newLab):
        self.data["config"]["labs"].append(newLab)
        self.saveData()

    def addFaculty(self, newFaculty):
        self.data["config"]["faculty"].append(newFaculty)
        self.saveData()

    def addCourse(self, newCourse):
        self.data["config"]["courses"].append(newCourse)
        self.saveData()

