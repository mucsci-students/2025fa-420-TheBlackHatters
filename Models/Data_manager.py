import json
import Models.Faculty_model as FacultyModel

# This will manage all of the data for the whole config file.

from Models.Course_model import (
    add_course_to_config,
    delete_course_from_config,
)


# We will need to give a config filePath or it will start will an empty file
# note: empty file only inclues,
class DataManager:
    def __init__(self, filePath=None):
        self.new = True
        self.filePath = filePath
        self.data = None
        if filePath:
            self.loadFile(filePath)
        else:
            self.data = self.deafultData()

    @staticmethod
    def requireData(func):
        # Creating a decorateor so i dont have to write if else to make ruff check happy :)
        def wrapper(self, *args, **kwargs):
            if self.data is None:
                raise ValueError(f"Cannot call '{func.__name__}' — data is not loaded.")
            return func(self, *args, **kwargs)

        return wrapper

    # we want to load if we have a file path
    def loadFile(self, filePath):
        self.filePath = filePath
        if filePath:
            # Use scheduler loader
            with open(filePath, "r") as file:
                self.data = json.load(file)

            # self.data = load_config_from_file(CombinedConfig, self.filePath)
            # print(self.data)

    def deafultData(self):
        # deafult data if the file path is empty.
        # all the defult data will come from a templateFile I created
        # Without other stuff form the config file the scheduler won't run to generate schedules
        with open("template/ConfigTemplate.json", "r") as file:
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

    @requireData
    def updateLimit(self, limit):
        self.data["limit"] = limit

    @requireData
    def updateOptimizerFlags(self, flags):
        self.data["optimizer_flags"] = flags

    # each method below will get the data from file:
    # Rooms CRUD(Create, Read, Update, Delete)
    @requireData
    def getRooms(self):
        return self.data["config"]["rooms"]

    @requireData
    def addRoom(self, newRoom):
        self.data["config"]["rooms"].append(newRoom)
        # actally saves the data in file
        # self.saveData(outPath = self.filePath)

    @requireData
    def editRoom(self, oldName, newName):
        rooms = self.data["config"]["rooms"]
        idx = rooms.index(oldName)
        rooms[idx] = newName
        # self.saveData(outPath = self.filePath)

    @requireData
    def removeRoom(self, roomName):
        # Prevent removing a room that's in use by any course
        courses = self.data["config"].get("courses", [])
        for course in courses:
            if roomName in course.get("room", []):
                raise ValueError(
                    f"Cannot remove room '{roomName}' as it is used by course '{course['course_id']}'"
                )

        rooms = self.data["config"]["rooms"]
        rooms.remove(roomName)
        # self.saveData(outPath = self.filePath)

    # Labs CRUD
    @requireData
    def getLabs(self):
        return self.data["config"]["labs"]

    @requireData
    def addLab(self, newLab):
        self.data["config"]["labs"].append(newLab)
        # self.saveData(outPath = self.filePath)

    @requireData
    def editLabs(self, oldName, newName):
        labs = self.data["config"]["labs"]
        idx = labs.index(oldName)
        labs[idx] = newName
        # self.saveData(outPath = self.filePath)

    @requireData
    def removeLabs(self, labName):
        # Prevent removing a lab that's in use by any course
        courses = self.data["config"].get("courses", [])
        for course in courses:
            if labName in course.get("lab", []):
                raise ValueError(
                    f"Cannot remove lab '{labName}' as it is used by course '{course['course_id']}'"
                )

        labs = self.data["config"]["labs"]
        labs.remove(labName)
        # self.saveData(outPath = self.filePath)

    # Course CRUD
    @requireData
    def getCourses(self):
        """Return the list of all valid courses, auto-cleaning invalid references."""
        self._clean_invalid_references()
        return self.data["config"].get("courses", [])

    @requireData
    def addCourse(self, course_dict):
        config_obj = self.data["config"]
        try:
            # Allow forward references / circular conflicts when adding courses
            add_course_to_config(config_obj, course_dict, strict_membership=False)
            print(f"Added course: {course_dict['course_id']}")
        except Exception as e:
            raise ValueError(str(e))

    @requireData
    def editCourse(self, old_course_id, updates, target_index=None):
        config_obj = self.data["config"]

        try:
            courses = config_obj.get("courses", [])
            matching = [c for c in courses if c.get("course_id") == old_course_id]
            if not matching:
                raise ValueError(f"Course not found: {old_course_id}")

            idx = (
                target_index if target_index is not None else courses.index(matching[0])
            )
            current = courses[idx]

            # Merge updates into a fresh dict
            new_data = current.copy()
            new_data.update(updates)

            from Models.Course_model import Course

            candidate = Course.from_dict(new_data)

            candidate.validate(
                config_obj=config_obj,
                existing_courses=courses,
                strict_membership=True,
                ignore_index=idx,
            )

            # Replace course only if validation passes
            courses[idx] = candidate.to_dict()

            # Cascade rename: update any conflicts that referenced the old id
            if old_course_id != candidate.course_id:
                for course in courses:
                    if "conflicts" in course and old_course_id in course["conflicts"]:
                        # replace occurrences of old id with the new id
                        course["conflicts"] = [
                            candidate.course_id if x == old_course_id else x
                            for x in course.get("conflicts", [])
                        ]

            print(f"Updated course: {old_course_id} → {candidate.course_id}")

        except Exception as e:
            raise ValueError(str(e))

    @requireData
    def removeCourse(self, course):
        cfg = self.data.get("config", {})
        try:
            if isinstance(course, dict):
                course_id = course.get("course_id")
            else:
                course_id = str(course)

            deleted = delete_course_from_config(cfg, course_id)
            self.data["config"] = cfg
            print(f"Removed course: {course_id}")
            return deleted
        except Exception as e:
            raise ValueError(str(e))

    @requireData
    def _clean_invalid_references(self):
        """
        Cleans all invalid references in course lists:
          - Removes missing rooms, labs, faculty, and conflicts.
        Returns True if any data was changed.
        """
        config = self.data.get("config", {})
        courses = config.get("courses", [])

        existing_rooms = set(config.get("rooms", []))
        existing_labs = set(config.get("labs", []))
        existing_courses = {c.get("course_id") for c in courses if "course_id" in c}
        existing_faculty = {
            f["name"] if isinstance(f, dict) and "name" in f else str(f)
            for f in config.get("faculty", [])
        }

        changed = False

        for c in courses:
            # Rooms
            if "room" in c:
                valid_rooms = [r for r in c["room"] if r in existing_rooms]
                if len(valid_rooms) != len(c["room"]):
                    c["room"] = valid_rooms
                    changed = True

            # Labs
            if "lab" in c:
                valid_labs = [labs for labs in c["lab"] if labs in existing_labs]
                if len(valid_labs) != len(c["lab"]):
                    c["lab"] = valid_labs
                    changed = True

            # Conflicts
            if "conflicts" in c:
                valid_conflicts = [
                    conf for conf in c["conflicts"] if conf in existing_courses
                ]
                if len(valid_conflicts) != len(c["conflicts"]):
                    c["conflicts"] = valid_conflicts
                    changed = True

            # Faculty
            if "faculty" in c:
                valid_faculty = [f for f in c["faculty"] if f in existing_faculty]
                if len(valid_faculty) != len(c["faculty"]):
                    c["faculty"] = valid_faculty
                    changed = True

        return changed

    # Faculty CRUD
    @requireData
    def getFaculty(self):
        return self.data["config"]["faculty"]

    @requireData
    def getFacultyByName(self, name: str):
        """Return a single faculty entry by name (case-insensitive), or None if not found."""
        faculty_list = self.data.get("config", {}).get("faculty", [])
        if not name or not isinstance(name, str):
            return None

        name_lower = name.strip().lower()
        for f in faculty_list:
            if isinstance(f, dict) and f.get("name", "").lower() == name_lower:
                return f
        return None

    @requireData
    def addFaculty(self, newFaculty):
        conFaculty = self.data["config"]["faculty"]
        FacultyModel.Faculty.addFaculty(conFaculty, newFaculty)
        # self.saveData(outPath = self.filePath)

    @requireData
    def removeFaculty(self, facName):
        # Prevent removing faculty that's assigned to any course
        courses = self.data["config"].get("courses", [])
        for course in courses:
            if facName in course.get("faculty", []):
                raise ValueError(
                    f"Cannot remove faculty '{facName}' as they are teaching course '{course['course_id']}'"
                )

        conFaculty = self.data["config"]["faculty"]
        result = FacultyModel.Faculty.removeFaculty(conFaculty, facName)
        if result is None:
            raise ValueError(f"Faculty member '{facName}' not found")
        # self.saveData(outPath = self.filePath)
