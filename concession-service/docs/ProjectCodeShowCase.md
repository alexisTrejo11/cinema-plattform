# Code Showcase

## Code Examples (`CodeExample[]`)

### Example 1: Domain Entity with DDD

- **ID**: "domain-entity"
- **Title**: "Cinema Domain Entity"
- **Description**: "Pure domain model representing a cinema aggregate root with business logic separated from infrastructure"
- **Category**: "Domain-Driven Design"
- **Duration** (optional): ""
- **Views** (optional):
- **Tags** (optional):
  - DDD
  - Domain Entity
  - Clean Architecture

#### Files (`CodeFile[]`)

**File 1:**

- **Name**: "entities.py"
- **Path**: "app/core/cinema/domain/entities.py"
- **Language**: "python"
- **Content**:

  ```python
  from pydantic import Field
  from .base import CinemaBase
  from typing import Optional

  class Cinema(CinemaBase):
      """Domain model representing a cinema with all required fields.

      This is a pure domain entity with no infrastructure concerns.
      It contains business logic and validates domain rules.
      """
      id: Optional[int] = Field(None, description="Unique identifier")
      name: str
      cinema_status: CinemaStatus
      cinema_type: CinemaType
      region: CinemaRegion
      tax_number: str
      screens: int
      has_parking: bool
      has_food_court: bool
      latitude: Optional[Decimal]
      longitude: Optional[Decimal]

      def is_operational(self) -> bool:
          """Business rule: cinema is operational if OPEN and active."""
          return self.cinema_status == CinemaStatus.OPEN and self.is_active
  ```

- **Highlighted**: `true`
- **Explanation**: "Domain entities are pure Python objects with no database or framework dependencies, following DDD principles"

---

### Example 2: Repository Pattern

- **ID**: "repository-pattern"
- **Title**: "Repository Implementation"
- **Description**: "SQLAlchemy repository implementation with data mapper pattern translating between database models and domain entities"
- **Category**: "Data Access"
- **Tags**:
  - Repository Pattern
  - SQLAlchemy
  - Async

#### Files (`CodeFile[]`)

**File 1:**

- **Name**: "repositories.py"
- **Path**: "app/core/cinema/infrastructure/persistence/sqlalchemy/repositories.py"
- **Language**: "python"
- **Content**:

  ```python
  from sqlalchemy import select, func, and_
  from sqlalchemy.ext.asyncio import AsyncSession
  from app.core.cinema.domain.entities import Cinema
  from app.core.cinema.domain.repositories import CinemaRepository
  from app.core.shared.pagination import PaginationParams, Page
  from .models import CinemaModel
  from .mappers import CinemaModelMapper

  class SQLAlchemyCinemaRepository(CinemaRepository):
      """Repository implementation using SQLAlchemy async."""

      def __init__(self, session: AsyncSession):
          self.session = session

      async def find_active(self, params: PaginationParams) -> Page[Cinema]:
          # Count total active cinemas
          count_stmt = (
              select(func.count())
              .select_from(CinemaModel)
              .where(CinemaModel.is_active == True)
          )
          count_result = await self.session.execute(count_stmt)
          total = count_result.scalar() or 0

          # Get paginated active cinemas
          stmt = (
              select(CinemaModel)
              .where(CinemaModel.is_active == True)
              .offset(params.offset)
              .limit(params.limit)
          )

          result = await self.session.execute(stmt)
          models = result.scalars().all()

          # Map database models to domain entities
          cinemas = [CinemaModelMapper.to_domain(model) for model in models]
          return Page.create(items=cinemas, total=total, params=params)

      async def find_by_id(self, entity_id: int) -> Optional[Cinema]:
          model = await self.session.get(CinemaModel, entity_id)
          return CinemaModelMapper.to_domain(model) if model else None
  ```

- **Highlighted**: `true`
- **Explanation**: "Repository abstracts data access and uses mapper to convert SQLAlchemy models to domain entities, maintaining layer separation"

---

### Example 3: Use Case Pattern

- **ID**: "use-case-pattern"
- **Title**: "Use Case Application Layer"
- **Description**: "Application service orchestrating business workflows with caching, validation, and transaction management"
- **Category**: "Application Layer"
- **Tags**:
  - Use Case
  - Application Service
  - Caching

#### Files (`CodeFile[]`)

**File 1:**

