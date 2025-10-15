# Resources: https://customtkinter.tomschimansky.com/documentation/widgets 
import customtkinter as ctk
from tkinter import StringVar, IntVar
from Controller.main_controller import (RoomsController, LabsController, FacultyController,
                                        configImportBTN, configExportBTN, generateSchedulesBtn,
                                        importSchedulesBTN, exportAllSchedulesBTN, exportOneScheduleBTN,
                                        CourseController)

# should create controllers for other things too
roomCtr = RoomsController()
facultyCtr = FacultyController()
labCtr = LabsController()
courseCtr = CourseController()

# Dummy Data to just put something in the forms i will create
# This data is just for testing Purpuses! 
##Rooms = ["Roddy 136","Roddy 140","Roddy 147", "Roddy 1","Roddy 2","Roddy 3"]
Courses = [
    {"course_id": "CMSC 140",
     "credits": 4,
     "room": ["Roddy 136", "Roddy 140", "Roddy 147"],
     "lab": [],
     "conflicts": ["CMSC 161", "CMSC 162"],
     "faculty": []
     },
    {"course_id": "CMSC 140",
     "credits": 4,
     "room": ["Roddy 136", "Roddy 140", "Roddy 147"],
     "lab": [],
     "conflicts": ["CMSC 161", "CMSC 162"],
     "faculty": []
     }]

Faculty = [
    {"name": "Zoppetti",
     "maximum_credits": 12,
     "minimum_credits": 12,
     "unique_course_limit": 3,
     "times": {
         "MON": ["11:00-16:00"],
         "TUE": [],
         "WED": ["10:00-15:00"],
         "THU": ["10:00-17:00"],
         "FRI": ["11:00-16:00"]},
     "course_preferences": {"CMSC 362": 5, "CMSC 476": 5, "CMSC 161": 4},
     "room_preferences": {"Roddy 136": 5, "Roddy 140": 1, "Roddy 147": 1},
     "lab_preferences": {"Linux": 5, "Mac": 1}
     },
    {"name": "Hardy",
     "maximum_credits": 14,
     "minimum_credits": 12,
     "unique_course_limit": 2,
     "times": {
         "MON": ["09:00-15:00"],
         "TUE": ["09:00-15:00"],
         "WED": ["09:00-15:00"],
         "THU": [],
         "FRI": ["09:00-15:00"]},
     "course_preferences": {"CMSC 140": 5, "CMSC 152": 4},
     "room_preferences": {"Roddy 147": 10, "Roddy 140": 1, "Roddy 136": 1},
     "lab_preferences": {"Linux": 3, "Mac": 3}
     },
    {"name": "Ho",
     "maximum_credits": 12,
     "minimum_credits": 12,
     "unique_course_limit": 3,
     "times": {
         "MON": ["11:00-16:00"],
         "TUE": [],
         "WED": ["10:00-15:00"],
         "THU": ["10:00-17:00"],
         "FRI": ["11:00-16:00"]},
     "course_preferences": {"CMSC 362": 5, "CMSC 476": 5, "CMSC 161": 4},
     "room_preferences": {"Roddy 136": 5, "Roddy 140": 1, "Roddy 147": 1},
     "lab_preferences": {"Linux": 5, "Mac": 1}
     },
]
scheduleExample = [[
    ["CMSC 140.01", "Hardy", "Roddy 147", "None", "MON 13:00-13:50", "WED 13:00-14:50", "FRI 13:00-13:50"],
    ["CMSC 140.02", "Hardy", "Roddy 147", "None", "MON 13:00-13:50", "WED 13:00-14:50", "FRI 13:00-13:50"],
    ["CMSC 152.01", "Hardy", "Roddy 147", "Mac", "MON 11:00-11:50", "TUE 10:00-11:50^", "FRI 11:00-11:50"],
    ["CMSC 161.01", "Zoppetti", "Roddy 136", "Linux", "MON 14:00-14:50", "THU 13:10-15:00^", "FRI 14:00-14:50"],
    ["CMSC 161.02", "Wertz", "Roddy 147", "Linux", "TUE 08:00-09:50", "THU 08:00-09:50"]],

    [
        ["CMSC 140.01", "Hardy2", "Roddy 1147", "None", "MON 13:00-13:50", "WED 13:00-14:50", "FRI 13:00-13:50"],
        ["CMSC 140.02", "Hardy2", "Roddy 1147", "None", "MON 13:00-13:50", "WED 13:00-14:50", "FRI 13:00-13:50"],
        ["CMSC 152.01", "Hardy2", "Roddy 1147", "Mac", "MON 11:00-11:50", "TUE 10:00-11:50^", "FRI 11:00-11:50"],
        ["CMSC 161.01", "Zoppetti2", "Roddy 1136", "Linux", "MON 14:00-14:50", "THU 13:10-15:00^", "FRI 14:00-14:50"],
        ["CMSC 161.02", "Wertz2", "Roddy 1147", "Linux", "TUE 08:00-09:50", "THU 08:00-09:50"]
    ],
    [
        ["CMSC 140.01", "Hardy2", "Roddy 1147", "None", "MON 13:00-13:50", "WED 13:00-14:50", "FRI 13:00-13:50"],
        ["CMSC 140.02", "Hardy2", "Roddy 1147", "None", "MON 13:00-13:50", "WED 13:00-14:50", "FRI 13:00-13:50"],
        ["CMSC 152.01", "Hardy2", "Roddy 1147", "Mac", "MON 11:00-11:50", "TUE 10:00-11:50^", "FRI 11:00-11:50"],
        ["CMSC 161.01", "Zoppetti2", "Roddy 1136", "Linux", "MON 14:00-14:50", "THU 13:10-15:00^", "FRI 14:00-14:50"],
        ["CMSC 161.02", "Wertz2", "Roddy 1147", "Linux", "TUE 08:00-09:50", "THU 08:00-09:50"]
    ]]


# The config page has left/right. This function when called with with data will fill the left side. 
# right now we are not using the data varabale and just working with dummy data. 
# frame: the place we are going to put all out stuff.
# facultyData: will contain the faculty data for all faculty..  
def dataFacultyLeft(frame, controller, refresh, facultyData=None):

    # we create a container to put everything inside, this container lives inside the frame
    # with .pack we display the continer on the screen(fill="both": fills the x and y direction,
    # expand=True: allows it to expand when we change the screen size. padx/y = 5: adds 5px padding on all sides :)
    container = ctk.CTkFrame(frame, fg_color="transparent")
    container.pack(fill="both", expand=True, padx=5, pady=5)

    # just want to refresh the page to open new form
    def onAdd():
        refresh(target="ConfigPage")

    # we are creating and puting on screen at same time with .pack. 
    # Button lives in container we crated above
    # Button has text "Add" inside it        
    ctk.CTkButton(container, text="Add", width= 120, height = 20, command=lambda: onAdd()).pack(side="top", padx=5)


    def onDelete(facName):
        controller.removeFaculty(facName, refresh)

    def onEdit(faculty):
        refresh(target="ConfigPage", data=faculty)

    facList = facultyCtr.listFaculty()
    sorted_fac = sorted(facList, key=lambda x: x["name"])
    
    # This will loop thought the facultyData and display the names on the left side 
    for faculty in sorted_fac:
        # For each faculty member I need their name, edit and delete btn.
        # I need to create a fram to put thoses element.
        # fg_color =  "transparent" mean this frame I am creating has no color.
        rowFrame = ctk.CTkFrame(container, fg_color="transparent")
        rowFrame.pack(fill="x", pady=5, padx=5)

        facName = faculty["name"]
        # This is a Label, text showen on screen! 
        # Label lives inside the rowFrame we created above, text is the name
        ctk.CTkLabel(rowFrame, text=facName, font=("Arial", 14, "bold"), anchor="w").pack(side="left", fill="x", expand=True)

        # Buttons. The two buttions are for deleting and editing Faculty.
        # Again .pack displays on screen, we are adding both buttons on rowFrame
        ctk.CTkButton(rowFrame, text="Delete", width=30, height = 20, command=lambda n = facName: onDelete(n)).pack(side="left", padx=5)
        ctk.CTkButton(rowFrame, text="Edit", width=30,  height = 20, command=lambda f = faculty: onEdit(f)).pack(side="left", padx=5)


