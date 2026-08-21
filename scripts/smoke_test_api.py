import json
from datetime import datetime
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


BASE_URL = "http://127.0.0.1:8000"


def request(method: str, path: str, payload: dict | None = None):
    data = None
    headers = {"Content-Type": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")

    req = Request(
        f"{BASE_URL}{path}",
        data=data,
        headers=headers,
        method=method,
    )

    try:
        with urlopen(req, timeout=10) as response:
            body = response.read().decode("utf-8")
            return response.status, json.loads(body) if body else None
    except HTTPError as exc:
        body = exc.read().decode("utf-8")
        raise RuntimeError(f"{method} {path} failed: {exc.code} {body}") from exc
    except URLError as exc:
        raise RuntimeError(
            f"Could not reach API at {BASE_URL}. Start it with: uvicorn api.main:app --reload"
        ) from exc


def main() -> int:
    suffix = datetime.now().strftime("%Y%m%d%H%M%S")
    vendor_code = f"VEN-API-{suffix}"
    customer_code = f"CUS-API-{suffix}"
    sku = f"SKU-API-{suffix}"
    order_number = f"ORD-API-{suffix}"

    status, _ = request("GET", "/")
    print(f"PASS GET / -> {status}")

    status, _ = request("GET", "/health")
    print(f"PASS GET /health -> {status}")

    status, vendor = request(
        "POST",
        "/vendors",
        {
            "vendor_code": vendor_code,
            "name": "API Smoke Vendor",
            "email": f"vendor-{suffix}@example.com",
            "phone": "+27-11-555-0000",
            "city": "Johannesburg",
        },
    )
    print(f"PASS POST /vendors -> {status}")

    status, customer = request(
        "POST",
        "/customers",
        {
            "customer_code": customer_code,
            "first_name": "API",
            "last_name": "Smoke",
            "email": f"customer-{suffix}@example.com",
            "phone": "+27-10-555-0000",
            "city": "Cape Town",
        },
    )
    print(f"PASS POST /customers -> {status}")

    status, item = request(
        "POST",
        "/inventory",
        {
            "sku": sku,
            "name": "API Smoke Monitor",
            "quantity": 10,
            "price": "3500.00",
            "description": "Created by the FastAPI smoke test.",
            "vendor_code": vendor_code,
        },
    )
    print(f"PASS POST /inventory -> {status}")

    status, order = request(
        "POST",
        "/orders",
        {
            "order_number": order_number,
            "customer_code": customer_code,
            "sku": sku,
            "quantity_ordered": 2,
            "status": "paid",
        },
    )
    print(f"PASS POST /orders -> {status}")
    print(json.dumps(order, indent=2, default=str))

    status, _ = request("PATCH", f"/orders/{order_number}/status", {"status": "shipped"})
    print(f"PASS PATCH /orders/{order_number}/status -> {status}")

    status, _ = request("GET", f"/orders/{order_number}")
    print(f"PASS GET /orders/{order_number} -> {status}")

    status, _ = request("GET", "/orders")
    print(f"PASS GET /orders -> {status}")

    status, _ = request("DELETE", f"/orders/{order_number}")
    print(f"PASS DELETE /orders/{order_number} -> {status}")

    status, _ = request("DELETE", f"/inventory/{item['id']}")
    print(f"PASS DELETE /inventory/{item['id']} -> {status}")

    status, _ = request("DELETE", f"/customers/{customer['customer_code']}")
    print(f"PASS DELETE /customers/{customer['customer_code']} -> {status}")

    status, _ = request("DELETE", f"/vendors/{vendor['vendor_code']}")
    print(f"PASS DELETE /vendors/{vendor['vendor_code']} -> {status}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
