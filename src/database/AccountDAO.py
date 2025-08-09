import psycopg
import logging
from typing import Optional, Tuple
from src.database.PostgreSQLDB import PostgreSQLDB
from src.models.Account import Account
from psycopg.errors import UniqueViolation

logger = logging.getLogger(__name__)


class AccountDAO:
    @staticmethod
    def addAccount(discord_uid: int) -> bool:
        try:
            with PostgreSQLDB() as connection:
                with connection.cursor() as cursor:
                    try:
                        cursor.execute("INSERT INTO account (user_id) VALUES (%s)", (discord_uid,)) # (discord_uid,) => tuple
                        return True
                    except UniqueViolation as e: # If the account is already registered
                        connection.rollback()
                        logger.warning(f"Account already exists for user_id={discord_uid}.")
                        return False
                connection.commit()
                logger.info(f"New account successfully created => user_id={discord_uid}.")
                return True
        except psycopg.DatabaseError as e:
            connection.rollback()
            logger.error(f"Error while inserting new user ({discord_uid}): {e}")
            return False

    @staticmethod
    def setTimezone(discord_uid: int, timezone: str) -> bool:
        if not Account.is_a_timezone(timezone):
            logger.error(f"Error updating user timezone: timezone ({timezone}) not supported")
            return False
        
        try:
            with PostgreSQLDB() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("UPDATE account SET timezone = %s WHERE user_id = %s", (timezone, discord_uid))
                connection.commit()
                logger.info(f"User timezone updated for user_id={discord_uid}")
                return True
        except psycopg.DatabaseError as e:
            connection.rollback()
            logger.error(f"Error updating user_id={discord_uid} timezone: {e}")
            return False

    @staticmethod
    def getAccountById(discord_uid: int) -> Optional[Tuple]:
        try:
            result = None
            with PostgreSQLDB() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM account WHERE user_id = %s", (discord_uid,))
                    result = cursor.fetchone()
                if result:
                    logger.info(f"User info retrieved for user_id={discord_uid}")
                else:
                    logger.info(f"No account found for user_id={discord_uid}")
                return result
        except psycopg.DatabaseError as e:
            logger.error(f"Error getting account for user_id={discord_uid}: {e}")
            return result
