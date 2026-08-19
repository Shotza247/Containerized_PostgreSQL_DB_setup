INSERT INTO inventory (sku, name, quantity, price)
VALUES
    ('SKU001', 'Laptop', 10, 15000.00),
    ('SKU002', 'Mouse', 50, 250.00),
    ('SKU003', 'Keyboard', 25, 750.00)
ON CONFLICT (sku) DO UPDATE
SET
    name = EXCLUDED.name,
    quantity = EXCLUDED.quantity,
    price = EXCLUDED.price,
    updated_at = CURRENT_TIMESTAMP;
