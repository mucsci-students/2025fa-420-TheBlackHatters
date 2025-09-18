# File Name: lab_cli.py
# Author: Bhagi Dhakal
# Last Modified: September 16, 2025 (10:10 PM)
#
# This is a CLI for the labs.
#   With this we can add, modify, and remove labs,
#   make this changes directly to the json file. 


# This will prompt the user to enter the name they want to add
def addLabCli(LabModel):
    print("Please enter the Name of the lab you want to add: ")
    name = input()

    LabModel.add(name)

# This will prompt the user to enther the name they want to remove
def removeLabCli(LabModel):
    print("Please enter the Name of the lab you want to remove: ")
    name = input()

    LabModel.remove(name)


# This will prompt the user to enter the lab name they want to change
# and the name they want to change to 
def modifyLabCli(LabModel):
    oldName = input("Please enter the name of the lab you want to modify: ")
    newName = input("Please enter the new lab name: ")

    LabModel.modify(oldName, newName)




