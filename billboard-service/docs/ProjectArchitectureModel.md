# Architecture Model

## 1. Layers (`ArchitectureLayer[]`)

### Layer 1: Presentation Layer

- **Name**: Presentation Layer
- **Description**: HTTP API endpoints via FastAPI with role-based access control
- **Components**:
  - FastAPI routers (showtime_controller)
  - Dependency injection via FastAPI Depends
  - JWT authentication middleware
  - Rate limiting middleware
- **Color**: "#4A90E2"
- **Expanded** (optional): `true`
- **Responsibilities** (optional):
  - Handle HTTP requests/responses
  - Input validation via Pydantic
  - Authentication/Authorization
  - Route registration
- **Technologies** (optional):
  - FastAPI
  - Pydantic
  - SlowAPI

---

### Layer 2: Application Layer

- **Name**: Application Layer
- **Description**: Use cases implementing business workflows for showtimes and seats
- **Components**:
  - Showtime use cases (GetShowtimeById, SearchShowtimes, DraftShowtime, LaunchShowtime, CancelShowtime, RestoreShowtime, UpdateShowtime, DeleteShowtime)
  - Seat use cases (GetSeatsByShowtime, TakeSeat, LeaveSeat)
  - DTOs for request/response
- **Color**: "#7ED321"
- **Expanded** (optional): `true`
- **Responsibilities** (optional):
  - Orchestrate domain operations
  - Business workflow implementation
  - Catalog service integration via ports
- **Technologies** (optional):
  - Use case pattern
  - Port/Adapter pattern for external services

---

### Layer 3: Domain Layer

- **Name**: Domain Layer
- **Description**: Core business entities, enums, value objects, and repository interfaces
- **Components**:
  - Showtime entity with business rules (price validation, duration, schedule)
  - ShowtimeSeat entity with take/leave operations
  - Domain enums (ShowtimeStatus)
  - Domain exceptions
  - Repository interfaces
- **Color**: "#F5A623"
- **Expanded** (optional): `true`
- **Responsibilities** (optional):
  - Encapsulate business rules
  - Ensure domain invariants
  - Define repository contracts
- **Technologies** (optional):
  - Pure Python (no framework dependencies)
  - Pydantic BaseModel

---

### Layer 4: Infrastructure Layer

- **Name**: Infrastructure Layer
- **Description**: External integrations - database persistence, caching, gRPC clients
- **Components**:
  - SQLAlchemy repositories
  - Model mappers
  - PostgreSQL models
  - Redis caching
  - gRPC client for catalog service
  - Kafka publisher
- **Color**: "#D0021B"
- **Expanded** (optional): `false`
- **Responsibilities** (optional):
  - Database persistence
  - Caching layer
  - External service calls
  - Protocol translation
- **Technologies** (optional):
  - SQLAlchemy (async)
  - Redis
  - gRPC + protobuf
  - PostgreSQL

---

## 2. Design Patterns (`DesignPattern[]`)

### Pattern 1: Clean Architecture

- **Title**: Clean Architecture
- **Emoji**: "🏗️"
- **Description**: Four-layer architecture with strict dependency rules
- **Category**: "Architecture"
- **Badge**: "Primary"

---

### Pattern 2: Use Case Pattern

- **Title**: Use Case Pattern
- **Emoji**: "🎯"
- **Description**: Each use case is a single class implementing business operations
- **Category**: "Application"
- **Badge**: "Primary"

---

### Pattern 3: Port & Adapter

- **Title**: Port & Adapter (Hexagonal)
- **Emoji**: "🔌"
- **Description**: Catalog gateway as port with gRPC adapter
- **Category**: "Integration"
- **Badge**: "Secondary"

---

### Pattern 4: Repository Pattern

- **Title**: Repository Pattern
- **Emoji**: "📦"
- **Description**: Abstract data access through repository interfaces
- **Category**: "Persistence"
- **Badge**: "Primary"

---

### Pattern 5: Soft Delete

- **Title**: Soft Delete Pattern
- **Emoji**: "🗑️"
- **Description**: Showtimes use deleted_at timestamp for audit trail
- **Category**: "Persistence"
- **Badge**: "Secondary"

---

## 3. Scalability Strategies (`StrategyItem[]`)

- **Title**: Horizontal Scaling
- **Description**: Deploy multiple instances behind load balancer

- **Title**: Redis Caching
- **Description**: Cache frequently accessed showtimes for sub-50ms response

- **Title**: Database Connection Pooling
- **Description**: Async SQLAlchemy with connection pooling

---

## 4. Security Strategies (`StrategyItem[]`)

- **Title**: JWT Authentication
- **Description**: All admin API endpoints require valid JWT token

- **Title**: Role-Based Access Control
- **Description**: Admin endpoints require admin/manager role

- **Title**: Input Validation
- **Description**: All request bodies validated via Pydantic models

---

## 5. Cache Strategies (`CacheStrategy[]`)

- **Name**: Redis Cache
- **Description**: Cache showtimes and seat availability
- **TTL**: "5 minutes"
- **Coverage**: "Active showtimes, seat status"

---

