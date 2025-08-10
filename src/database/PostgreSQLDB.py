import os
import logging
import psycopg
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()

DBUSER = os.getenv("DBUSER")
DBPASS = os.getenv("PASSWORD")
DBHOST = os.getenv("HOSTNAME2")
DBNAME = os.getenv("DBNAME") 


class PostgreSQLDB:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg.connect(
                user=DBUSER,
                password=DBPASS,
                host=DBHOST,
                dbname=DBNAME,
            )
        except psycopg.DatabaseError as e:
            logger.error(f"Error while connecting to database: {e}")

    def close(self):
        if self.connection:
            self.connection.close()

    def __enter__(self):
        self.connect()
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
