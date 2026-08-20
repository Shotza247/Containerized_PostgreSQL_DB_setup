from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Vendor:
    id: int
    vendor_code: str
    name: str
    email: str
    phone: str | None
    city: str | None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_row(cls, row: tuple | None) -> "Vendor | None":
        if row is None:
            return None

        return cls(
            id=row[0],
            vendor_code=row[1],
            name=row[2],
            email=row[3],
            phone=row[4],
            city=row[5],
            created_at=row[6],
            updated_at=row[7],
        )
