# Project Features

## Feature List (`ProjectFeature[]`)

### Feature 1: Cinema Management

- **ID**: "cinema-management"
- **Title**: "Multi-Location Cinema Management"
- **Description**: "Comprehensive cinema chain management system supporting multiple locations with detailed metadata including amenities, social media links, geographic coordinates, and regional classification."
- **Icon**: "🎬"
- **Category** (`FeatureCategory`): `database`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Multi-region support (CDMX metropolitan area)
  - Cinema types: VIP, Traditional
  - Amenities tracking: parking, food court, coffee station, disability access
  - Social media integration (Facebook, Instagram, X/Twitter, TikTok)
  - Geographic coordinates for location mapp.g
  - Soft delete with restoration capabilities
- **Tech Stack** (optional):
  - FastAPI REST controllers
  - SQLAlchemy async ORM
  - PostgreSQL with JSONB support
  - Redis caching layer
- **Metrics** (optional, `FeatureMetric[]`):
  - **Label**: "API Response Time"
  - **Value**: "<50ms (cached)"
  - **Trend** (optional): `stable`
  - **Icon** (optional): "⚡"
- **Code Snippet** (optional, `CodeSnippet`):
  - **Language**: "python"
  - **Filename** (optional): "cinema/domain/entities.py"
  - **Code**:
    ```python
    @dataclass
    class Cinema:
        """Cinema aggregate root entity."""
        id: Optional[int]
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
    ```

---

### Feature 2: Movie Catalog Management

- **ID**: "movie-catalog"
- **Title**: "Movie Exhibition & Catalog Management"
- **Description**: "Complete movie catalog system with multi-language support, genre classification, rating management, and projection period tracking for current and upcoming exhibitions."
- **Icon**: "🎥"
- **Category** (`FeatureCategory`): `database`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Genre classification (Action, Comedy, Drama, Romance, Thriller, Sci-Fi, Horror, Animation)
  - Rating system (G, PG, PG-13, R, NC-17)
  - Projection period management (start/end dates)
  - Multi-language metadata (original title, local title)
  - Trailer and poster URL integration
  - Soft delete with restoration
- **Tech Stack**:
  - FastAPI async endpoints
  - PostgreSQL with date range indexing
  - Redis caching for active movies
- **Metrics**:
  - **Label**: "Cache Hit Rate"
  - **Value**: "85%+"
  - **Trend**: `up`
  - **Icon**: "📊"

---

### Feature 3: Theater Management

- **ID**: "theater-management"
- **Title**: "Multi-Theater Screen Management"
- **Description**: "Theater inventory management supporting multiple screen types, capacity tracking, maintenance mode, and seat mapp.g integration."
- **Icon**: "🎪"
- **Category** (`FeatureCategory`): `database`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Theater types: 2D, 3D, IMAX, 4DX, VIP
  - Capacity management per theater
  - Maintenance mode flag
  - Linked to cinema locations
  - Seat inventory integration
  - Soft delete support
- **Tech Stack**:
  - SQLAlchemy relationships (Cinema ↔ Theater)
  - Composite indexing for performance
  - Cascade delete handling

---

### Feature 4: Seat Inventory Management

- **ID**: "seat-inventory"
- **Title**: "Theater Seat Mapp.g & Inventory"
- **Description**: "Detailed seat-level inventory management with multiple seat types, maintenance tracking, and grid-based layout (row/number) for accurate theater mapp.g."
- **Icon**: "💺"
- **Category** (`FeatureCategory`): `database`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - 6 seat types: Standard, VIP, Accessible, Premium, 4DX, Loveseat
  - Grid-based layout (row + seat number)
  - Maintenance tracking per seat
  - Unique constraint per theater location
  - Active/inactive status management
- **Tech Stack**:
  - PostgreSQL unique constraints
  - Enum-based seat types
  - Foreign key cascade deletes

---

### Feature 5: Showtime Scheduling & Lifecycle

