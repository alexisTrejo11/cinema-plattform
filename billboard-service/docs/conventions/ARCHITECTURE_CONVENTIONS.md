¡Perfecto! Aquí tienes un template de convenciones en inglés para mantener tu arquitectura simple pero consistente. Puedes guardarlo como `ARCHITECTURE_CONVENTIONS.md` en la raíz de tu proyecto:

# 🏗️ Project Architecture Conventions

## 📁 Directory Structure Template

```
app/
├── core/                               # Business domains (bounded contexts)
│   ├── {domain_name}/                   # e.g., movies, cinema, showtime, theater
│   │   ├── __init__.py
│   │   │
│   │   ├── domain/                      # Business logic layer
│   │   │   ├── __init__.py
│   │   │   ├── entities.py               # Domain entities (business objects)
│   │   │   ├── value_objects.py          # Immutable value objects
│   │   │   ├── enums.py                   # Domain-specific enums
│   │   │   ├── exceptions.py              # Domain exceptions
│   │   │   ├── repositories.py            # Repository interfaces (abstract)
│   │   │   └── services.py                # Domain services (complex business logic)
│   │   │
│   │   ├── application/                  # Application layer
│   │   │   ├── __init__.py
│   │   │   ├── dtos.py                    # Data Transfer Objects
│   │   │   ├── mappers.py                  # Entity <-> DTO mappings
│   │   │   ├── use_cases.py                # ALL use cases in one file (simple)
│   │   │   └── cache.py                    # Domain-specific cache keys/helpers
│   │   │
│   │   └── infrastructure/               # External adapters layer
│   │       ├── __init__.py
│   │       ├── api/                        # HTTP/Controllers layer
│   │       │   ├── __init__.py
│   │       │   ├── dependencies.py          # FastAPI dependencies
│   │       │   └── controllers.py           # ALL endpoints in one file (simple)
│   │       │
│   │       └── persistence/                # Database layer
│   │           ├── __init__.py
│   │           ├── models.py                 # SQLAlchemy models
│   │           ├── mappers.py                 # Model <-> Entity mappings
│   │           └── repositories.py            # Repository implementations
│   │
│   └── shared/                           # Shared kernel (cross-domain code)
│       ├── __init__.py
│       ├── cache/                          # Cache utilities
│       │   ├── __init__.py
│       │   ├── base.py                      # Base cache service
│       │   └── decorators.py                # Cache decorators
│       ├── exceptions.py                    # Global exceptions
│       ├── pagination.py                    # Pagination utilities
│       └── validators.py                     # Shared validation logic
│
├── config/                               # Application configuration
│   ├── __init__.py
│   ├── app_config.py                       # Pydantic settings
│   ├── cache_config.py                      # Redis/Cache setup
│   ├── database.py                          # Database connection
│   ├── exceptions.py                        # Global exception handlers
│   ├── logging.py                           # Logging configuration
│   └── middleware.py                         # Global middleware
│
├── main.py                                # FastAPI application entry point
└── __init__.py
```

## 📝 Naming Conventions

### 1. **File Names** (use snake_case)
| Type | Convention | Example |
|------|------------|---------|
| Domain files | `{entity}_file.py` | `movie_entity.py`, `seat_value_object.py` |
| Application files | `{purpose}.py` | `use_cases.py`, `dtos.py`, `mappers.py` |
| Infrastructure files | `{technology}_{purpose}.py` | `sqlalchemy_models.py`, `fastapi_controllers.py` |
| Test files | `test_{module}.py` | `test_movie_use_cases.py` |

### 2. **Class Names** (use PascalCase)
| Type | Convention | Example |
|------|------------|---------|
| Entities | `{EntityName}` | `Movie`, `Cinema`, `ShowTime` |
| DTOs | `{EntityName}{Purpose}DTO` | `MovieCreateDTO`, `MovieResponseDTO` |
| Use Cases | `{Action}{EntityName}UseCase` | `CreateMovieUseCase`, `GetMovieUseCase` |
| Repositories | `{EntityName}Repository` | `MovieRepository`, `CinemaRepository` |
| Mappers | `{EntityName}Mapper` | `MovieMapper`, `ShowTimeMapper` |
| Controllers | `{EntityName}Controller` | `MovieController`, `CinemaController` |

### 3. **Function/Method Names** (use snake_case)
| Type | Convention | Example |
|------|------------|---------|
| Use case methods | `execute()` | Always use `execute()` for consistency |
| Repository methods | `{action}_{entity}` | `get_movie()`, `create_cinema()`, `delete_showtime()` |
| Controller endpoints | `{action}_{entity}` | `get_movies()`, `create_cinema()`, `update_showtime()` |
| Helper functions | descriptive verb | `validate_date()`, `calculate_price()`, `format_response()` |

## 🎯 Simple Architecture Rules

