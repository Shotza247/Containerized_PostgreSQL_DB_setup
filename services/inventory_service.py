from DB_SetUp import PostgresDB
from models.inventory import InventoryItem
from repository import inventory_repo


class InventoryService:
    def __init__(self, db: PostgresDB | None = None) -> None:
        self.db = db or PostgresDB()

    def create_item(
        self,
        sku: str,
        name: str,
        quantity: int,
        price,
        description: str | None = None,
    ) -> InventoryItem:
        self._validate_item(sku, name, quantity, price)

        with self.db.connection() as connection:
            item_id = inventory_repo.create_item(
                connection,
                sku,
                name,
                quantity,
                price,
                description,
            )
            item = inventory_repo.get_item_by_id(connection, item_id)

        return item

    def get_item_by_id(self, item_id: int) -> InventoryItem | None:
        with self.db.connection() as connection:
            return inventory_repo.get_item_by_id(connection, item_id)

    def get_item_by_sku(self, sku: str) -> InventoryItem | None:
        with self.db.connection() as connection:
            return inventory_repo.get_item_by_sku(connection, sku)

    def list_items(self) -> list[InventoryItem]:
        with self.db.connection() as connection:
            return inventory_repo.list_items(connection)

    def search_items(self, keyword: str) -> list[InventoryItem]:
        with self.db.connection() as connection:
            return inventory_repo.search_items(connection, keyword)

    def update_item(
        self,
        item_id: int,
        sku: str,
        name: str,
        quantity: int,
        price,
        description: str | None = None,
    ) -> InventoryItem | None:
        self._validate_item(sku, name, quantity, price)

        with self.db.connection() as connection:
            updated = inventory_repo.update_item(
                connection,
                item_id,
                sku,
                name,
                quantity,
                price,
                description,
            )
            if not updated:
                return None

            return inventory_repo.get_item_by_id(connection, item_id)

    def delete_item(self, item_id: int) -> bool:
        with self.db.connection() as connection:
            return inventory_repo.delete_item(connection, item_id)

    def _validate_item(self, sku: str, name: str, quantity: int, price) -> None:
        if not sku.strip():
            raise ValueError("SKU is required.")
        if not name.strip():
            raise ValueError("Item name is required.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        if price < 0:
            raise ValueError("Price cannot be negative.")
