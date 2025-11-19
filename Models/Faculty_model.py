# File Name: Faculty_model.py

# Author: Liam Delaney, Nicholas DiPace
# Last Modified: November 11, 2025


class Faculty(list):
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
        super().__init__()  # initialize list parent
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

    # -------------------------------
    # Static helper methods for lists
    # -------------------------------

    @staticmethod
    def facCheck(faculty_list, name):
        """Check if any faculty entry contains the given name substring."""
        i = 0
        for entry in faculty_list:
            subFaculty = entry.get("name") if isinstance(entry, dict) else None
            if subFaculty is None:
                i += 1
                continue
            # only perform substring check for string types
            try:
                if name in subFaculty:
                    return True
            except TypeError:
                # name or subFaculty not iterable/compatible — skip this entry
                pass
            i += 1
        return False

    @staticmethod
    def viewFaculty(faculty_list):
        """Print all faculty entries, each followed by a blank line."""
        for entry in faculty_list:
            print(entry)
            print()

    @staticmethod
    def addFaculty(faculty_list, new_faculty):
        """Append a new faculty entry to the list."""
        faculty_list.append(new_faculty)

    @staticmethod
    def removeFaculty(faculty_list, faculty_name):
        """Remove and return the first matching faculty entry by name substring."""
        i = 0
        for entry in faculty_list:
            subFaculty = entry.get("name") if isinstance(entry, dict) else None
            if subFaculty is None:
                i += 1
                continue
            try:
                if faculty_name in subFaculty:
                    rem = faculty_list[i]
                    del faculty_list[i]
                    return rem
            except TypeError:
                # faculty_name or subFaculty not iterable/compatible — skip this entry
                pass
            i += 1
        return None
