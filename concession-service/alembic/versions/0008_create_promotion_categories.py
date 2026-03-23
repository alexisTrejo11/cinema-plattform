"""create promotion_categories table

Revision ID: 0008
Revises: 0007
Create Date: 2026-03-20
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0008"
down_revision: Union[str, Sequence[str], None] = "0007"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        sa.text(
            """
CREATE TABLE promotion_categories (
    promotion_id UUID NOT NULL,
    category_id INTEGER NOT NULL,
    PRIMARY KEY (promotion_id, category_id),
    CONSTRAINT promotion_categories_promotion_id_fkey
        FOREIGN KEY (promotion_id)
        REFERENCES promotions(id)
        ON DELETE CASCADE,
    CONSTRAINT promotion_categories_category_id_fkey
        FOREIGN KEY (category_id)
        REFERENCES product_categories(id)
        ON DELETE CASCADE
)
"""
        )
    )


def downgrade() -> None:
    op.execute(sa.text("DROP TABLE IF EXISTS promotion_categories"))
