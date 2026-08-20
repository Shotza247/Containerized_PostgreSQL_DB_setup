INSERT INTO customers (
    customer_code,
    first_name,
    last_name,
    email,
    phone,
    city
)
SELECT
    'CUS-' || LPAD(customer_number::text, 3, '0') AS customer_code,
    CASE ((customer_number - 1) % 10)
        WHEN 0 THEN 'Amina'
        WHEN 1 THEN 'Lebo'
        WHEN 2 THEN 'Maya'
        WHEN 3 THEN 'Noah'
        WHEN 4 THEN 'Thabo'
        WHEN 5 THEN 'Zara'
        WHEN 6 THEN 'Ethan'
        WHEN 7 THEN 'Naledi'
        WHEN 8 THEN 'Kai'
        ELSE 'Sofia'
    END AS first_name,
    'Customer ' || LPAD(customer_number::text, 3, '0') AS last_name,
    'customer' || LPAD(customer_number::text, 3, '0') || '@example.com' AS email,
    '+27-10-' || LPAD((1000000 + customer_number)::text, 7, '0') AS phone,
    CASE (customer_number % 5)
        WHEN 0 THEN 'Johannesburg'
        WHEN 1 THEN 'Cape Town'
        WHEN 2 THEN 'Durban'
        WHEN 3 THEN 'Pretoria'
        ELSE 'Gqeberha'
    END AS city
FROM generate_series(1, 40) AS seeded_customers(customer_number)
ON CONFLICT (customer_code) DO UPDATE
SET
    first_name = EXCLUDED.first_name,
    last_name = EXCLUDED.last_name,
    email = EXCLUDED.email,
    phone = EXCLUDED.phone,
    city = EXCLUDED.city,
    updated_at = CURRENT_TIMESTAMP;
