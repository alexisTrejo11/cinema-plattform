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



-- Create Promotion Table
CREATE TABLE promotions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    promotion_type VARCHAR(50) NOT NULL,
    discount_value DECIMAL(10, 2) NOT NULL,
    rule JSONB NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    max_uses INTEGER,
    current_uses INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    category_id INTEGER,
    CONSTRAINT fk_category
        FOREIGN KEY (category_id)
        REFERENCES product_categories(id)
        ON DELETE SET NULL
);

CREATE TABLE promotion_products (
    promotion_id UUID NOT NULL,
    product_id UUID NOT NULL,
    PRIMARY KEY (promotion_id, product_id),
    CONSTRAINT fk_promotion
        FOREIGN KEY (promotion_id)
        REFERENCES promotions(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_product
        FOREIGN KEY (product_id)
        REFERENCES products(id)
        ON DELETE CASCADE
);

-- Indexes for promotions
CREATE INDEX IF NOT EXISTS idx_promotions_id ON promotions (id);
CREATE INDEX IF NOT EXISTS idx_promotions_active ON promotions (is_active) WHERE is_active = TRUE;