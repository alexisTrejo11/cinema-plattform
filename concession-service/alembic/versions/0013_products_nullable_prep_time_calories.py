"""products: allow NULL for preparation_time_mins and calories

Matches 0003_create_products (INTEGER without NOT NULL) and the domain/API
where these fields are optional. Fixes DBs created via SQLAlchemy metadata
that incorrectly enforced NOT NULL on these columns.

Revision ID: 0013
Revises: 0012
Create Date: 2026-03-23
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0013"
down_revision: Union[str, Sequence[str], None] = "0012"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        sa.text(
            """
ALTER TABLE products
    ALTER COLUMN preparation_time_mins DROP NOT NULL;
ALTER TABLE products
    ALTER COLUMN calories DROP NOT NULL;
"""
        )
    )


def downgrade() -> None:
    op.execute(
        sa.text(
            """
UPDATE products SET preparation_time_mins = 0 WHERE preparation_time_mins IS NULL;
UPDATE products SET calories = 0 WHERE calories IS NULL;
ALTER TABLE products
    ALTER COLUMN preparation_time_mins SET NOT NULL;
ALTER TABLE products
    ALTER COLUMN calories SET NOT NULL;
"""
        )
    )
