# Resourses: https://customtkinter.tomschimansky.com/documentation/widgets 
import customtkinter as ctk
from tkinter import Canvas, StringVar


# Dummy Data to just put something here:
Rooms = ["Roddy 136","Roddy 140","Roddy 147"]
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


def dataFacultyLeft(frame):
    # we are creating and puting on screen at same time with . pack here
    for faculty in Faculty:
        # Horizontal container for label  and buttons
        rowFrame = ctk.CTkFrame(frame, fg_color =  "transparent")
        rowFrame.pack(fill="x", pady=5, padx=5)

        # Label
        ctk.CTkLabel(rowFrame, text=faculty["name"], font=("Arial", 14, "bold"), anchor="w").pack(side="left", fill="x", expand=True)

        # Buttons
        ctk.CTkButton(rowFrame, text="Delete", width=30, height = 20, command=lambda f=faculty: print(f"Delete Button conteoller")).pack(side="left", padx=5)
        ctk.CTkButton(rowFrame, text="Edit", width=30,  height = 20, command=lambda f=faculty: print(f"Edit Button conteoller")).pack(side="left", padx=5)

def dataFacultyRight(frame, data=None):
    pass

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

        self.show_view("MainPage")

    def createMainPage(self):
        frame = ctk.CTkFrame(self)
        self.views["MainPage"] = frame

        title = ctk.CTkLabel(frame, text="Course Constraint Scheduler Companion", font=("Arial", 30, "bold"))
        title.pack(pady=40)

        btnEditConfig = ctk.CTkButton(frame, text="Edit Config", width=200, height=40, command=lambda: self.show_view("ConfigPage"))
        btnEditConfig.pack(pady=15)

        btnRunScheduler = ctk.CTkButton(frame, text="Run Scheduler", width=200, height=40, command=lambda: self.show_view("SchedulerPage") )
        btnRunScheduler.pack(pady=15)

    def createConfigPage(self):
        frame = ctk.CTkFrame(self)
        self.views["ConfigPage"] = frame

        # For now, but shoud be in controller 
        self.configPath = StringVar()

        # Back Button (⬅)
        backBtn = ctk.CTkButton(frame, text="⬅ Back", width=100,command=lambda: self.show_view("MainPage"))
        backBtn.pack(pady=10, anchor="w", padx=15)


        importFrame = ctk.CTkFrame(frame)
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
        self.createTwoColumn(tabview.tab("Faculty"), dataFacultyLeft, lambda frame: dataFacultyRight(frame, data=Faculty[0]))

        tabview.add("Courses")
        self.createTwoColumn(tabview.tab("Courses"))

        tabview.add("Rooms")
        self.createTwoColumn(tabview.tab("Rooms"))

        tabview.add("Labs")
        self.createTwoColumn(tabview.tab("Labs"))


    def createSchedulerPage(self):
        frame = ctk.CTkFrame(self)
        self.views["SchedulerPage"] = frame

        backBtn = ctk.CTkButton(frame, text="⬅ Back", width=100, command=lambda: self.show_view("MainPage"))
        backBtn.pack(pady=10, anchor="w", padx=15)

        lbl = ctk.CTkLabel(frame, text="Run Scheduler/ Page", font=("Arial", 20, "bold"))
        lbl.pack(pady=40)

        ctk.CTkButton(frame, text="Save Schedules .. ", width=200).pack(pady=30)
    
    def createTwoColumn(self, parent, popluateLeftData = None, popluateRightData = None):

        # Container frame for left and right
        container = ctk.CTkFrame(parent)
        container.pack(expand=True, fill="both", padx=10, pady=10)

        # Left frame
        leftFrame = ctk.CTkFrame(container, width=250,fg_color =  "transparent")
        leftFrame.pack(side="left", fill="y", padx=(0,5), pady=5)
        leftFrame.pack_propagate(False)

        # Right frame 
        rightFrame = ctk.CTkFrame(container, fg_color =  "transparent")
        rightFrame.pack(side="left", expand=True, fill="both", padx=(5,0), pady=5)

        # Scrollable Left Frame, might not need it if not enought items
        leftCanvas = Canvas(leftFrame, bg="#2b2b2b")
        leftScroll = ctk.CTkScrollbar(leftFrame, command=leftCanvas.yview, fg_color =  "transparent")
        leftScroll.pack(side="right", fill="y")
        leftCanvas.pack(side="left", fill="both", expand=True)
        leftCanvas.configure(yscrollcommand=leftScroll.set)

        leftInner = ctk.CTkFrame(leftCanvas, fg_color =  "transparent")
        leftCanvas.create_window((0,0), window=leftInner, anchor="nw")

        # Placeholder iterms for the left side. needs to get info from file then read
        if popluateLeftData:
            popluateLeftData(leftInner)

        leftInner.update_idletasks()
        leftCanvas.config(scrollregion=leftCanvas.bbox("all"))
        self.scrollbarVisibility(leftCanvas, leftScroll)

        # Scrollable Right Frame, might not need again
        rightCanvas = Canvas(rightFrame, bg="#1f1f1f")
        rightScroll = ctk.CTkScrollbar(rightFrame, command=rightCanvas.yview)
        rightScroll.pack(side="right", fill="y")
        rightCanvas.pack(side="left", fill="both", expand=True)
        rightCanvas.configure(yscrollcommand=rightScroll.set)

        rightInner = ctk.CTkFrame(rightCanvas, fg_color =  "transparent")
        rightCanvas.create_window((0,0), window=rightInner, anchor="nw")

        # Placeholder iterms on the right side.
        if popluateRightData:
            popluateRightData(rightInner)

        rightInner.update_idletasks()
        rightCanvas.config(scrollregion=rightCanvas.bbox("all"))
        self.scrollbarVisibility(rightCanvas, rightScroll)



    def scrollbarVisibility(self, canvas, scrollbar):
        canvas.update_idletasks() 
        if canvas.bbox("all")[3] <= canvas.winfo_height():
            scrollbar.pack_forget()  # hide scrollbar
        else:
            scrollbar.pack(side="right", fill="y")  # show scrollbar


    def show_view(self, view_name):
        # Hide all views
        for view in self.views.values():
            view.pack_forget()

        # Show the selected view from list
        self.views[view_name].pack(expand=True, fill="both")

