# File Name: ClassPattern_model.py
# Fully rewritten to satisfy all unit tests in test_class_pattern_model.py

import re

WEEKDAYS = {"MON", "TUE", "WED", "THU", "FRI"}


# ------------------------------
# Validation helpers
# ------------------------------


def _validate_time_string(t):
    if t is None:
        return None
    if not isinstance(t, str):
        raise ValueError("Invalid time string")
    if not re.match(r"^\d{2}:\d{2}$", t):
        raise ValueError(f"Time must be HH:MM format, got: {t}")
    return t


def _validate_duration(v):
    try:
        d = int(v)
    except Exception:
        raise ValueError(f"Invalid duration: {v}")
    if d <= 0:
        raise ValueError("duration must be > 0")
    return d


# -----------------------------------
# Meeting parser (simple dictionary)
# -----------------------------------


def _clean_meeting(m):
    """Convert dict → validated pure meeting dict."""
    if not isinstance(m, dict):
        raise ValueError("meeting must be a dict")

    if "day" not in m:
        raise ValueError("meeting must include 'day'")
    if "duration" not in m:
        raise ValueError("meeting must include 'duration'")

    day = str(m["day"]).strip().upper()
    if day not in WEEKDAYS:
        raise ValueError(f"Invalid meeting day: {m['day']}")

    duration = _validate_duration(m["duration"])
    lab = bool(m.get("lab", False))

    # Extra keys discarded (tests require this)
    out = {"day": day, "duration": duration}
    if lab:
        out["lab"] = True

    return out


# ------------------------------
# ClassPattern model
# ------------------------------


class ClassPattern:
    def __init__(self, credits, meetings, start_time=None, disabled=False):
        # ---- credits ----
        try:
            c = int(credits)
        except Exception:
            raise ValueError("Invalid credits")
        if c <= 0:
            raise ValueError("credits must be a positive integer")
        self.credits = c

        # ---- meetings ----
        if not isinstance(meetings, list) or len(meetings) == 0:
            raise ValueError("'meetings' must be a non-empty list")
        self.meetings = [_clean_meeting(m) for m in meetings]

        # ---- start_time ----
        self.start_time = _validate_time_string(start_time)

        # ---- disabled ----
        self.disabled = bool(disabled)

    # ------------------------------
    # dict conversion
    # ------------------------------

    @staticmethod
    def from_dict(d):
        if not isinstance(d, dict):
            raise ValueError("class pattern must be a dict")
        if "credits" not in d:
            raise ValueError("class pattern missing 'credits'")
        if "meetings" not in d:
            raise ValueError("class pattern missing 'meetings'")

        return ClassPattern(
            credits=d["credits"],
            meetings=d["meetings"],
            start_time=d.get("start_time"),
            disabled=d.get("disabled", False),
        )

    def to_dict(self):
        out = {"credits": self.credits, "meetings": self.meetings.copy()}
        if self.start_time is not None:
            out["start_time"] = self.start_time
        if self.disabled:
            out["disabled"] = True
        return out

    # ------------------------------
    # Editing utilities
    # ------------------------------

    def set_credits(self, new):
        if new is None:
            return  # preserve old
        try:
            v = int(new)
        except Exception:
            raise ValueError("credits must be an integer")
        if v <= 0:
            raise ValueError("credits must be > 0")
        self.credits = v

    def add_meeting(self, meeting_dict):
        self.meetings.append(_clean_meeting(meeting_dict))

    def remove_meeting(self, index):
        if not (0 <= index < len(self.meetings)):
            raise ValueError("invalid meeting index")
        del self.meetings[index]

    def update_meeting(self, index, updates):
        if not (0 <= index < len(self.meetings)):
            raise ValueError("invalid meeting index")

        cur = self.meetings[index]

        merged = {
            "day": updates.get("day", cur["day"]),
            "duration": updates.get("duration", cur["duration"]),
            "lab": updates.get("lab", cur.get("lab", False)),
        }

        self.meetings[index] = _clean_meeting(merged)

    def set_start_time(self, t):
        if t is None:
            self.start_time = None
        else:
            self.start_time = _validate_time_string(t)

    def set_disabled(self, flag):
        self.disabled = bool(flag)


# ============================================================
# Config-level operations
# ============================================================


def _get_class_patterns_list(config_obj):
    """Ensure config_obj['classes'] exists and is a list."""
    if "classes" not in config_obj or not isinstance(config_obj["classes"], list):
        config_obj["classes"] = []
    return config_obj["classes"]


def add_class_pattern_to_config(config_obj, pattern_dict):
    patterns = _get_class_patterns_list(config_obj)

    cp = ClassPattern.from_dict(pattern_dict)
    stored = cp.to_dict()

    patterns.append(stored)
    return stored


def modify_class_pattern_in_config(config_obj, index, updates=None):
    patterns = _get_class_patterns_list(config_obj)
    updates = updates or {}

    if not (0 <= index < len(patterns)):
        # TESTS REQUIRE IndexError, not ValueError
        raise IndexError(f"Invalid pattern index {index}")

    cur = ClassPattern.from_dict(patterns[index])

    # Apply updates
    if "credits" in updates:
        cur.set_credits(updates["credits"])

    if "start_time" in updates:
        cur.set_start_time(updates["start_time"])

    if "disabled" in updates:
        cur.set_disabled(updates["disabled"])

    if "meetings" in updates and updates["meetings"] is not None:
        if not isinstance(updates["meetings"], list):
            raise ValueError("'meetings' must be a list")
        cur.meetings = [_clean_meeting(m) for m in updates["meetings"]]

    stored = cur.to_dict()
    patterns[index] = stored
    return stored


def delete_class_pattern_from_config(config_obj, index):
    patterns = _get_class_patterns_list(config_obj)

    if not (0 <= index < len(patterns)):
        # TESTS REQUIRE IndexError
        raise IndexError(f"Invalid pattern index {index}")

    return patterns.pop(index)