# This function will populate the right side of the page. (If you don't understand left and right load the program and go into config file. Should make sence once you see it!)
# this function kinda of acts like a form for user to fill.
# we need to display the current data if user pressed edit on button before or just get an empty one
def dataFacultyRight(frame, controller, refresh, data=None):
    #Checks if the data being passed in is a string (will break things if so, so stops it)
    #if isinstance(data, str):
    #    pass
    #else:
        # This is for the name of faculty: which has a label and entry;
        # it will look somehting like this: Name:__E.g: Hobbs_______
        # Again we create a frame to add the label and entry.
        rowName = ctk.CTkFrame(frame, fg_color="transparent")
        rowName.pack(fill="x", pady=5, padx=5)

        # this is the label for Name.
        # We just create and display the label here
        ctk.CTkLabel(rowName, text="Name:", width=120, anchor="w", font=("Arial", 30, "bold")).pack(side = "left", padx=10, pady=(0, 2))

        # this is for and entry, this is where the user can write things in 
        nameEntry = ctk.CTkEntry(rowName, placeholder_text="E.g: Hobbs",font=("Arial", 30, "bold") )
        nameEntry.pack(side="left", fill="x", expand=True, padx=5)

        # Gets the faculty type
        facultyType = ctk.StringVar(value="full")

        # This is what onFacultyTypeChange will change to reflect the maximum credit range a faculty can have (0-4 for adjunct, 0-12 for full-time)
        maxCreditsToRead = ctk.StringVar(value="0")
        # This is what onFacultyTypeChange will change to reflect the minimum credit range a faculty can have
        minCreditsToRead = ctk.StringVar(value="0")
        # This is what onFacultyTypeChange will change to reflect the unique course limit range a faculty can have (0-1 for adjunct, 0-2 for full-time)
        uniqueLimitToRead = ctk.StringVar(value="0")

        # Sets the maximum credits, minimum credits, and unique course limit a faculty can have
        def onFacultyTypeChange():
            if facultyType.get() == "full":
                newMaxCredits = [str(i) for i in range(0, 13)]
                newMinCredits = [str(i) for i in range(0, 13)]
                newUniqueLimit = [str(i) for i in range(0, 3)]
            else:
                newMaxCredits = [str(i) for i in range(0, 5)]
                newMinCredits = [str(i) for i in range(0, 5)]
                newUniqueLimit = [str(i) for i in range(0, 2)]
            maxEntry.configure(values=newMaxCredits)
            minEntry.configure(values=newMinCredits)
            uniqueEntry.configure(values=newUniqueLimit)

        # Makes a row container for the full/adjunct buttons
        rowFacultyType = ctk.CTkFrame(frame, fg_color="transparent")
        rowFacultyType.pack(fill="x", pady=5)

        # Label for the faculty type
        facultyLabel = ctk.CTkLabel(rowFacultyType, text="Is the faculty full-time or adjunct?",
                                    font=("Arial", 25, "bold")).pack(side="left", padx=10, pady=5)
        # Full-time button
        fullSelection = ctk.CTkRadioButton(rowFacultyType, text="Full-time", variable=facultyType, value="full",
                                           font=("Arial", 20, "bold"), command=onFacultyTypeChange).pack(side="left",
                                                                                                         padx=10)
        # Adjunct button
        adjunctSelection = ctk.CTkRadioButton(rowFacultyType, text="Adjunct", variable=facultyType, value="adjunct",
                                              font=("Arial", 20, "bold"), command=onFacultyTypeChange).pack(side="left",
                                                                                                            padx=10)

        # if we have data given here we just display the data
        # for example when someone clicks edit.
        if data:
            if data != None:
                nameEntry.insert(0, data.get("name", ""))

        # This is to display the credit things
        # we need to place, Label and Entry to for each of those we need a frame
        # we put those two things in the frame and show it on the screen.
        rowCredits = ctk.CTkFrame(frame, fg_color="transparent")
        rowCredits.pack(fill="x", pady=5, padx=5, expand=True)

        # Helper text for entering credits
        ctk.CTkLabel(rowCredits, text="(Minimum is 0, Maximum is 4 for adjunct faculty and 12 for full-time faculty)",
                     anchor="w", font=("Arial", 15, "bold", "underline"), justify="left", text_color="cyan").pack(
            anchor="w", padx=5, pady=(0, 5))

        # Dropdown menu, and label for minimum credits
        ctk.CTkLabel(rowCredits, text="Min Credits:", font=("Arial", 30, "bold")).pack(side="left", fill="x", padx=5)
        minEntry = ctk.CTkOptionMenu(rowCredits, variable=minCreditsToRead, values=[str(i) for i in range(0, 13)],
                                     font=("Arial", 30, "bold"), dropdown_font=("Arial", 20))
        minEntry.pack(side="left", fill="x", expand=True, padx=5)

        rowCredits = ctk.CTkFrame(frame, fg_color="transparent")
        rowCredits.pack(fill="x", pady=5, padx=5, expand=True)

        # Dropdown menu and label for maximum credits
        ctk.CTkLabel(rowCredits, text="Max Credits:", font=("Arial", 30, "bold")).pack(side="left", fill="x", padx=5)
        maxEntry = ctk.CTkOptionMenu(rowCredits, variable=maxCreditsToRead, values=[str(i) for i in range(0, 13)],
                                     font=("Arial", 30, "bold"), dropdown_font=("Arial", 20))
        maxEntry.pack(side="left", fill="x", expand=True, padx=5)

        # Same things for Unique Course Limit:
        rowCredits = ctk.CTkFrame(frame, fg_color="transparent")
        rowCredits.pack(fill="x", pady=5, padx=5, expand=True)

        # Dropdown menu, label, and helper text for unique course limit
        ctk.CTkLabel(rowCredits, text="(Minimum is 0, Maximum is 1 for adjunct faculty and 2 for full-time faculty):",
                     anchor="w", font=("Arial", 15, "bold", "underline"), text_color="cyan", justify="left").pack(
            anchor="w", padx=5, pady=(0, 5))
        ctk.CTkLabel(rowCredits, text="Unique Course Limit:", font=("Arial", 30, "bold")).pack(side="left", fill="x",
                                                                                               padx=5)
        uniqueEntry = ctk.CTkOptionMenu(rowCredits, variable=uniqueLimitToRead, values=[str(i) for i in range(0, 3)],
                                        font=("Arial", 30, "bold"), dropdown_font=("Arial", 20))
        uniqueEntry.pack(side="left", fill="x", expand=True, padx=5)

        # Actally put the data in the entrys, if there is data given
        if data:
            minEntry.set(str(data.get("minimum_credits", 0)))
            maxEntry.set(str(data.get("maximum_credits", 0)))
            uniqueEntry.set(str(data.get("unique_course_limit", 0)))

        # Again we create row frame for the time availability, that will hold eveything for time
        # Wa also add a label with the text Availability (MON-FRI), and font and put on screen.
        rowAvailability = ctk.CTkFrame(frame, fg_color="transparent")
        rowAvailability.pack(fill="x", pady=5, padx=5)
        # Label and helper text for availability
        ctk.CTkLabel(rowAvailability, text="Availability (MON-FRI):", anchor="w", font=("Arial", 30, "bold")).pack(
            anchor="w", padx=10, pady=(2, 0))
        ctk.CTkLabel(rowAvailability,
                     text=f"(Leave blank for 9:00-5:00, type \"n/a\" if they are not available on that day):",
                     anchor="w", font=("Arial", 15, "bold", "underline"), justify="left", text_color="cyan").pack(
            side="top", fill="x", pady=(0, 5))

        # now this will actally put the times from the data
        # we will just loop through the days
        days = ["MON", "TUE", "WED", "THU", "FRI"]

        # in the for loop we create a frame again for each day, with label and engry

        dayEntries = {}

        for day in days:
            dayFrame = ctk.CTkFrame(rowAvailability, fg_color="transparent")
            dayFrame.pack(fill="x", padx=20, pady=(0, 2))

            # Label for the day
            ctk.CTkLabel(dayFrame, text=f"{day}:", width=50, anchor="w", font=("Arial", 25, "bold")).pack(side="left")

            # entry for each of the day and show it on screen
            dayEntry = ctk.CTkEntry(dayFrame, placeholder_text="E.g: 8:00-10:00, 12:30-5:00",
                                    font=("Arial", 30, "bold"))
            dayEntry.pack(side="left", fill="x", expand=True)

            dayEntries[day] = dayEntry

            # this will display the given data if we do give it data,
            # other wise is just empty
            if data and "times" in data:
                dayEntry.insert(0, ', '.join(data["times"].get(day, [])))

        # Course Preference Frame, we create it and pack in on screen
        # In side this frame we will write everything for course_preferences
        rowCourse = ctk.CTkFrame(frame, fg_color="transparent")
        rowCourse.pack(fill="x", pady=5, padx=5)

        # IMPORTANT, PLEASE READ TO AVOID CONFUSION:
        # At the moment, when editing, the program loads data from the dummy data I created specifically for this section
        # When you click the dropdown menus, different rooms and courses are shown than the ones initially displayed
        # When the file loads things from an actual config file, it will load ALL THE ROOMS AND COURSES AVAILABLE
        # At the moment, the items in the dropdown are reading from the dummy data at the top of the file. This will be replaced with actual data from a JSON file.
        # The items initially being displayed are read from the COURSE PREFERENCES, which is where we will want to read them from when outputting existing data
        # In summary, the DISPLAYS data from the preferences and allows you to select courses that exist FROM THE EXISTING COURSES
        # This is how it is intended to work, though it may be confusing right now

        # Dict to store the course preferences to return
        coursePreferences = {}

        # List of all possible courses
        all_courses = sorted({c["course_id"] for c in courseCtr.listCourses()})

        # Track each course dropdown variable + widget
        course_vars = []

        # Function to update dropdowns so already selected courses don't appear in other dropdowns
        def update_course_dropdowns(*args):
            selected_courses = {var.get() for var, _ in course_vars if var.get() != "None"}
            for var, dropdown in course_vars:
                current = var.get()
                available = [c for c in all_courses if c not in selected_courses or c == current]
                # Always include "None" at the front
                if "None" not in available:
                    available.insert(0, "None")
                dropdown.configure(values=available)

        ctk.CTkLabel(rowCourse, text="Course Preferences:", anchor="w", font=("Arial", 30, "bold")).pack(anchor="w",
                                                                                                         padx=10,
                                                                                                         pady=(2, 5))

        ctk.CTkLabel(rowCourse, text="(Set name to None to remove - Second option is for Weight):", anchor="w",
                     font=("Arial", 15, "bold", "underline"), text_color="cyan", justify="left").pack(anchor="w",
                                                                                                      padx=5,
                                                                                                      pady=(0, 5))
        ctk.CTkLabel(rowCourse, text="(Maximum 3 entries, further are truncated):", anchor="w",
                     font=("Arial", 15, "bold", "underline"), text_color="cyan", justify="left").pack(anchor="w",
                                                                                                      padx=5,
                                                                                                      pady=(0, 5))

        # Lets the user add additonal course rows if desired.
        addCourseButton = ctk.CTkButton(rowCourse, text="Add Course", width=30, height=20,
                                        command=lambda: preference_bar_creation("None", 5)).pack(side=ctk.LEFT, padx=5)

        # Allows for more modular bar creation if we need to allow user to choose to add more classes.
        def preference_bar_creation(course_name, weight):
            courseRow = ctk.CTkFrame(rowCourse, fg_color="transparent")
            courseRow.pack(fill="x", padx=20, pady=2)

            # Ensure default value is the course from dummy data if it exists in course_ids
            values_list = ["None"] + all_courses
            ##print(str(values_list))
            if course_name not in values_list:
                values_list.append(course_name)
            course_var = ctk.StringVar(value=course_name)
            course_dropdown = ctk.CTkOptionMenu(courseRow, variable=course_var, values=all_courses, width=200,
                                                font=("Arial", 20))
            course_dropdown.pack(side="left", padx=20, pady=2)

            # Trace for mutual exclusivity
            course_var.trace_add("write", update_course_dropdowns)
            course_vars.append((course_var, course_dropdown))

            # Weight dropdown
            weight_dropdown = ctk.CTkOptionMenu(courseRow, width=150, values=[str(i) for i in range(11)])
            weight_dropdown.set(str(weight) if data else "5")
            weight_dropdown.pack(side="left", padx=(0, 10), fill="x")

            # Store references
            coursePreferences[course_name] = {
                "course_var": course_var,
                "weight_dropdown": weight_dropdown
            }

        # Create one dropdown row per course in the data if editing, otherwise create empty rows
        # Decide how many dropdown rows to create
        if data:
            course_data = data.get("course_preferences")
            if course_data != None:
                print(course_data)
                for course in course_data:
                    # Stores the weight for the course.
                    weight = course_data.get(course)
                    # Creates the Course entries
                    preference_bar_creation(course, weight)
        else:
            # for i in range(3):
            #     preference_bar_creation("None", 5)
            preference_bar_creation("None", 5)

        # Initial synchronization of dropdowns
        update_course_dropdowns()

        # room Prefrence EXACT SAME THING AS ABOVE(Course Prefrence)

        # Dict to store the room preferences to return
        roomPreferences = {}

        # This loads the rooms from the JSON data
        room_ids = roomCtr.listRooms()
        # all_rooms = sorted({c["room_id"] for c in room_ids})

        # Track each room dropdown variable + widget
        room_vars = []

        # Function to update the dropdowns so already selected rooms don't appear in the dropdown menu again
        def update_room_dropdowns(*args):
            # Collect all selected rooms (ignore "None")
            selected_rooms = {var.get() for var, _ in room_vars if var.get() != "None"}

            for var, dropdown in room_vars:
                current_value = var.get()

                # Build available list without duplicating "None"
                available = [r for r in room_ids if r not in selected_rooms or r == current_value]

                # Include "None" only if this dropdown currently has it selected
                if "None" not in available:
                    available.insert(0, "None")

                dropdown.configure(values=available)

        rowRoom = ctk.CTkFrame(frame, fg_color="transparent")
        rowRoom.pack(fill="x", pady=5, padx=5)

        # The room selection section
        # List of all rooms from JSON config
        # all_rooms = json_data["config"]["rooms"]

        # Dict to store the room preferences
        roomPreferences = {}
        room_vars = []

        ctk.CTkLabel(rowRoom, text="Room Preferences:", anchor="w", font=("Arial", 30, "bold")).pack(anchor="w",
                                                                                                     padx=10,
                                                                                                     pady=(2, 5))
        ctk.CTkLabel(rowRoom, text="(Maximum 3 entries):", anchor="w", font=("Arial", 15, "bold", "underline"),
                     text_color="cyan", justify="left").pack(anchor="w", padx=5, pady=(0, 5))

        addRoomButton = ctk.CTkButton(rowRoom, text="Add Room", width=30, height=20,
                                      command=lambda: room_bar_creation("None", 5)).pack(side=ctk.LEFT, padx=5)

        def room_bar_creation(room_name, weight):
            roomRow = ctk.CTkFrame(rowRoom, fg_color="transparent")
            roomRow.pack(fill="x", padx=20, pady=2)

            # Ensure default value is the room from data if it exists
            values_list = ["None"] + room_ids
            if room_name not in values_list:
                values_list.append(room_name)

            room_var = ctk.StringVar(value=room_name)
            room_dropdown = ctk.CTkOptionMenu(roomRow, variable=room_var, values=values_list, width=200,
                                              font=("Arial", 20))
            room_dropdown.pack(side="left", padx=20, pady=2)

            # Trace for mutual exclusivity
            room_var.trace_add("write", update_room_dropdowns)
            room_vars.append((room_var, room_dropdown))

            # Weight dropdown
            weight_dropdown = ctk.CTkOptionMenu(roomRow, width=150, values=[str(i) for i in range(11)])
            weight_dropdown.set(str(weight))
            weight_dropdown.pack(side="left", padx=(0, 10), fill="x")

            # Store references
            roomPreferences[room_name] = {
                "room_var": room_var,
                "weight_dropdown": weight_dropdown
            }

    
        if data:
            room_data = data.get("room_preferences")
            if room_data != None:
                for room in room_data:
                    # Stores the weight for the course.
                    weight = room_data.get(room)
                    # Creates the Course entries
                    room_bar_creation(room, weight)
        else:
            # for i in range(3):
            #     room_bar_creation("None", 5)
            room_bar_creation("None", 5)

        # Lab Prefrence EXACT SAME THING AS ABOVE (Course Prefrence and Room Preferences)
        labPreferences = {}
        lab_ids = labCtr.listLabs()
        # all_labs = sorted({c["lab_id"] for c in lab_ids})
        lab_vars = []

        # Function to update the dropdowns so already selected labs don't appear in the dropdown menu again
        def update_lab_dropdowns(*args):
            # Collect all selected labs (ignore "None")
            selected_labs = {var.get() for var, _ in lab_vars if var.get() != "None"}

            for var, dropdown in lab_vars:
                current_value = var.get()

                # Build available list without duplicating "None"
                available = [r for r in lab_ids if r not in selected_labs or r == current_value]

                # Include "None" only if this dropdown currently has it selected
                if "None" not in available:
                    available.insert(0, "None")

                dropdown.configure(values=available)

        rowLab = ctk.CTkFrame(frame, fg_color="transparent")
        rowLab.pack(fill="x", pady=5, padx=5)

        ctk.CTkLabel(rowLab, text="Lab Preferences:", anchor="w", font=("Arial", 30, "bold")).pack(anchor="w", padx=10,
                                                                                                   pady=(2, 5))
        ctk.CTkLabel(rowLab, text="(Maximum 2 entries):", anchor="w", font=("Arial", 15, "bold", "underline"),
                     text_color="cyan", justify="left").pack(anchor="w", padx=5, pady=(0, 5))

        # Allows user to add additional lab entries if needed.
        addLabButton = ctk.CTkButton(rowLab, text="Add Lab", width=30, height=20,
                                     command=lambda: lab_bar_creation("None", 5)).pack(side=ctk.LEFT, padx=5)

        # Lab Entry constructor, Allows for more modular creation of lab entries.
        def lab_bar_creation(lab, weight):
            labRow = ctk.CTkFrame(rowLab, fg_color="transparent")
            labRow.pack(fill="x", padx=20, pady=2)

            # Ensure default value is the room from data if it exists
            values_list = ["None"] + lab_ids
            if lab not in values_list:
                values_list.append(lab)

            lab_var = ctk.StringVar(value=lab)
            dropdown = ctk.CTkOptionMenu(labRow, variable=lab_var, values=values_list, width=200, font=("Arial", 20))
            dropdown.pack(side="left", padx=20, pady=2)

            # Trace for mutual exclusivity
            lab_var.trace_add("write", update_lab_dropdowns)
            lab_vars.append((lab_var, dropdown))

            # ctk.CTkLabel(labRow, text=f"{lab}:", anchor="w", width=150, font=("Arial", 25, "bold")).pack( side="left", padx=20, pady=2)
            weight_dropdown = ctk.CTkOptionMenu(labRow, width=150, values=[str(i) for i in range(11)])
            weight_dropdown.set(str(weight))
            weight_dropdown.pack(side="left", padx=(0, 10), fill="x")

            labPreferences[lab] = {
                "lab_var": lab_var,
                "weight_dropdown": weight_dropdown
            }

        # Creates Lab entry for each Lab in the Faculty Data, otherwise creates two.
        if data:
            lab_data = data.get("lab_preferences")
            if lab_data != None:
                for lab in lab_data:
                    # Stores the weight for the course.
                    weight = lab_data.get(lab)
                    # Creates the Course entries
                    lab_bar_creation(lab, weight)
        else:
            # for i in range(2):
            #     lab_bar_creation("None", 5)
            lab_bar_creation("None", 5)

        # Creates a pop-up to display error messages when attempting to save faculty
        def show_error_popup(errors):
            popup = ctk.CTkToplevel()
            popup.title("Error(s) Found!")
            popup.geometry("400x300")
            popup.grab_set()

            ctk.CTkLabel(popup, text="Please correct the following:", font=("Arial", 20, "bold"),
                         text_color="red").pack(pady=(10, 5))

            # Display each error as a label
            for err in errors:
                ctk.CTkLabel(popup, text=f"• {err}", font=("Arial", 15), anchor="w", justify="left",
                             wraplength=350).pack(anchor="w", padx=20, pady=2)

            # Add a Close button
            ctk.CTkButton(popup, text="Close", width=100, command=popup.destroy).pack(pady=15)

        # Gets the faculty data to return to the program
        def returnFacultyData():

            # Stores potential errors that may exist when trying to save changes
            errors = []

            # Gets the user input for the faculty name
            faculty_name = nameEntry.get()
            # Checks if user entered a name for the faculty, gives an error if not
            if not faculty_name:
                errors.append("Please enter a faculty name!")

            # Gets the user input for the maximum credits
            maximum_credits = int(maxEntry.get())
            maximum_credits = int(maxEntry.get())

            # Gets the user input for the minimum credits
            minimum_credits = int(minEntry.get())
            minimum_credits = int(minEntry.get())

            if minimum_credits > maximum_credits:
                errors.append("Minimum credits cannot be greater than maximum credits!")

            # Gets the available times
            availability = {}
            for day, entry in dayEntries.items():
                value = entry.get().strip()
                if not value:
                    availability[day] = ["9:00-5:00"]
                elif value.lower() == "n/a":
                    availability[day] = []
                else:
                    availability[day] = [v.strip() for v in value.split(",")]

            # Gets the user input for the unique course limit
            unique_course_limit = uniqueEntry.get()

            # Gets the course preferences and formats them properly
            course_preferences = {}
            for key, widgets in coursePreferences.items():
                course_name = widgets["course_var"].get()
                weight = int(widgets["weight_dropdown"].get())

                # If 'None' is selected, skip it
                if course_name != "None":
                    course_preferences[course_name] = weight

            # Gets the room preferences and formats them properly
            room_preferences = {}
            for key, widgets in roomPreferences.items():
                room_name = widgets["room_var"].get()
                weight = int(widgets["weight_dropdown"].get())

                # Skip if "None" is selected
                if room_name != "None":
                    room_preferences[room_name] = weight

            # Gets the lab preferences and formats them properly
            lab_preferences = {}
            for lab, widgets in labPreferences.items():
                lab_name = widgets["lab_var"].get()
                weight = int(widgets["weight_dropdown"].get())

                # Skip if "None" is selected
                if lab_name != "None":
                    lab_preferences[lab_name] = weight

            # If there are errors, show popup and return nothing
            if errors:
                show_error_popup(errors)
                return [False, None]

            # Otherwise, success popup
            success_popup = ctk.CTkToplevel()
            success_popup.title("Success")
            success_popup.geometry("300x150")
            success_popup.grab_set()
            ctk.CTkLabel(success_popup, text="Faculty successfully saved!", font=("Arial", 18, "bold"),
                         text_color="green").pack(pady=30)
            ctk.CTkButton(success_popup, text="OK", command=success_popup.destroy).pack()

            # Returns the new_faculty with the given data
            new_faculty = {"name": faculty_name, "maximum_credits": maximum_credits, "minimum_credits": minimum_credits,
                           "unique_course_limit": unique_course_limit, "times": availability,
                           "course_preferences": course_preferences, "room_preferences": room_preferences,
                           "lab_preferences": lab_preferences}
            # Prints out information being returned, for testing purposes:
            # print("Faculty name: " ,faculty_name, "Max credits: ", maximum_credits, "Min credits: ", minimum_credits, "Unqiue course limit: ", unique_course_limit, "Availablity: ", availability, "Course preferences: ", course_preferences, "Room preferences: ", room_preferences, "Lab preferences: ", lab_preferences)
            return [True, new_faculty]

        # The actions that will happen when save changes is pressed - either calling edit faculty or add faculty.
        def onSave():
            #Gets the values from all entries
            result = returnFacultyData()
            #Checks if there was a problem, if so does nothing.
            if result[0]:
                #Grabs the new faculty data.
                newFaculty = result[1]
                if data:
                    #Stores the original name for the data for proper replacement when editing in case the name has changed.
                    facName = data.get("name")
                    controller.editFaculty(newFaculty, facName, refresh)
                else:
                    controller.addFaculty(newFaculty, refresh)

        
        # this is the save buttion that will save changes when we add a new faculty and when we modify existing
        ctk.CTkButton(frame, text="Save Changes", width=100, font=("Arial", 20, "bold"), height = 40, command=lambda: onSave()).pack(side="bottom", padx=5)






