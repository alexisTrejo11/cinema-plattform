"""create showtime seats table

Revision ID: 0002_create_showtime_seats
Revises: 0001_create_showtimes
Create Date: 2026-04-03 00:00:01
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0002_create_showtime_seats"
down_revision: Union[str, Sequence[str], None] = "0001_create_showtimes"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "showtime_seats",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("showtime_id", sa.Integer(), nullable=False),
        sa.Column("theater_seat_id", sa.Integer(), nullable=False),
        sa.Column("taken_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("transaction_id", sa.Integer(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["showtime_id"], ["showtimes.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("showtime_id", "theater_seat_id", name="uq_showtime_seat"),
    )
    op.create_index("idx_showtime_seats_showtime_id", "showtime_seats", ["showtime_id"])
    op.create_index("idx_showtime_seats_user_id", "showtime_seats", ["user_id"])


def downgrade() -> None:
    op.drop_index("idx_showtime_seats_user_id", table_name="showtime_seats")
    op.drop_index("idx_showtime_seats_showtime_id", table_name="showtime_seats")
    op.drop_table("showtime_seats")
