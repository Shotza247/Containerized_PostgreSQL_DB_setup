UPDATE inventory
SET
    name = 'Gaming Laptop',
    quantity = 25,
    price = 47000.00,
    description = 'Updated from a reusable SQL update script.',
    updated_at = CURRENT_TIMESTAMP
WHERE sku = 'SKU001';
