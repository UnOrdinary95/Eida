import re
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class Reminder:
    """Core reminder model with comprehensive validation."""

    def __init__(
        self,
        user_id: int,
        reminder_name: str,
        time: str,
        date: str,
        intervals: str,
        message: str,
        reminder_id: int = None,
        status: bool = True,
    ):
        self.user_id = user_id
        self.reminder_name = reminder_name
        self.time = time
        # Auto-fill today's date when user doesn't specify, common use case
        if date == "":
            self.date = datetime.now().date().strftime("%d/%m/%Y")
        else:
            self.date = date
        self.intervals = intervals
        self.message = message
        self.reminder_id = reminder_id
        self.status = status

    @staticmethod
    def validate_time(time: str) -> bool:
        """
        Validate time format (HH:MM) with 24-hour format.
        Regex ensures hours 00-23 and minutes 00-59 for precise scheduling.
        """
        if not re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", time):
            logger.error("Invalid time format")
            return False
        logger.info("Valid time format")
        return True

    @staticmethod
    def validate_date(date: str) -> bool:
        """
        Validate date format (DD/MM/YYYY) and actual date validity.
        Empty string allowed for "today" convenience.
        Two-step validation: format check then actual date existence.
        """
        if date == "":
            logger.info("No date provided, using current date")
            return True

        # Format validation catches obvious errors early
        if not re.match(r"^(0[1-9]|[12]\d|3[01])/(0[1-9]|1[0-2])/\d{4}$", date):
            logger.error("Invalid date format")
            return False

        logger.info("Valid date format")
        try:
            # Actual date validation catches impossible dates like 31/02/2024
            datetime.strptime(date, "%d/%m/%Y")
            logger.info("Valid date value")
            return True
        except ValueError:
            logger.error("Invalid date value")
            return False

    @staticmethod
    def validate_intervals(intervals: str) -> bool:
        """
        Validate intervals format for recurring reminders.
        Supports two patterns: every X time (e10m2h1d) or weekly (w:mon,wed,fri).
        Empty string creates one-time reminder.
        """
        if intervals == "":
            logger.info("No intervals provided")
            return True

        # Pattern: e10m2h1d (every 10 minutes, 2 hours, 1 day)
        if re.match(r"^e(\d+m)?(\d+h)?(\d+d)?$", intervals):
            parts = re.findall(r"(\d+)([mhd])", intervals)
            for num, unit in parts:
                num = int(num)
                # Minimum 10 minutes prevents spam, maximum 60 minutes prevents confusion with hours
                if unit == "m" and (num < 10 or num > 60):
                    logger.error("Minutes must be between 10 and 60")
                    return False
                # Maximum 24 hours prevents confusion with days
                if unit == "h" and num > 24:
                    logger.error("Hours must be <= 24")
                    return False
            logger.info("Valid intervals format")
            return True

        # Pattern: w:mon,tue,wed or w:* (all days)
        if re.match(
            r"^w:(?:\*|(?:mon|tue|wed|thu|fri|sat|sun)(?:,(?:mon|tue|wed|thu|fri|sat|sun))*)$",
            intervals,
        ):
            logger.info("Valid intervals format")
            return True

        logger.error("Invalid intervals format")
        return False

    @staticmethod
    def validate_reminder_name(name: str) -> bool:
        """
        Validate reminder name length for database storage and UI display.
        50 character limit ensures readability in Discord embeds.
        """
        if len(name) > 50:
            logger.error("Reminder name too long (max 50 chars)")
            return False
        logger.info("Valid reminder name")
        return True

    @staticmethod
    def validate_message(message: str) -> bool:
        """
        Validate reminder message content and length.
        1024 char limit matches Discord embed description limit.
        Empty messages not allowed since they serve no purpose.
        """
        if message == "":
            logger.error("No message provided")
            return False

        if len(message) > 1024:
            logger.error("Message too long (max 1024 chars)")
            return False
        logger.info(message)
        return True
