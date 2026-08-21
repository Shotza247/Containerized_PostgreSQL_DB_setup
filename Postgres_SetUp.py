import argparse
from datetime import datetime

from logging_config import logger


def run_inventory_demo() -> None:
    from services.customers_service import CustomerService
    from services.inventory_service import InventoryService
    from services.orders_service import OrderService
    from services.vendors_service import VendorService

    customer_service = CustomerService()
    inventory_service = InventoryService()
    order_service = OrderService()
    vendor_service = VendorService()
    demo_suffix = datetime.now().strftime("%Y%m%d%H%M%S")
    customer_code = f"CUS-DEMO-{demo_suffix}"
    vendor_code = f"VEN-DEMO-{demo_suffix}"
    sku = f"DEMO-{demo_suffix}"
    order_number = f"ORD-DEMO-{demo_suffix}"

    vendor = vendor_service.create_vendor(
        vendor_code=vendor_code,
        name="Demo Vendor",
        email=f"vendor-{demo_suffix}@example.com",
        phone="+27-11-000-0000",
        city="Johannesburg",
    )
    logger.info("Created vendor: %s", vendor)

    customer = customer_service.create_customer(
        customer_code=customer_code,
        first_name="Demo",
        last_name="Customer",
        email=f"customer-{demo_suffix}@example.com",
        phone="+27-10-000-0000",
        city="Cape Town",
    )
    logger.info("Created customer: %s", customer)

    item = inventory_service.create_item(
        sku=sku,
        name="Demo Laptop",
        quantity=5,
        price=9999.99,
        description="Created by the service-layer demo.",
        vendor_code=vendor_code,
    )
    logger.info("Created inventory item: %s", item)

    updated_item = inventory_service.update_item(
        item_id=item.id,
        sku=sku,
        name="Demo Gaming Laptop",
        quantity=10,
        price=12999.99,
        description="Updated by the service-layer demo.",
        vendor_code=vendor_code,
    )
    logger.info("Updated inventory item: %s", updated_item)

    order = order_service.place_order(
        order_number=order_number,
        customer_code=customer_code,
        sku=sku,
        quantity_ordered=2,
        status="paid",
    )
    logger.info("Created order: %s", order)

    orders = order_service.list_orders_with_details()
    logger.info("Orders with details: %s", orders)

    order_deleted = order_service.delete_order(order_number)
    logger.info("Deleted demo order: %s", order_deleted)

    item_deleted = inventory_service.delete_item(item.id)
    logger.info("Deleted demo inventory item: %s", item_deleted)

    customer_deleted = customer_service.delete_customer(customer_code)
    logger.info("Deleted demo customer: %s", customer_deleted)

    vendor_deleted = vendor_service.delete_vendor(vendor_code)
    logger.info("Deleted demo vendor: %s", vendor_deleted)


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
    subparsers.add_parser("demo", help="Run the sample inventory/order service flow.")

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
