import pytz
import logging

logger = logging.getLogger(__name__)


class Account:
    """Represents user account data separate from Discord user objects."""

    def __init__(self, user_id: int, timezone: str = ""):
        self.user_id = user_id
        # Empty string default allows detection of unset timezone vs invalid timezone
        self.timezone = timezone

    @staticmethod
    def is_a_timezone(timezone: str) -> bool:
        """Validate timezone string against pytz database."""
        if timezone in pytz.all_timezones:
            # Log valid timezones for debugging user setup success
            logger.info(f"Valid timezone: {timezone}")
            return True
        else:
            # Log invalid attempts to help troubleshoot user input issues
            logger.error(f"Invalid timezone: {timezone}")
            return False
