"""create stored_payment_methods table

Revision ID: 20260401_01
Revises: 20260331_03
Create Date: 2026-04-01 12:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "20260401_01"
down_revision: Union[str, None] = "20260331_03"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "stored_payment_methods",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("payment_method_id", sa.String(length=255), nullable=False),
        sa.Column("provider_token", sa.String(length=255), nullable=False, server_default=""),
        sa.Column("card", sa.JSON(), nullable=True),
        sa.Column("is_default", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_stored_payment_methods_user_id",
        "stored_payment_methods",
        ["user_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_stored_payment_methods_user_id", table_name="stored_payment_methods")
    op.drop_table("stored_payment_methods")
