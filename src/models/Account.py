import pytz


class Account:
    def __init__(self, user_id: int, timezone: str):
        self.user_id = user_id
        self.timezone = timezone

    @staticmethod
    def is_a_timezone(timezone: str) -> bool:
        if timezone in pytz.all_timezones:
            return True
        else:
            return False