# 🎬 Cinema Platform - Coding Conventions

> Detailed coding standards and patterns for microservices development

---

## 📋 Table of Contents

1. [Python Style Guide](#python-style-guide)
2. [Code Organization](#code-organization)
3. [Domain Patterns](#domain-patterns)
4. [Application Layer Patterns](#application-layer-patterns)
5. [Infrastructure Patterns](#infrastructure-patterns)
6. [API Design Patterns](#api-design-patterns)
7. [Error Handling](#error-handling)
8. [Async Programming](#async-programming)
9. [Testing Patterns](#testing-patterns)
10. [Code Examples](#code-examples)

---

## 🐍 Python Style Guide

### PEP 8 Compliance

- **Line Length**: Maximum 120 characters
- **Indentation**: 4 spaces (no tabs)
- **Blank Lines**: 2 blank lines between top-level definitions
- **Import Order**: Standard library → Third-party → Local application

```python
# Correct import order
import os
import logging
from typing import Optional

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.users.domain import User
```

### Type Hints

**Always use type hints** for function signatures and class attributes:

```python
# ✅ Good
async def get_user(user_id: int) -> User | None:
    ...

class UserRepository:
    async def create(self, user: User) -> User:
        ...
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        ...
```

```python
# ❌ Bad
async def get_user(user_id):
    ...

class UserRepository:
    async def create(self, user):
        ...
```

### Docstrings

Use docstrings for public APIs:

```python
async def get_user(user_id: int) -> User | None:
    """
    Retrieve a user by their ID.
    
    Args:
        user_id: The unique identifier of the user.
    
    Returns:
        The User entity if found, None otherwise.
    
    Raises:
        UserNotFoundError: If the user does not exist.
    """
    ...
```

---

## 📦 Code Organization

### Layer Responsibilities

#### Domain Layer (Innermost)

```python
# app/users/domain/entities.py
from pydantic import BaseModel, Field
from datetime import datetime

class User(BaseModel):
    """Domain entity - no framework imports."""
    
    id: int = 0
    email: str
    name: str
    created_at: datetime = Field(default_factory=datetime.now)
    
    def activate(self) -> None:
        """Domain logic for activation."""
        if self.status == Status.ACTIVE:
            raise UserAlreadyActiveError()
        self.status = Status.ACTIVE
```

#### Application Layer

```python
# app/users/application/commands.py
from dataclasses import dataclass
from datetime import date

@dataclass
class CreateUserCommand:
    email: str
    name: str
    date_of_birth: date
    password: str
```

```python
# app/users/application/use_cases/create_user_usecase.py
class CreateUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    
    async def execute(self, command: CreateUserCommand) -> User:
        user = User.create(command)
        return await self.user_repo.create(user)
```

#### Infrastructure Layer

```python
# app/users/infrastructure/persistence/sqlalchemy_user_repo.py
from sqlalchemy.ext.asyncio import AsyncSession

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, user: User) -> User:
        model = UserModel.from_domain(user)
        self.session.add(model)
        await self.session.commit()
        return model.to_domain()
```

### Dependency Injection Pattern

```python
# app/users/infrastructure/api/dependencies.py
from functools import dependency_injector

def get_user_repository(session: AsyncSession = Depends(get_db)) -> UserRepository:
    return SQLAlchemyUserRepository(session)

def get_user_usecase(
    repo: UserRepository = Depends(get_user_repository)
) -> CreateUserUseCase:
    return CreateUserUseCase(repo)
```

---

## 🏛️ Domain Patterns

### Entity Pattern

```python
# app/users/domain/entities.py
from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from .exceptions import InvalidUserDataError

class User(BaseModel):
    """Core domain entity - immutable once created."""
    
    model_config = {"arbitrary_types_allowed": True}
    
    id: int = 0
    email: str
    name: str
    status: Status = Status.PENDING
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    @model_validator(mode="after")
    def validate_email(self) -> "User":
        if "@" not in self.email:
            raise InvalidUserDataError("Invalid email format")
        return self
    
    def activate(self) -> None:
        """Business logic - activation."""
        self.status = Status.ACTIVE
        self.updated_at = datetime.now()
    
    @classmethod
    def create(cls, data: dict) -> "User":
        """Factory method for creation."""
        return cls(**data)
```

### Value Object Pattern

```python
# app/users/domain/valueobjects.py
from pydantic import BaseModel
from uuid import UUID

class UserId(BaseModel):
    """Value object for user identifier."""
    
    value: UUID
    
    @classmethod
    def generate(cls) -> "UserId":
        return cls(value=UUID.uuid4())
    
    @classmethod
    def from_string(cls, value: str) -> "UserId":
        return cls(value=UUID(value))
    
    def __str__(self) -> str:
        return str(self.value)
```

### Repository Interface Pattern

```python
# app/users/domain/repositories.py
from abc import ABC, abstractmethod
from typing import Optional

class UserRepository(ABC):
    """Repository interface - defined in domain layer."""
    
    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional["User"]:
        """Retrieve user by ID."""
        ...
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional["User"]:
        """Retrieve user by email."""
        ...
    
    @abstractmethod
    async def create(self, user: "User") -> "User":
        """Create a new user."""
        ...
    
    @abstractmethod
    async def update(self, user: "User") -> "User":
        """Update an existing user."""
        ...
    
    @abstractmethod
    async def delete(self, user_id: int) -> None:
        """Delete a user by ID."""
        ...
```

### Enum Pattern

```python
# app/users/domain/enums.py
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    CUSTOMER = "CUSTOMER"
    EMPLOYEE = "EMPLOYEE"
    MANAGER = "MANAGER"

class Status(str, Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    BANNED = "BANNED"
```

### Exception Pattern

```python
# app/users/domain/exceptions.py

class UserNotFoundError(Exception):
    """Raised when a user is not found."""
    def __init__(self, user_id: int | str):
        self.user_id = user_id
        super().__init__(f"User not found: {user_id}")

class UserAlreadyExistsError(Exception):
    """Raised when attempting to create a user that already exists."""
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"User already exists: {email}")

class InvalidUserDataError(Exception):
    """Raised when user data validation fails."""
    def __init__(self, message: str, field: str | None = None):
        self.field = field
        super().__init__(message)
```

---

## 🏗️ Application Layer Patterns

### Command Pattern

```python
# app/users/application/commands.py
from dataclasses import dataclass
from datetime import date

@dataclass
class CreateUserCommand:
    email: str
    name: str
    date_of_birth: date
    password: str

@dataclass
class UpdateUserCommand:
    name: Optional[str] = None
    email: Optional[str] = None

@dataclass
class ActivateUserCommand:
    user_id: int
    activation_token: Optional[str] = None
```

### Query Pattern

```python
# app/users/application/queries.py
from dataclasses import dataclass
from app.shared.pagination import PaginationQuery

@dataclass
class GetUserByIdQuery:
    user_id: int
    include_profile: bool = False

@dataclass
class SearchUsersQuery:
    pagination: PaginationQuery
    role: Optional[str] = None
    status: Optional[str] = None
    email_contains: Optional[str] = None
```

### Use Case Pattern

```python
# app/users/application/use_cases/create_user_usecase.py
from app.users.domain import User
from app.users.domain.repositories import UserRepository
from app.users.domain.exceptions import UserAlreadyExistsError

class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def execute(self, command: CreateUserCommand) -> User:
        existing = await self.user_repository.get_by_email(command.email)
        if existing:
            raise UserAlreadyExistsError(command.email)
        
        user = User.create(command.__dict__)
        return await self.user_repository.create(user)
```

### Container Pattern

```python
# app/users/application/use_cases/container.py
from app.users.domain.repositories import UserRepository
from app.users.application.use_cases.create_user_usecase import CreateUserUseCase
from app.users.application.use_cases.get_user_usecase import GetUserUseCase

class UserUseCases:
    def __init__(self, user_repository: UserRepository):
        self.create = CreateUserUseCase(user_repository)
        self.get = GetUserUseCase(user_repository)
    
    async def create_user(self, command: CreateUserCommand) -> User:
        return await self.create.execute(command)
    
    async def get_user(self, query: GetUserByIdQuery) -> User:
        return await self.get.execute(query)
```

---

## 🏭 Infrastructure Patterns

### SQLAlchemy Model Pattern

```python
# app/users/infrastructure/persistence/models.py
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from app.config.db import Base
from app.users.domain import UserRole, Status

class UserModel(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default=UserRole.CUSTOMER)
    status: Mapped[Status] = mapped_column(SQLEnum(Status), default=Status.PENDING)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_domain(self) -> User:
        return User(
            id=self.id,
            email=self.email,
            name=self.name,
            role=self.role,
            status=self.status,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
    
    @classmethod
    def from_domain(cls, user: User) -> "UserModel":
        return cls(
            id=user.id if user.id != 0 else None,
            email=user.email,
            name=user.name,
            role=user.role,
            status=user.status,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
```

### Repository Implementation Pattern

```python
# app/users/infrastructure/persistence/sqlalchemy_user_repo.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.users.domain import User
from app.users.domain.repositories import UserRepository
from app.users.infrastructure.persistence.models import UserModel

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.session.get(UserModel, user_id)
        return result.to_domain() if result else None
    
    async def get_by_email(self, email: str) -> User | None:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return model.to_domain() if model else None
    
    async def create(self, user: User) -> User:
        model = UserModel.from_domain(user)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model.to_domain()
    
    async def update(self, user: User) -> User:
        model = await self.session.get(UserModel, user.id)
        for key, value in user.__dict__.items():
            if key not in ("id", "created_at"):
                setattr(model, key, value)
        await self.session.commit()
        await self.session.refresh(model)
        return model.to_domain()
    
    async def delete(self, user_id: int) -> None:
        model = await self.session.get(UserModel, user_id)
        if model:
            await self.session.delete(model)
            await self.session.commit()
```

### DTO Pattern

```python
# app/users/application/dto.py
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=1)
    password: str = Field(..., min_length=8)

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    role: str
    status: str
    created_at: datetime
    
    @classmethod
    def from_domain(cls, user: User) -> "UserResponse":
        return cls(
            id=user.id,
            email=user.email,
            name=user.name,
            role=user.role.value,
            status=user.status.value,
            created_at=user.created_at,
        )
```

---

## 🌐 API Design Patterns

### Controller Pattern

```python
# app/users/infrastructure/api/user_controllers.py
from fastapi import APIRouter, Depends, Path, HTTPException, status
from app.config.rate_limit import limiter
from app.users.application.commands import CreateUserCommand
from app.users.application.dto import UserCreate, UserResponse
from app.users.infrastructure.api.dependencies import get_user_usecase

router = APIRouter(prefix="/api/v2/users", tags=["Users"])

@router.get("/{user_id}", response_model=UserResponse)
@limiter.limit("60/minute")
async def get_user(
    user_id: int = Path(..., description="ID of the user"),
    usecase = Depends(get_user_usecase),
):
    user = await usecase.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse.from_domain(user)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def create_user(
    data: UserCreate,
    usecase = Depends(get_user_usecase),
):
    command = CreateUserCommand(**data.model_dump())
    user = await usecase.create_user(command)
    return UserResponse.from_domain(user)
```

### Protected Endpoint Pattern

```python
from app.config.security import require_roles
from app.users.domain import User

@router.post("/users/{user_id}/ban")
@limiter.limit("10/minute")
async def ban_user(
    user_id: int,
    _admin: User = Depends(require_roles("admin")),
    usecase = Depends(get_user_usecase),
):
    await usecase.ban_user(user_id)
    return {"message": f"User {user_id} banned"}
```

---

## ⚠️ Error Handling

### Exception Handler Pattern

```python
# app/config/global_exception_handler.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.users.domain.exceptions import UserNotFoundError, UserAlreadyExistsError

def add_exception_handlers(app: FastAPI):
    @app.exception_handler(UserNotFoundError)
    async def user_not_found_handler(request: Request, exc: UserNotFoundError):
        return JSONResponse(
            status_code=404,
            content={"error": "USER_NOT_FOUND", "message": str(exc)}
        )
    
    @app.exception_handler(UserAlreadyExistsError)
    async def user_exists_handler(request: Request, exc: UserAlreadyExistsError):
        return JSONResponse(
            status_code=400,
            content={"error": "USER_ALREADY_EXISTS", "message": str(exc)}
        )
```

### Result Pattern

```python
# app/shared/response.py
from typing import TypeVar, Generic

T = TypeVar("T")

class Result(Generic[T]):
    def __init__(self, data: T | None = None, error: str | None = None):
        self._data = data
        self._error = error
    
    def is_success(self) -> bool:
        return self._error is None
    
    def get_data(self) -> T:
        if self._error:
            raise ValueError("Cannot get data from failed result")
        return self._data
    
    def get_error_message(self) -> str:
        return self._error or "Unknown error"
    
    @classmethod
    def success(cls, data: T) -> "Result[T]":
        return cls(data=data)
    
    @classmethod
    def error(cls, message: str) -> "Result[T]":
        return cls(error=message)
```

---

## ⚡ Async Programming

### Async Context Managers

```python
# app/config/db.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

engine = create_async_engine(settings.DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

### Async Repository Pattern

```python
async def get_users_by_ids(self, user_ids: list[int]) -> list[User]:
    stmt = select(UserModel).where(UserModel.id.in_(user_ids))
    result = await self.session.execute(stmt)
    models = result.scalars().all()
    return [model.to_domain() for model in models]
```

---

## 🧪 Testing Patterns

### Unit Test Pattern

```python
# app/tests/unit/test_user_entity.py
import pytest
from app.users.domain.entities import User
from app.users.domain.exceptions import InvalidUserDataError

class TestUser:
    def test_create_user_with_valid_data(self):
        user = User.create({"email": "test@example.com", "name": "Test User"})
        assert user.email == "test@example.com"
        assert user.name == "Test User"
    
    def test_create_user_with_invalid_email_raises_error(self):
        with pytest.raises(InvalidUserDataError):
            User.create({"email": "invalid-email", "name": "Test"})
    
    def test_activate_user(self):
        user = User.create({"email": "test@example.com", "name": "Test"})
        user.activate()
        assert user.status == Status.ACTIVE
```

### Integration Test Pattern

```python
# app/tests/integration/test_user_controller.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response = await client.post(
        "/api/v2/users/",
        json={"email": "new@example.com", "name": "New User", "password": "SecurePass123!"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "new@example.com"

@pytest.mark.asyncio
async def test_get_user_not_found(client: AsyncClient):
    response = await client.get("/api/v2/users/99999")
    assert response.status_code == 404
```

---

## 💡 Code Examples

### Complete Domain Entity

```python
# app/users/domain/entities.py
from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from .enums import Status
from .exceptions import InvalidUserDataError

class User(BaseModel):
    model_config = {"arbitrary_types_allowed": True}
    
    id: int = 0
    email: str
    name: str
    status: Status = Status.PENDING
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    @model_validator(mode="after")
    def validate_email(self) -> "User":
        if "@" not in self.email:
            raise InvalidUserDataError("Invalid email format", field="email")
        return self
    
    @classmethod
    def create(cls, data: dict) -> "User":
        return cls(**data)
    
    def activate(self) -> None:
        if self.status == Status.ACTIVE:
            raise InvalidUserDataError("User already active")
        self.status = Status.ACTIVE
        self.updated_at = datetime.now()
    
    def ban(self) -> None:
        self.status = Status.BANNED
        self.updated_at = datetime.now()
```

### Complete Use Case

```python
# app/users/application/use_cases/create_user_usecase.py
from app.users.domain import User
from app.users.domain.repositories import UserRepository
from app.users.domain.exceptions import UserAlreadyExistsError
from app.users.application.commands import CreateUserCommand

class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def execute(self, command: CreateUserCommand) -> User:
        existing = await self.user_repository.get_by_email(command.email)
        if existing:
            raise UserAlreadyExistsError(command.email)
        
        user = User.create(command.__dict__)
        created_user = await self.user_repository.create(user)
        
        return created_user
```

### Complete Controller

```python
# app/users/infrastructure/api/user_controllers.py
from fastapi import APIRouter, Depends, Path, HTTPException, status
from app.config.rate_limit import limiter
from app.config.security import require_roles
from app.users.application.commands import CreateUserCommand
from app.users.application.dto import UserCreate, UserResponse
from app.users.application.use_cases.container import UserUseCases
from app.users.domain import User
from app.users.infrastructure.api.dependencies import get_user_usecase

router = APIRouter(prefix="/api/v2/users", tags=["Users"])

@router.get("/{user_id}", response_model=UserResponse)
@limiter.limit("60/minute")
async def get_user(
    user_id: int = Path(..., description="ID of the user"),
    usecase: UserUseCases = Depends(get_user_usecase),
):
    try:
        user = await usecase.get_by_id(user_id)
        return UserResponse.from_domain(user)
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def create_user(
    data: UserCreate,
    usecase: UserUseCases = Depends(get_user_usecase),
):
    try:
        command = CreateUserCommand(**data.model_dump())
        user = await usecase.create_user(command)
        return UserResponse.from_domain(user)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

---

## ✅ Quick Reference

| Pattern | Location | Key Points |
|---------|----------|------------|
| Entity | `domain/entities.py` | Pydantic, business logic, no framework deps |
| Value Object | `domain/valueobjects.py` | Immutable, defined by attributes |
| Repository Interface | `domain/repositories.py` | ABC, abstract methods only |
| Repository Implementation | `infrastructure/persistence/*.py` | Implements interface |
| Command | `application/commands.py` | Dataclass, input data |
| Query | `application/queries.py` | Dataclass, query parameters |
| Use Case | `application/use_cases/*.py` | Orchestrates domain logic |
| DTO | `application/dto.py` | Pydantic, API boundaries |
| Controller | `infrastructure/api/*.py` | FastAPI routes |
| Model | `infrastructure/persistence/models.py` | SQLAlchemy ORM |
