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


    # This is to display the credit thigns  
    rowCredits = ctk.CTkFrame(frame, fg_color="transparent")
    rowCredits.pack(fill="x", pady=5, padx=5)

    ctk.CTkLabel(rowCredits, text="Minimum Credits:", font=("Arial", 30, "bold")).grid(row=0, column=0, padx=10, pady=2, sticky="w")
    minEntry = ctk.CTkEntry(rowCredits, placeholder_text="E.g: 4", font=("Arial", 30, "bold"))
    minEntry.grid(row=0, column=1, sticky="ew", padx=5)

    ctk.CTkLabel(rowCredits, text="Maximum Credits:", font=("Arial", 30, "bold")).grid(row=1, column=0, padx=10, pady=2, sticky="w")
    maxEntry = ctk.CTkEntry(rowCredits, placeholder_text="E.g: 12", font=("Arial", 30, "bold"))
    maxEntry.grid(row=1, column=1, sticky="ew", padx=5)

    ctk.CTkLabel(rowCredits, text="Unique Course Limit:", font=("Arial", 30, "bold")).grid(row=2, column=0, padx=10, pady=2, sticky="w")
    uniqueEntry = ctk.CTkEntry(rowCredits, placeholder_text="E.g: 3", font=("Arial", 30, "bold"))
    uniqueEntry.grid(row=2, column=1, sticky="ew", padx=5)

    rowCredits.grid_columnconfigure(1, weight=1)

    if data:
        minEntry.insert(0, data.get("minimum_credits", ""))
        maxEntry.insert(0, data.get("maximum_credits", ""))
        uniqueEntry.insert(0, data.get("unique_course_limit", ""))


    # time avavlity
    rowAvailability = ctk.CTkFrame(frame, fg_color="transparent")
    rowAvailability.pack(fill="x", pady=5, padx=5)
    ctk.CTkLabel(rowAvailability, text="Availability (MON-FRI):", anchor="w", font=("Arial", 30, "bold")).pack(anchor="w", padx=10, pady=(2,0))

    availabilityEntries = {}
    days = ["MON", "TUE", "WED", "THU", "FRI"]
    for day in days:
        dayFrame = ctk.CTkFrame(rowAvailability, fg_color="transparent")
        dayFrame.pack(fill="x", padx=20, pady=(0,2))
        ctk.CTkLabel(dayFrame, text=f"{day}:", width=50, anchor="w", font=("Arial", 25, "bold")).pack(side="left")
        dayEntry = ctk.CTkEntry(dayFrame, placeholder_text="E.g: 8:00-10:00, 12:30-5:00", font=("Arial", 30, "bold"))
        dayEntry.pack(side="left", fill="x", expand=True)
        if data and "times" in data:
            dayEntry.insert(0, ', '.join(data["times"].get(day, [])))
        availabilityEntries[day] = dayEntry

    # course Prefrence
    rowCourse = ctk.CTkFrame(frame, fg_color="transparent")
    rowCourse.pack(fill="x", pady=5, padx=5)

    ctk.CTkLabel(rowCourse, text="Course Preferences:", anchor="w", font=("Arial", 30, "bold")).pack(anchor="w", padx=10, pady=(2, 5))

    if data and "course_preferences" in data:
        for course, weight in data["course_preferences"].items():
            courseRow = ctk.CTkFrame(rowCourse, fg_color="transparent")
            courseRow.pack(fill="x", padx=20, pady=2)

            ctk.CTkLabel(courseRow, text=f"{course}:", anchor="w", width=150, font=("Arial", 25, "bold")).grid(row=0, column=0, sticky="w")

            weightEntry = ctk.CTkEntry(courseRow, width=80, justify="center", font=("Arial", 25, "bold"))
            weightEntry.grid(row=0, column=1, sticky="w", padx=5)

            weightEntry.insert(0, str(weight))

    # room Prefrence
    rowRoom = ctk.CTkFrame(frame, fg_color="transparent")
    rowRoom.pack(fill="x", pady=5, padx=5)

    ctk.CTkLabel(rowRoom, text="Room Preferences:", anchor="w", font=("Arial", 30, "bold")).pack(anchor="w", padx=10, pady=(2, 5))

    if data and "room_preferences" in data:
        for room, weight in data["room_preferences"].items():
            roomRow = ctk.CTkFrame(rowRoom, fg_color="transparent")
            roomRow.pack(fill="x", padx=20, pady=2)

            ctk.CTkLabel(roomRow, text=room, anchor="w", width=150,  font=("Arial", 25, "bold")).grid(row=0, column=0, sticky="w")

            weightEntry = ctk.CTkEntry(roomRow, width=80, justify="center",  font=("Arial", 25, "bold"))
            weightEntry.grid(row=0, column=1, sticky="w", padx=5)

            weightEntry.insert(0, str(weight))

    # Lab Prefrence
    rowLab = ctk.CTkFrame(frame, fg_color="transparent")
    rowLab.pack(fill="x", pady=5, padx=5)

    ctk.CTkLabel(rowLab, text="Lab Preferences:", anchor="w", font=("Arial", 30, "bold")).pack(anchor="w", padx=10, pady=(2, 5))

    if data and "lab_preferences" in data:
        for lab, weight in data["lab_preferences"].items():
            labRow = ctk.CTkFrame(rowLab, fg_color="transparent")
            labRow.pack(fill="x", padx=20, pady=2)

            ctk.CTkLabel(labRow, text=lab, anchor="w", width=150,  font=("Arial", 25, "bold")).grid(row=0, column=0, sticky="w")

            weightEntry = ctk.CTkEntry(labRow, width=80, justify="center",  font=("Arial", 25, "bold"))
            weightEntry.grid(row=0, column=1, sticky="w", padx=5)

            weightEntry.insert(0, str(weight))

    ctk.CTkButton(frame, text="Save Changes", width=100, font=("Arial", 20, "bold"), height = 40, command=lambda: print(f"Save chagnes conteoller")).pack(side="bottom", padx=5)



