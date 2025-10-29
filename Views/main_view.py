# Resources: https://customtkinter.tomschimansky.com/documentation/widgets 
import customtkinter as ctk
from tkinter import StringVar, IntVar
from Controller.main_controller import (RoomsController, LabsController, FacultyController,
                                        configImportBTN, configExportBTN, generateSchedulesBtn,
                                        importSchedulesBTN, exportSchedulesBTN,
                                        CourseController)

import threading, math, re, random

from datetime import datetime


# should create controllers for other things too
roomCtr = RoomsController()
facultyCtr = FacultyController()
labCtr = LabsController()
courseCtr = CourseController()

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


def defaultScheduleViewer(frame, schedules, pathEntaryVar, idx, numOfSch, order = None):
    schedules = orderedSchedules(schedules, "Default")
    # for each of the schedules we create a frame to put schedule in
    schFrame = ctk.CTkFrame(frame, fg_color="#1F1E1E")
    schFrame.pack(padx=(0, 10), pady=(0, 30), fill="x", expand=True)

    # in the schedule frame we will put the header frame which will schedule name,
    # and buttion to export csv or json
    scheduleHeaderFrame = ctk.CTkFrame(schFrame, fg_color="transparent")
    scheduleHeaderFrame.pack(side="top", padx=(0, 10), fill="x", expand=True)

    schedulesTitle = ctk.CTkLabel(scheduleHeaderFrame, width=100, 
        text=f"Schedule:{idx + 1} of {numOfSch}",
        font=("Arial", 15, "bold"))
    
    schedulesTitle.pack(side="left", padx=(0, 10), fill="x", expand=True)

    def onView():
        plotWeeklySchedule(schedules)

    ctk.CTkButton(scheduleHeaderFrame, text="View", width=100, height=35,
        command=onView
        ).pack(side="left",padx=(0, 10),pady=(10, 0),fill="x",expand=False)

    ctk.CTkButton(scheduleHeaderFrame, text="Export", width=100, height=35,
        command=lambda: exportSchedulesBTN(schedules, pathEntaryVar)
        ).pack(side="left",padx=(0, 10),pady=(10, 0),fill="x",expand=False)

    # Create the table frame inside schFrame
    # this is actally for the table it self
    tableFrame = ctk.CTkFrame(schFrame, fg_color="transparent", height=300)  # scrollable if many rows
    tableFrame.pack(fill="both", expand=True, padx=10, pady=10)

    # Table header
    headerFrame = ctk.CTkFrame(tableFrame)
    headerFrame.pack(fill="x", pady=(0, 2))
    #columns = ["Course", "Faculty", "Room", "Lab", "Time"]
    columns = ["Course", "Faculty", "Room", "Lab", "Mon", "Tue", "Wed", "Thu", "Fri"]
    for col in columns:
        lbl = ctk.CTkLabel(headerFrame, text=col, font=("Arial", 12, "bold"), width=120, anchor="w")
        lbl.pack(side="left", padx=5)

    # Table rows, and put in the data
    days = ["MON", "TUE", "WED", "THU", "FRI"]
    for row in schedules:
        rowFrame = ctk.CTkFrame(tableFrame)
        rowFrame.pack(fill="x", pady=1)

        other = row[:4]
        times = row[4:]

        dayToTime = {t.split()[0]: t.split()[1] for t in times}
        FixedTimes = [dayToTime.get(day, '') for day in days]

        row = other + FixedTimes

        for idx, item in enumerate(row):
            lbl = ctk.CTkLabel(rowFrame, text=item, font=("Arial", 12), width=120, anchor="w")
            lbl.pack(side="left", padx=5)

