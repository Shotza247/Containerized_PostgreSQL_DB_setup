# PostgreSQL Data Project Template

This project is a reusable PostgreSQL starter template for local data projects,
backend services, experiments, and small applications that need a database setup
they can copy into another codebase.

The main goal is to make PostgreSQL easy to:

- start locally with Docker
- configure with environment variables
- initialize with ordered schema files
- seed with repeatable sample data
- reset during development
- use from Python code through a small reusable connection helper

## Project Structure

```text
PostgresSQl_setup/
  DB_SetUp.py
  Postgres_SetUp.py
  config.py
  logging_config.py
  docker-compose.yml
  .env.example
  requirements.txt
  database/
    schema/
      001_create_inventory_table.sql
      002_add_inventory_description_column.sql
      003_create_orders_table.sql
    seed/
      001_inventory_seed.sql
      002_orders_seed.sql
      003_update_inventory_item.sql
    dev/
      reset_inventory.sql
  repository/
    __init__.py
    inventory_repo.py
    orders_repo.py
  services/
    __init__.py
    inventory_service.py
    orders_service.py
  models/
    __init__.py
    inventory.py
    order.py
  utils/
```

## Core Template Files

These files are the reusable PostgreSQL template:

- `docker-compose.yml` starts PostgreSQL locally.
- `.env.example` documents required database variables.
- `config.py` loads `.env` values and validates database config.
- `logging_config.py` configures shared logging.
- `DB_SetUp.py` provides reusable Python database helpers.
- `Postgres_SetUp.py` provides command-line setup commands.
- `database/schema` stores ordered schema scripts.
- `database/seed` stores ordered seed and update scripts.
- `database/dev` stores local-only reset scripts.

## Implemented Sample App Layer

These folders are now set up as a working `inventory` and `orders` sample app.
They show how a real codebase can sit on top of the reusable PostgreSQL
template:

- `repository/` contains raw SQL data-access functions.
- `services/` contains business workflows and validation.
- `models/` contains Python representations of database objects.
- `utils/` is for small shared helpers.

For a pure database template, these folders are not strictly required. In this
project, they are intentionally included to demonstrate the recommended app
architecture.

## Quick Start

Create a local `.env` file:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and set your database password.

Create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Start PostgreSQL:

```powershell
docker compose up -d
```

Check the database connection:

```powershell
py Postgres_SetUp.py check
```

Create tables:

```powershell
py Postgres_SetUp.py init
```

Create tables and seed data:

```powershell
py Postgres_SetUp.py init --with-seed
```

Run seed scripts only:

```powershell
py Postgres_SetUp.py seed
```

Reset local development tables:

```powershell
py Postgres_SetUp.py reset
```

Run the example inventory/order service flow:

```powershell
py Postgres_SetUp.py demo
```

## Command Reference

| Command | Purpose |
| --- | --- |
| `py Postgres_SetUp.py check` | Tests the PostgreSQL connection. |
| `py Postgres_SetUp.py init` | Runs all files in `database/schema` in filename order. |
| `py Postgres_SetUp.py init --with-seed` | Runs schema files, then seed files. |
| `py Postgres_SetUp.py seed` | Runs all files in `database/seed` in filename order. |
| `py Postgres_SetUp.py reset` | Runs development reset scripts. |
| `py Postgres_SetUp.py demo` | Runs the implemented inventory/order service demo. |

## Template Blueprint

```mermaid
flowchart TD
    A[Developer] --> B[Postgres_SetUp.py CLI]
    A --> C[Application Code]

    subgraph Setup["Database Setup And Admin Path"]
        B --> D[DB_SetUp.py]
        D --> E[config.py]
        D --> F[database/schema/*.sql]
        D --> G[database/seed/*.sql]
        D --> H[database/dev/*.sql]
        I[docker-compose.yml] --> J[(PostgreSQL)]
        F --> J
        G --> J
        H --> J
        D --> J
    end

    subgraph Runtime["Application Runtime Path"]
        C --> K[services/]
        K --> L[repository/]
        L --> D
        K --> M[models/]
    end
```

The setup/admin path can use `DB_SetUp.py` directly because commands like
`init`, `seed`, and `reset` are database lifecycle tasks. The application
runtime path should go through `services/` first, then `repository/`, then
`DB_SetUp.py`.

## Database Blueprint

```mermaid
erDiagram
    INVENTORY ||--o{ ORDERS : "has orders"

    INVENTORY {
        int id PK
        varchar sku UK
        varchar name
        int quantity
        numeric price
        text description
        timestamp created_at
        timestamp updated_at
    }

    ORDERS {
        int id PK
        varchar order_number UK
        int inventory_id FK
        int quantity_ordered
        numeric unit_price
        varchar status
        timestamp created_at
        timestamp updated_at
    }
```

## SQL File Pattern

Schema files should be additive and ordered:

```text
001_create_inventory_table.sql
002_add_inventory_description_column.sql
003_create_orders_table.sql
```

Seed files should also be ordered:

```text
001_inventory_seed.sql
002_orders_seed.sql
003_update_inventory_item.sql
```

The current seed setup creates:

- 75 inventory items
- 120 orders connected to inventory items
- 1 follow-up inventory item update for `SKU001`

Prefer repeatable SQL when possible:

- Use `CREATE TABLE IF NOT EXISTS`.
- Use `ADD COLUMN IF NOT EXISTS`.
- Use `ON CONFLICT` for seed data.
- Use stable lookup columns like `sku` or `order_number`.

## Current Tables

### `inventory`

Stores products or stock items.

Important columns:

- `id`: primary key
- `sku`: unique item code
- `name`: item name
- `quantity`: available stock
- `price`: item price
- `description`: optional item description
- `created_at`: row creation timestamp
- `updated_at`: row update timestamp

### `orders`

Stores orders connected to inventory items.

Important columns:

- `id`: primary key
- `order_number`: unique order code
- `inventory_id`: foreign key to `inventory(id)`
- `quantity_ordered`: number of units ordered
- `unit_price`: price used on the order
- `status`: order state
- `created_at`: row creation timestamp
- `updated_at`: row update timestamp

## Example Join Query

Use this to check that orders are connected to inventory:

```sql
SELECT
    orders.order_number,
    inventory.sku,
    inventory.name,
    orders.quantity_ordered,
    orders.unit_price,
    orders.status
FROM orders
JOIN inventory ON inventory.id = orders.inventory_id
ORDER BY orders.order_number;
```

Check the seed counts:

```sql
SELECT COUNT(*) AS inventory_count FROM inventory;
SELECT COUNT(*) AS order_count FROM orders;
```

## Use In Python

For normal application workflows, use the service layer first. Use `DB_SetUp.py`
directly for setup scripts, health checks, one-off admin tasks, or low-level
database utilities.

Use the managed connection helper when you want automatic commit, rollback, and
close behavior:

```python
from DB_SetUp import get_connection


with get_connection() as connection:
    with connection.cursor() as cursor:
        cursor.execute("SELECT version();")
        print(cursor.fetchone()[0])
```

Initialize the database from another script:

```python
from DB_SetUp import initialize_database


initialize_database(with_seed=True)
```

Use the raw connection helper when your code wants to control transactions:

```python
from DB_SetUp import connect


connection = connect()
try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1;")
    connection.commit()
finally:
    connection.close()
```

## Repository, Service, And Models

The implemented sample app layer follows this responsibility split:

```mermaid
flowchart LR
    A[Route, CLI, Notebook, or App] --> B[Service Layer]
    B --> C[Repository Layer]
    C --> D[DB_SetUp.py]
    D --> E[(PostgreSQL)]
    B --> F[Models]
    C --> F
```

### Repository

Repository files should contain database access only:

- SQL queries
- inserts
- updates
- deletes
- row fetching
- transaction-safe database operations

Example:

```text
repository/inventory_repo.py
repository/orders_repo.py
```

Current repository responsibilities:

- `inventory_repo.py` handles item CRUD, item lookup, item search, and stock quantity updates.
- `orders_repo.py` handles order CRUD, order lookup, status updates, and order/inventory joins.

Repositories should not call `commit()` or `rollback()` directly. The service
or database helper owns transactions so multi-step workflows can succeed or
fail as one unit.

### Service

Service files should contain business rules:

- check whether inventory has enough stock
- create an order and reduce inventory in one transaction
- validate inputs before calling repository functions
- coordinate multiple repositories

Example:

```text
services/inventory_service.py
services/orders_service.py
```

Current service responsibilities:

- `InventoryService` validates item input and wraps inventory repository calls.
- `OrderService` places orders, checks stock, creates the order, and reduces inventory in one transaction.

### Models

Model files should contain Python representations of data:

```python
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class InventoryItem:
    id: int
    sku: str
    name: str
    quantity: int
    price: Decimal
    description: str | None
    created_at: datetime
    updated_at: datetime
```

Models are part of the sample app layer and make repository/service return
values easier to understand than raw tuples.

Current models:

- `InventoryItem`
- `Order`
- `OrderWithInventory`

## Service Usage Example

Use services from application code instead of calling repositories directly:

```python
from services.inventory_service import InventoryService
from services.orders_service import OrderService


inventory_service = InventoryService()
order_service = OrderService()

item = inventory_service.create_item(
    sku="SKU100",
    name="Monitor",
    quantity=12,
    price=3500.00,
    description="27 inch display",
)

order = order_service.place_order(
    order_number="ORD-100",
    sku=item.sku,
    quantity_ordered=2,
    status="paid",
)

print(order.total_price)
```

## Project Audits

Project development is tracked in [AUDIT_LOG.md](AUDIT_LOG.md).

Use the audit trail to document:

- schema changes
- seed data changes
- service, repository, and model changes
- architecture decisions
- README and diagram changes
- bugs, fixes, and verification results
- ideation growth and co-creation notes

Current audit entries live in `docs/audits/`. Use
`docs/audits/AUDIT_TEMPLATE.md` when adding a new audit entry.

## Docker Commands

```powershell
docker compose ps
docker compose logs postgres
docker compose stop
docker compose start
docker compose down
```

Remove the database volume and all local data:

```powershell
docker compose down -v
```

## Reusing This Template

To embed only the core PostgreSQL template into another Python project, copy:

- `DB_SetUp.py`
- `config.py`
- `logging_config.py`
- `database/`
- `.env.example`
- `docker-compose.yml`
- the dependencies from `requirements.txt`

To also include the sample app architecture, copy:

- `models/`
- `repository/`
- `services/`

Then replace or extend the sample `inventory` and `orders` domain with your
project's tables and workflows.
