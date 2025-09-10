import json

# Creates a faculty
def createFaculty():
    # Gets faculty name
    print("Enter a faculty name: ")
    faculty_name = input()

    # Something should be added here to check for invalid inputs
    print("Are they full-time or adjunct? (Enter \"full\" or \"adjunct\")")
    full_or_part_time = input().lower()

    # This checks if the faculty is full-time or adjunct, and sets the course limit
    if full_or_part_time == "full":
        unique_course_limit = 2
    else:
        unique_course_limit = 1

    # This gets available times for every day of the week
    # Add error checking
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

    # Gets the course preferences for faculty, removes anything after the third entry
    # If preferences is empty then it replaces the list with "N/A"
    print("What are their course preferences? (Separate courses with commas, maximum of 3)")
    preferences = [input().lower().replace(" ", "")]
    if len(preferences) > 2:
        preferences = preferences[:3]
    if len(preferences) == 0:
        preferences = ["N/A"]

    # Gets the courses the faculty member teaches
    # Checks if faculty is adjunct or not, if so remove everything after first entry
    # If courses_taught is empty then it replaces the list with "N/A"
    print("What courses do they teach? (Maximum of 2 for full-time, 1 for adjunct)")
    courses_taught = [input().lower().replace(" ", "")]
    if full_or_part_time != "full":
        courses_taught = courses_taught[:1]
    if len(courses_taught) == 0:
        courses_taught = ["N/A"]

    # Not sure what 'weight' is supposed to make me do
    
    # This is the data that will be passed into the json file
    data = {
        "name": faculty_name,
        "full-time/adjunct": full_or_part_time,
        "unique course limit": unique_course_limit,
        "available days/times": {
            "Monday": time_available[0],
            "Tuesday": time_available[1],
            "Wednesday": time_available[2],
            "Thursday": time_available[3],
            "Friday": time_available[4]
        },
        "course preferences": preferences,
        "course(s) taught": courses_taught
    }
    print(data)
    return data


# Add a new faculty / modify an existing faculty / delete a faculty
# Name
# Full-time (12 credits) or Adjunct (0-4 credits)
# Unique course limit (2 for full-time, 1 for adjunct)
# Times
# Default time range of 9-5
# Specify a day
# Preferences
# Specify a course (need not exist yet)
# Specify a weight


# Edits information of a faculty
def editFaculty():
    print("This is where the user can edit a faculty's information")
    
# Removes a faculty
def removeFaculty():
    print("This is where the user can remove a faculty")

# This is the initial prompt asking the user what action they want to take
def promptUser():
    print("What would like to do? Your options are: " \
    "\n Add faculty (Type 1 or add), \n Edit faculty (Type 2 or edit), \n Remove faculty (Type 3 or remove)" \
    "\n Enter your choice here (Case Insensitive): ")

    # This stores the string the user inputted from the prompt above
    action = input()

    # Series of if-else statements that check the response the user gave to the prompt
    if action == "1" or action.lower() == "add":
        new_faculty = createFaculty()
        # writeFile(new_faculty)
        print('\033[32mFaculty created successfully.\033[0m')
    elif action == "2" or action.lower() == "edit":
        editFaculty()
    elif action == "3" or action.lower() == "remove":
        removeFaculty()
    else:
        print("Invalid response, please try again \n")
        promptUser()

# Runs the initial prompting
promptUser()

# Writes the file
# def writeFile(data):
#     with open("output.json", "w") as json_file:
#         json.dump(data, json_file)