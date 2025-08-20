from dataclasses import dataclass


@dataclass
class ReminderInfo:
    is_active: bool
    name: str
    date: str
    time: str
