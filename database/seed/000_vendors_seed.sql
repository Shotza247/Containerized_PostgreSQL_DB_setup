INSERT INTO vendors (
    vendor_code,
    name,
    email,
    phone,
    city
)
SELECT
    'VEN-' || LPAD(vendor_number::text, 3, '0') AS vendor_code,
    CASE ((vendor_number - 1) % 10)
        WHEN 0 THEN 'Northstar Supplies'
        WHEN 1 THEN 'Cape Digital Wholesale'
        WHEN 2 THEN 'Ubuntu Hardware Co'
        WHEN 3 THEN 'Vertex Office Tech'
        WHEN 4 THEN 'Summit Components'
        WHEN 5 THEN 'Metro Device Partners'
        WHEN 6 THEN 'Blue Peak Logistics'
        WHEN 7 THEN 'Nova Print Supply'
        WHEN 8 THEN 'Signal Network Goods'
        ELSE 'Prime Workspace Vendors'
    END AS name,
    'vendor' || LPAD(vendor_number::text, 3, '0') || '@example.com' AS email,
    '+27-11-' || LPAD((2000000 + vendor_number)::text, 7, '0') AS phone,
    CASE (vendor_number % 5)
        WHEN 0 THEN 'Johannesburg'
        WHEN 1 THEN 'Cape Town'
        WHEN 2 THEN 'Durban'
        WHEN 3 THEN 'Pretoria'
        ELSE 'Bloemfontein'
    END AS city
FROM generate_series(1, 10) AS seeded_vendors(vendor_number)
ON CONFLICT (vendor_code) DO UPDATE
SET
    name = EXCLUDED.name,
    email = EXCLUDED.email,
    phone = EXCLUDED.phone,
    city = EXCLUDED.city,
    updated_at = CURRENT_TIMESTAMP;
