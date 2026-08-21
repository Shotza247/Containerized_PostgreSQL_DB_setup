from decimal import Decimal

from pydantic import BaseModel, Field


class CustomerCreate(BaseModel):
    customer_code: str = Field(..., min_length=1)
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=3)
    phone: str | None = None
    city: str | None = None


class CustomerUpdate(BaseModel):
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=3)
    phone: str | None = None
    city: str | None = None


class VendorCreate(BaseModel):
    vendor_code: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=3)
    phone: str | None = None
    city: str | None = None


class VendorUpdate(BaseModel):
    name: str = Field(..., min_length=1)
    email: str = Field(..., min_length=3)
    phone: str | None = None
    city: str | None = None


class InventoryCreate(BaseModel):
    sku: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    quantity: int = Field(..., ge=0)
    price: Decimal = Field(..., ge=0)
    description: str | None = None
    vendor_code: str | None = None


class InventoryUpdate(BaseModel):
    sku: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    quantity: int = Field(..., ge=0)
    price: Decimal = Field(..., ge=0)
    description: str | None = None
    vendor_code: str | None = None


class OrderCreate(BaseModel):
    order_number: str = Field(..., min_length=1)
    customer_code: str = Field(..., min_length=1)
    sku: str = Field(..., min_length=1)
    quantity_ordered: int = Field(..., gt=0)
    status: str = Field(default="pending", min_length=1)


class OrderStatusUpdate(BaseModel):
    status: str = Field(..., min_length=1)
