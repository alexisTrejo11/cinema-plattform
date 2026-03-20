"""create products table

Revision ID: 0003
Revises: 0002
Create Date: 2026-03-20
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0003"
down_revision: Union[str, Sequence[str], None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        sa.text(
            """
CREATE TABLE IF NOT EXISTS products (
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
        ON DELETE RESTRICT
)
"""
        )
    )
    op.execute(sa.text("CREATE INDEX IF NOT EXISTS idx_products_id ON products (id)"))
    op.execute(
        sa.text("CREATE INDEX IF NOT EXISTS idx_products_category_id ON products (category_id)")
    )
    op.execute(
        sa.text(
            "CREATE INDEX IF NOT EXISTS idx_products_is_available ON products (is_available) WHERE is_available = TRUE"
        )
    )
    op.execute(sa.text("CREATE INDEX IF NOT EXISTS idx_products_price ON products (price)"))
    op.execute(sa.text("CREATE INDEX IF NOT EXISTS idx_products_name ON products (name)"))


def downgrade() -> None:
    op.execute(sa.text("DROP TABLE IF EXISTS products"))
