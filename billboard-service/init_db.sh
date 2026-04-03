#!/bin/bash
set -e  # Exit immediately if any command fails

timeout=60
elapsed=0

DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-5432}
DB_USER=${DB_USER:-postgres}
DB_PASSWORD=${DB_PASSWORD:-postgres}
DB_NAME=${DB_NAME:-cinema_billboard}

echo "Waiting for PostgreSQL to become available..."

# Set password as environment variable
export PGPASSWORD="$DB_PASSWORD"

# Wait for PostgreSQL to become available
until psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c '\q' >/dev/null 2>&1; do
  sleep 1
  elapsed=$((elapsed+1))
  echo "Waiting... ($elapsed/$timeout seconds)"
  
  if [ $elapsed -ge $timeout ]; then
    echo "Timeout reached while waiting for PostgreSQL"
    echo "Last connection attempt output:"
    psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c '\q'  # Show actual error
    exit 1
  fi
done

echo "PostgreSQL connection successful"

# Execute SQL files in order 
#cd /app.b
#cd /app.b
#for sql_file in v1__*.sql; do
#  echo "Executing $sql_file"
#  psql -h db -U postgres -d billboard -f "$sql_file"
#done

#echo "Database setup complete"

exec uvicorn main:fast_api_app.-host 0.0.0.0 --port 8000
