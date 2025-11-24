# Models/time_slot_model.py
from dataclasses import dataclass, field
from typing import List, Dict, Any
import re

TIME_RE = re.compile(r"^([01]\d|2[0-3]):([0-5]\d)$")


def parse_time_to_minutes(t: str) -> int:
    """Convert 'HH:MM' to minutes since midnight. Raises ValueError on bad format."""
    if not isinstance(t, str) or not TIME_RE.match(t):
        raise ValueError(f"Invalid time format: {t!r}. Expected 'HH:MM'")
    hh, mm = t.split(":")
    return int(hh) * 60 + int(mm)


def minutes_to_time_str(m: int) -> str:
    if m < 0 or m >= 24 * 60:
        raise ValueError("minutes out of range 0..1439")
    hh = m // 60
    mm = m % 60
    return f"{hh:02d}:{mm:02d}"


@dataclass
class TimeInterval:
    start: str
    end: str
    spacing: int  # minutes
    professors: List[str] = field(default_factory=list)
    labs: List[str] = field(default_factory=list)
    courses: List[str] = field(default_factory=list)

    def validate(self) -> None:
        s = parse_time_to_minutes(self.start)
        e = parse_time_to_minutes(self.end)
        if e <= s:
            raise ValueError(
                f"Interval end must be after start: {self.start} - {self.end}"
            )
        if self.spacing <= 0:
            raise ValueError("spacing must be a positive integer (minutes)")

    def generate_slots(self) -> List[str]:
        """Return list of slot start times (HH:MM) for this interval using spacing."""
        self.validate()
        slots = []
        s = parse_time_to_minutes(self.start)
        e = parse_time_to_minutes(self.end)
        t = s
        while t < e:
            slots.append(minutes_to_time_str(t))
            t += self.spacing
        return slots

    def to_dict(self) -> Dict[str, Any]:
        out = {"start": self.start, "spacing": self.spacing, "end": self.end}
        if self.professors:
            out["professors"] = list(self.professors)
        if self.labs:
            out["labs"] = list(self.labs)
        if self.courses:
            out["courses"] = list(self.courses)
        return out

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TimeInterval":
        return cls(
            start=d["start"],
            spacing=int(d["spacing"]),
            end=d["end"],
            professors=[
                str(x).strip() for x in d.get("professors", []) if str(x).strip()
            ],
            labs=[str(x).strip() for x in d.get("labs", []) if str(x).strip()],
            courses=[str(x).strip() for x in d.get("courses", []) if str(x).strip()],
        )


@dataclass
class TimeSlotConfig:
    # times: mapping MON/TUE/... -> List[TimeInterval]
    times: Dict[str, List[TimeInterval]] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TimeSlotConfig":
        times_raw = d.get("times", {})
        times = {}
        for day, intervals in times_raw.items():
            times[day] = [TimeInterval.from_dict(i) for i in intervals]
        return cls(times=times)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "times": {
                day: [iv.to_dict() for iv in intervals]
                for day, intervals in self.times.items()
            },
        }

    # ---- Time interval operations ----
    def add_interval(self, day: str, interval_dict: Dict[str, Any]) -> None:
        iv = TimeInterval.from_dict(interval_dict)
        iv.validate()
        self.times.setdefault(day, []).append(iv)

    def remove_interval(self, day: str, index: int) -> None:
        if day not in self.times:
            raise KeyError(f"No intervals for day {day}")
        self.times[day].pop(index)
        if not self.times[day]:
            del self.times[day]

    def edit_interval(
        self, day: str, index: int, new_interval_dict: Dict[str, Any]
    ) -> None:
        if day not in self.times:
            raise KeyError(f"No intervals for day {day}")
        iv = TimeInterval.from_dict(new_interval_dict)
        iv.validate()
        self.times[day][index] = iv

    def get_intervals(self, day: str) -> List[TimeInterval]:
        return list(self.times.get(day, []))

    def generate_slots_for_day(self, day: str) -> List[str]:
        """Generate all slot start times for a given day (concatenate intervals in order)."""
        slots = []
        for iv in self.times.get(day, []):
            slots.extend(iv.generate_slots())
        return slots

    def generate_all_slots(self) -> Dict[str, List[str]]:
        """Return mapping day -> list of HH:MM start times."""
        return {day: self.generate_slots_for_day(day) for day in self.times.keys()}
