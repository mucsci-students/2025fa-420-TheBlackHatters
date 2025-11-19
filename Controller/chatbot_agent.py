# ChatbotAgent.py
# Author: Fletcher Burton

import os
import json
import traceback
from typing import List, Dict, Optional, Union
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.tools import StructuredTool

import Controller.main_controller as ctrl

DM = ctrl.DM

load_dotenv()


# Pydantic Schemas
class AddItemArgs(BaseModel):
    category: str = Field(description="room | lab | course | faculty")
    data: dict = Field(default_factory=dict)


class EditItemArgs(BaseModel):
    category: str = Field(description="room | lab | course | faculty")
    identifier: str = Field(description="Unique ID or name to edit.")
    updates: dict = Field(default_factory=dict)


class DeleteItemArgs(BaseModel):
    category: str = Field(description="room | lab | course | faculty")
    identifier: str = Field(description="Unique ID or name to delete.")


class NoArgs(BaseModel):
    pass


# Intent Classification Schema
# --- Insert CourseDetails schema here ---


class CourseDetails(BaseModel):
    course_id: str
    credits: int
    room: List[str] = []
    lab: List[str] = []
    conflicts: List[str] = []
    faculty: List[str] = []


# Inserted FacultyDetails schema
class FacultyDetails(BaseModel):
    name: str
    minimum_credits: int
    maximum_credits: int
    unique_course_limit: int
    times: Dict[str, List[str]] = {}
    course_preferences: Dict[str, int] = {}
    room_preferences: Dict[str, int] = {}
    lab_preferences: Dict[str, int] = {}


class Intent(BaseModel):
    intent: str = Field(description="add | edit | delete | show")
    category: str = Field(description="course | faculty | room | lab")
    identifier: Optional[str] = Field(default=None)
    details: Optional[Union[CourseDetails, FacultyDetails, dict]] = Field(default=None)