# this function will fill in the data on the right side of the two column
def dataRoomRight(frame, controller, refresh, data=None):
    # rooms = controller.listRooms()
    # we should know what this does by now.
    # we make a frame to lay things on top
    container = ctk.CTkFrame(frame, fg_color="transparent")
    container.pack(fill="x", pady=5, padx=5)

    # we put a label, and entry for name.
    ctk.CTkLabel(container, text="Name:", width=120, anchor="w", font=("Arial", 30, "bold")).grid(row=0, column=0,
                                                                                                  padx=10, pady=2)
    nameEntry = ctk.CTkEntry(container, width=350, placeholder_text="E.g: Roddy 140", font=("Arial", 30, "bold"))
    nameEntry.grid(row=0, column=1, sticky="ew", padx=5)

    if data:
        nameEntry.insert(0, data)

    def onSave():
        name = nameEntry.get()
        if name.strip():
            if data:
                controller.editRoom(data, name, refresh)
            else:
                controller.addRoom(name, refresh)
        else:
            ctk.CTkLabel(frame, text="Please Input Valid Room Name! ", width=120, anchor="w", font=("Arial", 30, "bold"), text_color = "red").grid(row=0, column=0,padx=10, pady=2)


    # TODO: Need to add command properly.

    ctk.CTkButton(frame, text="Save Changes", width=100, font=("Arial", 20, "bold"), height=40, command=onSave).pack(
        side="bottom", padx=5)


