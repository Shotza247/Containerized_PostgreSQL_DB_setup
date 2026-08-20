from models.vendor import Vendor


VENDOR_COLUMNS = """
    id,
    vendor_code,
    name,
    email,
    phone,
    city,
    created_at,
    updated_at
"""


def create_vendor(
    connection,
    vendor_code: str,
    name: str,
    email: str,
    phone: str | None = None,
    city: str | None = None,
) -> int:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO vendors (
                vendor_code,
                name,
                email,
                phone,
                city
            )
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
            """,
            (vendor_code, name, email, phone, city),
        )

        return cursor.fetchone()[0]


def get_vendor_by_id(connection, vendor_id: int) -> Vendor | None:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            SELECT
                {VENDOR_COLUMNS}
            FROM vendors
            WHERE id = %s;
            """,
            (vendor_id,),
        )

        return Vendor.from_row(cursor.fetchone())


def get_vendor_by_code(connection, vendor_code: str) -> Vendor | None:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            SELECT
                {VENDOR_COLUMNS}
            FROM vendors
            WHERE vendor_code = %s;
            """,
            (vendor_code,),
        )

        return Vendor.from_row(cursor.fetchone())


def list_vendors(connection) -> list[Vendor]:
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            SELECT
                {VENDOR_COLUMNS}
            FROM vendors
            ORDER BY vendor_code;
            """
        )

        return [Vendor.from_row(row) for row in cursor.fetchall()]


def update_vendor(
    connection,
    vendor_code: str,
    name: str,
    email: str,
    phone: str | None = None,
    city: str | None = None,
) -> bool:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            UPDATE vendors
            SET
                name = %s,
                email = %s,
                phone = %s,
                city = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE vendor_code = %s;
            """,
            (name, email, phone, city, vendor_code),
        )

        return cursor.rowcount > 0


def delete_vendor(connection, vendor_code: str) -> bool:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            DELETE FROM vendors
            WHERE vendor_code = %s;
            """,
            (vendor_code,),
        )

        return cursor.rowcount > 0