def roomLabsScheduleViewer(frame, schedulesInstance, pathEntaryVar, idx, numOfSch, order):
    # for each of the schedules we create a frame to put schedule in
    schedules = orderedSchedules(schedulesInstance, order)
    schFrame = ctk.CTkFrame(frame, fg_color="#1F1E1E")
    schFrame.pack(padx=(0, 10), pady=(0, 30), fill="x", expand=True)

    # in the schedule frame we will put the header frame which will schedule name,
    # and buttion to export csv or json
    scheduleHeaderFrame = ctk.CTkFrame(schFrame, fg_color="transparent")
    scheduleHeaderFrame.pack(side="top", padx=(0, 10), fill="x", expand=True)

    schedulesTitle = ctk.CTkLabel(scheduleHeaderFrame, width=100, 
        text=f"Schedule:{idx + 1} of {numOfSch}",
        font=("Arial", 15, "bold"))
    
    schedulesTitle.pack(side="left", padx=(0, 10), fill="x", expand=True)

    def onView():
        plotWeeklySchedule(schedulesInstance)

    ctk.CTkButton(scheduleHeaderFrame, text="View", width=100, height=35,
        command=onView
        ).pack(side="left",padx=(0, 10),pady=(10, 0),fill="x",expand=False)


    ctk.CTkButton(scheduleHeaderFrame, text="Export", width=100, height=35,
        command=lambda: exportSchedulesBTN(schedulesInstance, pathEntaryVar)
        ).pack(side="left",padx=(0, 10),pady=(10, 0),fill="x",expand=False)

    tableFrame = ctk.CTkFrame(schFrame, fg_color="transparent", height=300) 
    tableFrame.pack(fill="both", expand=True, padx=10, pady=10)

    for Room, courses in schedules[0].items():
        ctk.CTkLabel(tableFrame, text=f"{Room}", font=("Arial", 15, "bold")).pack(anchor="w", pady=(10, 2))

        headerFrame = ctk.CTkFrame(tableFrame)
        headerFrame.pack(fill="x", padx=20, pady=(0, 2))
        columns = ["Course", "Faculty", "Mon", "Tue", "Wed", "Thu", "Fri"]
        daysName = ["MON", "TUE", "WED", "THU", "FRI"]
        for col in columns:
            ctk.CTkLabel(headerFrame, text=col, font=("Arial", 12, "bold"), width=120, anchor="w"
                        ).pack(side="left",padx=5)

        for row in courses:
            course, faculty, lab, *days = row
            rowFrame = ctk.CTkFrame(tableFrame)
            rowFrame.pack(fill="x", padx=20, pady=1)

            times = row[2:]

            dayToTime = {t.split()[0]: t.split()[1] for t in times}
            FixedTimes = [dayToTime.get(day, '') for day in daysName]

            values = [course, faculty] + FixedTimes
            for item in values:
                ctk.CTkLabel(rowFrame, text=item, font=("Arial", 12), 
                    width=120, anchor="w").pack(side="left",padx=5)

                


