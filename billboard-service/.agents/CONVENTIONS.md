# Coding Conventions

These conventions apply to Cinema Platform services and are maintained from `employee-service/agents`.

## Python Style

- Follow PEP 8.
- Format with Black.
- Recommended line length: 88.
- Sort imports with isort (Black profile).
- Add type hints for all public function signatures.
- Add docstrings for public APIs and complex business operations.

## Import Order

1. Standard library
2. Third-party
3. Local application modules

```python
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.employees.domain.entities import Employee
```

## Layer Boundaries

- `domain/`
  - entities, value objects, enums, domain exceptions, repository contracts
  - no FastAPI/SQLAlchemy imports
- `application/`
  - commands, queries, DTOs, use cases
  - orchestration and policy, not framework plumbing
- `infrastructure/`
  - API controllers/dependencies
  - persistence models/repositories
  - external adapters (cache, messaging, grpc)

## Domain Conventions

- Prefer explicit entities/value objects over generic dictionaries.
- Keep invariants inside domain methods or value object validation.
- Use domain-specific exceptions.
- Keep repository interfaces small and intention-revealing.

## Application Conventions

- Commands/queries are lightweight data carriers.
- Use case methods should express intent (`hire`, `approve`, `assign_schedule`).
- One use case should handle one business workflow.
- Keep transaction boundaries explicit in infra/application orchestration.

## Infrastructure Conventions

- SQLAlchemy models map to domain entities via `to_domain()` / `from_domain()`.
- Repositories return domain entities, not ORM objects.
- API schemas validate boundary data and convert to commands/DTOs.
- Keep HTTP error shaping in API layer or global handlers.

## API Conventions

- Resource URLs are plural and stable.
- Use consistent status codes (`201` create, `200` read/update, `204` delete).
- Use pagination for list endpoints.
- Rate limit public endpoints.
- Protect privileged actions with role checks.

## Alembic Conventions

- Use clear migration messages.
- Include indexes and constraints with schema changes.
- Keep migrations deterministic and reversible.
- For seed migrations, prefer explicit values and safe sequence resets.

## Testing Conventions

- Unit tests for domain behavior.
- Repository/integration tests for persistence rules.
- API tests for validation and error responses.
- Name tests by behavior:
  - `test_creates_employee_with_valid_data`
  - `test_returns_404_when_employee_not_found`

## Documentation Conventions

- Update docs whenever architecture or APIs change.
- Keep examples aligned with actual code layout.
- Avoid duplicate guidance in multiple locations.

