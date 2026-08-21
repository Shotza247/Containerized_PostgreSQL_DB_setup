# Template 2: FastAPI-Fed Streamlit Dashboard

This is a future project template idea, not part of the current backend runtime
implementation.

## Purpose

Build a Streamlit dashboard project on top of the FastAPI backend from this
template.

The intended architecture is:

```text
Streamlit Dashboard -> FastAPI API -> Services -> Repositories -> PostgreSQL
```

Streamlit should not talk directly to the repositories or database in this
template family. It should behave like a real frontend/client and request data
from FastAPI.

## Possible Dashboard Views

- inventory table
- low-stock inventory alerts
- orders table with customer and inventory details
- customers list
- vendors list
- order status summary
- revenue by order status
- top ordered products
- vendor supplied item counts

## Not Included Yet

- Streamlit app files
- dashboard charts
- Kafka
- Flink
- real-time event streaming

Those belong to later templates once the backend API and runtime path are
verified.
