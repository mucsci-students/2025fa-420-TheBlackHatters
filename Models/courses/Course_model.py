# File Name: Course_model.py
# Author: Fletcher Burton
# Last Modified: September 17, 2025
#
# Course model with one validate() for both create/modify,
# helpers to add/modify/delete inside config['config']['courses'].

# Helpers

def _clean_list(items):
    out, seen = [], set()
    for x in items or []:
        s = str(x).strip()
        if s and s not in seen:
            seen.add(s)
            out.append(s)
    return out

def _get_courses_list(config_obj):
    if not isinstance(config_obj, dict):
        raise ValueError("config_obj must be the INNER dict: config['config']")
    if "courses" not in config_obj or not isinstance(config_obj["courses"], list):
        config_obj["courses"] = []
    return config_obj["courses"]

def _find_course_indexes(courses_list, course_id):
    """Return list of all indexes that match a course_id (may be empty)."""
    target = str(course_id).strip()
    idxs = []
    for i, c in enumerate(courses_list or []):
        if str(c.get("course_id", "")).strip() == target:
            idxs.append(i)
    return idxs

class Course:
    def __init__(self, course_id, credits, room=None, lab=None, conflicts=None, faculty=None):
        self.course_id = str(course_id).strip()
        self.credits = int(credits)
        self.room = _clean_list(room or [])
        self.lab = _clean_list(lab or [])
        self.conflicts = _clean_list(conflicts or [])
        self.faculty = _clean_list(faculty or [])

    @staticmethod
    def from_dict(data):
        if not isinstance(data, dict):
            raise ValueError("course must be a dict")
        if "course_id" not in data:
            raise ValueError("missing 'course_id'")
        if "credits" not in data:
            raise ValueError("missing 'credits'")
        return Course(
            course_id=data["course_id"],
            credits=data["credits"],
            room=data.get("room", []),
            lab=data.get("lab", []),
            conflicts=data.get("conflicts", []),
            faculty=data.get("faculty", []),
        )

    def to_dict(self, omit_empty=True):
        d = {
            "course_id": self.course_id,
            "credits": int(self.credits),
            "room": list(self.room),
            "lab": list(self.lab),
            "conflicts": list(self.conflicts),
            "faculty": list(self.faculty),
        }
        if omit_empty:
            for k in ("room", "lab", "conflicts", "faculty"):
                if not d[k]:
                    del d[k]
        return d

    # Edit functions
    def rename(self, new_course_id):
        new_id = str(new_course_id).strip()
        if not new_course_id:
            raise ValueError("new course_id cannot be null")
        self.course_id = new_course_id

    def set_credits(self, n):
        n = int(n)
        if n < 0:
            raise ValueError("credits must be >= 0")
        self.credits = n

    def set_rooms(self, rooms):        self.room = _clean_list(rooms)
    def add_rooms(self, rooms):        self.room = _clean_list([*self.room, *(rooms or [])])
    def remove_rooms(self, rooms):     self.room = [x for x in self.room if x not in set(_clean_list(rooms))]

    def set_labs(self, labs):          self.lab = _clean_list(labs)
    def add_labs(self, labs):          self.lab = _clean_list([*self.lab, *(labs or [])])
    def remove_labs(self, labs):       self.lab = [x for x in self.lab if x not in set(_clean_list(labs))]

    def set_conflicts(self, conflicts):  self.conflicts = _clean_list(conflicts)
    def add_conflicts(self, conflicts):  self.conflicts = _clean_list([*self.conflicts, *(conflicts or [])])
    def remove_conflicts(self, conflicts): self.conflicts = [x for x in self.conflicts if x not in set(_clean_list(conflicts))]

    def set_faculty(self, faculty):    self.faculty = _clean_list(faculty)
    def add_faculty(self, faculty):    self.faculty = _clean_list([*self.faculty, *(faculty or [])])
    def remove_faculty(self, faculty): self.faculty = [x for x in self.faculty if x not in set(_clean_list(faculty))]

    # Validation function (used for create & modify)
    def validate(
        self,
        *,
        config_obj=None,          # inner dict: config['config']; for rooms/labs membership
        existing_courses=None,    # list of dicts or Course objects; for uniqueness
        strict_membership=False,  # True -> unknown rooms/labs raise
        ignore_index=None         # when modifying, skip that index in uniqueness check
    ):
        # Basic
        if not self.course_id:
            raise ValueError("course_id cannot be empty")
        if not isinstance(self.credits, int):
            raise ValueError("credits must be an int")
        if self.credits < 0:
            raise ValueError("credits must be >= 0")

        # Membership
        if isinstance(config_obj, dict):
            cfg_rooms = list(config_obj.get("rooms", []) or [])
            cfg_labs = list(config_obj.get("labs", []) or [])
            msgs = []
            if cfg_rooms:
                bad_rooms = [r for r in self.room if r not in cfg_rooms]
                if bad_rooms:
                    msgs.append("unknown room(s): " + ", ".join(bad_rooms))
            if cfg_labs:
                bad_labs = [l for l in self.lab if l not in cfg_labs]
                if bad_labs:
                    msgs.append("unknown lab(s): " + ", ".join(bad_labs))
            if strict_membership and msgs:
                raise ValueError("; ".join(msgs))

        # Uniqueness
        if existing_courses is not None and ignore_index is None:
            for i, c in enumerate(existing_courses or []):
                other_id = c.course_id if isinstance(c, Course) else str(c.get("course_id", "")).strip()
                if other_id == self.course_id:
                    raise ValueError(f"duplicate course_id '{self.course_id}' at index {i}")

    # Helper function when creating
    @staticmethod
    def build_and_validate(data, *, config_obj=None, existing_courses=None, strict_membership=False):
        c = Course.from_dict(data)
        c.validate(config_obj=config_obj, existing_courses=existing_courses, strict_membership=strict_membership)
        return c


