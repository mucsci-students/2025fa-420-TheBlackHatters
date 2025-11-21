# File Name: main.py

# Author: Bhagi Dhakal, Fletcher Burton, Liam Delaney
# Last Modified: October 20, 2025
#
# Run Command: python3 -m CLI.main -- Make sure to be in root of the project
# This is the main file that will intergrate all out models,
#       CLIs together.
#

# Imports
import sys
import os
from contextlib import contextmanager
import json
import csv
import click
from CLI.course_cli import mainCourseController
from CLI.faculty_cli import mainFacultyController
from Models.Room_model import Room
from Models.Labs_model import Lab

# from CLI.room_cli import *
from CLI.room_cli import mainRoomControler
from CLI.lab_cli import mainLabControler
from scheduler import (
    Scheduler,
    load_config_from_file
)
from scheduler.config import CombinedConfig
from CLI.display_schedule import display_schedule

from Views.main_view import SchedulerApp
from CLI.test_cli import run_tests_cli

# output/input Path
filePath = "output/mainConfig.json"


fileData = None


# this is to parse the JSON file, putting each of the section into
# their respective model
def parseJson(path):
    with open(path, "r") as file:
        fileData = json.load(file)

    config = fileData.get("config", {})

    # everything inside config (bottom 4 everything we need, I believe)
    Rooms = Room(config.get("rooms"))
    Labs = Lab(config.get("labs"))
    Courses = config.get("courses")
    Faculty = config.get("faculty")

    other = {
        "time_slot_config": fileData.get("time_slot_config", {}),
        "limit": fileData.get("limit", {}),
        "optimizer_flags": fileData.get("optimizer_flags", {}),
    }

    # just return the others here as well.
    return Rooms, Labs, Courses, Faculty, other


def clearTerminal():
    if os.name == "nt":
        _ = os.system("cls")
    else:
        _ = os.system("clear")


# welcome the user and provide the options for our shell.
def welcomeMessage():
    clearTerminal()
    print("=" * 50)
    print("   Welcome to the Scheduling Config System!")
    print("=" * 50)

    print("This program will parse your config files. ")
    print("With this program you can modify your config files. ")
    print("You will be able to add, modify, remove: ")
    print("faculty, courses, labs, Rooms.")
    print("Run and display the scheduler.")

    print("\n")
    print("Please select one option:\n")
    print("1. Configuration\n")
    print("2. Run Scheduler\n")
    print("3. Display Saved Schedules\n")
    print("0. Exit\n")


# Saves the data to the config file.
def saveConfig(path, rooms, labs, courses, faculty, other):
    newData = {
        "config": {
            "rooms": rooms.rooms if hasattr(rooms, "rooms") else rooms,
            "labs": labs.labs,
            "courses": courses,
            "faculty": faculty,
        },
        "time_slot_config": other.get("time_slot_config", {}),
        "limit": other.get("limit", int),
        "optimizer_flags": other.get("optimizer_flags", {}),
    }

    with open(path, "w") as file:
        json.dump(newData, file, indent=4)

    print("Changes have been saved! \n")


