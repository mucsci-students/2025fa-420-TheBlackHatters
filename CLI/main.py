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

    # everythign inside config
    Rooms = Room(config.get('rooms'))


    # just return the others here as well. 
    return Rooms

# updates the json file with the changes made by user. 
def updateJson(path, data):
    pass 


# main function where everything will start form. 
def main():
    rooms = parseJson(outputPath)
    

    # call CLI functions.. 




if __name__ == "__main__" :
    main()