INSERT INTO inventory (
    sku,
    name,
    quantity,
    price,
    description
)
SELECT
    'SKU' || LPAD(item_number::text, 3, '0') AS sku,
    CASE ((item_number - 1) % 12)
        WHEN 0 THEN 'Laptop'
        WHEN 1 THEN 'Mouse'
        WHEN 2 THEN 'Keyboard'
        WHEN 3 THEN 'Monitor'
        WHEN 4 THEN 'Docking Station'
        WHEN 5 THEN 'USB-C Hub'
        WHEN 6 THEN 'Webcam'
        WHEN 7 THEN 'Headset'
        WHEN 8 THEN 'External SSD'
        WHEN 9 THEN 'Router'
        WHEN 10 THEN 'Tablet'
        ELSE 'Printer'
    END || ' ' || LPAD(item_number::text, 3, '0') AS name,
    20 + ((item_number * 7) % 180) AS quantity,
    ROUND(
        (
            CASE ((item_number - 1) % 12)
                WHEN 0 THEN 15000.00
                WHEN 1 THEN 250.00
                WHEN 2 THEN 750.00
                WHEN 3 THEN 4200.00
                WHEN 4 THEN 1800.00
                WHEN 5 THEN 650.00
                WHEN 6 THEN 950.00
                WHEN 7 THEN 1200.00
                WHEN 8 THEN 2200.00
                WHEN 9 THEN 1600.00
                WHEN 10 THEN 8500.00
                ELSE 3200.00
            END
            + (item_number * 13.75)
        )::numeric,
        2
    ) AS price,
    'Seeded inventory item ' || LPAD(item_number::text, 3, '0') AS description
FROM generate_series(1, 75) AS seeded_items(item_number)
ON CONFLICT (sku) DO UPDATE
SET
    name = EXCLUDED.name,
    quantity = EXCLUDED.quantity,
    price = EXCLUDED.price,
    description = EXCLUDED.description,
    updated_at = CURRENT_TIMESTAMP;
