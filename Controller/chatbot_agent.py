# ChatbotAgent.py

import os
import re
import json
import traceback
from typing import List, Dict, Optional, Tuple
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.tools import StructuredTool
from langgraph.prebuilt import create_react_agent

from Controller.main_controller import DM  # DataManager singleton

# Load .env for OPENAI_API_KEY if present
load_dotenv()


# -------------------------------
# Pydantic schemas (for tools API)
# -------------------------------

class AddItemArgs(BaseModel):
    category: str = Field(description="room | lab | course | faculty")
    data: dict = Field(default_factory=dict, description="Values to add for the item.")


class EditItemArgs(BaseModel):
    category: str = Field(description="room | lab | course | faculty")
    identifier: str = Field(description="Primary key of the item (e.g. course_id or faculty name)")
    updates: dict = Field(description="Fields to replace on the item.")


class DeleteItemArgs(BaseModel):
    category: str = Field(description="room | lab | course | faculty")
    identifier: str = Field(description="The item to remove (e.g. 'CMSC 140', 'Roddy 136').")


class KeyPathArgs(BaseModel):
    key_path: str = Field(description="Dot/bracket notation path into DM.data")
    new_value: str = Field(description="JSON string or raw string for the new value.")


class NoArgs(BaseModel):
    pass


# -------------------------------
# Chatbot Agent
# -------------------------------