- **Name**: "use_cases.py"
- **Path**: "app/core/cinema/application/use_cases.py"
- **Language**: "python"
- **Content**:

  ```python
  from typing import Optional
  from app.core.cinema.domain.repositories import CinemaRepository
  from app.core.cinema.application.dtos import CinemaResponseDTO
  from app.core.cinema.application.mappers import CinemaDTOMapper
  from app.core.shared.exceptions import EntityNotFoundException
  from app.core.cinema.application.cache import cinema_cache

  class GetCinemaByIdUseCase:
      """Retrieve a cinema by ID with caching."""

      def __init__(self, repository: CinemaRepository):
          self.repository = repository
          self.mapper = CinemaDTOMapper()

      @cinema_cache(key_prefix="cinema:id", ttl=300)
      async def execute(self, cinema_id: int) -> CinemaResponseDTO:
          """Execute use case to get cinema by ID.

          Args:
              cinema_id: Unique cinema identifier

          Returns:
              CinemaResponseDTO with cinema details

          Raises:
              EntityNotFoundException if cinema not found
          """
          cinema = await self.repository.find_by_id(cinema_id)

          if not cinema:
              raise EntityNotFoundException(
                  entity_name="Cinema",
                  entity_id=cinema_id
              )

          return self.mapper.to_response_dto(cinema)


  class SearchCinemasUseCase:
      """Search cinemas with filters and pagination."""

      def __init__(self, repository: CinemaRepository):
          self.repository = repository
          self.mapper = CinemaDTOMapper()

      async def execute(
          self,
          params: PaginationParams,
          filters: SearchCinemaFilters
      ) -> Page[CinemaResponseDTO]:
          """Execute search with filters."""
          cinema_page = await self.repository.search(params, filters)

          # Map domain entities to DTOs
          dto_items = [
              self.mapper.to_response_dto(cinema)
              for cinema in cinema_page.items
          ]

          return Page.create(
              items=dto_items,
              total=cinema_page.total,
              params=params
          )
  ```

- **Highlighted**: `true`
- **Explanation**: "Use cases encapsulate business workflows, coordinate repositories, and apply caching decorators for performance"

---

### Example 4: JWT Authentication Middleware

- **ID**: "jwt-middleware"
- **Title**: "JWT Authentication Middleware"
- **Description**: "Middleware extracting and validating JWT tokens, populating request context with user information"
- **Category**: "Security"
- **Tags**:
  - JWT
  - Authentication
  - Middleware

#### Files (`CodeFile[]`)

**File 1:**

- **Name**: "jwt_auth_middleware.py"
- **Path**: "app/config/jwt_auth_middleware.py"
- **Language**: "python"
- **Content**:

  ```python
  import jwt
  from fastapi import Request, HTTPException, status
  from pydantic import BaseModel, Field
  from typing import Optional, Any

  class AuthUserContext(BaseModel):
      """User context extracted from JWT token."""
      user_id: Optional[str] = None
      subject: Optional[str] = None
      email: Optional[str] = None
      username: Optional[str] = None
      roles: list[str] = Field(default_factory=list)
      claims: dict[str, Any] = Field(default_factory=dict)

      @classmethod
      def from_claims(cls, claims: dict[str, Any]) -> "AuthUserContext":
          """Extract user context from JWT claims."""
          roles_raw = claims.get("roles") or claims.get("role") or []

          if isinstance(roles_raw, str):
              roles = [roles_raw]
          elif isinstance(roles_raw, list):
              roles = [str(role) for role in roles_raw]
          else:
              roles = []

          return cls(
              user_id=_first_text_claim(claims, "user_id", "uid", "sub"),
              subject=_first_text_claim(claims, "sub"),
              email=_first_text_claim(claims, "email"),
              username=_first_text_claim(
                  claims, "username", "preferred_username", "name"
              ),
              roles=roles,
              claims=claims,
          )


  async def jwt_auth_middleware(request: Request, call_next):
      """Extract and validate JWT token from Authorization header."""
      auth_header = request.headers.get("Authorization", "")

      if not auth_header.startswith("Bearer "):
          request.state.current_user = None
          return await call_next(request)

      token = auth_header.replace("Bearer ", "")

      try:
          claims = jwt.decode(
              token,
              settings.jwt_secret,
              algorithms=["HS256"]
          )
          request.state.current_user = AuthUserContext.from_claims(claims)
      except jwt.ExpiredSignatureError:
          raise HTTPException(
              status_code=status.HTTP_401_UNAUTHORIZED,
              detail="Token has expired"
          )
      except jwt.InvalidTokenError:
          raise HTTPException(
              status_code=status.HTTP_401_UNAUTHORIZED,
              detail="Invalid token"
          )

      return await call_next(request)
  ```

