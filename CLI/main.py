# File Name: main.py
# Author: Bhagi Dhakal, Fletcher Burton
# Last Modified: September 21, 2025
#
# Run Command: python3 -m CLI.main -- Make sure to be in root of the project
# This is the main file that will intergrate all out models, 
#       CLIs together. 
#      (TODO: Expalin what needs to happen in the file. )
#   


# Imports
import os #very dangerous
import json
import scheduler

from CLI.course_cli import mainCourseController
from Models.Room_model import Room
from Models.Labs_model import Lab
from CLI.room_cli import *
from CLI.lab_cli import *
from scheduler import (
    Scheduler,
    load_config_from_file,
)
from scheduler.config import CombinedConfig

# output/input Path
outputPath = "output/example1.json"
inputPath = "output/example.json"


fileData = None

# this is to parse the JSON file, putting each of the section into
# their respective model 
def parseJson(path):

    # TODO: IF file is empty or difrent structur error and it will crash 
    # we need to fix that...
    with open(path, 'r') as file:
        fileData = json.load(file)

    config = fileData.get("config", {})

    # everythign inside config (bottom 4 eveything we need, I belive)
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


# welcome the user and the options for our shell..
def welcomeMessage():
    if os.name == 'nt':  
        _ = os.system('cls')
    else: 
        _ = os.system('clear')

    print("=" * 50)
    print("   Welcome to the Scheduling Config System!")
    print("=" * 50)

    print("This program will parse your config files. ")
    print("With this program you can modify your config files. ")
    print("You will be able to add, modify, remove: ")
    print("faculty, courses, labs, Rooms.")
    print("Run and display the scheduler.")


    # should be in its own function 
    print("\n")
    print("Please select one option: ")
    print("1. View Current Config File")
    print("2. Add, Modify, Delete Faculty")
    print("3. Add, Modify, Delete Rooms")
    print("4. Add, Modify, Delete Labs")
    print("5. Add, Modify, Delete Courses")
    print("6. Run Scheduler")
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

## This is a function to run the scheduler from our program! 
# TODO: Need to specify: config file, time slot, limit, format, outputfile, optimize? 
# TODO: display schedules in CSV
def runScheduler():

    # Load configuration
    config = load_config_from_file(CombinedConfig, "output/example.json")

    # Create scheduler
    scheduler = Scheduler(config)

    # Generate schedules
    for schedule in scheduler.get_models():
        print("Schedule:")
        for course in schedule:
            print(f"{course.as_csv()}")

    return


def displayConfig(rooms, labs, courses, faculty):
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
        rooms = ", ".join(c.get("room", [])) or "(none)"
        labs_list = ", ".join(c.get("lab", [])) or "(none)"
        conflicts = ", ".join(c.get("conflicts", [])) or "(none)"
        faculty_list = ", ".join(c.get("faculty", [])) or "(none)"

        print(f"  {idx}. {course_id} ({credits} credits)")
        print(f"     Rooms: {rooms}")
        print(f"     Labs: {labs_list}")
        print(f"     Conflicts: {conflicts}")
        print(f"     Faculty: {faculty_list}")

    # Faculty
    print("\nFaculty:")
    for f in faculty:
        name = f.get("name", "N/A")
        max_c = f.get("maximum_credits", "N/A")
        min_c = f.get("minimum_credits", "N/A")
        unique_limit = f.get("unique_course_limit", "N/A")
        print(f"  - {name} (Credits: {min_c}-{max_c}, Unique Course Limit: {unique_limit})")

    print("\n=============================\n")




# main function where everything will start form. 
def main():
    rooms, labs, courses, faculty, other = parseJson(inputPath)
    
    while True:
        welcomeMessage()
        choice = input("Enter choice: ")

        if choice == "1":
            # Display the current file:
            displayConfig(rooms, labs, courses, faculty)
            input("Press Enter to continue...")
        elif choice == "2":
            ##Faculty
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
            mainCourseController(courses, inputPath)
            saveConfig(outputPath, rooms, labs, courses, faculty, other)
            input("Press Enter to continue...")
        elif choice == "6":
            # Run Scheduler
            runScheduler()
            saveConfig(outputPath, rooms, labs, courses, faculty, other)
            input("Press Enter to continue...")
        elif choice == "0":
            saveConfig(outputPath, rooms, labs, courses, faculty, other)
            print("Goodbye!")
            break
        else:
            print("Option not yet implemented.")
            input("Press Enter to continue...")

    quit()







if __name__ == "__main__" :
    main()





# scheduler output/example.json --limit 3 --format json --output output/schedules
