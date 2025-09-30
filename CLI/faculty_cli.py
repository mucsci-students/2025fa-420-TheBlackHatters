# File Name: faculty_cli.py

# Author: Liam Delaney, Nicholas DiPace
# Last Modified: September 29, 2025

import Models.Faculty_model as FacultyModel

# Gets the days and times the faculty is available
def daysAndTimes():

    # This gets available times for every day of the week
    # ".replace(" ", "")" removes any spaces the user may have accidentally added, just as a quality of life thing
    print("\033[31mNOTE: For the following prompts, if a faculty is available two or more different times in one day,\033[0m")
    print("\033[31mseparate the times by commas:\033[0m")
    #print("")

    days = ["MON", "TUE", "WED", "THU", "FRI"]
    availability = {}

    for day in days:
        print(f"When are they available on {day}? (Leave blank for 9:00-5:00, type \"N/A\" if they are not available)")
        time_input = input().lower().replace(" ", "")
        
        if time_input == "":
            time_input = "9:00-5:00"
            availability[day] = [time_input]
        else:
            time_input = time_input.split(",")  

            availability[day] = time_input

    return availability

# Prints a list of all current faculty entries.
def viewFacultyCLI(Faculty):
    FacultyModel.Faculty.viewFaculty(Faculty)

# This adds the faculty, just here to make things cleaner in the promptUser method
def addFacultyCLI(Faculty):
    # Gets faculty name
    print("Enter the faculty's name: ")
    faculty_name = input()

    # Checks for blank input:
    if faculty_name.replace(" ", "") == "":
        print("You entered a blank name!")
        return
    if faculty_name.replace(" ", "").lower() == "killian":
        print("Hello Client!")

    #Checks if faculty is already in system.
    if FacultyModel.Faculty.facCheck(Faculty, faculty_name)==True:
        print("Faculty is already in system!")
        return
    
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

    # Gets the maximum teachable credits for a faculty member
    if full_or_part_time == "full":
        max_teachable_credits = 12
    else:
        max_teachable_credits = 4

    # Gets the minimum credits the faculty can teach
    print("Enter the minimum credits a faculty can teach per semester (Default is 0):")
    min_credits = input()
    try:
        if int(min_credits) < 0 or int(min_credits) > int(max_teachable_credits):
            min_credits = 0
    except ValueError:
        min_credits = 0
    
    # Gets the maximum credits the faculty can teach
    print("Enter the maximum credits a faculty can teach per semester (Default is " + str(max_teachable_credits) + "):")
    max_credits = input()
    try:
        if int(max_credits) > max_teachable_credits or int(max_credits) < int(min_credits):
            max_credits = max_teachable_credits
    except ValueError:
        max_credits = max_teachable_credits

    #credit_range = str(min_credits) + "-" + str(max_credits)

    # Calls the function that gets days and times
    time_available = daysAndTimes()

    # Gets the course preferences for faculty, removes anything after the third entry
    # If preferences is empty then it replaces the list with "N/A"
    print("What are their course preferences? (Separate courses with commas, maximum of 3)")
    course_preferences = list(filter(None, input().lower().replace(" ", "").split(',')))
    if len(course_preferences) > 2:
        course_preferences = course_preferences[:3]
    if len(course_preferences) == 0:
        course_weight = "N/A"

    if len(course_preferences) > 0:
        # Loop for getting course weight
        i = 0
        course_weight = [None] * len(course_preferences)
        course_result = []

        # Error checks if what they inputted is valid and if not it defaults to 5
        while i < len(course_preferences):
            print("Enter the course weight (0-10) for " + str(course_preferences[i]) + " (Default is 5, 0 means no preference):")
            course_weight[i] = input().replace(" ", "")
            try:
                if 0 <= int(course_weight[i]) <= 10:
                    course_weight[i] = int(course_weight[i])
                else:
                    course_weight[i] = 5
            except ValueError:
                course_weight[i] = 5

            course_result.extend([course_preferences[i], course_weight[i]])
            i += 1
        course_preferences = {course_result[i]: course_result[i + 1] for i in range(0, len(course_result), 2)}

        

    # Gets the faculty room preferences
    print("What are their room preferences? (Separate courses with commas, maximum of 3)")
    room_preferences = list(filter(None, input().lower().replace(" ", "").split(',')))
    if len(room_preferences) > 2:
        room_preferences = room_preferences[:3]
    if len(room_preferences) == 0:
        room_weight = "N/A"

    if len(room_preferences) > 0:
        # Loop for getting room weight
        i = 0
        room_weight = [None] * len(room_preferences)
        room_result = []

        # Error checks if what they inputted is valid and if not it defaults to 5
        while i < len(room_preferences):
            print("Enter the room weight (0-10) for " + str(room_preferences[i]) + " (Default is 5, 0 means no preference):")
            room_weight[i] = input().replace(" ", "")
            try:
                if 0 <= int(room_weight[i]) <= 10:
                    room_weight[i] = int(room_weight[i])
                else:
                    room_weight[i] = 5
            except ValueError:
                room_weight[i] = 5

            room_result.extend([room_preferences[i], room_weight[i]])
            i += 1
        room_preferences = {room_result[i]: room_result[i + 1] for i in range(0, len(room_result), 2)}

    # Gets the faculty lab preferences
    print("What are their lab preferences? (Separate courses with commas, maximum of 3)")
    lab_preferences = list(filter(None, input().lower().replace(" ", "").split(',')))
    if len(lab_preferences) > 2:
        lab_preferences = lab_preferences[:3]
    if len(lab_preferences) == 0:
        lab_weight = "N/A"

    if len(lab_preferences) > 0:
        # Loop for getting lab weight
        i = 0
        lab_weight = [None] * len(lab_preferences)
        lab_result = []

        # Error checks if what they inputted is valid and if not it defaults to 5
        while i < len(lab_preferences):
            print("Enter the lab weight (0-10) for " + str(lab_preferences[i]) + " (Default is 5, 0 means no preference):")
            lab_weight[i] = input().replace(" ", "")
            try:
                if 0 <= int(lab_weight[i]) <= 10:
                    lab_weight[i] = int(lab_weight[i])
                else:
                    lab_weight[i] = 5
            except ValueError:
                lab_weight[i] = 5

            lab_result.extend([lab_preferences[i], lab_weight[i]])
            i += 1
        lab_preferences = {lab_result[i]: lab_result[i + 1] for i in range(0, len(lab_result), 2)}
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
    new_faculty = {"name":faculty_name, "maximum_credits":max_credits, "minimum_credits":min_credits, "unique_course_limit":unique_course_limit, "times":time_available, "course_preferences":course_preferences, "room_preferences":room_preferences, "lab_preferences":lab_preferences}
    #Checks if the faculty being added already exists in the Config, proceed if not found, stop otherwise.
    # print(new_faculty)
    FacultyModel.Faculty.addFaculty(Faculty, new_faculty)
    print("Faculty added.")
    

