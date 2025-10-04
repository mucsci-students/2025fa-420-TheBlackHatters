# Resourses: https://customtkinter.tomschimansky.com/documentation/widgets 
import customtkinter as ctk
from tkinter import Canvas, StringVar


# Dummy Data to just put something in the forms i will create
# This data is just for testing Purpuses! 
Rooms = ["Roddy 136","Roddy 140","Roddy 147", "Roddy 1","Roddy 2","Roddy 3"]
Labs = ["Linux","Mac"]
Courses = [
           {    "course_id": "CMSC 140",
                "credits": 4,
                "room": ["Roddy 136","Roddy 140","Roddy 147"],
                "lab": [],
                "conflicts": [ "CMSC 161","CMSC 162"],
                "faculty": []
            },
            {   "course_id": "CMSC 140",
                "credits": 4,
                "room": ["Roddy 136","Roddy 140","Roddy 147"],
                "lab": [],
                "conflicts": ["CMSC 161","CMSC 162"],
                "faculty": []
            }]

Faculty = [
            {   "name": "Zoppetti",
                "maximum_credits": 12,
                "minimum_credits": 12,
                "unique_course_limit": 3,
                "times": {
                    "MON": ["11:00-16:00"],
                    "TUE": [],
                    "WED": ["10:00-15:00"],
                    "THU": ["10:00-17:00"],
                    "FRI": ["11:00-16:00"]},
                "course_preferences": {"CMSC 362": 5,"CMSC 476": 5,"CMSC 161": 4},
                "room_preferences": {"Roddy 136": 5,"Roddy 140": 1,"Roddy 147": 1},
                "lab_preferences": {"Linux": 5,"Mac": 1}
            },
            {   "name": "Hardy",
                "maximum_credits": 14,
                "minimum_credits": 12,
                "unique_course_limit": 2,
                "times": {
                    "MON": ["09:00-15:00"],
                    "TUE": ["09:00-15:00"],
                    "WED": ["09:00-15:00"],
                    "THU": [],
                    "FRI": ["09:00-15:00"]},
                "course_preferences": {"CMSC 140": 5,"CMSC 152": 4},
                "room_preferences": {"Roddy 147": 10,"Roddy 140": 1, "Roddy 136": 1},
                "lab_preferences": { "Linux": 3, "Mac": 3}
            },
            {   "name": "Ho",
                "maximum_credits": 12,
                "minimum_credits": 12,
                "unique_course_limit": 3,
                "times": {
                    "MON": ["11:00-16:00"],
                    "TUE": [],
                    "WED": ["10:00-15:00"],
                    "THU": ["10:00-17:00"],
                    "FRI": ["11:00-16:00"]},
                "course_preferences": {"CMSC 362": 5,"CMSC 476": 5,"CMSC 161": 4},
                "room_preferences": {"Roddy 136": 5,"Roddy 140": 1,"Roddy 147": 1},
                "lab_preferences": {"Linux": 5,"Mac": 1}
            },
]
scheduleExample =     [[
        ["CMSC 140.01","Hardy","Roddy 147","None","MON 13:00-13:50","WED 13:00-14:50","FRI 13:00-13:50"],
        ["CMSC 140.02","Hardy","Roddy 147","None","MON 13:00-13:50","WED 13:00-14:50","FRI 13:00-13:50"],
        ["CMSC 152.01","Hardy","Roddy 147","Mac","MON 11:00-11:50","TUE 10:00-11:50^","FRI 11:00-11:50"],
        ["CMSC 161.01","Zoppetti","Roddy 136","Linux","MON 14:00-14:50","THU 13:10-15:00^","FRI 14:00-14:50"],
        ["CMSC 161.02","Wertz","Roddy 147","Linux","TUE 08:00-09:50","THU 08:00-09:50"]],

        [       
        ["CMSC 140.01","Hardy2","Roddy 1147","None","MON 13:00-13:50","WED 13:00-14:50","FRI 13:00-13:50"],
        ["CMSC 140.02","Hardy2","Roddy 1147","None","MON 13:00-13:50","WED 13:00-14:50","FRI 13:00-13:50"],
        ["CMSC 152.01","Hardy2","Roddy 1147","Mac","MON 11:00-11:50","TUE 10:00-11:50^","FRI 11:00-11:50"],
        ["CMSC 161.01","Zoppetti2","Roddy 1136","Linux","MON 14:00-14:50","THU 13:10-15:00^","FRI 14:00-14:50"],
        ["CMSC 161.02","Wertz2","Roddy 1147","Linux","TUE 08:00-09:50","THU 08:00-09:50"]
        ],
        [       
        ["CMSC 140.01","Hardy2","Roddy 1147","None","MON 13:00-13:50","WED 13:00-14:50","FRI 13:00-13:50"],
        ["CMSC 140.02","Hardy2","Roddy 1147","None","MON 13:00-13:50","WED 13:00-14:50","FRI 13:00-13:50"],
        ["CMSC 152.01","Hardy2","Roddy 1147","Mac","MON 11:00-11:50","TUE 10:00-11:50^","FRI 11:00-11:50"],
        ["CMSC 161.01","Zoppetti2","Roddy 1136","Linux","MON 14:00-14:50","THU 13:10-15:00^","FRI 14:00-14:50"],
        ["CMSC 161.02","Wertz2","Roddy 1147","Linux","TUE 08:00-09:50","THU 08:00-09:50"]
        ]]