## 6. Architecture Features (`ArchitectureFeature[]`)

- **Title**: Showtime Lifecycle
- **Emoji**: "📅"
- **Description**: Draft → Upcoming → Completed/Cancelled states with business rules

- **Title**: Seat Reservation
- **Emoji**: "💺"
- **Description**: Real-time seat take/leave with transaction tracking

- **Title**: Buffer Time Management
- **Emoji**: "⏱️"
- **Description**: Pre-show and post-show buffer times (cleaning, commercials)

---

## 7. Architecture Diagram (`ArchitectureDiagramModel`)

### Legend (`LegendItem[]`)

- **Type**: "client"
- **Label**: "Client Application"
- **Color**: "#4A90E2"
- **Icon**: "👤"

- **Type**: "service"
- **Label**: "Billboard Service"
- **Color**: "#7ED321"
- **Icon**: "⚙️"

- **Type**: "database"
- **Label**: "PostgreSQL"
- **Color**: "#F5A623"
- **Icon**: "🗄️"

- **Type**: "cache"
- **Label**: "Redis"
- **Color**: "#D0021B"
- **Icon**: "⚡"

### Nodes (`DiagramNode[]`)

- **ID**: "client-1"
- **Label**: "Web/Mobile Client"
- **Type**: `client`
- **x**: 100
- **y**: 100
- **Status**: `healthy`

- **ID**: "billboard-service"
- **Label**: "Billboard Service"
- **Type**: `service`
- **x**: 400
- **y**: 100
- **Connections**: ["postgres", "redis", "catalog-service", "payment-service"]
- **Status**: `healthy`

- **ID**: "postgres"
- **Label**: "PostgreSQL"
- **Type**: `database`
- **x**: 400
- **y**: 300

- **ID**: "redis"
- **Label**: "Redis"
- **Type**: `cache`
- **x**: 600
- **y**: 100

- **ID**: "catalog-service"
- **Label**: "Catalog Service (gRPC)"
- **Type**: `service`
- **x**: 600
- **y**: 200

- **ID**: "payment-service"
- **Label**: "Payment Service (gRPC)"
- **Type**: `service`
- **x**: 600
- **y**: 300

### Connections (`DiagramConnection[]`)

- **ID**: "conn-1"
- **From**: "client-1"
- **To**: "billboard-service"
- **Protocol**: "HTTP/REST"
- **Is Active**: `true`

- **ID**: "conn-2"
- **From**: "billboard-service"
- **To**: "postgres"
- **Protocol**: "PostgreSQL"
- **Is Active**: `true`

- **ID**: "conn-3"
- **From**: "billboard-service"
- **To**: "redis"
- **Protocol**: "Redis"
- **Is Active**: `true`

- **ID**: "conn-4"
- **From**: "billboard-service"
- **To**: "catalog-service"
- **Protocol**: "gRPC"
- **Is Active**: `true`

- **ID**: "conn-5"
- **From**: "billboard-service"
- **To**: "payment-service"
- **Protocol**: "gRPC"
- **Is Active**: `true`

---

## 8. Data Flow (`DataFlowModel`)

### Request Flow (`FlowStep[]`)

- **Number**: 1
- **Title**: "Client Request"
- **Description**: Client sends HTTP request to create/showtime
- **Icon**: "👤"

- **Number**: 2
- **Title**: "Validation"
- **Description**: FastAPI validates JWT and request body
- **Icon**: "🔒"

- **Number**: 3
- **Title**: "Business Rules"
- **Description**: Domain entity validates price, duration, schedule
- **Icon**: "📋"

- **Number**: 4
- **Title**: "Catalog Integration"
- **Description**: gRPC call to validate movie and theater
- **Icon**: "🔗"

- **Number**: 5
- **Title**: "Persistence"
- **Description**: Save showtime to PostgreSQL
- **Icon**: "🗄️"

- **Number**: 6
- **Title**: "Response"
- **Description**: Return showtime response
- **Icon**: "✅"

### Event Flow (`FlowStep[]`)

- **Number**: 1
- **Title**: "Showtime Created"
- **Description**: ShowtimeCreated event emitted
- **Icon**: "📅"

- **Number**: 2
- **Title**: "Kafka Publishing"
- **Description**: Event published to billboard.events
- **Icon**: "📤"

---

## 9. Tech Decisions (`TechDecisionsModel`)

- **Title**: "FastAPI over Flask/Django"
- **Problem**: "Need async-capable, high-performance REST API"
- **Solution**: "FastAPI with native async support and automatic OpenAPI docs"
- **Outcome**: "High performance, type safety, automatic documentation"
- **Icon**: "🐍"

- **Title**: "gRPC for Catalog Integration"
- **Problem**: "Need high-performance service-to-service calls"
- **Solution**: "gRPC with protobuf for catalog service communication"
- **Outcome**: "< 30ms response time for catalog queries"
- **Icon**: "🔗"

- **Title**: "Business Rules in Domain"
- **Problem**: "Need centralized validation logic"
- **Solution**: "Domain entity methods for price, duration, schedule validation"
- **Outcome**: "Reusable, testable business logic"
- **Icon**: "📋"
