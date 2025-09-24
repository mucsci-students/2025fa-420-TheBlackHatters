import Models.Faculty_model as FacultyModel

# Gets the days and times the faculty is available
def daysAndTimes():

    # This gets available times for every day of the week
    # ".replace(" ", "")" removes any spaces the user may have accidentally added, just as a quality of life thing
    print("\033[31mNOTE: For the following prompts, if a faculty is available two or more different times in one day,\033[0m")
    print("\033[31mseparate the times by commas:\033[0m")
    #print("")
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
def addFacultyCLI(Faculty):
    # Gets faculty name
    print("Enter the faculty's name: ")
    faculty_name = input()

    # Checks for blank input:
    if faculty_name.replace(" ", "") == "":
        print("You entered a blank name!")
        return

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

    credit_range = str(min_credits) + "-" + str(max_credits)

    # Calls the function that gets days and times
    time_available = daysAndTimes()

    # Gets the course preferences for faculty, removes anything after the third entry
    # If preferences is empty then it replaces the list with "N/A"
    print("What are their course preferences? (Separate courses with commas, maximum of 3)")
    preferences = list(filter(None, input().lower().replace(" ", "").split(',')))
    if len(preferences) > 2:
        preferences = preferences[:3]
    if len(preferences) == 0:
        course_weight = "N/A"

    if len(preferences) > 0:
        # Loop for getting course weight
        i = 0
        course_weight = [None] * len(preferences)

        # Error checks if what they inputted is valid and if not it defaults to 3
        while i < len(preferences):
            print("Enter the course weight (0-10) for " + str(preferences[i]) + " (Default is 5, 0 means no preference):")
            course_weight[i] = input().replace(" ", "")
            try:
                if 0 <= int(course_weight[i]) <= 10:
                    course_weight[i] = int(course_weight[i])
                else:
                    course_weight[i] = 5
            except ValueError:
                course_weight[i] = 5
            i += 1

    # Gets the courses the faculty member teaches
    # Checks if faculty is adjunct or not, if so remove everything after first entry
    # If courses_taught is empty then it replaces the list with "N/A"
    print("How many courses can they teach? (Maximum of 2 for full-time, 1 for adjunct)")
    courses_taught = input().lower().replace(" ", "").split(',')
    if full_or_part_time != "full":
        courses_taught = courses_taught[:1]
    if len(courses_taught) == 0:
        courses_taught = ["N/A"]

    # This creates the new faculty with the info gotten from above
    new_faculty = {"name":faculty_name, "full-time/adjunct":full_or_part_time, "unique_course_limit":unique_course_limit, "available days/times":time_available, "course preferences":preferences, "course weight":course_weight, "course(s) taught":courses_taught, "credit range": credit_range}
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
        full_or_part_time = previous_faculty.get('available days/times')
        unique_course_limit = previous_faculty.get('unique course limit')
        time_available = previous_faculty.get('available days/times')
        preferences = previous_faculty.get('preferences')
        courses_taught = previous_faculty.get('courses_taught')
        credit_range = previous_faculty.get('credit_range')
        course_weight = previous_faculty.get('course weight')

        # Prompts the user to edit information and asks what information they want to edit
        print("What would you like to edit? Your options are:")
        print("name, full time or adjunct, availability, course preferences, courses taught, credit range (separate choices with commas)")
        things_to_edit = input().lower().replace(" ", "").split(',')
        #print(things_to_edit)

        # List of if statements that checks the list for what to edit
        # As a QOL addition for the user, the strings below have no spaces between them
        if "name" in things_to_edit:
            print("Enter the new name for this faculty:")
            faculty_name = input()

        # Updates if the faculty is full-time or adjunct
        if "fulltimeoradjunct" in things_to_edit:
            print("Are they full-time or adjunct? (Enter \"full\" or \"adjunct\") (Default: full)")
            response = input().lower().replace(" ", "")

            # Checks if the input is valid, defaults to full if invalid
            if response != "full" and full_or_part_time != "adjunct":
                full_or_part_time = "full"

            # This checks if the faculty is full-time or adjunct, and sets the course limit
            if full_or_part_time == "full":
                unique_course_limit = 2
            else:
                unique_course_limit = 1

        # Calls the daysAndTimes method to update the faculty's availability
        if "availability" in things_to_edit:
            time_available = daysAndTimes()

        if "credit range" in things_to_edit:
            if full_or_part_time == "full":
                max_teachable_credits = 12
            else:
                max_teachable_credits = 4

            # Gets the minimum credits the faculty can teach
            print("Enter the minimum credits a faculty can teach per semester (default is 0):")
            min_credits = input()
            try:
                if int(min_credits) < 0 or int(min_credits) > int(max_teachable_credits):
                    min_credits = 0
            except ValueError:
                min_credits = 0
    
            # Gets the maximum credits the faculty can teach
            print("Enter the maximum credits a faculty can teach per semester (default is " + str(max_teachable_credits) + "):")
            max_credits = input()
            try:
                if int(max_credits) > max_teachable_credits or int(max_credits) < int(min_credits):
                    max_credits = max_teachable_credits
            except ValueError:
                max_credits = max_teachable_credits
            
            credit_range = str(min_credits) + "-" + str(max_credits)

        # Updates the course preferences
        # NOTE: temp_preferences is a temporary variable to store the actual list of preferences for conditional checking, 
        # and is not returned
        if "coursepreferences" in things_to_edit:
            print("What are their course preferences? (Separate courses with commas, maximum of 3)")
            temp_preferences = list(filter(None, input().lower().replace(" ", "").split(',')))
            if len(temp_preferences) > 2:
                temp_preferences = temp_preferences[:3]
            if len(temp_preferences) == 0:
                preferences = {"course preferences":["N/A"]}
            else: 
                # Loop for getting course weight
                i = 0
                course_weight = [None] * len(temp_preferences)

                # Error checks if what they inputted is valid and if not it defaults to 3
                while i < len(temp_preferences):
                    print("Enter the course weight (0-10) for " + str(temp_preferences[i]) + " (Default is 5, 0 means no preference):")
                    course_weight[i] = input().replace(" ", "")
                    try:
                        if 0 <= int(course_weight[i]) <= 10:
                            course_weight[i] = int(course_weight[i])
                        else:
                            course_weight[i] = 5
                    except ValueError:
                        course_weight[i] = 5
                    i=i+1

        # Updates the courses taught
        if "coursestaught" in things_to_edit:
            print("What courses do they teach? (Maximum of 2 for full-time, 1 for adjunct)")
            courses_taught = input().lower().replace(" ", "").split(',')

            if full_or_part_time != "full":
                courses_taught = courses_taught[:1]
            if len(courses_taught) == 0:
                courses_taught = ["N/A"]


        edited_faculty = {"name":faculty_name, "full-time/adjunct":full_or_part_time, "unique_course_limit":unique_course_limit, "available days/times":time_available, "course preferences":preferences, "course weight":course_weight, "course(s) taught":courses_taught, "credit range": credit_range}
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
        print("What would like to do? Your options are: " \
        "\n 1. Add faculty (Type 1 or add), \n 2. Edit faculty (Type 2 or edit), \n 3. Remove faculty (Type 3 or remove), \n 4. Go back (Type 4 or back)" \
        "\n Enter your choice here (Case Insensitive): ")

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

        # Exits while loop and returns to where call originated.
        elif action == "4" or action.lower() == "back":
            return

        # If the user enters an invalid input
        else:
            print("Invalid response!")
