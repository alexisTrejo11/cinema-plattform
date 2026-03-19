# Architecture Model

## 1. Layers (`ArchitectureLayer[]`)

### Layer 1: API Layer

- **Name**: "API Layer (Infrastructure)"
- **Description**: "FastAPI REST controllers handling HTTP requests, response formatting, authentication, and rate limiting"
- **Components**:
  - FastAPI Routers
  - Request/Response DTOs
  - JWT Authentication Middleware
  - Rate Limiting Middleware
  - Logging Middleware
  - Exception Handlers
- **Color**: "#3498db"
- **Expanded** (optional): `true`
- **Responsibilities** (optional):
  - HTTP request validation
  - JWT token verification
  - Rate limit enforcement
  - Response serialization
  - Error formatting
- **Technologies** (optional):
  - FastAPI
  - Pydantic v2
  - SlowAPI
  - PyJWT

---

### Layer 2: Application Layer

- **Name**: "Application Layer"
- **Description**: "Use cases and business workflows orchestrating domain logic and coordinating between repositories"
- **Components**:
  - Use Case Classes
  - Application DTOs
  - Domain Mappers
  - Cache Decorators
  - Transaction Coordinators
- **Color**: "#e74c3c"
- **Expanded** (optional): `true`
- **Responsibilities** (optional):
  - Business workflow orchestration
  - Use case execution
  - Cross-aggregate operations
  - DTO transformation
  - Cache management
- **Technologies** (optional):
  - Python dataclasses
  - Async/await pattern
  - Redis caching

---

### Layer 3: Domain Layer

- **Name**: "Domain Layer (Core Business Logic)"
- **Description**: "Pure business logic with entities, value objects, domain services, and repository interfaces"
- **Components**:
  - Domain Entities
  - Value Objects
  - Repository Interfaces
  - Domain Services
  - Domain Exceptions
  - Business Rules
- **Color**: "#2ecc71"
- **Expanded** (optional): `true`
- **Responsibilities** (optional):
  - Business invariants enforcement
  - Domain model definition
  - Business rule validation
  - Entity lifecycle management
  - Domain event definitions
- **Technologies** (optional):
  - Python dataclasses
  - Abstract base classes
  - Enums

---

### Layer 4: Infrastructure/Persistence Layer

- **Name**: "Infrastructure Layer (Persistence)"
- **Description**: "Database implementations, SQLAlchemy models, repository implementations, and data access"
- **Components**:
  - SQLAlchemy Models
  - Repository Implementations
  - Database Mappers
  - Connection Pool Management
  - Transaction Management
  - Migration Scripts (Alembic)
- **Color**: "#f39c12"
- **Expanded** (optional): `true`
- **Responsibilities** (optional):
  - Data persistence
  - Query execution
  - Transaction management
  - Schema migration
  - Database connection handling
- **Technologies** (optional):
  - SQLAlchemy 2.0 (async)
  - PostgreSQL 16
  - asyncpg driver
  - Alembic

---

## 2. Design Patterns (`DesignPattern[]`)

### Pattern 1: Domain-Driven Design (DDD)

- **Title**: "Domain-Driven Design Architecture"
- **Emoji**: "🏛️"
- **Description**: "Clean architecture with clear separation between domain, application, and infrastructure layers ensuring business logic independence from frameworks"
- **Category**: "Architectural"
- **Badge**: "Core Pattern"

---

### Pattern 2: Repository Pattern

- **Title**: "Repository Pattern"
- **Emoji**: "📚"
- **Description**: "Abstraction layer over data access with interfaces in domain layer and implementations in infrastructure, enabling database-agnostic business logic"
- **Category**: "Data Access"
- **Badge**: "DDD Pattern"

---

### Pattern 3: Data Mapper Pattern

- **Title**: "Data Mapper Pattern"
- **Emoji**: "🔄"
- **Description**: "Decouples database schema from domain models using mapper classes to translate between SQLAlchemy models and domain entities"
- **Category**: "Data Transformation"
- **Badge**: "DDD Pattern"

