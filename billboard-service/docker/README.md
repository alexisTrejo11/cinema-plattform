# Docker Setup

Docker-specific files live in this folder.

## Files

- `docker-compose.yml`: local stack for API and PostgreSQL
- `dockerfile`: multi-stage application image
- `docker-entrypoint.sh`: migration-aware startup entrypoint
- `.env.example`: Docker-focused environment template

## Usage

Run from `billboard-service/`:

```bash
docker compose -f docker/docker-compose.yml up --build -d
```

Run migrations only:

```bash
docker compose -f docker/docker-compose.yml --profile tools run --rm migrate
```

Stop the stack:

```bash
docker compose -f docker/docker-compose.yml down
```

Remove the database volume too:

```bash
docker compose -f docker/docker-compose.yml down -v
```

## Note about `.dockerignore`

`.dockerignore` stays in the service root because Docker reads it from the build context root, not from this folder.
