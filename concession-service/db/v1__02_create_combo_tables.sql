
CREATE TABLE combos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    description VARCHAR(500) DEFAULT '',
    price NUMERIC(10,2) NOT NULL,
    discount_percentage NUMERIC(5,2) DEFAULT 0.00,
    image_url VARCHAR(500),
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_combos_price CHECK (price > 0),
    CONSTRAINT chk_combos_discount CHECK (discount_percentage BETWEEN 0 AND 100)
);

CREATE TABLE combo_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    combo_id UUID NOT NULL,
    product_id UUID NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_combo_items_combo_id 
        FOREIGN KEY (combo_id) 
        REFERENCES combos(id) 
        ON DELETE CASCADE,  -- Delete items when combo is deleted
    CONSTRAINT fk_combo_items_product_id 
        FOREIGN KEY (product_id) 
        REFERENCES products(id)
        ON DELETE RESTRICT,  -- Prevent product deletion if used in combos
    CONSTRAINT chk_combo_items_quantity CHECK (quantity > 0),
    CONSTRAINT uq_combo_items_product UNIQUE (combo_id, product_id)  -- Prevent duplicate products in same combo
);


-- Indexes for combos
CREATE INDEX IF NOT EXISTS idx_combo_name ON combos(name);
CREATE INDEX IF NOT EXISTS idx_combo_id ON combos(id);
CREATE INDEX IF NOT EXISTS idx_combos_price ON combos(price) WHERE is_available = TRUE;
CREATE INDEX IF NOT EXISTS idx_combo_availability ON combos(is_available) WHERE is_available = TRUE;

-- Indexes for combo_items
CREATE INDEX IF NOT EXISTS idx_combo_items_combo ON combo_items(combo_id);
CREATE INDEX IF NOT EXISTS idx_combo_items_product ON combo_items(product_id);
CREATE INDEX IF NOT EXISTS idx_combo_items_quantity ON combo_items(quantity);

