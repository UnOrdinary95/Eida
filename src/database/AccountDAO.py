import psycopg2

from src.database.PostgreSQLDB import PostgreSQLDB


# INSERT USER
with PostgreSQLDB() as db:
    cursor = db.cursor()

    try:
        cursor.execute("INSERT INTO account (user_id) VALUES (100)")
        db.commit()
    except psycopg2.Error as e:
        db.rollback()
        print(f"Error inserting user: {e}")
    finally:
        cursor.close()


# UPDATE USER TZ
with PostgreSQLDB() as db:
    cursor = db.cursor()

    try:
        cursor.execute("UPDATE account SET timezone = 'un timezone random' WHERE user_id = 100")
        db.commit()
    except psycopg2.Error as e:
        db.rollback()
        print(f"Error updating user timezone: {e}")
    finally:
        cursor.close()
