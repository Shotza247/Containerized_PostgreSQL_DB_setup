def get_postgres_version(connection):
    cursor = connection.cursor()

    cursor.execute("SELECT version();")

    version = cursor.fetchone()[0]

    cursor.close()

    return version

    
def create_item(connection, sku, name, quantity, price):
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO Inventory (
            sku,
            name,
            quantity,
            price
        )
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """,
        (sku, name, quantity, price)
    )

    item_id = cursor.fetchone()[0]

    connection.commit()
    cursor.close()

    return item_id

def get_item_by_id(connection, item_id):
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            sku,
            name,
            quantity,
            price,
            created_at,
            updated_at
        FROM Inventory
        WHERE id = %s;
        """,
        (item_id,)
    )

    item = cursor.fetchone()

    cursor.close()

    return item

def get_item_by_sku(connection, sku):
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            sku,
            name,
            quantity,
            price,
            created_at,
            updated_at
        FROM Inventory
        WHERE sku = %s;
        """,
        (sku,)
    )

    item = cursor.fetchone()

    cursor.close()

    return item

def list_items(connection):
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            sku,
            name,
            quantity,
            price,
            created_at,
            updated_at
        FROM Inventory
        ORDER BY id;
        """
    )

    items = cursor.fetchall()

    cursor.close()

    return items

def search_items(connection, keyword):
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            sku,
            name,
            quantity,
            price,
            created_at,
            updated_at
        FROM Inventory
        WHERE
            name ILIKE %s
            OR sku ILIKE %s
        ORDER BY name;
        """,
        (f"%{keyword}%", f"%{keyword}%")
    )

    items = cursor.fetchall()

    cursor.close()

    return items

def update_item(connection, item_id, sku, name, quantity, price):
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE Inventory
        SET
            sku = %s,
            name = %s,
            quantity = %s,
            price = %s,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = %s;
        """,
        (
            sku,
            name,
            quantity,
            price,
            item_id
        )
    )

    connection.commit()

    cursor.close()
    
def delete_item(connection, item_id):
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM Inventory
        WHERE id = %s;
        """,
        (item_id,)
    )

    connection.commit()

    cursor.close()