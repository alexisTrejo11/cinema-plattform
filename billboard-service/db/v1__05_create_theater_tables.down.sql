DROP TABLE IF EXISTS theater_seats;
DROP TRIGGER IF EXISTS trg_theaters_updated_at ON theaters;
DROP TABLE IF EXISTS theaters;
DROP TYPE IF EXISTS seat_type_enum;
DROP TYPE IF EXISTS theater_type_enum;
DROP FUNCTION IF EXISTS update_timestamp();