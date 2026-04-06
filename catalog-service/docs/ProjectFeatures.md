# Project Features

## Feature List (`ProjectFeature[]`)

### Feature 1: Movie Catalog Management

- **ID**: "movie-catalog"
- **Title**: Movie Catalog Management
- **Description**: Complete CRUD operations for movie catalog with search, filtering, and exhibition date management.
- **Icon**: "🎬"
- **Category** (`FeatureCategory`): `api`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Full movie CRUD operations
  - Search by title, genre, rating
  - Get movies in current exhibition
  - Projection date range validation
  - Soft delete support
- **Tech Stack** (optional):
  - FastAPI
  - SQLAlchemy (async)
  - PostgreSQL

---

### Feature 2: Cinema Management

- **ID**: "cinema-management"
- **Title**: Cinema Management
- **Description**: Manage cinema locations with comprehensive details including amenities, location, and contact info.
- **Icon**: "🏠"
- **Category** (`FeatureCategory`): `api`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Cinema CRUD operations
  - Location with coordinates
  - Contact information management
  - Social media links
  - Amenities configuration
  - Soft delete with restore
- **Tech Stack** (optional):
  - FastAPI
  - Pydantic
  - Value Objects (Location, ContactInfo)

---

### Feature 3: Theater Management

- **ID**: "theater-management"
- **Title**: Theater Management
- **Description**: Manage theaters within cinemas with capacity rules and type-based validation.
- **Icon**: "🎭"
- **Category** (`FeatureCategory`): `api`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Theater CRUD operations
  - Capacity validation by theater type (IMAX: 150-300, VIP: 10-50, etc.)
  - Maintenance mode support
  - Cinema-theater relationship
  - Soft delete with restore
- **Tech Stack** (optional):
  - Domain entities with business rules
  - FastAPI

---

### Feature 4: Seat Management

- **ID**: "seat-management"
- **Title**: Seat Management
- **Description**: Manage individual seats within theaters with row/seat number and type classification.
- **Icon**: "💺"
- **Category** (`FeatureCategory`): `api`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Seat CRUD operations
  - Seat type classification (STANDARD, VIP, ACCESSIBLE)
  - Theater-seat relationship
  - Active/inactive seat status

---

### Feature 5: Search & Filtering

- **ID**: "search-filtering"
- **Title**: Search & Filtering
- **Description**: Advanced search and filtering capabilities across movies, cinemas, and theaters.
- **Icon**: "🔍"
- **Category** (`FeatureCategory`): `api`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Multi-field search
  - Pagination support
  - Active/inactive filtering
  - Genre and rating filters (movies)
  - Region and type filters (cinemas)

---

### Feature 6: Role-Based Access Control

- **ID**: "rbac"
- **Title**: Role-Based Access Control
- **Description**: JWT authentication with role enforcement for admin operations.
- **Icon**: "🔒"
- **Category** (`FeatureCategory`): `security`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Admin/manager endpoints for mutations
  - Public read endpoints
  - JWT token validation
  - Role-based middleware

---

### Feature 7: Redis Caching

- **ID**: "caching"
- **Title**: Redis Caching
- **Description**: Redis caching support for frequently accessed catalog data.
- **Icon**: "⚡"
- **Category** (`FeatureCategory`): `caching`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Redis integration via fastapi-cache
  - Cache frequently accessed queries
  - Configurable TTL

---

### Feature 8: gRPC Server

- **ID**: "grpc-server"
- **Title**: gRPC Server
- **Description**: Built-in gRPC server for high-performance inter-service catalog queries.
- **Icon**: "🔗"
- **Category** (`FeatureCategory`): `integration`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Real-time catalog queries from ticket service
  - High-performance binary protocol
  - Embedded in main service
- **Tech Stack** (optional):
  - grpcio
  - protobuf

---

### Feature 9: Rate Limiting

- **Rate Limiting**: "🚦"
- **Category** (`FeatureCategory`): `security`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Per-endpoint rate limits (60/min read, 10/min write)
  - IP-based throttling
  - SlowAPI integration

---

### Feature 10: Pagination

- **ID**: "pagination"
- **Title**: Pagination
- **Description**: Standardized pagination across all list endpoints with offset/limit.
- **Icon**: "📄"
- **Category** (`FeatureCategory`): `api`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Consistent pagination pattern
  - Offset/limit parameters
  - Total count metadata

---

### Feature 11: Soft Delete

- **ID**: "soft-delete"
- **Title**: Soft Delete Pattern
- **Description**: All entities support soft delete with restore capability.
- **Icon**: "🗑️"
- **Category** (`FeatureCategory`): `database`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - deleted_at timestamp
  - Restore functionality
  - Audit trail preservation

---

### Feature 12: Database Persistence

- **ID**: "database-persistence"
- **Title**: Database Persistence
- **Description**: PostgreSQL persistence with SQLAlchemy ORM and async support.
- **Icon**: "🗄️"
- **Category** (`FeatureCategory`): `database`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Async SQLAlchemy with asyncpg
  - Alembic migrations
  - Model-to-entity mapping
  - Soft-delete queries