# This edits a faculty, just here to make things cleaner in the promptUser method
def editFacultyCLI(Faculty):
    # Begins here, prompts the user
    print("What is the name of the faculty would you like to edit?")
    faculty_to_edit = input()
    if faculty_to_edit.replace(" ", "") == "":
        print("Error! You entered nothing!")
        return
    # Checks if the faculty is in the system.
    if FacultyModel.Faculty.facCheck(Faculty, faculty_to_edit)==False:
        print("Faculty does not exist!")
        return
    else:
        #Removes the previous version of the faculty from the system and stores it in this object.
        previous_faculty = FacultyModel.Faculty.removeFaculty(Faculty, faculty_to_edit)

        # Creating the variables used in returned data
        # Get information from the previous faculty
        faculty_name = previous_faculty.get('name')
        unique_course_limit = previous_faculty.get('unique course limit')
        max_credits = previous_faculty.get('max_credits')
        min_credits = previous_faculty.get('min_credits')
        time_available = previous_faculty.get('available days/times')
        course_preferences = previous_faculty.get('course_preferences')
        room_preferences = previous_faculty.get('room_preferences')
        lab_preferences = previous_faculty.get('lab_preferences')

        # Prompts the user to edit information and asks what information they want to edit
        print("What would you like to edit? Your options are:")
        print("name, availability, course preferences, credits, \nroom preferences, lab preferences (separate choices with commas)")
        things_to_edit = input().lower().replace(" ", "").split(',')
        #print(things_to_edit)

        # List of if statements that checks the list for what to edit
        # As a QOL addition for the user, the strings below have no spaces between them
        if "name" in things_to_edit:
            print("Enter the new name for this faculty:")
            faculty_name = input()

        # # Updates if the faculty is full-time or adjunct
        # if "fulltimeoradjunct" in things_to_edit:
        #     print("Are they full-time or adjunct? (Enter \"full\" or \"adjunct\") (Default: full)")
        #     response = input().lower().replace(" ", "")

        #     # Checks if the input is valid, defaults to full if invalid
        #     if response != "full" and full_or_part_time != "adjunct":
        #         full_or_part_time = "full"

        #     # This checks if the faculty is full-time or adjunct, and sets the course limit
        #     if full_or_part_time == "full":
        #         unique_course_limit = 2
        #     else:
        #         unique_course_limit = 1

        # Calls the daysAndTimes method to update the faculty's availability
        if "availability" in things_to_edit:
            time_available = daysAndTimes()

        if "credits" in things_to_edit:
            print("Are they full-time or adjunct? (Enter \"full\" or \"adjunct\") (Default: full)")
            response = input().lower().replace(" ", "")
            if response == "full" or response == "":
                max_teachable_credits = 12
            else:
                max_teachable_credits = 4

            if max_teachable_credits == 12:
                unique_course_limit = 2
            else:
                unique_course_limit = 1
            # Gets the minimum credits the faculty can teach
            print("Enter the minimum credits a faculty can teach per semester (default is 0):")
            minimum_credits = input()
            try:
                if int(minimum_credits) < 0 or int(minimum_credits) > int(max_teachable_credits):
                    minimum_credits = 0
            except ValueError:
                minimum_credits = 0
    
            # Gets the maximum credits the faculty can teach
            print("Enter the maximum credits a faculty can teach per semester (default is " + str(max_teachable_credits) + "):")
            maximum_credits = input()
            try:
                if int(maximum_credits) > max_teachable_credits or int(maximum_credits) < int(maximum_credits):
                    maximum_credits = max_teachable_credits
            except ValueError:
                maximum_credits = max_teachable_credits
            
            #credit_range = str(min_credits) + "-" + str(max_credits)

        # Updates the course preferences
        # NOTE: temp_preferences is a temporary variable to store the actual list of preferences for conditional checking, 
        # and is not returned
        if "coursepreferences" in things_to_edit:
            print("What are their course preferences? (Separate courses with commas, maximum of 3)")
            course_preferences = list(filter(None, input().lower().replace(" ", "").split(',')))
            if len(course_preferences) > 2:
                course_preferences = course_preferences[:3]
            if len(course_preferences) == 0:
                course_preferences = previous_faculty.get('course_preferences')

            elif len(course_preferences) > 0:
                # Loop for getting course weight
                i = 0
                course_weight = [None] * len(course_preferences)
                course_result = []

                # Error checks if what they inputted is valid and if not it defaults to 5
                while i < len(course_preferences):
                    print("Enter the course weight (0-10) for " + str(course_preferences[i]) + " (Default is 5, 0 means no preference):")
                    course_weight[i] = input().replace(" ", "")
                    try:
                        if 0 <= int(course_weight[i]) <= 10:
                            course_weight[i] = int(course_weight[i])
                        else:
                            course_weight[i] = 5
                    except ValueError:
                        course_weight[i] = 5

                    course_result.extend([course_preferences[i], course_weight[i]])
                    i += 1
                course_preferences = {course_result[i]: course_result[i + 1] for i in range(0, len(course_result), 2)}
        
        if "roompreferences" in things_to_edit:
            print("What are their room preferences? (Separate courses with commas, maximum of 3)")
            room_preferences = list(filter(None, input().lower().replace(" ", "").split(',')))
            if len(room_preferences) > 2:
                room_preferences = room_preferences[:3]
            if len(room_preferences) == 0:
                room_preferences = previous_faculty.get('room_preferences')

            elif len(room_preferences) > 0:
                # Loop for getting room weight
                i = 0
                room_weight = [None] * len(room_preferences)
                room_result = []

                # Error checks if what they inputted is valid and if not it defaults to 5
                while i < len(room_preferences):
                    print("Enter the room weight (0-10) for " + str(room_preferences[i]) + " (Default is 5, 0 means no preference):")
                    room_weight[i] = input().replace(" ", "")
                    try:
                        if 0 <= int(room_weight[i]) <= 10:
                            room_weight[i] = int(room_weight[i])
                        else:
                            room_weight[i] = 5
                    except ValueError:
                        room_weight[i] = 5

                    room_result.extend([room_preferences[i], room_weight[i]])
                    i += 1
                room_preferences = {room_result[i]: room_result[i + 1] for i in range(0, len(room_result), 2)}

        if "labpreferences" in things_to_edit:
            print("What are their lab preferences? (Separate courses with commas, maximum of 3)")
            lab_preferences = list(filter(None, input().lower().replace(" ", "").split(',')))
            if len(lab_preferences) > 2:
                lab_preferences = lab_preferences[:3]
            if len(lab_preferences) == 0:
                lab_preferences = previous_faculty.get('lab_preferences')
            elif len(lab_preferences) > 0:
                # Loop for getting lab weight
                i = 0
                lab_weight = [None] * len(lab_preferences)
                lab_result = []

                # Error checks if what they inputted is valid and if not it defaults to 5
                while i < len(lab_preferences):
                    print("Enter the lab weight (0-10) for " + str(lab_preferences[i]) + " (Default is 5, 0 means no preference):")
                    lab_weight[i] = input().replace(" ", "")
                    try:
                        if 0 <= int(lab_weight[i]) <= 10:
                            lab_weight[i] = int(lab_weight[i])
                        else:
                            lab_weight[i] = 5
                    except ValueError:
                        lab_weight[i] = 5

                    lab_result.extend([lab_preferences[i], lab_weight[i]])
                    i += 1
                lab_preferences = {lab_result[i]: lab_result[i + 1] for i in range(0, len(lab_result), 2)}
        # Updates the courses taught
        # if "coursestaught" in things_to_edit:
        #     print("What courses do they teach? (Maximum of 2 for full-time, 1 for adjunct)")
        #     courses_taught = input().lower().replace(" ", "").split(',')

        #     if full_or_part_time != "full":
        #         courses_taught = courses_taught[:1]
        #     if len(courses_taught) == 0:
        #         courses_taught = ["N/A"]

        edited_faculty = {"name":faculty_name, "maximum_credits":maximum_credits, "minimum_credits":minimum_credits, "unique_course_limit":unique_course_limit, "times":time_available, "course_preferences":course_preferences, "room_preferences":room_preferences, "lab_preferences":lab_preferences}
        FacultyModel.Faculty.addFaculty(Faculty, edited_faculty)


