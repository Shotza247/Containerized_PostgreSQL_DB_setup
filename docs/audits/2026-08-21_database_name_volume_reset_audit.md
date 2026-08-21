# 2026-08-21 Database Name Docker Volume Reset Audit

## Purpose

Document a setup issue discovered when changing the configured PostgreSQL
database name from the default `postgres` database to a project-specific name
such as `EcommerceStore`.

## User Intent

The user wanted future project users to know that changing `.env` database
variables, especially `DB_NAME`, may require resetting the Docker volume before
running:

```powershell
py Postgres_SetUp.py check
```

## Issue

The application attempted to connect to:

```text
localhost:5432/EcommerceStore
```

PostgreSQL returned:

```text
FATAL: database "EcommerceStore" does not exist
```

## Cause

The Postgres Docker image applies `POSTGRES_DB`, `POSTGRES_USER`, and
`POSTGRES_PASSWORD` during the first initialization of the database volume.

If a container/volume was first created with:

```text
DB_NAME=postgres
```

and the `.env` file is later changed to:

```text
DB_NAME=EcommerceStore
```

the existing Docker volume is not automatically recreated and the new database
is not automatically created.

## Chosen Fix Documented

Only the reset-volume option was added to the README Quick Start section:

```powershell
docker compose down -v
docker compose up -d
```

This intentionally omits the manual SQL `CREATE DATABASE` option because the
preferred template path is simpler for local development and easier for future
users to follow.

## Files Updated

- `README.md`
- `AUDIT_LOG.md`
- `docs/audits/2026-08-21_database_name_volume_reset_audit.md`

## Verification

Documentation placement was checked in the README Quick Start section before:

```powershell
py Postgres_SetUp.py check
```

No live Docker reset was performed by Codex.

## Future Reminder

When changing database identity values in `.env`, especially `DB_NAME`, treat
the Docker volume as part of the database state. If the volume already exists,
reset it before expecting the new database name to exist.