def facultyScheduleViewer(frame, schedulesInstance, pathEntaryVar, idx, numOfSch, order):
    # for each of the schedules we create a frame to put schedule in
    schedules = orderedSchedules(schedulesInstance, order)
    schFrame = ctk.CTkFrame(frame, fg_color="#1F1E1E")
    schFrame.pack(padx=(0, 10), pady=(0, 30), fill="x", expand=True)

    # in the schedule frame we will put the header frame which will schedule name,
    # and buttion to export csv or json
    scheduleHeaderFrame = ctk.CTkFrame(schFrame, fg_color="transparent")
    scheduleHeaderFrame.pack(side="top", padx=(0, 10), fill="x", expand=True)

    schedulesTitle = ctk.CTkLabel(scheduleHeaderFrame, width=100, 
        text=f"Schedule:{idx+1} of {numOfSch}",font=("Arial", 15, "bold"))
    
    schedulesTitle.pack(side="left", padx=(0, 10), fill="x", expand=True)

    def onView():
        plotWeeklySchedule(schedulesInstance)

    ctk.CTkButton(scheduleHeaderFrame, text="View", width=100, height=35,
        command=onView
        ).pack(side="left",padx=(0, 10),pady=(10, 0),fill="x",expand=False)


    ctk.CTkButton(scheduleHeaderFrame, text="Export", width=100, height=35,
        command=lambda idx=1: exportSchedulesBTN(schedulesInstance, pathEntaryVar)
        ).pack(side="left",padx=(0, 10),pady=(10, 0),fill="x",expand=False)

    tableFrame = ctk.CTkFrame(schFrame, fg_color="transparent", height=300)  
    tableFrame.pack(fill="both", expand=True, padx=10, pady=10)

    for faculty_name, courses in schedules[0].items():
        ctk.CTkLabel(tableFrame, text=f"{faculty_name}", font=("Arial", 15, "bold")).pack(anchor="w", pady=(10, 2))

        headerFrame = ctk.CTkFrame(tableFrame)
        headerFrame.pack(fill="x", padx=20, pady=(0, 2))
        columns = ["Course", "Room (lab)", "Mon", "Tue", "Wed", "Thu", "Fri"]
        daysName = ["MON", "TUE", "WED", "THU", "FRI"]
        for col in columns:
            ctk.CTkLabel(headerFrame, text=col, font=("Arial", 12, "bold"), 
                        width=120, anchor="w").pack(side="left",padx=5)

        for row in courses:
            course, room, lab, *days = row
            rowFrame = ctk.CTkFrame(tableFrame)
            rowFrame.pack(fill="x", padx=20, pady=1)

            times = row[3:]

            dayToTime = {t.split()[0]: t.split()[1] for t in times}
            FixedTimes = [dayToTime.get(day, '') for day in daysName]

            if lab in (None, "None"):
                values = [course, room] + FixedTimes
            else:
                values = [course, room + " "+ lab] + FixedTimes

            for item in values:
                ctk.CTkLabel(rowFrame, text=item, font=("Arial", 12), 
                    width=120, anchor="w").pack(side="left", padx=5)


def sortSchedulesByTime(data):
    # Priority for the days, no classes on SAT, SUN but who knows.. 
    dayOrder = {'MON': 0, 'TUE': 1, 'WED': 2, 'THU': 3, 'FRI': 4, 'SAT': 5, 'SUN': 6}
    def getEarliestMeeting(schedule):
        times = []
        for entry in schedule[4:]:
            try:
                day, time_range = entry.split()
                startTime = time_range.split('-')[0]
                hour, minute = map(int, startTime.split(':'))
                times.append((dayOrder[day], hour, minute))
            except Exception:
                continue
        return min(times) if times else (float('inf'), float('inf'), float('inf'))

    # sort using the funciton we give it, usingt he times 
    return sorted(data, key=getEarliestMeeting)



def filterDurations(times, dur):
    valid = []
    for t in times:
        t = t.replace('^', '').strip()
        try:
            day, time_range = t.split(' ')
            start, end = time_range.split('-')

            fmt = "%H:%M"
            start_time = datetime.strptime(start, fmt)
            end_time = datetime.strptime(end, fmt)

            duration = (end_time - start_time).seconds / 60
            if duration == dur:
                valid.append(t)
        except ValueError:
            continue 
    return valid

def orderedSchedules(schedules, order):
    schedules = sortSchedulesByTime(schedules)
    reoderedSchedules = []
    if not schedules:
        return schedules

    if order == "Default":
        return schedules
    else :
        result = {}
        for row in schedules:
            course, faculty, room, lab, *days = row
            if order == "Rooms & Labs":
                if room not in result:
                    result[room] = []

                result[room].append([course, faculty] + days)
            elif order == "Faculty":
                if faculty not in result:
                    result[faculty] = []

                result[faculty].append([course, room, lab] + days)

        for row in schedules:
            course, faculty, room, lab, *days = row
            if order == "Rooms & Labs":
                if lab not in (None, "None"):
                    if lab not in result:
                        result[lab] = []
                    times = filterDurations(days, 110)
                    result[lab].append([course, faculty] + times)

        reoderedSchedules.append(result)

    return reoderedSchedules
    