class UnifiedRouter:
    """
    Uses GPT-5-mini to decide whether the message is conversational or actionable.
    If conversational -> return text
    If actionable -> return structured JSON intent
    """

    def __init__(self):
        self.llm = ChatOpenAI(model_name="gpt-5-mini", temperature=0)
        self.intent_parser = PydanticOutputParser(pydantic_object=Intent)

        self.system_prompt = """
        You are a scheduling assistant for managing rooms, labs, courses, and faculty.

        When the user issues a request that starts with or clearly implies viewing data, such as:
            - "view faculty"
            - "show faculty"
            - "list faculty"
            - "display faculty"
            - "see faculty"
            - "view courses"
            - "show courses"
            - "list courses"
            - "display courses"
            - "see courses"
            - "view rooms"
            - "show rooms"
            - "list rooms"
            - "display rooms"
            - "see rooms"
            - "view labs"
            - "show labs"
            - "list labs"
            - "display labs"
            - "see labs"

        you MUST return a JSON intent with:
            intent: "show"
            category: one of "faculty", "course", "room", or "lab" matching what the user asked to view
            identifier: null
            details: {}

        This rule MUST override any other reasoning. Do NOT treat these as add/edit/delete commands and do NOT ask follow-up questions; simply return the structured JSON intent.

        Decide what the user wants:
        - If the user is asking a general or conversational question (like greetings, help, explanation),
          respond naturally in text (not JSON).
        - If the user wants to perform an action (add/edit/delete/show something),
          return JSON describing the intent with these fields:
            intent: add | edit | delete | show
            category: course | faculty | room | lab
            identifier: optional name/id
            details: dictionary with other info
        For COURSES, you MUST always output the field "course_id" inside the "details" object. Do NOT use "name" or "title" for courses.

        For COURSES, the "details" object MUST match this exact structure:

        {
          "course_id": "(Course type name, ex: CMSC, BIO) ###",
          "credits": <integer>,
          "room": [ "RoomName1", "RoomName2", ... ],
          "lab": [ "LabName1", "LabName2", ... ],
          "conflicts": [ "(Course type name, ex: CMSC, BIO) ###", ... ],
          "faculty": [ "FacultyName1", ... ]
        }

        Rules:
        - Lists MUST contain ONLY item names, with no added explanation text.
        - Do NOT include sentences, phrases, or descriptive language inside lists.
        - Do NOT include any extra fields.
        - Do NOT rename any field; use these exact keys.

        For FACULTY, the "details" object MUST match this exact structure:

        {
          "name": "Faculty Name",
          "minimum_credits": <integer>,
          "maximum_credits": <integer>,
          "unique_course_limit": <integer>,
          "times": {
            "MON": ["HH:MM-HH:MM", ...],
            "TUE": ["HH:MM-HH:MM", ...],
            "WED": ["HH:MM-HH:MM", ...],
            "THU": ["HH:MM-HH:MM", ...],
            "FRI": ["HH:MM-HH:MM", ...]
          },
          "course_preferences": { "CMSC ###": <int>, ... },
          "room_preferences": { "RoomName": <int>, ... },
          "lab_preferences": { "LabName": <int>, ... }
        }

        Rules:
        - Times must be lists of time ranges only, no descriptive text.
        - Preference maps must only contain key → integer.
        - No SAT or SUN keys.
        - No extra fields allowed.
        - No explanations, sentences, or descriptive language in values.

        The model MUST produce clean JSON that fits these schemas exactly when returning an action intent.

        Respond with **either**:
          1. Natural language answer (plain text)
          2. JSON matching {format_instructions}
          
        When the user says:
            - "view faculty"
            - "show faculty"
            - "list faculty"
            - "display faculty"
            - "see faculty"

            You MUST output the following intent JSON:

            {
            "intent": "show",
            "category": "faculty",
            "identifier": null,
            "details": {}
            }
            
        For ROOMS, the "details" object MUST match this exact structure:

        {
          "name": "RoomName"
        }

        For LABS, the "details" object MUST match this exact structure:

        {
          "name": "LabName"
        }

        Rules:
        - For rooms and labs, "name" must be the human-readable identifier (e.g., "Roddy 123", "Mac").
        - Do NOT add any extra fields besides "name".
        """

    def route(self, text: str):
        """
        Ask GPT-5-mini to decide response type.
        Returns either a string (conversation) or an Intent object.
        """
        full_prompt = f"""{self.system_prompt}

    User message: {text}

    Respond with either:
    1. Plain text (if conversational)
    2. JSON matching this schema:
    {self.intent_parser.get_format_instructions()}
    """
        raw = self.llm.invoke(full_prompt).content
        result = str(raw).strip() if raw is not None else ""

        # Try to parse JSON → Intent
        try:
            return self.intent_parser.parse(result)
        except Exception:
            # Not JSON → treat as conversational response
            return result


# Chatbot Agent


