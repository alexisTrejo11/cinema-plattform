"""seed movies

Revision ID: 0004_seed_movies
Revises: 0003_create_movies_schema
Create Date: 2026-03-12 00:03:00
"""

from migration_sql import run_migration_sql, run_migration_sql_if_table_empty


revision = "0004_seed_movies"
down_revision = "0003_create_movies_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    run_migration_sql_if_table_empty(
        "v1__04__insert_billboard_demo_data", "up", "movies"
    )


def downgrade() -> None:
    run_migration_sql("v1__04__insert_billboard_demo_data", "down")