class ChatbotAgent:
    """
    Natural-language CRUD over the scheduler config (rooms, labs, courses, faculty).
    Returns structured dicts that the GUI can use to change tabs & refresh.
    """

    def __init__(self, config_path_getter):
        self.get_config_path = config_path_getter

        self.disabled = False
        if not os.getenv("OPENAI_API_KEY"):
            print("[ERROR] Missing OPENAI_API_KEY. Chatbot disabled.")
            self.model = None
            self.agent_executor = None
            self.disabled = True
            return

        # Model is not used to generate text; we keep it set up for parity with your stack.
        self.model = init_chat_model(
            "gpt-5-mini",
            model_provider="openai",
            temperature=0.0,
            max_tokens=256,
        )
        # Register tools (we call them directly; create_react_agent kept for compatibility)
        self.tools = self._create_tools()
        self.agent_executor = create_react_agent(self.model, self.tools)

        self.last_user_input = ""

    # -----------
    # UI helpers
    # -----------

    @staticmethod
    def _switch_tab_for(category: str) -> str:
        m = {
            "course": "Courses",
            "courses": "Courses",
            "room": "Rooms",
            "rooms": "Rooms",
            "lab": "Labs",
            "labs": "Labs",
            "faculty": "Faculty",
            "professor": "Faculty",
            "instructor": "Faculty",
            "teacher": "Faculty",
        }
        return m.get(category.lower(), "Faculty")

    @staticmethod
    def _ok(response: str, category: str, action: str, payload: Optional[dict] = None) -> dict:
        return {
            "response": response,
            "category": category,
            "action": action,
            "switch_tab": ChatbotAgent._switch_tab_for(category),
            **({"payload": payload} if payload else {}),
        }

    @staticmethod
    def _err(response: str, category: str, action: str) -> dict:
        return {
            "response": response,
            "category": category,
            "action": action,
            "switch_tab": ChatbotAgent._switch_tab_for(category),
            "error": True,
        }

    # -------------------------
    # Tool: view / update value
    # -------------------------

    def _tool_view_config(self):
        if not hasattr(DM, "data") or not DM.data:
            return "No configuration loaded."
        cfg = DM.data.get("config", {})
        rooms = len(cfg.get("rooms", []))
        labs = len(cfg.get("labs", []))
        courses = len(cfg.get("courses", []))
        faculty = len(cfg.get("faculty", []))
        return f"Config summary: {rooms} rooms, {labs} labs, {courses} courses, {faculty} faculty."

    def _tool_update_config_value(self, key_path: str, new_value: str):
        try:
            if not hasattr(DM, "data") or not DM.data:
                return "No configuration loaded. Import a config first."

            ref = DM.data
            keys = key_path.split(".")
            for k in keys[:-1]:
                if "[" in k and "]" in k:
                    name, idx = k[:-1].split("[")
                    ref = ref[name][int(idx)]
                else:
                    ref = ref[k]

            final_key = keys[-1]
            val = json.loads(new_value) if new_value.strip().startswith(("{", "[", '"')) else new_value
            if "[" in final_key and "]" in final_key:
                name, idx = final_key[:-1].split("[")
                ref[name][int(idx)] = val
            else:
                ref[final_key] = val

            DM.saveData(self.get_config_path())
            return f"Updated {key_path}."
        except Exception as e:
            traceback.print_exc()
            return f"Error updating {key_path}: {e}"

    def _tool_show_details(self, target: str = ""):
        # Kept simple for now
        try:
            cfg = DM.data.get("config", {})
            t = (target or "").strip().lower()
            if t in ("rooms", "room"):
                return {"rooms": cfg.get("rooms", [])}
            if t in ("labs", "lab"):
                return {"labs": cfg.get("labs", [])}
            if t in ("courses", "course"):
                return {"courses": cfg.get("courses", [])}
            if t in ("faculty", "instructors", "professors"):
                return {"faculty": cfg.get("faculty", [])}
            return "Say 'show courses', 'show rooms', etc."
        except Exception as e:
            return f"Error: {e}"

    # -------------------------
    # Parsing helpers
    # -------------------------

    @staticmethod
    def _find_first_course_id(text: str) -> Optional[str]:
        """
        Accept ANY token sequence that looks like 'Word(s) number' (e.g., "BIO 345", "EDU 112", "CMSC 140"),
        OR a single token with letters+digits ("CS150", "PHYS204").
        If multiple matches, prefer the one nearest 'course' mention.
        """
        # Generic patterns (liberal)
        patterns = [
            r"\b[A-Za-z]{2,}\s*\d{1,4}[A-Za-z]?\b",       # Word 123 / Word123 / Word123A
            r"\b[A-Za-z]{2,}\s+[A-Za-z]{2,}\s*\d{1,4}\b"  # Two words then digits (e.g., "Data Sci 200")
        ]
        for pat in patterns:
            m = re.search(pat, text)
            if m:
                return m.group(0).strip()
        return None

    @staticmethod
    def _find_number_after(text: str, key: str) -> Optional[int]:
        m = re.search(rf"{key}\s*(?:of|is|=|to)?\s*(\d+)", text, flags=re.IGNORECASE)
        return int(m.group(1)) if m else None

    @staticmethod
    def _extract_faculty_names_from_text(text: str) -> List[str]:
        # Heuristic: Proper names (capitalized words, optionally two tokens)
        names = re.findall(r"\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)?\b", text)
        # Remove common nouns that collide
        blacklist = {"Room", "Lab", "Building", "Course", "Credits", "Add", "Delete", "Edit"}
        return [n for n in names if n not in blacklist]

    @staticmethod
    def _extract_rooms_from_text(text: str, known_rooms: List[str]) -> List[str]:
        res = []
        lower = text.lower()
        # Include any known rooms explicitly mentioned
        for r in known_rooms:
            if r.lower() in lower:
                res.append(r)
        # Also catch patterns like "Roddy 73", "Muncy 445"
        for m in re.findall(r"\b[A-Z][a-zA-Z]+\s*\d+\b", text):
            if m not in res:
                res.append(m)
        # Deduplicate while preserving order
        return list(dict.fromkeys(res))

    @staticmethod
    def _extract_labs_from_text(text: str, known_labs: List[str]) -> List[str]:
        res = []
        lower = text.lower()
        for l in known_labs:
            if l.lower() in lower:
                res.append(l)
        # Also allow single tokens like "Linux", "Mac"
        for m in re.findall(r"\b[A-Z][a-zA-Z0-9]+\b", text):
            if m in ("Lab", "Room"):
                continue
            if m not in res and any(m.lower() == k.lower() for k in known_labs):
                res.append(m)
        return list(dict.fromkeys(res))

    @staticmethod
    def _extract_conflicts_from_text(text: str, known_rooms: List[str] = None, known_labs: List[str] = None) -> List[
        str]:
        """
        Extract course-like tokens (e.g., CMSC 161, BIO 120) while excluding known rooms/labs
        and ignoring numeric-only or verb fragments like 'be 5'.
        """
        known_rooms = [r.lower() for r in (known_rooms or [])]
        known_labs = [l.lower() for l in (known_labs or [])]

        # Match only tokens that have letters immediately followed by digits
        matches = re.findall(r"\b[A-Za-z]{2,}\s*\d{1,4}[A-Za-z]?\b", text)
        results = []
        for m in matches:
            lower_m = m.lower()
            if lower_m in known_rooms or lower_m in known_labs:
                continue
            # Skip nonsense like "be 5" or verbs before digits
            if re.match(r"be\s*\d+", m, re.IGNORECASE):
                continue
            results.append(m.strip())
        return list(dict.fromkeys(results))

    @staticmethod
    def _convert_to_24h(t: str) -> str:
        """Convert strings like '9am', '14:30', '4 pm' into 24-hour format '09:00'."""
        t = t.strip().lower()
        m = re.match(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", t)
        if not m:
            return t  # already looks like 13:10 or malformed
        hh = int(m.group(1))
        mm = int(m.group(2) or 0)
        ap = (m.group(3) or "").lower()
        if ap == "pm" and hh != 12:
            hh += 12
        if ap == "am" and hh == 12:
            hh = 0
        return f"{hh:02d}:{mm:02d}"

    @staticmethod
    def _extract_min_max_uniq(text: str) -> Tuple[Optional[int], Optional[int], Optional[int]]:
        """
        Extract minimum_credits, maximum_credits, and unique_course_limit
        from flexible natural language such as:
          - "min credits is set to 2"
          - "maximum credits set to 8"
          - "4 min credits and 4 max credits"
          - "unique course limit of 20"
          - "min 3 max 8"
        Returns (min_credits, max_credits, unique_limit)
        """
        text = text.lower()

        # --- helper to try multiple regexes and return first match ---
        def grab(patterns):
            for p in patterns:
                m = re.search(p, text, flags=re.IGNORECASE)
                if m:
                    try:
                        return int(m.group(1))
                    except Exception:
                        pass
            return None

        # --- comprehensive patterns ---
        min_patterns = [
            # “min credits is set to 2”
            r"\bmin(?:imum)?\s*credits?\s*(?:is|are)?\s*(?:set\s*to|to|=|of)?\s*(\d+)",
            # “min credits 4”
            r"\bmin(?:imum)?\s*credits?\s*(\d+)",
            # “4 min credits”
            r"(\d+)\s*min(?:imum)?\s*credits?",
            # “min 4”
            r"\bmin(?:imum)?\s*(\d+)"
        ]

        max_patterns = [
            r"\bmax(?:imum)?\s*credits?\s*(?:is|are)?\s*(?:set\s*to|to|=|of)?\s*(\d+)",
            r"\bmax(?:imum)?\s*credits?\s*(\d+)",
            r"(\d+)\s*max(?:imum)?\s*credits?",
            r"\bmax(?:imum)?\s*(\d+)"
        ]

        uniq_patterns = [
            r"\bunique\s*(?:course\s*)?limit\s*(?:is|are)?\s*(?:set\s*to|to|=|of)?\s*(\d+)",
            r"\bunique\s*(?:course\s*)?limit\s*(\d+)"
        ]

        min_c = grab(min_patterns)
        max_c = grab(max_patterns)
        uniq = grab(uniq_patterns)

        print(f"[DEBUG] Extracted mins/max/uniq => min:{min_c} max:{max_c} uniq:{uniq}")
        return (min_c, max_c, uniq)

    @staticmethod
    def _parse_times_from_text(text: str) -> Dict[str, List[str]]:
        """
        Parse phrases like:
            "MON 10:00-12:00"
            "Monday 11am-4pm"
            "on mon 09:00-10:50, wed 14:00-15:00"
        Build a dict with ONLY the mentioned days; all others omitted (caller will clear).
        """
        day_map = {
            "mon": "MON", "monday": "MON",
            "tue": "TUE", "tues": "TUE", "tuesday": "TUE",
            "wed": "WED", "wednesday": "WED",
            "thu": "THU", "thur": "THU", "thurs": "THU", "thursday": "THU",
            "fri": "FRI", "friday": "FRI",
            "sat": "SAT", "saturday": "SAT",
            "sun": "SUN", "sunday": "SUN",
        }

        def to_24h(t: str) -> str:
            t = t.strip().lower()
            m = re.match(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", t)
            if not m:
                return t  # Already like 13:10
            hh = int(m.group(1))
            mm = int(m.group(2) or 0)
            ap = (m.group(3) or "").lower()
            if ap == "pm" and hh != 12:
                hh += 12
            if ap == "am" and hh == 12:
                hh = 0
            return f"{hh:02d}:{mm:02d}"

        results: Dict[str, List[str]] = {}
        # Pattern captures things like "mon 10:00-12:00", "monday 11am-4pm"
        for m in re.finditer(
            r"\b(mon|monday|tue|tues|tuesday|wed|wednesday|thu|thur|thurs|thursday|fri|friday|sat|saturday|sun|sunday)\b[^0-9a-zA-Z]+([0-9:apm\s]+)-([0-9:apm\s]+)",
            text, flags=re.IGNORECASE,
        ):
            raw_day, start_s, end_s = m.group(1), m.group(2), m.group(3)
            day = day_map[raw_day.lower()]
            start_24 = to_24h(start_s)
            end_24 = to_24h(end_s)
            results.setdefault(day, []).append(f"{start_24}-{end_24}")

        # Also allow compact forms: "mon 10-12", "wed 9-15"
        for m in re.finditer(
            r"\b(mon|tue|tues|wed|thu|thur|thurs|fri|sat|sun)\b\s+(\d{1,2})(?::(\d{2}))?-(\d{1,2})(?::(\d{2}))?",
            text, flags=re.IGNORECASE,
        ):
            raw_day, sh, sm, eh, em = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
            day = day_map[raw_day.lower()]
            sm_i = int(sm or 0)
            em_i = int(em or 0)
            start = f"{int(sh):02d}:{sm_i:02d}"
            end = f"{int(eh):02d}:{em_i:02d}"
            results.setdefault(day, []).append(f"{start}-{end}")

        return results

    @staticmethod
    def _parse_lab_prefs(text: str) -> Dict[str, int]:
        """
        Extract lab preferences from text, supporting:
          - "lab preference of the Mac lab weight of 1"
          - "the Mac lab weight of 1"
          - "Mac lab weight of 1"
          - "weight of 3 for Windows lab"
          - "AI lab = 2"
          - "Data 5"
        Returns {"Mac": 1, "Windows": 3, "Data": 5}
        """
        labs_norm = ["Linux", "Mac", "Windows", "AI", "Data", "GPU"]

        # Narrow scope to lab preference clause if present
        m_clause = re.search(
            r"(lab\s+preferences?|lab\s+preference)\b(?::| of)?\s*(.+?)(?=(?:course\s+preferences?|course\s+preference|room\s+preferences?|room\s+preference)\b|$)",
            text,
            flags=re.IGNORECASE | re.DOTALL,
        )
        span = m_clause.group(2) if m_clause else text  # fallback to full text

        pairs: Dict[str, int] = {}

        # --- Patterns ---
        # A. "<Lab> (lab)? weight of|= <num>" (handles "the Mac lab weight of 1")
        pat_a = re.compile(
            r"(?:the\s+)?(Linux|Mac|Windows|AI|Data|GPU)\b(?:\s+lab)?\s*(?:weight(?:\s+of)?|with a weight of|=)\s*(\d+)",
            flags=re.IGNORECASE,
        )

        # B. "weight of|= <num> for <Lab>" (handles "weight of 1 for the Mac lab")
        pat_b = re.compile(
            r"(?:weight(?:\s+of)?|with a weight of|=)\s*(\d+)\s*(?:for|to)?\s*(?:the\s+)?(Linux|Mac|Windows|AI|Data|GPU)\b(?:\s+lab)?",
            flags=re.IGNORECASE,
        )

        # C. Simple "<Lab> <num>" (handles "Mac 1" or "Mac lab 1")
        pat_c = re.compile(
            r"(?:the\s+)?(Linux|Mac|Windows|AI|Data|GPU)\b(?:\s+lab)?\s+(\d+)\b",
            flags=re.IGNORECASE,
        )

        # --- Run matches ---
        for rx in (pat_a, pat_b, pat_c):
            for g in rx.finditer(span):
                if rx is pat_b:
                    num, lab = g.group(1), g.group(2)
                else:
                    lab, num = g.group(1), g.group(2)
                lab = lab.capitalize()
                if lab in labs_norm:
                    pairs[lab] = int(num)

        # --- Debug output ---
        print("[DEBUG] Lab pref slice:", repr(span))
        print("[DEBUG] Lab pref matches:", json.dumps(pairs, indent=2))
        return pairs

    # -------------------------
    # ADD / EDIT / DELETE tools
    # -------------------------

    def _tool_add_item(self, category: str, data: dict):
        try:
            if not hasattr(DM, "data") or not DM.data:
                return self._err("No configuration loaded. Import a config first.", category, "add")

            text = (self.last_user_input or "")
            category = category.lower().strip()
            cfg = DM.data.get("config", {})

            if category in ("room", "rooms"):
                # Room name from text or data
                name = data.get("name")
                if not name:
                    # accept e.g., "Roddy 136", or last token after "room"
                    m = re.search(r"(?:room\s+|roddy\s+)?([A-Z][A-Za-z]+\s*\d+)", text, re.IGNORECASE)
                    name = m.group(1).strip() if m else None
                if not name:
                    return self._err("Plpaease specify a room name to add.", category, "add")
                try:
                    DM.addRoom(name)
                    return self._ok(f"Room '{name}' added (not yet saved).", category, "add")
                except Exception as e:
                    return self._err(f"Failed to add room '{name}': {e}", category, "add")

            if category in ("lab", "labs"):
                name = data.get("name")
                if not name:
                    # Improved: match patterns like "lab called Windows", "add a lab named Science Lab 3"
                    m = re.search(
                        r"(?:lab(?:\s+(?:called|named|is|called\s+as))?\s+)([A-Z][A-Za-z0-9]+(?:\s+[A-Za-z0-9]+)*)",
                        text,
                        re.IGNORECASE,
                    )
                    if not m:
                        # Fallback: standalone capitalized word after "lab"
                        m = re.search(r"lab\s+([A-Z][A-Za-z0-9]+(?:\s+[A-Za-z0-9]+)*)", text, re.IGNORECASE)
                    name = m.group(1).strip() if m else None

                if not name:
                    return self._err("Please specify a lab name to add.", category, "add")

                try:
                    DM.addLab(name)
                    return self._ok(f"Lab '{name}' added (not yet saved).", category, "add")
                except Exception as e:
                    return self._err(f"Failed to add lab '{name}': {e}", category, "add")

            if category in ("faculty", "professor", "instructor", "teacher"):
                # Build a full faculty object with sensible defaults
                new_fac = dict(data) if data else {}
                if "name" not in new_fac or not new_fac["name"]:
                    names = self._extract_faculty_names_from_text(text)
                    if names:
                        new_fac["name"] = names[0]
                if "name" not in new_fac or not new_fac["name"]:
                    return self._err("Faculty must include a name.", "faculty", "add")

                # Match "min credits" or "minimum credits"
                min_c, max_c, uniq = self._extract_min_max_uniq(text)
                new_fac.setdefault("minimum_credits", 0 if min_c is None else min_c)
                new_fac.setdefault("maximum_credits", 12 if max_c is None else max_c)
                new_fac.setdefault("unique_course_limit", 1 if uniq is None else uniq)

                # Times: if specified, put ONLY those days; others empty
                parsed_times = self._parse_times_from_text(text)

                # detect "monday from 9am to 5pm" style
                if not parsed_times:
                    for m in re.finditer(
                            r"(monday|tuesday|wednesday|thursday|friday|mon|tue|wed|thu|fri)\s*(?:from)?\s*([0-9:apm\s]+)\s*(?:to|-)\s*([0-9:apm\s]+)",
                            text, flags=re.IGNORECASE):
                        day, start, end = m.groups()
                        start_24 = self._convert_to_24h(start)
                        end_24 = self._convert_to_24h(end)
                        parsed_times.setdefault(day[:3].upper(), []).append(f"{start_24}-{end_24}")

                if parsed_times:
                    all_days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
                    new_fac["times"] = {d: parsed_times.get(d, []) for d in all_days}
                else:
                    # sensible default 9-5 M-F
                    new_fac["times"] = {
                        d: (["09:00-17:00"] if d in ["MON", "TUE", "WED", "THU", "FRI"] else [])
                        for d in ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
                    }

                # Preferences (fully replace if provided in data; otherwise parse from text)
                cp = data.get("course_preferences")
                rp = data.get("room_preferences")
                lp = data.get("lab_preferences")

                # Course preferences — only matches true course-like patterns
                if cp is None:
                    cp = {}
                    known_rooms = [r.lower() for r in cfg.get("rooms", [])]

                    # Match course-like tokens (e.g., CMSC 362, BIO 120)
                    for m in re.finditer(
                            r"\b([A-Z]{2,}\s*\d{1,4}[A-Za-z]?)\b\s*(?:weight|with a weight of|=)\s*(\d+)",
                            text,
                            re.IGNORECASE,
                    ):
                        course = m.group(1).strip()
                        # Exclude if it matches a known room (case-insensitive)
                        if not any(course.lower() == r for r in known_rooms):
                            cp[course.upper().replace("  ", " ")] = int(m.group(2))

                if rp is None:
                    rp = {}
                    for m in re.finditer(
                            r"\b([A-Z][A-Za-z]+\s*\d+)\b\s*(?:weight|with a weight of|=)\s*(\d+)",
                            text, re.IGNORECASE):
                        room_name = m.group(1)
                        # Avoid treating course IDs (like CMSC 4) as rooms
                        if not re.match(r"^[A-Z]{2,}\s*\d{1,4}$", room_name):
                            rp[room_name] = int(m.group(2))

                if lp is None:
                    lp = self._parse_lab_prefs(text)

                new_fac["course_preferences"] = cp
                new_fac["room_preferences"] = rp
                new_fac["lab_preferences"] = lp

                try:
                    print("[DEBUG] Faculty add payload:\n", json.dumps(new_fac, indent=2))
                    DM.addFaculty(new_fac)
                    return self._ok(f"Faculty '{new_fac['name']}' added (not yet saved).", "faculty", "add")
                except Exception as e:
                    return self._err(f"Failed to add faculty '{new_fac.get('name','?')}': {e}", "faculty", "add")

            if category in ("course", "courses"):
                course_id = data.get("course_id") or self._find_first_course_id(text)
                if not course_id:
                    return self._err("Please include a course id to add (e.g., 'add course BIO 345').", "course", "add")

                credits = data.get("credits")
                if credits is None:
                    # parse "... with 4 credits" or "... has 3 credits"
                    m = re.search(r"(\d+)\s*credits?", text, re.IGNORECASE)
                    credits = int(m.group(1)) if m else 4

                known_rooms = cfg.get("rooms", [])
                known_labs = cfg.get("labs", [])
                known_faculty = [f.get("name") for f in cfg.get("faculty", []) if isinstance(f, dict)]

                rooms = data.get("room") or self._extract_rooms_from_text(text, known_rooms)
                labs = data.get("lab") or self._extract_labs_from_text(text, known_labs)
                faculty = data.get("faculty") or [n for n in self._extract_faculty_names_from_text(text) if n in known_faculty]

                # Conflicts from text (remove self if present)
                conflicts = data.get("conflicts")
                if conflicts is None:
                    conflicts = [c for c in self._extract_conflicts_from_text(text) if c.upper() != course_id.upper()]

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
                    return self._ok(f"Course '{course_id}' added (not yet saved).", "course", "add")
                except Exception as e:
                    return self._err(f"Failed to add course '{course_id}': {e}", "course", "add")

            return self._err(f"Unknown category '{category}'.", category, "add")
        except Exception as e:
            traceback.print_exc()
            return self._err(f"Error adding {category}: {e}", category, "add")

    def _tool_edit_item(self, category: str, identifier: str, updates: dict):
        try:
            if not hasattr(DM, "data") or not DM.data:
                return self._err("No configuration loaded. Import a config first.", category, "edit")

            category = category.lower().strip()
            cfg = DM.data.get("config", {})

            # ROOMS
            if category in ("room", "rooms"):
                rooms = cfg.get("rooms", [])
                target = next((r for r in rooms if r.lower() == identifier.lower()), None)
                if not target:
                    return self._err(f"Room '{identifier}' not found.", category, "edit")

                new_name = updates.get("name")
                if not new_name:
                    # Look for patterns like "to Roddy 894" or "be called Roddy 894"
                    m = re.search(r"(?:to|called|named|be called)\s+([A-Z][A-Za-z]+\s*\d+)", self.last_user_input,
                                  re.IGNORECASE)
                    if m:
                        new_name = m.group(1).strip()

                if not new_name:
                    return self._err("Provide 'name' to rename the room.", category, "edit")

                DM.editRoom(target, new_name)
                return self._ok(f"Room '{target}' renamed to '{new_name}' (not yet saved).", category, "edit")

            # LABS
            if category in ("lab", "labs"):
                labs = cfg.get("labs", [])
                target = next((l for l in labs if l.lower() == identifier.lower()), None)
                if not target:
                    return self._err(f"Lab '{identifier}' not found.", category, "edit")

                new_name = updates.get("name")
                if not new_name:
                    # Handles: "to be called Windows", "to Windows", "called Windows", "rename lab Mac to Windows"
                    m = re.search(
                        r"\b(?:to\s+(?:be\s+called|called|named)|as|rename\s+(?:to|as)?|be\s+called)\s+([A-Z][A-Za-z0-9]+(?:\s+[A-Za-z0-9]+)*)",
                        self.last_user_input,
                        re.IGNORECASE,
                    )
                    if m:
                        new_name = m.group(1).strip()

                if not new_name:
                    return self._err("Provide 'name' to rename the lab.", category, "edit")

                try:
                    DM.editLabs(target, new_name)
                    return self._ok(f"Lab '{target}' renamed to '{new_name}' (not yet saved).", category, "edit")
                except Exception as e:
                    return self._err(f"Failed to rename lab '{target}': {e}", category, "edit")
            # COURSES
            if category in ("course", "courses"):
                # Build updates from text if not provided
                text = self.last_user_input
                payload = dict(updates or {})
                # credits
                if "credits" not in payload:
                    m = re.search(r"(\d+)\s*credits?", text, re.IGNORECASE)
                    if m:
                        payload["credits"] = int(m.group(1))

                # rooms / labs / faculty / conflicts — full replacements if provided in updates
                known_rooms = cfg.get("rooms", [])
                known_labs = cfg.get("labs", [])
                known_faculty = [f.get("name") for f in cfg.get("faculty", []) if isinstance(f, dict)]

                if "room" not in payload:
                    rooms = self._extract_rooms_from_text(text, known_rooms)
                    rooms = [r for r in rooms if
                             not re.match(r"^[A-Z]{2,}\s*\d+$", r)]
                    if rooms:
                        payload["room"] = rooms
                if "lab" not in payload:
                    labs = self._extract_labs_from_text(text, known_labs)
                    if labs:
                        payload["lab"] = labs
                if "faculty" not in payload:
                    fac = [n for n in self._extract_faculty_names_from_text(text) if n in known_faculty]
                    if fac:
                        payload["faculty"] = fac
                if "conflicts" not in payload:
                    conf = [
                        c for c in self._extract_conflicts_from_text(text, known_rooms, known_labs)
                        if c.upper() != identifier.upper()
                    ]
                    if conf:
                        payload["conflicts"] = conf

                try:
                    DM.editCourse(identifier, payload, target_index=updates.get("_index"))
                    return self._ok(f"Course '{identifier}' updated in memory.", "course", "edit", payload=payload)
                except Exception as e:
                    return self._err(f"Failed to edit course '{identifier}': {e}", "course", "edit")

            # FACULTY
            if category in ("faculty", "professor", "instructor", "teacher"):
                text = self.last_user_input
                fac = DM.getFacultyByName(identifier)
                if not fac:
                    return self._err(f"Faculty '{identifier}' not found.", "faculty", "edit")

                # Start with a copy of existing faculty data
                new_fac = fac.copy()

                # ✅ Reuse add logic for consistency
                # Parse numeric credit limits
                min_c, max_c, uniq = self._extract_min_max_uniq(text)
                if min_c is not None:
                    new_fac["minimum_credits"] = min_c
                if max_c is not None:
                    new_fac["maximum_credits"] = max_c
                if uniq is not None:
                    new_fac["unique_course_limit"] = uniq

                # ✅ Reuse time parser
                parsed_times = self._parse_times_from_text(text)
                if not parsed_times:
                    # Fallback to "monday from 9am to 5pm" style
                    for m in re.finditer(
                            r"(monday|tuesday|wednesday|thursday|friday|mon|tue|wed|thu|fri)\s*(?:from)?\s*([0-9:apm\s]+)\s*(?:to|-)\s*([0-9:apm\s]+)",
                            text, flags=re.IGNORECASE):
                        day, start, end = m.groups()
                        start_24 = self._convert_to_24h(start)
                        end_24 = self._convert_to_24h(end)
                        parsed_times.setdefault(day[:3].upper(), []).append(f"{start_24}-{end_24}")

                if parsed_times:
                    all_days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
                    new_fac["times"] = {d: parsed_times.get(d, []) for d in all_days}

                # ✅ Reuse preference parsing (identical to add)
                cfg = DM.data.get("config", {})
                known_rooms = [r.lower() for r in cfg.get("rooms", [])]

                # Course preferences
                cp = {}
                for m in re.finditer(
                        r"\b([A-Z]{2,}\s*\d{1,4}[A-Za-z]?)\b\s*(?:weight|with a weight of|=)\s*(\d+)",
                        text, re.IGNORECASE,
                ):
                    course = m.group(1).strip()
                    if not any(course.lower() == r for r in known_rooms):
                        cp[course.upper().replace("  ", " ")] = int(m.group(2))

                # Room preferences
                rp = {}
                for m in re.finditer(
                        r"\b([A-Z][A-Za-z]+\s*\d+)\b\s*(?:weight|with a weight of|=)\s*(\d+)",
                        text, re.IGNORECASE,
                ):
                    rp[m.group(1)] = int(m.group(2))

                # Lab preferences — reuse working add parser
                lp = self._parse_lab_prefs(text)

                # Apply parsed prefs if any
                if cp:
                    new_fac["course_preferences"] = cp
                if rp:
                    new_fac["room_preferences"] = rp
                if lp:
                    new_fac["lab_preferences"] = lp

                print("[DEBUG] Faculty edit payload:\n", json.dumps(new_fac, indent=2))

                # Commit to DM
                fac_list = DM.data["config"]["faculty"]
                for i, fobj in enumerate(fac_list):
                    if isinstance(fobj, dict) and fobj.get("name", "").lower() == identifier.lower():
                        fac_list[i] = new_fac
                        break

                return self._ok(
                    f"Faculty '{identifier}' updated in memory.",
                    "faculty",
                    "edit",
                    payload=new_fac
                )

            return self._err(f"Unknown category '{category}'.", category, "edit")
        except Exception as e:
            traceback.print_exc()
            return self._err(f"Error editing {category}: {e}", category, "edit")

    def _tool_delete_item(self, category: str, identifier: str):
        try:
            if not hasattr(DM, "data") or not DM.data:
                return self._err("No configuration loaded. Import a config first.", category, "delete")

            category = category.lower().strip()

            if category in ("room", "rooms"):
                try:
                    DM.removeRoom(identifier)
                    return self._ok(f"Room '{identifier}' removed (not yet saved).", category, "delete")
                except Exception as e:
                    return self._err(f"Failed to remove room '{identifier}': {e}", category, "delete")

            if category in ("lab", "labs"):
                try:
                    labs = DM.data["config"].get("labs", [])
                    target = next((l for l in labs if l.lower() == identifier.lower()), None)
                    if not target:
                        return self._err(f"Lab '{identifier}' not found.", category, "delete")

                    labs.remove(target)
                    return self._ok(f"Lab '{target}' removed (not yet saved).", category, "delete")
                except Exception as e:
                    return self._err(f"Failed to remove lab '{identifier}': {e}", category, "delete")

            if category in ("course", "courses"):
                try:
                    DM.removeCourse(identifier)
                    return self._ok(f"Course '{identifier}' removed (not yet saved).", category, "delete")
                except Exception as e:
                    return self._err(f"Failed to remove course '{identifier}': {e}", category, "delete")

            if category in ("faculty", "professor", "instructor", "teacher"):
                try:
                    # DataManager expects exact name
                    fac = DM.getFacultyByName(identifier)
                    if not fac:
                        return self._err(f"Faculty '{identifier}' not found.", "faculty", "delete")
                    # Remove by exact name
                    # Reuse removeFaculty API which checks dependencies
                    from Controller.main_controller import DataManager as _DMType  # type hint only
                    DM.removeFaculty(identifier)
                    return self._ok(f"Faculty '{identifier}' removed (not yet saved).", "faculty", "delete")
                except Exception as e:
                    return self._err(f"Failed to remove faculty '{identifier}': {e}", "faculty", "delete")

            return self._err(f"Unknown category '{category}'.", category, "delete")
        except Exception as e:
            traceback.print_exc()
            return self._err(f"Error deleting {category}: {e}", category, "delete")

    # -------------------------
    # Tool registration
    # -------------------------

    def _create_tools(self) -> List[StructuredTool]:
        return [
            StructuredTool.from_function(
                name="view_config",
                func=self._tool_view_config,
                description="Summarize current config (rooms, labs, courses, faculty).",
                args_schema=NoArgs,
                return_direct=True,
            ),
            StructuredTool.from_function(
                name="update_config_value",
                func=self._tool_update_config_value,
                description="Update a value via dot/bracket path into DM.data.",
                args_schema=KeyPathArgs,
                return_direct=True,
            ),
            StructuredTool.from_function(
                name="show_details",
                func=self._tool_show_details,
                description="Show details for rooms/labs/courses/faculty.",
                return_direct=True,
            ),
            StructuredTool.from_function(
                name="add_item",
                func=self._tool_add_item,
                description="Add a room | lab | course | faculty.",
                args_schema=AddItemArgs,
                return_direct=True,
            ),
            StructuredTool.from_function(
                name="edit_item",
                func=self._tool_edit_item,
                description="Edit a room | lab | course | faculty (full replace semantics for prefs/availability).",
                args_schema=EditItemArgs,
                return_direct=True,
            ),
            StructuredTool.from_function(
                name="delete_item",
                func=self._tool_delete_item,
                description="Delete a room | lab | course | faculty.",
                args_schema=DeleteItemArgs,
                return_direct=True,
            ),
        ]

    # -------------------------
    # Intent routing
    # -------------------------

    @staticmethod
    def _detect_category(text: str) -> Optional[str]:
        """
        Robustly detect whether the user is referring to a course, faculty, room, or lab.
        Priority order:
          1. Explicit phrasing ("add faculty", "edit room", etc.)
          2. Faculty creation/edit (when describing a person or teaching load)
          3. Course edits (when referring to course IDs or teaching assignments)
          4. Room / Lab changes
        """

        t = text.lower().strip()

        # --- Explicit phrasing wins outright ---
        if re.search(r"\b(add|edit|update|delete|remove|create)\s+faculty\b", t):
            return "faculty"
        if re.search(r"\b(add|edit|update|delete|remove|create)\s+(room|rooms)\b", t):
            return "room"
        if re.search(r"\b(add|edit|update|delete|remove|create)\s+(lab|labs)\b", t):
            return "lab"
        if re.search(r"\b(add|edit|update|delete|remove|create)\s+(course|class|courses)\b", t):
            return "course"

        # --- Faculty-style intent ---
        # Look for words that usually appear in faculty creation/update statements
        if re.search(r"\b(min|max)\s*credits?\b", t) or re.search(r"\b(unique\s*course\s*limit)\b", t):
            return "faculty"
        if re.search(r"\b(course|room|lab)\s+preference\b", t):
            return "faculty"
        if re.search(r"\b(available|availability|teaches|schedule|office\s*hours?)\b", t):
            return "faculty"
        if re.search(r"\b(faculty|professor|instructor|teacher)\b", t):
            return "faculty"

        # --- Course context ---
        # Detect explicit course identifiers or credits tied to courses
        if re.search(r"\b(cmsc|bio|math|edu|phys|course|class)\b", t):
            return "course"

        # --- Room / Lab cues ---
        if re.search(r"\b(room|roddy|hall|building)\b", t):
            return "room"
        if re.search(r"\blab\b", t):
            return "lab"

        return None

    @staticmethod
    def _detect_action(text: str) -> Optional[str]:
        t = text.lower()
        if any(w in t for w in ("add", "create", "new")):
            return "add"
        if any(w in t for w in ("edit", "update", "change", "modify", "set")):
            return "edit"
        if any(w in t for w in ("delete", "remove", "drop")):
            return "delete"
        if any(w in t for w in ("show", "list", "display")):
            return "show"
        return None

    @staticmethod
    def _extract_identifier(text: str, category: str) -> Optional[str]:
        text = text.strip()

        if category == "course":
            return ChatbotAgent._find_first_course_id(text)

        if category == "faculty":
            names = ChatbotAgent._extract_faculty_names_from_text(text)
            return names[0] if names else None

        if category == "room":
            m = re.search(r"(?:room\s+)?([A-Z][A-Za-z]+\s*\d+)", text, re.IGNORECASE)
            return m.group(1).strip() if m else None

        if category == "lab":
            # --- Handle both "delete lab Mac" and "delete Mac lab" cleanly ---
            # 1. "delete lab Mac" / "edit lab Mac to Windows"
            m1 = re.search(r"\blab\s+([A-Z][A-Za-z0-9]+(?:\s+[A-Za-z0-9]+)*)", text, re.IGNORECASE)
            # 2. "delete Mac lab" / "remove Windows lab"
            m2 = re.search(r"\b([A-Z][A-Za-z0-9]+(?:\s+[A-Za-z0-9]+)*)\s+lab\b", text, re.IGNORECASE)

            # Prefer the one that is NOT the command word itself (like “delete”)
            for m in [m1, m2]:
                if m:
                    name = m.group(1).strip()
                    if name.lower() not in ("delete", "remove", "edit", "update", "add", "lab"):
                        return name
            return None

        return None

    # -------------------------
    # Public query entrypoint
    # -------------------------

    def query(self, user_input: str):
        """
        Returns either a string (on hard error) or a dict:
        {
          "response": "...",
          "category": "course|room|lab|faculty",
          "action": "add|edit|delete|show",
          "switch_tab": "Courses|Rooms|Labs|Faculty",
          "payload": {...}
        }
        """
        if self.disabled:
            return "Chatbot is disabled (no API key)."

        try:
            self.last_user_input = user_input or ""
            action = self._detect_action(self.last_user_input) or "add"  # default to add if vague
            category = self._detect_category(self.last_user_input) or "course"

            # SHOW
            if action == "show":
                res = self._tool_show_details(category)
                return self._ok("Showing details.", category, "show", payload=res if isinstance(res, dict) else None)

            # DELETE
            if action == "delete":
                ident = self._extract_identifier(self.last_user_input, category)
                if not ident:
                    return self._err(f"Please specify which {category} to delete.", category, "delete")
                return self._tool_delete_item(category, ident)

            # EDIT
            if action == "edit":
                ident = self._extract_identifier(self.last_user_input, category)
                if not ident:
                    return self._err(f"Please specify which {category} to edit.", category, "edit")
                # No pre-baked updates: parser inside _tool_edit_item builds replacements as needed
                return self._tool_edit_item(category, ident, updates={})

            # ADD (default)
            if action == "add":
                return self._tool_add_item(category, data={})

            # Fallback
            return self._err("I couldn't determine your intent. Try 'add course BIO 345'.", category, "unknown")

        except Exception as e:
            traceback.print_exc()
            return {"response": f"Error: {e}"}