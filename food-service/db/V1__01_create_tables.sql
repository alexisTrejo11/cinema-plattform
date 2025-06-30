CREATE TABLE food_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (now() AT TIME ZONE 'utc'),
    CONSTRAINT uq_food_categories_name UNIQUE (name)
);

CREATE TABLE food_products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price NUMERIC(10,2) NOT NULL,
    image_url VARCHAR(500),
    is_available BOOLEAN DEFAULT TRUE,
    preparation_time_mins INTEGER,
    calories INTEGER,
    category_id INTEGER NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (now() AT TIME ZONE 'utc'),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (now() AT TIME ZONE 'utc'),
    CONSTRAINT fk_food_products_category_id 
        FOREIGN KEY (category_id) 
        REFERENCES food_categories (id)
        ON DELETE RESTRICT  -- Prevent category deletion if products exist
);

CREATE TABLE combos (
    id SERIAL PRIMARY KEY,
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
    id SERIAL PRIMARY KEY,
    combo_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_combo_items_combo_id 
        FOREIGN KEY (combo_id) 
        REFERENCES combos(id) 
        ON DELETE CASCADE,  -- Delete items when combo is deleted
    CONSTRAINT fk_combo_items_product_id 
        FOREIGN KEY (product_id) 
        REFERENCES food_products(id)
        ON DELETE RESTRICT,  -- Prevent product deletion if used in combos
    CONSTRAINT chk_combo_items_quantity CHECK (quantity > 0),
    CONSTRAINT uq_combo_items_product UNIQUE (combo_id, product_id)  -- Prevent duplicate products in same combo
);

-- Indexes for food_categories
CREATE INDEX IF NOT EXISTS ix_food_categories_id ON food_categories (id);
CREATE INDEX IF NOT EXISTS ix_food_categories_active ON food_categories (is_active) WHERE is_active = TRUE;

-- Indexes for food_products
CREATE INDEX IF NOT EXISTS ix_food_products_id ON food_products (id);
CREATE INDEX IF NOT EXISTS ix_food_products_category_id ON food_products (category_id);
CREATE INDEX IF NOT EXISTS ix_food_products_is_available ON food_products (is_available) WHERE is_available = TRUE;
CREATE INDEX IF NOT EXISTS ix_food_products_price ON food_products (price);
CREATE INDEX IF NOT EXISTS ix_food_products_name ON food_products (name);

-- Indexes for combos
CREATE INDEX IF NOT EXISTS idx_combo_name ON combos(name);
CREATE INDEX IF NOT EXISTS idx_combo_id ON combos(id);
CREATE INDEX IF NOT EXISTS idx_combos_price ON combos(price) WHERE is_available = TRUE;
CREATE INDEX IF NOT EXISTS idx_combo_availability ON combos(is_available) WHERE is_available = TRUE;

-- Indexes for combo_items
CREATE INDEX IF NOT EXISTS idx_combo_items_combo ON combo_items(combo_id);
CREATE INDEX IF NOT EXISTS idx_combo_items_product ON combo_items(product_id);
CREATE INDEX IF NOT EXISTS idx_combo_items_quantity ON combo_items(quantity);