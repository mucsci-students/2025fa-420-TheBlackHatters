# File Name: course_cli.py
# Author: Ben Richardson, Fletcher Burton
# Last Modified: September 21, 2025

import sys
from typing import List, Optional
from Models.courses.Course_model import Course

courses = {}
conflicts = {}
_courses_ref = None
_rooms_ref: List[str] = []
_labs_ref: List[str] = []
_faculty_names: List[str] = []

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
        # this dict is only used for quick display of a single line,
        # duplicates will be listed separately in _print_courses_list()
        courses[name] = {
            "credits": str(c.get("credits", "")),
            "room": _first_or_empty(c.get("room", [])),
        }

def _find_course_indexes(course_name: str) -> List[int]:
    name = (course_name or "").strip()
    idxs = []
    for i, c in enumerate(_courses_ref or []):
        if str(c.get("course_id", "")).strip() == name:
            idxs.append(i)
    return idxs

def _pick_course_index_for_modify(name: str) -> int:
    idxs = _find_course_indexes(name)
    if not idxs:
        return -1
    if len(idxs) == 1:
        return idxs[0]
    print(f"Multiple '{name}' found:")
    for n, i in enumerate(idxs, 1):
        cd = _courses_ref[i]
        rooms = ", ".join(cd.get("room", [])) or "(none)"
        labs = ", ".join(cd.get("lab", [])) or "(none)"
        fac = ", ".join(cd.get("faculty", [])) or "(none)"
        print(f"  {n}. credits={cd.get('credits','')}, rooms=[{rooms}], labs=[{labs}], faculty=[{fac}]")
    sel = input(f"Select 1-{len(idxs)}: ").strip()
    try:
        k = int(sel)
        if 1 <= k <= len(idxs):
            return idxs[k-1]
    except Exception:
        pass
    print("Invalid selection.")
    return -1

def _print_courses_list():
    if not _courses_ref:
        print("No courses found.")
        return
    print("Courses:")
    for c in _courses_ref:
        name = str(c.get("course_id", "")).strip() or "(unnamed)"
        rooms = ", ".join(c.get("room", [])) or "(none)"
        labs = ", ".join(c.get("lab", [])) or "(none)"
        faculty = ", ".join(c.get("faculty", [])) or "(none)"
        print(f"  {name}: credits={c.get('credits','')}, rooms=[{rooms}], labs=[{labs}], faculty=[{faculty}]")

def _print_single_course(name: str, idx: Optional[int] = None):
    if idx is None:
        idxs = _find_course_indexes(name)
        idx = idxs[0] if idxs else -1
    if idx == -1:
        print("Course not found.")
        return
    c = _courses_ref[idx]
    rooms = ", ".join(c.get("room", [])) or "(none)"
    labs = ", ".join(c.get("lab", [])) or "(none)"
    faculty = ", ".join(c.get("faculty", [])) or "(none)"
    conflicts_list = ", ".join(c.get("conflicts", [])) or "(none)"
    print(f"{name}:")
    print(f"  credits: {c.get('credits','')}")
    print(f"  rooms: {rooms}")
    print(f"  lab: {labs}")
    print(f"  faculty: {faculty}")
    print(f"  conflicts: {conflicts_list}")

def _parse_allowed_list(raw: str, allowed: List[str]) -> List[str]:
    vals = [x.strip() for x in (raw or "").split(",") if x.strip()]
    if not vals:
        return []
    bad = [v for v in vals if v not in allowed]
    if bad:
        raise ValueError(f"invalid entries: {', '.join(bad)}; allowed: {', '.join(allowed)}")
    seen = set()
    out = []
    for v in vals:
        if v not in seen:
            seen.add(v)
            out.append(v)
    return out

def _list_and_get_allowed(label: str, allowed: List[str], prompt: str, allow_blank_keep: bool = False) -> Optional[List[str]]:
    print(f"{label}: {', '.join(allowed) if allowed else '(none)'}")
    raw = input(prompt).strip()
    if allow_blank_keep and raw == "":
        return None
    return _parse_allowed_list(raw, allowed) if raw else []