# The config page has left/right. This function when called with with data will fill the left side. 
# right now we are not using the data varabale and just working with dummy data. 
# frame: the place we are going to put all out stuff.
# facultyData: will contain the faculty data for all faculty..  
def dataFacultyLeft(frame, facultyData = None):

    # we create a container to put everything inside, this container lives inside the frame
    # with .pack we display the continer on the screen(fill="both": fills the x and y direction,
    # expand=True: allows it to expand when we change the screen size. padx/y = 5: adds 5px padding on all sides :)
    container = ctk.CTkFrame(frame, fg_color =  "transparent")
    container.pack(fill="both", expand=True, padx=5, pady=5)

    # we are creating and puting on screen at same time with .pack. 
    # Button lives in container we crated above
    # Button has text "Add" inside it
    # *** Command = Function: Important we need to make this functional, 
    # TODO: We need this button to on the right generate empty form on right for user to add a new faculty
    ctk.CTkButton(container, text="Add", width= 120, height = 20, command=lambda: print(f"Add Button conteoller")).pack(side="top", padx=5)

    # TODO: we need to loop throught the facultyData and show the names of the faculty
    # This will loop thought the facultyData and display the names on the left side 
    for faculty in Faculty:
        
        # For each faculty member I need their name, edit and delete btn. 
        # I need to create a fram to put thoses element. 
        # fg_color =  "transparent" mean this frame I am creating has no color. 
        rowFrame = ctk.CTkFrame(container, fg_color =  "transparent")
        rowFrame.pack(fill="x", pady=5, padx=5)

        # This is a Label, text showen on screen! 
        # Label lives inside the rowFrame we created above, text is the name
        # TODO: chanage the faculty["name"] put the actualy name when we change the loop later
        ctk.CTkLabel(rowFrame, text=faculty["name"], font=("Arial", 14, "bold"), anchor="w").pack(side="left", fill="x", expand=True)

        # Buttons. The two buttions are for deleting and editing Faculty.
        # TODO: We need ot add the commnd Function. 
        # Again .pack displays on screen, we are adding both buttons on rowFrame
        ctk.CTkButton(rowFrame, text="Delete", width=30, height = 20, command=lambda faculty: print(f"Delete Button conteoller")).pack(side="left", padx=5)
        ctk.CTkButton(rowFrame, text="Edit", width=30,  height = 20, command=lambda faculty: print(f"Edit Button conteoller")).pack(side="left", padx=5)


