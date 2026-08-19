import argparse

from logging_config import logger
from repository.inventory_repo import (
    create_item,
    delete_item,
    get_item_by_id,
    get_item_by_sku,
    get_postgres_version,
    list_items,
    update_item,
)


def run_inventory_demo() -> None:
    from DB_SetUp import PostgresDB

    db = PostgresDB()

    with db.connection() as connection:
        version = get_postgres_version(connection)
        logger.info("Connected to PostgreSQL: %s", version)

        item_id = create_item(
            connection,
            "SKU015",
            "Laptop",
            5,
            9999.99,
        )
        logger.info("Inserted item ID: %s", item_id)

        item = get_item_by_id(connection, item_id)
        logger.info("Item by ID: %s", item)

        item = get_item_by_sku(connection, "SKU015")
        logger.info("Item by SKU: %s", item)

        items = list_items(connection)
        logger.info("Inventory items: %s", items)

        updated = update_item(
            connection,
            item_id,
            "SKU015",
            "Gaming Laptop",
            25,
            47000.00,
        )
        logger.info("Inventory updated: %s", updated)

        deleted = delete_item(connection, item_id)
        logger.info("Inventory deleted: %s", deleted)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Reusable PostgreSQL setup utility.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("check", help="Verify that the database is reachable.")

    init_parser = subparsers.add_parser(
        "init",
        help="Run schema SQL files in database/schema.",
    )
    init_parser.add_argument(
        "--with-seed",
        action="store_true",
        help="Run seed SQL files after schema setup.",
    )

    subparsers.add_parser("seed", help="Run seed SQL files in database/seed.")
    subparsers.add_parser("reset", help="Run dev reset SQL files in database/dev.")
    subparsers.add_parser("demo", help="Run the inventory CRUD demo.")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    from DB_SetUp import PostgresDB, check_connection, initialize_database
    from config import DEV_DIR, SCHEMA_DIR, SEED_DIR

    db = PostgresDB()

    if args.command == "check":
        check_connection()
    elif args.command == "init":
        initialize_database(SCHEMA_DIR, SEED_DIR, with_seed=args.with_seed)
        logger.info("Database schema initialized.")
    elif args.command == "seed":
        db.seed(SEED_DIR)
        logger.info("Database seed scripts completed.")
    elif args.command == "reset":
        db.execute_directory(DEV_DIR)
        logger.info("Development reset scripts completed.")
    elif args.command == "demo":
        run_inventory_demo()
    else:
        parser.error(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