def dataRoomRight(frame, data= None):


    container = ctk.CTkFrame(frame, fg_color="transparent")
    container.pack(fill="x", pady=5, padx=5)

    ctk.CTkLabel(container, text="Name:", width=120, anchor="w", font=("Arial", 30, "bold")).grid(row=0, column=0, padx=10, pady=2)
    nameEntry = ctk.CTkEntry(container, width=350, placeholder_text="E.g: Roddy 140",font=("Arial", 30, "bold") )
    nameEntry.grid(row=0, column=1, sticky="ew", padx=5)

    ctk.CTkButton(frame, text="Save Changes", width=100, font=("Arial", 20, "bold"), height = 40, command=lambda: print(f"Save chagnes conteoller for Rooms ")).pack(side="bottom", padx=5)


def dataRoomLeft(frame, data=None):

    # I need two rows, 1 for add buttion, other for the content
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




def dataLabsRight(frame, data= None):
    # Note that that data here is a specefic one to display, for example a name of a lab
    # we will also treat this as a form to fill out

    rowName = ctk.CTkFrame(frame, fg_color="transparent")
    rowName.pack(fill="x", pady=5, padx=5)

    ctk.CTkLabel(rowName, text="Name:", width=120, anchor="w", font=("Arial", 30, "bold")).grid(row=0, column=0, padx=10, pady=2)
    nameEntry = ctk.CTkEntry(rowName, width=350, placeholder_text="E.g: Mac",font=("Arial", 30, "bold") )
    nameEntry.grid(row=0, column=1, sticky="ew", padx=5)

    ctk.CTkButton(frame, text="Save Changes", width=100, font=("Arial", 20, "bold"), height = 40, command=lambda: print(f"Save chagnes conteoller for labs")).pack(side="bottom", padx=5)


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

    




class SchedulerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Scheduler Application")
        self.geometry("1200x700")
        self.minsize(1200,700)
        self.resizable(True, True)
        ctk.set_appearance_mode("dark")   
        ctk.set_default_color_theme("dark-blue") 

        self.views = {}

        # the pages
        self.createMainPage()
        self.createSchedulerPage()
        self.createConfigPage()
        self.createViewSchedulePage()

        self.show_view("MainPage")

        # What we need to order the schedule by
        # deafult is normal as is,
        # Choices: Default, Room & Labs, Faculty
        self.selectedOrderBy = "Default"

    def createMainPage(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        self.views["MainPage"] = frame

        title = ctk.CTkLabel(frame, text="Course Constraint Scheduler Companion", font=("Arial", 30, "bold"))
        title.pack(pady=40)

        btnEditConfig = ctk.CTkButton(frame, text="Edit Config", width=200, height=40, command=lambda: self.show_view("ConfigPage"))
        btnEditConfig.pack(pady=15)

        btnRunScheduler = ctk.CTkButton(frame, text="Run Scheduler", width=200, height=40, command=lambda: self.show_view("RunSchedulerPage") )
        btnRunScheduler.pack(pady=15)

        btnViewScheduler = ctk.CTkButton(frame, text="View Schedules", width=200, height=40, command=lambda: self.show_view("ViewSchedulePage") )
        btnViewScheduler.pack(pady=15)


    def createConfigPage(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        self.views["ConfigPage"] = frame

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

        tabview = ctk.CTkTabview(frame)
        tabview.pack(expand=True, fill="both", pady=20, padx=20)


        tabview.add("Faculty")
        # we don't know the frame so it kind of like a place holder until later on in the program
        self.createTwoColumn(tabview.tab("Faculty"), dataFacultyLeft, lambda frame: dataFacultyRight(frame))

        tabview.add("Courses")
        self.createTwoColumn(tabview.tab("Courses"))

        tabview.add("Rooms")
        self.createTwoColumn(tabview.tab("Rooms"), lambda frame:dataRoomLeft(frame), lambda frame:dataRoomRight(frame))

        tabview.add("Labs") 
        self.createTwoColumn(tabview.tab("Labs"), lambda frame:dataLabsLeft(frame, data=Labs), lambda frame:dataLabsRight(frame, data=Labs))

    def orderByChoice(self, choice):
        ## This will only return the user selected choice so we know what to order by. 
        self.selectedOrderBy = choice
        print(choice)
        return choice

    def createViewSchedulePage(self):
        # this view will be to strictly to view the schedules. 
        frame = ctk.CTkFrame(self, fg_color="transparent")
        self.views["ViewSchedulePage"] = frame

        # This is the header stuff (back, import,export,pathentry/message)
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

        dropDownFrame = ctk.CTkFrame(importFrame, fg_color="transparent")
        dropDownFrame.pack(side="right", padx=(0,10))
        dropDownLabel = ctk.CTkLabel(dropDownFrame, width = 100, text="Order By: ", font=("Arial", 15, "bold"))
        dropDownLabel.pack(side="left", padx=(0,10), fill="x", expand=True)
        dropdown = ctk.CTkOptionMenu(dropDownFrame, width=150, values=["Deafult", "Rooms & Labs", "Faculty"],  command= lambda choice: self.orderByChoice(choice))
        dropdown.set("Default")
        dropdown.pack(side="left", padx=(0,10), fill="x")



        # This the actaully for the schedule viewer now. 
        schedulesFrame = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        schedulesFrame.pack(expand=True,  fill="both", padx=10, pady=10)

        for idx, schedule in enumerate(scheduleExample, start=1):
            
            color = "#1F1E1E"
            if idx % 2 == 0:
                color = "transparent"

            schFrame = ctk.CTkFrame(schedulesFrame, fg_color = color)
            schFrame.pack(padx=(0,10), pady=(0, 30), fill="x", expand=True)

            scheduleHeaderFrame = ctk.CTkFrame(schFrame, fg_color="transparent")
            scheduleHeaderFrame.pack(side="top", padx=(0,10), fill="x", expand=True)

            schedulesTitle = ctk.CTkLabel(scheduleHeaderFrame, width = 100, text=f"Schedule:{idx}", font=("Arial", 15, "bold"))
            schedulesTitle.pack(side="left", padx=(0,10), fill="x", expand=True)

            ctk.CTkButton(scheduleHeaderFrame, text="Export CSV", width=100, height=35, command=lambda: print(f"Export CSV {idx}")).pack(side="left", padx=(0,10), pady=(10,0), fill="x", expand=False)
            ctk.CTkButton(scheduleHeaderFrame, text="Export JSON", width=100, height=35, command=lambda: print(f"Export JSON {idx}")).pack(side="left", padx=(0,10), pady=(10,0),fill="x", expand=False)

            # Create the table frame inside schFrame
            tableFrame = ctk.CTkFrame(schFrame, fg_color="transparent", height=300)  # scrollable if many rows
            tableFrame.pack(fill="both", expand=True, padx=10, pady=10)

            # Table header
            headerFrame = ctk.CTkFrame(tableFrame)
            headerFrame.pack(fill="x", pady=(0,2))
            columns = ["Course", "Faculty", "Room", "Lab", "Mon", "Tue", "Wed", "Thu", "Fri"]
            for col in columns:
                lbl = ctk.CTkLabel(headerFrame, text=col, font=("Arial", 12, "bold"), width=120, anchor="w")
                lbl.pack(side="left", padx=5)

            # Table rows
            for row in schedule:
                rowFrame = ctk.CTkFrame(tableFrame)
                rowFrame.pack(fill="x", pady=1)
                for item in row:
                    lbl = ctk.CTkLabel(rowFrame, text=item, font=("Arial", 12), width=120, anchor="w")
                    lbl.pack(side="left", padx=5)


    def createSchedulerPage(self):
        #TODO: still have lots of work here
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

        # CTkScrollableFrame exists, just using it

        # Container frame for left and right
        container = ctk.CTkFrame(parent, fg_color="transparent")
        container.pack(expand=True, fill="both", padx=10, pady=10)

        # Left frame
        leftFrame = ctk.CTkFrame(container, width=250,fg_color =  "transparent")
        leftFrame.pack(side="left", fill="y", padx=(0,5), pady=5)
        leftFrame.pack_propagate(False)

        leftInner = ctk.CTkScrollableFrame(leftFrame, fg_color="transparent")
        leftInner.pack(expand=True, fill="both")
        if popluateLeftData:
            popluateLeftData(leftInner)

        # right Frame
        rightFrameC = ctk.CTkFrame(container,fg_color =  "transparent")
        rightFrameC.pack(side="left", expand=True, fill="both", padx=(0,5), pady=5)

        rightInner = ctk.CTkScrollableFrame(rightFrameC, fg_color="transparent")
        rightInner.pack(expand=True, fill="both")

        if popluateRightData:
            popluateRightData(rightInner)

    def show_view(self, view_name):
        # Hide all views
        for view in self.views.values():
            view.pack_forget()

        # Show the selected view from list
        self.views[view_name].pack(expand=True, fill="both")

