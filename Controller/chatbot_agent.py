import functools
import json
import time
import traceback
import re
from typing import List
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import StructuredTool
from langgraph.prebuilt import create_react_agent

from Controller.main_controller import DM

import os

import os
from dotenv import load_dotenv

# Load .env variables if present
load_dotenv()

# Ensure the key exists
if not os.getenv("OPENAI_API_KEY"):
    print("[ERROR] Missing OpenAI API key.")


# Tool Argument schemas

class AddItemArgs(BaseModel):
    category: str = Field(
        description="Which type of item to add: room, lab, course, or faculty."
    )
    data: dict = Field(
        default_factory=dict,
        description=(
            "The data for the new item to add (e.g. {'course_id': 'EDU 112', 'credits': 3, "
            "'room': ['Roddy 136'], 'lab': [], 'faculty': ['Zoppetti']})."
        ),
    )


class EditItemArgs(BaseModel):
    category: str = Field(description="Which category to edit: room, lab, course, or faculty.")
    identifier: str = Field(description="Name or ID of the item to edit.")
    updates: dict = Field(description="Dictionary of updates to apply to the item.")


class DeleteItemArgs(BaseModel):
    category: str = Field(description="Which category to delete from: room, lab, course, or faculty.")
    identifier: str = Field(description="Name or ID of the item to delete.")

class KeyPathArgs(BaseModel):
    key_path: str = Field(
        description="Dot-separated path to the key in the configuration JSON (e.g. faculty[0].name)"
    )
    new_value: str = Field(description="New value (string or JSON).")


class NoArgs(BaseModel):
    pass


