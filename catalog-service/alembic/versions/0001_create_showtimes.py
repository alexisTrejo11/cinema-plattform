"""create showtimes table

Revision ID: 0001_create_showtimes
Revises:
Create Date: 2026-04-03 00:00:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001_create_showtimes"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


showtime_language_enum = sa.Enum(
    "ORIGINAL_ENGLISH",
    "ORIGINAL_SPANISH",
    "ORIGINAL_JAPANESE",
    "ORIGINAL_KOREAN",
    "DUBBED_ENGLISH",
    "DUBBED_SPANISH",
    name="showtime_language_enum",
)

showtime_type_enum = sa.Enum(
    "TRADITIONAL_2D",
    "TRADITIONAL_3D",
    "IMAX_2D",
    "IMAX_3D",
    "4D",
    "4DX",
    "VIP_2D",
    "VIP_3D",
    name="showtime_type_enum",
)

showtime_status_enum = sa.Enum(
    "DRAFT",
    "UPCOMING",
    "IN_PROGRESS",
    "COMPLETED",
    "CANCELLED",
    name="showtime_status_enum",
)


def upgrade() -> None:
    bind = op.get_bind()
    showtime_language_enum.create(bind, checkfirst=True)
    showtime_type_enum.create(bind, checkfirst=True)
    showtime_status_enum.create(bind, checkfirst=True)

    op.create_table(
        "showtimes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("movie_id", sa.Integer(), nullable=False),
        sa.Column("theater_id", sa.Integer(), nullable=False),
        sa.Column("cinema_id", sa.Integer(), nullable=False),
        sa.Column("start_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("price", sa.Numeric(6, 2), nullable=False),
        sa.Column("language", showtime_language_enum, nullable=False),
        sa.Column("type", showtime_type_enum, nullable=False),
        sa.Column(
            "status",
            showtime_status_enum,
            nullable=False,
            server_default=sa.text("'DRAFT'"),
        ),
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
    )
    op.create_index("idx_showtimes_theater_time", "showtimes", ["theater_id", "start_time"])
    op.create_index("idx_showtimes_start_time", "showtimes", ["start_time"])


def downgrade() -> None:
    op.drop_index("idx_showtimes_start_time", table_name="showtimes")
    op.drop_index("idx_showtimes_theater_time", table_name="showtimes")
    op.drop_table("showtimes")

    bind = op.get_bind()
    showtime_status_enum.drop(bind, checkfirst=True)
    showtime_type_enum.drop(bind, checkfirst=True)
    showtime_language_enum.drop(bind, checkfirst=True)