class ChatbotAgent:
    """
    AI-driven CRUD controller for scheduler configuration.
    Delegates intent recognition to OpenAI (IntentClassifier).
    """

    def __init__(self, config_path_getter):
        self.get_config_path = config_path_getter

        from Controller import main_controller

        if hasattr(main_controller, "DM") and os.path.exists(self.get_config_path()):
            try:
                with open(self.get_config_path(), "r") as f:
                    main_controller.DM.data = json.load(f)
                main_controller.DM.filePath = self.get_config_path()
            except Exception as e:
                print(f"[ChatbotAgent] Warning: could not reload config: {e}")

        self.disabled = False
        if not os.getenv("OPENAI_API_KEY"):
            print("[ERROR] Missing OPENAI_API_KEY. Chatbot disabled.")
            self.model = None
            self.agent_executor = None
            self.disabled = True
            return

        self.router = UnifiedRouter()
        self.tools = self._create_tools()
        self.model = ChatOpenAI(model_name="gpt-5-mini", temperature=0)
        self.last_user_input = ""

    # UI helper
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
    def _ok(
        response: str, category: str, action: str, payload: Optional[dict] = None
    ) -> dict:
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

    # --- Helpers to normalize faculty payloads from messy LLM output / free text ---

    @staticmethod
    def _to_int(value, default=None):
        if value is None:
            return default
        if isinstance(value, (int, float)):
            return int(value)
        s = str(value).strip()
        # pick the first integer in the string
        import re

        m = re.search(r"-?\d+", s)
        return int(m.group(0)) if m else default

    @staticmethod
    def _to_pref_dict(obj):
        """
        Accepts:
          - {"A": 2, "B": 3}
          - [{"name": "A", "weight": 2}, {"name": "B", "weight": 3}]
          - [("A", 2), ("B", 3)]
          - ["A:2", "B:3"]
        Returns a clean dict[str,int].
        """
        if not obj:
            return {}
        if isinstance(obj, dict):
            # Coerce values to int
            return {str(k): ChatbotAgent._to_int(v, 0) for k, v in obj.items()}
        out = {}
        if isinstance(obj, list):
            for item in obj:
                if isinstance(item, dict):
                    name = (
                        item.get("name")
                        or item.get("id")
                        or item.get("course")
                        or item.get("room")
                        or item.get("lab")
                    )
                    weight = ChatbotAgent._to_int(item.get("weight"), 0)
                    if name:
                        out[str(name)] = weight
                elif isinstance(item, (list, tuple)) and len(item) >= 2:
                    out[str(item[0])] = ChatbotAgent._to_int(item[1], 0)
                else:
                    # "CMSC 124 weight 4" or "Roddy 2:3"
                    s = str(item)
                    import re

                    m = re.search(
                        r"([A-Za-z0-9#\-\s]+?)\s*(?:weight|:)\s*(\d+)", s, re.I
                    )
                    if m:
                        out[m.group(1).strip()] = int(m.group(2))
        return out

    @staticmethod
    def _parse_time_span(span: str):
        """
        '7am to 5pm' -> '07:00-17:00'
        '08:30-12:00' passthrough
        """
        if not span:
            return None
        s = (
            span.strip()
            .lower()
            .replace("–", "-")
            .replace("—", "-")
            .replace(" to ", "-")
        )
        import re

        # If already HH:MM-HH:MM
        if re.match(r"^\d{1,2}:\d{2}-\d{1,2}:\d{2}$", s):
            return s

        # Accept '7am-5pm', '7 am - 5 pm', '8-4pm' etc.
        def hm(tok):
            m = re.match(r"^\s*(\d{1,2})(?::(\d{2}))?\s*(am|pm)?\s*$", tok)
            if not m:
                return None
            h = int(m.group(1))
            mi = int(m.group(2) or 0)
            ampm = (m.group(3) or "").lower()
            if ampm == "pm" and h != 12:
                h += 12
            if ampm == "am" and h == 12:
                h = 0
            return f"{h:02d}:{mi:02d}"

        parts = [p for p in re.split(r"\s*-\s*", s) if p]
        if len(parts) != 2:
            return None
        a, b = hm(parts[0]), hm(parts[1])
        return f"{a}-{b}" if a and b else None

    @staticmethod
    def _weekday_key(name: str):
        name = (name or "").strip().lower()
        mapping = {
            "monday": "MON",
            "mon": "MON",
            "tuesday": "TUE",
            "tue": "TUE",
            "tues": "TUE",
            "wednesday": "WED",
            "wed": "WED",
            "thursday": "THU",
            "thu": "THU",
            "thur": "THU",
            "thurs": "THU",
            "friday": "FRI",
            "fri": "FRI",
            "saturday": "SAT",
            "sat": "SAT",
            "sunday": "SUN",
            "sun": "SUN",
        }
        return mapping.get(name)

    def _extract_times_from_text(self, text: str):
        """
        Pull day→time from raw user input like:
        'available on Monday from 7am to 5pm, tuesday from 4pm to 6pm, friday 8am to 4pm'
        """
        import re

        times = {}
        # Patterns: "<day> from X to Y" OR "<day> X to Y"
        day_re = r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday|mon|tue|tues|wed|thu|thur|thurs|fri|sat|sun)"
        span_re = (
            r"(?:(?:from\s+)?([0-9:\sampAMP\.]+?)\s*(?:to|-)\s*([0-9:\sampAMP\.]+))"
        )
        for m in re.finditer(day_re + r"\s+" + span_re, text, re.I):
            day = self._weekday_key(m.group(1))
            start, end = m.group(2), m.group(3)
            span = self._parse_time_span(f"{start}-{end}")
            if day and span:
                times.setdefault(day, []).append(span)

        # Also handle a looser comma series like "monday 7am-5pm, tuesday 4pm-6pm"
        for m in re.finditer(
            day_re + r"\s+([0-9:\sampAMP\.]+-[0-9:\sampAMP\.]+)", text, re.I
        ):
            day = self._weekday_key(m.group(1))
            span = self._parse_time_span(m.group(2))
            if day and span:
                times.setdefault(day, []).append(span)

        return times

    def _normalize_faculty_payload(self, data: dict, raw_text: str) -> dict:
        """
        Returns a new dict that satisfies DM.addFaculty’s schema.
        Pulls missing fields out of raw_text if needed.
        """
        norm = {}

        # --- name ---
        name = (data or {}).get("name")
        if not name:
            import re

            m = re.search(r"(?:named|called)\s+([A-Z][A-Za-z0-9_\-\s]*)", raw_text)
            if m:
                name = m.group(1).strip()
        if not name:
            raise ValueError("Faculty must include a valid 'name' field.")
        norm["name"] = name

        # --- numeric fields ---
        norm["minimum_credits"] = self._to_int(
            data.get("minimum_credits") or data.get("min_credits"), 0
        )
        norm["maximum_credits"] = self._to_int(
            data.get("maximum_credits") or data.get("max_credits"), 0
        )
        norm["unique_course_limit"] = self._to_int(
            data.get("unique_course_limit")
            or data.get("unique_limit")
            or data.get("unique_courses"),
            0,
        )

        # Try to extract numbers from the raw text if still 0
        import re

        if not norm["minimum_credits"]:
            m = re.search(
                r"min(?:imum)?\s*credits?\s*(?:is|=)?\s*(\d+)", raw_text, re.I
            )
            if m:
                norm["minimum_credits"] = int(m.group(1))
        if not norm["maximum_credits"]:
            m = re.search(
                r"max(?:imum)?\s*credits?\s*(?:is|=)?\s*(\d+)", raw_text, re.I
            )
            if m:
                norm["maximum_credits"] = int(m.group(1))
        if not norm["unique_course_limit"]:
            m = re.search(
                r"unique\s*course\s*limit\s*(?:of|is|=)?\s*(\d+)", raw_text, re.I
            )
            if m:
                norm["unique_course_limit"] = int(m.group(1))

        # --- availability ("times") ---
        # Use ONLY structured times from the LLM. Do NOT infer from raw text.
        clean_times = {}
        times = data.get("times") or {}

        if isinstance(times, dict):
            for k, spans in times.items():
                day = self._weekday_key(k)
                if not day:
                    continue
                if isinstance(spans, list):
                    clean_times[day] = [
                        self._parse_time_span(s)
                        for s in spans
                        if self._parse_time_span(s)
                    ]
                else:
                    parsed = self._parse_time_span(str(spans))
                    if parsed:
                        clean_times.setdefault(day, []).append(parsed)

        # Ensure all weekdays exist
        for d in ["MON", "TUE", "WED", "THU", "FRI"]:
            clean_times.setdefault(d, [])

        norm["times"] = clean_times

        # --- preferences ---
        # Use ONLY the structured values from the LLM. Do NOT infer from raw text.
        course_pref_input = data.get("course_preferences") or {}
        room_pref_input = data.get("room_preferences") or {}
        lab_pref_input = data.get("lab_preferences") or {}

        norm["course_preferences"] = self._to_pref_dict(course_pref_input)
        norm["room_preferences"] = self._to_pref_dict(room_pref_input)
        norm["lab_preferences"] = self._to_pref_dict(lab_pref_input)

        # Persist all required faculty fields even if empty
        ALLOWED_FIELDS = [
            "name",
            "minimum_credits",
            "maximum_credits",
            "unique_course_limit",
            "times",
            "course_preferences",
            "room_preferences",
            "lab_preferences",
        ]

        for k in ALLOWED_FIELDS:
            if k not in norm:
                if k == "times":
                    norm[k] = {"MON": [], "TUE": [], "WED": [], "THU": [], "FRI": []}
                elif k.endswith("_preferences"):
                    norm[k] = {}
                elif k in ("minimum_credits", "maximum_credits", "unique_course_limit"):
                    norm[k] = 0
                else:
                    norm[k] = ""

        # Ensure times includes all weekdays
        for d in ["MON", "TUE", "WED", "THU", "FRI"]:
            norm["times"].setdefault(d, [])

        return norm

    def _normalize_course_payload(self, data: dict, raw_text: str) -> dict:
        """
        Normalize and sanitize a course payload without guessing intent.
        OpenAI must provide the structure — this only ensures correct schema shape.
        Required course schema:

        {
            "course_id": str,
            "credits": int,
            "room": list[str],
            "lab": list[str],
            "conflicts": list[str],
            "faculty": list[str]
        }
        """
        clean = dict(data or {})

        # --- Enforce required fields ---------------------------------------------

        REQUIRED_LIST_FIELDS = ["room", "lab", "conflicts", "faculty"]

        # course_id ---------------------------------------------------------------
        course_id = clean.get("course_id") or clean.get("name") or clean.get("title")
        if not course_id:
            raise ValueError(
                "Missing required field: 'course_id'. The LLM must supply this."
            )
        clean["course_id"] = str(course_id).strip()

        # credits ---------------------------------------------------------------
        credits = (
            clean.get("credits") or clean.get("credit_hours") or clean.get("hours")
        )
        try:
            clean["credits"] = int(credits)
        except Exception:
            raise ValueError(
                "Missing or invalid 'credits'. The LLM must provide an integer."
            )

        # list fields ------------------------------------------------------------
        for field in REQUIRED_LIST_FIELDS:
            val = clean.get(field)

            if val is None:
                clean[field] = []
            elif isinstance(val, list):
                clean[field] = [str(x).strip() for x in val]
            else:
                clean[field] = [str(val).strip()]

        # Ensure persistence of all required fields, even if empty
        required_fields = ["room", "lab", "conflicts", "faculty"]
        for f in required_fields:
            if f not in clean or clean[f] is None:
                clean[f] = []
        # Ensure credits exists
        if "credits" not in clean:
            clean["credits"] = 0

        return clean

    # -------------------------
    # Tool: view / update value
    # -------------------------

    def _tool_view_config(self):
        if not hasattr(DM, "data") or not DM.data:
            return "No configuration loaded."
        cfg = (DM.data or {}).get("config", {})
        rooms = len(cfg.get("rooms", []))
        labs = len(cfg.get("labs", []))
        courses = len(cfg.get("courses", []))
        faculty = len(cfg.get("faculty", []))
        return f"Config summary: {rooms} rooms, {labs} labs, {courses} courses, {faculty} faculty."

    def _tool_show_details(self, target: str = ""):
        try:
            data = DM.data or {}
            cfg = data.get("config", {})
            t = (target or "").lower()
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

    def _tool_update_config_value(self, key_path: str, new_value: str):
        try:
            if not hasattr(DM, "data") or not DM.data:
                return "No configuration loaded. Import a config first."

            ref = DM.data
            keys = key_path.split(".")
            for k in keys[:-1]:
                ref = ref[k]
            ref[keys[-1]] = json.loads(new_value)
            DM.saveData(self.get_config_path())
            return f"Updated {key_path}."
        except Exception as e:
            return f"Error updating {key_path}: {e}"

    # -----------------------------
    # CRUD tool wrappers
    # -----------------------------

    def _tool_add_item(self, category: str, data: dict):
        try:
            if category == "room":
                DM.addRoom(data.get("name", "Unnamed Room"))
                return self._ok("Room added.", category, "add")

            if category == "lab":
                DM.addLab(data.get("name", "Unnamed Lab"))
                return self._ok("Lab added.", category, "add")

            if category == "faculty":
                # Convert FacultyDetails → dict
                if isinstance(data, FacultyDetails):
                    data = data.dict()

                clean = self._normalize_faculty_payload(data, self.last_user_input)

                DM.addFaculty(clean)
                return self._ok(f"Faculty '{clean['name']}' added.", category, "add")

            if category == "course":
                clean = self._normalize_course_payload(data, self.last_user_input)
                DM.addCourse(clean)
                return self._ok(
                    f"Course '{clean['course_id']}' added.", category, "add"
                )

            return self._err(f"Unknown category '{category}'.", category, "add")

        except Exception as e:
            traceback.print_exc()
            return self._err(f"Error adding {category}: {e}", category, "add")

    def _tool_edit_item(self, category: str, identifier: str, updates: dict):
        try:
            if category == "room":
                DM.editRoom(identifier, updates.get("name", identifier))
                return self._ok(f"Room '{identifier}' updated.", category, "edit")

            if category == "lab":
                DM.editLabs(identifier, updates.get("name", identifier))
                return self._ok(f"Lab '{identifier}' updated.", category, "edit")

            if category == "faculty":
                # Convert FacultyDetails → dict
                if isinstance(updates, FacultyDetails):
                    updates = updates.dict()

                clean_updates = self._normalize_faculty_payload(
                    updates, self.last_user_input
                )

                # Remove name field if it’s just the same identifier
                if clean_updates.get("name", "").lower() == identifier.lower():
                    clean_updates.pop("name", None)

                DM.editFaculty(identifier, clean_updates)
                return self._ok(f"Faculty '{identifier}' updated.", category, "edit")

            if category == "course":
                DM.editCourse(identifier, updates)
                return self._ok(f"Course '{identifier}' updated.", category, "edit")

            return self._err(f"Unknown category '{category}'.", category, "edit")

        except Exception as e:
            traceback.print_exc()
            return self._err(f"Error editing {category}: {e}", category, "edit")

    def _tool_delete_item(self, category: str, identifier: str):
        try:
            if category == "room":
                DM.removeRoom(identifier)
                return self._ok(f"Room '{identifier}' deleted.", category, "delete")
            if category == "lab":
                DM.removeLabs(identifier)
                return self._ok(f"Lab '{identifier}' deleted.", category, "delete")
            if category == "faculty":
                DM.removeFaculty(identifier)
                return self._ok(f"Faculty '{identifier}' deleted.", category, "delete")
            if category == "course":
                DM.removeCourse(identifier)
                return self._ok(f"Course '{identifier}' deleted.", category, "delete")
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
                name="show_details",
                func=self._tool_show_details,
                description="Show detailed list for given category.",
                return_direct=True,
            ),
            StructuredTool.from_function(
                name="add_item",
                func=self._tool_add_item,
                description="Add a new item (room, lab, course, or faculty).",
                args_schema=AddItemArgs,
                return_direct=True,
            ),
            StructuredTool.from_function(
                name="edit_item",
                func=self._tool_edit_item,
                description="Edit an existing item.",
                args_schema=EditItemArgs,
                return_direct=True,
            ),
            StructuredTool.from_function(
                name="delete_item",
                func=self._tool_delete_item,
                description="Delete an existing item.",
                args_schema=DeleteItemArgs,
                return_direct=True,
            ),
        ]

    # -----------------------------
    # Main Query Entrypoint
    # -----------------------------

    def query(self, user_input: str):
        if self.disabled:
            return "Chatbot is disabled (no API key)."

        self.last_user_input = user_input or ""
        try:
            routed = self.router.route(self.last_user_input)

            # Conversational response
            if isinstance(routed, str):
                return {
                    "response": routed,
                    "category": "general",
                    "action": "chat",
                    "switch_tab": "Faculty",
                }

            # Action intent -> run CRUD logic
            intent = routed.intent
            category = routed.category
            identifier = routed.identifier
            details = routed.details or {}

            if intent == "show":
                res = self._tool_show_details(category)
                return self._ok("Showing details.", category, "show", payload=res)
            if intent == "add":
                return self._tool_add_item(category, details)
            if intent == "edit":
                if not identifier:
                    return self._err("Missing identifier for edit.", category, "edit")
                return self._tool_edit_item(category, identifier, updates=details)
            if intent == "delete":
                if not identifier:
                    return self._err(
                        "Missing identifier for delete.", category, "delete"
                    )
                return self._tool_delete_item(category, identifier)

            return self._err("Unknown intent.", category, intent)

        except Exception as e:
            traceback.print_exc()
            return {"response": f"Error processing input: {e}"}
