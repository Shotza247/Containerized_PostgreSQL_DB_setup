from models.order import Order, OrderWithDetails, OrderWithInventory


ORDER_COLUMNS = """
    id,
    order_number,
    customer_id,
    inventory_id,
    quantity_ordered,
    unit_price,
    status,
    created_at,
    updated_at
"""


def create_order(
    connection,
    order_number: str,
    customer_id: int | None,
    inventory_id: int,
    quantity_ordered: int,
    unit_price,
    status: str = "pending",
) -> int:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO orders (
                order_number,
                customer_id,
                inventory_id,
                quantity_ordered,
                unit_price,
                status
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
            """,
            (
                order_number,
                customer_id,
                inventory_id,
                quantity_ordered,
                unit_price,
                status,
            ),
        )

        return cursor.fetchone()[0]


def get_order_by_id(connection, order_id: int) -> Order | None:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            SELECT
                {ORDER_COLUMNS}
            FROM orders
            WHERE id = %s;
            """,
            (order_id,),
        )

        return Order.from_row(cursor.fetchone())


def get_order_by_number(connection, order_number: str) -> Order | None:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            SELECT
                {ORDER_COLUMNS}
            FROM orders
            WHERE order_number = %s;
            """,
            (order_number,),
        )

        return Order.from_row(cursor.fetchone())


def list_orders(connection) -> list[Order]:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            SELECT
                {ORDER_COLUMNS}
            FROM orders
            ORDER BY id;
            """
        )

        return [Order.from_row(row) for row in cursor.fetchall()]


def list_orders_with_inventory(connection) -> list[OrderWithInventory]:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                orders.id,
                orders.order_number,
                orders.inventory_id,
                inventory.sku,
                inventory.name,
                orders.quantity_ordered,
                orders.unit_price,
                orders.status,
                orders.created_at,
                orders.updated_at
            FROM orders
            JOIN inventory ON inventory.id = orders.inventory_id
            ORDER BY orders.order_number;
            """
        )

        return [OrderWithInventory.from_row(row) for row in cursor.fetchall()]


def list_orders_with_details(connection) -> list[OrderWithDetails]:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                orders.id,
                orders.order_number,
                orders.customer_id,
                customers.customer_code,
                customers.first_name || ' ' || customers.last_name AS customer_name,
                orders.inventory_id,
                inventory.sku,
                inventory.name,
                orders.quantity_ordered,
                orders.unit_price,
                orders.status,
                orders.created_at,
                orders.updated_at
            FROM orders
            JOIN inventory ON inventory.id = orders.inventory_id
            LEFT JOIN customers ON customers.id = orders.customer_id
            ORDER BY orders.order_number;
            """
        )

        return [OrderWithDetails.from_row(row) for row in cursor.fetchall()]


def update_order_status(connection, order_number: str, status: str) -> bool:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE orders
            SET
                status = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE order_number = %s;
            """,
            (status, order_number),
        )

        return cursor.rowcount > 0


def delete_order(connection, order_number: str) -> bool:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            DELETE FROM orders
            WHERE order_number = %s;
            """,
            (order_number,),
        )

        return cursor.rowcount > 0