def runScheduler(otherData):
    while True:
        print("\n--- Scheduler Controller ---")
        print("1. Run Scheduler")
        print("0. Back")
        choice = input("Select: ")

        if choice == "0":
            return

        elif choice == "1":
            configInput = input(
                "Enter config file path (default: output/mainConfig.json): "
            )
            if not configInput:
                configInput = "output/mainConfig.json"

            while True:
                limit = input("Enter numbers of schedules to generate (default: 10): ")
                if not limit:
                    limit = 10
                    break
                if limit.isdigit():
                    limit = int(limit)
                    break
                else:
                    print("Please enter a valid integer.")

            while True:
                format = input(
                    "Enter a format file csv or json (default: json): "
                ).lower()

                if not format:
                    format = "json"
                    break
                if format == "json" or format == "csv":
                    break
                else:
                    print("Please enter a valid format (csv or json): ")

            outputFile = input("Enter the name of the output file: ").lower()

            optimizeList = [
                "faculty_course",
                "faculty_room",
                "faculty_lab",
                "same_room",
                "same_lab",
                "pack_rooms",
            ]
            selectedOptimizeList = []

            for opt in optimizeList:
                while True:
                    choice = (
                        input(
                            f"Do you want to apply '{opt}' optimization? (y/n, Default: n): "
                        )
                        .strip()
                        .lower()
                    )

                    if not choice:
                        choice = "n"
                    if choice in ("y", "n"):
                        break
                    print("Please enter 'y' or 'n'.")

                if choice == "y":
                    selectedOptimizeList.append(opt)

            print("\nSelected optimizations:")
            print(selectedOptimizeList if selectedOptimizeList else "None selected.")

            # update config file with new opt, and limit
            if os.path.exists(configInput):
                with open(configInput, "r") as f:
                    data = json.load(f)

                # Update values
                data["limit"] = limit
                data["optimizer_flags"] = selectedOptimizeList

                # Write back to the same file
                with open(configInput, "w") as f:
                    json.dump(data, f, indent=4)
            else:
                print(f"Cannot open config File: {configInput}.\n")
                return

            print("Running the schedule: \n")
            config = load_config_from_file(CombinedConfig, f"{configInput}")


            # Create scheduler
            scheduler = Scheduler(config)

            all_schedules = []
            count = 0

            for schedule in scheduler.get_models():
                schedule_list = [course.as_csv().split(",") for course in schedule]
                all_schedules.append(schedule_list)

                # Convert schedule to list of CSV rows
                schedule_list = [course.as_csv().split(",") for course in schedule]
                all_schedules.append(schedule_list)

                # Print live progress after each schedule
                bar_length = 50
                progress = int((count / limit) * bar_length)
                bar = "█" * progress + "-" * (bar_length - progress)
                print(f"Progress: |{bar}| {count}/{limit}")

            print("\nAll schedules generated!\n")

            if format == "json":
                with open(f"output/{outputFile}.json", "w") as f:
                    json.dump(all_schedules, f, indent=4)
                print(f"\nSchedules saved to output/{outputFile}.json")

            elif format == "csv":
                with open(f"output/{outputFile}.csv", "w", newline="") as f:
                    writer = csv.writer(f)
                    for schedule_list in all_schedules:
                        writer.writerow([])
                        writer.writerows(schedule_list)

                print(f"\nSchedules saved to output/{outputFile}.csv")

    # return


def whatAction(rooms, labs, courses, faculty, other):
    while True:
        print("Please choose an option: \n")
        print("1. Add, Modify, Delete Faculty\n")
        print("2. Add, Modify, Delete Rooms\n")
        print("3. Add, Modify, Delete Labs\n")
        print("4. Add, Modify, Delete Courses\n")
        print("5. Chatbot Mode (natural language)\n")
        print("0. Go Back\n")
        choice = input("Enter choice: ")
        if choice == "1":
            ##Faculty
            mainFacultyController(faculty)
            saveConfig(filePath, rooms, labs, courses, faculty, other)
        elif choice == "2":
            ## Room
            mainRoomControler(rooms)
            saveConfig(filePath, rooms, labs, courses, faculty, other)
        elif choice == "3":
            ## Labs
            mainLabControler(labs)
            saveConfig(filePath, rooms, labs, courses, faculty, other)
        elif choice == "4":
            # courses
            mainCourseController(courses, rooms, labs, faculty)
            saveConfig(filePath, rooms, labs, courses, faculty, other)
        elif choice == "5":
            from CLI.chatbot_cli import main as chatbot_main

            saveConfig(filePath, rooms, labs, courses, faculty, other)
            chatbot_main(filePath)

            # reload changes made by chatbot
            rooms, labs, courses, faculty, other = parseJson(filePath)
            print("\nChatbot session ended. Configuration reloaded from disk.\n")
        elif choice == "0":
            # Go back to selections.
            break


def configMessage():
    print("\n")
    print("Please select one option: \n")
    print("1. Import Config\n")
    print("2. Create New Config\n")
    print("3. Edit config\n")
    print("4. View Current Config File\n")
    print("0. Back\n")


def configurationPrompt(filePath, rooms, labs, courses, faculty, other):
    while True:
        configMessage()
        choice = input("Enter choice: ")
        if choice == "1":
            # Ask for an alternative Config file path
            print("Enter the file path: ")
            while True:
                userPath = input()
                # Checks if the provided path is valid
                if os.path.exists(userPath):
                    # If so, makes it the input path
                    # filePath = userPath ?  output/example.json
                    print("Config Loaded Successfully")
                    return
                else:
                    # If not, tells the user and asks for another path.
                    print("Invalid path!")
                    print("\n")
                    print("Enter a valid file path: (i.e output/example.json)")
        elif choice == "2":
            # Gives a blank config
            name = input("Enter the file name: (i.e newconfig)")
            createEmptyJson(name)
        elif choice == "3":
            ##Faculty
            whatAction(rooms, labs, courses, faculty, other)
        elif choice == "4":
            # Display the current file:
            displayConfig(rooms, labs, courses, faculty)
        elif choice == "0":
            # return to main selection:
            break


def createEmptyJson(name):
    with open("output/blank_template.json", "r") as template:
        data = json.load(template)
    file_name = "output/" + name + ".json"
    print(file_name)
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)
    return file_name


