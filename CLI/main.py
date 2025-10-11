# File Name: main.py

# Author: Bhagi Dhakal, Fletcher Burton
# Last Modified: September 21, 2025

#
# Run Command: python3 -m CLI.main -- Make sure to be in root of the project
# This is the main file that will intergrate all out models, 
#       CLIs together. 
#


# Imports
import os #very dangerous
import json, csv
import scheduler

from CLI.course_cli import mainCourseController
from CLI.faculty_cli import mainFacultyController
from Models.Room_model import Room
from Models.Labs_model import Lab
from CLI.room_cli import *
from CLI.lab_cli import *
from scheduler import (
    Scheduler,
    load_config_from_file,
)
from scheduler.config import CombinedConfig
from CLI.display_schedule import display_schedule

from Views.main_view import SchedulerApp
from CLI.test_cli import run_tests_cli

# output/input Path
outputPath = "output/example1.json"
inputPath = "output/mainConfig.json"


fileData = None

# this is to parse the JSON file, putting each of the section into
# their respective model 
def parseJson(path):

    # TODO: IF file is empty or difrent structur error and it will crash 
    # we need to fix that...
    with open(path, 'r') as file:
        fileData = json.load(file)

    config = fileData.get("config", {})

    # everything inside config (bottom 4 everything we need, I believe)
    Rooms = Room(config.get('rooms'))
    Labs = Lab(config.get('labs'))
    Courses = config.get('courses')
    Faculty = config.get('faculty')

    other = {
        "time_slot_config": fileData.get("time_slot_config", {}),
        "limits": fileData.get("limits", {}),
        "optimizer_flags": fileData.get("optimizer_flags", {})
    }

    # just return the others here as well. 
    return Rooms, Labs, Courses, Faculty, other


def clearTerminal():
    if os.name == 'nt':  
        _ = os.system('cls')
    else: 
        _ = os.system('clear')

# welcome the user and the options for our shell..
def welcomeMessage():
    clearTerminal()

    # should be in its own function 
    print("\n")
    print("Please select one option: ")
    print("1. View Current Config File")
    print("2. Add, Modify, Delete Faculty")
    print("3. Add, Modify, Delete Rooms")
    print("4. Add, Modify, Delete Labs")
    print("5. Add, Modify, Delete Courses")
    print("6. Run Scheduler")
    print("7. Display Saved Schedules")
    print("0. Exit")


# easier function to save daate
def saveConfig(path, rooms, labs, courses, faculty, other):
    newData = {
        "config" : {
            "rooms": rooms.rooms if hasattr(rooms, "rooms") else rooms,
            "labs": labs.labs,
            "courses": courses,
            "faculty": faculty,
        },
        "time_slot_config": other.get("time_slot_config", {}),
        "limits": other.get("limits", int),
        "optimizer_flags": other.get("optimizer_flags", {})
    }

    with open(path, 'w') as file:
        json.dump(newData, file, indent=4)

    print("Changes have been saved! \n")

def runScheduler():
    while True:
        print("\n--- Scheduler Controller ---")
        print("1. Run Scheduler")
        print("0. Back")
        choice = input("Select: ")


        if choice == "0":
            return

        elif choice == "1":
            configInput = input("Enter config file path (default: output/mainConfig.json): ")
            if not configInput:
                configInput = "output/mainConfig.json"

            while True:
                limit = input("Enter numbers of schedules to generate (default: 10): ")
                if not limit:
                    limit = 10
                    break
                if limit.isdigit():
                    limit = int(limit)
                    break
                else:
                    print("Please enter a valid integer.")

            while True:
                format = input("Enter a format file csv or json (default: json): ").lower()

                if not format:
                    format = 'json'
                    break
                if format  == "json" or format == "csv":
                    break
                else: 
                    print("Please enter a valid format (csv or json): ")
            
            
            outputFile = input("Enter the name of the output file: ").lower()

            while True: 

                optimize = input("Do you want to optimize the schedules (y/n, Default: n): ").lower()

                if not optimize :
                    optimize = 'n'
                    break
                if optimize == 'n' or optimize == 'y':
                    break
                else: 
                    print("Please enter (y or n): ")

            print("Running the schedule: \n")

            config = load_config_from_file(CombinedConfig, f"{configInput}")

            # # Create scheduler
            scheduler = Scheduler(config)

            all_schedules = []

            for schedule in scheduler.get_models():
                schedule_list = []
                for course in schedule:
                    csv_line = course.as_csv()
                    print(csv_line)

                    schedule_list.append(csv_line.split(','))
                    
                all_schedules.append(schedule_list)


            if format == "json":
                with open(f"output/{outputFile}.json", "w") as f:
                    json.dump(all_schedules, f, indent=4)
                print(f"\nSchedules saved to output/{outputFile}.json")

            elif format == "csv":
                with open(f"output/{outputFile}.csv", "w", newline="") as f:
                    writer = csv.writer(f)
                    for schedule_list in all_schedules:

                        writer.writerow([])
                        writer.writerows(schedule_list)

                print(f"\nSchedules saved to output/{outputFile}.csv")

    # return


