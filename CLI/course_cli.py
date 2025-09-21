# File Name: course_cli.py
# Author: Ben Richardson, Fletcher Burton
# Last Modified: September 21, 2025
#
# CLI for managing courses and conflicts.
#

import sys
from Models.courses.Course_model import Course

courses = {}
conflicts = {}
_courses_ref = None

def _print_courses_list():
    _refresh_local_view_from_ref()
    if courses:
        print("Courses:")
        for name, data in courses.items():
            print(f"  {name}: credits={data['credits']}, room={data['room']}")
    else:
        print("No courses found.")

def _print_conflicts_list():
    if conflicts:
        print("Conflicts:")
        for cid, data in conflicts.items():
            print(f"  {cid}: description={data['description']}")
    else:
        print("No conflicts found.")

def _find_course_index(course_name: str) -> int:
    name = (course_name or "").strip()
    for i, c in enumerate(_courses_ref or []):
        if str(c.get("course_id", "")).strip() == name:
            return i
    return -1

def _first_or_empty(v):
    return v[0] if isinstance(v, list) and v else ""

def _refresh_local_view_from_ref():
    courses.clear()
    if not _courses_ref:
        return
    for c in _courses_ref:
        name = str(c.get("course_id", "")).strip()
        if not name:
            continue
        courses[name] = {
            "credits": str(c.get("credits", "")),
            "room": _first_or_empty(c.get("room", [])),
        }

def add_course():
    name = input("Enter course name: ").strip()
    if _find_course_index(name) != -1:
        print("Course already exists.")
        return

    credits = input("Enter course credits: ").strip()
    room = input("Enter course room: ").strip()

    try:
        new_course = Course.build_and_validate(
            {
                "course_id": name,
                "credits": int(credits),
                "room": [room] if room else [],
                "lab": [],
                "conflicts": [],
                "faculty": [],
            },
            existing_courses=_courses_ref,
            strict_membership=False,
        )
        _courses_ref.append(new_course.to_dict())
        courses[name] = {"credits": credits, "room": room}
        print(f"Course {name} added successfully!")
    except Exception as e:
        print(f"Error: {e}")

def modify_course():
    _print_courses_list()
    name = input("Enter course name to modify: ").strip()
    idx = _find_course_index(name)
    if idx == -1:
        print("Course not found.")
        return

    print(f"Current data: {courses.get(name, {'credits':'', 'room':''})}")
    credits = input("Enter new course credits (leave blank to keep current): ").strip()
    room = input("Enter new course room (leave blank to keep current): ").strip()

    try:
        cur = Course.from_dict(_courses_ref[idx])
        if credits:
            cur.set_credits(int(credits))
        if room:
            cur.set_rooms([room])
        cur.validate(existing_courses=_courses_ref, ignore_index=idx, strict_membership=False)
        _courses_ref[idx] = cur.to_dict()
        if name not in courses:
            courses[name] = {"credits": "", "room": ""}
        if credits:
            courses[name]["credits"] = credits
        if room:
            courses[name]["room"] = room
        print(f"Course {name} updated successfully!")
    except Exception as e:
        print(f"Error: {e}")

def delete_course():
    _print_courses_list()
    name = input("Enter course name to delete: ").strip()
    idx = _find_course_index(name)
    if idx == -1:
        print("Course not found.")
        return

    try:
        _courses_ref.pop(idx)
        if name in courses:
            del courses[name]
        print(f"Course {name} deleted successfully!")
    except Exception as e:
        print(f"Error: {e}")

def add_conflict():
    conflict_id = input("Enter conflict ID: ").strip()
    if conflict_id in conflicts:
        print("Conflict already exists.")
        return
    description = input("Enter conflict description: ").strip()
    conflicts[conflict_id] = {"description": description}
    print(f"Conflict {conflict_id} added successfully!")

def modify_conflict():
    _print_conflicts_list()
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
    _print_conflicts_list()
    conflict_id = input("Enter conflict ID to delete: ").strip()
    if conflict_id in conflicts:
        del conflicts[conflict_id]
        print(f"Conflict {conflict_id} deleted successfully!")
    else:
        print("Conflict not found.")

def cli_menu():
    _refresh_local_view_from_ref()
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
            _refresh_local_view_from_ref()
            print("Courses:")
            for name, data in courses.items():
                print(f"  {name}: credits={data['credits']}, room={data['room']}")
        elif choice == "8":
            if conflicts:
                print("Conflicts:")
                for cid, data in conflicts.items():
                    print(f"  {cid}: description={data['description']}")
            else:
                print("No conflicts found.")
        elif choice == "9":
            return
        else:
            print("Invalid choice, try again.")

def mainCourseController(courses_list, config_path):
    global _courses_ref
    _courses_ref = courses_list
    cli_menu()