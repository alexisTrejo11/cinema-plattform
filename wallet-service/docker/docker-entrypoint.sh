#!/bin/sh
set -eu

mode=${1:-serve}
max_attempts=${MIGRATION_MAX_ATTEMPTS:-20}
delay_seconds=${MIGRATION_RETRY_DELAY:-3}

run_migrations() {
  attempt=1
  while true; do
    if alembic upgrade head; then
      break
    fi
    if [ "$attempt" -ge "$max_attempts" ]; then
      echo "Failed to run migrations after $max_attempts attempts" >&2
      exit 1
    fi
    echo "Migration attempt ${attempt} failed, retrying in ${delay_seconds}s..." >&2
    attempt=$((attempt + 1))
    sleep "$delay_seconds"
  done
}

case "$mode" in
  migrate)
    run_migrations
    ;;
  serve)
    run_migrations
    exec python main.py
    ;;
  serve-grpc)
    run_migrations
    exec python -m app.grpc_server
    ;;
  *)
    exec "$@"
    ;;
esac