# This function will populate the right side of the page. (If you don't understand left and right load the program and go into config file. Should make sence once you see it!)
# this function kinda of acts like a form for user to fill. 
# we need to display the current data if user pressed edit on button before or just get an empty one
def dataFacultyRight(frame, data=None):


    # This is for the name of faculty: which has a lebel and entry;
    # it will look somehting like this: Name:__E.g: Hobbs_______
    # Again we create a frame to add the label and entry. 
    rowName = ctk.CTkFrame(frame, fg_color="transparent")
    rowName.pack(fill="x", pady=5, padx=5)

    # this is the label for Name. 
    # We just create and display the label here
    ctk.CTkLabel(rowName, text="Name:", width=120, anchor="w", font=("Arial", 30, "bold")).pack(side = "left", padx=10, pady=(0, 2))

    # this is for and entry, this is where the user can write things in 
    # TODO: get what the user had typed in and validate what the user has put when click save buttion at the bottom
    nameEntry = ctk.CTkEntry(rowName, placeholder_text="E.g: Hobbs",font=("Arial", 30, "bold") )
    nameEntry.pack(side="left", fill="x", expand=True, padx=5)


    # if we have data given here we just display the data
    # for example when someone clicks edit. 
    if data:
        nameEntry.insert(0, data.get("name", ""))


    # This is to display the credit things   
    # we need to place, Label and Entry to for each of those we need a frame 
    # we put those two things in the frame and show it on the screen. 
    rowCredits = ctk.CTkFrame(frame, fg_color="transparent")
    rowCredits.pack(fill="x", pady=5, padx=5, expand = True)

    ctk.CTkLabel(rowCredits, text="Min Credits:", font=("Arial", 30, "bold")).pack(side="left", fill = "x",padx=5)
    minEntry = ctk.CTkEntry(rowCredits, placeholder_text="E.g: 4", font=("Arial", 30, "bold"))
    minEntry.pack(side="left", fill="x", expand=True, padx=5)

    rowCredits = ctk.CTkFrame(frame, fg_color="transparent")
    rowCredits.pack(fill="x", pady=5, padx=5, expand = True)

    # same things for Max Credits 
    ctk.CTkLabel(rowCredits, text="Max Credits:", font=("Arial", 30, "bold")).pack( side = "left",fill = "x", padx=5)
    maxEntry = ctk.CTkEntry(rowCredits, placeholder_text="E.g: 12", font=("Arial", 30, "bold"))
    maxEntry.pack(side="left", fill="x", expand=True, padx=5)

    # same things for Unique Course Limit:
    rowCredits = ctk.CTkFrame(frame, fg_color="transparent")
    rowCredits.pack(fill="x", pady=5, padx=5, expand = True)

    ctk.CTkLabel(rowCredits, text="Unique Course Limit:", font=("Arial", 30, "bold")).pack( side = "left", fill = "x", padx=5)
    uniqueEntry = ctk.CTkEntry(rowCredits, placeholder_text="E.g: 3", font=("Arial", 30, "bold"))
    uniqueEntry.pack(side="left", fill="x", expand=True, padx=5)

    # TODO: Actally put the data in the entrys, if there is data given
    if data:
        minEntry.insert(0, data.get("minimum_credits", ""))
        maxEntry.insert(0, data.get("maximum_credits", ""))
        uniqueEntry.insert(0, data.get("unique_course_limit", ""))


    # Again we create row frame for the time availability, that will hold eveything for time
    # Wa also add a label with the text Availability (MON-FRI), and font and put on screen. 
    rowAvailability = ctk.CTkFrame(frame, fg_color="transparent")
    rowAvailability.pack(fill="x", pady=5, padx=5)
    ctk.CTkLabel(rowAvailability, text="Availability (MON-FRI):", anchor="w", font=("Arial", 30, "bold")).pack(anchor="w", padx=10, pady=(2,0))


    # now this will actally put the times from the data 
    # we will just loop through the days
    days = ["MON", "TUE", "WED", "THU", "FRI"]

    # in the for loop we create a frame again for each day, with label and engry
    for day in days:
        dayFrame = ctk.CTkFrame(rowAvailability, fg_color="transparent")
        dayFrame.pack(fill="x", padx=20, pady=(0,2))

        # Label for the day
        ctk.CTkLabel(dayFrame, text=f"{day}:", width=50, anchor="w", font=("Arial", 25, "bold")).pack(side="left")

        # entry for each of the day and show it on screen
        dayEntry = ctk.CTkEntry(dayFrame, placeholder_text="E.g: 8:00-10:00, 12:30-5:00", font=("Arial", 30, "bold"))
        dayEntry.pack(side="left", fill="x", expand=True)

        # this will display the given data if we do give it data,
        # other wise is just empty
        if data and "times" in data:
            dayEntry.insert(0, ', '.join(data["times"].get(day, [])))

    # Course Prefrence Frame. We create it and pack in on screen
    # In side this frame we will write everything for course_preferences
    rowCourse = ctk.CTkFrame(frame, fg_color="transparent")
    rowCourse.pack(fill="x", pady=5, padx=5)

    # this is just creating label with text: Course Preferences
    ctk.CTkLabel(rowCourse, text="Course Preferences:", anchor="w", font=("Arial", 30, "bold")).pack(anchor="w", padx=10, pady=(2, 5))

    # TODO: Need to make sure this works with actual data, not data for testing purposes, Faculty
    # we seperate with course and weight for each item in data
    dummyData = Faculty[0].get("course_preferences")
    for course, weight in dummyData.items():
        # Again we create a row frame to put the label and weight in. 
        courseRow = ctk.CTkFrame(rowCourse, fg_color="transparent")
        courseRow.pack(fill="x", padx=20, pady=2)

        # we create the label, with the couse name, and also create entry for user input
        # TODO: this course need to be form the list of courese. 
        ctk.CTkLabel(courseRow, text=f"{course}:", anchor="w", width=150, font=("Arial", 25, "bold")).pack( side="left", padx=20, pady=2)
        dropdown = ctk.CTkOptionMenu(courseRow, width=150, values=["1","2","3","4","5", "6", "7","8","9", "10"])

        if data:
            dropdown.set(str(weight))
        else:
            # deafult 
            dropdown.set("5")
        dropdown.pack(side="left", padx=(0,10), fill="x")



    # room Prefrence EXACT SAME THING AS ABOVE(Course Prefrence)
    rowRoom= ctk.CTkFrame(frame, fg_color="transparent")
    rowRoom.pack(fill="x", pady=5, padx=5)

    ctk.CTkLabel(rowRoom, text="Room Preferences:", anchor="w", font=("Arial", 30, "bold")).pack(anchor="w", padx=10, pady=(2, 5))
    dummyData = Faculty[0].get("room_preferences")
    for room, weight in dummyData.items():
        roomRow = ctk.CTkFrame(rowRoom, fg_color="transparent")
        roomRow.pack(fill="x", padx=20, pady=2)

        ctk.CTkLabel(roomRow, text=f"{room}:", anchor="w", width=150, font=("Arial", 25, "bold")).pack( side="left", padx=20, pady=2)
        dropdown = ctk.CTkOptionMenu(roomRow, width=150, values=["1","2","3","4","5", "6", "7","8","9", "10"])

        if data:
            dropdown.set(str(weight))
        else:
            # deafult 
            dropdown.set("5")
        dropdown.pack(side="left", padx=(0,10), fill="x")

    # Lab Prefrence EXACT SAME THING AS ABOVE (Course Prefrence and Room Preferences)
    rowLab = ctk.CTkFrame(frame, fg_color="transparent")
    rowLab.pack(fill="x", pady=5, padx=5)

    ctk.CTkLabel(rowLab, text="Lab Preferences:", anchor="w", font=("Arial", 30, "bold")).pack(anchor="w", padx=10, pady=(2, 5))
    dummyData = Faculty[0].get("lab_preferences")
    print(dummyData)
    for lab, weight in dummyData.items():
        labRow = ctk.CTkFrame(rowLab, fg_color="transparent")
        labRow.pack(fill="x", padx=20, pady=2)

        ctk.CTkLabel(labRow, text=f"{lab}:", anchor="w", width=150, font=("Arial", 25, "bold")).pack( side="left", padx=20, pady=2)
        dropdown = ctk.CTkOptionMenu(labRow, width=150, values=["1","2","3","4","5", "6", "7","8","9", "10"])

        if data:
            dropdown.set(str(weight))
        else:
            # deafult 
            dropdown.set("5")
        dropdown.pack(side="left", padx=(0,10), fill="x")

    # this is the save buttion that will save changes when we add a new faculty and when we modify existing
    # TODO: need to make the button work
    ctk.CTkButton(frame, text="Save Changes", width=100, font=("Arial", 20, "bold"), height = 40, command=lambda: print(f"Save chagnes conteoller")).pack(side="bottom", padx=5)


# this function will fill in the data on the right side of the two column 
def dataRoomRight(frame, data= None):

    # we should know what this does by now. 
    # we make a frame to lay things on top
    container = ctk.CTkFrame(frame, fg_color="transparent")
    container.pack(fill="x", pady=5, padx=5)

    # we put a label, and entry for name. 
    ctk.CTkLabel(container, text="Name:", width=120, anchor="w", font=("Arial", 30, "bold")).grid(row=0, column=0, padx=10, pady=2)
    nameEntry = ctk.CTkEntry(container, width=350, placeholder_text="E.g: Roddy 140",font=("Arial", 30, "bold") )
    nameEntry.grid(row=0, column=1, sticky="ew", padx=5)

    # Button to save Changes
    # TODO: Need to add command properly. 
    ctk.CTkButton(frame, text="Save Changes", width=100, font=("Arial", 20, "bold"), height = 40, command=lambda: print(f"Save chagnes conteoller for Rooms ")).pack(side="bottom", padx=5)

# This function is to popluate the left side of the screen.
# pretty much same things as above. 
def dataRoomLeft(frame, data=None):

    # frame to put everything in
    container = ctk.CTkFrame(frame, fg_color =  "transparent")
    container.pack(fill="both", expand=True, padx=5, pady=5)

    ctk.CTkButton(container, text="Add", width= 120, height = 20, command=lambda: print(f"Add Button conteoller")).pack(side="top", padx=5)

    for room in Rooms:
        # Horizontal container for label  and buttons
        rowFrame = ctk.CTkFrame(container, fg_color =  "transparent")
        rowFrame.pack(fill="x", pady=5, padx=5)

        # Label
        ctk.CTkLabel(rowFrame, text=room, font=("Arial", 14, "bold"), anchor="w").pack(side="left", fill="x", expand=True)

        # Buttons to edit and delete
        ctk.CTkButton(rowFrame, text="Delete", width=30, height = 20, command=lambda faculty: print(f"Delete Button conteoller")).pack(side="left", padx=5)
        ctk.CTkButton(rowFrame, text="Edit", width=30,  height = 20, command=lambda faculty: print(f"Edit Button conteoller")).pack(side="left", padx=5)



