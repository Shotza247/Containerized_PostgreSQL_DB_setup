from utils.DB_SetUp import connect
from repository.inventory_repo import (
    get_postgres_version,
    create_item,
    get_item_by_id,
    get_item_by_sku,
    list_items,
)

from utils.logging_config import logger

connection = None

try:
    connection = connect()

    version = get_postgres_version(connection)
    logger.info("Connected to PostgreSQL: %s", version)

    #Verify the postgres version
    version = get_postgres_version(connection)
    logger.info(version)

    #Create a new item in the inventory
    item_id = create_item(
    connection,
    "SKU012",
    "Laptop",
    5,
    9999.99)
    logger.info("Inserted Item ID: %s", item_id)
    
    #Get item by id
    item = get_item_by_id(connection, item_id)
    logger.info(item)
    
    #Read by sku
    item = get_item_by_sku(connection, "SKU001")
    logger.info(item)

    #list all items
    items = list_items(connection)
    logger.info(items)

except Exception:
    connection.rollback()
    logger.exception("Application failed.")

finally:
    if connection:
        connection.close()
        logger.info("Connection closed.")