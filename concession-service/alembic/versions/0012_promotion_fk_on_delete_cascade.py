"""promotion join tables: enforce ON DELETE CASCADE on promotion_id FKs

Revision ID: 0012
Revises: 0011
Create Date: 2026-03-23
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0012"
down_revision: Union[str, Sequence[str], None] = "0011"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        sa.text(
            """
ALTER TABLE promotion_products
    DROP CONSTRAINT IF EXISTS promotion_products_promotion_id_fkey;
ALTER TABLE promotion_products
    ADD CONSTRAINT promotion_products_promotion_id_fkey
    FOREIGN KEY (promotion_id) REFERENCES promotions(id) ON DELETE CASCADE;

ALTER TABLE promotion_categories
    DROP CONSTRAINT IF EXISTS promotion_categories_promotion_id_fkey;
ALTER TABLE promotion_categories
    ADD CONSTRAINT promotion_categories_promotion_id_fkey
    FOREIGN KEY (promotion_id) REFERENCES promotions(id) ON DELETE CASCADE;
"""
        )
    )


def downgrade() -> None:
    op.execute(
        sa.text(
            """
ALTER TABLE promotion_products
    DROP CONSTRAINT IF EXISTS promotion_products_promotion_id_fkey;
ALTER TABLE promotion_products
    ADD CONSTRAINT promotion_products_promotion_id_fkey
    FOREIGN KEY (promotion_id) REFERENCES promotions(id);

ALTER TABLE promotion_categories
    DROP CONSTRAINT IF EXISTS promotion_categories_promotion_id_fkey;
ALTER TABLE promotion_categories
    ADD CONSTRAINT promotion_categories_promotion_id_fkey
    FOREIGN KEY (promotion_id) REFERENCES promotions(id);
"""
        )
    )
