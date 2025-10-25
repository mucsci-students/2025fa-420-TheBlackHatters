# File Name: Labs_model.py
# Author: Bhagi Dhakal
# Last Modified: September 16, 2025 (9:20PM)
#
# This is a model for the Labs, Pretty much same as labs.
#   With this we can add, modify, and remove Labs. 


class Lab: 
    def __init__(self, labs = None):
        # Init, the labs should be a list [], create a copy to ensure independence
        self.labs = list(labs) if labs is not None else []

    def __str__(self):
        return f"Labs in the system: {self.labs}."

    #TODO Might need to change a way to add multiple labs at the same time
    def add(self, labName):
        # This will add the lab name to our list of labs,
        # if the lab is not in the list  

        if labName not in self.labs:
            self.labs.append(labName); 

    #TODO Might need to change a way to remove multiple labs at the same time  
    def remove(self, labName): 

        # check if lab is in the list, 
        # if there then remove it, 
        # else print a message to say lab not found

        if labName in self.labs:
            self.labs.remove(labName)
        else: 
            print(f"The lab with name {labName} is not in the system!")
        
    #TODO Might need to change a way to modify multiple labs at the same time
    def modify(self, oldName, newName): 
        # Change the lab name form oldName to newName
        # if it's in the list , else raise error
        
        if oldName in self.labs:
            #Might need additional checks to be safe! 
            index = self.labs.index(oldName)
            self.labs[index] = newName
        else: 
            print(f"The lab with name {oldName} is not in the system! Cannot change {oldName} to {newName}.")
        
    
    def toJson(self):
        ## Not exactly to json, just ready do put into json
        return list(self.labs)