# Config-level helpers (for the CLI to call)

def add_course_to_config(config_obj, course_dict, *, strict_membership=True):
    """
    Validate and append a new course dict to config_obj['courses'].
    Raises ValueError if invalid or duplicate.
    """
    courses = _get_courses_list(config_obj)
    course = Course.build_and_validate(course_dict, config_obj=config_obj, existing_courses=courses, strict_membership=strict_membership)
    courses.append(course.to_dict())
    return course.to_dict()

def modify_course_in_config(config_obj, course_id, *, updates=None, strict_membership=True, target_index=None):
    """
    Replace fields for a course by id or index.
    If multiple courses share the same course_id, and target_index is None,
    the first match is modified. GUI can specify target_index for duplicates.
    """
    courses = _get_courses_list(config_obj)

    # Determine which index to edit
    if target_index is not None:
        if target_index < 0 or target_index >= len(courses):
            raise ValueError(f"invalid target_index: {target_index}")
        idx = target_index
    else:
        # fallback: edit first match
        idxs = _find_course_indexes(courses, course_id)
        if not idxs:
            raise ValueError(f"course not found: {course_id}")
        if len(idxs) > 1:
            print(f"⚠️ Multiple '{course_id}' found; editing first instance (index {idxs[0]}).")
        idx = idxs[0]

    cur = Course.from_dict(courses[idx])
    updates = updates or {}

    if "course_id" in updates and updates["course_id"] is not None:
        cur.rename(updates["course_id"])
    if "credits" in updates and updates["credits"] is not None:
        cur.set_credits(updates["credits"])
    if "room" in updates and updates["room"] is not None:
        cur.set_rooms(updates["room"])
    if "lab" in updates and updates["lab"] is not None:
        cur.set_labs(updates["lab"])
    if "conflicts" in updates and updates["conflicts"] is not None:
        cur.set_conflicts(updates["conflicts"])
    if "faculty" in updates and updates["faculty"] is not None:
        cur.set_faculty(updates["faculty"])

    # Validate, ignoring the same index
    cur.validate(
        config_obj=config_obj,
        existing_courses=courses,
        strict_membership=False,
        ignore_index=idx,
    )

    courses[idx] = cur.to_dict()
    return courses[idx]

def delete_course_from_config(config_obj, course_id):
    courses = _get_courses_list(config_obj)
    idx = _find_course_index(courses, course_id)
    if idx == -1:
        raise ValueError(f"course not found: {course_id}")
    return courses.pop(idx)