# This function is to popluate the left side of the screen.
# pretty much same things as above.
def dataRoomLeft(frame, controller, refresh, data=None):
    # frame to put everything in
    container = ctk.CTkFrame(frame, fg_color="transparent")
    container.pack(fill="both", expand=True, padx=5, pady=5)

    # just want to refresh the page to open new form
    def onAdd():
        refresh(target="ConfigPage")

    # TODO: Creates new form on the right
    ctk.CTkButton(container, text="Add", width=120, height=20,
                  command=lambda: onAdd()
                  ).pack(side="top", padx=5)

    def onDelete(room):
        controller.removeRoom(room, refresh)

    def onEdit(room):
        refresh(target="ConfigPage", data=room)

    for room in controller.listRooms():
        # Horizontal container for label  and buttons
        rowFrame = ctk.CTkFrame(container, fg_color="transparent")
        rowFrame.pack(fill="x", pady=5, padx=5)

        # Label
        ctk.CTkLabel(rowFrame, text=room, font=("Arial", 14, "bold"), anchor="w").pack(side="left", fill="x",
                                                                                       expand=True)

        # Buttons to edit and delete
        ctk.CTkButton(rowFrame, text="Delete", width=30, height=20,
                      command=lambda r=room: onDelete(r)
                      ).pack(side="left", padx=5)

        ctk.CTkButton(rowFrame, text="Edit", width=30, height=20,
                      command=lambda r=room: onEdit(r)
                      ).pack(side="left", padx=5)