- **Highlighted**: `true`
- **Explanation**: "Middleware pattern validates JWT tokens and injects user context into request state for downstream use"

---

### Example 5: Role-Based Authorization

- **ID**: "rbac-decorator"
- **Title**: "Role-Based Access Control Decorator"
- **Description**: "Decorator enforcing role-based access control on protected endpoints"
- **Category**: "Security"
- **Tags**:
  - RBAC
  - Authorization
  - Decorator

#### Files (`CodeFile[]`)

**File 1:**

- **Name**: "jwt_auth_middleware.py"
- **Path**: "app/config/jwt_auth_middleware.py"
- **Language**: "python"
- **Content**:

  ```python
  from functools import wraps
  from typing import Callable
  from fastapi import Request, HTTPException, status

  def require_roles(*required_roles: str) -> Callable:
      """Decorator for role-based access control.

      Usage:
          @require_roles("admin", "manager")
          async def protected_endpoint(request: Request):
              # Only admin or manager can access
              pass
      """
      def decorator(func: Callable) -> Callable:
          @wraps(func)
          async def wrapper(*args, **kwargs):
              request: Request = kwargs.get("request")

              if not request or not hasattr(request.state, "current_user"):
                  raise HTTPException(
                      status_code=status.HTTP_401_UNAUTHORIZED,
                      detail="Authentication required"
                  )

              user_roles = request.state.current_user.roles

              if not any(role in user_roles for role in required_roles):
                  raise HTTPException(
                      status_code=status.HTTP_403_FORBIDDEN,
                      detail=f"Requires one of: {', '.join(required_roles)}"
                  )

              return await func(*args, **kwargs)

          return wrapper
      return decorator


  # Usage in controller
  @router.post("/showtimes/", status_code=201)
  @require_roles("admin", "manager")
  async def create_showtime(
      request: Request,
      data: CreateShowtimeDTO
  ):
      """Create new showtime (admin/manager only)."""
      return await use_case.execute(data)
  ```

- **Highlighted**: `true`
- **Explanation**: "Decorator pattern enforces role-based authorization, checking user roles extracted from JWT token"

---

### Example 6: Cache Decorator

- **ID**: "cache-decorator"
- **Title**: "Cache-Aside Pattern Decorator"
- **Description**: "Decorator implementing cache-aside pattern with Redis for performance optimization"
- **Category**: "Performance"
- **Tags**:
  - Caching
  - Redis
  - Performance

#### Files (`CodeFile[]`)

**File 1:**

- **Name**: "cache.py"
- **Path**: "app/core/cinema/application/cache.py"
- **Language**: "python"
- **Content**:

  ```python
  from functools import wraps
  from typing import Callable, Optional
  import json
  from redis.asyncio import Redis

  def cinema_cache(key_prefix: str, ttl: int = 300):
      """Cache decorator for cinema use cases.

      Args:
          key_prefix: Prefix for cache key
          ttl: Time to live in seconds (default 5 minutes)
      """
      def decorator(func: Callable) -> Callable:
          @wraps(func)
          async def wrapper(self, *args, **kwargs):
              # Generate cache key from arguments
              cache_key = f"{key_prefix}:{args[0]}" if args else key_prefix

              # Try to get from cache
              redis: Redis = await get_redis_client()
              cached_value = await redis.get(cache_key)

              if cached_value:
                  # Cache hit - deserialize and return
                  return json.loads(cached_value)

              # Cache miss - execute function
              result = await func(self, *args, **kwargs)

              # Store in cache with TTL
              await redis.setex(
                  cache_key,
                  ttl,
                  json.dumps(result.model_dump())
              )

              return result

          return wrapper
      return decorator


  # Usage in use case
  class GetCinemaByIdUseCase:
      @cinema_cache(key_prefix="cinema:id", ttl=300)
      async def execute(self, cinema_id: int) -> CinemaResponseDTO:
          # This result will be cached for 5 minutes
          cinema = await self.repository.find_by_id(cinema_id)
          return self.mapper.to_response_dto(cinema)
  ```

- **Highlighted**: `true`
- **Explanation**: "Cache-aside pattern with decorator checks Redis before executing function, storing result on cache miss"

---

### Example 7: Pagination Pattern

