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
    def __init__(
        self,
        faculty_name,
        maximum_credits,
        minimum_credits,
        unique_course_limit,
        time_available,
        course_preferences,
        room_preferences,
        lab_preferences,
    ):
        # init, faculty should be a list of faculty objects.
        self.name = faculty_name
        self.maximum_credits = maximum_credits
        self.minimum_credits = minimum_credits
        self.unique_course_limit = unique_course_limit
        self.times = time_available
        self.course_preferences = course_preferences
        self.room_preferences = room_preferences
        self.lab_preferences = lab_preferences

    def __str__(self):
        # Defensive stringification: use getattr with defaults to avoid AttributeError
        name = getattr(self, "name", None)
        min_cr = getattr(self, "minimum_credits", None)
        max_cr = getattr(self, "maximum_credits", None)
        course_limit = getattr(self, "unique_course_limit", None)
        times = getattr(self, "times", None)
        course_prefs = getattr(self, "course_preferences", None)
        room_prefs = getattr(self, "room_preferences", None)
        lab_prefs = getattr(self, "lab_preferences", None)

        return (
            f"Faculty member: {name}\n"
            f"Credits: {min_cr}-{max_cr}\n"
            f"Course Limit: {course_limit}\n"
            f"Times Available: {times}\n"
            f"Course Preferences: {course_prefs}\n"
            f"Room Preferences: {room_prefs}\n"
            f"Lab Preferences: {lab_prefs}"
        )

    # Checks if the provided name of a faculty member already exists in the JSON file.
    # Returns true if found, otherwise false.
    def facCheck(self, name):
        i = 0
        for entry in self:
            # guard against entries without 'name' or with None
            subFaculty = self[i].get("name") if isinstance(self[i], dict) else None
            if subFaculty is None:
                i = i + 1
                continue
            # only perform substring check for string types
            try:
                if name in subFaculty:
                    return True
            except TypeError:
                # name or subFaculty not iterable/compatible — skip this entry
                pass
            i = i + 1
        return False

    # Prints a list of all current faculty entries.
    def viewFaculty(self):
        for entry in self:
            # print each entry followed by a blank line (match existing tests expecting "\n\n")
            print(entry)
            print()

    # Adds the faculty to the JSON file by taking in the data of a faculty member
    # Assumes checks are already done.
    def addFaculty(self, new_faculty):
        self.append(new_faculty)

    # Finds a faculty based on their name and deletes them from the JSON file.
    # Faculty is a list of faculty, so we iterate through to find the index for deletion.
    def removeFaculty(self, faculty_name):
        i = 0
        for entry in self:
            # Specifically stores the 'name' section of the faculty list entry.
            subFaculty = self[i].get("name") if isinstance(self[i], dict) else None
            # If there's no name on this entry, skip it
            if subFaculty is None:
                i = i + 1
                continue
            try:
                if faculty_name in subFaculty:
                    rem = self[i]
                    del self[i]
                    return rem
            except TypeError:
                # faculty_name or subFaculty not iterable/compatible — skip this entry
                pass
            i = i + 1
        # If we get here, faculty wasn't found
        return None  # Return None when faculty is not found
