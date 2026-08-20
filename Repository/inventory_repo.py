from models.inventory import InventoryItem


INVENTORY_COLUMNS = """
    id,
    sku,
    name,
    quantity,
    price,
    description,
    vendor_id,
    created_at,
    updated_at
"""


def get_postgres_version(connection) -> str:
    with connection.cursor() as cursor:
        cursor.execute("SELECT version();")
        return cursor.fetchone()[0]


def create_item(
    connection,
    sku: str,
    name: str,
    quantity: int,
    price,
    description: str | None = None,
    vendor_id: int | None = None,
) -> int:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO inventory (
                sku,
                name,
                quantity,
                price,
                description,
                vendor_id
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
            """,
            (sku, name, quantity, price, description, vendor_id),
        )

        return cursor.fetchone()[0]


def get_item_by_id(connection, item_id: int) -> InventoryItem | None:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            SELECT
                {INVENTORY_COLUMNS}
            FROM inventory
            WHERE id = %s;
            """,
            (item_id,),
        )

        return InventoryItem.from_row(cursor.fetchone())


def get_item_by_sku(connection, sku: str) -> InventoryItem | None:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            SELECT
                {INVENTORY_COLUMNS}
            FROM inventory
            WHERE sku = %s;
            """,
            (sku,),
        )

        return InventoryItem.from_row(cursor.fetchone())


def list_items(connection) -> list[InventoryItem]:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            SELECT
                {INVENTORY_COLUMNS}
            FROM inventory
            ORDER BY id;
            """
        )

        return [InventoryItem.from_row(row) for row in cursor.fetchall()]


def search_items(connection, keyword: str) -> list[InventoryItem]:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            SELECT
                {INVENTORY_COLUMNS}
            FROM inventory
            WHERE
                name ILIKE %s
                OR sku ILIKE %s
                OR description ILIKE %s
            ORDER BY name;
            """,
            (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"),
        )

        return [InventoryItem.from_row(row) for row in cursor.fetchall()]


def update_item(
    connection,
    item_id: int,
    sku: str,
    name: str,
    quantity: int,
    price,
    description: str | None = None,
    vendor_id: int | None = None,
) -> bool:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE inventory
            SET
                sku = %s,
                name = %s,
                quantity = %s,
                price = %s,
                description = %s,
                vendor_id = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s;
            """,
            (
                sku,
                name,
                quantity,
                price,
                description,
                vendor_id,
                item_id,
            ),
        )

        return cursor.rowcount > 0


def decrease_item_quantity(connection, item_id: int, quantity: int) -> bool:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE inventory
            SET
                quantity = quantity - %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
              AND quantity >= %s;
            """,
            (quantity, item_id, quantity),
        )

        return cursor.rowcount > 0


def delete_item(connection, item_id: int) -> bool:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            DELETE FROM inventory
            WHERE id = %s;
            """,
            (item_id,),
        )

        return cursor.rowcount > 0
