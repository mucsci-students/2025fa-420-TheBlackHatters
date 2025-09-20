import Faculty_model as faculty

# Gets the days and times the faculty is available
def daysAndTimes():

    # This gets available times for every day of the week
    # ".replace(" ", "")" removes any spaces the user may have accidentally added, just as a quality of life thing
    print("When are they available on Monday? (Leave blank for 9:00-5:00, type \"N/A\" if they are not available)")
    time_available = [input().lower().replace(" ", "")]
    print("When are they available on Tuesday? (Leave blank for 9:00-5:00, type \"N/A\" if they are not available)")
    time_available = time_available + [input().lower().replace(" ", "")]
    print("When are they available on Wednesday? (Leave blank for 9:00-5:00, type \"N/A\" if they are not available)")
    time_available = time_available + [input().lower().replace(" ", "")]
    print("When are they available on Thursday? (Leave blank for 9:00-5:00, type \"N/A\" if they are not available)")
    time_available = time_available + [input().lower().replace(" ", "")]
    print("When are they available on Friday? (Leave blank for 9:00-5:00, type \"N/A\" if they are not available)")
    time_available = time_available + [input().lower().replace(" ", "")]

    # Checks if there are any blank entries in the time_available list
    i = 0
    while i < len(time_available):
        if time_available[i] == "":
            time_available[i] = "9:00-5:00"
        i += 1
    return time_available

# This adds the faculty, just here to make things cleaner in the promptUser method
def addFacultyHelper():
    # Gets faculty name
    print("Enter a faculty name: ")
    faculty_name = input()

    # Something should be added here to check for invalid inputs
    print("Are they full-time or adjunct? (Enter \"full\" or \"adjunct\") (Default: full)")
    full_or_part_time = input().lower().replace(" ", "")

    # Checks if the input is valid, defaults to full if invalid
    if full_or_part_time != "full" and full_or_part_time != "adjunct":
        full_or_part_time = "full"

    # This checks if the faculty is full-time or adjunct, and sets the course limit
    if full_or_part_time == "full":
        unique_course_limit = 2
    else:
        unique_course_limit = 1

    # Calls the function that gets days and times
    time_available = daysAndTimes()

    # Gets the course preferences for faculty, removes anything after the third entry
    # If preferences is empty then it replaces the list with "N/A"
    print("What are their course preferences? (Separate courses with commas, maximum of 3)")
    preferences = input().lower().replace(" ", "").split(',')
    if len(preferences) > 2:
        preferences = preferences[:3]
    if len(preferences) == 0:
        preferences = ["N/A"]


    # Loop for getting course weight
    i = 0
    course_weight = [None] * len(preferences)

    # Error checks if what they inputted is valid and if not it defaults to 3
    while i < len(preferences):
        print("Enter the course weight (1-5) for " + preferences[i] + " (Default is 3):")
        course_weight[i] = input().replace(" ", "")
        try:
            if 1 <= int(course_weight[i]) <= 5:
                course_weight[i] = int(course_weight[i])
            else:
                course_weight[i] = 3
        except ValueError:
            course_weight[i] = 3
        i += 1

    # Gets the courses the faculty member teaches
    # Checks if faculty is adjunct or not, if so remove everything after first entry
    # If courses_taught is empty then it replaces the list with "N/A"
    print("What courses do they teach? (Maximum of 2 for full-time, 1 for adjunct)")
    courses_taught = input().lower().replace(" ", "").split(',')
    if full_or_part_time != "full":
        courses_taught = courses_taught[:1]
    if len(courses_taught) == 0:
        courses_taught = ["N/A"]

    # This creates the new faculty with the info gotten from above
    new_faculty = faculty.Faculty(faculty_name, full_or_part_time, unique_course_limit, time_available, preferences, courses_taught, course_weight)
    return new_faculty
    

