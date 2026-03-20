CREATE TABLE promotions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    promotion_type VARCHAR(50) NOT NULL,
    discount_value DECIMAL(10, 2) NOT NULL,
    rule JSONB NOT NULL,
    start_date TIMESTAMP WITH TIME ZONE NOT NULL,
    end_date TIMESTAMP WITH TIME ZONE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    max_uses INTEGER,
    current_uses INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
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

CREATE TABLE promotion_categories (
    promotion_id UUID NOT NULL,
    category_id INTEGER NOT NULL,
    PRIMARY KEY (promotion_id, category_id),
    CONSTRAINT fk_promotion_category
        FOREIGN KEY (promotion_id)
        REFERENCES promotions(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_category_promotion
        FOREIGN KEY (category_id)
        REFERENCES product_categories(id)
        ON DELETE CASCADE
);

-- Indexes for promotions
CREATE INDEX IF NOT EXISTS idx_promotions_id ON promotions (id);
CREATE INDEX IF NOT EXISTS idx_promotions_active ON promotions (is_active) WHERE is_active = TRUE;
