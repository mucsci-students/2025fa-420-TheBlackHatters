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

# output/input Path
outputPath = "output/example.json"


fileData = None

# this is to parse the JSON file, putting each of the section into
# their respective model 
def parseJson(path):
    with open(path, 'r') as file:
        fileData = json.load(file)

    config = fileData.get("config", {})

    # everythign inside config (bottom 4 eveything we need, I belive)
    Rooms = Room(config.get('rooms'))
    Labs = config.get('labs')
    Courses = config.get('courses')
    Faculty = config.get('faculty')

    timeSlots = fileData.get("time_slot_config", {})
    limit = fileData.get("limits", {})
    optimizerFlags = fileData.get("optimizer_flags", {})



    # just return the others here as well. 
    return Rooms, Labs, Courses, Faculty

# updates the json file with the changes made by user. 
def updateJson(path, data):

    with open(path, 'w') as file:
        json.dump(data, file)

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
    print("You will be able to add, modify, remove:  faculty, courses, labs, Rooms." \
    " Run and display the scheduler.")


    # should be in its own function 
    print("\n")
    print("Please select one option: ")
    print("1. View Current Congi File")
    print("2. Add, Modify, Delete Faculty")
    print("3. Add, Modify, Delete Rooms")
    print("4. Add, Modify, Delete Labs")
    print("5. Add, Modify, Delete Courses")
    print("6. Save Changes") # maybe better for user if this happned automaticly 
    print("7. Run Program")
    print("0. Exit")


# evethifor 
def CLIRooms():
    pass
    # pass 






# main function where everything will start form. 
def main():
    rooms, labs, courses, faculty = parseJson(outputPath)
    
    welcomeMessage()

    # call CLI functions.. 






if __name__ == "__main__" :
    main()