def displayConfig(rooms, labs, courses, faculty):
    #this Function will display the config File,
    # in a human readable way. 

    print("\n=== Current Configuration ===\n")

    # Rooms
    print("Rooms:")
    if hasattr(rooms, "rooms"):
        for r in rooms.rooms:
            print(f"  - {r}")
    else:
        for r in rooms:
            print(f"  - {r}")

    # Labs
    print("\nLabs:")
    if hasattr(labs, "labs"):
        for l in labs.labs:
            print(f"  - {l}")
    else:
        for l in labs:
            print(f"  - {l}")

    # Courses
    print("\nCourses:")
    for idx, c in enumerate(courses, start=1):
        course_id = c.get("course_id", "N/A")
        credits = c.get("credits", "N/A")
        rooms_str = ", ".join(c.get("room", []) or []) or "(none)"
        labs_str = ", ".join(c.get("lab", []) or []) or "(none)"
        conflicts_str = ", ".join(c.get("conflicts", []) or []) or "(none)"
        faculty_str = ", ".join(c.get("faculty", []) or []) or "(none)"
        print(f"  {idx}. {course_id} ({credits} credits)")
        print(f"     Rooms: {rooms_str}")
        print(f"     Labs: {labs_str}")
        print(f"     Conflicts: {conflicts_str}")
        print(f"     Faculty: {faculty_str}\n")

    def _print_prefs(title, dct):
        items = list((dct or {}).items())
        items.sort(key=lambda x: (-x[1], x[0]))
        if items:
            print(f"    {title}:")
            for k, v in items:
                print(f"      - {k}: {v}")
        else:
            print(f"    {title}: (none)")

    def _print_times(times_obj):
        days = ["MON", "TUE", "WED", "THU", "FRI"]
        any_slot = False
        for d in days:
            slots = times_obj.get(d, []) if isinstance(times_obj, dict) else []
            if slots:
                any_slot = True
                print(f"      - {d}: {', '.join(slots)}")
        if not any_slot:
            print("      (none)")

    print("\nFaculty:")
    for idx, f in enumerate(faculty, start=1):
        name = f.get("name", "N/A")
        max_c = f.get("maximum_credits", "N/A")
        min_c = f.get("minimum_credits", "N/A")
        unique_limit = f.get("unique_course_limit", "N/A")
        print(f"  {idx}. {name}")
        print(f"    Credits Range: {min_c}-{max_c}")
        print(f"    Unique Course Limit: {unique_limit}")
        print(f"    Times:")
        _print_times(f.get("times", {}))
        _print_prefs("Course Preferences", f.get("course_preferences", {}))
        _print_prefs("Room Preferences", f.get("room_preferences", {}))
        _print_prefs("Lab Preferences", f.get("lab_preferences", {}))
        print()
    print("\n=============================\n")

def runCLIorGUI():

    print("=" * 50)
    print("   Welcome to the Scheduling Config System!")
    print("=" * 50)

    print("This program will parse your config files. ")
    print("With this program you can modify your config files. ")
    print("You will be able to add, modify, remove: ")
    print("faculty, courses, labs, Rooms.")
    print("Run and display the scheduler.")

    while True:
        clearTerminal()

        print("Please choose an option: \n")
        print("1: Run CLI \n")
        print("2: Run GUI \n")
        print("3: Run Tests \n")
        choice = input("Your choice: ")
        if choice == '1':
            welcomeMessage()
            rooms, labs, courses, faculty, other = parseJson(inputPath)
            
            while True:
                choice = input("Enter choice: ")

                if choice == "1":
                    # Display the current file: 
                    displayConfig(rooms, labs, courses, faculty)
                    input("Press Enter to continue...")
                elif choice == "2":
                    ##Faculty
                    mainFacultyController(faculty)
                    saveConfig(outputPath, rooms, labs, courses, faculty, other)
                    input("Press Enter to continue...")
                elif choice == "3":
                    ## Room
                    mainRoomControler(rooms)
                    saveConfig(outputPath, rooms, labs, courses, faculty, other)
                    input("Press Enter to continue...")
                elif choice == "4":
                    ## Labs 
                    mainLabControler(labs)
                    saveConfig(outputPath, rooms, labs, courses, faculty, other)
                    input("Press Enter to continue...")
                elif choice == "5":
                    # courses
                    mainCourseController(courses, rooms, labs, faculty, inputPath)
                    saveConfig(outputPath, rooms, labs, courses, faculty, other)
                    input("Press Enter to continue...")
                elif choice == "6":
                    # Run Scheduler
                    runScheduler()
                    saveConfig(outputPath, rooms, labs, courses, faculty, other)
                    input("Press Enter to continue...")
                elif choice == "7":
                    # Display saved schedules
                    display_schedule()
                    input("Press Enter to continue...")
                elif choice == "0":
                    saveConfig(outputPath, rooms, labs, courses, faculty, other)
                    print("Goodbye!")
                    break
                else:
                    print("Option not yet implemented.")
                    input("Press Enter to continue...")

        elif choice == '2':
            app = SchedulerApp()
            app.mainloop()
            quit()
        elif choice == '3':
            run_tests_cli()
        else: 
            print("Please type valid respond! ")
            input("Press Enter to continue...")



    


# main function where everything will start form. 
def main():
    runCLIorGUI()

    quit()







if __name__ == "__main__" :
    main()






