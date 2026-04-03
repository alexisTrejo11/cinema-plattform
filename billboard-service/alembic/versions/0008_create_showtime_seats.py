"""create showtime seats schema

Revision ID: 0008_create_showtime_seats
Revises: 0007_create_showtimes
Create Date: 2026-04-03 00:00:00
"""

from migration_sql import execute_sql

revision = '0008_create_showtime_seats'
down_revision = '0007_create_showtimes'
branch_labels = None
depends_on = None

_UP_SQL = 'CREATE TABLE IF NOT EXISTS showtime_seats(\n    id SERIAL PRIMARY KEY,\n    showtime_id INT NOT NULL,\n    theater_seat_id INT NOT NULL,\n\n    taken_at TIMESTAMP WITH TIME ZONE,\n    transation_id INT,\n    taken_by_user_id INT,\n\n    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,\n    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,\n\n    CONSTRAINT fk_showtime\n        FOREIGN KEY (showtime_id)\n        REFERENCES showtimes (id)\n        ON DELETE CASCADE,    \n    \n    CONSTRAINT fk_theater_seat\n        FOREIGN KEY (theater_seat_id)\n        REFERENCES theater_seats (id)\n        ON DELETE RESTRICT,\n\n    CONSTRAINT uq_showtime_seat\n        UNIQUE (showtime_id, theater_seat_id)    \n);\n\nCREATE INDEX IF NOT EXISTS idx_showtime_seats_showtime_id ON showtime_seats (showtime_id);\nCREATE INDEX IF NOT EXISTS idx_showtime_seats_user_id ON showtime_seats (taken_by_user_id);\n\n\nCREATE OR REPLACE FUNCTION update_updated_at_column()\nRETURNS TRIGGER AS $$\nBEGIN\n    NEW.updated_at = NOW();\n    RETURN NEW;\nEND;\n$$ LANGUAGE plpgsql;\n\n\nDROP TRIGGER IF EXISTS update_showtime_seats_updated_at ON showtime_seats;\n\nCREATE TRIGGER update_showtime_seats_updated_at\nBEFORE UPDATE ON showtime_seats\nFOR EACH ROW\nEXECUTE FUNCTION update_updated_at_column();'

_DOWN_SQL = 'DROP TRIGGER IF EXISTS update_showtime_seats_updated_at ON showtime_seats;\nDROP TABLE IF EXISTS showtime_seats;'


def upgrade() -> None:
    execute_sql(_UP_SQL)


def downgrade() -> None:
    execute_sql(_DOWN_SQL)
