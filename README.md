# Reusable PostgreSQL Setup

This project gives you a small PostgreSQL setup you can run locally or embed in
another Python codebase.

## What is included

- `docker-compose.yml` starts a local PostgreSQL container.
- `.env.example` shows the database environment variables the app expects.
- `config.py` loads and validates database settings.
- `DB_SetUp.py` exposes reusable connection and setup helpers.
- `Postgres_SetUp.py` provides a command-line interface for common setup tasks.
- `database/schema/*.sql` contains schema files, run in filename order.
- `database/seed/*.sql` contains seed files, run in filename order.
- `database/dev/*.sql` contains local-only reset scripts.

## Quick Start

Create your local environment file:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and set a real password.

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

Create the schema:

```powershell
py Postgres_SetUp.py init
```

Create the schema and seed data:

```powershell
py Postgres_SetUp.py init --with-seed
```

Run only seed scripts:

```powershell
py Postgres_SetUp.py seed
```

Run the example inventory CRUD flow:

```powershell
py Postgres_SetUp.py demo
```

Reset the local inventory table:

```powershell
py Postgres_SetUp.py reset
```

## Embed In Another Codebase

Copy these pieces into the target project:

- `DB_SetUp.py`
- `config.py`
- `logging_config.py`
- `database/`
- `.env.example`
- the dependencies from `requirements.txt`

Then use the connection helper:

```python
from DB_SetUp import get_connection


with get_connection() as connection:
    with connection.cursor() as cursor:
        cursor.execute("SELECT version();")
        print(cursor.fetchone()[0])
```

Or initialize the database from application startup or a deployment script:

```python
from DB_SetUp import initialize_database


initialize_database(with_seed=True)
```

For code that wants to manage commits manually, use the raw connection helper:

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

## Add Your Own Tables

Add schema files to `database/schema` with numeric prefixes:

```text
001_create_inventory_table.sql
002_create_customers_table.sql
003_create_orders_table.sql
```

Add repeatable seed scripts to `database/seed`. Prefer `ON CONFLICT` in seed
files so they can run safely more than once.

## Useful Docker Commands

```powershell
docker compose ps
docker compose logs postgres
docker compose stop
docker compose start
docker compose down
```

To remove the database volume and all local data:

```powershell
docker compose down -v
```
