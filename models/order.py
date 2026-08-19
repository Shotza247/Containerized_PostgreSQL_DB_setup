from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class Order:
    id: int
    order_number: str
    inventory_id: int
    quantity_ordered: int
    unit_price: Decimal
    status: str
    created_at: datetime
    updated_at: datetime

    @property
    def total_price(self) -> Decimal:
        return self.unit_price * self.quantity_ordered

    @classmethod
    def from_row(cls, row: tuple | None) -> "Order | None":
        if row is None:
            return None

        return cls(
            id=row[0],
            order_number=row[1],
            inventory_id=row[2],
            quantity_ordered=row[3],
            unit_price=row[4],
            status=row[5],
            created_at=row[6],
            updated_at=row[7],
        )


@dataclass(frozen=True)
class OrderWithInventory:
    id: int
    order_number: str
    inventory_id: int
    inventory_sku: str
    inventory_name: str
    quantity_ordered: int
    unit_price: Decimal
    status: str
    created_at: datetime
    updated_at: datetime

    @property
    def total_price(self) -> Decimal:
        return self.unit_price * self.quantity_ordered

    @classmethod
    def from_row(cls, row: tuple | None) -> "OrderWithInventory | None":
        if row is None:
            return None

        return cls(
            id=row[0],
            order_number=row[1],
            inventory_id=row[2],
            inventory_sku=row[3],
            inventory_name=row[4],
            quantity_ordered=row[5],
            unit_price=row[6],
            status=row[7],
            created_at=row[8],
            updated_at=row[9],
        )
