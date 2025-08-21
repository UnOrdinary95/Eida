import psycopg
import logging
from typing import Optional, List
from src.models.Reminder import Reminder
from psycopg.errors import UniqueViolation
import src.database.PostgreSQLDB as psqldb
from datetime import datetime, timedelta
from src.models.dto import ReminderInfo
import re

logger = logging.getLogger(__name__)


class ReminderDAO:
    @staticmethod
    def add_reminder(reminder: Reminder) -> bool:
        """
        Insert new reminder with data type conversion for PostgreSQL storage.
        """
        try:
            with psycopg.connect(
                user=psqldb.DBUSER,
                password=psqldb.DBPASS,
                host=psqldb.DBHOST,
                dbname=psqldb.DBNAME,
            ) as connection:
                with connection.cursor() as cursor:
                    try:
                        cursor.execute(
                            "INSERT INTO reminder (user_id, r_name, r_time, r_date, r_intervals, r_message)"
                            " VALUES (%s, %s, %s, %s, %s, %s)",
                            (
                                reminder.user_id,
                                reminder.reminder_name,
                                datetime.strptime(reminder.time, "%H:%M").time(),
                                datetime.strptime(reminder.date, "%d/%m/%Y").date(),
                                reminder.intervals,
                                reminder.message,
                            ),
                        )
                    except UniqueViolation as e:
                        # Expected when user tries to create reminder with same name
                        logger.warning(
                            f"Reminder already exists for user_id={reminder.user_id}."
                        )
                        return False
            logger.info(
                f"New reminder successfully created for user_id={reminder.user_id}."
            )
            return True
        except psycopg.DatabaseError as e:
            logger.error(
                f"Error while inserting new reminder for user_id={reminder.user_id}: {e}"
            )
            return False

    @staticmethod
    def set_reminder_message(
        discord_uid: int, reminder_name: str, reminder_message: str
    ) -> bool:
        """
        Update existing reminder message using user_id + reminder_name as composite key.
        """
        try:
            with psycopg.connect(
                user=psqldb.DBUSER,
                password=psqldb.DBPASS,
                host=psqldb.DBHOST,
                dbname=psqldb.DBNAME,
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE reminder SET r_message = %s WHERE user_id = %s AND r_name = %s",
                        (reminder_message, discord_uid, reminder_name),
                    )
                    # Check rowcount to verify reminder exists and was updated
                    if cursor.rowcount == 0:
                        logger.warning(
                            f"No reminder found to update for user_id={discord_uid} and reminder_name={reminder_name}"
                        )
                        return False
            logger.info(
                f"Reminder message updated for user_id={discord_uid} and reminder_name={reminder_name}"
            )
            return True
        except psycopg.DatabaseError as e:
            logger.error(
                f"Error updating reminder message for user_id={discord_uid} and reminder_name={reminder_name}: {e}"
            )
            return False

    @staticmethod
    def set_reminder_time(
        discord_uid: int, reminder_name: str, reminder_time: str
    ) -> bool:
        """
        Update reminder time with string-to-time conversion for database storage.
        """
        try:
            with psycopg.connect(
                user=psqldb.DBUSER,
                password=psqldb.DBPASS,
                host=psqldb.DBHOST,
                dbname=psqldb.DBNAME,
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE reminder SET r_time = %s WHERE user_id = %s AND r_name = %s",
                        (
                            datetime.strptime(reminder_time, "%H:%M").time(),
                            discord_uid,
                            reminder_name,
                        ),
                    )
                    # Verify reminder exists and was successfully updated
                    if cursor.rowcount == 0:
                        logger.warning(
                            f"No reminder found to update for user_id={discord_uid} and reminder_name={reminder_name}"
                        )
                        return False
            logger.info(
                f"Reminder time updated for user_id={discord_uid} and reminder_name={reminder_name}"
            )
            return True
        except psycopg.DatabaseError as e:
            logger.error(
                f"Error updating reminder time for user_id={discord_uid} and reminder_name={reminder_name}: {e}"
            )
            return False

    @staticmethod
    def set_reminder_date(
        discord_uid: int, reminder_name: str, reminder_date: str
    ) -> bool:
        """
        Update reminder date with string-to-date conversion for PostgreSQL storage.
        """
        try:
            with psycopg.connect(
                user=psqldb.DBUSER,
                password=psqldb.DBPASS,
                host=psqldb.DBHOST,
                dbname=psqldb.DBNAME,
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE reminder SET r_date = %s WHERE user_id = %s AND r_name = %s",
                        (
                            # Convert "DD/MM/YYYY" string to date object for database storage
                            datetime.strptime(reminder_date, "%d/%m/%Y").date(),
                            discord_uid,
                            reminder_name,
                        ),
                    )
                    # Ensure reminder was found and updated successfully
                    if cursor.rowcount == 0:
                        logger.warning(
                            f"No reminder found to update for user_id={discord_uid} and reminder_name={reminder_name}"
                        )
                        return False
            logger.info(
                f"Reminder date updated for user_id={discord_uid} and reminder_name={reminder_name}"
            )
            return True
        except psycopg.DatabaseError as e:
            logger.error(
                f"Error updating reminder date for user_id={discord_uid} and reminder_name={reminder_name}: {e}"
            )
            return False

    @staticmethod
    def set_reminder_name(discord_uid: int, reminder_name: str, new_name: str) -> bool:
        """
        Update reminder name using old name as identifier.
        """
        try:
            with psycopg.connect(
                user=psqldb.DBUSER,
                password=psqldb.DBPASS,
                host=psqldb.DBHOST,
                dbname=psqldb.DBNAME,
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE reminder SET r_name = %s WHERE user_id = %s AND r_name = %s",
                        (new_name, discord_uid, reminder_name),
                    )
                    # Verify reminder was found using the old name before update
                    if cursor.rowcount == 0:
                        logger.warning(
                            f"No reminder found to update for user_id={discord_uid} and reminder_name={reminder_name}"
                        )
                        return False
            logger.info(
                f"Reminder name updated for user_id={discord_uid} and reminder_name={reminder_name}"
            )
            return True
        except psycopg.DatabaseError as e:
            logger.error(
                f"Error updating reminder name for user_id={discord_uid} and reminder_name={reminder_name}: {e}"
            )
            return False

    @staticmethod
    def set_reminder_intervals(
        discord_uid: int, reminder_name: str, reminder_intervals: str
    ) -> bool:
        """
        Update reminder recurrence pattern (e.g., 'e10m2h1d' or 'w:mon,tue,fri').
        """
        try:
            with psycopg.connect(
                user=psqldb.DBUSER,
                password=psqldb.DBPASS,
                host=psqldb.DBHOST,
                dbname=psqldb.DBNAME,
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE reminder SET r_intervals = %s WHERE user_id = %s AND r_name = %s",
                        (reminder_intervals, discord_uid, reminder_name),
                    )
                    # Confirm reminder exists before attempting interval modification
                    if cursor.rowcount == 0:
                        logger.warning(
                            f"No reminder found to update for user_id={discord_uid} and reminder_name={reminder_name}"
                        )
                        return False
            logger.info(
                f"Reminder intervals updated for user_id={discord_uid} and reminder_name={reminder_name}"
            )
            return True
        except psycopg.DatabaseError as e:
            logger.error(
                f"Error updating reminder intervals for user_id={discord_uid} and reminder_name={reminder_name}: {e}"
            )
            return False

    @staticmethod
    def delete_reminder(discord_uid: int, reminder_name: str) -> bool:
        """
        Permanently remove reminder from database.
        """
        try:
            with psycopg.connect(
                user=psqldb.DBUSER,
                password=psqldb.DBPASS,
                host=psqldb.DBHOST,
                dbname=psqldb.DBNAME,
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM reminder WHERE user_id = %s AND r_name = %s",
                        (discord_uid, reminder_name),
                    )
                    # Verify reminder existed before deletion attempt
                    if cursor.rowcount == 0:
                        logger.warning(
                            f"No reminder found to delete for user_id={discord_uid} and reminder_name={reminder_name}"
                        )
                        return False
            logger.info(
                f"Reminder deleted for user_id={discord_uid} and reminder_name={reminder_name}"
            )
            return True
        except psycopg.DatabaseError as e:
            logger.error(
                f"Error deleting reminder for user_id={discord_uid} and reminder_name={reminder_name}: {e}"
            )
            return False

    @staticmethod
    def toggle_reminder_status(discord_uid: int, reminder_name: str) -> bool:
        """
        Switch reminder between active and inactive states using SQL NOT operator.
        Allows users to pause/resume reminders without losing configuration.
        """
        try:
            with psycopg.connect(
                user=psqldb.DBUSER,
                password=psqldb.DBPASS,
                host=psqldb.DBHOST,
                dbname=psqldb.DBNAME,
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE reminder SET is_active = NOT is_active WHERE user_id = %s AND r_name = %s",
                        (discord_uid, reminder_name),
                    )
                    # Confirm reminder exists before status toggle
                    if cursor.rowcount == 0:
                        logger.warning(
                            f"No reminder found to update for user_id={discord_uid} and reminder_name={reminder_name}"
                        )
                        return False
            logger.info(
                f"Reminder status toggled for user_id={discord_uid} and reminder_name={reminder_name}"
            )
            return True
        except psycopg.DatabaseError as e:
            logger.error(
                f"Error toggling reminder status for user_id={discord_uid} and reminder_name={reminder_name}: {e}"
            )
            return False

    @staticmethod
    def reminder_exists(discord_uid: int, reminder_name: str) -> Optional[Reminder]:
        """
        Retrieve full reminder data if it exists, None otherwise.
        """
        try:
            with psycopg.connect(
                user=psqldb.DBUSER,
                password=psqldb.DBPASS,
                host=psqldb.DBHOST,
                dbname=psqldb.DBNAME,
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM reminder WHERE user_id = %s AND r_name = %s",
                        (discord_uid, reminder_name),
                    )
                    result = cursor.fetchone()
            if result:
                # Unpack database row fields in table column order
                (
                    reminder_id,
                    r_name,
                    r_message,
                    r_time,
                    r_date,
                    r_intervals,
                    status,
                    user_id,
                ) = result
                logger.info(
                    f"Reminder info retrieved for user_id={discord_uid} and reminder_name={reminder_name}"
                )
                # Convert database types back to Reminder model string formats
                return Reminder(
                    user_id,
                    r_name,
                    r_time.strftime("%H:%M") if r_time else "",
                    r_date.strftime("%d/%m/%Y") if r_date else "",
                    r_intervals,
                    r_message,
                    reminder_id,
                    status,
                )
            else:
                # Not an error - reminder simply doesn't exist
                logger.info(
                    f"No reminder found for user_id={discord_uid} and reminder_name={reminder_name}"
                )
                return None
        except psycopg.DatabaseError as e:
            logger.error(
                f"Error getting reminder for user_id={discord_uid} and reminder_name={reminder_name}: {e}"
            )
            return None

    @staticmethod
    def get_reminder_count(discord_uid: int) -> int:
        """
        Get total reminder count for pagination calculations.
        """
        try:
            with psycopg.connect(
                user=psqldb.DBUSER,
                password=psqldb.DBPASS,
                host=psqldb.DBHOST,
                dbname=psqldb.DBNAME,
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT COUNT(*) FROM reminder WHERE user_id = %s",
                        (discord_uid,),
                    )
                    result = cursor.fetchone()[0]

            if result:
                logger.info(f"Reminder count retrieved for user_id={discord_uid}")
                return result
            else:
                logger.info(f"No reminders found for user_id={discord_uid}")
                return 0
        except psycopg.DatabaseError as e:
            logger.error(f"Error getting reminder count for user_id={discord_uid}: {e}")
            return 0

    @staticmethod
    def get_reminders_by_offset(
        discord_uid: int, offset: int, page_size: int
    ) -> List[ReminderInfo]:
        """
        Retrieve paginated reminders using OFFSET/LIMIT for dashboard display.
        Returns lightweight ReminderInfo DTOs instead of full Reminder objects.
        """
        try:
            with psycopg.connect(
                user=psqldb.DBUSER,
                password=psqldb.DBPASS,
                host=psqldb.DBHOST,
                dbname=psqldb.DBNAME,
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT is_active, r_name, r_date, r_time FROM reminder WHERE user_id = %s ORDER BY r_name OFFSET %s LIMIT %s",
                        (discord_uid, offset, page_size),
                    )
                    result = cursor.fetchall()

            if result:
                reminders = []
                for row in result:
                    is_active, r_name, r_date, r_time = row

                    # Create DTO with formatted strings for immediate display
                    reminder = ReminderInfo(
                        is_active=is_active,
                        name=r_name,
                        date=r_date.strftime("%d/%m/%Y") if r_date else "",
                        time=r_time.strftime("%H:%M") if r_time else "",
                    )
                    reminders.append(reminder)

                logger.info(f"Reminder retrieved for user_id={discord_uid}")
                return reminders
            else:
                logger.info(f"No reminders found for user_id={discord_uid}")
                return []
        except psycopg.DatabaseError as e:
            logger.error(f"Error getting reminder for user_id={discord_uid}: {e}")
            return []

    @staticmethod
    def get_reminders_by_offset_activity(
        discord_uid: int, offset: int, page_size: int, activity: bool
    ) -> List[ReminderInfo]:
        """
        Retrieve paginated reminders filtered by active/inactive status.
        Enables filtered dashboard views (show only active or only inactive reminders).
        """
        try:
            with psycopg.connect(
                user=psqldb.DBUSER,
                password=psqldb.DBPASS,
                host=psqldb.DBHOST,
                dbname=psqldb.DBNAME,
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT is_active, r_name, r_date, r_time FROM reminder WHERE user_id = %s AND is_active = %s ORDER BY r_name OFFSET %s LIMIT %s",
                        (discord_uid, activity, offset, page_size),
                    )
                    result = cursor.fetchall()

            if result:
                reminders = []
                for row in result:
                    is_active, r_name, r_date, r_time = row

                    # Convert database types to display-ready string formats
                    reminder = ReminderInfo(
                        is_active=is_active,
                        name=r_name,
                        date=r_date.strftime("%d/%m/%Y") if r_date else "",
                        time=r_time.strftime("%H:%M") if r_time else "",
                    )
                    reminders.append(reminder)

                logger.info(
                    f"Reminder retrieved for user_id={discord_uid} and activity={activity}"
                )
                return reminders
            else:
                logger.info(
                    f"No reminders found for user_id={discord_uid} and activity={activity}"
                )
                return []
        except psycopg.DatabaseError as e:
            logger.error(
                f"Error getting reminder for user_id={discord_uid} and activity={activity}: {e}"
            )
            return []

    @staticmethod
    def get_reminder_count_by_activity(discord_uid: int, activity: bool) -> int:
        """
        Get count of reminders filtered by active/inactive status for pagination.
        Used to calculate total pages in filtered dashboard views.
        """
        try:
            with psycopg.connect(
                user=psqldb.DBUSER,
                password=psqldb.DBPASS,
                host=psqldb.DBHOST,
                dbname=psqldb.DBNAME,
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT COUNT(*) FROM reminder WHERE user_id = %s AND is_active = %s",
                        (discord_uid, activity),
                    )
                    result = cursor.fetchone()[0]

            if result:
                logger.info(
                    f"Reminder count by activity retrieved for user_id={discord_uid} and activity={activity}"
                )
                return result
            else:
                logger.info(
                    f"No reminders found for user_id={discord_uid} and activity={activity}"
                )
                return 0
        except psycopg.DatabaseError as e:
            logger.error(
                f"Error getting reminder count by activity for user_id={discord_uid}, activity={activity}: {e}"
            )
            return 0

    @staticmethod
    def get_due_reminders(current_time: datetime) -> List[Reminder]:
        """
        Find all active reminders scheduled at or before current time.
        Used by reminder task to determine which reminders need to be sent.
        """
        try:
            with psycopg.connect(
                user=psqldb.DBUSER,
                password=psqldb.DBPASS,
                host=psqldb.DBHOST,
                dbname=psqldb.DBNAME,
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        # Check three conditions: active, correct date, time has passed
                        "SELECT user_id, r_name, r_time, r_date, r_intervals, r_message, is_active FROM reminder WHERE is_active = %s AND r_date = %s AND r_time <= %s",
                        (True, current_time.date(), current_time.time()),
                    )
                    result = cursor.fetchall()

            reminders = []
            for row in result:
                user_id, reminder_name, time, date, intervals, message, status = row

                # Convert database types back to Reminder model format for processing
                reminder = Reminder(
                    user_id=user_id,
                    reminder_name=reminder_name,
                    time=time.strftime("%H:%M") if time else "",
                    date=date.strftime("%d/%m/%Y") if date else "",
                    intervals=intervals or "",
                    message=message or "",
                    status=status,
                )
                reminders.append(reminder)

            logger.info(f"{len(reminders)} due reminders retrieved")
            return reminders
        except psycopg.DatabaseError as e:
            # Return empty list to prevent reminder task from failing
            logger.error(f"Error getting due reminders: {e}")
            return []

    @staticmethod
    def update_reminder_date_time(reminder: Reminder) -> bool:
        """
        Reschedule recurring reminder to its next occurrence after being sent.
        Complex operation involving interval parsing and datetime calculations.
        """
        if not reminder.intervals:
            # One-time reminders don't need rescheduling
            logger.info(f"No interval specified for reminder {reminder.reminder_name}")
            return True

        try:
            # Step 1: Parse current reminder datetime from string format
            current_datetime = ReminderDAO._parse_reminder_datetime(reminder)
            if not current_datetime:
                logger.error(
                    f"Could not parse current datetime for reminder {reminder.reminder_name}"
                )
                return False

            # Step 2: Calculate when the reminder should next occur
            next_datetime = ReminderDAO._calculate_next_occurrence(
                current_datetime, reminder.intervals
            )
            if not next_datetime:
                logger.error(
                    f"Could not calculate next occurrence for reminder {reminder.reminder_name}"
                )
                return False

            # Step 3: Update database with new scheduled time
            return ReminderDAO._update_reminder_datetime_in_db(reminder, next_datetime)

        except Exception as e:
            logger.error(
                f"Error updating reminder date/time for {reminder.reminder_name}: {e}"
            )
            return False

    @staticmethod
    def _parse_reminder_datetime(reminder: Reminder) -> Optional[datetime]:
        """
        Convert reminder's string date/time fields to datetime object for calculations.
        Handles the format conversion between model strings and Python datetime.
        """
        try:
            date_str = reminder.date  # Format: DD/MM/YYYY
            time_str = reminder.time  # Format: HH:MM

            if not date_str or not time_str:
                return None

            # Manual parsing to match the expected DD/MM/YYYY format
            day, month, year = map(int, date_str.split("/"))
            hour, minute = map(int, time_str.split(":"))

            return datetime(year, month, day, hour, minute)

        except (ValueError, AttributeError) as e:
            logger.error(f"Error parsing datetime from reminder: {e}")
            return None

    @staticmethod
    def _calculate_next_occurrence(
        current_datetime: datetime, interval: str
    ) -> Optional[datetime]:
        """
        Route interval calculation to appropriate handler based on pattern.
        Supports two patterns: weekly (w:) and regular time-based (e).
        """
        try:
            if interval.startswith("w:"):
                # Weekly pattern: w:mon,tue,fri or w:*
                return ReminderDAO._calculate_weekly_next(current_datetime, interval)

            elif interval.startswith("e"):
                # Regular pattern: e10m2h1d (every 10 minutes, 2 hours, 1 day)
                return ReminderDAO._calculate_regular_next(current_datetime, interval)

            else:
                logger.error(f"Invalid interval format: {interval}")
                return None

        except Exception as e:
            logger.error(f"Error calculating next occurrence: {e}")
            return None

    @staticmethod
    def _calculate_weekly_next(
        current_datetime: datetime, interval: str
    ) -> Optional[datetime]:
        """
        Calculate next weekly occurrence by finding the next matching weekday.
        Preserves original time while advancing to next valid day.
        """
        try:
            days_part = interval[2:]  # Remove "w:" prefix
            days = [day.strip().lower() for day in days_part.split(",")]

            # Map day names to Python weekday numbers (Monday=0)
            day_mapping = {
                "mon": 0,
                "tue": 1,
                "wed": 2,
                "thu": 3,
                "fri": 4,
                "sat": 5,
                "sun": 6,
            }

            target_weekdays = [day_mapping[day] for day in days if day in day_mapping]

            if not target_weekdays:
                return None

            # Check next 7 days to find the next matching weekday
            for i in range(1, 8):
                check_date = current_datetime + timedelta(days=i)
                if check_date.weekday() in target_weekdays:
                    # Preserve original time, only change date
                    return datetime(
                        check_date.year,
                        check_date.month,
                        check_date.day,
                        current_datetime.hour,
                        current_datetime.minute,
                    )

            return None

        except Exception as e:
            logger.error(f"Error calculating weekly next occurrence: {e}")
            return None

    @staticmethod
    def _calculate_regular_next(
        current_datetime: datetime, interval: str
    ) -> Optional[datetime]:
        """
        Calculate next regular interval occurrence by parsing time components.
        Supports combined intervals like e10m2h1d (10 minutes + 2 hours + 1 day).
        """
        try:
            interval = interval[1:]  # Remove "e" prefix

            # Initialize all time components
            minutes = 0
            hours = 0
            days = 0

            # Extract each time component using regex
            minute_match = re.search(r"(\d+)m", interval)
            hour_match = re.search(r"(\d+)h", interval)
            day_match = re.search(r"(\d+)d", interval)

            if minute_match:
                minutes = int(minute_match.group(1))
            if hour_match:
                hours = int(hour_match.group(1))
            if day_match:
                days = int(day_match.group(1))

            # Combine all time components into single timedelta
            delta = timedelta(days=days, hours=hours, minutes=minutes)
            next_datetime = current_datetime + delta

            return next_datetime

        except Exception as e:
            logger.error(f"Error calculating regular next occurrence: {e}")
            return None

    @staticmethod
    def _update_reminder_datetime_in_db(
        reminder: Reminder, next_datetime: datetime
    ) -> bool:
        """
        Update reminder's scheduled date and time in database with calculated next occurrence.
        Final step in the recurring reminder rescheduling process.
        """
        try:
            with psycopg.connect(
                user=psqldb.DBUSER,
                password=psqldb.DBPASS,
                host=psqldb.DBHOST,
                dbname=psqldb.DBNAME,
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE reminder SET r_date = %s, r_time = %s WHERE user_id = %s AND r_name = %s",
                        (
                            # Convert datetime back to separate date and time for database storage
                            next_datetime.date(),
                            next_datetime.time(),
                            reminder.user_id,
                            reminder.reminder_name,
                        ),
                    )
                    # Verify reminder still exists
                    if cursor.rowcount == 0:
                        logger.warning(
                            f"No reminder found to update for user_id={reminder.user_id} and reminder_name={reminder.reminder_name}"
                        )
                        return False

            logger.info(
                f"Reminder datetime updated for user_id={reminder.user_id} and reminder_name={reminder.reminder_name}. Next occurrence: {next_datetime}"
            )
            return True

        except psycopg.DatabaseError as e:
            logger.error(
                f"Error updating reminder datetime for user_id={reminder.user_id} and reminder_name={reminder.reminder_name}: {e}"
            )
            return False
