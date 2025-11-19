# File Name: meeting_pattern_cli.py
# Author: Fletcher Burton
# Last Modified: November 19, 2025
#
# CLI for managing Class Meeting Patterns in the JSON config.
#
# Each pattern is a dict like:
# {
#   "credits": 4,
#   "start_time": "10:00",          # optional
#   "disabled": true,               # optional
#   "meetings": [
#       {"day": "MON", "duration": 75, "lab": False},
#       {"day": "WED", "duration": 75, "lab": True},
#   ]
# }

from typing import List, Dict, Any, Optional

_patterns_ref: List[Dict[str, Any]] = []

# Map user input to MON/TUE/etc.
_DAY_INPUT_MAP = {
    "mon": "MON",
    "monday": "MON",
    "tue": "TUE",
    "tues": "TUE",
    "tuesday": "TUE",
    "wed": "WED",
    "weds": "WED",
    "wednesday": "WED",
    "thu": "THU",
    "thur": "THU",
    "thurs": "THU",
    "thursday": "THU",
    "fri": "FRI",
    "friday": "FRI",
}

# Reverse map for display
_DAY_DISPLAY_MAP = {
    "MON": "Monday",
    "TUE": "Tuesday",
    "WED": "Wednesday",
    "THU": "Thursday",
    "FRI": "Friday",
}


def _normalize_day(raw: str) -> str:
    """Convert 'monday', 'Mon', 'MON' → 'MON' etc., or raise ValueError."""
    r = (raw or "").strip().lower()
    if r in _DAY_INPUT_MAP:
        return _DAY_INPUT_MAP[r]
    # allow direct MON/TUE/etc.
    r_up = r.upper()
    if r_up in _DAY_DISPLAY_MAP:
        return r_up
    raise ValueError("Day must be Monday–Friday (e.g. 'Mon', 'Monday').")


def _display_day(code: str) -> str:
    return _DAY_DISPLAY_MAP.get(code, code or "(unknown)")


def _input_int(prompt: str, allow_blank: bool = False) -> Optional[int]:
    while True:
        raw = input(prompt).strip()
        if allow_blank and raw == "":
            return None
        try:
            return int(raw)
        except Exception:
            print("Please enter a valid integer.")


def _input_yes_no(prompt: str, default: Optional[bool] = None) -> Optional[bool]:
    """
    Returns True/False, or None if user pressed Enter and default is None.
    If default is True/False, empty input returns default.
    """
    while True:
        raw = input(prompt).strip().lower()
        if raw == "" and default is not None:
            return default
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        if raw == "" and default is None:
            return None
        print("Please enter 'y' or 'n'.")


def _build_meetings_interactively() -> List[Dict[str, Any]]:
    meetings: List[Dict[str, Any]] = []
    num = _input_int("How many meetings in this pattern? ", allow_blank=False)
    if num is None or num <= 0:
        print("Pattern must have at least one meeting.")
        return []

    for i in range(1, num + 1):
        print(f"\nMeeting #{i}:")
        # Day
        while True:
            day_raw = input("  Enter day (Monday–Friday): ").strip()
            try:
                day_code = _normalize_day(day_raw)
                break
            except ValueError as e:
                print(f"  Error: {e}")
        # Duration
        duration = _input_int("  Enter duration in minutes: ", allow_blank=False)
        # Lab flag
        is_lab = _input_yes_no("  Is this a lab meeting? (y/n, default n): ", default=False)

        meetings.append(
            {
                "day": day_code,
                "duration": duration,
                "lab": bool(is_lab),
            }
        )
    return meetings


def _print_patterns_list():
    if not _patterns_ref:
        print("\nNo class meeting patterns defined.\n")
        return
    print("\n=== Class Meeting Patterns ===")
    for idx, p in enumerate(_patterns_ref, start=1):
        credits = p.get("credits", "")
        start_time = p.get("start_time", None)
        disabled = p.get("disabled", False)
        print(f"\nPattern #{idx}:")
        print(f"  credits: {credits}")
        if start_time:
            print(f"  start_time: {start_time}")
        else:
            print("  start_time: (none)")
        print(f"  disabled: {bool(disabled)}")
        meetings = p.get("meetings", [])
        if not meetings:
            print("  Meetings: (none)")
        else:
            print("  Meetings:")
            for m in meetings:
                day_code = m.get("day", "")
                duration = m.get("duration", "")
                lab = m.get("lab", False)
                lab_suffix = " (lab)" if lab else ""
                print(
                    f"    - {_display_day(day_code)} "
                    f"{duration} minutes{lab_suffix}"
                )
    print("\n==============================\n")


def _select_pattern_index() -> int:
    if not _patterns_ref:
        print("No patterns to select.")
        return -1
    _print_patterns_list()
    while True:
        raw = input(f"Select pattern number (1-{len(_patterns_ref)}) or blank to cancel: ").strip()
        if raw == "":
            return -1
        try:
            k = int(raw)
            if 1 <= k <= len(_patterns_ref):
                return k - 1
        except Exception:
            pass
        print("Invalid selection, try again.")


