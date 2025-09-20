# TheBlackHatters
Team Members:
- Liam Delaney
- Nicholas DiPace
- Bhagi Dhakal
- Fletcher Burton
- Nick Filemyr
- Basu Subedi
- Ben Richardson

# Course Constraint Scheduler Companion
This is a tool built for the Course Constraint Scheduler that allows you to create configuration files and run the scheduler completely in the command line.

## Installation Instructions
Must be running at least Python version 3.12

**Installation**
1. Clone the repository with `git clone <url>` to download the project. This will be your working directory.
2. Link the folder in Visual Studio Code and open terminal or just open a terminal in the directory. (Powershell if using Windows)<br>
PS. Powershell script execution will not work unless you either set the execution policy to bypass with `Set-ExecutionPolicy Bypass` or within your working terminal (must be run in admin) run `Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process` to temporarily allow scripts. The latter is recommended for security reasons.
3. Run `python3 -m venv venv` to create a virtual environment.
4. Run `venv/Scripts/Activate.ps1` to enter the virtual environment. (you can use `deactivate` to exit the virtual environment).<br> **For Mac users**, run `source venv/bin/activate`
5. Use `pip install course-constraint-scheduler` to install the [Scheduler project](https://github.com/mucsci/Scheduler).
6. Finally, run `python -m CLI.main` to start the Scheduler Companion.

## Operation Instructions

### Viewing Current Config<br>
Typing 1 will show you the current state of the configuration file that is given to the scheduler.

### Adding, Editing, and Removing Faculty
**Adding a faculty member**<br>
Typing 2 will bring you to the faculty portion.

1. View <br>
   See which labs are in the current working configuration file.
2. Add <br>
   Add a lab to the configuration file. Eg. 'Mac Lab'
3. Delete <br>
    Delete a lab from the configuration. Enter the name you wish to delete.
4. Modify <br>
   Change the name of a lab.

```add faculty [faculty name] [full-time / adjunct] [unique course limit] [available time range] [available days] [preferences] [courses] [weight]```

<hr>

### Adding, Editing, and Removing Rooms/Labs<br>
Typing 3 will bring you into the lab portion, and 4 for rooms.

1. View Labs<br>
   See which labs are in the current working configuration file.
2. Add lab<br>
   Add a lab to the configuration file. Eg. 'Mac Lab'
3. Delete lab<br>
    Delete a lab from the configuration. Enter the name you wish to delete.
4. Modify lab<br>
   Change the name of a lab.

The same is true for all room commands.


<hr>

### Adding, Editing, and Removing Courses
**Adding a course**<br>
Typing 5 will bring you into the Course portion. <br>
1. Add course<br>
   Starts with inputting a course ID, then name, credits, room. These are required criteria, use the other functions to add conflicts.
2. Modify course<br>
   Here you can modify a course by its course ID. You can change name, credits, and room data.
3. Delete course<br>
   Delete a course by its course ID.
4. Add conflict<br>
   Add conflicts by ID.
5. Modify conflict<br>
   Change conflicts by ID.
6. Delete conflict<br>
   Delete conflicts by ID.
7. Show all courses<br>
   Shows all courses currently in configuration file.
8. Show all conflicts<br>
   Shows all conflicts currently in configuration file.

<hr>

### Run The Scheduler
Typing 6 will run the Scheduler with the current configuration file.
   
