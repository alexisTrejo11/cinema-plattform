"""create promotions table

Revision ID: 0006
Revises: 0005
Create Date: 2026-03-20
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0006"
down_revision: Union[str, Sequence[str], None] = "0005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        sa.text(
            """
CREATE TABLE IF NOT EXISTS promotions (
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
)
"""
        )
    )
    op.execute(sa.text("CREATE INDEX IF NOT EXISTS idx_promotions_id ON promotions (id)"))
    op.execute(
        sa.text(
            "CREATE INDEX IF NOT EXISTS idx_promotions_active ON promotions (is_active) WHERE is_active = TRUE"
        )
    )


def downgrade() -> None:
    op.execute(sa.text("DROP TABLE IF EXISTS promotions"))
