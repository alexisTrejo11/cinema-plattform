CREATE TABLE food_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (now() AT TIME ZONE 'utc'),
    CONSTRAINT uq_food_categories_name UNIQUE (name)
);

CREATE INDEX IF NOT EXISTS ix_food_categories_id ON food_categories (id);

CREATE TABLE food_products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price FLOAT NOT NULL,
    image_url VARCHAR(500),
    is_available BOOLEAN DEFAULT TRUE,
    preparation_time_mins INTEGER,
    calories INTEGER,
    category_id INTEGER NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (now() AT TIME ZONE 'utc'),
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (now() AT TIME ZONE 'utc'),
    CONSTRAINT fk_food_products_category_id FOREIGN KEY (category_id) 
        REFERENCES food_categories (id)
);

CREATE INDEX IF NOT EXISTS ix_food_products_id ON food_products (id);

CREATE INDEX IF NOT EXISTS ix_food_products_category_id ON food_products (category_id);

CREATE INDEX IF NOT EXISTS ix_food_products_is_available ON food_products (is_available);
CREATE INDEX IF NOT EXISTS ix_food_products_price ON food_products (price);