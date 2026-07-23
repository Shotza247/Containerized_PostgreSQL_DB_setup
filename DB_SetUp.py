import psycopg2

from config import DB_CONFIG
from logging_config import logger


def connect():
    connection = None
    cursor = None

    try:
        logger.info("Connecting to PostgreSQL...")

        connection = psycopg2.connect(**DB_CONFIG)

        logger.info("Connection successful.")

        # Create a cursor
        cursor = connection.cursor()

        # Check PostgreSQL version
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()

        logger.info("Connected to: %s", db_version[0])

        # Create a test table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) NOT NULL
            );
        """)

        logger.info("Verified table 'test_users' exists.")

        # Insert a test record
        cursor.execute(
            """
            INSERT INTO test_users (name)
            VALUES (%s)
            RETURNING id;
            """,
            ("Alice",)
        )

        user_id = cursor.fetchone()[0]

        logger.info("Inserted test user with ID: %s", user_id)

        connection.commit()

        return connection

    except Exception:
        logger.exception("Database operation failed.")

        if connection:
            connection.rollback()

        raise

    finally:
        if cursor:
            cursor.close()