"""create movies schema

Revision ID: 0003_create_movies_schema
Revises: 0002_seed_cinemas
Create Date: 2026-04-03 00:00:00
"""

from migration_sql import execute_sql

revision = '0003_create_movies_schema'
down_revision = '0002_seed_cinemas'
branch_labels = None
depends_on = None

_UP_SQL = "DO $$ BEGIN\n    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'movie_genre') THEN\n        CREATE TYPE movie_genre AS ENUM ('ACTION', 'COMEDY', 'DRAMA', 'ROMANCE', 'THRILLER', 'SCI_FI');\n    END IF;\nEND $$;\n\nDO $$ BEGIN\n    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'movie_rating') THEN\n        CREATE TYPE movie_rating AS ENUM ('G', 'PG', 'PG_13', 'R', 'NC_17');\n    END IF;\nEND $$;\n\nCREATE TABLE IF NOT EXISTS movies (\n    id SERIAL PRIMARY KEY,\n    title VARCHAR(200) NOT NULL,\n    original_title VARCHAR(200),\n    minute_duration INTEGER,\n    release_date DATE,\n    projection_start_date DATE,\n    projection_end_date DATE,\n    synopsis TEXT NOT NULL DEFAULT '',\n    genre movie_genre NOT NULL,\n    rating movie_rating NOT NULL,\n    poster_url TEXT,\n    trailer_url TEXT,\n    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n    deleted_at TIMESTAMP DEFAULT NULL\n);\n\nCREATE INDEX IF NOT EXISTS idx_movies_title ON movies(title);\nCREATE INDEX IF NOT EXISTS idx_movies_dates ON movies(release_date);\nCREATE INDEX IF NOT EXISTS idx_movies_projection_dates ON movies(projection_start_date, projection_end_date);\nCREATE INDEX IF NOT EXISTS idx_movies_genre ON movies(genre);\n\nCREATE OR REPLACE FUNCTION update_updated_at_column() \nRETURNS TRIGGER AS $$\nBEGIN\n    NEW.updated_at = NOW();\n    RETURN NEW;\nEND;\n$$ LANGUAGE plpgsql;\n\nDROP TRIGGER IF EXISTS update_movies_updated_at ON movies;\n\nCREATE TRIGGER update_movies_updated_at\nBEFORE UPDATE ON movies\nFOR EACH ROW\nEXECUTE FUNCTION update_updated_at_column();\n\n"

_DOWN_SQL = 'DROP TRIGGER IF EXISTS update_movies_updated_at ON movies;\nDROP TABLE IF EXISTS movies;\nDROP TYPE IF EXISTS movie_rating;\nDROP TYPE IF EXISTS movie_genre;'


def upgrade() -> None:
    execute_sql(_UP_SQL)


def downgrade() -> None:
    execute_sql(_DOWN_SQL)
