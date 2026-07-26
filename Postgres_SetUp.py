from utils.DB_SetUp import connect
from repository.inventory_repo import (
    get_postgres_version,
    create_item,
    get_item_by_id,
    get_item_by_sku,
    list_items,
    update_item,
    delete_item
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
    "SKU015",
    "Laptop",
    5,
    9999.99)
    logger.info("Inserted Item ID: %s", item_id)
    item_id = create_item(
        connection,
        "SKU001",
        "Laptop",
        10,
        15000.00
        )
    logger.info("Inserted Item ID: %s", item_id)
    
    #Get item by id
    item = get_item_by_id(connection, item_id)
    logger.info(item)
    item = get_item_by_id(connection, item_id)
    logger.info(item)
    
    
    #Read by sku
    item = get_item_by_sku(connection, "SKU001")
    logger.info(item)

    #list all items
    items = list_items(connection)
    logger.info(f"Postgres_Db_Items: {items}")
    
    #update inventory item
    updated = update_item(
    connection,
    item_id,
    "SKU001",
    "Gaming Laptop",
    25,
    47000.00
    )
    logger.info(f"Inventory item_id: {item_id} updated.")
    if updated:
        logger.info("Inventory updated successfully.")
    else:
        logger.warning("Item not found.")
    
    #delete inventory
    deleted = delete_item(connection, item_id)
    logger.info(f"Inventory item_id: {item_id} deleted.")
    
    if deleted:
        logger.info("Inventory deleted successfully.")
    else:
        logger.warning("Nothing was deleted.")\
    #check if delete worked
    item = get_item_by_id(connection, item_id)
    logger.info(item)
    

except Exception:
    connection.rollback()
    logger.exception("Application failed.")

finally:
    if connection:
        connection.close()
        logger.info("Connection closed.")