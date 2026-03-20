CREATE TABLE IF NOT EXISTS showtime_seats(
    id SERIAL PRIMARY KEY,
    showtime_id INT NOT NULL,
    theater_seat_id INT NOT NULL,

    taken_at TIMESTAMP WITH TIME ZONE,
    transation_id INT,
    taken_by_user_id INT,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_showtime
        FOREIGN KEY (showtime_id)
        REFERENCES showtimes (id)
        ON DELETE CASCADE,    
    
    CONSTRAINT fk_theater_seat
        FOREIGN KEY (theater_seat_id)
        REFERENCES theater_seats (id)
        ON DELETE RESTRICT,

    CONSTRAINT uq_showtime_seat
        UNIQUE (showtime_id, theater_seat_id)    
);

CREATE INDEX IF NOT EXISTS idx_showtime_seats_showtime_id ON showtime_seats (showtime_id);
CREATE INDEX IF NOT EXISTS idx_showtime_seats_user_id ON showtime_seats (taken_by_user_id);


CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


DROP TRIGGER IF EXISTS update_showtime_seats_updated_at ON showtime_seats;

CREATE TRIGGER update_showtime_seats_updated_at
BEFORE UPDATE ON showtime_seats
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();