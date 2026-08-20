INSERT INTO orders (
    order_number,
    customer_id,
    inventory_id,
    quantity_ordered,
    unit_price,
    status
)
SELECT
    'ORD-' || LPAD(order_number::text, 3, '0') AS order_number,
    customers.id AS customer_id,
    inventory.id AS inventory_id,
    1 + ((order_number * 3) % 8) AS quantity_ordered,
    inventory.price AS unit_price,
    CASE (order_number % 5)
        WHEN 0 THEN 'cancelled'
        WHEN 1 THEN 'pending'
        WHEN 2 THEN 'paid'
        WHEN 3 THEN 'shipped'
        ELSE 'delivered'
    END AS status
FROM generate_series(1, 120) AS seeded_orders(order_number)
JOIN inventory
    ON inventory.sku = 'SKU' || LPAD((((order_number - 1) % 75) + 1)::text, 3, '0')
JOIN customers
    ON customers.customer_code = 'CUS-' || LPAD((((order_number - 1) % 40) + 1)::text, 3, '0')
ON CONFLICT (order_number) DO UPDATE
SET
    customer_id = EXCLUDED.customer_id,
    inventory_id = EXCLUDED.inventory_id,
    quantity_ordered = EXCLUDED.quantity_ordered,
    unit_price = EXCLUDED.unit_price,
    status = EXCLUDED.status,
    updated_at = CURRENT_TIMESTAMP;
