import pytz
import logging

logger = logging.getLogger(__name__)

class Account:
    def __init__(self, user_id: int, timezone: str = ""):
        self.user_id = user_id
        self.timezone = timezone

    @staticmethod
    def is_a_timezone(timezone: str) -> bool:
        if timezone in pytz.all_timezones:
            logger.info(f"Valid timezone: {timezone}")
            return True
        else:
            logger.error(f"Invalid timezone: {timezone}")
            return False
