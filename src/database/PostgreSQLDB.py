import os

import psycopg2


class PostgreSQLDB:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                user=os.getenv("USERNAME"),
                password=os.getenv("PASSWORD"),
                host=os.getenv("HOSTNAME"),
                dbname=os.getenv("DBNAME")
            )
        except psycopg2.Error as e:
            print(f"Error connecting to database: {e}")

    def close(self):
        if self.connection:
            self.connection.close()

    def __enter__(self):
        self.connect()
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
