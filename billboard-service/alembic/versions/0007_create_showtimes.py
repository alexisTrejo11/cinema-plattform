"""create showtimes schema and seed data

Revision ID: 0007_create_showtimes
Revises: 0006_seed_theaters
Create Date: 2026-03-12 00:06:00
"""

from migration_sql import run_migration_sql


revision = "0007_create_showtimes"
down_revision = "0006_seed_theaters"
branch_labels = None
depends_on = None


def upgrade() -> None:
    run_migration_sql("v1__07__create_showtime_table", "up")


def downgrade() -> None:
    run_migration_sql("v1__07__create_showtime_table", "down")
