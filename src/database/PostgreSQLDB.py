import os
import logging
import psycopg
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()

# Database connection parameters from environment for security
DBUSER = os.getenv("DBUSER")
DBPASS = os.getenv("PASSWORD")
DBHOST = os.getenv("HOSTNAME2")
DBNAME = os.getenv("DBNAME")


class PostgreSQLDB:
    """
    Database connection wrapper with context manager support.
    Provides automatic connection cleanup and consistent error handling.
    """

    def __init__(self):
        self.connection = None

    def connect(self):
        """Establish database connection with centralized error handling"""
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
        """Safely close database connection if it exists"""
        if self.connection:
            self.connection.close()

    def __enter__(self):
        """Context manager entry: establish connection and return it for use"""
        self.connect()
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit: ensure connection is always closed"""
        self.close()
