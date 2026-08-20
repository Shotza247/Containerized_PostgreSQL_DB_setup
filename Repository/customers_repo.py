from models.customer import Customer


CUSTOMER_COLUMNS = """
    id,
    customer_code,
    first_name,
    last_name,
    email,
    phone,
    city,
    created_at,
    updated_at
"""


def create_customer(
    connection,
    customer_code: str,
    first_name: str,
    last_name: str,
    email: str,
    phone: str | None = None,
    city: str | None = None,
) -> int:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO customers (
                customer_code,
                first_name,
                last_name,
                email,
                phone,
                city
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
            """,
            (customer_code, first_name, last_name, email, phone, city),
        )

        return cursor.fetchone()[0]


def get_customer_by_id(connection, customer_id: int) -> Customer | None:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            SELECT
                {CUSTOMER_COLUMNS}
            FROM customers
            WHERE id = %s;
            """,
            (customer_id,),
        )

        return Customer.from_row(cursor.fetchone())


def get_customer_by_code(connection, customer_code: str) -> Customer | None:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            SELECT
                {CUSTOMER_COLUMNS}
            FROM customers
            WHERE customer_code = %s;
            """,
            (customer_code,),
        )

        return Customer.from_row(cursor.fetchone())


def list_customers(connection) -> list[Customer]:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            SELECT
                {CUSTOMER_COLUMNS}
            FROM customers
            ORDER BY customer_code;
            """
        )

        return [Customer.from_row(row) for row in cursor.fetchall()]


def update_customer(
    connection,
    customer_code: str,
    first_name: str,
    last_name: str,
    email: str,
    phone: str | None = None,
    city: str | None = None,
) -> bool:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE customers
            SET
                first_name = %s,
                last_name = %s,
                email = %s,
                phone = %s,
                city = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE customer_code = %s;
            """,
            (first_name, last_name, email, phone, city, customer_code),
        )

        return cursor.rowcount > 0


def delete_customer(connection, customer_code: str) -> bool:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            DELETE FROM customers
            WHERE customer_code = %s;
            """,
            (customer_code,),
        )

        return cursor.rowcount > 0
