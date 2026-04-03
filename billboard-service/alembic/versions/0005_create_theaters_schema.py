"""create theaters schema

Revision ID: 0005_create_theaters_schema
Revises: 0004_seed_movies
Create Date: 2026-04-03 00:00:00
"""

from migration_sql import execute_sql

revision = '0005_create_theaters_schema'
down_revision = '0004_seed_movies'
branch_labels = None
depends_on = None

_UP_SQL = "DO $$ BEGIN\n    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'theater_type_enum') THEN\n        CREATE TYPE theater_type_enum AS ENUM ('TWO_D', 'THREE_D', 'IMAX', 'FOUR_DX', 'VIP');\n    END IF;\nEND $$;\n\nCREATE TABLE IF NOT EXISTS theaters (\n    id SERIAL PRIMARY KEY,\n    cinema_id INT NOT NULL,\n    name VARCHAR(50) NOT NULL,\n    capacity INT NOT NULL CHECK (capacity > 0),\n    theater_type theater_type_enum NOT NULL,\n    is_active BOOLEAN NOT NULL DEFAULT TRUE,\n    maintenance_mode BOOLEAN NOT NULL DEFAULT FALSE,\n    \n    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,\n    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,\n    deleted_at TIMESTAMP WITH TIME ZONE DEFAULT NULL,\n    \n    CONSTRAINT fk_cinema \n        FOREIGN KEY (cinema_id) \n        REFERENCES cinemas (id) ON DELETE CASCADE\n);\n\n\nCREATE INDEX IF NOT EXISTS idx_theaters_cinema_id ON theaters (cinema_id);\nCREATE INDEX IF NOT EXISTS idx_theaters_type ON theaters (theater_type);\nCREATE INDEX IF NOT EXISTS idx_theaters_active_cinema_type ON theaters (cinema_id, theater_type, is_active);\n\nCREATE OR REPLACE FUNCTION update_timestamp()\nRETURNS TRIGGER AS $$\nBEGIN\n    NEW.updated_at = CURRENT_TIMESTAMP;\n    RETURN NEW;\nEND;\n$$ LANGUAGE plpgsql;\n\nDROP TRIGGER IF EXISTS trg_theaters_updated_at ON theaters;\n\nCREATE TRIGGER trg_theaters_updated_at\nBEFORE UPDATE ON theaters\nFOR EACH ROW\nEXECUTE FUNCTION update_timestamp();\n\n\n\nDO $$ BEGIN\n    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'seat_type_enum') THEN\n        CREATE TYPE seat_type_enum AS ENUM (\n    'STANDARD',\n    'VIP',\n    'ACCESSIBLE', -- For disabled access\n    'PREMIUM',\n    'FOUR_DX',\n    'LOVESEAT'\n);\n    END IF;\nEND $$;\n\nCREATE TABLE IF NOT EXISTS theater_seats(\n    id SERIAL PRIMARY KEY,\n    theater_id int NOT NULL,\n    seat_row VARCHAR(5) NOT NULL,\n    seat_number INT NOT NULL,\n    seat_type seat_type_enum NOT NULL DEFAULT 'STANDARD',\n    need_maintenance BOOLEAN NOT NULL DEFAULT FALSE,\n    is_active BOOLEAN NOT NULL DEFAULT TRUE,\n    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,\n    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,\n    \n    CONSTRAINT fk_theater\n        FOREIGN KEY (theater_id)\n        REFERENCES theaters (id)\n        ON DELETE CASCADE,\n        \n    CONSTRAINT uq_theater_seat_position\n        UNIQUE (theater_id, seat_row, seat_number)\n);\n\nCREATE INDEX IF NOT EXISTS idx_theater_seats_theater_id ON theater_seats (theater_id);\nCREATE INDEX IF NOT EXISTS idx_theater_seats_row_number ON theater_seats (theater_id, seat_row, seat_number);\n\n\n\n"

_DOWN_SQL = 'DROP TABLE IF EXISTS theater_seats;\nDROP TRIGGER IF EXISTS trg_theaters_updated_at ON theaters;\nDROP TABLE IF EXISTS theaters;\nDROP TYPE IF EXISTS seat_type_enum;\nDROP TYPE IF EXISTS theater_type_enum;\nDROP FUNCTION IF EXISTS update_timestamp();'


def upgrade() -> None:
    execute_sql(_UP_SQL)


def downgrade() -> None:
    execute_sql(_DOWN_SQL)
