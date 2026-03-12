"""create theaters schema

Revision ID: 0005_create_theaters_schema
Revises: 0004_seed_movies
Create Date: 2026-03-12 00:04:00
"""

from migration_sql import run_migration_sql


revision = "0005_create_theaters_schema"
down_revision = "0004_seed_movies"
branch_labels = None
depends_on = None


def upgrade() -> None:
    run_migration_sql("v1__05_create_theater_tables", "up")


def downgrade() -> None:
    run_migration_sql("v1__05_create_theater_tables", "down")
