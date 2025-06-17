#!/bin/bash
set -e  # Exit immediately if any command fails

timeout=60
elapsed=0

echo "Waiting for PostgreSQL to become available..."

# Set password as environment variable
export PGPASSWORD=postgres

# Wait for PostgreSQL to become available
until psql -h db -p 5432 -U postgres -d users -c '\q' >/dev/null 2>&1; do
  sleep 1
  elapsed=$((elapsed+1))
  echo "Waiting... ($elapsed/$timeout seconds)"
  
  if [ $elapsed -ge $timeout ]; then
    echo "Timeout reached while waiting for PostgreSQL"
    echo "Last connection attempt output:"
    psql -h db -p 5432 -U postgres -d users -c '\q'  # Show actual error
    exit 1
  fi
done

echo "PostgreSQL connection successful"


echo "Database setup complete"

cd /app
exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload
