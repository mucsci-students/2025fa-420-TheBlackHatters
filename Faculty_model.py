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
        self.faculty_name = faculty_name
        self.full_or_part_time = full_or_part_time
        self.unique_course_limit = unique_course_limit
        self.time_available = time_available
        self.preferences = preferences
        self.courses_taught = courses_taught
        self.course_weight = course_weight

    # Adds the faculty to the JSON file by taking in the data of a faculty member
    def addFaculty(faculty_data):
        print("TODO")
    
    # Finds a faculty based on their name and edits their JSON file data
    def editFaculty(faculty_name):

        #Should find the faculty in the JSON file and replace them
        print("TODO")

    # Finds a faculty based on their name and deletes them from the JSON file
    def removeFaculty(faculty_name):
        print("TODO")