---

### Pattern 4: Use Case Pattern

- **Title**: "Use Case / Interactor Pattern"
- **Emoji**: "⚙️"
- **Description**: "Each business operation is encapsulated as a single-purpose use case class with an execute() method for consistent application flow"
- **Category**: "Business Logic"
- **Badge**: "Application Pattern"

---

### Pattern 5: Dependency Injection

- **Title**: "Dependency Injection"
- **Emoji**: "💉"
- **Description**: "FastAPI's Depends() mechanism for constructor injection of repositories, use cases, and services promoting testability and loose coupling"
- **Category**: "Structural"
- **Badge**: "Framework Pattern"

---

### Pattern 6: Cache-Aside (Lazy Loading)

- **Title**: "Cache-Aside Pattern"
- **Emoji**: "💾"
- **Description**: "Application checks cache before database, loads on miss, with decorator-based implementation on use case methods"
- **Category**: "Performance"
- **Badge**: "Caching Strategy"

---

### Pattern 7: Middleware Chain

- **Title**: "Middleware Chain Pattern"
- **Emoji**: "🔗"
- **Description**: "Request processing pipeline with authentication, rate limiting, and logging middleware executing in sequence"
- **Category**: "Request Processing"
- **Badge**: "API Pattern"

---

### Pattern 8: Strategy Pattern

- **Title**: "Strategy Pattern (Status Transitions)"
- **Emoji**: "🎯"
- **Description**: "Showtime status transitions encapsulated as strategies with validation rules for state machine behavior"
- **Category**: "Behavioral"
- **Badge**: "Domain Pattern"

---

## 3. Scalability Strategies (`StrategyItem[]`)

### Strategy 1: Horizontal Scaling

- **Title**: "Stateless Service Design"
- **Description**: "API layer is completely stateless enabling horizontal scaling with load balancer distribution across multiple container instances"

---

### Strategy 2: Database Connection Pooling

- **Title**: "Async Connection Pool"
- **Description**: "SQLAlchemy async connection pool with configurable size prevents connection exhaustion under high load"

---

### Strategy 3: Redis Caching Layer

- **Title**: "Distributed Cache"
- **Description**: "Redis cache for frequently accessed data (cinemas, movies, theaters) reduces database load by 85% with sub-50ms latency"

---

### Strategy 4: Database Indexing

- **Title**: "Strategic Indexing"
- **Description**: "Composite indexes on high-query columns (cinema_id+theater_id+start_time) optimize search performance for complex queries"

---

### Strategy 5: Cursor-Based Pagination

- **Title**: "Cursor Pagination"
- **Description**: "Offset-free pagination using cursor tokens prevents performance degradation on deep page navigation"

---

### Strategy 6: Async I/O Throughout

- **Title**: "100% Async Architecture"
- **Description**: "FastAPI + SQLAlchemy async + asyncpg driver maximizes concurrency and throughput under load"

---

## 4. Security Strategies (`StrategyItem[]`)

### Strategy 1: JWT Authentication

- **Title**: "JWT-Based Authentication"
- **Description**: "Stateless Bearer token authentication with HS256 signing validates every request without database lookups"

---

### Strategy 2: Role-Based Access Control (RBAC)

- **Title**: "Role-Based Authorization"
- **Description**: "Decorator-based role checking (@require_roles) protects sensitive endpoints from unauthorized access"

---

### Strategy 3: Rate Limiting

- **Title**: "IP-Based Rate Limiting"
- **Description**: "60 req/min for reads, 10 req/min for writes prevents abuse and DDoS attacks"

---

### Strategy 4: Input Validation

- **Title**: "Pydantic Schema Validation"
- **Description**: "Automatic request validation with Pydantic v2 prevents injection attacks and invalid data"

---

### Strategy 5: Prepared Statements

- **Title**: "SQL Injection Prevention"
- **Description**: "SQLAlchemy Core with parameterized queries prevents SQL injection attacks"

