# File Name: room_cli.py
# Author: Bhagi Dhakal
# Last Modified: September 15, 2025 (10:00 PM)
#
# This is a CLI for the Rooms.
#   With this we can add, modify, and remove rooms,
#   make this changes directly to the json file. 


# Imports.. 


# Need to get a way to pull the file and get the rooms already there? 
# Is this nessaarray? 

# This will prompt the user to enter the name they want to add
def addRoomCli(RoomModel):
    print("Please enter the Name of the room you want to add: ")
    name = input()

    RoomModel.add(name)

# This will prompt the user to enther the name they want to remove
def removeRoomCli(RoomModel):
    print("Please enter the Name of the room you want to remove: ")
    name = input()

    RoomModel.remove(name)


# This will prompt the user to enter the room name they want to change
# and the name they want to change to 
def modifyRoomCli(RoomModel):
    oldName = input("Please enter the name of the room you want to modify: ")
    newName = input("Please enter the new room name: ")

    RoomModel.modify(oldName, newName)