- **ID**: "pagination"
- **Title**: "Cursor-Based Pagination"
- **Description**: "Reusable pagination pattern with offset/limit and total count for API responses"
- **Category**: "API Design"
- **Tags**:
  - Pagination
  - API
  - Performance

#### Files (`CodeFile[]`)

**File 1:**

- **Name**: "pagination.py"
- **Path**: "app/core/shared/pagination.py"
- **Language**: "python"
- **Content**:

  ```python
  from typing import Generic, TypeVar, List
  from pydantic import BaseModel, Field

  T = TypeVar("T")

  class PaginationParams(BaseModel):
      """Pagination request parameters."""
      offset: int = Field(0, ge=0, description="Number of items to skip")
      limit: int = Field(10, ge=1, le=100, description="Max items per page")

      @property
      def page_number(self) -> int:
          """Calculate current page number."""
          return (self.offset // self.limit) + 1


  class Page(BaseModel, Generic[T]):
      """Generic paginated response."""
      items: List[T] = Field(description="List of items for current page")
      total: int = Field(description="Total number of items")
      offset: int = Field(description="Current offset")
      limit: int = Field(description="Items per page")
      has_next: bool = Field(description="Whether next page exists")
      has_previous: bool = Field(description="Whether previous page exists")

      @classmethod
      def create(
          cls,
          items: List[T],
          total: int,
          params: PaginationParams
      ) -> "Page[T]":
          """Create paginated response."""
          return cls(
              items=items,
              total=total,
              offset=params.offset,
              limit=params.limit,
              has_next=(params.offset + params.limit) < total,
              has_previous=params.offset > 0
          )


  # Usage in API
  @router.get("/cinemas/active/")
  async def get_active_cinemas(
      offset: int = 0,
      limit: int = 10
  ) -> Page[CinemaResponseDTO]:
      params = PaginationParams(offset=offset, limit=limit)
      return await use_case.execute(params)
  ```

- **Highlighted**: `true`
- **Explanation**: "Generic pagination pattern provides consistent structure across all API endpoints with total count and navigation flags"

---

### Example 8: Global Exception Handling

- **ID**: "exception-handling"
- **Title**: "Centralized Exception Handler"
- **Description**: "FastAPI exception handlers providing consistent error responses across all endpoints"
- **Category**: "Error Handling"
- **Tags**:
  - Exceptions
  - API
  - Error Handling

#### Files (`CodeFile[]`)

**File 1:**

- **Name**: "global_exception_handler.py"
- **Path**: "app/config/global_exception_handler.py"
- **Language**: "python"
- **Content**:

  ```python
  from fastapi import Request, status
  from fastapi.responses import JSONResponse
  from fastapi.exceptions import RequestValidationError
  from app.core.shared.exceptions import (
      DomainException,
      ApplicationException,
      EntityNotFoundException
  )

  async def domain_exception_handler(
      request: Request,
      exc: DomainException
  ) -> JSONResponse:
      """Handle domain-specific business rule violations."""
      return JSONResponse(
          status_code=status.HTTP_400_BAD_REQUEST,
          content={
              "error": {
                  "code": exc.error_code,
                  "message": exc.message,
                  "details": exc.details
              }
          }
      )


  async def not_found_exception_handler(
      request: Request,
      exc: EntityNotFoundException
  ) -> JSONResponse:
      """Handle entity not found errors."""
      return JSONResponse(
          status_code=status.HTTP_404_NOT_FOUND,
          content={
              "error": {
                  "code": "NOT_FOUND",
                  "message": str(exc),
                  "entity": exc.entity_name,
                  "id": exc.entity_id
              }
          }
      )


  async def validation_exception_handler(
      request: Request,
      exc: RequestValidationError
  ) -> JSONResponse:
      """Handle Pydantic validation errors."""
      errors = []
      for error in exc.errors():
          errors.append({
              "field": ".".join(str(loc) for loc in error["loc"]),
              "message": error["msg"],
              "type": error["type"]
          })

      return JSONResponse(
          status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
          content={
              "error": {
                  "code": "VALIDATION_ERROR",
                  "message": "Invalid request data",
                  "validation_errors": errors
              }
          }
      )


  # Register handlers in FastAPI app
  exception_handlers = {
      DomainException: domain_exception_handler,
      EntityNotFoundException: not_found_exception_handler,
      RequestValidationError: validation_exception_handler
  }
  ```

- **Highlighted**: `true`
- **Explanation**: "Centralized exception handling ensures consistent error responses with proper HTTP status codes and detailed error information"
