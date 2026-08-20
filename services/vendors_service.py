from DB_SetUp import PostgresDB
from models.vendor import Vendor
from repository import vendors_repo


class VendorService:
    def __init__(self, db: PostgresDB | None = None) -> None:
        self.db = db or PostgresDB()

    def create_vendor(
        self,
        vendor_code: str,
        name: str,
        email: str,
        phone: str | None = None,
        city: str | None = None,
    ) -> Vendor:
        self._validate_vendor(vendor_code, name, email)

        with self.db.connection() as connection:
            vendor_id = vendors_repo.create_vendor(
                connection,
                vendor_code,
                name,
                email,
                phone,
                city,
            )
            vendor = vendors_repo.get_vendor_by_id(connection, vendor_id)

        return vendor

    def get_vendor_by_code(self, vendor_code: str) -> Vendor | None:
        with self.db.connection() as connection:
            return vendors_repo.get_vendor_by_code(connection, vendor_code)

    def list_vendors(self) -> list[Vendor]:
        with self.db.connection() as connection:
            return vendors_repo.list_vendors(connection)

    def update_vendor(
        self,
        vendor_code: str,
        name: str,
        email: str,
        phone: str | None = None,
        city: str | None = None,
    ) -> Vendor | None:
        self._validate_vendor(vendor_code, name, email)

        with self.db.connection() as connection:
            updated = vendors_repo.update_vendor(
                connection,
                vendor_code,
                name,
                email,
                phone,
                city,
            )
            if not updated:
                return None

            return vendors_repo.get_vendor_by_code(connection, vendor_code)

    def delete_vendor(self, vendor_code: str) -> bool:
        with self.db.connection() as connection:
            return vendors_repo.delete_vendor(connection, vendor_code)

    def _validate_vendor(self, vendor_code: str, name: str, email: str) -> None:
        if not vendor_code.strip():
            raise ValueError("Vendor code is required.")
        if not name.strip():
            raise ValueError("Vendor name is required.")
        if "@" not in email:
            raise ValueError("A valid vendor email is required.")