# same as ROOMS
def dataLabsRight(frame, data= None):
    # Note that that data here is a specefic one to display, for example a name of a lab
    # we will also treat this as a form to fill out

    rowName = ctk.CTkFrame(frame, fg_color="transparent")
    rowName.pack(fill="x", pady=5, padx=5)

    ctk.CTkLabel(rowName, text="Name:", width=120, anchor="w", font=("Arial", 30, "bold")).grid(row=0, column=0, padx=10, pady=2)
    nameEntry = ctk.CTkEntry(rowName, width=350, placeholder_text="E.g: Mac",font=("Arial", 30, "bold") )
    nameEntry.grid(row=0, column=1, sticky="ew", padx=5)

    ctk.CTkButton(frame, text="Save Changes", width=100, font=("Arial", 20, "bold"), height = 40, command=lambda: print(f"Save chagnes conteoller for labs")).pack(side="bottom", padx=5)

# same as ROOMS
def dataLabsLeft(frame, data=None):
    # Note that that data here is a list of Labs 

    # I need two rows, 1 for add buttion, other for the content
    container = ctk.CTkFrame(frame, fg_color =  "transparent")
    container.pack(fill="both", expand=True, padx=5, pady=5)

    # we are creating and puting on screen at same time with . pack here
    ctk.CTkButton(container, text="Add", width= 120, height = 20, command=lambda: print(f"Add Button conteoller")).pack(side="top", padx=5)

    for d in data:
        # Horizontal container for label  and buttons
        rowFrame = ctk.CTkFrame(container, fg_color =  "transparent")
        rowFrame.pack(fill="x", pady=5, padx=5)

        # Label
        ctk.CTkLabel(rowFrame, text=d, font=("Arial", 14, "bold"), anchor="w").pack(side="left", fill="x", expand=True)

        # Buttons
        ctk.CTkButton(rowFrame, text="Delete", width=30, height = 20, command=lambda faculty: print(f"Delete Button conteoller")).pack(side="left", padx=5)
        ctk.CTkButton(rowFrame, text="Edit", width=30,  height = 20, command=lambda faculty: print(f"Edit Button conteoller")).pack(side="left", padx=5)