---

### Strategy 6: Non-Root Container Execution

- **Title**: "Least Privilege Principle"
- **Description**: "Docker containers run as non-root user (UID 1000) limiting potential attack surface"

---

## 5. Cache Strategies (`CacheStrategy[]`)

### Cache 1: Cinema Cache

- **Name**: "Cinema Listing Cache"
- **Description**: "Active cinemas cached with 5-minute TTL"
- **TTL**: "300 seconds"
- **Coverage**: "GET /cinemas/active/"

---

### Cache 2: Movie Cache

- **Name**: "Active Movies Cache"
- **Description**: "Current exhibition movies cached with 5-minute TTL"
- **TTL**: "300 seconds"
- **Coverage**: "GET /movies/active/"

---

### Cache 3: Theater Cache

- **Name**: "Theater Inventory Cache"
- **Description**: "Theater configurations cached per cinema with 10-minute TTL"
- **TTL**: "600 seconds"
- **Coverage**: "GET /theaters/cinema/{id}"

---

### Cache 4: Showtime Cache

- **Name**: "Showtime Schedule Cache"
- **Description**: "Upcoming showtimes cached with 2-minute TTL for real-time accuracy"
- **TTL**: "120 seconds"
- **Coverage**: "GET /showtimes/"

---

## 6. Architecture Features (`ArchitectureFeature[]`)

### Feature 1: Async-First Design

- **Title**: "100% Async Architecture"
- **Emoji**: "⚡"
- **Description**: "Fully asynchronous design from API to database using FastAPI, SQLAlchemy 2.0 async, and asyncpg for maximum concurrency"

---

### Feature 2: Domain-Driven Design

- **Title**: "Clean DDD Architecture"
- **Emoji**: "🏛️"
- **Description**: "Strict layer separation with domain, application, and infrastructure layers following DDD principles"

---

### Feature 3: Type Safety

- **Title**: "End-to-End Type Safety"
- **Emoji**: "🔒"
- **Description**: "Pydantic v2 models throughout with Python type hints ensuring compile-time type checking"

---

### Feature 4: Testability

- **Title**: "High Testability"
- **Emoji**: "🧪"
- **Description**: "Dependency injection and repository pattern enable 100% unit test coverage with mocked dependencies"

---

### Feature 5: Observability

- **Title**: "Full Observability"
- **Emoji**: "👁️"
- **Description**: "Structured logging, request tracing, and error monitoring provide complete visibility into system behavior"

---

## 7. Architecture Diagram (`ArchitectureDiagramModel`)

### Legend (`LegendItem[]`)

#### Legend 1:

- **Type**: "client"
- **Label**: "Client Application"
- **Color**: "#3498db"
- **Icon**: "📱"

#### Legend 2:

- **Type**: "gateway"
- **Label**: "API Gateway"
- **Color**: "#e74c3c"
- **Icon**: "🚪"

#### Legend 3:

- **Type**: "service"
- **Label**: "Application Service"
- **Color**: "#2ecc71"
- **Icon**: "⚙️"

#### Legend 4:

- **Type**: "database"
- **Label**: "Data Store"
- **Color**: "#f39c12"
- **Icon**: "🗄️"

---

### Nodes (`DiagramNode[]`)

#### Node 1:

- **ID**: "client"
- **Label**: "Web/Mobile Client"
- **Type**: `client`
- **x**: 100
- **y**: 50
- **Status**: `healthy`

#### Node 2:

- **ID**: "fastapi"
- **Label**: "FastAPI Gateway"
- **Type**: `gateway`
- **x**: 300
- **y**: 50
- **Status**: `healthy`
- **Traffic**: "60 req/min"

#### Node 3:

- **ID**: "cinema-service"
- **Label**: "Cinema Domain"
- **Type**: `service`
- **x**: 500
- **y**: 20
- **Status**: `healthy`

#### Node 4:

