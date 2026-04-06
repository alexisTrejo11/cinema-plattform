# Cinema Platform Agent Guide

This is the canonical guide for creating and evolving services in the Cinema Platform.

## Scope

- Applies to all services in this repository.
- Prefer these conventions over older duplicated guides.
- Keep service-specific details in each service `README.md` and `docs/`.

## Quick Start

1. Create a service folder: `<domain>-service/`.
2. Create standard structure:
  - `app/`
  - `alembic/`
  - `docker/`
  - `docs/`
  - `README.md`, `requirements.txt`, `alembic.ini`, `pytest.ini`
3. Add baseline config and health endpoint.
4. Add first migration and run `alembic upgrade head`.
5. Add basic tests for domain + repository + API.

## Service Structure

```text
<service>-service/
├── app/
│   ├── config/
│   ├── middleware/
│   ├── <domain_a>/
│   │   ├── domain/
│   │   ├── application/
│   │   └── infrastructure/
│   ├── <domain_b>/
│   └── shared/
├── alembic/
│   └── versions/
├── docker/
├── docs/
├── main.py
├── requirements.txt
├── alembic.ini
├── pytest.ini
└── README.md
```

## Architecture Rules

- Use Hexagonal Architecture (Ports and Adapters).
- `domain/` must be framework-agnostic.
- Repository interfaces belong in `domain/`.
- Implement repositories in `infrastructure/persistence/`.
- HTTP routes and DTO mapping belong in `infrastructure/api/`.
- Application layer orchestrates use cases, not persistence details.

## Naming Rules

- Files: `snake_case.py`
- Classes: `PascalCase`
- Functions/variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Tables: plural `snake_case`
- Indexes: `ix_<table>_<column>`
- Enums: upper-case values (`ACTIVE`, `PENDING`, etc.)

## API Rules

- Base path: `/api/v{version}/...`
- Resource names are plural (`/employees`, `/vacation-requests`).
- Use explicit response models.
- Validate input at API boundary.
- Apply rate-limits to exposed endpoints.
- Keep auth in middleware/dependencies, not in domain entities.

## Configuration Rules

- Use `pydantic-settings` for env config.
- Keep defaults safe for local development.
- Never hardcode production secrets.
- Build DB URL from components or a single explicit URL in settings.
- Validate external dependencies at startup when enabled.

## Database Rules

- All schema changes through Alembic migrations.
- Every migration must include `upgrade()` and `downgrade()`.
- Name migrations by intent, e.g. `create_employees_table`.
- Seed/demo migrations should be explicit and idempotent in behavior.

## Testing Rules

- `pytest` with async support.
- Minimum for a new domain:
  - entity/value object tests
  - repository tests
  - one API happy-path and one failure case
- Keep shared fixtures in `app/tests/conftest.py`.

## Docker Rules

- Prefer multi-stage image builds.
- Include health checks.
- Entrypoint should run migrations before serving.
- Compose should use health-based dependency ordering.

## Documentation Rules

- Keep service `README.md` actionable (setup, run, test, migrate).
- Keep `docs/InfrastructureModel.md` and `docs/APISchema.md` updated.
- When architecture changes, update docs in same PR.

## Checklist

- Structure follows this guide
- Domain is framework-agnostic
- Migrations added for schema changes
- Tests added/updated
- Docs updated

