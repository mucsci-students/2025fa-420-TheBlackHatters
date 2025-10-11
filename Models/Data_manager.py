import json
from scheduler import load_config_from_file
from scheduler.config import CombinedConfig
from Models.courses.Course_model import (
    add_course_to_config,
    modify_course_in_config,
    delete_course_from_config
)

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
            #Use scheduler loader
            with open(filePath, 'r') as file:
                self.data = json.load(file)

            # self.data = load_config_from_file(CombinedConfig, self.filePath)
            # print(self.data)



    def deafultData(self):
        # deafult data if the file path is empty. 
        # all the defult data will come from a templateFile I created
        # Without other stuff form the config file the scheduler won't run to generate schedules
        with open("template/ConfigTemplate.json", 'r') as file:
            config = json.load(file)
        # config = load_config_from_file(CombinedConfig, "template/ConfigTemplate.json")
        return config

    def saveData(self, path=None):
        """Save data to the current or given path."""
        if path is None:
            path = self.filePath
        if not path:
            print("No path specified for saveData()")
            return
        with open(path, "w") as f:
            json.dump(self.data, f, indent=4)

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
        """Return the list of all courses."""
        return self.data["config"].get("courses", [])

    def addCourse(self, course_dict):
        """
        Add a validated course to the config.
        course_dict = {
            "course_id": "CMSC 101",
            "credits": 4,
            "room": ["Roddy 136"],
            "lab": ["Linux Lab"],
            "conflicts": ["CMSC 140"],
            "faculty": ["Zoppetti"]
        }
        """
        config_obj = self.data["config"]
        add_course_to_config(config_obj, course_dict, strict_membership=True)
        print(f"Added course: {course_dict['course_id']}")

    def editCourse(self, old_course_id, updates):
        """
        Edit a course using its existing course_id.
        updates = {
            "course_id": "CMSC 102",
            "credits": 3,
            "room": ["Roddy 120"]
        }
        """
        config_obj = self.data["config"]
        modify_course_in_config(config_obj, old_course_id, updates=updates, strict_membership=True)
        print(f"✏️ Updated course: {old_course_id} → {updates.get('course_id', old_course_id)}")

    def removeCourse(self, course):
        """Delete a course from config."""
        cfg = self.data.get("config", {})
        try:
            # Handle both dict and string inputs safely
            if isinstance(course, dict):
                course_id = course.get("course_id")
            else:
                course_id = str(course)

            deleted = delete_course_from_config(cfg, course_id)
            self.data["config"] = cfg
            #self.saveData()
            print(f"Removed course: {course_id}")
            return deleted
        except ValueError as e:
            print(f"Failed to remove course: {e}")
            raise

    # Faculty CRUD
    def getFaculty(self):
        return self.data["config"]["faculty"]

    def addFaculty(self, newFaculty):
        self.data["config"]["faculty"].append(newFaculty)
        #self.saveData(outPath = self.filePath)



