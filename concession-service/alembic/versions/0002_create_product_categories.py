"""create product_categories table

Revision ID: 0002
Revises: 0001
Create Date: 2026-03-20
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0002"
down_revision: Union[str, Sequence[str], None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        sa.text(
            """
CREATE TABLE IF NOT EXISTS product_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (now() AT TIME ZONE 'utc'),
    CONSTRAINT uq_product_categories_name UNIQUE (name)
)
"""
        )
    )
    op.execute(
        sa.text(
            "CREATE INDEX IF NOT EXISTS idx_product_categories_id ON product_categories (id)"
        )
    )
    op.execute(
        sa.text(
            "CREATE INDEX IF NOT EXISTS idx_product_categories_active ON product_categories (is_active) WHERE is_active = TRUE"
        )
    )


def downgrade() -> None:
    op.execute(sa.text("DROP TABLE IF EXISTS product_categories"))