# This edits a faculty, just here to make things cleaner in the promptUser method
def editFacultyHelper(faculty_to_edit):
    # Creating the variables used in returned data
    # Get information from file, "None's" are temporary
    faculty_name = None
    full_or_part_time = None
    unique_course_limit = None
    time_available = [None, None, None, None, None]
    preferences = None
    courses_taught = None
    

    # Prompts the user to edit information and asks what information they want to edit
    print("What would you like to edit? Your options are:")
    print("name, full time or adjunct, availability, course preferences, courses taught")
    things_to_edit = input().lower().replace(" ", "").split(',')
    print(things_to_edit)

    # List of if statements that checks the list for what to edit
    # As a QOL addition for the user, the strings below have no spaces between them
    if "name" in things_to_edit:
        print("Enter the new name for this faculty:")
        faculty_name = input()

    # Updates if the faculty is full-time or adjunct
    if "fulltimeoradjunct" in things_to_edit:
        print("Are they full-time or adjunct? (Enter \"full\" or \"adjunct\") (Default: full)")
        full_or_part_time = input().lower().replace(" ", "")

        # Checks if the input is valid, defaults to full if invalid
        if full_or_part_time != "full" and full_or_part_time != "adjunct":
            full_or_part_time = "full"

        # This checks if the faculty is full-time or adjunct, and sets the course limit
        if full_or_part_time == "full":
            unique_course_limit = 2
        else:
            unique_course_limit = 1

    # Calls the daysAndTimes method to update the faculty's availability
    if "availability" in things_to_edit:
        time_available = daysAndTimes()

    # Updates the course preferences
    if "coursepreferences" in things_to_edit:
        print("What are their course preferences? (Separate courses with commas, maximum of 3)")
        preferences = input().lower().replace(" ", "").split(',')
        if len(preferences) > 2:
            preferences = preferences[:3]
        if len(preferences) == 0:
            preferences = ["N/A"]

    # Loop for getting course weight
    i = 0
    course_weight = [None] * len(preferences)

    # Error checks if what they inputted is valid and if not it defaults to 3
    while i < len(preferences):
        print("Enter the course weight (1-5) for " + preferences[i] + " (Default is 3):")
        course_weight[i] = input().replace(" ", "")
        try:
            if 1 <= int(course_weight[i]) <= 5:
                course_weight[i] = int(course_weight[i])
            else:
                course_weight[i] = 3
        except ValueError:
            course_weight[i] = 3
        i += 1

    # Updates the courses taught
    if "coursestaught" in things_to_edit:
        print("What courses do they teach? (Maximum of 2 for full-time, 1 for adjunct)")
        courses_taught = input().lower().replace(" ", "").split(',')

        if full_or_part_time != "full":
            courses_taught = courses_taught[:1]
        if len(courses_taught) == 0:
            courses_taught = ["N/A"]
    
    edited_faculty = faculty.Faculty(faculty_name, full_or_part_time, unique_course_limit, time_available, preferences, courses_taught, course_weight)
    return edited_faculty


def removeFacultyHelper(name_to_remove):
    print("Are you sure you want to delete this faculty? This cannot be undone. (y/n)")
    remove_or_not = input().lower()

    if remove_or_not == "yes" or remove_or_not == "y":
        # The code to remove the faculty member will go here

        print("Faculty has been successfully removed")
    
    # Should find name of faculty in the JSON file and set the data appropriately
    else:       
        print("Removal cancelled")

def promptUser():
    print("What would like to do? Your options are: " \
    "\n Add faculty (Type 1 or add), \n Edit faculty (Type 2 or edit), \n Remove faculty (Type 3 or remove)" \
    "\n Enter your choice here (Case Insensitive): ")

    # This stores the string the user inputted from the prompt above
    action = input()

    # Series of if-else statements that check the response the user gave to the prompt:
    # Adds a faculty
    if action == "1" or action.lower() == "add":
        new_faculty = addFacultyHelper()
        faculty.Faculty.addFaculty(new_faculty)

    # Edits a faculty
    elif action == "2" or action.lower() == "edit":
        print("What is the name of the faculty would you like to edit?")
        faculty_to_edit = input()
        editFacultyHelper(faculty_to_edit)

    # Removes a faculty
    elif action == "3" or action.lower() == "remove":
        print("What is the name of the faculty you want to remove?")
        name_to_remove = input()
        removeFacultyHelper(name_to_remove)

    # If the user enters an invalid input
    else:
        print("Invalid response, please try again \n")
        promptUser()

# Runs initial prompting
promptUser()
