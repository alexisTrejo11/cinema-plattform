-- ENUMS
CREATE TYPE showtime_type_enum AS ENUM (
    'TRADITIONAL_2D',
    'TRADITIONAL_3D',
    'IMAX_2D',
    'IMAX_3D',
    '4D',
    '4DX',
    'VIP_2D',
    'VIP_3D'
);

CREATE TYPE showtime_language_enum AS ENUM (
    'ORIGINAL_ENGLISH',
    'ORIGINAL_SPANISH',
    'ORIGINAL_JAPANESE',
    'ORIGINAL_KOREAN',
    'DUBBED_ENGLISH',
    'DUBBED_SPANISH'
);

-- TABLE: Showtimes
CREATE TABLE showtimes (
    id SERIAL PRIMARY KEY,
    movie_id INT NOT NULL,
    theater_id INT NOT NULL,
    cinema_id INT NOT NULL,
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE NOT NULL,
    price NUMERIC(6, 2) NOT NULL,
    language showtime_language_enum NOT NULL, 
    type showtime_type_enum NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_cinema FOREIGN KEY (cinema_id) REFERENCES cinemas (id) ON DELETE CASCADE,
    CONSTRAINT fk_movie FOREIGN KEY (movie_id) REFERENCES movies (id) ON DELETE CASCADE,
    CONSTRAINT fk_theater FOREIGN KEY (theater_id) REFERENCES theaters (id) ON DELETE CASCADE
);

-- INDEX
CREATE INDEX idx_showtimes_movie_id ON showtimes (movie_id);
CREATE INDEX idx_showtimes_theater_id ON showtimes (theater_id);
CREATE INDEX idx_showtimes_theater_time ON showtimes (theater_id, start_time);
CREATE INDEX idx_showtimes_start_time ON showtimes (start_time);

-- EXAMPLE SHOWTIMES : Only Added for Cinema 1
INSERT INTO showtimes (cinema_id, movie_id, theater_id, start_time, end_time, price, type, language)
VALUES (1, 1, 1, '2025-08-03 10:00:00-06', '2025-08-03 12:00:00-06', 10.50, 'TRADITIONAL_2D', 'ORIGINAL_ENGLISH');

INSERT INTO showtimes (cinema_id, movie_id, theater_id, start_time, end_time, price, type, language)
VALUES (1, 2, 2, '2025-08-03 14:30:00-06', '2025-08-03 16:45:00-06', 12.00, 'IMAX_3D', 'DUBBED_SPANISH');

INSERT INTO showtimes (cinema_id, movie_id, theater_id, start_time, end_time, price, type, language)
VALUES (1, 3, 3, '2025-08-04 18:00:00-06', '2025-08-04 20:30:00-06', 9.75, 'TRADITIONAL_3D', 'ORIGINAL_SPANISH');

INSERT INTO showtimes (cinema_id, movie_id, theater_id, start_time, end_time, price, type, language)
VALUES (1, 4, 4, '2025-08-04 21:00:00-06', '2025-08-04 23:15:00-06', 11.25, '4DX', 'ORIGINAL_ENGLISH');

INSERT INTO showtimes (cinema_id, movie_id, theater_id, start_time, end_time, price, type, language)
VALUES (1, 5, 5, '2025-08-05 11:00:00-06', '2025-08-05 13:45:00-06', 13.00, 'VIP_2D', 'ORIGINAL_KOREAN');

INSERT INTO showtimes (cinema_id, movie_id, theater_id, start_time, end_time, price, type, language)
VALUES (1, 6, 6, '2025-08-05 16:00:00-06', '2025-08-05 18:30:00-06', 8.50, 'TRADITIONAL_2D', 'DUBBED_ENGLISH');

INSERT INTO showtimes (cinema_id, movie_id, theater_id, start_time, end_time, price, type, language)
VALUES (1, 7, 7, '2025-08-06 19:30:00-06', '2025-08-06 22:00:00-06', 10.00, 'IMAX_2D', 'ORIGINAL_ENGLISH');

INSERT INTO showtimes (cinema_id, movie_id, theater_id, start_time, end_time, price, type, language)
VALUES (1, 8, 8, '2025-08-06 20:00:00-06', '2025-08-06 22:15:00-06', 9.00, 'TRADITIONAL_3D', 'ORIGINAL_JAPANESE');

INSERT INTO showtimes (cinema_id, movie_id, theater_id, start_time, end_time, price, type, language)
VALUES (1, 9, 9, '2025-08-07 10:30:00-06', '2025-08-07 12:45:00-06', 11.50, 'VIP_3D', 'DUBBED_SPANISH');

INSERT INTO showtimes (cinema_id, movie_id, theater_id, start_time, end_time, price, type, language)
VALUES (1, 10, 10, '2025-08-07 15:00:00-06', '2025-08-07 17:00:00-06', 10.75, '4D', 'ORIGINAL_ENGLISH');