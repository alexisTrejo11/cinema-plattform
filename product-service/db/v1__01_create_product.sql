CREATE TABLE product_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (now() AT TIME ZONE 'utc'),
    CONSTRAINT uq_product_categories_name UNIQUE (name)
);

CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
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
    CONSTRAINT fk_products_category_id 
        FOREIGN KEY (category_id) 
        REFERENCES product_categories (id)
        ON DELETE RESTRICT  -- Prevent category deletion if products exist
);

-- Indexes for product_categories
CREATE INDEX IF NOT EXISTS idx_product_categories_id ON product_categories (id);
CREATE INDEX IF NOT EXISTS idx_product_categories_active ON product_categories (is_active) WHERE is_active = TRUE;

-- Indexes for products
CREATE INDEX IF NOT EXISTS idx_products_id ON products (id);
CREATE INDEX IF NOT EXISTS idx_products_category_id ON products (category_id);
CREATE INDEX IF NOT EXISTS idx_products_is_available ON products (is_available) WHERE is_available = TRUE;
CREATE INDEX IF NOT EXISTS idx_products_price ON products (price);
CREATE INDEX IF NOT EXISTS idx_products_name ON products (name);
