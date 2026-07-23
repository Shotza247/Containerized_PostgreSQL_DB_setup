from DB_SetUp import connect
from DBOps import (
    get_postgres_version,
    create_test_table,
    insert_test_user,
)
from logging_config import logger

connection = None

try:
    connection = connect()

    version = get_postgres_version(connection)
    logger.info("Connected to PostgreSQL: %s", version)

    create_test_table(connection)
    logger.info("Table verified.")

    user_id = insert_test_user(connection, "Alice")
    logger.info("Inserted user with ID: %s", user_id)

except Exception:
    logger.exception("Application failed.")

finally:
    if connection:
        connection.close()
        logger.info("Connection closed.")