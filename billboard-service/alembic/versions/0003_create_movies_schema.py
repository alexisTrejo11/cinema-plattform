"""create movies schema

Revision ID: 0003_create_movies_schema
Revises: 0002_seed_cinemas
Create Date: 2026-03-12 00:02:00
"""

from migration_sql import run_migration_sql


revision = "0003_create_movies_schema"
down_revision = "0002_seed_cinemas"
branch_labels = None
depends_on = None


def upgrade() -> None:
    run_migration_sql("v1__03_create_billboard_table", "up")


def downgrade() -> None:
    run_migration_sql("v1__03_create_billboard_table", "down")
