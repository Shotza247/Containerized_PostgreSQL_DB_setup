import psycopg2

from utils.config import DB_CONFIG
from utils.logging_config import logger


def connect():
    connection = None
    cursor = None

    try:
        logger.info("Connecting to PostgreSQL...")

        connection = psycopg2.connect(**DB_CONFIG)

        logger.info("Connection successful.")

        return connection

    except Exception:
        logger.exception("Database operation failed.")

        if connection:
            connection.rollback()

        raise

    finally:
        if cursor:
            cursor.close()