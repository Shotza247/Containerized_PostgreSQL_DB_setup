from DB_SetUp import PostgresDB
from models.order import Order, OrderWithDetails, OrderWithInventory
from repository import customers_repo, inventory_repo, orders_repo


class OrderService:
    def __init__(self, db: PostgresDB | None = None) -> None:
        self.db = db or PostgresDB()

    def place_order(
        self,
        order_number: str,
        customer_code: str,
        sku: str,
        quantity_ordered: int,
        status: str = "pending",
    ) -> Order:
        if not order_number.strip():
            raise ValueError("Order number is required.")
        if not customer_code.strip():
            raise ValueError("Customer code is required.")
        if quantity_ordered <= 0:
            raise ValueError("Order quantity must be greater than zero.")

        with self.db.connection() as connection:
            existing_order = orders_repo.get_order_by_number(connection, order_number)
            if existing_order:
                raise ValueError(f"Order already exists: {order_number}")

            customer = customers_repo.get_customer_by_code(connection, customer_code)
            if customer is None:
                raise ValueError(f"Customer not found for code: {customer_code}")

            item = inventory_repo.get_item_by_sku(connection, sku)
            if item is None:
                raise ValueError(f"Inventory item not found for SKU: {sku}")

            if item.quantity < quantity_ordered:
                raise ValueError(
                    f"Not enough stock for {sku}. "
                    f"Available: {item.quantity}, requested: {quantity_ordered}."
                )

            order_id = orders_repo.create_order(
                connection,
                order_number,
                customer.id,
                item.id,
                quantity_ordered,
                item.price,
                status,
            )

            stock_updated = inventory_repo.decrease_item_quantity(
                connection,
                item.id,
                quantity_ordered,
            )
            if not stock_updated:
                raise ValueError(f"Could not reserve stock for SKU: {sku}")

            order = orders_repo.get_order_by_id(connection, order_id)
            if order is None:
                raise RuntimeError(f"Order was created but could not be loaded: {order_id}")

            return order

    def get_order_by_id(self, order_id: int) -> Order | None:
        with self.db.connection() as connection:
            return orders_repo.get_order_by_id(connection, order_id)

    def get_order_by_number(self, order_number: str) -> Order | None:
        with self.db.connection() as connection:
            return orders_repo.get_order_by_number(connection, order_number)

    def list_orders(self) -> list[Order]:
        with self.db.connection() as connection:
            return orders_repo.list_orders(connection)

    def list_orders_with_inventory(self) -> list[OrderWithInventory]:
        with self.db.connection() as connection:
            return orders_repo.list_orders_with_inventory(connection)

    def list_orders_with_details(self) -> list[OrderWithDetails]:
        with self.db.connection() as connection:
            return orders_repo.list_orders_with_details(connection)

    def update_status(self, order_number: str, status: str) -> bool:
        if not status.strip():
            raise ValueError("Order status is required.")

        with self.db.connection() as connection:
            return orders_repo.update_order_status(connection, order_number, status)

    def delete_order(self, order_number: str) -> bool:
        with self.db.connection() as connection:
            return orders_repo.delete_order(connection, order_number)
