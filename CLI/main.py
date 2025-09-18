# File Name: main.py
# Author: Bhagi Dhakal
# Last Modified: September 15, 2025 (10:00 PM) By Bhagi Dhakal
#
# Run Command: python3 -m CLI.main -- Make sure to be in root of the project
# This is the main file that will intergrate all out models, 
#       CLIs together. 
#      (TODO: Expalin what needs to happen in the file. )
#   


# Imports
import os #very dangerous
import json
from Models.Room_model import Room
from CLI.room_cli import *
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
    Labs = config.get('labs')
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
    print("   |Welcome to the Scheduling Config System!|")
    print("=" * 50)

    print("This program will parse your config files. ")
    print("With this program you can modify your config files. ")
    print("You will be able to add, modify, remove: ")
    print("faculty, courses, labs, Rooms.")
    print("Run and display the scheduler.")


    # should be in its own function 
    print("\n")
    print("Please select one option: ")
    print("1. View Current Congfi File")
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
            "labs": labs,
            "courses": courses,
            "faculty": faculty,
        },
        "time_slot_config": other.get("time_slot_config", {}),
        "limits": other.get("limits", {}),
        "optimizer_flags": other.get("optimizer_flags", {})
    }

    with open(path, 'w') as file:
        json.dump(newData, file, indent=4)

    print("Changes have been saved! \n")

# main function where everything will start form. 
def main():
    rooms, labs, courses, faculty, other = parseJson(inputPath)
    
    while True:
        welcomeMessage()
        choice = input("Enter choice: ")

        if choice == "1":
            input("Press Enter to continue...")
        elif choice == "2":

            saveConfig(outputPath, rooms, labs, courses, faculty, other)
            input("Press Enter to continue...")
        elif choice == "3":
            mainRoomControler(rooms)
            saveConfig(outputPath, rooms, labs, courses, faculty, other)
            input("Press Enter to continue...")
        elif choice == "4":

            saveConfig(outputPath, rooms, labs, courses, faculty, other)
            input("Press Enter to continue...")
        elif choice == "5":

            saveConfig(outputPath, rooms, labs, courses, faculty, other)
            input("Press Enter to continue...")
        elif choice == "6":

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