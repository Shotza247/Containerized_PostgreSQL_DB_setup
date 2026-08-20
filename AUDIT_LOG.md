# Project Audit Log

This file tracks the growth of the PostgreSQL data project template: decisions,
implementation changes, verification results, and the reasoning behind each
stage of the build.

Use this log as the project memory. Each meaningful development step should add
a new dated audit entry under `docs/audits/`.

## Audit Entries

| Date | Entry | Focus |
| --- | --- | --- |
| 2026-08-19 | [Project Development Audit](docs/audits/2026-08-19_project_development_audit.md) | Reusable PostgreSQL template, inventory/orders schema, services, repositories, models, seed data, diagrams, and README evolution. |
| 2026-08-20 | [FastAPI Runtime And CRM/Vendor Expansion Audit](docs/audits/2026-08-20_fastapi_runtime_crm_vendor_audit.md) | Customers/vendors schema, four-table domain model, FastAPI endpoints, API smoke test script, and Template 2 Streamlit planning note. |

## Current Architecture Rule

Normal application workflows should follow this path:

```text
Application Code -> Services -> Repositories -> DB_SetUp.py -> PostgreSQL
```

Setup and admin workflows can use `DB_SetUp.py` directly:

```text
Postgres_SetUp.py CLI -> DB_SetUp.py -> schema/seed/dev SQL -> PostgreSQL
```

## Future Audit Practice

Create a new audit entry when one of these happens:

- the database schema changes
- seed data changes
- service, repository, or model behavior changes
- architecture diagrams or project structure changes
- a bug is discovered, fixed, or intentionally deferred
- a design decision changes direction
- the project moves from template/demo toward a real application

Use [AUDIT_TEMPLATE.md](docs/audits/AUDIT_TEMPLATE.md) for future entries.