# Determines which Faculty to remove and calls the Model to remove them.
def removeFacultyCLI(Faculty):
    print("What is the name of the faculty you want to remove?")
    name_to_remove = input()
    
    if FacultyModel.Faculty.facCheck(Faculty, name_to_remove)==False or name_to_remove.replace(" ", "") == "":
        print("Faculty does not exist!")
        return
    else:
        print("Are you sure you want to delete this faculty? This cannot be undone. (y/n)")
        remove_or_not = input().lower()

        if remove_or_not == "yes" or remove_or_not == "y":
            FacultyModel.Faculty.removeFaculty(Faculty, name_to_remove)
    
        else:       
            print("Removal cancelled")


# Directs the action the user wishes to take to the proper sections of the program.
def mainFacultyController(Faculty):
     # Repeats until 0/back is entered to return to call location (main).
    while True:
        print("What would like to do? Your options are:")
        print("1. Add faculty (Type 1 or add),")
        print("2. Edit faculty (Type 2 or edit),")
        print("3. Remove faculty (Type 3 or remove),")
        print("4. View Faculty in System (Type 4 or view)")
        print("5. Go back (Type 5 or back)")
        print(" Enter your choice here (Case Insensitive): ")

        # This stores the string the user inputted from the prompt above
        action = input()

        # Series of if-else statements that check the response the user gave to the prompt:
        # Adds a faculty
        if action == "1" or action.lower() == "add":
            addFacultyCLI(Faculty)

        # Edits a faculty
        elif action == "2" or action.lower() == "edit":
            editFacultyCLI(Faculty)
            print("Faculty updated")

        # Removes a faculty
        elif action == "3" or action.lower() == "remove":
            removeFacultyCLI(Faculty)
            print("Faculty removed.")

        # Prints a list of all current faculty entries.
        elif action == "4" or action.lower() == "view":
            viewFacultyCLI(Faculty)
        
        # Exits while loop and returns to where call originated.
        elif action == "5" or action.lower() == "back":
            return

        # If the user enters an invalid input
        else:
            print("Invalid response!")


