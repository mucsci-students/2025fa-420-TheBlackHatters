# model.py

import re


# Returns True if 'HH:MM' is formatted correctly and represents a real time.
def validate_time(t: str) -> bool:
    TIME_PATTERN = re.compile(r"^\d{2}:\d{2}$")
    if not TIME_PATTERN.match(t):
        return False
    hh, mm = map(int, t.split(":"))
    return 0 <= hh <= 23 and 0 <= mm <= 59


# Timeslot modifications.
class TimeSlotModel:
    def __init__(self, config: dict):
        self.config = config
        self.times = config.get("times", {})

    # Returns days with a list of their contents.
    def list_slots(self, day: str):
        return self.times.get(day, [])

    # Add a new slot to a day.
    def add_slot(self, day: str, start: str, spacing: int, end: str):
        if not (validate_time(start) and validate_time(end)):
            raise ValueError("Invalid time format")

        self.times.setdefault(day, []).append(
            {"start": start, "spacing": spacing, "end": end}
        )

    # Edit a specific slot on a day.
    def edit_slot(
        self,
        day: str,
        index: int,
        start: str | None = None,
        spacing: int | None = None,
        end: str | None = None,
    ) -> None:
        if day not in self.times or not (0 <= index < len(self.times[day])):
            raise IndexError("Invalid slot index")

        slot = self.times[day][index]

        if start:
            if not validate_time(start):
                raise ValueError("Invalid start time")
            slot["start"] = start

        if end:
            if not validate_time(end):
                raise ValueError("Invalid end time")
            slot["end"] = end

        if spacing is not None:
            slot["spacing"] = spacing

        self.times[day][index] = slot

    # Delete a specific slot on a day.
    def delete_slot(self, day: str, index: int):
        if day not in self.times or not (0 <= index < len(self.times[day])):
            raise IndexError("Invalid slot index")
        return self.times[day].pop(index)
