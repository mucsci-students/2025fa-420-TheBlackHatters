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
First, install the [Course Constraint Scheduler](https://github.com/mucsci/Scheduler)<br>
or use ```pip install course-constraint-scheduler```

Then clone the repository with ```git clone <repository url>```

1) create virtual environment
2) install everything from requirements.txt 
python -m venv venv
venv\Scripts\activate.bat
3) run our program 

To run the companion, open a terminal in the repository, cd into the root with ```cd root``` and run the main.py file with ```python main.py```

## Operation Instructions

### Adding, Editing, and Removing Faculty
**Adding a faculty member**
```add faculty [faculty name] [full-time / adjunct] [unique course limit] [available time range] [available days] [preferences] [courses] [weight]```

Example:<br>
`add faculty Prof._Hobbs adjunct 3 9-5 M-W none CMSC_420 3`<br>
**Editing a faculty member**
```edit faculty``` will prompt you for the faculty member's name and what criteria to change, then change it.

**Deleting a faculty member**
```delete faculty``` will prompt you for the faculty member's name, then delete it.
<hr>

### Adding, Editing, and Removing Courses
**Adding a course**<br>
```add course [course id] [credits] [room] [lab] [conflicts] [faculty]```<br>
If any of the required criteria are not present, it will not create the course and ask you to try again with the correct information.

Example: `add course CMSC_420 4 Roddy_140 Mac_Lab none Prof._Hobbs`<br>
**Editing a course**
`edit course` will prompt you for the course name and what criteria to change, then change it.

**Deleting a course**
`delete course` will prompt you for the course name, then delete it.
<hr>

### Adding, Editing, and Removing Rooms/Labs
**Adding a lab**<br>
using `add lab` will prompt you for a name. Preferred format is as follows:<br>
Eg. Mac Lab, Linux Lab, Windows Lab

Example: `add lab Linux_Lab`<br>
**Editing a lab**<br>
typing ```edit lab``` will prompt you for a name of an existing lab. Then enter the new name for the lab.

**Deleting a lab**<br>
typing ```delete lab``` will prompt you for the name of the lab, and then delete it if the lab exists.

The same is true for `add room`, `edit room`, and `delete room`

### Displaying Saved Schedules
To view previously generated schedules saved as CSV files, choose option 7 from the main menu.

You will see a numbered list of all available schedule CSV files in the output/ folder. 

Example:

Which Schedule?
1. test_schedule.csv

Enter either the number or the file name to display the contents in a readable format:

--- Schedule Contents ---
Course   | Day      | Time        | Room      | Lab   | Faculty
CMSC140  | Monday   | 09:00-10:30 | Roddy 136 |       | Prof.Zoppetti
CMSC152  | Tuesday  | 10:00-11:30 | Roddy 147 | Mac   | Prof.Hogg
CMSC161  | Monday   | 11:00-12:30 | Roddy 136 | Linux | Prof.Rogers
...
-------------------------

Notes:

Both numeric input and exact file names are accepted.

If no schedules exist, the program displays: No saved schedules found.