def dataCoursesLeft(frame, courseData=None):
    # List of courses on the left + an add button
    container = ctk.CTkFrame(frame, fg_color="transparent")
    container.pack(fill="both", expand=True, padx=5, pady=5)

    ctk.CTkButton(
        container, text="Add", width=120, height=20,
        command=lambda: print("Add Course clicked")
    ).pack(side="top", padx=5)

    # use provided data or fallback to global dummy Courses
    course_list = courseData if courseData is not None else Courses

    for idx, course in enumerate(course_list):
        row = ctk.CTkFrame(container, fg_color="transparent")
        row.pack(fill="x", pady=5, padx=5)

        # Show ex "CMSC 140"
        title = f'{course.get("course_id","(no id)")}'
        ctk.CTkLabel(row, text=title, font=("Arial", 14, "bold"), anchor="w").pack(
            side="left", fill="x", expand=True
        )

        # Wire up buttons as needed later
        ctk.CTkButton(
            row, text="Delete", width=30, height=20,
            command=lambda i=idx: print(f"Delete Course index={i}")
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            row, text="Edit", width=30, height=20,
            command=lambda crs=course: print(f"Edit Course {crs.get('course_id','')}")  # hook to load right side
        ).pack(side="left", padx=5)


def dataCoursesRight(frame, data=None):
    # Right pane form for a single course (new or edit)

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

    # Conflicts (comma separated course IDs)
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

    # Prefill when editing
    if data:
        entry_id.insert(0, data.get("course_id", ""))
        entry_cr.insert(0, str(data.get("credits", "")))
        entry_rm.insert(0, ", ".join(data.get("room", [])))
        entry_lab.insert(0, ", ".join(data.get("lab", [])))
        entry_cf.insert(0, ", ".join(data.get("conflicts", [])))
        entry_fc.insert(0, ", ".join(data.get("faculty", [])))

    # Save button (hook up to controller later)
    ctk.CTkButton(
        frame, text="Save Changes", width=100, font=("Arial", 20, "bold"), height=40,
        command=lambda: print("Save Course clicked")
    ).pack(side="bottom", padx=5, pady=10)
    