- **ID**: "showtime-scheduling"
- **Title**: "Advanced Showtime Scheduling System"
- **Description**: "Complete showtime lifecycle management from draft creation to completion with status transitions, multi-language support, pricing, and format selection."
- **Icon**: "📅"
- **Category** (`FeatureCategory`): `database`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Status lifecycle: DRAFT → UPCOMING → IN_PROGRESS → COMPLETED/CANCELLED
  - Launch and cancel operations (manager/admin only)
  - Multi-language support (6 languages including dubbing/original)
  - Multiple formats: 2D, 3D, IMAX, 4DX, VIP
  - Pricing per showtime
  - Time-based filtering and search
  - Seat availability integration
- **Tech Stack**:
  - State machine pattern for status transitions
  - Role-based authorization
  - Time-indexed queries
- **Metrics**:
  - **Label**: "Avg Scheduling Time"
  - **Value**: "<2s"
  - **Trend**: `stable`
  - **Icon**: "⏱️"
- **Code Snippet**:
  - **Language**: "python"
  - **Filename**: "showtime/application/use_cases.py"
  - **Code**:
    ```python
    class LaunchShowtimeUseCase:
        """Transition showtime from DRAFT to UPCOMING."""
        async def execute(self, showtime_id: int) -> ShowtimeDTO:
            showtime = await self.repository.get_by_id(showtime_id)
            if showtime.status != ShowtimeStatus.DRAFT:
                raise InvalidStatusTransitionException()
            showtime.status = ShowtimeStatus.UPCOMING
            updated = await self.repository.update(showtime)
            return self.mapp..to_dto(updated)
    ```

---

### Feature 6: JWT Authentication & Authorization

- **ID**: "jwt-auth"
- **Title**: "JWT-Based Authentication & RBAC"
- **Description**: "Secure authentication using JSON Web Tokens with role-based access control for admin and manager operations."
- **Icon**: "🔐"
- **Category** (`FeatureCategory`): `security`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Bearer token authentication
  - JWT validation with HS256 algorithm
  - Role extraction from token claims
  - Role-based endpoint protection (admin, manager)
  - Request context injection
  - 401 Unauthorized for invalid tokens
- **Tech Stack**:
  - PyJWT library
  - FastAPI middleware
  - Decorator-based authorization
- **Code Snippet**:
  - **Language**: "python"
  - **Filename**: "config/jwt_auth_middleware.py"
  - **Code**:
    ```python
    def require_roles(*required_roles: str):
        """Decorator for role-based access control."""
        def decorator(func):
            async def wrapp.(*args, **kwargs):
                request = kwargs.get("request")
                user_roles = request.state.current_user.roles
                if not any(role in user_roles for role in required_roles):
                    raise HTTPException(status_code=403)
                return await func(*args, **kwargs)
            return wrapp.
        return decorator
    ```

---

### Feature 7: Redis Caching Layer

- **ID**: "redis-caching"
- **Title**: "High-Performance Redis Caching"
- **Description**: "Cache-aside pattern implementation using Redis for sub-50ms response times on frequently accessed resources."
- **Icon**: "⚡"
- **Category** (`FeatureCategory`): `caching`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Decorator-based caching
  - TTL-based expiration
  - Automatic cache invalidation on mutations
  - Cache key generation per use case
  - Async Redis client
  - Connection pooling
- **Tech Stack**:
  - Redis 7 Alpine
  - fastapi-cache library
  - Async connection pool
- **Metrics**:
  - **Label**: "Cache Hit Rate"
  - **Value**: "85%"
  - **Trend**: `up`
  - **Icon**: "🎯"

---

### Feature 8: Rate Limiting

- **ID**: "rate-limiting"
- **Title**: "Token Bucket Rate Limiting"
- **Description**: "IP-based rate limiting to prevent abuse and ensure fair resource usage across all API endpoints."
- **Icon**: "🚦"
- **Category** (`FeatureCategory`): `security`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - IP-based rate limiting
  - 60 requests/minute for read operations
  - 10 requests/minute for write operations
  - 429 Too Many Requests response
  - Configurable per endpoint
  - SlowAPI integration
- **Tech Stack**:
  - SlowAPI library
  - In-memory token bucket
  - FastAPI middleware

