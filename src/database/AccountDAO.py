import psycopg2

from typing import Optional, Tuple
from src.database.PostgreSQLDB import PostgreSQLDB
from src.models.Account import Account

class AccountDAO:
    @staticmethod
    def addAccount(anID: int) -> Optional[bool]:
        with PostgreSQLDB() as db:
            cursor = db.cursor()

            try:
                cursor.execute("INSERT INTO account (user_id) VALUES (%s)", (anID,))
                db.commit()
                return True
            except psycopg2.Error as e:
                db.rollback()
                print(f"Error inserting user: {e}")
            finally:
                cursor.close()


    @staticmethod
    def setTimezone(anID: int, aTimezone: str) -> Optional[bool]:
        if Account.is_a_timezone(aTimezone):
            with PostgreSQLDB() as db:
                cursor = db.cursor()

                try:
                    cursor.execute("UPDATE account SET timezone = %s WHERE user_id = %s", (aTimezone, anID))
                    db.commit()
                    return True
                except psycopg2.Error as e:
                    db.rollback()
                    print(f"Error updating user timezone: {e}")
                finally:
                    cursor.close()
        else:
            print("Error updating user timezone: timezone not supported")
            return False

    @staticmethod
    def getAccountByID(anID: int) -> Optional[Tuple]:
        with PostgreSQLDB() as db:
            with db.cursor() as cursor:
                try:
                    cursor.execute("SELECT * FROM account WHERE user_id = %s", (anID,))
                    return cursor.fetchone()
                except psycopg2.Error as e:
                    print(f"Error getting account: {e}")
                    return None

# AccountDAO.addAccount(1000)
# AccountDAO.setTimezone(1000, "Europe/Paris")