### **Rule 1: One file per layer (simple approach)**
```
domain/
├── entities.py      # All domain entities
├── repositories.py  # All repository interfaces
└── services.py      # All domain services

application/
├── use_cases.py     # All use cases
├── dtos.py          # All DTOs
└── mappers.py       # All mappers

infrastructure/
├── api/
│   └── controllers.py  # All endpoints
└── persistence/
    ├── models.py       # All DB models
    └── repositories.py # All repository implementations
```

### **Rule 2: Naming consistency across domains**
```python
# GOOD - Consistent pattern
movies/application/use_cases.py
cinema/application/use_cases.py  
showtime/application/use_cases.py
theater/application/use_cases.py

# BAD - Inconsistent
movies/application/use_cases.py
cinema/application/usecases.py
showtime/application/use-cases.py
theater/application/use_case.py
```

### **Rule 3: Import conventions**
```python
# Domain imports domain (OK)
from app.core.movies.domain.entities import Movie
from app.core.movies.domain.repositories import MovieRepository

# Application imports domain (OK)
from app.core.movies.application.dtos import MovieDTO
from app.core.movies.application.use_cases import CreateMovieUseCase

# Infrastructure imports everything (OK)
from app.core.movies.infrastructure.api.controllers import router
from app.core.movies.infrastructure.persistence.models import MovieModel

# Never import infrastructure into domain (❌)
from app.core.movies.infrastructure.persistence.models import MovieModel  # DON'T
```

## 🔧 Standard File Templates

### **domain/entities.py**
```python
"""Domain entities for {domain_name} bounded context."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class {EntityName}:
    """Domain entity representing a {entity_description}."""
    id: Optional[int]
    name: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    def update(self, **kwargs) -> None:
        """Update entity attributes."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
```

### **application/use_cases.py**
```python
"""Use cases for {domain_name} domain."""
from app.core.{domain_name}.domain.entities import {EntityName}
from app.core.{domain_name}.domain.repositories import {EntityName}Repository
from app.core.{domain_name}.application.dtos import {EntityName}DTO
from app.core.{domain_name}.application.mappers import {EntityName}Mapper

class Create{EntityName}UseCase:
    """Create a new {entity_name}."""
    
    def __init__(self, repository: {EntityName}Repository):
        self.repository = repository
        self.mapper = {EntityName}Mapper()
    
    async def execute(self, data: {EntityName}DTO) -> {EntityName}DTO:
        entity = self.mapper.to_entity(data)
        created = await self.repository.create(entity)
        return self.mapper.to_dto(created)

class Get{EntityName}UseCase:
    """Retrieve a {entity_name} by ID."""
    
    def __init__(self, repository: {EntityName}Repository):
        self.repository = repository
        self.mapper = {EntityName}Mapper()
    
    async def execute(self, entity_id: int) -> {EntityName}DTO:
        entity = await self.repository.get_by_id(entity_id)
        return self.mapper.to_dto(entity) if entity else None
```

### **infrastructure/api/controllers.py**
```python
"""FastAPI controllers for {domain_name} endpoints."""
from fastapi import APIRouter, Depends, HTTPException

from app.core.{domain_name}.application.use_cases import (
    Create{EntityName}UseCase,
    Get{EntityName}UseCase
)
from app.core.{domain_name}.application.dtos import {EntityName}DTO
from app.core.{domain_name}.infrastructure.api.dependencies import (
    get_{entity_name}_repository
)

router = APIRouter(prefix="/{endpoint_prefix}", tags=["{domain_name}"])

@router.post("/", response_model={EntityName}DTO)
async def create_{entity_name}(
    data: {EntityName}DTO,
    use_case: Create{EntityName}UseCase = Depends()
):
    """Create a new {entity_name}."""
    return await use_case.execute(data)

@router.get("/{entity_id}", response_model={EntityName}DTO)
async def get_{entity_name}(
    entity_id: int,
    use_case: Get{EntityName}UseCase = Depends()
):
    """Get {entity_name} by ID."""
    result = await use_case.execute(entity_id)
    if not result:
        raise HTTPException(status_code=404, detail="{EntityName} not found")
    return result
```

## ✅ Quick Checklist for New Modules

- [ ] **Domain**: entities, repositories (interfaces), enums, exceptions
- [ ] **Application**: dtos, mappers, use_cases, cache (if needed)
- [ ] **Infrastructure**: 
  - API: controllers, dependencies
  - Persistence: models, repositories (implementations)
- [ ] **Tests**: test_use_cases.py, test_controllers.py
- [ ] **Naming**: Consistent with conventions above
- [ ] **Imports**: Follow dependency direction (domain ← application ← infrastructure)

---

This template ensures:
- **Simple** but structured approach
- **Consistent** naming across all domains
- **Clear** separation of concerns
- **Easy** onboarding for new developers
- **Scalable** for future growth

Would you like me to help you apply these conventions to any specific part of your project?