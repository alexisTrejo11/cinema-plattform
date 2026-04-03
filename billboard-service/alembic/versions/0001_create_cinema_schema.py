"""create cinema schema

Revision ID: 0001_create_cinema_schema
Revises: 
Create Date: 2026-04-03 00:00:00
"""

from migration_sql import execute_sql

revision = '0001_create_cinema_schema'
down_revision = None
branch_labels = None
depends_on = None

_UP_SQL = "DO $$ BEGIN\n    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'cinema_status_enum') THEN\n        CREATE TYPE cinema_status_enum AS ENUM ('OPEN', 'CLOSED', 'MAINTENANCE');\n    END IF;\nEND $$;\n\nDO $$ BEGIN\n    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'cinema_type_enum') THEN\n        CREATE TYPE cinema_type_enum AS ENUM ('VIP', 'TRADITIONAL');\n    END IF;\nEND $$;\n\nDO $$ BEGIN\n    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'location_region_enum') THEN\n        CREATE TYPE location_region_enum AS ENUM ('CDMX_SOUTH', 'CDMX_NORTH', 'CDMX_CENTER', 'CDMX_EAST', 'CDMX_WEST');\n    END IF;\nEND $$;\n\nCREATE TABLE IF NOT EXISTS cinemas (\n    id SERIAL PRIMARY KEY,\n    image TEXT NOT NULL DEFAULT '',\n    name VARCHAR(255) NOT NULL UNIQUE,\n    tax_number VARCHAR(255) NOT NULL UNIQUE,\n    is_active BOOLEAN NOT NULL DEFAULT FALSE,\n    description TEXT NOT NULL DEFAULT '',\n    screens INTEGER NOT NULL DEFAULT 0 CHECK (screens >= 0),\n\n    last_renovation DATE,\n    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,\n    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,\n\n    region location_region_enum NOT NULL,\n    type cinema_type_enum NOT NULL, \n    status cinema_status_enum NOT NULL, \n\n    -- Amenities \n    has_parking BOOLEAN NOT NULL DEFAULT FALSE,\n    has_food_court BOOLEAN NOT NULL DEFAULT FALSE,\n    has_coffee_station BOOLEAN NOT NULL DEFAULT FALSE,\n    has_disabled_access BOOLEAN NOT NULL DEFAULT FALSE,\n\n    -- Contact Info \n    address VARCHAR(500) NOT NULL,\n    phone VARCHAR(20) NOT NULL,\n    email_contact VARCHAR(255) NOT NULL UNIQUE,\n\n    latitude DOUBLE PRECISION NOT NULL CHECK (latitude >= -90.0 AND latitude <= 90.0),\n    longitude DOUBLE PRECISION NOT NULL CHECK (longitude >= -180.0 AND longitude <= 180.0),\n\n    -- Social Media \n    facebook_url TEXT,\n    instagram_url TEXT, \n    x_url TEXT,\n    tik_tok_url TEXT,\n\n    features TEXT[] NOT NULL DEFAULT '{}'\n);\n\n\nCREATE INDEX IF NOT EXISTS idx_cinemas_name ON cinemas(name);\nCREATE INDEX IF NOT EXISTS idx_cinemas_tax_number ON cinemas(tax_number);\nCREATE INDEX IF NOT EXISTS idx_cinemas_email_contact ON cinemas(email_contact);\nCREATE INDEX IF NOT EXISTS idx_cinemas_status ON cinemas(status);\nCREATE INDEX IF NOT EXISTS idx_cinemas_type ON cinemas(type);\n-- Consider adding a GIST index for geographic queries if you plan to use them extensively\n-- CREATE EXTENSION IF NOT EXISTS postgis; -- If using PostGIS for spatial queries\n-- CREATE INDEX idx_cinemas_location ON cinemas USING GIST (ST_MakePoint(longitude, latitude));\n\nCREATE OR REPLACE FUNCTION update_updated_at_column()\nRETURNS TRIGGER AS $$\nBEGIN\n    NEW.updated_at = NOW();\n    RETURN NEW;\nEND;\n$$ LANGUAGE plpgsql;\n\nDROP TRIGGER IF EXISTS update_cinemas_updated_at ON cinemas;\n\nCREATE TRIGGER update_cinemas_updated_at\nBEFORE UPDATE ON cinemas\nFOR EACH ROW\nEXECUTE FUNCTION update_updated_at_column();\n\n"

_DOWN_SQL = 'DROP TRIGGER IF EXISTS update_cinemas_updated_at ON cinemas;\nDROP TABLE IF EXISTS cinemas;\nDROP TYPE IF EXISTS location_region_enum;\nDROP TYPE IF EXISTS cinema_type_enum;\nDROP TYPE IF EXISTS cinema_status_enum;\nDROP FUNCTION IF EXISTS update_updated_at_column();'


def upgrade() -> None:
    execute_sql(_UP_SQL)


def downgrade() -> None:
    execute_sql(_DOWN_SQL)
