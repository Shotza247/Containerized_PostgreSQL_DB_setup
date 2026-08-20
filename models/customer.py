from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Customer:
    id: int
    customer_code: str
    first_name: str
    last_name: str
    email: str
    phone: str | None
    city: str | None
    created_at: datetime
    updated_at: datetime

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def from_row(cls, row: tuple | None) -> "Customer | None":
        if row is None:
            return None

        return cls(
            id=row[0],
            customer_code=row[1],
            first_name=row[2],
            last_name=row[3],
            email=row[4],
            phone=row[5],
            city=row[6],
            created_at=row[7],
            updated_at=row[8],
        )
