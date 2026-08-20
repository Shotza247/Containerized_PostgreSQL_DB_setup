ALTER TABLE inventory
ADD COLUMN IF NOT EXISTS vendor_id INTEGER REFERENCES vendors(id) ON DELETE SET NULL;

CREATE INDEX IF NOT EXISTS idx_inventory_vendor_id
ON inventory (vendor_id);
