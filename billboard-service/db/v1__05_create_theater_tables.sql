DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'theater_type_enum') THEN
        CREATE TYPE theater_type_enum AS ENUM ('TWO_D', 'THREE_D', 'IMAX', 'FOUR_DX', 'VIP');
    END IF;
END $$;

CREATE TABLE theaters (
    id SERIAL PRIMARY KEY,
    cinema_id INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    capacity INT NOT NULL CHECK (capacity > 0),
    theater_type theater_type_enum NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    maintenance_mode BOOLEAN NOT NULL DEFAULT FALSE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_cinema 
        FOREIGN KEY (cinema_id) 
        REFERENCES cinemas (id) ON DELETE CASCADE
);


CREATE INDEX idx_theaters_cinema_id ON theaters (cinema_id);
CREATE INDEX idx_theaters_type ON theaters (theater_type);
CREATE INDEX idx_theaters_active_cinema_type ON theaters (cinema_id, theater_type, is_active);

CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_theaters_updated_at
BEFORE UPDATE ON theaters
FOR EACH ROW
EXECUTE FUNCTION update_timestamp();



CREATE TYPE seat_type_enum AS ENUM (
    'STANDARD',
    'VIP',
    'ACCESSIBLE', -- For disabled access
    'PREMIUM',
    'FOUR_DX',
    'LOVESEAT'
);

CREATE TABLE theater_seats(
    id SERIAL PRIMARY KEY,
    theater_id int NOT NULL,
    seat_row VARCHAR(5) NOT NULL,
    seat_number INT NOT NULL,
    seat_type seat_type_enum NOT NULL DEFAULT 'STANDARD',
    need_maintenance BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_theater
        FOREIGN KEY (theater_id)
        REFERENCES theaters (id)
        ON DELETE CASCADE,
        
    CONSTRAINT uq_theater_seat_position
        UNIQUE (theater_id, seat_row, seat_number)
);

CREATE INDEX idx_theater_seats_theater_id ON theater_seats (theater_id);
CREATE INDEX idx_theater_seats_row_number ON theater_seats (theater_id, seat_row, seat_number);



