# File Name: room_cli.py
# Author: Bhagi Dhakal
# Last Modified: September 15, 2025 (10:00 PM)
#
# This is a CLI for the Rooms.
#   With this we can add, modify, and remove rooms,
#   make this changes directly to the json file.


def viewRooms(RoomModel):
    return print(f"Current Rooms In System: {RoomModel.toJson()}.")


# This will prompt the user to enter the name they want to add
def addRoomCli(RoomModel):
    name = input("Enter Room name to Add:  ")
    RoomModel.add(name)
    viewRooms(RoomModel)


# This will prompt the user to enther the name they want to remove
def removeRoomCli(RoomModel):
    name = input("Enter Room name to remove: ")
    RoomModel.remove(name)
    viewRooms(RoomModel)


# This will prompt the user to enter the room name they want to change
# and the name they want to change to
def modifyRoomCli(RoomModel):
    oldName = input("Enter Room name to modify: ")
    newName = input("Enter new Room name: ")

    RoomModel.modify(oldName, newName)
    viewRooms(RoomModel)


# ROOM CONTROLER!
def mainRoomControler(RoomModel):
    while True:
        print("\n--- Room Controler ---")
        print("1. View Rooms")
        print("2. Add Room")
        print("3. Delete Room")
        print("4. Modify Room")
        print("0. Back")
        choice = input("Select: ")

        if choice == "1":
            viewRooms(RoomModel)
        elif choice == "2":
            addRoomCli(RoomModel)
        elif choice == "3":
            removeRoomCli(RoomModel)
        elif choice == "4":
            modifyRoomCli(RoomModel)
        elif choice == "0":
            return
        else:
            print("Invalid option. ")
