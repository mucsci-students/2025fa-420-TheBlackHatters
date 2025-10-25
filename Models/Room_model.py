# File Name: Rooms_model.py
# Author: Bhagi Dhakal
# Last Modified: September 11, 2025 (10:20AM)
#
# This is a model for the Rooms.
#   With this we can add, modify, and remove rooms. 


class Room: 
    def __init__(self, rooms = None):
        # Init, the rooms should be a list [], 
        # Make an internal copy so external mutations don't affect us
        self.rooms = list(rooms) if rooms is not None else []

    def __str__(self):
        return f"Rooms in the system: {self.rooms}."

    #TODO Might need to change a way to add multiple rooms at the same time
    def add(self, roomName):
        # This will add the room name to our list of rooms,
        # if the room is not in the list  

        if roomName not in self.rooms:
            self.rooms.append(roomName); 

    #TODO Might need to change a way to remove multiple rooms at the same time  
    def remove(self, roomName): 

        # check if room is in the list, 
        # if there then remove it, 
        # else print a message to say room not found

        if roomName in self.rooms:
            self.rooms.remove(roomName)
        else: 
            print(f"The room with name {roomName} is not in the system!")
        
    #TODO Might need to change a way to modify multiple rooms at the same time
    def modify(self, oldName, newName): 
        # Change the room name form oldName to newName
        # if it's in the list , else raise error
        
        if oldName in self.rooms:
            #Might need additional checks to be safe! 
            index = self.rooms.index(oldName)
            self.rooms[index] = newName
        else: 
            print(f"The room with name {oldName} is not in the system! Cannot change {oldName} to {newName}.")
        
    
    def toJson(self):
        ## Not exactly to json, just ready do put into json
        # Return a shallow copy to avoid exposing internal list by reference
        return list(self.rooms)


