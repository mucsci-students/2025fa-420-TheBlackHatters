class Faculty:

    faculty_name = None
    full_or_part_time = None
    unique_course_limit = None
    time_available = [None, None, None, None, None]
    preferences = None
    courses_taught = None
    course_weight = []

    # Constructor
    def __init__(self, faculty_name, full_or_part_time, unique_course_limit, time_available, preferences, courses_taught, course_weight):
        #init, faculty should be a list of faculty objects.
        self.name = faculty_name
        self.full_or_part_time = full_or_part_time
        self.unique_course_limit = unique_course_limit
        self.times = time_available
        self.course_preferences = preferences  
        self.courses = courses_taught
        self.course_weight = course_weight

    def __str__(self):
        return f"Faculty in the system: {self.faculty}."

    # Checks if the provided name of a faculty member already exists in the JSON file.
    # Returns true if found, otherwise false.
    def facCheck(self, name):
        i=0
        for entry in self:
            subFaculty = self[i].get('name')
            if name in subFaculty:
                return True
            else:
                i=i+1
        return False


    # Adds the faculty to the JSON file by taking in the data of a faculty member
    def viewFaculty(self, faculty_data):
        return f"Faculty in the System: {self.faculty}"


    # Adds the faculty to the JSON file by taking in the data of a faculty member
    # Assumes checks are already done.
    def addFaculty(self, new_faculty):
        self.append(new_faculty)        


    # Finds a faculty based on their name and deletes them from the JSON file.
    # Faculty is a list of faculty, so we iterate through to find the index for deletion.
    def removeFaculty(self, faculty_name):
        i=0
        for entry in Faculty:
            # Specifically stores the 'name' section of the faculty list entry.
            subFaculty = self[i].get('name')
            # Checks if the name to be deleted is in that entry.
            if faculty_name in subFaculty:
                # If so, deletes that index.
                rem = self[i]
                del self[i]
                return rem
            else:
                # otherwise, iterate and back to the top of loop.
                i=i+1