def add_course():
    name = input("Enter course name: ").strip()
    if _find_course_indexes(name):
        print("Note: duplicate course name exists; adding another entry.")
    credits = input("Enter course credits: ").strip()
    rooms = _list_and_get_allowed("Available rooms", _rooms_ref, "Enter room(s) (comma separated) [optional]: ")
    labs = _list_and_get_allowed("Available labs", _labs_ref, "Enter labs (comma separated) [optional]: ")
    faculty = _list_and_get_allowed("Available faculty", _faculty_names, "Enter faculty (comma separated) [optional]: ")
    try:
        new_course = Course.build_and_validate(
            {
                "course_id": name,
                "credits": int(credits),
                "room": rooms or [],
                "lab": labs or [],
                "conflicts": [],
                "faculty": faculty or [],
            },
            strict_membership=False,
        )
        _courses_ref.append(new_course.to_dict())
        _refresh_local_view_from_ref()
        print(f"Course {name} added successfully!")
        _print_single_course(name, idx=len(_courses_ref)-1)
    except Exception as e:
        print(f"Error: {e}")

def modify_course():
    _print_courses_list()
    name = input("Enter course name to modify: ").strip()
    idx = _pick_course_index_for_modify(name)
    if idx == -1:
        print("Course not found.")
        return
    current = _courses_ref[idx]
    cur_rooms = ", ".join(current.get("room", [])) or "(none)"
    cur_labs = ", ".join(current.get("lab", [])) or "(none)"
    cur_fac = ", ".join(current.get("faculty", [])) or "(none)"
    print(f"Current data: {{'credits': '{current.get('credits','')}', 'rooms': '{cur_rooms}', 'lab': '{cur_labs}', 'faculty': '{cur_fac}'}}")
    credits = input("Enter new course credits (leave blank to keep current): ").strip()
    rooms = _list_and_get_allowed("Available rooms", _rooms_ref, "Enter room(s) (comma separated; leave blank to keep current): ", allow_blank_keep=True)
    labs = _list_and_get_allowed("Available labs", _labs_ref, "Enter labs (comma separated; leave blank to keep current): ", allow_blank_keep=True)
    faculty = _list_and_get_allowed("Available faculty", _faculty_names, "Enter faculty (comma separated; leave blank to keep current): ", allow_blank_keep=True)
    try:
        cur = Course.from_dict(current)
        if credits:
            cur.set_credits(int(credits))
        if rooms is not None:
            cur.set_rooms(rooms)
        if labs is not None:
            cur.set_labs(labs)
        if faculty is not None:
            cur.set_faculty(faculty)
        cur.validate(ignore_index=idx, strict_membership=False)
        _courses_ref[idx] = cur.to_dict()
        _refresh_local_view_from_ref()
        print(f"Course {name} updated successfully!")
        _print_single_course(name, idx=idx)
    except Exception as e:
        print(f"Error: {e}")

def delete_course():
    _print_courses_list()
    name = input("Enter course name to delete: ").strip()
    idxs = _find_course_indexes(name)
    if not idxs:
        print("Course not found.")
        return
    if len(idxs) > 1:
        print(f"Multiple '{name}' found:")
        for n, i in enumerate(idxs, 1):
            cd = _courses_ref[i]
            rooms = ", ".join(cd.get("room", [])) or "(none)"
            labs = ", ".join(cd.get("lab", [])) or "(none)"
            fac = ", ".join(cd.get("faculty", [])) or "(none)"
            print(f"  {n}. credits={cd.get('credits','')}, rooms=[{rooms}], labs=[{labs}], faculty=[{fac}]")
        sel = input(f"Select 1-{len(idxs)}: ").strip()
        try:
            k = int(sel)
            if 1 <= k <= len(idxs):
                idx = idxs[k-1]
            else:
                print("Invalid selection.")
                return
        except Exception:
            print("Invalid selection.")
            return
    else:
        idx = idxs[0]
    try:
        removed = _courses_ref.pop(idx)
        _refresh_local_view_from_ref()
        print(f"Course {removed.get('course_id','(unnamed)')} deleted successfully!")
    except Exception as e:
        print(f"Error: {e}")

