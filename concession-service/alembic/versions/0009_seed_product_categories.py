"""seed product categories

Revision ID: 0009
Revises: 0008
Create Date: 2026-03-20
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0009"
down_revision: Union[str, Sequence[str], None] = "0008"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        sa.text(
            """
INSERT INTO product_categories (name, description, is_active) VALUES
('Popcorn', 'Freshly popped cinema popcorn varieties', true),
('Drinks', 'Cold beverages and refreshments', true),
('Candy', 'Assorted chocolates and sweets', true),
('Hot Food', 'Hot snacks and meals', true),
('Combo Meals', 'Special value meal deals', true)
ON CONFLICT (name) DO NOTHING
"""
        )
    )


def downgrade() -> None:
    op.execute(
        sa.text(
            """
DELETE FROM product_categories WHERE name IN (
    'Popcorn',
    'Drinks',
    'Candy',
    'Hot Food',
    'Combo Meals'
)
"""
        )
    )
