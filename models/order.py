from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class Order:
    id: int
    order_number: str
    customer_id: int | None
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
            customer_id=row[2],
            inventory_id=row[3],
            quantity_ordered=row[4],
            unit_price=row[5],
            status=row[6],
            created_at=row[7],
            updated_at=row[8],
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


@dataclass(frozen=True)
class OrderWithDetails:
    id: int
    order_number: str
    customer_id: int | None
    customer_code: str | None
    customer_name: str | None
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
    def from_row(cls, row: tuple | None) -> "OrderWithDetails | None":
        if row is None:
            return None

        return cls(
            id=row[0],
            order_number=row[1],
            customer_id=row[2],
            customer_code=row[3],
            customer_name=row[4],
            inventory_id=row[5],
            inventory_sku=row[6],
            inventory_name=row[7],
            quantity_ordered=row[8],
            unit_price=row[9],
            status=row[10],
            created_at=row[11],
            updated_at=row[12],
        )
