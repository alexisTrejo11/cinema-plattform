"""create showtime seats schema

Revision ID: 0008_create_showtime_seats
Revises: 0007_create_showtimes
Create Date: 2026-03-12 00:07:00
"""

from migration_sql import run_migration_sql


revision = "0008_create_showtime_seats"
down_revision = "0007_create_showtimes"
branch_labels = None
depends_on = None


def upgrade() -> None:
    run_migration_sql("v1__08_create_showtime_seats_table", "up")


def downgrade() -> None:
    run_migration_sql("v1__08_create_showtime_seats_table", "down")
