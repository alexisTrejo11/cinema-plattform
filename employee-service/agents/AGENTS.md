# 🎬 Cinema Platform - Agent Guide

> Comprehensive guide for creating new microservices following platform conventions

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Project Structure](#project-structure)
3. [Architecture Pattern](#architecture-pattern)
4. [Domain Organization](#domain-organization)
5. [Package Conventions](#package-conventions)
6. [Naming Conventions](#naming-conventions)
7. [Configuration Management](#configuration-management)
8. [Dependencies](#dependencies)
9. [API Design](#api-design)
10. [Database Setup](#database-setup)
11. [Docker Setup](#docker-setup)
12. [Testing](#testing)
13. [Documentation](#documentation)
14. [gRPC Integration](#grpc-integration)

---

## 🚀 Quick Start

### 1. Create Service Directory

```bash
cd cinema-plattform
mkdir my-new-service
cd my-new-service
```

### 2. Initialize Project Structure

```
my-new-service/
├── app/
│   ├── __init__.py
│   ├── config/
│   ├── middleware/
│   ├── [domain_modules]/
│   ├── shared/
│   └── tests/
├── alembic/
├── docker/
├── docs/
├── main.py
├── requirements.txt
├── alembic.ini
├── pytest.ini
└── README.md
```

### 3. Copy Base Configuration Files

```bash
# From user-service or concession-service
cp ../user-service/requirements.txt .
cp ../user-service/alembic.ini .
cp ../user-service/pytest.ini .
cp ../user-service/main.py .
```

---

## 📁 Project Structure

### Standard Directory Layout

```
my-new-service/
├── app/                          # Application code
│   ├── __init__.py
│   ├── config/                   # Configuration module
│   │   ├── __init__.py
│   │   ├── app_config.py       # Pydantic settings
│   │   ├── db/
│   │   │   └── postgres_config.py
│   │   ├── cache_config.py     # Redis configuration
│   │   ├── security.py        # JWT/RBAC
│   │   ├── rate_limit.py      # Rate limiting
│   │   ├── logging.py         # Logging setup
│   │   ├── global_exception_handler.py
│   │   └── [optional] kafka_config.py
│   │
│   ├── middleware/              # HTTP middleware
│   │   ├── __init__.py
│   │   ├── auth_middleware.py
│   │   └── [optional] logging_middleware.py
│   │
│   ├── [domain1]/              # Domain module (e.g., users, products)
│   │   ├── __init__.py
│   │   ├── domain/            # Domain layer (DDD)
│   │   │   ├── __init__.py
│   │   │   ├── entities.py    # Domain entities
│   │   │   ├── valueobjects.py
│   │   │   ├── enums.py
│   │   │   ├── exceptions.py
│   │   │   └── repositories.py # Repository interfaces
│   │   │
│   │   ├── application/       # Application layer (CQRS)
│   │   │   ├── __init__.py
│   │   │   ├── commands.py    # Command objects
│   │   │   ├── queries.py    # Query objects
│   │   │   ├── dtos.py       # Data Transfer Objects
│   │   │   ├── use_cases.py
│   │   │   └── use_cases/
│   │   │       └── container.py
│   │   │
│   │   └── infrastructure/    # Infrastructure layer
│   │       ├── __init__.py
│   │       ├── api/
│   │       │   ├── controllers.py
│   │       │   ├── dto.py
│   │       │   ├── dependencies.py
│   │       │   └── docs_examples.py
│   │       └── persistence/
│   │           ├── models.py
│   │           ├── sqlalchemy_repo.py
│   │           └── mapper.py
│   │
│   ├── [domain2]/
│   │   └── ...
│   │
│   ├── shared/                 # Shared utilities
│   │   ├── __init__.py
│   │   ├── pagination.py
│   │   ├── response.py
│   │   ├── exceptions.py
│   │   └── logging.py
│   │
│   └── tests/                 # Test suite
│       ├── __init__.py
│       ├── conftest.py
│       ├── unit/
│       └── integration/
│
├── alembic/                    # Database migrations
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/
│
├── docker/                     # Docker configuration
│   ├── dockerfile
│   ├── docker-compose.yml
│   ├── docker-entrypoint.sh
│   └── nginx/
│       ├── Dockerfile
│       ├── nginx.conf
│       └── entrypoint.sh
│
├── docs/                      # Documentation
│   ├── ProjectMetadata.md
│   ├── ProjectOverview.md
│   ├── ProjectFeatures.md
│   ├── ProjectArchitectureModel.md
│   ├── InfrastructureModel.md
│   ├── APISchema.md
│   ├── ProjectMetric.md
│   ├── ProjectCodeShowCase.md
│   ├── ProjectLinks.md
│   └── MediaGallerySection.md
│
├── main.py                    # Application entry point
├── requirements.txt
├── alembic.ini
├── pytest.ini
├── README.md
└── [service].proto           # gRPC definitions (if needed)
```

---

## 🏗️ Architecture Pattern

### Hexagonal Architecture (Ports & Adapters)

```
┌─────────────────────────────────────────────────────────────┐
│                      API Layer (FastAPI)                     │
│  Controllers • Middleware • DTOs • Exception Handlers         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                         │
│     Use Cases • Commands/Queries • DTOs • Services          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      Domain Layer                           │
│  Entities • Value Objects • Enums • Repository Interfaces     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                 Infrastructure Layer                         │
│    SQLAlchemy Repositories • Cache • External Services       │
└─────────────────────────────────────────────────────────────┘
```

### Key Principles

1. **Domain Layer is Pure** - No framework dependencies
2. **Repository Interfaces in Domain** - Infrastructure implements them
3. **Use Cases Orchestrate** - Business logic in application layer
4. **DTOs at Boundaries** - Convert between layers
5. **Dependency Injection** - FastAPI's `Depends()` for wiring

---

## 📦 Domain Organization

### Single Domain Example (Simple Service)

```
app/
├── config/
├── middleware/
├── users/                     # Single domain
│   ├── domain/
│   ├── application/
│   └── infrastructure/
└── shared/
```

### Multi-Domain Example (Complex Service)

```
app/
├── config/
├── middleware/
├── users/                    # Users domain
├── profiles/                # Profiles domain
├── subscriptions/           # Subscriptions domain
├── billing/                 # Billing domain
└── shared/
```

---

## 📋 Package Conventions

### `__init__.py` Exports

Always export public interfaces from `__init__.py`:

```python
# app/users/domain/__init__.py
from .entities import User, Account
from .valueobjects import UserId, Email
from .enums import UserRole, Status
from .exceptions import UserNotFoundError

__all__ = [
    "User",
    "Account",
    "UserId",
    "Email",
    "UserRole",
    "Status",
    "UserNotFoundError",
]
```

### `__init__.py` in Application Layer

```python
# app/users/application/__init__.py
from .commands import CreateUserCommand, UpdateUserCommand
from .queries import GetUserByIdQuery, SearchUsersQuery
from .dtos import UserResponse, UserCreate

__all__ = [
    "CreateUserCommand",
    "UpdateUserCommand",
    "GetUserByIdQuery",
    "SearchUsersQuery",
    "UserResponse",
    "UserCreate",
]
```

---

## 🎨 Naming Conventions

### Files

| Type | Convention | Example |
|------|------------|---------|
| Domain entities | `entity_name.py` | `user.py`, `product.py` |
| Value objects | `valueobject_name.py` | `user_id.py`, `money.py` |
| Enums | `enums.py` | `user_status.py` or `enums.py` |
| Repositories | `repository_name.py` | `sqlalchemy_user_repo.py` |
| Controllers | `resource_name.py` or `*_controllers.py` | `user_controllers.py` |
| Use cases | `use_case_name.py` or `*_usecases.py` | `create_user_usecase.py` |
| DTOs | `dto.py` or `dtos.py` | `user_dto.py` |
| Middleware | `*_middleware.py` | `auth_middleware.py` |

### Classes

| Type | Convention | Example |
|------|------------|---------|
| Entities | PascalCase | `class User:` |
| Value Objects | PascalCase | `class UserId:` |
| Enums | PascalCase | `class UserRole:` |
| Repository | PascalCase + Repository | `class SQLAlchemyUserRepository:` |
| Use Case | PascalCase + UseCase | `class CreateUserUseCase:` |
| Controller | PascalCase | `class UserController:` |
| DTO | PascalCase + [Request\|Response] | `class UserResponse:` |
| Command | PascalCase + Command | `class CreateUserCommand:` |
| Query | PascalCase + Query | `class GetUserByIdQuery:` |

### Variables & Functions

| Type | Convention | Example |
|------|------------|---------|
| Variables | snake_case | `user_id`, `is_active` |
| Functions | snake_case | `get_user_by_id()` |
| Private | leading underscore | `_private_method()` |
| Constants | UPPER_SNAKE | `MAX_RETRY_COUNT` |
| Async functions | snake_case | `async def get_user()` |

### API Routes

| Type | Convention | Example |
|------|------------|---------|
| Base path | `/api/v{version}/` | `/api/v2/` |
| Resource | plural, kebab-case | `/api/v2/users/` |
| Nested | kebab-case | `/api/v2/users/{user_id}/orders/` |
| Action | kebab-case | `/api/v2/users/{id}/activate` |

### Database Tables

| Type | Convention | Example |
|------|------------|---------|
| Table name | plural, snake_case | `users`, `product_categories` |
| Column name | snake_case | `user_id`, `created_at` |
| Foreign key | `*_id` | `user_id`, `category_id` |
| Index | `ix_{table}_{column}` | `ix_users_email` |

---

## ⚙️ Configuration Management

### Environment Configuration Pattern

```python
# app/config/app_config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # Application
    API_VERSION: str = "1.0"
    DEBUG_MODE: bool = False
    
    # Database
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    
    # Redis
    REDIS_URL: str
    
    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_AUDIENCE: str | None = None
    JWT_ISSUER: str | None = None
    
    # [Optional] Kafka
    KAFKA_ENABLED: bool = False
    KAFKA_BOOTSTRAP_SERVERS: str = ""
    
    # [Optional] gRPC
    GRPC_HOST: str = "0.0.0.0"
    GRPC_PORT: int = 50051
    
    model_config = SettingsConfigDict(
        env_file="./.env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

@lru_cache()
def get_settings_cached_instance():
    return Settings()

settings = get_settings_cached_instance()
```

### Config Module Exports

```python
# app/config/__init__.py
from .app_config import settings
from .cache_config import get_redis_client, init_cache, close_cache
from .security import AuthUserContext, require_roles
from .rate_limit import limiter
from .logging import setup_logging
from . import global_exception_handler

__all__ = [
    "settings",
    "get_redis_client",
    "init_cache",
    "close_cache",
    "AuthUserContext",
    "require_roles",
    "limiter",
    "setup_logging",
    "global_exception_handler",
]
```

### Environment Variables (.env)

```bash
# Application
API_VERSION=1.0
DEBUG_MODE=false

# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=my_service

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_SECRET_KEY=change-me-to-a-long-random-secret
JWT_ALGORITHM=HS256
JWT_AUDIENCE=
JWT_ISSUER=

# gRPC
GRPC_HOST=0.0.0.0
GRPC_PORT=50051
```

---

## 📦 Dependencies

### requirements.txt Structure

```txt
# FastAPI and dependencies
fastapi[standard]
pydantic
pydantic-settings

# Database and ORM
SQLAlchemy
asyncpg
psycopg2-binary
greenlet

# Caching
fastapi-cache[redis]
redis>=5.0.0

# Testing
pytest
pytest-asyncio
pytest-mock

# Logging
colorlog

# Rate Limiting
slowapi

# Authentication
PyJWT

# HTTP Clients
aiohttp

# Database Migrations
alembic

# Production Server
gunicorn>=20.1.0

# gRPC [Optional]
grpcio
grpcio-tools
```

### Install Pattern

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🌐 API Design

### REST API Conventions

#### URL Structure

```
/api/v{version}/{resource}
/api/v{version}/{resource}/{id}
/api/v{version}/{resource}/{id}/{sub-resource}
```

#### HTTP Methods

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v2/users/` | List resources |
| GET | `/api/v2/users/{id}` | Get single resource |
| POST | `/api/v2/users/` | Create resource |
| PUT | `/api/v2/users/{id}` | Full update |
| PATCH | `/api/v2/users/{id}` | Partial update |
| DELETE | `/api/v2/users/{id}` | Delete resource |

#### Request/Response Patterns

```python
# Standard imports
from fastapi import APIRouter, Depends, Path, Query, status

router = APIRouter(prefix="/api/v2/users", tags=["Users"])

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    description="Retrieves a single user by their unique ID",
)
@limiter.limit("60/minute")
async def get_user(
    user_id: int = Path(..., description="ID of the user"),
    usecase: UserUseCases = Depends(get_user_usecase),
):
    user = await usecase.get_by_id(user_id)
    return UserResponse.from_domain(user)
```

#### Authentication Pattern

```python
from app.config.security import require_roles

# Public endpoint
@router.get("/users/")
async def list_users():
    ...

# Protected endpoint
@router.post("/users/")
async def create_user(
    user_data: UserCreate,
    _admin: User = Depends(require_roles("admin", "manager")),
):
    ...
```

#### Pagination Pattern

```python
from app.shared.pagination import PaginationParams

@router.get("/users/")
async def list_users(
    pagination: PaginationParams = Depends(),
):
    page = await usecase.list(pagination)
    return {
        "items": page.items,
        "total": page.total,
        "page": page.page,
        "page_size": page.page_size,
    }
```

---

## 🗄️ Database Setup

### Alembic Configuration

```ini
# alembic.ini
[alembic]
script_location = alembic
prepend_sys_path = .
version_path_separator = os

sqlalchemy.url = driver://user:pass@localhost/dbname

[post_write_hooks]

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic
```

### Migration File Structure

```python
# alembic/versions/0001_create_users.py
"""create users

Revision ID: 0001
Revises: 
Create Date: 2024-01-15
"""
from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

def downgrade() -> None:
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')
```

### SQLAlchemy Model Pattern

```python
# app/users/infrastructure/persistence/models.py
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.config.db import Base

class UserModel(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    
    def to_domain(self) -> User:
        return User(
            id=self.id,
            email=self.email,
            created_at=self.created_at,
        )
    
    @classmethod
    def from_domain(cls, user: User) -> "UserModel":
        return cls(
            id=user.id if user.id != 0 else None,
            email=user.email,
            created_at=user.created_at,
        )
```

### Repository Pattern

```python
# app/users/domain/repositories.py
from abc import ABC, abstractmethod

class UserRepository(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None: ...
    
    @abstractmethod
    async def create(self, user: User) -> User: ...
    
    @abstractmethod
    async def update(self, user: User) -> User: ...
    
    @abstractmethod
    async def delete(self, user_id: int) -> None: ...

# app/users/infrastructure/persistence/sqlalchemy_repo.py
class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.session.get(UserModel, user_id)
        return result.to_domain() if result else None
```

---

## 🐳 Docker Setup

### Dockerfile (Multi-stage)

```dockerfile
FROM python:3.13-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

FROM python:3.13-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:${PATH}"

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/venv /opt/venv
COPY . .

RUN chmod +x /app/docker/docker-entrypoint.sh

RUN addgroup --system app \
    && adduser --system --ingroup app app \
    && chown -R app:app /app

USER app

EXPOSE 8000 50051

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3)" || exit 1

CMD ["/app/docker/docker-entrypoint.sh", "serve"]
```

### docker-compose.yml

```yaml
name: my-new-service

services:
  redis:
    image: redis:7-alpine
    restart: unless-stopped
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 20

  db:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${DB_NAME:-my_service}
      POSTGRES_USER: ${DB_USER:-postgres}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-postgres}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d my_service"]
      interval: 5s
      timeout: 3s
      retries: 20

  app-1:
    build:
      context: ..
      dockerfile: docker/dockerfile
    image: my-service:local
    restart: unless-stopped
    env_file:
      - ../.env
    environment:
      DATABASE_URL: postgresql+asyncpg://${DB_USER:-postgres}:${DB_PASSWORD:-postgres}@db:5432/${DB_NAME:-my_service}
      REDIS_URL: redis://redis:6379/0
    command: ["/app/docker/docker-entrypoint.sh", "serve"]
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - my_network

  app-2:
    image: my-service:local
    # ... similar config

  app-3:
    image: my-service:local
    # ... similar config

  nginx:
    build:
      context: ./nginx
      dockerfile: Dockerfile
    ports:
      - "80:80"
    depends_on:
      - app-1
      - app-2
      - app-3
    networks:
      - my_network

networks:
  my_network:
    driver: bridge

volumes:
  postgres_data:
```

### docker-entrypoint.sh

```bash
#!/bin/sh
set -eu

mode=${1:-serve}
max_attempts=${MIGRATION_MAX_ATTEMPTS:-20}
delay_seconds=${MIGRATION_RETRY_DELAY_SECONDS:-3}

run_migrations() {
    attempt=1
    while true; do
        if alembic upgrade head; then
            break
        fi
        if [ "$attempt" -ge "$max_attempts" ]; then
            echo "Migration failed after ${attempt} attempts" >&2
            exit 1
        fi
        echo "Migration attempt ${attempt} failed, retrying..." >&2
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
        exec gunicorn main:app \
            --worker-class uvicorn.workers.UvicornWorker \
            --bind 0.0.0.0:8000 \
            --workers "${GUNICORN_WORKERS:-4}"
        ;;
    serve-grpc)
        run_migrations
        exec python -m app.grpc.server
        ;;
    *)
        exec "$@"
        ;;
esac
```

---

## 🧪 Testing

### pytest.ini

```ini
[pytest]
asyncio_mode = auto
pythonpath = .
testpaths = app/tests
```

### conftest.py Pattern

```python
# app/tests/conftest.py
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.config.db import Base

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/test_db"

@pytest_asyncio.fixture(scope="function")
async def engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def session(engine):
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
    await session.close()

@pytest_asyncio.fixture
async def sample_user(session):
    user = UserModel(email="test@example.com")
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
```

### Test Structure

```
app/tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── unit/
│   ├── test_entities.py
│   ├── test_value_objects.py
│   └── test_use_cases.py
├── repository/
│   ├── test_user_repository.py
│   └── conftest.py
└── integration/
    ├── conftest.py          # Integration fixtures
    ├── test_user_controller.py
    └── test_auth_controller.py
```

---

## 📖 Documentation

### Required Documentation Files

```
docs/
├── ProjectMetadata.md        # Project metadata
├── ProjectOverview.md        # Problem, solution, metrics
├── ProjectFeatures.md        # Feature list with details
├── ProjectArchitectureModel.md # Architecture patterns
├── InfrastructureModel.md   # Docker, deployment
├── APISchema.md             # API endpoints
├── ProjectMetric.md         # Performance metrics
├── ProjectCodeShowCase.md    # Code examples
├── ProjectLinks.md          # External links
└── MediaGallerySection.md  # Screenshots/diagrams
```

### README.md Structure

```markdown
# 🎬 Cinema Platform - My Service

> Service description

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)]
[![FastAPI](https://img.shields.io/badge/FastAPI-0.1+-green.svg)]

## Overview
## Features
## Quick Start
## Architecture
## API Documentation
## Testing
## Deployment
## Documentation
```

---

## 🔌 gRPC Integration

### proto File Structure

```protobuf
syntax = "proto3";

package myservice;

service MyService {
  rpc GetEntityById (EntityByIdRequest) returns (EntityReply) {}
  rpc GetEntitiesByIds (EntityByIdsRequest) returns (EntityListReply) {}
}

message EntityByIdRequest {
  string id = 1;
}

message EntityReply {
  bool exists = 1;
  EntityData data = 2;
}
```

### gRPC Server Pattern

```python
# app/grpc/server.py
import asyncio
from grpc import aio
from app.grpc.generated import myservice_pb2_grpc
from app.grpc.servicer import MyServiceGrpcServicer

async def serve(host: str = "0.0.0.0", port: int = 50051) -> None:
    server = aio.server()
    myservice_pb2_grpc.add_MyServiceServicer_to_server(
        MyServiceGrpcServicer(), server
    )
    server.add_insecure_port(f"{host}:{port}")
    await server.start()
    await server.wait_for_termination()

if __name__ == "__main__":
    asyncio.run(serve())
```

### Generate gRPC Code

```bash
python -m grpc_tools.protoc \
    -I. \
    --python_out=. \
    --grpc_python_out=. \
    myservice.proto
```

---

## ✅ Checklist

When creating a new service, ensure:

- [ ] Project structure follows conventions
- [ ] Domain layer has no framework dependencies
- [ ] Repository interfaces in domain layer
- [ ] Infrastructure implements repositories
- [ ] Use cases orchestrate business logic
- [ ] DTOs at API boundaries
- [ ] Configuration via Pydantic Settings
- [ ] Redis caching configured
- [ ] JWT authentication implemented
- [ ] Rate limiting configured
- [ ] Alembic migrations setup
- [ ] Docker multi-stage build configured
- [ ] Health check endpoint
- [ ] Unit tests for domain logic
- [ ] Integration tests for controllers
- [ ] Documentation completed
- [ ] README.md created

---

## 📚 See Also

- [User Service Example](../user-service/)
- [Concession Service Example](../concession-service/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Domain-Driven Design](https://martinfowler.com/tags/domain%20driven%20design.html)
