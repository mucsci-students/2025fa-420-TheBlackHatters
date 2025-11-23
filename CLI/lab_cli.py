# File Name: lab_cli.py
# Author: Bhagi Dhakal
# Last Modified: September 20, 2025 (10:10 PM)
#
# This is a CLI for the labs.
#   With this we can add, modify, and remove labs,
#   make this changes directly to the json file.


def viewLabs(LabModel):
    return print(f"Current Labs In System: {LabModel.toJson()}.")


# This will prompt the user to enter the name they want to add
def addLabCli(LabModel):
    print("Lab name to Add: ")
    name = input()

    LabModel.add(name)
    viewLabs(LabModel)


# This will prompt the user to enther the name they want to remove
def removeLabCli(LabModel):
    print("Enter Lab name to remove: ")
    name = input()

    LabModel.remove(name)
    viewLabs(LabModel)


# This will prompt the user to enter the lab name they want to change
# and the name they want to change to
def modifyLabCli(LabModel):
    oldName = input("Lab name to modify: ")
    newName = input("Enter new Lab name: ")

    LabModel.modify(oldName, newName)
    viewLabs(LabModel)


# Main Labs Cli Controller
def mainLabControler(LabModel):
    while True:
        print("\n--- Lab Controler ---")
        print("1. View Labs")
        print("2. Add Lab")
        print("3. Delete Lab")
        print("4. Modify Lab")
        print("0. Back")
        choice = input("Select: ")

        if choice == "1":
            viewLabs(LabModel)
        elif choice == "2":
            addLabCli(LabModel)
        elif choice == "3":
            removeLabCli(LabModel)
        elif choice == "4":
            modifyLabCli(LabModel)
        elif choice == "0":
            return
        else:
            print("Invalid option. ")