def add_conflict():
    _print_courses_list()
    course_name = input("Enter course name to add a conflict to: ").strip()
    idx = _pick_course_index_for_modify(course_name)
    if idx == -1:
        print("Course not found.")
        return
    all_course_names = [str(c.get("course_id","")).strip() for c in _courses_ref]
    print(f"Available course names: {', '.join(all_course_names)}")
    conflict_name = input("Enter conflicting course name: ").strip()
    if conflict_name not in all_course_names:
        print("Invalid conflict name.")
        return
    try:
        cur = Course.from_dict(_courses_ref[idx])
        cur.add_conflicts([conflict_name])
        cur.validate(strict_membership=False)
        _courses_ref[idx] = cur.to_dict()
        print(f"Conflict '{conflict_name}' added to {course_name}.")
        _print_single_course(course_name, idx=idx)
    except Exception as e:
        print(f"Error: {e}")

def modify_conflict():
    _print_courses_list()
    course_name = input("Enter course name whose conflict you want to modify: ").strip()
    idx = _pick_course_index_for_modify(course_name)
    if idx == -1:
        print("Course not found.")
        return
    cur_dict = _courses_ref[idx]
    current_conflicts = list(cur_dict.get("conflicts", []))
    if not current_conflicts:
        print("No conflicts found.")
        return
    print("Conflicts:")
    for c in current_conflicts:
        print(f"  {c}")
    all_course_names = [str(c.get("course_id","")).strip() for c in _courses_ref]
    print(f"Available course names: {', '.join(all_course_names)}")
    old_name = input("Enter existing conflict name to change: ").strip()
    if old_name not in current_conflicts:
        print("Conflict not found.")
        return
    new_name = input("Enter new conflict name: ").strip()
    if new_name not in all_course_names:
        print("Invalid conflict name.")
        return
    try:
        cur = Course.from_dict(cur_dict)
        cur.remove_conflicts([old_name])
        cur.add_conflicts([new_name])
        cur.validate(strict_membership=False)
        _courses_ref[idx] = cur.to_dict()
        print(f"Conflict '{old_name}' changed to '{new_name}' for {course_name}.")
        _print_single_course(course_name, idx=idx)
    except Exception as e:
        print(f"Error: {e}")

def delete_conflict():
    _print_courses_list()
    course_name = input("Enter course name to delete a conflict from: ").strip()
    idx = _pick_course_index_for_modify(course_name)
    if idx == -1:
        print("Course not found.")
        return
    cur_dict = _courses_ref[idx]
    current_conflicts = list(cur_dict.get("conflicts", []))
    if not current_conflicts:
        print("No conflicts found.")
        return
    print("Conflicts:")
    for c in current_conflicts:
        print(f"  {c}")
    conflict_name = input("Enter conflict name to delete: ").strip()
    if conflict_name not in current_conflicts:
        print("Conflict not found.")
        return
    try:
        cur = Course.from_dict(cur_dict)
        cur.remove_conflicts([conflict_name])
        cur.validate(strict_membership=False)
        _courses_ref[idx] = cur.to_dict()
        print(f"Conflict '{conflict_name}' removed from {course_name}.")
        _print_single_course(course_name, idx=idx)
    except Exception as e:
        print(f"Error: {e}")

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
        print("8. Show Conflicts For A Course")
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
            _print_courses_list()
        elif choice == "8":
            _print_courses_list()
            course_name = input("Enter course name to view conflicts: ").strip()
            idxs = _find_course_indexes(course_name)
            if not idxs:
                print("Course not found.")
            else:
                # if duplicates, just show all conflicts from each match
                for j, idx in enumerate(idxs, 1):
                    cur = _courses_ref[idx]
                    lst = cur.get("conflicts", [])
                    if len(idxs) > 1:
                        print(f"Instance {j}:")
                    if lst:
                        print("Conflicts:")
                        for c in lst:
                            print(f"  {c}")
                    else:
                        print("No conflicts found.")
        elif choice == "9":
            return
        else:
            print("Invalid choice, try again.")

def mainCourseController(courses_list, rooms_obj_or_list, labs_obj_or_list, faculty_list):
    global _courses_ref, _rooms_ref, _labs_ref, _faculty_names
    _courses_ref = courses_list
    if hasattr(rooms_obj_or_list, "rooms"):
        _rooms_ref = list(rooms_obj_or_list.rooms or [])
    else:
        _rooms_ref = list(rooms_obj_or_list or [])
    if hasattr(labs_obj_or_list, "labs"):
        _labs_ref = list(labs_obj_or_list.labs or [])
    else:
        _labs_ref = list(labs_obj_or_list or [])
    _faculty_names = [f.get("name","") for f in (faculty_list or []) if isinstance(f, dict) and f.get("name")]
    cli_menu()