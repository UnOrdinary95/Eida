import psycopg
import logging
from src.models.Reminder import Reminder
from psycopg.errors import UniqueViolation
import src.database.PostgreSQLDB as psqldb

logger = logging.getLogger(__name__)


class ReminderDAO:
    @staticmethod
    def add_reminder(reminder: Reminder) -> bool:
        try:
            with psycopg.connect(
                user=psqldb.DBUSER,
                password=psqldb.DBPASS,
                host=psqldb.DBHOST,
                dbname=psqldb.DBNAME
            ) as connection:
                with connection.cursor() as cursor:
                    try:
                        cursor.execute("INSERT INTO reminder (user_id, r_name, r_time, r_date, r_intervals, r_message)" \
                        " VALUES (%s, %s, %s, %s, %s, %s)", (reminder.user_id, reminder.reminder_name, reminder.time, reminder.date, reminder.intervals, reminder.message))
                    except UniqueViolation as e:
                        logger.warning(f"Reminder already exists for user_id={reminder.user_id}.")
                        return False
            logger.info(f"New reminder successfully created for user_id={reminder.user_id}.")
            return True
        except psycopg.DatabaseError as e:
            logger.error(f"Error while inserting new reminder for user_id={reminder.user_id}: {e}")
            return False