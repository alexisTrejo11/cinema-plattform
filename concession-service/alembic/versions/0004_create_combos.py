"""create combos table

Revision ID: 0004
Revises: 0003
Create Date: 2026-03-20
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0004"
down_revision: Union[str, Sequence[str], None] = "0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        sa.text(
            """
CREATE TABLE IF NOT EXISTS combos (
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
)
"""
        )
    )
    op.execute(sa.text("CREATE INDEX IF NOT EXISTS idx_combo_name ON combos(name)"))
    op.execute(sa.text("CREATE INDEX IF NOT EXISTS idx_combo_id ON combos(id)"))
    op.execute(
        sa.text(
            "CREATE INDEX IF NOT EXISTS idx_combos_price ON combos(price) WHERE is_available = TRUE"
        )
    )
    op.execute(
        sa.text(
            "CREATE INDEX IF NOT EXISTS idx_combo_availability ON combos(is_available) WHERE is_available = TRUE"
        )
    )


def downgrade() -> None:
    op.execute(sa.text("DROP TABLE IF EXISTS combos"))