- **ID**: "movie-service"
- **Label**: "Movie Domain"
- **Type**: `service`
- **x**: 500
- **y**: 60
- **Status**: `healthy`

#### Node 5:

- **ID**: "showtime-service"
- **Label**: "Showtime Domain"
- **Type**: `service`
- **x**: 500
- **y**: 100
- **Status**: `healthy`

#### Node 6:

- **ID**: "theater-service"
- **Label**: "Theater Domain"
- **Type**: `service`
- **x**: 500
- **y**: 140
- **Status**: `healthy`

#### Node 7:

- **ID**: "postgres"
- **Label**: "PostgreSQL 16"
- **Type**: `database`
- **x**: 700
- **y**: 60
- **Status**: `healthy`

#### Node 8:

- **ID**: "redis"
- **Label**: "Redis Cache"
- **Type**: `database`
- **x**: 700
- **y**: 120
- **Status**: `healthy`

---

### Connections (`DiagramConnection[]`)

#### Connection 1:

- **ID**: "client-api"
- **From**: "client"
- **To**: "fastapi"
- **Label**: "HTTPS/REST"
- **Protocol**: "HTTP/2"
- **Is Active**: `true`

#### Connection 2:

- **ID**: "api-cinema"
- **From**: "fastapi"
- **To**: "cinema-service"
- **Label**: "Use Cases"
- **Protocol**: "Internal"
- **Is Active**: `true`

#### Connection 3:

- **ID**: "api-movie"
- **From**: "fastapi"
- **To**: "movie-service"
- **Label**: "Use Cases"
- **Protocol**: "Internal"
- **Is Active**: `true`

#### Connection 4:

- **ID**: "api-showtime"
- **From**: "fastapi"
- **To**: "showtime-service"
- **Label**: "Use Cases"
- **Protocol**: "Internal"
- **Is Active**: `true`

#### Connection 5:

- **ID**: "api-theater"
- **From**: "fastapi"
- **To**: "theater-service"
- **Label**: "Use Cases"
- **Protocol**: "Internal"
- **Is Active**: `true`

#### Connection 6:

- **ID**: "services-postgres"
- **From**: "cinema-service"
- **To**: "postgres"
- **Label**: "SQL Queries (asyncpg)"
- **Protocol**: "PostgreSQL"
- **Is Active**: `true`

#### Connection 7:

- **ID**: "services-redis"
- **From**: "cinema-service"
- **To**: "redis"
- **Label**: "Cache Operations"
- **Protocol**: "Redis"
- **Is Active**: `true`

---

## 8. Data Flow (`DataFlowModel`)

### Request Flow (`FlowStep[]`)

#### Step 1:

- **Number**: 1
- **Title**: "Client Request"
- **Description**: "Client sends HTTP request with optional JWT Bearer token"
- **Icon**: "📱"

#### Step 2:

- **Number**: 2
- **Title**: "Middleware Chain"
- **Description**: "Request passes through logging → JWT validation → rate limiting middleware"
- **Icon**: "🔗"

#### Step 3:

- **Number**: 3
- **Title**: "Controller Layer"
- **Description**: "FastAPI controller validates request body against Pydantic schema and routes to use case"
- **Icon**: "🚪"

#### Step 4:

- **Number**: 4
- **Title**: "Use Case Execution"
- **Description**: "Application layer executes business workflow, checks cache, and calls repository if needed"
- **Icon**: "⚙️"

#### Step 5:

- **Number**: 5
- **Title**: "Domain Logic"
- **Description**: "Domain entities enforce business rules and invariants"
- **Icon**: "🏛️"

#### Step 6:

- **Number**: 6
- **Title**: "Repository Query"
- **Description**: "Repository implementation queries PostgreSQL via SQLAlchemy async"
- **Icon**: "🗄️"

#### Step 7:

- **Number**: 7
- **Title**: "Data Mapping"
- **Description**: "Mapper translates SQLAlchemy model to domain entity then to DTO"
- **Icon**: "🔄"

