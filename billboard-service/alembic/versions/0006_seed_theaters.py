"""seed theaters and seats

Revision ID: 0006_seed_theaters
Revises: 0005_create_theaters_schema
Create Date: 2026-03-12 00:05:00
"""

from migration_sql import run_migration_sql


revision = "0006_seed_theaters"
down_revision = "0005_create_theaters_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    run_migration_sql("v1__06_insert_theater_demo_data", "up")


def downgrade() -> None:
    run_migration_sql("v1__06_insert_theater_demo_data", "down")
