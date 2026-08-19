from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class InventoryItem:
    id: int
    sku: str
    name: str
    quantity: int
    price: Decimal
    description: str | None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_row(cls, row: tuple | None) -> "InventoryItem | None":
        if row is None:
            return None

        return cls(
            id=row[0],
            sku=row[1],
            name=row[2],
            quantity=row[3],
            price=row[4],
            description=row[5],
            created_at=row[6],
            updated_at=row[7],
        )