# same as ROOMS
def dataLabsRight(frame, controller, refresh, data=None):
    # Note that that data here is a specefic one to display, for example a name of a lab
    # we will also treat this as a form to fill out

    rowName = ctk.CTkFrame(frame, fg_color="transparent")
    rowName.pack(fill="x", pady=5, padx=5)

    ctk.CTkLabel(rowName, text="Name:", width=120, anchor="w", font=("Arial", 30, "bold")).grid(row=0, column=0,
                                                                                                padx=10, pady=2)
    nameEntry = ctk.CTkEntry(rowName, width=350, placeholder_text="E.g: Mac", font=("Arial", 30, "bold"))
    nameEntry.grid(row=0, column=1, sticky="ew", padx=5)

    if data:
        nameEntry.insert(0, data)

    def onSave():
        name = nameEntry.get()
        if name.strip():
            if data:
                controller.editLab(data, name, refresh)
            else:
                controller.addLab(name, refresh)
        else :
            ctk.CTkLabel(frame, text="Please Input Valid Lab Name! ", width=120, anchor="w", font=("Arial", 30, "bold"), text_color = "red").grid(row=0, column=0,padx=10, pady=2)


    ctk.CTkButton(frame, text="Save Changes", width=100, font=("Arial", 20, "bold"), height=40,
                  command=lambda: onSave()
                  ).pack(side="bottom", padx=5)


# same as ROOMS
def dataLabsLeft(frame, controller, refresh, data=None):
    # Note that that data here is a list of Labs

    # I need two rows, 1 for add buttion, other for the content
    container = ctk.CTkFrame(frame, fg_color="transparent")
    container.pack(fill="both", expand=True, padx=5, pady=5)

    def onAdd():
        refresh(target="ConfigPage")

    # we are creating and puting on screen at same time with . pack here
    ctk.CTkButton(container, text="Add", width=120, height=20, command=lambda: onAdd()
                  ).pack(side="top", padx=5)

    def onDelete(lab):
        controller.removeLab(lab, refresh)

    def onEdit(lab):

        refresh(target="ConfigPage", data=lab)

    for lab in controller.listLabs():
        # Horizontal container for label  and buttons
        rowFrame = ctk.CTkFrame(container, fg_color="transparent")
        rowFrame.pack(fill="x", pady=5, padx=5)

        # Label
        ctk.CTkLabel(rowFrame, text=lab, font=("Arial", 14, "bold"), anchor="w").pack(side="left", fill="x",
                                                                                      expand=True)

        # Buttons
        ctk.CTkButton(rowFrame, text="Delete", width=30, height=20,
                      command=lambda l=lab: onDelete(l)
                      ).pack(side="left", padx=5)
        ctk.CTkButton(rowFrame, text="Edit", width=30, height=20,
                      command=lambda l=lab: onEdit(l)
                      ).pack(side="left", padx=5)


def dataCoursesLeft(frame, controller, refresh, data=None):
    container = ctk.CTkFrame(frame, fg_color="transparent")
    container.pack(fill="both", expand=True, padx=5, pady=5)

    def onAdd():
        refresh(target="ConfigPage")

    ctk.CTkButton(container, text="Add", width=120, height=20,
                  command=lambda: onAdd()).pack(side="top", padx=5)

    def onDelete(course):
        controller.removeCourse(course, refresh)

    def onEdit(course, index):
        refresh(target="ConfigPage", data={"course": course, "index": index})

    for i, course in enumerate(controller.listCourses()):
        row = ctk.CTkFrame(container, fg_color="transparent")
        row.pack(fill="x", pady=5, padx=5)

        title = f'{course.get("course_id", "(no id)")}'
        ctk.CTkLabel(row, text=title, font=("Arial", 14, "bold"), anchor="w").pack(
            side="left", fill="x", expand=True
        )

        # Delete button
        ctk.CTkButton(
            row, text="Delete", width=30, height=20,
            command=lambda c=course: onDelete(c)
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            row, text="Edit", width=30, height=20,
            command=lambda c=course, idx=i: onEdit(c, idx)
        ).pack(side="left", padx=5)


def dataCoursesRight(frame, controller, refresh, data=None):
    def split_csv(s):
        return [x.strip() for x in s.split(",") if x.strip()] if s else []

    # ✅ Handle both raw course dicts and {"course": ..., "index": ...}
    course = None
    target_index = None
    if isinstance(data, dict):
        if "course" in data and "index" in data:
            course = data["course"]
            target_index = data["index"]
        else:
            course = data
    else:
        course = data

    # --- UI fields ---
    # Course ID
    row_id = ctk.CTkFrame(frame, fg_color="transparent")
    row_id.pack(fill="x", pady=5, padx=5)
    ctk.CTkLabel(row_id, text="Course ID:", width=140, anchor="w", font=("Arial", 30, "bold")).pack(
        side="left", padx=10
    )
    entry_id = ctk.CTkEntry(row_id, placeholder_text="E.g: CMSC 140", font=("Arial", 30, "bold"))
    entry_id.pack(side="left", fill="x", expand=True)

    # Credits
    row_cr = ctk.CTkFrame(frame, fg_color="transparent")
    row_cr.pack(fill="x", pady=5, padx=5)
    ctk.CTkLabel(row_cr, text="Credits:", width=140, anchor="w", font=("Arial", 30, "bold")).pack(
        side="left", padx=10
    )
    entry_cr = ctk.CTkEntry(row_cr, placeholder_text="E.g: 4", font=("Arial", 30, "bold"))
    entry_cr.pack(side="left", fill="x", expand=True, padx=5)

    # Rooms
    row_rm = ctk.CTkFrame(frame, fg_color="transparent")
    row_rm.pack(fill="x", pady=5, padx=5)
    ctk.CTkLabel(row_rm, text="Rooms:", width=140, anchor="w", font=("Arial", 30, "bold")).pack(
        side="left", padx=10
    )
    entry_rm = ctk.CTkEntry(row_rm, placeholder_text="E.g: Roddy 136, Roddy 140", font=("Arial", 30, "bold"))
    entry_rm.pack(side="left", fill="x", expand=True, padx=5)

    # Labs
    row_lab = ctk.CTkFrame(frame, fg_color="transparent")
    row_lab.pack(fill="x", pady=5, padx=5)
    ctk.CTkLabel(row_lab, text="Labs:", width=140, anchor="w", font=("Arial", 30, "bold")).pack(
        side="left", padx=10
    )
    entry_lab = ctk.CTkEntry(row_lab, placeholder_text="E.g: Linux, Mac", font=("Arial", 30, "bold"))
    entry_lab.pack(side="left", fill="x", expand=True, padx=5)

    # Conflicts
    row_cf = ctk.CTkFrame(frame, fg_color="transparent")
    row_cf.pack(fill="x", pady=5, padx=5)
    ctk.CTkLabel(row_cf, text="Conflicts:", width=140, anchor="w", font=("Arial", 30, "bold")).pack(
        side="left", padx=10
    )
    entry_cf = ctk.CTkEntry(row_cf, placeholder_text="E.g: CMSC 161, CMSC 162", font=("Arial", 30, "bold"))
    entry_cf.pack(side="left", fill="x", expand=True, padx=5)

    # Faculty
    row_fc = ctk.CTkFrame(frame, fg_color="transparent")
    row_fc.pack(fill="x", pady=5, padx=5)
    ctk.CTkLabel(row_fc, text="Faculty:", width=140, anchor="w", font=("Arial", 30, "bold")).pack(
        side="left", padx=10
    )
    entry_fc = ctk.CTkEntry(row_fc, placeholder_text="E.g: Hardy, Zoppetti", font=("Arial", 30, "bold"))
    entry_fc.pack(side="left", fill="x", expand=True, padx=5)

    # --- Prefill when editing ---
    if course:
        entry_id.insert(0, course.get("course_id", ""))
        entry_cr.insert(0, str(course.get("credits", "")))
        entry_rm.insert(0, ", ".join(course.get("room", [])))
        entry_lab.insert(0, ", ".join(course.get("lab", [])))
        entry_cf.insert(0, ", ".join(course.get("conflicts", [])))
        entry_fc.insert(0, ", ".join(course.get("faculty", [])))

    # --- Error display ---
    error_label = ctk.CTkLabel(
        frame,
        text="",
        text_color="red",
        font=("Arial", 20, "bold"),
        wraplength=600,
        anchor="center",
        justify="center"
    )
    error_label.pack(pady=(10, 5))

    # --- Save logic ---
    def onSave():
        error_label.configure(text="")

        new_course = {
            "course_id": entry_id.get().strip(),
            "credits": entry_cr.get().strip(),
            "room": split_csv(entry_rm.get()),
            "lab": split_csv(entry_lab.get()),
            "conflicts": split_csv(entry_cf.get()),
            "faculty": split_csv(entry_fc.get()),
        }

        # Try add or edit
        if course:
            error = controller.editCourse(course.get("course_id"), new_course, refresh, target_index=target_index)
        else:
            error = controller.addCourse(new_course, refresh)

        # Display any model error inline
        if error:
            error_label.configure(text=error)

    # --- Save button ---
    ctk.CTkButton(
        frame, text="Save Changes", width=100, font=("Arial", 20, "bold"), height=40,
        command=onSave
    ).pack(side="bottom", padx=5, pady=10)


