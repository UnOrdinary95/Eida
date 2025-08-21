import psycopg
import logging
from typing import Optional
from src.models.Account import Account
from psycopg.errors import UniqueViolation
import src.database.PostgreSQLDB as psqldb

logger = logging.getLogger(__name__)


class AccountDAO:
    """
    Data Access Object for account operations.
    Uses static methods since no instance state is needed for database operations.
    """

    @staticmethod
    def add_account(discord_uid: int) -> bool:
        """Create new account record for Discord user."""
        try:
            with psycopg.connect(
                user=psqldb.DBUSER,
                password=psqldb.DBPASS,
                host=psqldb.DBHOST,
                dbname=psqldb.DBNAME,
            ) as connection:
                with connection.cursor() as cursor:
                    try:
                        # Tuple syntax required for single parameter to avoid string iteration
                        cursor.execute(
                            "INSERT INTO account (user_id) VALUES (%s)", (discord_uid,)
                        )
                    except UniqueViolation as e:
                        # Expected error when user tries to register multiple times
                        logger.warning(
                            f"Account already exists for user_id={discord_uid}."
                        )
                        return False
            logger.info(f"New account successfully created => user_id={discord_uid}.")
            return True
        except psycopg.DatabaseError as e:
            logger.error(f"Error while inserting new user ({discord_uid}): {e}")
            return False

    @staticmethod
    def set_timezone(discord_uid: int, timezone: str) -> bool:
        """
        Update user's timezone setting with pre-validation.
        """
        # Validate timezone using pytz before database interaction
        if not Account.is_a_timezone(timezone):
            return False

        try:
            with psycopg.connect(
                user=psqldb.DBUSER,
                password=psqldb.DBPASS,
                host=psqldb.DBHOST,
                dbname=psqldb.DBNAME,
            ) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE account SET timezone = %s WHERE user_id = %s",
                        (timezone, discord_uid),
                    )
            logger.info(f"User timezone updated for user_id={discord_uid}")
            return True
        except psycopg.DatabaseError as e:
            logger.error(f"Error updating user_id={discord_uid} timezone: {e}")
            return False

    @staticmethod
    def account_exists(discord_uid: int) -> Optional[Account]:
        """
        Check if account exists and return Account object if found.
        Returns Optional[Account] to handle both existence check and data retrieval.
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
                        "SELECT * FROM account WHERE user_id = %s", (discord_uid,)
                    )
                    result = cursor.fetchone()
            if result:
                # Unpack database row into Account model fields
                user_id, timezone = result
                logger.info(f"User info retrieved for user_id={discord_uid}")
                return Account(user_id, timezone)
            else:
                logger.info(f"No account found for user_id={discord_uid}")
                return None
        except psycopg.DatabaseError as e:
            logger.error(f"Error getting account for user_id={discord_uid}: {e}")
            return None
