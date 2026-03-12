DROP TRIGGER IF EXISTS update_cinemas_updated_at ON cinemas;
DROP TABLE IF EXISTS cinemas;
DROP TYPE IF EXISTS location_region_enum;
DROP TYPE IF EXISTS cinema_type_enum;
DROP TYPE IF EXISTS cinema_status_enum;
DROP FUNCTION IF EXISTS update_updated_at_column();