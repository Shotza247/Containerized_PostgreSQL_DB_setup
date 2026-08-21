# 2026-08-20 FastAPI Runtime And CRM/Vendor Expansion Audit

## Purpose

Document the expansion from an inventory/orders backend template into a more
realistic four-table application runtime with FastAPI endpoints.

## User Intent

The user wanted to add:

- a customer CRM table for people buying items
- a vendor table for people or companies supplying items
- FastAPI endpoints to test the application runtime path

The user explicitly chose not to add Streamlit, Kafka, or Flink yet. Streamlit
was documented as a future Template 2 project that will sit on top of this
FastAPI backend.

## Changes Made

### Database Schema

Added:

- `customers`
- `vendors`
- `inventory.vendor_id`
- `orders.customer_id`

Current relationship shape:

```text
vendors -> inventory -> orders -> customers
```

More precisely:

```text
vendors supplies inventory
customers places orders
orders references inventory
```

### Seed Data

Added:

- 40 generated customers
- 10 generated vendors

Updated:

- inventory seed now assigns each inventory item to a vendor
- order seed now assigns each order to a customer and inventory item

### Models

Added:

- `Customer`
- `Vendor`

Updated:

- `InventoryItem` includes `vendor_id`
- `Order` includes `customer_id`
- `OrderWithDetails` includes customer and inventory context

### Repositories

Added:

- `customers_repo.py`
- `vendors_repo.py`

Updated:

- `inventory_repo.py` can write/read `vendor_id`
- `orders_repo.py` can write/read `customer_id`
- `orders_repo.py` includes `list_orders_with_details()`

### Services

Added:

- `CustomerService`
- `VendorService`

Updated:

- `InventoryService` resolves `vendor_code` to `vendor_id`
- `OrderService` requires `customer_code`, resolves it to `customer_id`, checks
  stock, creates the order, and reduces inventory in one transaction

### FastAPI Runtime

Added:

- `api/main.py`
- `api/schemas.py`
- `api/__init__.py`

Endpoint groups:

- health
- customers
- vendors
- inventory
- orders

Runtime path being tested:

```text
FastAPI -> Services -> Repositories -> DB_SetUp.py -> PostgreSQL
```

### API Smoke Test

Added:

- `scripts/smoke_test_api.py`

The smoke test creates:

- one vendor
- one customer
- one inventory item connected to the vendor
- one order connected to the customer and inventory item

Then it reads order details back through the API.

### Future Template 2

Added:

- `docs/templates/TEMPLATE_2_STREAMLIT_DASHBOARD.md`

Decision:

Streamlit will be a separate template built on top of FastAPI, not mixed into
this backend template.

Future intended path:

```text
Streamlit Dashboard -> FastAPI API -> Services -> Repositories -> PostgreSQL
```

## Verification

Completed from the sandbox:

```powershell
python -m compileall api models repository services Postgres_SetUp.py
python Postgres_SetUp.py --help
```

Results:

- Python syntax compilation passed.
- CLI help still works.
- `requirements.txt` now includes `fastapi` and `uvicorn[standard]`.

Not completed from the sandbox:

- Live FastAPI import/run test.
- Live API smoke test.
- Live PostgreSQL seed execution.

Reason:

The sandbox Python did not have `fastapi` or `psycopg2`, and the project `.venv`
executable was blocked by Windows sandbox permissions. These should be tested
from the user's normal project terminal after running `pip install -r
requirements.txt`.

## Local Test Plan

Run from the project folder:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
docker compose up -d
py Postgres_SetUp.py init --with-seed
uvicorn api.main:app --reload
```

In a second terminal:

```powershell
py scripts/smoke_test_api.py
```

## Design Decisions

- Customers and vendors were added before Kafka/Flink because they deepen the
  domain model without adding streaming infrastructure complexity.
- FastAPI was added before Streamlit because the backend runtime path should be
  verified before building a dashboard on top of it.
- Streamlit was documented as Template 2 to preserve the roadmap without
  expanding this template's scope.
- FastAPI routes call services, not repositories, to preserve the runtime
  architecture.
- Setup/admin commands can still use `DB_SetUp.py` directly.

## Next Steps

- Run the local test plan in a normal terminal.
- Confirm row counts for customers, vendors, inventory, and orders.
- Confirm `/docs` loads.
- Run the smoke test script.
- Add automated service tests after the endpoint smoke test passes.
