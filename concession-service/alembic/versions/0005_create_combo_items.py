"""create combo_items table

Revision ID: 0005
Revises: 0004
Create Date: 2026-03-20
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0005"
down_revision: Union[str, Sequence[str], None] = "0004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        sa.text(
            """
CREATE TABLE IF NOT EXISTS combo_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    combo_id UUID NOT NULL,
    product_id UUID NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_combo_items_combo_id
        FOREIGN KEY (combo_id)
        REFERENCES combos(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_combo_items_product_id
        FOREIGN KEY (product_id)
        REFERENCES products(id)
        ON DELETE RESTRICT,
    CONSTRAINT chk_combo_items_quantity CHECK (quantity > 0),
    CONSTRAINT uq_combo_items_product UNIQUE (combo_id, product_id)
)
"""
        )
    )
    op.execute(sa.text("CREATE INDEX IF NOT EXISTS idx_combo_items_combo ON combo_items(combo_id)"))
    op.execute(
        sa.text("CREATE INDEX IF NOT EXISTS idx_combo_items_product ON combo_items(product_id)")
    )
    op.execute(
        sa.text("CREATE INDEX IF NOT EXISTS idx_combo_items_quantity ON combo_items(quantity)")
    )


def downgrade() -> None:
    op.execute(sa.text("DROP TABLE IF EXISTS combo_items"))
