INSERT INTO orders (
    order_number,
    inventory_id,
    quantity_ordered,
    unit_price,
    status
)
SELECT
    'ORD-001',
    inventory.id,
    2,
    inventory.price,
    'paid'
FROM inventory
WHERE inventory.sku = 'SKU001'
ON CONFLICT (order_number) DO UPDATE
SET
    inventory_id = EXCLUDED.inventory_id,
    quantity_ordered = EXCLUDED.quantity_ordered,
    unit_price = EXCLUDED.unit_price,
    status = EXCLUDED.status,
    updated_at = CURRENT_TIMESTAMP;

INSERT INTO orders (
    order_number,
    inventory_id,
    quantity_ordered,
    unit_price,
    status
)
SELECT
    'ORD-002',
    inventory.id,
    5,
    inventory.price,
    'pending'
FROM inventory
WHERE inventory.sku = 'SKU002'
ON CONFLICT (order_number) DO UPDATE
SET
    inventory_id = EXCLUDED.inventory_id,
    quantity_ordered = EXCLUDED.quantity_ordered,
    unit_price = EXCLUDED.unit_price,
    status = EXCLUDED.status,
    updated_at = CURRENT_TIMESTAMP;