class ChatbotAgent:
    def __init__(self, config_path_getter):
        self.get_config_path = config_path_getter

        # Check API key before initializing model
        if not os.getenv("OPENAI_API_KEY"):
            print("[ERROR] OPENAI_API_KEY is not set. The chatbot cannot be initialized.")
            self.model = None
            self.agent_executor = None
            self.disabled = True
            return
        else:
            self.disabled = False

        print("[DEBUG] Initializing ChatbotAgent with OpenAI model...")
        self.model = init_chat_model(
            "gpt-5-mini",
            model_provider="openai",
            temperature=0.2,
            max_tokens=512
        )

        self.tools = self._create_tools()
        print(f"[DEBUG] Registered {len(self.tools)} tools: {[t.name for t in self.tools]}")

        self.agent_executor = create_react_agent(self.model, self.tools)
        print("[DEBUG] ChatbotAgent initialized successfully.\n")

    # Tool Implementations

    def _tool_view_config(self):
        """Return a summarized view of the current configuration (no full details, but includes duplicates)."""
        print("[DEBUG] Tool called: view_config")
        try:
            if not hasattr(DM, "data") or not DM.data:
                return "No configuration loaded. Please import a config file first."

            config = DM.data.get("config", {})
            summary_lines = []

            # --- Rooms ---
            rooms = config.get("rooms", [])
            summary_lines.append("Rooms:")
            if rooms:
                for r in rooms:
                    summary_lines.append(f"  • {r}")
            else:
                summary_lines.append("  None")

            # --- Labs ---
            labs = config.get("labs", [])
            summary_lines.append("\nLabs:")
            if labs:
                for lab in labs:
                    summary_lines.append(f"  • {lab}")
            else:
                summary_lines.append("  None")

            # --- Courses (include duplicates clearly) ---
            courses = config.get("courses", [])
            summary_lines.append(f"\nCourses ({len(courses)} total):")
            if not courses:
                summary_lines.append("  None found.")
            else:
                course_counts = {}
                for c in courses:
                    cid = c.get("course_id", "Unknown")
                    course_counts[cid] = course_counts.get(cid, 0) + 1
                    dup_count = course_counts[cid]

                    if dup_count > 1:
                        summary_lines.append(f"  • {cid} (duplicate #{dup_count})")
                    else:
                        summary_lines.append(f"  • {cid}")

            # --- Faculty ---
            faculty = config.get("faculty", [])
            summary_lines.append(f"\nFaculty ({len(faculty)} total):")
            if not faculty:
                summary_lines.append("  None found.")
            else:
                for f in faculty:
                    if isinstance(f, dict):
                        name = f.get("name") or f.get("faculty_name") or str(f)
                    else:
                        name = str(f)
                    summary_lines.append(f"  • {name}")

            # --- Helpful follow-up prompt ---
            summary_lines.append(
                "\nWould you like to see details for any category or specific item?\n"
                "You can ask things like:\n"
                "• 'Show details of all courses'\n"
                "• 'Show details for CMSC 140'\n"
                "• 'Show details for Zoppetti'\n"
            )

            return "\n".join(summary_lines)

        except Exception as e:
            print("[ERROR] view_config summary failed:", e)
            traceback.print_exc()
            return f"Error viewing configuration: {e}"

    def _tool_show_details(self, target: str):
        # Show detailed information for a category or specific entity, with fuzzy and semantic matching.
        print(f"[DEBUG] Tool called: show_details ({target})")
        try:
            import difflib

            if not hasattr(DM, "data") or not DM.data:
                return "No configuration loaded. Please import a config file first."

            config = DM.data.get("config", {})
            target_clean = target.lower().strip()

            # Clean input and remove filler words
            stopwords = [
                "the", "faculty", "course", "details", "of", "for", "about",
                "show", "me", "all", "information", "info", "available", "list", "view"
            ]
            for w in stopwords:
                target_clean = re.sub(rf"\b{w}\b", "", target_clean)
            target_clean = target_clean.strip()

            result_lines = []

            # Handle all-rooms queries
            if any(x in target.lower() for x in ["all rooms", "rooms", "room list"]):
                rooms = config.get("rooms", [])
                if not rooms:
                    return "No rooms found in the current configuration."
                result_lines.append(f"Showing all {len(rooms)} rooms:\n")
                for r in rooms:
                    result_lines.append(f"• {r}")
                return "\n".join(result_lines)

            # Handle all-labs queries
            if any(x in target.lower() for x in ["all labs", "labs", "lab list"]):
                labs = config.get("labs", [])
                if not labs:
                    return "No labs found in the current configuration."
                result_lines.append(f"Showing all {len(labs)} labs:\n")
                for l in labs:
                    result_lines.append(f"• {l}")
                return "\n".join(result_lines)

            # Handle all-courses queries
            if any(x in target.lower() for x in ["all courses", "courses", "course details"]):
                courses = config.get("courses", [])
                if not courses:
                    return "No courses found in the configuration."
                result_lines.append(f"Showing details for all {len(courses)} courses:\n")
                for idx, c in enumerate(courses, 1):
                    cid = c.get("course_id", "Unknown ID")
                    result_lines.append(
                        f"{idx}. {cid} ({c.get('credits', '?')} credits)\n"
                        f"  Rooms: {', '.join(c.get('room', [])) or 'None'}\n"
                        f"  Labs: {', '.join(c.get('lab', [])) or 'None'}\n"
                        f"  Faculty: {', '.join(c.get('faculty', [])) or 'None'}\n"
                        f"  Conflicts: {', '.join(c.get('conflicts', [])) or 'None'}\n"
                    )
                return "\n".join(result_lines)

            # Handle all-faculty queries
            if any(x in target.lower() for x in ["all faculty", "faculty", "faculty details"]):
                faculty_list = config.get("faculty", [])
                if not faculty_list:
                    return "No faculty found in the configuration."
                result_lines.append(f"Showing details for all {len(faculty_list)} faculty:\n")
                for f in faculty_list:
                    name = f.get("name", "Unknown")
                    result_lines.append(f"• {name}")
                return "\n".join(result_lines)

            # Specific course lookup (fuzzy)
            courses = config.get("courses", [])
            course_ids = [c.get("course_id", "").lower() for c in courses]
            close_match = difflib.get_close_matches(target_clean, course_ids, n=1, cutoff=0.6)
            if close_match:
                match = close_match[0]
                matches = [c for c in courses if c.get("course_id", "").lower() == match]
                if not matches:
                    return f"No course found for '{target}'."
                lines = [f"Found {len(matches)} instance(s) of course '{match.upper()}':"]
                for idx, c in enumerate(matches, 1):
                    lines.append(
                        f"\nInstance #{idx}:\n"
                        f"  ID: {c.get('course_id', 'Unknown ID')}\n"
                        f"  Credits: {c.get('credits', '?')}\n"
                        f"  Rooms: {', '.join(c.get('room', [])) or 'None'}\n"
                        f"  Labs: {', '.join(c.get('lab', [])) or 'None'}\n"
                        f"  Faculty: {', '.join(c.get('faculty', [])) or 'None'}\n"
                        f"  Conflicts: {', '.join(c.get('conflicts', [])) or 'None'}"
                    )
                return "\n".join(lines)

            # Specific faculty lookup (fuzzy, detailed)
            faculty_list = config.get("faculty", [])
            faculty_names = [f.get("name", "").lower() for f in faculty_list if isinstance(f, dict)]
            close_match = difflib.get_close_matches(target_clean, faculty_names, n=1, cutoff=0.6)
            if close_match:
                match_name = close_match[0]
                faculty_data = DM.getFacultyByName(match_name)
                if not faculty_data:
                    return f"No detailed information found for faculty '{match_name}'."

                lines = [f"Faculty: {faculty_data.get('name', 'Unknown')}"]
                lines.append(f"Min Credits: {faculty_data.get('minimum_credits', '?')}")
                lines.append(f"Max Credits: {faculty_data.get('maximum_credits', '?')}")
                lines.append(f"Unique Course Limit: {faculty_data.get('unique_course_limit', '?')}")

                # Availability
                times = faculty_data.get("times", {})
                if times:
                    lines.append("\nAvailability:")
                    for day, slots in times.items():
                        slot_text = ", ".join(slots) if slots else "None"
                        lines.append(f"  {day}: {slot_text}")

                # Preferences helper
                def prefs_to_str(title, prefs):
                    if not prefs:
                        return f"{title}: None"
                    pairs = [f"{k} ({v})" for k, v in prefs.items()]
                    return f"{title}: " + ", ".join(pairs)

                # Preferences
                lines.append("\n" + prefs_to_str("Course Preferences", faculty_data.get("course_preferences")))
                lines.append(prefs_to_str("Room Preferences", faculty_data.get("room_preferences")))
                lines.append(prefs_to_str("Lab Preferences", faculty_data.get("lab_preferences")))

                return "\n".join(lines)

            # Room or lab single-item fuzzy lookup
            all_rooms = [r.lower() for r in config.get("rooms", [])]
            all_labs = [l.lower() for l in config.get("labs", [])]

            match_room = difflib.get_close_matches(target_clean, all_rooms, n=1, cutoff=0.7)
            if match_room:
                return f"Room: {match_room[0].title()}"

            match_lab = difflib.get_close_matches(target_clean, all_labs, n=1, cutoff=0.7)
            if match_lab:
                return f"Lab: {match_lab[0].title()}"

            # Default fallback
            return f"No matching item found for '{target}'. Try 'all rooms', 'all labs', 'all courses', or a faculty name."

        except Exception as e:
            print("[ERROR] show_details failed:", e)
            traceback.print_exc()
            return f"Error showing details: {e}"

    def _tool_update_config_value(self, key_path: str, new_value: str):
        """Modify the configuration in DM.data and save."""
        print(f"[DEBUG] Tool called: update_config_value ({key_path} = {new_value})")
        try:
            if not hasattr(DM, "data") or not DM.data:
                return "No configuration loaded. Please import a config file first."

            # Navigate into DM.data using dot/bracket notation
            keys = key_path.split(".")
            ref = DM.data
            for k in keys[:-1]:
                if "[" in k and "]" in k:
                    name, idx = k[:-1].split("[")
                    ref = ref[name][int(idx)]
                else:
                    ref = ref[k]

            final_key = keys[-1]
            parsed_value = json.loads(new_value) if new_value.strip().startswith(("{", "[", '"')) else new_value
            if "[" in final_key and "]" in final_key:
                name, idx = final_key[:-1].split("[")
                ref[name][int(idx)] = parsed_value
            else:
                ref[final_key] = parsed_value

            # Persist changes using DataManager
            DM.saveData(self.get_config_path())
            return f"Updated {key_path} successfully."
        except Exception as e:
            print("[ERROR] update_config_value failed:", e)
            traceback.print_exc()
            return f"Error updating config: {e}"

    def _tool_add_item(self, category: str = None, data: dict = None):
        # Adds a new item (room, lab, course, or faculty) to configuration via DataManager validations.
        print(f"[DEBUG] Tool called: add_item (category={category}, data={data})")

        try:
            if not hasattr(DM, "data") or not DM.data:
                return "No configuration loaded. Please import a config file first."
            if category is None:
                return "You must specify a category such as 'room', 'lab', 'course', or 'faculty'."

            data = data or {}
            category = category.lower().strip()
            text = getattr(self, "last_user_input", "")

            # ----------------------------
            # ROOM LOGIC
            # ----------------------------
            if category in ["room", "rooms"]:
                new_room = data.get("name") or data.get("room") or data.get("id")

                if not new_room and text:
                    match = re.search(r"\b([A-Z][a-zA-Z]*(?:\s+\d+)*)\b", text)
                    if match:
                        new_room = match.group(1).strip()
                if not new_room:
                    return "Please provide a room name to add."

                try:
                    DM.addRoom(new_room)
                    print(f"[DEBUG] Added room via DataManager: {new_room}")
                    return f"Room '{new_room}' added to configuration (not yet saved)."
                except Exception as e:
                    return f"Failed to add room '{new_room}': {e}"

            # ----------------------------
            # LAB LOGIC
            # ----------------------------
            if category in ["lab", "labs"]:
                new_lab = data.get("name") or data.get("lab") or data.get("id")

                if not new_lab and text:
                    # Capture full lab name, like "Science Lab 3"
                    match = re.search(r"\b([A-Z][a-zA-Z]*(?:\s+[A-Za-z0-9]+)*)\b", text)
                    if match:
                        new_lab = match.group(1).strip()
                if not new_lab:
                    return "Please provide a lab name to add."

                try:
                    DM.addLab(new_lab)
                    print(f"[DEBUG] Added lab via DataManager: {new_lab}")
                    return f"Lab '{new_lab}' added to configuration (not yet saved)."
                except Exception as e:
                    return f"Failed to add lab '{new_lab}': {e}"

            # ----------------------------
            # FACULTY LOGIC
            # ----------------------------
            if category in ["faculty", "professor", "instructor"]:
                new_faculty = data
                text = getattr(self, "last_user_input", "")

                # --- Name extraction ---
                if "name" not in new_faculty or not new_faculty["name"]:
                    match = re.search(r"\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\b", text)
                    if match:
                        new_faculty["name"] = match.group(0).strip()
                if "name" not in new_faculty or not new_faculty["name"]:
                    return "Faculty entry must include a 'name' field."

                # --- Credit limits ---
                min_credits = re.search(r"min(?:imum)?\s*credits?\s*(?:of|is|=)?\s*(\d+)", text, re.IGNORECASE)
                max_credits = re.search(r"max(?:imum)?\s*credits?\s*(?:of|is|=)?\s*(\d+)", text, re.IGNORECASE)
                unique_limit = re.search(r"unique\s*course\s*limit\s*(?:of|is|=)?\s*(\d+)", text, re.IGNORECASE)

                new_faculty["minimum_credits"] = int(min_credits.group(1)) if min_credits else 0
                new_faculty["maximum_credits"] = int(max_credits.group(1)) if max_credits else 12
                new_faculty["unique_course_limit"] = int(unique_limit.group(1)) if unique_limit else 0

                # --- Availability parsing ---
                # Example input: "available from monday at 11am to 4pm"
                times = {"MON": [], "TUE": [], "WED": [], "THU": [], "FRI": [], "SAT": [], "SUN": []}
                day_map = {
                    "monday": "MON", "tuesday": "TUE", "wednesday": "WED",
                    "thursday": "THU", "friday": "FRI", "saturday": "SAT", "sunday": "SUN"
                }

                match = re.search(
                    r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday)"
                    r".*?(\d{1,2}\s*(?:am|pm)).*?(\d{1,2}\s*(?:am|pm))",
                    text,
                    re.IGNORECASE
                )
                if match:
                    day = match.group(1).lower()
                    start = match.group(2).upper().replace(" ", "")
                    end = match.group(3).upper().replace(" ", "")

                    # Convert times to HH:MM 24-hour format
                    def to_24h(t):
                        h = int(re.search(r"\d+", t).group(0))
                        if "PM" in t and h != 12:
                            h += 12
                        if "AM" in t and h == 12:
                            h = 0
                        return f"{h:02d}:00"

                    start_24, end_24 = to_24h(start), to_24h(end)
                    times[day_map[day]] = [f"{start_24}-{end_24}"]
                new_faculty["times"] = times

                # --- Course preferences ---
                # Example: "course preferences are CMSC 362 with a weight of 5"
                course_prefs = {}
                for match in re.finditer(r"\b([A-Z]{2,}\s?\d{2,4})\b.*?(?:weight\s*(?:of|=)?\s*(\d+))?", text):
                    code = match.group(1).strip().upper()
                    weight = int(match.group(2)) if match.group(2) else 1
                    course_prefs[code] = weight
                new_faculty["course_preferences"] = course_prefs

                # --- Room preferences ---
                # Example: "prefers Roddy 136 with weight 5"
                room_prefs = {}
                room_pattern = r"\b([A-Z][a-zA-Z]+(?:\s*\d+)?)\b.*?(?:weight\s*(?:of|=)?\s*(\d+))?"
                for match in re.finditer(room_pattern, text):
                    name = match.group(1).strip()
                    weight = int(match.group(2)) if match.group(2) else 1
                    if re.search(r"room|roddy|hall|lab|building", name, re.IGNORECASE):
                        room_prefs[name] = weight
                new_faculty["room_preferences"] = room_prefs

                # --- Lab preferences ---
                # Example: "lab preferences are Linux 5, Mac 1"
                lab_prefs = {}
                for match in re.finditer(r"\b(Linux|Mac|Windows|AI|Data)\b.*?(?:weight\s*(?:of|=)?\s*(\d+))?", text,
                                         re.IGNORECASE):
                    lab = match.group(1).capitalize()
                    weight = int(match.group(2)) if match.group(2) else 1
                    lab_prefs[lab] = weight
                new_faculty["lab_preferences"] = lab_prefs

                # --- Default values for missing prefs ---
                new_faculty.setdefault("course_preferences", {})
                new_faculty.setdefault("room_preferences", {})
                new_faculty.setdefault("lab_preferences", {})

                # --- Add via DataManager ---
                try:
                    DM.addFaculty(new_faculty)
                    print(f"[DEBUG] Added faculty via DataManager: {new_faculty}")
                    return f"Faculty '{new_faculty['name']}' added (not yet saved)."
                except Exception as e:
                    return f"Failed to add faculty '{new_faculty.get('name', '?')}': {e}"

            # ----------------------------
            # COURSE LOGIC
            # ----------------------------
            if category in ["course", "courses"]:
                course_id = data.get("course_id")
                if not course_id and text:
                    match = re.search(r"\b[A-Z]{2,}\s?\d{2,4}\b", text)
                    if match:
                        course_id = match.group(0).strip().upper()
                if not course_id:
                    return "Course must include a valid 'course_id' (e.g. CMSC 140)."

                credits = data.get("credits")
                if not credits and text:
                    match = re.search(r"(\d+)\s*credits?", text, re.IGNORECASE)
                    if match:
                        credits = int(match.group(1))
                if not credits:
                    credits = 4

                cfg = DM.data.get("config", {})
                known_rooms = cfg.get("rooms", [])
                known_labs = cfg.get("labs", [])
                known_faculty = [f.get("name") for f in cfg.get("faculty", []) if isinstance(f, dict)]
                known_courses = [c.get("course_id") for c in cfg.get("courses", [])]

                rooms = [r for r in known_rooms if r.lower() in text.lower()]
                if not rooms:
                    match = re.findall(r"\b[A-Z][a-zA-Z]*\s*\d+\b", text)
                    rooms = match or []

                labs = [l for l in known_labs if l.lower() in text.lower()]
                if not labs:
                    match = re.findall(r"\b[A-Z][a-zA-Z]*(?:\s+[A-Za-z0-9]+)*\b", text)
                    labs = [m for m in match if "lab" in m.lower()] or []

                faculty = [f for f in known_faculty if f.lower() in text.lower()]
                if not faculty:
                    match = re.findall(r"\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\b", text)
                    exclude = {"Room", "Lab", "Science", "Course", "Credits"}
                    faculty = [m for m in match if all(w not in exclude for w in m.split())]

                conflicts = [c for c in known_courses if c.lower() in text.lower()]
                if not conflicts:
                    match = re.findall(r"\b[A-Z]{2,}\s?\d{2,4}\b", text)
                    conflicts = match or []

                new_course = {
                    "course_id": course_id,
                    "credits": credits,
                    "room": rooms,
                    "lab": labs,
                    "faculty": faculty,
                    "conflicts": conflicts,
                }

                try:
                    DM.addCourse(new_course)
                    print(f"[DEBUG] Added course via DataManager: {new_course}")
                    return f"Course '{course_id}' added (not yet saved)."
                except Exception as e:
                    return f"Failed to add course '{course_id}': {e}"

            return f"Unknown category '{category}'. Use room, lab, course, or faculty."

        except Exception as e:
            print("[ERROR] add_item failed:", e)
            traceback.print_exc()
            return f"Error adding {category}: {e}"

    def _tool_edit_item(self, category: str, identifier: str, updates: dict):
        # Edits an existing item by name or ID in memory, without saving.
        print(f"[DEBUG] Tool called: edit_item (category={category}, identifier={identifier}, updates={updates})")
        try:
            if not hasattr(DM, "data") or not DM.data:
                return "No configuration loaded. Please import a config file first."

            category = category.lower().strip()
            cfg = DM.data.get("config", {})

            # Edit room
            if category in ["room", "rooms"]:
                rooms = cfg.get("rooms", [])
                if identifier not in rooms:
                    return f"Room '{identifier}' not found."
                idx = rooms.index(identifier)
                new_name = updates.get("name")
                if not new_name:
                    return "Please provide a new name for the room."
                rooms[idx] = new_name
                return f"Room '{identifier}' renamed to '{new_name}' (not yet saved)."

            # Edit lab
            if category in ["lab", "labs"]:
                labs = cfg.get("labs", [])
                if identifier not in labs:
                    return f"Lab '{identifier}' not found."
                idx = labs.index(identifier)
                new_name = updates.get("name")
                if not new_name:
                    return "Please provide a new name for the lab."
                labs[idx] = new_name
                return f"Lab '{identifier}' renamed to '{new_name}' (not yet saved)."

            # Edit course
            if category in ["course", "courses"]:
                courses = cfg.get("courses", [])
                found = None
                for c in courses:
                    if c.get("course_id") == identifier:
                        found = c
                        break
                if not found:
                    return f"Course '{identifier}' not found."
                found.update(updates)
                return f"Course '{identifier}' updated in memory (not yet saved)."

            # Edit faculty
            if category in ["faculty", "professor", "instructor"]:
                faculty_list = cfg.get("faculty", [])
                for f in faculty_list:
                    if f.get("name", "").lower() == identifier.lower():
                        f.update(updates)
                        return f"Faculty '{identifier}' updated in memory (not yet saved)."
                return f"Faculty '{identifier}' not found."

            return f"Unknown category '{category}'. Use room, lab, course, or faculty."

        except Exception as e:
            print("[ERROR] edit_item failed:", e)
            traceback.print_exc()
            return f"Error editing {category}: {e}"

    def _tool_delete_item(self, category: str, identifier: str):
        # Deletes an existing item by name or ID from memory.
        print(f"[DEBUG] Tool called: delete_item (category={category}, identifier={identifier})")
        try:
            if not hasattr(DM, "data") or not DM.data:
                return "No configuration loaded. Please import a config file first."

            category = category.lower().strip()
            cfg = DM.data.get("config", {})

            # Delete room
            if category in ["room", "rooms"]:
                rooms = cfg.get("rooms", [])
                if identifier not in rooms:
                    return f"Room '{identifier}' not found."
                rooms.remove(identifier)
                return f"Room '{identifier}' removed (not yet saved)."

            # Delete lab
            if category in ["lab", "labs"]:
                labs = cfg.get("labs", [])
                if identifier not in labs:
                    return f"Lab '{identifier}' not found."
                labs.remove(identifier)
                return f"Lab '{identifier}' removed (not yet saved)."

            # Delete course
            if category in ["course", "courses"]:
                courses = cfg.get("courses", [])
                for c in list(courses):
                    if c.get("course_id") == identifier:
                        courses.remove(c)
                        return f"Course '{identifier}' removed (not yet saved)."
                return f"Course '{identifier}' not found."

            # Delete faculty
            if category in ["faculty", "professor", "instructor"]:
                faculty_list = cfg.get("faculty", [])
                for f in list(faculty_list):
                    if f.get("name", "").lower() == identifier.lower():
                        faculty_list.remove(f)
                        return f"Faculty '{identifier}' removed (not yet saved)."
                return f"Faculty '{identifier}' not found."

            return f"Unknown category '{category}'. Use room, lab, course, or faculty."

        except Exception as e:
            print("[ERROR] delete_item failed:", e)
            traceback.print_exc()
            return f"Error deleting {category}: {e}"

    # Tool registration

    # Tool registration
    def _create_tools(self) -> List[StructuredTool]:
        return [
            StructuredTool.from_function(
                name="view_config",
                func=self._tool_view_config,
                description="Display the current scheduler configuration summary.",
                args_schema=NoArgs,
                return_direct=True,
            ),
            StructuredTool.from_function(
                name="update_config_value",
                func=self._tool_update_config_value,
                description="Update a field in the configuration using dot notation.",
                args_schema=KeyPathArgs,
                return_direct=True,
            ),
            StructuredTool.from_function(
                name="show_details",
                func=self._tool_show_details,
                description="Show detailed information for a specific item or category (e.g., all courses, Zoppetti, CMSC 140).",
                return_direct=True,
            ),
            StructuredTool.from_function(
                name="add_item",
                func=self._tool_add_item,
                description="Add a new room, lab, course, or faculty to the current configuration.",
                args_schema=AddItemArgs,
                return_direct=True,
            ),
            StructuredTool.from_function(
                name="edit_item",
                func=self._tool_edit_item,
                description="Edit an existing room, lab, course, or faculty in the configuration.",
                args_schema=EditItemArgs,
                return_direct=True,
            ),
            StructuredTool.from_function(
                name="delete_item",
                func=self._tool_delete_item,
                description="Delete an existing room, lab, course, or faculty from the configuration.",
                args_schema=DeleteItemArgs,
                return_direct=True,
            ),
        ]

    # Query endpoint

    def query(self, user_input: str) -> str:
        if getattr(self, "disabled", False):
            return "The AI Chatbot is disabled because no OpenAI API key was set."

        try:
            text = (user_input or "").strip()

            # Direct detail commands
            if text.lower().startswith("show details"):
                target = re.sub(r"show details( of| for)?", "", text, flags=re.I).strip() or "all courses"
                return self._tool_show_details(target)

            # Greetings / small talk
            if re.fullmatch(r"(hi|hello|hey|howdy|yo|sup)\W*", text.lower()):
                return (
                    "Hi! I can help with the scheduler configuration.\n"
                    "• View the current config (rooms, labs, courses, faculty)\n"
                    "• Make a change (e.g., “remove Mac lab from CMSC 330”)\n"
                    "• Explain what a field does\n\n"
                    "What would you like to do?"
                )

            self.last_user_input = user_input
            print(f"\n[DEBUG] Query started: {user_input}")

            system_message = SystemMessage(
                content=(
                    "You are the academic scheduling assistant.\n"
                    "Only use tools when explicitly requested by the user (view/change/show details).\n"
                    "Use 'view_config' to summarize the configuration in plain text (not JSON)."
                )
            )

            start = time.time()
            result = self.agent_executor.invoke({"messages": [system_message, HumanMessage(content=user_input)]})
            elapsed = time.time() - start
            print(f"[DEBUG] Agent call completed in {elapsed:.2f}s")

            # Universal Extractor
            response = None

            if isinstance(result, dict):
                # Direct top-level fields
                for key in ["output", "return_values", "final_output"]:
                    if key in result and result[key]:
                        response = str(result[key])
                        print(f"[DEBUG] Found response in result['{key}']")
                        break

                # Search inside messages (covers ToolMessage & AIMessage)
                if not response and "messages" in result:
                    for m in result["messages"]:
                        msg_dict = (
                            m.__dict__
                            if hasattr(m, "__dict__")
                            else m
                            if isinstance(m, dict)
                            else {}
                        )

                        # a) ToolMessage case (the most common for tool output)
                        if getattr(m, "__class__", type(m)).__name__ == "ToolMessage" or msg_dict.get("name"):
                            if "content" in msg_dict and msg_dict["content"]:
                                response = msg_dict["content"]
                                print("[DEBUG] Found response in ToolMessage.content")
                                break

                        # b) Direct content with summary keywords
                        if "content" in msg_dict and msg_dict["content"]:
                            content = msg_dict["content"]
                            if isinstance(content, str) and any(
                                    k in content for k in ["Rooms:", "Labs:", "Courses", "Faculty", "Showing details"]
                            ):
                                response = content
                                print("[DEBUG] Found response in message.content (tool text)")
                                break

                        # c) Embedded outputs in additional_kwargs
                        extras = msg_dict.get("additional_kwargs", {})
                        if extras:
                            for k, v in extras.items():
                                if isinstance(v, str) and any(
                                        kw in v for kw in ["Rooms:", "Labs:", "Courses", "Faculty", "Showing details"]
                                ):
                                    response = v
                                    print(f"[DEBUG] Found response in message.additional_kwargs['{k}']")
                                    break
                            if response:
                                break

                # LangGraph “tool_calls” fallback
                if not response and "tool_calls" in result:
                    response = str(result["tool_calls"])
                    print("[DEBUG] Found response in result['tool_calls']")

            # Default fallback
            if not response or not str(response).strip():
                print("[DEBUG] Could not extract tool output; dumping message structure:")
                from pprint import pprint
                pprint(result.get("messages", []))
                response = "(No response received.)"

            print(f"[DEBUG] Final resolved response:\n{response[:500]}...")
            return response

        except Exception as e:
            print("[ERROR] query() exception:", e)
            traceback.print_exc()
            return f"Error: {e}"