---

### Feature 9: Advanced Search & Filtering

- **ID**: "advanced-search"
- **Title**: "Multi-Criterion Search Engine"
- **Description**: "Powerful search capabilities across all domains with multiple filters, time-based queries, and cursor-based pagination."
- **Icon**: "🔍"
- **Category** (`FeatureCategory`): `api`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Multi-field search (name, type, region, status)
  - Time-based filtering (date ranges, time slots)
  - Status filtering (active, maintenance, deleted)
  - Cursor-based pagination
  - Sorting capabilities
  - Optimized database indexes
- **Tech Stack**:
  - SQLAlchemy query builders
  - PostgreSQL composite indexes
  - Pydantic query models

---

### Feature 10: Structured Logging & Monitoring

- **ID**: "structured-logging"
- **Title**: "Colorized Structured Logging"
- **Description**: "Comprehensive logging system with request/response tracking, error monitoring, and colorized console output for development."
- **Icon**: "📝"
- **Category** (`FeatureCategory`): `monitoring`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Structured JSON logs
  - Request/response logging middleware
  - Colorized console output (colorlog)
  - Error stack traces
  - Performance timing
  - Correlation IDs for request tracking
- **Tech Stack**:
  - Python logging module
  - Colorlog library
  - FastAPI middleware

---

### Feature 11: Global Exception Handling

- **ID**: "exception-handling"
- **Title**: "Centralized Exception Management"
- **Description**: "Unified exception handling with domain-specific errors, validation messages, and proper HTTP status code mapp.g."
- **Icon**: "🛡️"
- **Category** (`FeatureCategory`): `api`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Domain-specific exceptions
  - Validation error formatting
  - HTTP status code mapp.g
  - Error detail structures
  - Security-conscious error messages
  - Exception logging
- **Tech Stack**:
  - FastAPI exception handlers
  - Custom exception hierarchy
  - Pydantic validation errors

---

### Feature 12: Database Migrations

- **ID**: "db-migrations"
- **Title**: "Version-Controlled Database Migrations"
- **Description**: "Alembic-based migration system for reliable database schema evolution with automatic migration on deployment."
- **Icon**: "🗄️"
- **Category** (`FeatureCategory`): `database`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Alembic migration framework
  - Version-controlled schema changes
  - Automatic migration on startup
  - Rollback capabilities
  - Seed data management
  - Index optimization
- **Tech Stack**:
  - Alembic 1.12+
  - PostgreSQL DDL
  - Docker entrypoint integration

---

### Feature 13: Scheduled Cron Jobs

- **ID**: "cron-jobs"
- **Title**: "Automated Scheduled Tasks"
- **Description**: "Background job system for automated showtime status updates, seat availability sync, and maintenance tasks."
- **Icon**: "⏰"
- **Category** (`FeatureCategory`): `integration`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Showtime status auto-transitions (UPCOMING → IN_PROGRESS → COMPLETED)
  - Seat availability synchronization
  - Cache warming jobs
  - Database cleanup tasks
  - Configurable schedules
  - Error handling and retries
- **Tech Stack**:
  - APScheduler or similar
  - Async task execution
  - Database transactions
- **Metrics**:
  - **Label**: "Job Success Rate"
  - **Value**: "99.5%"
  - **Trend**: `stable`
  - **Icon**: "✅"

---

### Feature 14: Docker Containerization

- **ID**: "docker-deployment"
- **Title**: "Production-Ready Docker Setup"
- **Description**: "Multi-stage Docker builds with health checks, non-root execution, and orchestrated deployment via Docker Compose."
- **Icon**: "🐳"
- **Category** (`FeatureCategory`): `integration`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Multi-stage builds (builder + runtime)
  - Non-root user execution
  - Health checks for all services
  - Volume persistence
  - Environment-based configuration
  - Gunicorn with Uvicorn workers
- **Tech Stack**:
  - Docker multi-stage builds
  - Docker Compose v3
  - Gunicorn 20.1+
  - Uvicorn workers (4 default)
