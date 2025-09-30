# File Name: Faculty_model.py

# Author: Liam Delaney, Nicholas DiPace
# Last Modified: September 29, 2025

class Faculty:

    faculty_name = None
    maximum_credits = None
    minimum_credits = None
    unique_course_limit = None
    time_available = [None, None, None, None, None]
    course_preferences = {None}
    room_preferences = None
    lab_preferences = None
    
    

    # Constructor
    def __init__(self, faculty_name, maximum_credits, minimum_credits, unique_course_limit, time_available, course_preferences, room_preferences, lab_preferences):
        #init, faculty should be a list of faculty objects.
        self.name = faculty_name
        self.maximum_credits = maximum_credits
        self.minimum_credits = minimum_credits
        self.unique_course_limit = unique_course_limit
        self.times = time_available
        self.course_preferences = course_preferences
        self.room_preferences = room_preferences
        self.lab_preferences = lab_preferences
        
        

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


    # Prints a list of all current faculty entries.
    def viewFaculty(self):
        for entry in self:
            print(entry,"\n")


    # Adds the faculty to the JSON file by taking in the data of a faculty member
    # Assumes checks are already done.
    def addFaculty(self, new_faculty):
        self.append(new_faculty)        


    # Finds a faculty based on their name and deletes them from the JSON file.
    # Faculty is a list of faculty, so we iterate through to find the index for deletion.
    def removeFaculty(self, faculty_name):
        i=0
        for entry in self:
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
