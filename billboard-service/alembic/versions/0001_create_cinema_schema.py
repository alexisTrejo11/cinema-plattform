"""create cinema schema

Revision ID: 0001_create_cinema_schema
Revises:
Create Date: 2026-03-12 00:00:00
"""

from migration_sql import run_migration_sql


revision = "0001_create_cinema_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    run_migration_sql("v1__01_create_cinema_table", "up")


def downgrade() -> None:
    run_migration_sql("v1__01_create_cinema_table", "down")
