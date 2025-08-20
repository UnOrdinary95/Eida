from dataclasses import dataclass


@dataclass
class ReminderInfo:
    """
    Data Transfer Object for reminder display information.
    Simplified view of reminder data optimized for UI presentation.
    """

    is_active: bool
    name: str
    date: str
    time: str
