"""seed cinemas

Revision ID: 0002_seed_cinemas
Revises: 0001_create_cinema_schema
Create Date: 2026-03-12 00:01:00
"""

from migration_sql import run_migration_sql


revision = "0002_seed_cinemas"
down_revision = "0001_create_cinema_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    run_migration_sql("v1__02_insert_demo_data", "up")


def downgrade() -> None:
    run_migration_sql("v1__02_insert_demo_data", "down")
