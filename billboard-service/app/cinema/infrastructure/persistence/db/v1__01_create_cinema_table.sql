CREATE TYPE cinema_status_enum AS ENUM ('OPEN', 'CLOSED', 'MAINTENANCE');
CREATE TYPE cinema_type_enum AS ENUM ('VIP', 'TRADITIONAL');
CREATE TYPE location_region_enum AS ENUM ('CDMX_SOUTH', 'CDMX_NORTH', 'CDMX_CENTER', 'CDMX_EAST', 'CDMX_WEST');

CREATE TABLE cinemas (
    id SERIAL PRIMARY KEY,
    image TEXT NOT NULL DEFAULT '',
    name VARCHAR(255) NOT NULL UNIQUE,
    tax_number VARCHAR(255) NOT NULL UNIQUE,
    is_active BOOLEAN NOT NULL DEFAULT FALSE,
    description TEXT NOT NULL DEFAULT '',
    screens INTEGER NOT NULL DEFAULT 0 CHECK (screens >= 0),

    last_renovation DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    region location_region_enum NOT NULL,
    type cinema_type_enum NOT NULL, 
    status cinema_status_enum NOT NULL, 

    -- Amenities 
    has_parking BOOLEAN NOT NULL DEFAULT FALSE,
    has_food_court BOOLEAN NOT NULL DEFAULT FALSE,
    has_coffee_station BOOLEAN NOT NULL DEFAULT FALSE,
    has_disabled_access BOOLEAN NOT NULL DEFAULT FALSE,

    -- Contact Info 
    address VARCHAR(500) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    email_contact VARCHAR(255) NOT NULL UNIQUE,

    latitude DOUBLE PRECISION NOT NULL CHECK (latitude >= -90.0 AND latitude <= 90.0),
    longitude DOUBLE PRECISION NOT NULL CHECK (longitude >= -180.0 AND longitude <= 180.0),

    -- Social Media 
    facebook_url TEXT,
    instagram_url TEXT, 
    x_url TEXT,
    tik_tok_url TEXT,

    features TEXT[] NOT NULL DEFAULT '{}'
);


CREATE INDEX idx_cinemas_name ON cinemas(name);
CREATE INDEX idx_cinemas_tax_number ON cinemas(tax_number);
CREATE INDEX idx_cinemas_email_contact ON cinemas(email_contact);
CREATE INDEX idx_cinemas_status ON cinemas(status);
CREATE INDEX idx_cinemas_type ON cinemas(type);
-- Consider adding a GIST index for geographic queries if you plan to use them extensively
-- CREATE EXTENSION IF NOT EXISTS postgis; -- If using PostGIS for spatial queries
-- CREATE INDEX idx_cinemas_location ON cinemas USING GIST (ST_MakePoint(longitude, latitude));

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_cinemas_updated_at
BEFORE UPDATE ON cinemas
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