def plotWeeklyOrderSchedules(schedules, parentFrame, order):
    schedules = orderedSchedules(schedules, order)
    days = ["MON", "TUE", "WED", "THU", "FRI"]
    dayOrder = {d: i for i, d in enumerate(days)}
    hourHeight = 90
    dayWidth = 150
    leftMargin = 50

    def parseMeeting(meeting):
        try:
            day, times = meeting.split()
            times = times.replace('^', '')
            startStr, endStr = times.split('-')
            fmt = "%H:%M"
            start = datetime.strptime(startStr, fmt)
            end = datetime.strptime(endStr, fmt)
            return day, start, end
        except Exception:
            return None, None, None

    def getTimeRange(data):
        times = []
        time_pattern = re.compile(r'(\d{1,2}):(\d{2})-(\d{1,2}):(\d{2})')
        for _class in data:
            for item in _class:
                match = time_pattern.search(item)
                if match:
                    start_h, start_m, end_h, end_m = map(int, match.groups())
                    start = start_h + start_m / 60
                    end = end_h + end_m / 60
                    times.append((start, end))

        if not times:
            return None

        earliest_start = min(t[0] for t in times)
        latest_end = max(t[1] for t in times)
        rounded_latest_end = math.ceil(latest_end)

        return (int(earliest_start), rounded_latest_end)
        
    ctk.CTkLabel(parentFrame, text=f"By {order}:", width=120, height = 50, anchor="w", 
        font=("Arial", 30, "bold")).pack(padx = 10, pady = 10)

    for schedule_dict in schedules:
        for room, classes in schedule_dict.items():
            startHour, endHour = getTimeRange(classes)
            canvasWidth = leftMargin + len(days) * dayWidth + 20
            canvasHeight = (endHour - startHour) * hourHeight + 100

            offset = 50

            # Outer frame to center the room
            outer_frame = ctk.CTkFrame(parentFrame, fg_color="transparent")
            outer_frame.pack(pady=20)
            
            # Centered inner frame
            room_frame = ctk.CTkFrame(outer_frame, fg_color="transparent")
            room_frame.pack(anchor="n") 

            # Label for room, centered
            ctk.CTkLabel(room_frame, text=room, font=("Arial", 20, "bold")).pack(pady=5)

            # Create canvas for this room/class
            canvas = ctk.CTkCanvas(
                room_frame, width=canvasWidth, height=canvasHeight, highlightthickness=0
            )
            canvas.pack(pady=10)

            # Draw day headers
            for i, day in enumerate(days):
                x = leftMargin + i * dayWidth
                canvas.create_text(x + dayWidth/2, 20, text=day, font=("Helvetica", 12, "bold"))

            # Draw horizontal lines and time labels
            for i in range(startHour, endHour+1):
                # Bhagi's Wife helped..  :) 
                y = (i - startHour) * hourHeight  + offset
                canvas.create_text(leftMargin-5, y+10, text=f"{i:02d}:00", anchor="e", font=("Helvetica", 10))
                canvas.create_line(leftMargin, y, leftMargin + len(days)*dayWidth, y, fill="#cccccc")

            # Draw each class in this room
            COLORLIST = [
                "#6fa8dc","#93c47d","#f6b26b","#e06666","#8e7cc3",
                "#ffd966","#76a5af","#c27ba0","#a4c2f4","#b6d7a8"
            ]

            for cls in classes:
                course = cls[0]
                professor = cls[1]
                meetings = cls[2:]
                PICKEDCOLOR = COLORLIST[random.randint(0, 9)]
                for meeting in meetings:
                    day, start, end = parseMeeting(meeting)
                    if day not in dayOrder or not start or not end:
                        continue
                    
                    x = leftMargin + dayOrder[day] * dayWidth + 5
                    y = (start.hour + start.minute/60 - startHour) * hourHeight + offset
                    height = (end - start).seconds / 3600 * hourHeight - 2

                    # Rectangle for class
                    rect = canvas.create_rectangle(
                        x, y, x + dayWidth - 10, y + height,
                        fill=PICKEDCOLOR
                    )

                    # Text inside class
                    text = f"{course}\n{professor}\n{meeting.split()[1]}"
                    canvas.create_text(
                        x + (dayWidth - 10)/2, y + height/2,
                        text=text, font=("Helvetica", 9), fill="white", justify="center"
                    )



