import psycopg2

from typing import Optional, Tuple
from src.database.PostgreSQLDB import PostgreSQLDB
from src.models.Account import Account

class AccountDAO:
    @staticmethod
    def addAccount(anID: int) -> Optional[bool]:
        try:
            with PostgreSQLDB() as db:
                with db.cursor() as cursor:
                        cursor.execute("INSERT INTO account (user_id) VALUES (%s)", (anID,))
                        db.commit()
                        return True
        except psycopg2.Error as e:
            db.rollback()
            print(f"Error inserting user: {e}")
            return False

    @staticmethod
    def setTimezone(anID: int, aTimezone: str) -> Optional[bool]:
        if not Account.is_a_timezone(aTimezone):
            print(f"Error updating user timezone: timezone not supported")
            return False
        try:
            with PostgreSQLDB() as db:
                with db.cursor() as cursor:
                    cursor.execute("UPDATE account SET timezone = %s WHERE user_id = %s", (aTimezone, anID))
                    db.commit()
                    return True
        except psycopg2.Error as e:
            db.rollback()
            print(f"Error updating user timezone: {e}")
            return False

    @staticmethod
    def getAccountByID(anID: int) -> Optional[Tuple]:
        try:
            with PostgreSQLDB() as db:
                with db.cursor() as cursor:
                    cursor.execute("SELECT * FROM account WHERE user_id = %s", (anID,))
                    return cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Error getting account: {e}")
            return None