# def normalizeDayTimeSchedules(scheduleRow):


def defaultScheduleViewer(frame, schedules, pathEntaryVar):
    for idx, schedule in enumerate(schedules, start=1):
        # Tying to make actual altrenating color but looks a little ugly
        color = "#1F1E1E"
        if idx % 2 == 0:
            color = "transparent"

        # for each of the schedules we create a frame to put schedule in
        schFrame = ctk.CTkFrame(frame, fg_color=color)
        schFrame.pack(padx=(0, 10), pady=(0, 30), fill="x", expand=True)

        # in the schedule frame we will put the header frame which will schedule name,
        # and buttion to export csv or json
        scheduleHeaderFrame = ctk.CTkFrame(schFrame, fg_color="transparent")
        scheduleHeaderFrame.pack(side="top", padx=(0, 10), fill="x", expand=True)

        schedulesTitle = ctk.CTkLabel(scheduleHeaderFrame, width=100, text=f"Schedule:{idx}",
                                      font=("Arial", 15, "bold"))
        schedulesTitle.pack(side="left", padx=(0, 10), fill="x", expand=True)

        ctk.CTkButton(scheduleHeaderFrame, text="Export JSON", width=100, height=35,
                      command=lambda idx=idx: exportOneScheduleBTN(schedules, pathEntaryVar, idx)).pack(side="left",
                                                                                                        padx=(0, 10),
                                                                                                        pady=(10, 0),
                                                                                                        fill="x",
                                                                                                        expand=False)

        # Create the table frame inside schFrame
        # this is actally for the table it self
        tableFrame = ctk.CTkFrame(schFrame, fg_color="transparent", height=300)  # scrollable if many rows
        tableFrame.pack(fill="both", expand=True, padx=10, pady=10)

        # Table header
        headerFrame = ctk.CTkFrame(tableFrame)
        headerFrame.pack(fill="x", pady=(0, 2))
        columns = ["Course", "Faculty", "Room", "Lab", "Time"]
        for col in columns:
            lbl = ctk.CTkLabel(headerFrame, text=col, font=("Arial", 12, "bold"), width=120, anchor="w")
            lbl.pack(side="left", padx=5)

        # Table rows, and put in the data
        for row in schedule:
            rowFrame = ctk.CTkFrame(tableFrame)
            rowFrame.pack(fill="x", pady=1)
            for item in row:
                lbl = ctk.CTkLabel(rowFrame, text=item, font=("Arial", 12), width=120, anchor="w")
                lbl.pack(side="left", padx=5)


def roomLabsScheduleViewer(frame, schedules, pathEntaryVar):
    for idx, s in enumerate(schedules, start=1):
        # Tying to make actual altrenating color but looks a little ugly
        color = "#1F1E1E"
        if idx % 2 == 0:
            color = "transparent"

        # for each of the schedules we create a frame to put schedule in
        schFrame = ctk.CTkFrame(frame, fg_color=color)
        schFrame.pack(padx=(0, 10), pady=(0, 30), fill="x", expand=True)

        # in the schedule frame we will put the header frame which will schedule name,
        # and buttion to export csv or json
        scheduleHeaderFrame = ctk.CTkFrame(schFrame, fg_color="transparent")
        scheduleHeaderFrame.pack(side="top", padx=(0, 10), fill="x", expand=True)

        schedulesTitle = ctk.CTkLabel(scheduleHeaderFrame, width=100, text=f"Schedule:{idx}",
                                      font=("Arial", 15, "bold"))
        schedulesTitle.pack(side="left", padx=(0, 10), fill="x", expand=True)

        ctk.CTkButton(scheduleHeaderFrame, text="Export JSON", width=100, height=35,
                      command=lambda idx=idx: exportOneScheduleBTN(schedules, pathEntaryVar, idx)).pack(side="left",
                                                                                                        padx=(0, 10),
                                                                                                        pady=(10, 0),
                                                                                                        fill="x",
                                                                                                        expand=False)

        tableFrame = ctk.CTkFrame(schFrame, fg_color="transparent", height=300)  # scrollable if many rows
        tableFrame.pack(fill="both", expand=True, padx=10, pady=10)

        for room_name, labs in s.items():
            roomLabel = ctk.CTkLabel(tableFrame, text=f"Room: {room_name}", font=("Arial", 15, "bold"))
            roomLabel.pack(anchor="w", pady=(10, 2))

            for lab_name, courses in labs.items():
                labLabel = ctk.CTkLabel(tableFrame, text=f"{lab_name}", font=("Arial", 13, "bold"))
                labLabel.pack(anchor="w", padx=20, pady=(0, 5))

                # Table header
                headerFrame = ctk.CTkFrame(tableFrame)
                headerFrame.pack(fill="x", padx=30, pady=(0, 2))
                columns = ["Course", "Faculty", "Time"]
                for col in columns:
                    lbl = ctk.CTkLabel(headerFrame, text=col, font=("Arial", 12, "bold"), width=120, anchor="w")
                    lbl.pack(side="left", padx=5)

                # Table rows
                for row in courses:
                    course, faculty, room, lab, *days = row
                    rowFrame = ctk.CTkFrame(tableFrame)
                    rowFrame.pack(fill="x", padx=30, pady=1)
                    values = [course, faculty] + days
                    for item in values:
                        lbl = ctk.CTkLabel(rowFrame, text=item, font=("Arial", 12), width=120, anchor="w")
                        lbl.pack(side="left", padx=5)


def facultyScheduleViewer(frame, schedules, pathEntaryVar):
    for idx, s in enumerate(schedules, start=1):
        color = "#1F1E1E"
        if idx % 2 == 0:
            color = "transparent"

        # for each of the schedules we create a frame to put schedule in
        schFrame = ctk.CTkFrame(frame, fg_color=color)
        schFrame.pack(padx=(0, 10), pady=(0, 30), fill="x", expand=True)

        # in the schedule frame we will put the header frame which will schedule name,
        # and buttion to export csv or json
        scheduleHeaderFrame = ctk.CTkFrame(schFrame, fg_color="transparent")
        scheduleHeaderFrame.pack(side="top", padx=(0, 10), fill="x", expand=True)

        schedulesTitle = ctk.CTkLabel(scheduleHeaderFrame, width=100, text=f"Schedule:{idx}",
                                      font=("Arial", 15, "bold"))
        schedulesTitle.pack(side="left", padx=(0, 10), fill="x", expand=True)

        ctk.CTkButton(scheduleHeaderFrame, text="Export JSON", width=100, height=35,
                      command=lambda idx=idx: exportOneScheduleBTN(schedules, pathEntaryVar, idx)).pack(side="left",
                                                                                                        padx=(0, 10),
                                                                                                        pady=(10, 0),
                                                                                                        fill="x",
                                                                                                        expand=False)

        tableFrame = ctk.CTkFrame(schFrame, fg_color="transparent", height=300)  # scrollable if many rows
        tableFrame.pack(fill="both", expand=True, padx=10, pady=10)

        for faculty_name, courses in s.items():
            ctk.CTkLabel(tableFrame, text=f"{faculty_name}", font=("Arial", 15, "bold")).pack(anchor="w", pady=(10, 2))

            headerFrame = ctk.CTkFrame(tableFrame)
            headerFrame.pack(fill="x", padx=20, pady=(0, 2))
            columns = ["Course", "Room", "Lab", "Time"]
            for col in columns:
                ctk.CTkLabel(headerFrame, text=col, font=("Arial", 12, "bold"), width=120, anchor="w").pack(side="left",
                                                                                                            padx=5)

            for row in courses:
                course, room, lab, *days = row
                rowFrame = ctk.CTkFrame(tableFrame)
                rowFrame.pack(fill="x", padx=20, pady=1)
                values = [course, room, lab] + days
                for item in values:
                    ctk.CTkLabel(rowFrame, text=item, font=("Arial", 12), width=120, anchor="w").pack(side="left",
                                                                                                      padx=5)