#### Step 8:

- **Number**: 8
- **Title**: "Cache Update"
- **Description**: "Redis cache updated with result for subsequent requests"
- **Icon**: "💾"

#### Step 9:

- **Number**: 9
- **Title**: "Response Serialization"
- **Description**: "Pydantic DTO serialized to JSON response"
- **Icon**: "📤"

---

### Event Flow (`FlowStep[]`)

#### Step 1:

- **Number**: 1
- **Title**: "Showtime Status Change"
- **Description**: "Cron job triggers showtime status transition check"
- **Icon**: "⏰"

#### Step 2:

- **Number**: 2
- **Title**: "Status Update Use Case"
- **Description**: "Use case queries showtimes and updates status based on time"
- **Icon**: "🔄"

#### Step 3:

- **Number**: 3
- **Title**: "Cache Invalidation"
- **Description**: "Related cache keys invalidated in Redis"
- **Icon**: "🗑️"

#### Step 4:

- **Number**: 4
- **Title**: "Database Persistence"
- **Description**: "Updated entities persisted to PostgreSQL"
- **Icon**: "💾"

---

## 9. Tech Decisions (`TechDecisionsModel`)

### Decision 1: FastAPI Framework

- **Title**: "Why FastAPI over Flask/Django"
- **Problem**: "Need high-performance async REST API with automatic OpenAPI documentation"
- **Solution**: "FastAPI chosen for native async support, Pydantic integration, and OpenAPI generation"
- **Alternatives**:
  - Flask + async extensions (less mature async ecosystem)
  - Django REST Framework (synchronous, heavier framework)
  - Express.js (different language, less type safety)
- **Outcome**: "Achieved 100% async architecture with sub-50ms response times and auto-generated API docs"
- **Icon**: "⚡"

---

### Decision 2: Domain-Driven Design

- **Title**: "Why DDD Architecture"
- **Problem**: "Need maintainable codebase with clear separation of business logic from infrastructure"
- **Solution**: "Implemented DDD with domain, application, and infrastructure layers"
- **Alternatives**:
  - MVC pattern (less domain focus)
  - Transaction script (poor scalability)
  - Monolithic layering (tight coupling)
- **Outcome**: "Achieved 90%+ test coverage, domain logic fully independent from frameworks"
- **Icon**: "🏛️"

---

### Decision 3: PostgreSQL Database

- **Title**: "Why PostgreSQL over MySQL/MongoDB"
- **Problem**: "Need ACID compliance, complex queries, and JSON support for cinema operations"
- **Solution**: "PostgreSQL 16 chosen for JSONB, advanced indexing, and mature async driver"
- **Alternatives**:
  - MySQL (less feature-rich)
  - MongoDB (eventual consistency issues)
  - SQLite (not production-ready)
- **Outcome**: "Complex queries under 100ms, full ACID guarantees, JSONB for flexible fields"
- **Icon**: "🗄️"

---

### Decision 4: Redis Caching

- **Title**: "Why Redis for Caching"
- **Problem**: "Need sub-50ms response times for frequently accessed data"
- **Solution**: "Redis 7 with fastapi-cache for distributed caching layer"
- **Alternatives**:
  - In-memory cache (not distributed)
  - Memcached (less feature-rich)
  - No cache (slow performance)
- **Outcome**: "85%+ cache hit rate, <50ms cached responses, 80% load reduction on database"
- **Icon**: "💾"

---

### Decision 5: Alembic Migrations

- **Title**: "Why Alembic over Raw SQL"
- **Problem**: "Need version-controlled schema evolution with rollback capability"
- **Solution**: "Alembic migration framework integrated with SQLAlchemy"
- **Alternatives**:
  - Raw SQL scripts (no version control)
  - Django migrations (framework lock-in)
  - Flyway (Java ecosystem)
- **Outcome**: "Reliable schema migrations, automatic on deployment, full rollback support"
- **Icon**: "🔄"
