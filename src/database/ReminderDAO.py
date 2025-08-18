import psycopg
import logging
from typing import Optional, Tuple
from src.models.Reminder import Reminder
from psycopg.errors import UniqueViolation
import src.database.PostgreSQLDB as psqldb
from datetime import datetime

logger = logging.getLogger(__name__)


class ReminderDAO:
    @staticmethod
    def add_reminder(reminder: Reminder) -> bool:
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
                                reminder.time,
                                reminder.date,
                                reminder.intervals,
                                reminder.message,
                            ),
                        )
                    except UniqueViolation as e:
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
                        (reminder_time, discord_uid, reminder_name),
                    )
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
        discord_uid: int, reminder_name: str, reminder_date: datetime
    ) -> bool:
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
                        (reminder_date, discord_uid, reminder_name),
                    )
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
    def reminder_exists(discord_uid: int, reminder_name: str) -> Optional[Tuple]:
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
                logger.info(
                    f"Reminder info retrieved for user_id={discord_uid} and reminder_name={reminder_name}"
                )
            else:
                logger.info(
                    f"No reminder found for user_id={discord_uid} and reminder_name={reminder_name}"
                )
            return result
        except psycopg.DatabaseError as e:
            logger.error(
                f"Error getting reminder for user_id={discord_uid} and reminder_name={reminder_name}: {e}"
            )
            return None

    @staticmethod
    def get_reminder_count(discord_uid: int) -> int:
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
            logger.info(f"Reminder count retrieved for user_id={discord_uid}")
            return result
        except psycopg.DatabaseError as e:
            logger.error(f"Error getting reminder count for user_id={discord_uid}: {e}")
            return 0

    @staticmethod
    def get_reminders_by_offset(
        discord_uid: int, offset: int, page_size: int
    ) -> Optional[Tuple]:
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
            logger.info(f"Reminder retrieved for user_id={discord_uid}")
            return result
        except psycopg.DatabaseError as e:
            logger.error(f"Error getting reminder for user_id={discord_uid}: {e}")
            return None

    @staticmethod
    def get_reminders_by_offset_activity(
        discord_uid: int, offset: int, page_size: int, activity: bool
    ) -> Optional[Tuple]:
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
            logger.info(f"Reminder retrieved for user_id={discord_uid}")
            return result
        except psycopg.DatabaseError as e:
            logger.error(f"Error getting reminder for user_id={discord_uid}: {e}")
            return None

    @staticmethod
    def get_reminder_count_by_activity(discord_uid: int, activity: bool) -> int:
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
            logger.info(f"Reminder count by activity retrieved for user_id={discord_uid}, activity={activity}")
            return result
        except psycopg.DatabaseError as e:
            logger.error(f"Error getting reminder count by activity for user_id={discord_uid}, activity={activity}: {e}")
            return 0
