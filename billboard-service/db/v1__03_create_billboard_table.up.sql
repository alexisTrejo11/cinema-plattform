DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'movie_genre') THEN
        CREATE TYPE movie_genre AS ENUM ('ACTION', 'COMEDY', 'DRAMA', 'ROMANCE', 'THRILLER', 'SCI_FI');
    END IF;
END $$;

DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'movie_rating') THEN
        CREATE TYPE movie_rating AS ENUM ('G', 'PG', 'PG_13', 'R', 'NC_17');
    END IF;
END $$;

CREATE TABLE IF NOT EXISTS movies (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    original_title VARCHAR(200),
    minute_duration INTEGER NOT NULL,
    release_date DATE NOT NULL,
    end_date DATE NOT NULL,
    description TEXT NOT NULL,
    genre movie_genre NOT NULL,
    rating movie_rating NOT NULL,
    poster_url TEXT,
    trailer_url TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_movies_title ON movies(title);
CREATE INDEX IF NOT EXISTS idx_movies_dates ON movies(release_date, end_date);
CREATE INDEX IF NOT EXISTS idx_movies_active ON movies(is_active) WHERE is_active = TRUE;
CREATE INDEX IF NOT EXISTS idx_movies_genre ON movies(genre);
CREATE INDEX IF NOT EXISTS idx_movies_genre_active_dates ON movies(genre, is_active, release_date);

CREATE OR REPLACE FUNCTION update_updated_at_column() 
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS update_movies_updated_at ON movies;

CREATE TRIGGER update_movies_updated_at
BEFORE UPDATE ON movies
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