def displayConfig(rooms, labs, courses, faculty):
    # this Function will display the config File,
    # in a human readable way.

    print("\n=== Current Configuration ===\n")

    # Rooms
    print("Rooms:")
    if hasattr(rooms, "rooms"):
        for room in rooms.rooms:
            print(f"  - {room}")
    else:
        for room in rooms:
            print(f"  - {room}")

    # Labs
    print("\nLabs:")
    if hasattr(labs, "labs"):
        for lab in labs.labs:
            print(f"  - {lab}")
    else:
        for lab in labs:
            print(f"  - {lab}")

    # Courses
    print("\nCourses:")
    for idx, c in enumerate(courses, start=1):
        course_id = c.get("course_id", "N/A")
        credits = c.get("credits", "N/A")
        rooms_str = ", ".join(c.get("room", []) or []) or "(none)"
        labs_str = ", ".join(c.get("lab", []) or []) or "(none)"
        conflicts_str = ", ".join(c.get("conflicts", []) or []) or "(none)"
        faculty_str = ", ".join(c.get("faculty", []) or []) or "(none)"
        print(f"  {idx}. {course_id} ({credits} credits)")
        print(f"     Rooms: {rooms_str}")
        print(f"     Labs: {labs_str}")
        print(f"     Conflicts: {conflicts_str}")
        print(f"     Faculty: {faculty_str}\n")

    def _print_prefs(title, dct):
        items = list((dct or {}).items())
        items.sort(key=lambda x: (-x[1], x[0]))
        if items:
            print(f"    {title}:")
            for k, v in items:
                print(f"      - {k}: {v}")
        else:
            print(f"    {title}: (none)")

    def _print_times(times_obj):
        days = ["MON", "TUE", "WED", "THU", "FRI"]
        any_slot = False
        for d in days:
            slots = times_obj.get(d, []) if isinstance(times_obj, dict) else []
            if slots:
                any_slot = True
                print(f"      - {d}: {', '.join(slots)}")
        if not any_slot:
            print("      (none)")

    print("\nFaculty:")
    for idx, f in enumerate(faculty, start=1):
        name = f.get("name", "N/A")
        max_c = f.get("maximum_credits", "N/A")
        min_c = f.get("minimum_credits", "N/A")
        unique_limit = f.get("unique_course_limit", "N/A")
        print(f"  {idx}. {name}")
        print(f"    Credits Range: {min_c}-{max_c}")
        print(f"    Unique Course Limit: {unique_limit}")
        print("    Times:")
        _print_times(f.get("times", {}))
        _print_prefs("Course Preferences", f.get("course_preferences", {}))
        _print_prefs("Room Preferences", f.get("room_preferences", {}))
        _print_prefs("Lab Preferences", f.get("lab_preferences", {}))
        print()
    print("\n=============================\n")


def runCLI():
    while True:
        rooms, labs, courses, faculty, other = parseJson(filePath)
        welcomeMessage()
        choice = input("Enter choice: ")
        if choice == "1":
            ##Faculty
            configurationPrompt(filePath, rooms, labs, courses, faculty, other)
            input("Press Enter to continue...")
        elif choice == "2":
            # Run Scheduler
            runScheduler(other)
            saveConfig(filePath, rooms, labs, courses, faculty, other)
            input("Press Enter to continue...")
        elif choice == "3":
            # Display saved schedules
            display_schedule()
            input("Press Enter to continue...")
        elif choice == "0":
            saveConfig(filePath, rooms, labs, courses, faculty, other)
            print("Goodbye!")
            break
        else:
            print("Option not yet implemented.")
            input("Press Enter to continue...")


# we won't be printing anything in the terminal when running GUI
# Need to set this up for final product..
# Terminal output is still helpfull in developement.
@contextmanager
def suppressOutput():
    with open(os.devnull, "w") as devnull:
        old_stdout, old_stderr = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = (
            devnull,
            devnull,
        )  # Change output to null files not Terminal output
        try:
            yield
        finally:
            sys.stdout, sys.stderr = old_stdout, old_stderr  # reset


# main function where everything will start form.
@click.command()
@click.option("--cli", is_flag=True, help="Run in command-line mode")
@click.option("--tests", is_flag=True, help="Run tests instead")
def main(cli, tests):
    if cli:
        runCLI()
    elif tests:
        run_tests_cli()
    else:
        # Suppress any prints/outputs while GUI runs
        # Use this after developement, final Commit for sprint.
        # with suppressOutput():
        #     app = SchedulerApp()
        #     app.mainloop()
        app = SchedulerApp()
        app.mainloop()
        
    quit()


if __name__ == "__main__":
    main()