# this is the actual App
class SchedulerApp(ctk.CTk):
    def __init__(self):
        # our apps inherates everything form ctk.CTk
        super().__init__()
        # titel 
        self.title("Scheduler Application")

        # the min size
        self.geometry("1200x700")
        self.minsize(1200,700)

        # allows us to expand left and right and make full screen
        self.resizable(True, True)

        # setting how the app looks, Dark look the best and does not hurt the eye. 
        ctk.set_appearance_mode("dark")   
        ctk.set_default_color_theme("dark-blue") 

        # we will keep our views to dispaly here
        self.views = {}

        # the pages 
        self.createMainPage()
        self.createSchedulerPage()
        self.createConfigPage()
        self.createViewSchedulePage()

        # shows the main page in the begenning 
        self.show_view("MainPage")

        # What we need to order the schedule by
        # deafult is normal as is,
        # Choices: Default, Room & Labs, Faculty
        self.selectedOrderBy = "Default"

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
        btnEditConfig = ctk.CTkButton(frame, text="Edit Config", width=200, height=40, command=lambda: self.show_view("ConfigPage"))
        btnEditConfig.pack(pady=15)

        btnRunScheduler = ctk.CTkButton(frame, text="Run Scheduler", width=200, height=40, command=lambda: self.show_view("RunSchedulerPage") )
        btnRunScheduler.pack(pady=15)

        btnViewScheduler = ctk.CTkButton(frame, text="View Schedules", width=200, height=40, command=lambda: self.show_view("ViewSchedulePage") )
        btnViewScheduler.pack(pady=15)


    # this will create the config Page to modify/create new file
    def createConfigPage(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        self.views["ConfigPage"] = frame

        # For now, but shoud be in controller 
        # ned this for path
        # self.configPath = StringVar()

        # Back Button (⬅), goes back to the main page
        backBtn = ctk.CTkButton(frame, text="⬅ Back", width=100,command=lambda: self.show_view("MainPage"))
        backBtn.pack(pady=10, anchor="w", padx=15)

        # This frame is for the "header", importBTN, path entry, and Export btn
        importFrame = ctk.CTkFrame(frame, fg_color="transparent")
        importFrame.pack(fill="x", padx=20, pady=5)

        #creates import btn and shows it on screen.
        importBtn = ctk.CTkButton(importFrame, text="Import Config", width=150, command=lambda: self.functionHereIDkRN)
        importBtn.pack(side="left", padx=(0,10))    

        #creates path entry and shows it on screen, note state = readonly so user cant directly change
        # they must selcet proper file to show there. 
        pathEntry = ctk.CTkEntry(importFrame,  state="readonly", textvariable=self.configPath, width=500)
        pathEntry.pack(side="left", padx=(0,10), fill="x", expand=True)

        #creates export btn and shows it on screen.
        exportBtn = ctk.CTkButton(importFrame, text="Export Config", width=150, command=lambda: self.functionHereIDkRN)
        exportBtn.pack(side="left", padx=(0,10))

        # here we have the tab view with multiple tabs. 
        tabview = ctk.CTkTabview(frame)
        tabview.pack(expand=True, fill="both", pady=20, padx=20)

        # we create and add tabs for  Faculty, Courses, Labs, Rooms
        # NOTE: Frame is importtant here we create the two column system, left and right frame and display those late
        # 
        tabview.add("Faculty")
        # we don't know the frame so it kind of like a place holder until later on in the program
        self.createTwoColumn(tabview.tab("Faculty"),lambda frame:dataFacultyLeft(frame), lambda frame: dataFacultyRight(frame))

        tabview.add("Courses")
        self.createTwoColumn(tabview.tab("Courses"),lambda frame: dataCoursesLeft(frame, courseData=Courses), lambda frame: dataCoursesRight(frame))  # shows empty form by default

        tabview.add("Rooms")
        self.createTwoColumn(tabview.tab("Rooms"), lambda frame:dataRoomLeft(frame), lambda frame:dataRoomRight(frame))

        tabview.add("Labs") 
        self.createTwoColumn(tabview.tab("Labs"), lambda frame:dataLabsLeft(frame, data=Labs), lambda frame:dataLabsRight(frame, data=Labs))

    # this is to store and return the choice to order the schedules 
    def orderByChoice(self, choice):
        ## This will only return the user selected choice so we know what to order by. 
        self.selectedOrderBy = choice
        print(choice)
        return choice

    # this will create the ViewSchedulePage
    # this view will be to strictly to view the schedules. 
    def createViewSchedulePage(self):

        # like before make frames and save it 
        frame = ctk.CTkFrame(self, fg_color="transparent")
        self.views["ViewSchedulePage"] = frame

        # This is the header stuff (back, import,export,pathentry/message), same as before
        backBtn = ctk.CTkButton(frame, text="⬅ Back", width=100, command=lambda: self.show_view("MainPage"))
        backBtn.pack(pady=10, anchor="w", padx=15)

        importFrame = ctk.CTkFrame(frame, fg_color =  "transparent")
        importFrame.pack(fill="x", padx=20, pady=5)

        importBtn = ctk.CTkButton(importFrame, text="Import Schedules", width=150, command=lambda: self.functionHereIDkRN)
        importBtn.pack(side="left", padx=(0,10))    

        pathEntry = ctk.CTkEntry(importFrame,  state="readonly", textvariable=self.configPath)
        pathEntry.pack(side="left", padx=(0,10), fill="x", expand=True)

        importBtn = ctk.CTkButton(importFrame, text="Export All", width=150, command=lambda: self.functionHereIDkRN)
        importBtn.pack(side="left", padx=(0,10))      

        # new things here: this make the drop down label and  it self. 
        dropDownFrame = ctk.CTkFrame(importFrame, fg_color="transparent")
        dropDownFrame.pack(side="right", padx=(0,10))
        dropDownLabel = ctk.CTkLabel(dropDownFrame, width = 100, text="Order By: ", font=("Arial", 15, "bold"))
        dropDownLabel.pack(side="left", padx=(0,10), fill="x", expand=True)
        dropdown = ctk.CTkOptionMenu(dropDownFrame, width=150, values=["Deafult", "Rooms & Labs", "Faculty"],  command= lambda choice: self.orderByChoice(choice))
        dropdown.set("Default")
        dropdown.pack(side="left", padx=(0,10), fill="x")



        # This the actaully for the schedule viewer now. 
        # create the Frame to add the schedules to 
        schedulesFrame = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        schedulesFrame.pack(expand=True,  fill="both", padx=10, pady=10)

        # for each of the schedules in our files or generated ones 
        # we use enumerate, makes it easier to keep track of index and value at that index
        for idx, schedule in enumerate(scheduleExample, start=1):

            # Tying to make actual altrenating color but looks a little ugly
            color = "#1F1E1E"
            if idx % 2 == 0:
                color = "transparent"

            # for each of the schedules we create a frame to put schedule in 
            schFrame = ctk.CTkFrame(schedulesFrame, fg_color = color)
            schFrame.pack(padx=(0,10), pady=(0, 30), fill="x", expand=True)

            # in the schedule frame we will put the header frame which will schedule name, 
            # and buttion to export csv or json
            scheduleHeaderFrame = ctk.CTkFrame(schFrame, fg_color="transparent")
            scheduleHeaderFrame.pack(side="top", padx=(0,10), fill="x", expand=True)

            schedulesTitle = ctk.CTkLabel(scheduleHeaderFrame, width = 100, text=f"Schedule:{idx}", font=("Arial", 15, "bold"))
            schedulesTitle.pack(side="left", padx=(0,10), fill="x", expand=True)

            ctk.CTkButton(scheduleHeaderFrame, text="Export CSV", width=100, height=35, command=lambda: print(f"Export CSV {idx}")).pack(side="left", padx=(0,10), pady=(10,0), fill="x", expand=False)
            ctk.CTkButton(scheduleHeaderFrame, text="Export JSON", width=100, height=35, command=lambda: print(f"Export JSON {idx}")).pack(side="left", padx=(0,10), pady=(10,0),fill="x", expand=False)

            # Create the table frame inside schFrame
            # this is actally for the table it self 
            tableFrame = ctk.CTkFrame(schFrame, fg_color="transparent", height=300)  # scrollable if many rows
            tableFrame.pack(fill="both", expand=True, padx=10, pady=10)

            # Table header
            headerFrame = ctk.CTkFrame(tableFrame)
            headerFrame.pack(fill="x", pady=(0,2))
            columns = ["Course", "Faculty", "Room", "Lab", "Mon", "Tue", "Wed", "Thu", "Fri"]
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


    def createSchedulerPage(self):
        #TODO: still have lots of work here
        # should be able to understand this now
        frame = ctk.CTkFrame(self, fg_color="transparent")
        self.views["RunSchedulerPage"] = frame

        # For now, but shoud be in controller 
        self.configPath = StringVar()

        # Back Button (⬅)
        backBtn = ctk.CTkButton(frame, text="⬅ Back", width=100,command=lambda: self.show_view("MainPage"))
        backBtn.pack(pady=10, anchor="w", padx=15)


        importFrame = ctk.CTkFrame(frame, fg_color="transparent")
        importFrame.pack(fill="x", padx=20, pady=5)
        importBtn = ctk.CTkButton(importFrame, text="Import Config", width=150, command=lambda: self.functionHereIDkRN)
        importBtn.pack(side="left", padx=(0,10))    

        pathEntry = ctk.CTkEntry(importFrame,  state="readonly", textvariable=self.configPath, width=500)
        pathEntry.pack(side="left", padx=(0,10), fill="x", expand=True)

        exportBtn = ctk.CTkButton(importFrame, text="Export Config", width=150, command=lambda: self.functionHereIDkRN)
        exportBtn.pack(side="left", padx=(0,10))

        container = ctk.CTkFrame(frame)
        container.pack(expand=True, fill="both", padx=10, pady=10)

    
    def createTwoColumn(self, parent, popluateLeftData = None, popluateRightData = None):
        # This creates the look for the  confi page. 

        # Container frame for left and right
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=10, pady=10)

        # Left frame which will have a Scrollable Frame, that you can scroll if data overflow
        leftFrame = ctk.CTkFrame(container, width=250,fg_color =  "transparent")
        leftFrame.pack(side="left", fill="y", padx=(0,5), pady=5)
        leftFrame.pack_propagate(False)

        leftInner = ctk.CTkScrollableFrame(leftFrame, fg_color="transparent")
        leftInner.pack(expand=True, fill="both")

        # if we do have the data we can popluate the left side. 
        if popluateLeftData:
            popluateLeftData(leftInner)

        # right Frame, similar to left 
        rightFrameC = ctk.CTkFrame(container,fg_color =  "transparent")
        rightFrameC.pack(side="left", expand=True, fill="both", padx=(0,5), pady=5)

        rightInner = ctk.CTkScrollableFrame(rightFrameC, fg_color="transparent")
        rightInner.pack(expand=True, fill="both")

        if popluateRightData:
            popluateRightData(rightInner)

    # this function wil show the actual views.
    def show_view(self, view_name):
        # Hide all views
        for view in self.views.values():
            view.pack_forget()
            # forget will pretty much remove everthing from the screen and when we have new screen adds that 

        # Show the selected view from list,
        # each view when we create it will add thigns on screen every cycle
        self.views[view_name].pack(expand=True, fill="both")

