from dataclasses import asdict, is_dataclass

from fastapi import FastAPI, HTTPException, Query, status

from DB_SetUp import check_connection
from api.schemas import (
    CustomerCreate,
    CustomerUpdate,
    InventoryCreate,
    InventoryUpdate,
    OrderCreate,
    OrderStatusUpdate,
    VendorCreate,
    VendorUpdate,
)
from services.customers_service import CustomerService
from services.inventory_service import InventoryService
from services.orders_service import OrderService
from services.vendors_service import VendorService


app = FastAPI(
    title="PostgreSQL Data Project Template API",
    version="1.0.0",
)

customer_service = CustomerService()
inventory_service = InventoryService()
order_service = OrderService()
vendor_service = VendorService()


def serialize(value):
    if isinstance(value, list):
        return [serialize(item) for item in value]
    if is_dataclass(value):
        return asdict(value)
    return value


def payload_data(payload):
    if hasattr(payload, "model_dump"):
        return payload.model_dump()
    return payload.dict()


def bad_request(exc: ValueError) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(exc),
    )


@app.get("/")
def root():
    return {
        "name": "PostgreSQL Data Project Template API",
        "runtime_path": "FastAPI -> Services -> Repositories -> DB_SetUp.py -> PostgreSQL",
    }


@app.get("/health")
def health_check():
    try:
        version = check_connection()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc

    return {"status": "ok", "postgres_version": version}


@app.get("/customers")
def list_customers():
    return serialize(customer_service.list_customers())


@app.post("/customers", status_code=status.HTTP_201_CREATED)
def create_customer(payload: CustomerCreate):
    try:
        customer = customer_service.create_customer(**payload_data(payload))
    except ValueError as exc:
        raise bad_request(exc) from exc

    return serialize(customer)


@app.get("/customers/{customer_code}")
def get_customer(customer_code: str):
    customer = customer_service.get_customer_by_code(customer_code)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found.")

    return serialize(customer)


@app.put("/customers/{customer_code}")
def update_customer(customer_code: str, payload: CustomerUpdate):
    try:
        customer = customer_service.update_customer(
            customer_code=customer_code,
            **payload_data(payload),
        )
    except ValueError as exc:
        raise bad_request(exc) from exc

    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found.")

    return serialize(customer)


@app.delete("/customers/{customer_code}")
def delete_customer(customer_code: str):
    deleted = customer_service.delete_customer(customer_code)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found.")

    return {"deleted": True}


@app.get("/vendors")
def list_vendors():
    return serialize(vendor_service.list_vendors())


@app.post("/vendors", status_code=status.HTTP_201_CREATED)
def create_vendor(payload: VendorCreate):
    try:
        vendor = vendor_service.create_vendor(**payload_data(payload))
    except ValueError as exc:
        raise bad_request(exc) from exc

    return serialize(vendor)


@app.get("/vendors/{vendor_code}")
def get_vendor(vendor_code: str):
    vendor = vendor_service.get_vendor_by_code(vendor_code)
    if vendor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found.")

    return serialize(vendor)


@app.put("/vendors/{vendor_code}")
def update_vendor(vendor_code: str, payload: VendorUpdate):
    try:
        vendor = vendor_service.update_vendor(
            vendor_code=vendor_code,
            **payload_data(payload),
        )
    except ValueError as exc:
        raise bad_request(exc) from exc

    if vendor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found.")

    return serialize(vendor)


@app.delete("/vendors/{vendor_code}")
def delete_vendor(vendor_code: str):
    deleted = vendor_service.delete_vendor(vendor_code)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found.")

    return {"deleted": True}


@app.get("/inventory")
def list_inventory(q: str | None = Query(default=None)):
    if q:
        return serialize(inventory_service.search_items(q))

    return serialize(inventory_service.list_items())


@app.post("/inventory", status_code=status.HTTP_201_CREATED)
def create_inventory_item(payload: InventoryCreate):
    try:
        item = inventory_service.create_item(**payload_data(payload))
    except ValueError as exc:
        raise bad_request(exc) from exc

    return serialize(item)


@app.get("/inventory/{sku}")
def get_inventory_item(sku: str):
    item = inventory_service.get_item_by_sku(sku)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory item not found.")

    return serialize(item)


@app.put("/inventory/{item_id}")
def update_inventory_item(item_id: int, payload: InventoryUpdate):
    try:
        item = inventory_service.update_item(
            item_id=item_id,
            **payload_data(payload),
        )
    except ValueError as exc:
        raise bad_request(exc) from exc

    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory item not found.")

    return serialize(item)


@app.delete("/inventory/{item_id}")
def delete_inventory_item(item_id: int):
    deleted = inventory_service.delete_item(item_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory item not found.")

    return {"deleted": True}


@app.get("/orders")
def list_orders():
    return serialize(order_service.list_orders_with_details())


@app.post("/orders", status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreate):
    try:
        order = order_service.place_order(**payload_data(payload))
    except ValueError as exc:
        raise bad_request(exc) from exc

    return serialize(order)


@app.get("/orders/{order_number}")
def get_order(order_number: str):
    order = order_service.get_order_by_number(order_number)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found.")

    return serialize(order)


@app.patch("/orders/{order_number}/status")
def update_order_status(order_number: str, payload: OrderStatusUpdate):
    try:
        updated = order_service.update_status(order_number, payload.status)
    except ValueError as exc:
        raise bad_request(exc) from exc

    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found.")

    return serialize(order_service.get_order_by_number(order_number))


@app.delete("/orders/{order_number}")
def delete_order(order_number: str):
    deleted = order_service.delete_order(order_number)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found.")

    return {"deleted": True}
