# File Name: course_cli.py
# Author: Ben Richardson
# Last Modified: September 18, 2025
#
# CLI for managing courses and conflicts.
#

import sys

# ---------------- Data Storage ----------------
courses = {}
conflicts = {}

# ---------------- Course Functions ----------------
def add_course():
    course_id = input("Enter course ID: ").strip()
    if course_id in courses:
        print("Course already exists.")
        return
    name = input("Enter course name: ").strip()
    credits = input("Enter course credits: ").strip()
    room = input("Enter course room: ").strip()
    courses[course_id] = {"name": name, "credits": credits, "room": room}
    print(f"Course {course_id} added successfully!")

def modify_course():
    course_id = input("Enter course ID to modify: ").strip()
    if course_id not in courses:
        print("Course not found.")
        return
    print(f"Current data: {courses[course_id]}")
    name = input("Enter new course name (leave blank to keep current): ").strip()
    credits = input("Enter new course credits (leave blank to keep current): ").strip()
    room = input("Enter new course room (leave blank to keep current): ").strip()

    if name:
        courses[course_id]["name"] = name
    if credits:
        courses[course_id]["credits"] = credits
    if room:
        courses[course_id]["room"] = room

    print(f"Course {course_id} updated successfully!")

def delete_course():
    course_id = input("Enter course ID to delete: ").strip()
    if course_id in courses:
        del courses[course_id]
        print(f"Course {course_id} deleted successfully!")
    else:
        print("Course not found.")

# ---------------- Conflict Functions ----------------
def add_conflict():
    conflict_id = input("Enter conflict ID: ").strip()
    if conflict_id in conflicts:
        print("Conflict already exists.")
        return
    description = input("Enter conflict description: ").strip()
    conflicts[conflict_id] = {"description": description}
    print(f"Conflict {conflict_id} added successfully!")

def modify_conflict():
    conflict_id = input("Enter conflict ID to modify: ").strip()
    if conflict_id not in conflicts:
        print("Conflict not found.")
        return
    print(f"Current data: {conflicts[conflict_id]}")
    description = input("Enter new conflict description (leave blank to keep current): ").strip()
    if description:
        conflicts[conflict_id]["description"] = description
    print(f"Conflict {conflict_id} updated successfully!")

def delete_conflict():
    conflict_id = input("Enter conflict ID to delete: ").strip()
    if conflict_id in conflicts:
        del conflicts[conflict_id]
        print(f"Conflict {conflict_id} deleted successfully!")
    else:
        print("Conflict not found.")

# ---------------- CLI Menu ----------------
def cli_menu():
    while True:
        print("\n--- Course & Conflict Management CLI ---")
        print("1. Add Course")
        print("2. Modify Course")
        print("3. Delete Course")
        print("4. Add Conflict")
        print("5. Modify Conflict")
        print("6. Delete Conflict")
        print("7. Show All Courses")
        print("8. Show All Conflicts")
        print("9. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            add_course()
        elif choice == "2":
            modify_course()
        elif choice == "3":
            delete_course()
        elif choice == "4":
            add_conflict()
        elif choice == "5":
            modify_conflict()
        elif choice == "6":
            delete_conflict()
        elif choice == "7":
            print("Courses:", courses if courses else "No courses found.")
        elif choice == "8":
            print("Conflicts:", conflicts if conflicts else "No conflicts found.")
        elif choice == "9":
            print("Exiting program...")
            sys.exit()
        else:
            print("Invalid choice, try again.")