# this is the actual App
class SchedulerApp(ctk.CTk):
    def __init__(self):
        # our apps inherates everything form ctk.CTk
        super().__init__()
        # titel
        self.title("Scheduler Application")

        # the min size
        self.geometry("1200x700")
        self.minsize(1200, 700)

        # allows us to expand left and right and make full screen
        self.resizable(True, True)

        # setting how the app looks, Dark look the best and does not hurt the eye.
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # tracks what tab we are currently on
        self.selected_tabs = {}

        # What we need to order the schedule by
        # deafult is normal as is,
        # Choices: Default, Rooms & Labs, Faculty
        self.selectedOrderBy = "Default"

        ## imported schedules
        self.schedulesImported = None
        self.schedulesImportedPath = StringVar()

        # we will keep our views to dispaly here
        self.views = {}

        # the pages
        self.createMainPage()
        self.createSchedulerPage()
        self.createConfigPage()
        self.createViewSchedulePage()

        # shows the main page in the begenning
        self.show_view("MainPage")
        self.current_view = None

    # this creates the main page
    def createMainPage(self):
        # we create a frame for this view
        frame = ctk.CTkFrame(self, fg_color="transparent")

        # save this view so we can get to it later
        self.views["MainPage"] = frame

        # creating the titel and displaying on screem
        title = ctk.CTkLabel(frame, text="Course Constraint Scheduler Companion", font=("Arial", 30, "bold"))
        title.pack(pady=40)

        # we have 3 button one for each page we can get to from miin
        # when we click the button we just show the new page
        btnEditConfig = ctk.CTkButton(frame, text="Edit Config", width=200, height=40,
                                      command=lambda: self.show_view("ConfigPage"))
        btnEditConfig.pack(pady=15)

        btnRunScheduler = ctk.CTkButton(frame, text="Run Scheduler", width=200, height=40,
                                        command=lambda: self.show_view("RunSchedulerPage"))
        btnRunScheduler.pack(pady=15)

        btnViewScheduler = ctk.CTkButton(frame, text="View Schedules", width=200, height=40,
                                         command=lambda: self.show_view("ViewSchedulePage"))
        btnViewScheduler.pack(pady=15)

    # this will create the config Page to modify/create new file
    def createConfigPage(self, data=None):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        self.views["ConfigPage"] = frame

        # For now, but shoud be in controller
        # ned this for path
        # self.configPath = StringVar()
        if self.configPath.get() == "":
            self.configPath.set(
                "Start editing this new Config File or Import your own. Press export to save new changes.")

        # Back Button (⬅), goes back to the main page
        backBtn = ctk.CTkButton(frame, text="⬅ Back", width=100, command=lambda: self.show_view("MainPage"))
        backBtn.pack(pady=10, anchor="w", padx=15)

        # This frame is for the "header", importBTN, path entry, and Export btn
        importFrame = ctk.CTkFrame(frame, fg_color="transparent")
        importFrame.pack(fill="x", padx=20, pady=5)

        # creates import btn and shows it on screen.
        importBtn = ctk.CTkButton(importFrame, text="Import Config", width=150,
                                  command=lambda: configImportBTN(self.configPath, self.refresh))
        importBtn.pack(side="left", padx=(0, 10))

        # creates path entry and shows it on screen, note state = readonly so user cant directly change
        # they must selcet proper file to show there.

        pathEntry = ctk.CTkEntry(importFrame, state="readonly", textvariable=self.configPath, width=500)
        pathEntry.pack(side="left", padx=(0, 10), fill="x", expand=True)

        # creates export btn and shows it on screen.
        exportBtn = ctk.CTkButton(importFrame, text="Export Config", width=150,
                                  command=lambda: configExportBTN(self.configPath))
        exportBtn.pack(side="left", padx=(0, 10))

        # here we have the tab view with multiple tabs.
        tabview = ctk.CTkTabview(frame)
        tabview.pack(expand=True, fill="both", pady=20, padx=20)

        tabview.add("Faculty")
        tabview.add("Courses")
        tabview.add("Rooms")
        tabview.add("Labs")

        # this sets the current tabview, to current when we refresh
        #
        if "ConfigPage" in self.selected_tabs:
            tabview.set(self.selected_tabs["ConfigPage"])

        originalCommand = tabview._segmented_button.cget("command")

        def getTabChange(tab_name):

            # original tab buttion command to use
            if callable(originalCommand):
                originalCommand(tab_name)

            self.selected_tabs["ConfigPage"] = tab_name

        tabview._segmented_button.configure(command=getTabChange)

        # we create and add tabs for  Faculty, Courses, Labs, Rooms
        # NOTE: Frame is importtant here we create the two column system, left and right frame and display those late
        #
        # we don't know the frame so it kind of like a place holder until later on in the program

        # Determine if we're editing a course
        course_data = None
        if isinstance(data, dict) and "course" in data:
            course_data = data

        # Faculty tab — only gets faculty data if data looks like a faculty dict
        faculty_data = data if isinstance(data, dict) and "name" in data else None

        self.createTwoColumn(
            tabview.tab("Faculty"),
            lambda frame: dataFacultyLeft(frame, facultyCtr, self.refresh),
            lambda frame: dataFacultyRight(frame, facultyCtr, self.refresh, faculty_data)
            #Holding this
        )

        # Courses tab — only gets course data
        self.createTwoColumn(
            tabview.tab("Courses"),
            lambda frame: dataCoursesLeft(frame, courseCtr, self.refresh),
            lambda frame: dataCoursesRight(frame, courseCtr, self.refresh, course_data)
        )

        # Rooms and Labs should never get structured dicts like {"course": ..., "index": ...}
        self.createTwoColumn(
            tabview.tab("Rooms"),
            lambda frame: dataRoomLeft(frame, roomCtr, self.refresh),
            lambda frame: dataRoomRight(frame, roomCtr, self.refresh, data if isinstance(data, str) else None)
        )

        self.createTwoColumn(
            tabview.tab("Labs"),
            lambda frame: dataLabsLeft(frame, labCtr, self.refresh),
            lambda frame: dataLabsRight(frame, labCtr, self.refresh, data if isinstance(data, str) else None)
        )

    # this is to store and return the choice to order the schedules
    def orderByChoice(self, choice, sch):
        ## This will only return the user selected choice so we know what to order by.
        self.selectedOrderBy = choice

        for widget in self.views["ViewSchedulePage"].winfo_children():
            if isinstance(widget, ctk.CTkScrollableFrame):
                widget.destroy()

        self.refresh(target="ViewSchedulePage", data=sch)
        # return choice

    def orderedSchedules(self, schedules):
        if not schedules:
            return None

        if self.selectedOrderBy == "Default":
            return schedules
        elif self.selectedOrderBy == "Rooms & Labs":
            reoderedSchedules = []
            for s in schedules:
                result = {}
                for row in s:
                    course, faculty, room, lab, *days = row
                    lab_name = lab if lab else "No Lab"

                    if room not in result:
                        result[room] = {}
                    if lab_name not in result[room]:
                        result[room][lab_name] = []

                    # Store the course data without repeating room/lab (optional)
                    result[room][lab_name].append([course, faculty] + days)

                reoderedSchedules.append(result)

            return reoderedSchedules

        elif self.selectedOrderBy == "Faculty":
            reoderedSchedules = []
            for s in schedules:
                result = {}
                for row in s:
                    course, faculty, room, lab, *days = row

                    if faculty not in result:
                        result[faculty] = []

                    result[faculty].append([course, room, lab] + days)
                reoderedSchedules.append(result)
            return reoderedSchedules

        self.refresh(target="ViewSchedulePage")

    # this will create the ViewSchedulePage
    # this view will be to strictly to view the schedules.
    def createViewSchedulePage(self, schedules=None):

        # like before make frames and save it
        frame = ctk.CTkFrame(self, fg_color="transparent")
        self.views["ViewSchedulePage"] = frame

        # This is the header stuff (back, import,export,pathentry/message), same as before
        backBtn = ctk.CTkButton(frame, text="⬅ Back", width=100, command=lambda: self.show_view("MainPage"))
        backBtn.pack(pady=10, anchor="w", padx=15)

        importFrame = ctk.CTkFrame(frame, fg_color="transparent")
        importFrame.pack(fill="x", padx=20, pady=5)

        if self.schedulesImportedPath.get() == "":
            self.schedulesImportedPath.set("View your imported or generated schedules here!")

        # self.schedulesImported = None
        def onImport():
            self.schedulesImported = importSchedulesBTN(self.schedulesImportedPath)
            if self.schedulesImported:
                self.refresh(target="ViewSchedulePage", data=self.schedulesImported)

        if self.schedulesImported:
            scheduleOdered = self.orderedSchedules(self.schedulesImported)
        else:
            scheduleOdered = self.orderedSchedules(schedules)
        # print(scheduleOdered)

        importBtn = ctk.CTkButton(importFrame, text="Import Schedules", width=150, command=onImport)
        importBtn.pack(side="left", padx=(0, 10))

        pathEntry = ctk.CTkEntry(importFrame, state="readonly", textvariable=self.schedulesImportedPath)
        pathEntry.pack(side="left", padx=(0, 10), fill="x", expand=True)

        exportBtn = ctk.CTkButton(importFrame, text="Export All", width=150,
                                  command=lambda: exportAllSchedulesBTN(schedules, self.schedulesImportedPath))
        exportBtn.pack(side="left", padx=(0, 10))

        # new things here: this make the drop down label and  it self.
        dropDownFrame = ctk.CTkFrame(importFrame, fg_color="transparent")
        dropDownFrame.pack(side="right", padx=(0, 10))
        dropDownLabel = ctk.CTkLabel(dropDownFrame, width=100, text="Order By: ", font=("Arial", 15, "bold"))
        dropDownLabel.pack(side="left", padx=(0, 10), fill="x", expand=True)
        dropdown = ctk.CTkOptionMenu(dropDownFrame, width=150, values=["Default", "Rooms & Labs", "Faculty"],
                                     command=lambda choice: self.orderByChoice(choice, scheduleOdered))
        dropdown.set(self.selectedOrderBy)
        dropdown.pack(side="left", padx=(0, 10), fill="x")

        # This the actaully for the schedule viewer now.
        # create the Frame to add the schedules to
        schedulesFrame = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        schedulesFrame.pack(expand=True, fill="both", padx=10, pady=10)

        if scheduleOdered != None:
            if self.selectedOrderBy == "Default":
                defaultScheduleViewer(schedulesFrame, scheduleOdered, self.schedulesImportedPath)
            elif self.selectedOrderBy == "Rooms & Labs":
                roomLabsScheduleViewer(schedulesFrame, scheduleOdered, self.schedulesImportedPath)

            elif self.selectedOrderBy == "Faculty":
                facultyScheduleViewer(schedulesFrame, scheduleOdered, self.schedulesImportedPath)

    def createSchedulerPage(self):
        # TODO: still have lots of work here
        # should be able to understand this now
        frame = ctk.CTkFrame(self, fg_color="transparent")
        self.views["RunSchedulerPage"] = frame

        # For now, but shoud be in controller
        self.configPath = StringVar()
        if self.configPath.get() == "" or self.configPath.get() == ".json":
            self.configPath.set("Import Config File and Generate schedules! ")
        limit = StringVar()
        optimize = IntVar()

        # Back Button (⬅)
        backBtn = ctk.CTkButton(frame, text="⬅ Back", width=100, command=lambda: self.show_view("MainPage"))
        backBtn.pack(pady=10, anchor="w", padx=15)

        importFrame = ctk.CTkFrame(frame, fg_color="transparent")
        importFrame.pack(fill="x", padx=20, pady=5)

        importBtn = ctk.CTkButton(importFrame, text="Import Config", width=150,
                                  command=lambda: configImportBTN(self.configPath))
        importBtn.pack(side="left", padx=(0, 10))

        pathEntry = ctk.CTkEntry(importFrame, state="readonly", textvariable=self.configPath, width=500)
        pathEntry.pack(side="left", padx=(0, 10), fill="x", expand=True)

        container = ctk.CTkFrame(frame)
        container.pack(expand=True, fill="both", padx=10, pady=10)

        # limit entry
        ctk.CTkLabel(container, text="How many schedules do you want to generate?", font=("Arial", 20, "bold"),
                     anchor="w"
                     ).pack(padx=(0, 10))
        limitEntry = ctk.CTkEntry(container, textvariable=limit, placeholder_text="E.g: 5", font=("Arial", 20, "bold"),
                                  width=100)
        limitEntry.pack(padx=5)

        # Optimization choice (Yes / No)
        optFrame = ctk.CTkFrame(container, fg_color="transparent")
        optFrame.pack(pady=10)

        ctk.CTkLabel(optFrame, text="Do you want to optimize schedules?",
                     font=("Arial", 20, "bold")).pack(side="left", padx=10)
        ctk.CTkRadioButton(optFrame, text="Yes", variable=optimize, value=1).pack(side="left")
        ctk.CTkRadioButton(optFrame, text="No", variable=optimize, value=0).pack(side="left")
        # generatedSch = None

        def onView():
            self.refresh(target="ViewSchedulePage", data=self.schedulesImported)

        def onGenerate():
            limit_value = limitEntry.get()
            if limit_value.isdigit():
                limit_int = int(limit_value)
                optimize_value = optimize.get()
                self.schedulesImported = generateSchedulesBtn(limit_int, optimize_value)
                ctk.CTkLabel(container, text="Click View Schedules to see them!  ", font=("Arial", 20, "bold"),
                            ).pack(padx=(0, 10))
                viewBtn = ctk.CTkButton(container, text="View Schedules",
                               font=("Arial", 20, "bold"), width=150, command=onView)
                viewBtn.pack(padx=(0, 10))
            else:
                ctk.CTkLabel(container, text="Please enter a valid number!", font=("Arial", 20, "bold"),
                             text_color="red").pack(padx=(0, 10))

        genBtn = ctk.CTkButton(importFrame, text="Generate Schedules",
                               font=("Arial", 20, "bold"), width=150, command=onGenerate)
        genBtn.pack(padx=(0, 10))

    def createTwoColumn(self, parent, popluateLeft=None, popluateRight=None):
        # This creates the look for the  confi page.

        # Container frame for left and right
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=10, pady=10)

        # Left frame which will have a Scrollable Frame, that you can scroll if data overflow
        leftFrame = ctk.CTkFrame(container, width=250, fg_color="transparent")
        leftFrame.pack(side="left", fill="y", padx=(0, 5), pady=5)
        leftFrame.pack_propagate(False)

        leftInner = ctk.CTkScrollableFrame(leftFrame, fg_color="transparent")
        leftInner.pack(expand=True, fill="both")

        # if we do have the data we can popluate the left side.
        if popluateLeft:
            popluateLeft(leftInner)

        # right Frame, similar to left
        rightFrameC = ctk.CTkFrame(container, fg_color="transparent")
        rightFrameC.pack(side="left", expand=True, fill="both", padx=(0, 5), pady=5)

        rightInner = ctk.CTkScrollableFrame(rightFrameC, fg_color="transparent")
        rightInner.pack(expand=True, fill="both")

        if popluateRight:
            popluateRight(rightInner)

    def createPartialColumn(self, parent, container, popluateLeft=None, popluateRight=None):
        # This creates the look for the  confi page.

        # Container frame for left and right
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=10, pady=10)

        # Left frame which will have a Scrollable Frame, that you can scroll if data overflow
        leftFrame = ctk.CTkFrame(container, width=250, fg_color="transparent")
        leftFrame.pack(side="left", fill="y", padx=(0, 5), pady=5)
        leftFrame.pack_propagate(False)

        leftInner = ctk.CTkScrollableFrame(leftFrame, fg_color="transparent")
        leftInner.pack(expand=True, fill="both")

        # if we do have the data we can popluate the left side.
        if popluateLeft:
            popluateLeft(leftInner)

        # right Frame, similar to left
        rightFrameC = ctk.CTkFrame(container, fg_color="transparent")
        rightFrameC.pack(side="left", expand=True, fill="both", padx=(0, 5), pady=5)

        rightInner = ctk.CTkScrollableFrame(rightFrameC, fg_color="transparent")
        rightInner.pack(expand=True, fill="both")

        if popluateRight:
            popluateRight(rightInner)

    def refresh(self, target=None, data=None):
        # this refreshes everything when we load the data or do any CRUD behaviors
        # this is a bit slow but this the best i have gotten so far.

        # we can pick a specefic page to refresh or
        # if you just do self.refresh() it will reload eveything
        if target is None:

            last_view = self.current_view or "MainPage"

            # Rebuild everything
            for name, view in list(self.views.items()):
                view.destroy()

            self.views.clear()

            # Recreate all pages
            self.createMainPage()
            self.createSchedulerPage()
            self.createConfigPage(data=data)
            self.createViewSchedulePage(schedules=data)

            # Show main page again (or keep track of last one)
            self.show_view(last_view)
        else:
            # if we do have a view to refresh 
            # we just refresh/recreate that view only
            if target in self.views:
                self.views[target].destroy()
                del self.views[target]

            if target == "MainPage":
                self.createMainPage()
            elif target == "RunSchedulerPage":
                self.createSchedulerPage()
            elif target == "ConfigPage":
                self.createConfigPage(data=data)
            elif target == "ViewSchedulePage":
                self.createViewSchedulePage(schedules=data)

            self.show_view(target)

    # this function wil show the actual views.
    def show_view(self, view_name):
        # Hide all views
        for view in self.views.values():
            view.pack_forget()
            # forget will pretty much remove everthing from the screen and when we have new screen adds that 

        # Show the selected view from list,
        # each view when we create it will add thigns on screen every cycle
        self.views[view_name].pack(expand=True, fill="both")

        self.current_view = view_name

