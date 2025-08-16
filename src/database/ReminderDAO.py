import psycopg
import logging
from typing import Optional, Tuple
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

    @staticmethod    
    def set_reminder_message(discord_uid: int, reminder_name: str, reminder_message: str) -> bool:
        try:
            with psycopg.connect(
                user=psqldb.DBUSER,
                password=psqldb.DBPASS,
                host=psqldb.DBHOST,
                dbname=psqldb.DBNAME
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE reminder SET r_message = %s WHERE user_id = %s AND r_name = %s", (reminder_message, discord_uid, reminder_name))
            logger.info(f"Reminder message updated for user_id={discord_uid} and reminder_name={reminder_name}")
            return True
        except psycopg.DatabaseError as e:
            logger.error(f"Error updating reminder message for user_id={discord_uid} and reminder_name={reminder_name}: {e}")
            return False 

    @staticmethod
    def reminder_exists(discord_uid: int, reminder_name: str) -> Optional[Tuple]:
        try:
            with psycopg.connect(
                user=psqldb.DBUSER,
                password=psqldb.DBPASS,
                host=psqldb.DBHOST,
                dbname=psqldb.DBNAME
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM reminder WHERE user_id = %s AND r_name = %s", (discord_uid, reminder_name))
                    result = cursor.fetchone()
            if result:
                logger.info(f"Reminder info retrieved for user_id={discord_uid} and reminder_name={reminder_name}")
            else:
                logger.info(f"No reminder found for user_id={discord_uid} and reminder_name={reminder_name}")
            return result
        except psycopg.DatabaseError as e:
            logger.error(f"Error getting reminder for user_id={discord_uid} and reminder_name={reminder_name}: {e}")
            return None