def add_pattern():
    print("\n--- Add Class Meeting Pattern ---")
    credits = _input_int("Enter credits for this pattern: ", allow_blank=False)
    start_time = input(
        "Enter start time (HH:MM, optional; leave blank for no fixed start time): "
    ).strip()
    if not start_time:
        start_time = None
    disabled = _input_yes_no("Is this pattern disabled? (y/n, default n): ", default=False)

    meetings = _build_meetings_interactively()
    if not meetings:
        print("Aborted: no valid meetings defined.\n")
        return

    new_pattern: Dict[str, Any] = {
        "credits": credits,
        "meetings": meetings,
    }
    if start_time:
        new_pattern["start_time"] = start_time
    if disabled:
        new_pattern["disabled"] = True

    _patterns_ref.append(new_pattern)
    print("\nPattern added successfully!")
    _print_patterns_list()


def modify_pattern():
    print("\n--- Modify Class Meeting Pattern ---")
    idx = _select_pattern_index()
    if idx == -1:
        return
    pattern = _patterns_ref[idx]

    print("\nCurrent values:")
    credits = pattern.get("credits", "")
    start_time = pattern.get("start_time", None)
    disabled = bool(pattern.get("disabled", False))
    print(f"  credits: {credits}")
    print(f"  start_time: {start_time if start_time else '(none)'}")
    print(f"  disabled: {disabled}")

    # Credits
    raw_credits = input(
        "Enter new credits (leave blank to keep current): "
    ).strip()
    if raw_credits:
        try:
            pattern["credits"] = int(raw_credits)
        except Exception:
            print("Invalid credits entered, keeping previous value.")

    # Start time
    raw_start = input(
        "Enter new start time (HH:MM, leave blank to keep, '-' to clear): "
    ).strip()
    if raw_start == "-":
        pattern.pop("start_time", None)
    elif raw_start:
        pattern["start_time"] = raw_start  # basic string; scheduler will validate

    # Disabled flag
    disabled_new = _input_yes_no(
        "Is this pattern disabled? (y/n, leave blank to keep current): ",
        default=None,
    )
    if disabled_new is not None:
        pattern["disabled"] = bool(disabled_new)
    elif "disabled" in pattern:
        # keep existing; nothing to do
        pass

    # Meetings
    print("\nMeetings for this pattern:")
    meetings = pattern.get("meetings", [])
    if not meetings:
        print("  (none)")
    else:
        for m in meetings:
            print(
                f"  - {_display_day(m.get('day', ''))} "
                f"{m.get('duration', '')} minutes"
                f"{' (lab)' if m.get('lab', False) else ''}"
            )

    change_meetings = _input_yes_no(
        "\nDo you want to replace ALL meetings for this pattern? (y/n, default n): ",
        default=False,
    )
    if change_meetings:
        new_meetings = _build_meetings_interactively()
        if new_meetings:
            pattern["meetings"] = new_meetings
            print("Meetings updated.")
        else:
            print("No valid meetings entered; keeping previous meetings.")

    print("\nPattern updated successfully!")
    _print_patterns_list()


def delete_pattern():
    print("\n--- Delete Class Meeting Pattern ---")
    idx = _select_pattern_index()
    if idx == -1:
        return
    pat = _patterns_ref[idx]
    credits = pat.get("credits", "")
    start_time = pat.get("start_time", None)
    confirm = _input_yes_no(
        f"Are you sure you want to delete Pattern #{idx+1} "
        f"(credits={credits}, start_time={start_time or 'none'})? (y/n): ",
        default=False,
    )
    if not confirm:
        print("Deletion cancelled.")
        return
    _patterns_ref.pop(idx)
    print("Pattern deleted.\n")


def cli_menu():
    while True:
        print("\n--- Class Meeting Pattern Management CLI ---")
        print("1. View Meeting Patterns")
        print("2. Add Meeting Pattern")
        print("3. Modify Meeting Pattern")
        print("4. Delete Meeting Pattern")
        print("5. Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            _print_patterns_list()
        elif choice == "2":
            add_pattern()
        elif choice == "3":
            modify_pattern()
        elif choice == "4":
            delete_pattern()
        elif choice == "5":
            return
        else:
            print("Invalid choice, try again.")


def mainMeetingPatternController(patterns_list: List[Dict[str, Any]]):
    """
    Entry point from main.py.

    patterns_list is the live list from the parsed JSON config:
    fileData['config']['class_patterns'] (or an empty list).
    We mutate it in-place so main.py's saveConfig can write it back out.
    """
    global _patterns_ref
    if isinstance(patterns_list, list):
        _patterns_ref = patterns_list
    else:
        _patterns_ref = []

    cli_menu()