def plotWeeklySchedule(schedules):
    popup = ctk.CTkToplevel()
    popup.title("Weekly Schedule")
    popup.minsize(1200, 700)     
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    popup.attributes("-fullscreen", True)

    popup.bind("<Escape>", lambda e: popup.attributes("-fullscreen", False))

    container = ctk.CTkScrollableFrame(popup, fg_color="transparent")
    container.pack(fill="both", expand=True)

    roomFrame  = ctk.CTkFrame(container, fg_color="transparent")
    roomFrame.pack(expand = True, pady=10, padx = 10)

    plotWeeklyOrderSchedules(schedules, roomFrame, "Rooms & Labs")

    facultyFrame  = ctk.CTkFrame(container, fg_color="transparent")
    facultyFrame.pack(expand = True, pady=(10, 50), padx = 10)

    plotWeeklyOrderSchedules(schedules, facultyFrame, "Faculty")

    popup.lift()
    popup.focus_force()


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

        self.deafultSchedules = None
        self.schIndex = 0
        self.numOfSch = 0

        # we will keep our views to dispaly here
        self.views = {}

        self.createMainPage()
        self.views["MainPage"].pack(expand=True, fill="both")

    def createMainPage(self):
        # Create and store the main container
        frame = ctk.CTkFrame(self, fg_color="transparent")
        self.views["MainPage"] = frame

        tabview = ctk.CTkTabview(frame, width=1100, height=600)
        tabview.pack(expand=True, fill="both")

        tabview.add("Edit Config")
        tabview.add("Run Scheduler")
        tabview.add("View Schedules")

        self.tabview = tabview

        originalCmd = tabview._segmented_button.cget("command")

        def onTabChange(tab_name):
            if callable(originalCmd):
                originalCmd(tab_name)
            self.selected_tabs["MainPage"] = tab_name

        tabview._segmented_button.configure(command=onTabChange)

        self.createConfigPage(parent = tabview.tab("Edit Config"))
        self.createSchedulerPage(parent = tabview.tab("Run Scheduler"))
        self.createViewSchedulePage(parent = tabview.tab("View Schedules"))


    # this will create the config Page to modify/create new file
    def createConfigPage(self,  parent=None , data=None):
        parent = parent or self
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.views["ConfigPage"] = frame
        frame.pack(expand=True, fill="both")
        # For now, but shoud be in controller
        # ned this for path
        self.configPath = StringVar()
        if self.configPath.get() == "":
            self.configPath.set(
                "Start editing this new Config File or Import your own. Press export to save new changes.")

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
        # NOTE: Frame is importtant here we create the two column system, 
        # eft and right frame and display those late
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
        self.selectedOrderBy = choice
        self.refresh(target="ViewSchedulePage", data=sch)


    # this will create the ViewSchedulePage
    # this view will be to strictly to view the schedules.
    def createViewSchedulePage(self,  parent=None , schedules=None):

        parent = parent or self
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        self.views["ViewSchedulePage"] = frame
        frame.pack(expand=True, fill="both")

        importFrame = ctk.CTkFrame(frame, fg_color="transparent")
        importFrame.pack(fill="x", padx=20, pady=5)

        if self.schedulesImportedPath.get() == "":
            self.schedulesImportedPath.set("View your imported or generated schedules here!")

        # self.schedulesImported = None
        def onImport():
            self.schedulesImported = importSchedulesBTN(self.schedulesImportedPath)
            if self.schedulesImported:
                self.numOfSch = len(self.schedulesImported)
                self.refresh(target="ViewSchedulePage", data=self.schedulesImported)

        if self.schedulesImported and len(self.schedulesImported) > 0:
            self.numOfSch = len(self.schedulesImported)
            # clamp index in case it got out of range previously
            self.schIndex = self.schIndex % self.numOfSch  
            #scheduleOdered = orderedSchedules(self.schedulesImported[self.schIndex])
            self.deafultSchedules = self.schedulesImported
        else:
            self.numOfSch = len(schedules) if schedules else 0
            self.schIndex = 0
            self.deafultSchedules = schedules
            #scheduleOdered = self.orderedSchedules(schedules) if schedules else []

        importBtn = ctk.CTkButton(importFrame, text="Import Schedules", width=150, command=onImport)
        importBtn.pack(side="left", padx=(0, 10))

        pathEntry = ctk.CTkEntry(importFrame, state="readonly", textvariable=self.schedulesImportedPath)
        pathEntry.pack(side="left", padx=(0, 10), fill="x", expand=True)

        exportBtn = ctk.CTkButton(importFrame, text="Export All", width=150,
            command=lambda: exportSchedulesBTN(self.deafultSchedules, self.schedulesImportedPath))
        
        exportBtn.pack(side="left", padx=(0, 10))  

        # new things here: this make the drop down label and  it self.
        dropDownFrame = ctk.CTkFrame(importFrame, fg_color="transparent")
        dropDownFrame.pack(side="right", padx=(0, 10))
        dropDownLabel = ctk.CTkLabel(dropDownFrame, width=100, text="Order By: ", font=("Arial", 15, "bold"))
        dropDownLabel.pack(side="left", padx=(0, 10), fill="x", expand=True)
        dropdown = ctk.CTkOptionMenu(dropDownFrame, width=150, 
            values=["Default", "Rooms & Labs", "Faculty"],
            command=lambda choice: self.orderByChoice(choice, self.deafultSchedules))
        dropdown.set(self.selectedOrderBy)
        dropdown.pack(side="left", padx=(0, 10), fill="x")

        # This the actaully for the schedule viewer now.
        # create the Frame to add the schedules to
        schedulesFrame = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        schedulesFrame.pack(expand=True, fill="both", padx=10, pady=10)

        if self.deafultSchedules != None and self.deafultSchedules != {} and self.deafultSchedules != []:
            if self.selectedOrderBy == "Default":
                defaultScheduleViewer(
                    schedulesFrame, self.deafultSchedules[self.schIndex], 
                    self.schedulesImportedPath,self.schIndex, 
                    self.numOfSch
                )

            elif self.selectedOrderBy == "Rooms & Labs":
                roomLabsScheduleViewer(
                    schedulesFrame, self.deafultSchedules[self.schIndex], 
                    self.schedulesImportedPath, self.schIndex, 
                    self.numOfSch, self.selectedOrderBy
                    )
                
            elif self.selectedOrderBy == "Faculty":
                facultyScheduleViewer(
                    schedulesFrame, self.deafultSchedules[self.schIndex], 
                    self.schedulesImportedPath, self.schIndex, 
                    self.numOfSch, self.selectedOrderBy
                    )

        nextPrevious = ctk.CTkFrame(frame, fg_color="transparent")
        nextPrevious.pack(pady=10) 

        buttons_frame = ctk.CTkFrame(nextPrevious, fg_color="transparent")
        buttons_frame.pack(anchor="center")
        state = "normal" if self.numOfSch > 1 else "disabled"

        def changeSchedule(direction):
            if self.numOfSch == 0:
                return
            
            # direction = +1 for next, -1 for previous
            self.schIndex = (self.schIndex + direction) % self.numOfSch  
            self.refresh(target="ViewSchedulePage", data=None)

        previousBTN = ctk.CTkButton(buttons_frame, text="Previous", width=150,
            state = state, command=lambda: changeSchedule(-1))
        previousBTN.pack(side="left", padx=(0, 10))


        nextBTN = ctk.CTkButton(buttons_frame, text="Next", width=150,
            state = state, command=lambda: changeSchedule(1))
        nextBTN.pack(side="left", padx=(10, 0))

    def createSchedulerPage(self, parent = None):
        # should be able to understand this now
        parent = parent or self
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        #self.views["RunSchedulerPage"] = frame
        frame.pack(expand=True, fill="both")

        # For now, but shoud be in controller
        self.configPath = StringVar()
        if self.configPath.get() == "" or self.configPath.get() == ".json":
            self.configPath.set("Import Config File and Generate schedules! ")
        limit = StringVar()

        importFrame = ctk.CTkFrame(frame, fg_color="transparent")
        importFrame.pack(fill="x", padx=20, pady=5)

        importBtn = ctk.CTkButton(importFrame, text="Import Config", width=150,
            command=lambda: configImportBTN(self.configPath))
        
        importBtn.pack(side="left", padx=(0, 10))

        pathEntry = ctk.CTkEntry(importFrame, state="readonly", textvariable=self.configPath, width=500)
        pathEntry.pack(side="left", padx=(0, 10), fill="x", expand=True)

        # Use a scrollable container so many generated results / buttons remain reachable
        container = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=10, pady=10)

        # limit entry
        ctk.CTkLabel(container, text="How many schedules do you want to generate?", 
            font=("Arial", 20, "bold"), anchor="w").pack(padx=(0, 10))
        limitEntry = ctk.CTkEntry(container, textvariable=limit, 
            placeholder_text="E.g: 5", font=("Arial", 20, "bold"),width=100)
        
        limitEntry.pack(padx=5)

        # Helper text explaining how generating multiple schedule instances works
        ctk.CTkLabel(container, text="(When generating multiple schedule instances, the most recent generation will be at the bottom)", font=("Arial", 15, "bold", "underline"), justify="left", text_color="cyan").pack(padx=(0,10))
        optFrame = ctk.CTkFrame(container, fg_color="transparent")
        optFrame.pack(pady=0)

        optimizeList = [ "faculty_course","faculty_room","faculty_lab","same_room","same_lab","pack_rooms", "pack_labs" ]
        optimizeVars = {}  # store variables for each checkbox

        optionsFrame = ctk.CTkFrame(optFrame, fg_color="transparent")
        optionsFrame.pack(padx=20, pady=0, fill="x")

        ctk.CTkLabel(optionsFrame, text="Optimization Options", font=("Arial", 18, "bold")).pack(anchor="w", pady=(0,5))

        for opt in optimizeList:
            var = ctk.BooleanVar(value=False)
            checkbox = ctk.CTkCheckBox(optionsFrame, text=opt.replace("_", " ").title(), variable=var)
            checkbox.pack(anchor="w", pady=2)
            optimizeVars[opt] = var

        # These lines create a (for now) invisible progress bar
        progress_bar = ctk.CTkProgressBar(container, width=400, progress_color = "green")
        progress_bar.set(0)
        def onView():
            self.refresh(target="ViewSchedulePage", data=self.schedulesImported)
            if hasattr(self, 'tabview'):
                self.tabview.set("View Schedules")

        # Defines what happens when the generate button is clicked
        def onGenerate():
            selectedOpts = [key for key, var in optimizeVars.items() if var.get()]
            #print("Selected optimizations:", selectedOpts)
            limit_value = limitEntry.get()
            if limit_value.isdigit():
                limit_int = int(limit_value)
                status_label = ctk.CTkLabel(container, text="Starting generation...", font=("Arial", 18, "bold"))
                status_label.pack(pady=(10, 0))

                progress_bar.pack(pady=15)
                progress_bar.set(0)
                progress_bar.configure(mode="determinate")

                # Disable buttons during generation
                genBtn.configure(state="disabled")
                importBtn.configure(state="disabled")

                # Update UI immediately
                container.update_idletasks()

                # Create a simple progress callback that updates UI
                has_opt = bool(selectedOpts)
                def progress_callback(current_step, total_steps):
                    progress_bar.set(current_step / total_steps)
                    
                    if has_opt and current_step == 1:
                        status_label.configure(text="Creating optimization goals...")
                    else:
                        schedule_num = current_step - (1 if has_opt else 0)
                        status_label.configure(text=f"Generating schedule {schedule_num}/{limit_int}")
                    
                    # Force UI update after each progress update
                    container.update_idletasks()

                try:
                    # Check if config file is loaded before starting generation
                    if self.configPath.get() == "" or self.configPath.get() == ".json" or "Import Config File" in self.configPath.get():
                        raise ValueError("No configuration file loaded. Please import a config file first!")
                    # This will block the UI but show progress updates
                    self.schedulesImported = generateSchedulesBtn(limit_int, selectedOpts, progress_callback)
                    
                    # Final updates
                    status_label.configure(text="All schedules generated successfully!")
                    progress_bar.set(1)

                    generation_successful = True
                except ValueError as e:
                    # Handle the specific "no config file" error
                    if "No configuration file" in str(e):
                        status_label.configure(text="Error: No configuration file loaded!")
                        status_label.configure(text_color="red")
                        # You could also show a more detailed message
                        ctk.CTkLabel(container, text="Please click 'Import Config' and select a valid config file", 
                                    font=("Arial", 16), text_color="yellow").pack(padx=(0, 10))
                    else:
                        status_label.configure(text=f"Error: {str(e)}")
                        status_label.configure(text_color="red")
                    generation_successful = False
                    
                except Exception as e:
                    status_label.configure(text=f"Error during generation: {str(e)}")
                    status_label.configure(text_color="red")
                    generation_successful = False
                    
                finally:
                    # Hide progress bar and show completion UI
                    progress_bar.pack_forget()
                    
                    # Re-enable buttons
                    genBtn.configure(state="normal")
                    importBtn.configure(state="normal")
                    # Only show completion UI if generation was successful
                    if generation_successful:
                        # Show completion message and button
                        ctk.CTkLabel(container, text="Click View Schedules to see them!", 
                                    font=("Arial", 20, "bold")).pack(padx=(0, 10))
                        viewBtn = ctk.CTkButton(container, text="View Schedules", width=150,
                                            command=onView)
                        viewBtn.pack(padx=(0, 10))

            else:
                ctk.CTkLabel(container, text="Please enter a valid number!", font=("Arial", 20, "bold"),
                            text_color="red").pack(padx=(0, 10))

        genBtn = ctk.CTkButton(importFrame, text="Generate Schedules",
                             width=150, command=onGenerate)
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

    def refresh(self, target=None, data=None):
            if target is None:
                for name, view in list(self.views.items()):
                    view.destroy()

                self.views.clear()

                self.createMainPage()
                
                # Repack the main view
                self.views["MainPage"].pack(expand=True, fill="both")

            elif target in self.views:
                self.views[target].destroy()
                del self.views[target]
                
                tab_parent = None
                if hasattr(self, 'tabview'):
                    if target == "ConfigPage":
                        tab_parent = self.tabview.tab("Edit Config")
                    elif target == "RunSchedulerPage":
                        tab_parent = self.tabview.tab("Run Scheduler")
                    elif target == "ViewSchedulePage":
                        tab_parent = self.tabview.tab("View Schedules")

                if tab_parent is None and target != "MainPage":
                    print(f"Error: Could not find tab parent for {target}")
                    return
                if target == "MainPage":
                    self.createMainPage()
                    self.views["MainPage"].pack(expand=True, fill="both") # Repack it
                elif target == "RunSchedulerPage":
                    self.createSchedulerPage(parent=tab_parent)
                elif target == "ConfigPage":
                    self.createConfigPage(parent=tab_parent, data=data)
                elif target == "ViewSchedulePage":
                    self.createViewSchedulePage(parent=tab_parent, schedules=data)
