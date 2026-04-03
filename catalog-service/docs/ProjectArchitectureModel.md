# Architecture Model

## 1. Layers (`ArchitectureLayer[]`)

### Layer 1: Presentation Layer

- **Name**: Presentation Layer
- **Description**: HTTP API endpoints via FastAPI with role-based access control
- **Components**:
  - FastAPI routers (movie_controllers, cinema_controllers, theater_controllers, theather_seat_controllers)
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
- **Description**: Use cases implementing business workflows for each domain
- **Components**:
  - Movie use cases (GetMovieById, GetMoviesInExhibition, SearchMovies, CreateMovie, UpdateMovie, DeleteMovie)
  - Cinema use cases (GetCinemaById, ListActiveCinemas, SearchCinemas, CreateCinema, UpdateCinema, DeleteCinema, RestoreCinema)
  - Theater use cases (GetTheaterById, SearchTheaters, CreateTheater, UpdateTheater, DeleteTheater, RestoreTheater, GetTheatersByCinema)
  - Seat use cases (GetSeatById, GetSeatsByTheater, CreateSeat, UpdateSeat, DeleteSeat)
  - DTOs for request/response
- **Color**: "#7ED321"
- **Expanded** (optional): `true`
- **Responsibilities** (optional):
  - Orchestrate domain operations
  - Transaction management
  - Business workflow implementation
- **Technologies** (optional):
  - Use case pattern

---

### Layer 3: Domain Layer

- **Name**: Domain Layer
- **Description**: Core business entities, enums, value objects, and repository interfaces
- **Components**:
  - Movie entity with validation
  - Cinema entity with amenities and location
  - Theater entity with capacity rules
  - TheaterSeat entity
  - Domain enums (MovieGenre, MovieRating, CinemaType, CinemaStatus, TheaterType, SeatType)
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
- **Description**: External integrations - database persistence, caching, gRPC server
- **Components**:
  - SQLAlchemy repositories (movie, cinema, theater, seat)
  - Model mappers
  - PostgreSQL models
  - Redis caching
  - gRPC server implementation
- **Color**: "#D0021B"
- **Expanded** (optional): `false`
- **Responsibilities** (optional):
  - Database persistence
  - Caching layer
  - gRPC service provision
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
- **Description**: Four-layer architecture with strict dependency rules - inner layers define interfaces, outer layers implement them
- **Category**: "Architecture"
- **Badge**: "Primary"
- **GitHub Example URL** (optional): ""

---

### Pattern 2: Use Case Pattern

- **Title**: Use Case Pattern
- **Emoji**: "🎯"
- **Description**: Each use case is a single class implementing business operations with clear input/output
- **Category**: "Application"
- **Badge**: "Primary"
- **GitHub Example URL** (optional): ""

---

### Pattern 3: Repository Pattern

- **Title**: Repository Pattern
- **Emoji**: "📦"
- **Description**: Abstract data access through repository interfaces, allowing swap between implementations
- **Category**: "Persistence"
- **Badge**: "Primary"
- **GitHub Example URL** (optional): ""

---

### Pattern 4: Soft Delete

- **Title**: Soft Delete Pattern
- **Emoji**: "🗑️"
- **Description**: Entities use deleted_at timestamp to preserve audit trail and enable restore
- **Category**: "Persistence"
- **Badge**: "Secondary"
- **GitHub Example URL** (optional): ""

---

### Pattern 5: gRPC Server

- **Title**: gRPC Server
- **Emoji**: "🔗"
- **Description**: Built-in gRPC server for high-performance inter-service communication
- **Category**: "Integration"
- **Badge**: "Secondary"
- **GitHub Example URL** (optional): ""

---

## 3. Scalability Strategies (`StrategyItem[]`)

- **Title**: Horizontal Scaling
- **Description**: Deploy multiple instances of catalog-service behind load balancer for horizontal scaling

---

- **Title**: Redis Caching
- **Description**: Cache frequently accessed data (cinemas, theaters) in Redis for sub-50ms response times

---

- **Title**: Database Connection Pooling
- **Description**: Use SQLAlchemy async with connection pooling to handle concurrent requests efficiently

---

## 4. Security Strategies (`StrategyItem[]`)

- **Title**: JWT Authentication
- **Description**: All admin API endpoints require valid JWT token with user_id (sub) and roles claims

---

- **Title**: Role-Based Access Control
- **Description**: Admin endpoints require admin/manager role, public endpoints accessible without auth

---

- **Title**: Input Validation
- **Description**: All request bodies validated via Pydantic models with strict type checking

---

## 5. Cache Strategies (`CacheStrategy[]`)

- **Name**: Redis Cache
- **Description**: Optional Redis caching via fastapi-cache for frequently accessed data
- **TTL**: "5 minutes"
- **Coverage**: "Movies list, Cinemas, Theaters"

---

## 6. Architecture Features (`ArchitectureFeature[]`)

- **Title**: Multi-Domain Architecture
- **Emoji**: "🎬"
- **Description**: Separate domains for Movies, Cinemas, Theaters with independent use cases and repositories

---

- **Title**: gRPC Server
- **Emoji**: "🔗"
- **Description**: Built-in gRPC server for high-performance catalog queries from ticket service

---

- **Title**: Business Rule Validation
- **Emoji**: "📋"
- **Description**: Domain entities implement business rules (theater capacity by type validation)

---

## 7. Architecture Diagram (`ArchitectureDiagramModel`)

### Legend (`LegendItem[]`)

- **Type**: "client"
- **Label**: "Client Application"
- **Color**: "#4A90E2"
- **Icon**: "👤"

- **Type**: "service"
- **Label**: "Catalog Service"
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
- **Connections**: ["api-gateway"]
- **Status** (optional): `healthy`

- **ID**: "api-gateway"
- **Label**: "API Gateway"
- **Type**: `gateway`
- **x**: 300
- **y**: 100
- **Connections**: ["catalog-service"]
- **Status** (optional): `healthy`

- **ID**: "catalog-service"
- **Label**: "Catalog Service"
- **Type**: `service`
- **x**: 500
- **y**: 100
- **Connections**: ["postgres", "redis", "ticket-service"]
- **Status** (optional): `healthy`
- **Traffic**: "10000 QPS"

- **ID**: "postgres"
- **Label**: "PostgreSQL"
- **Type**: `database`
- **x**: 500
- **y**: 300
- **Connections**: []
- **Status** (optional): `healthy`

- **ID**: "redis"
- **Label**: "Redis"
- **Type**: `cache`
- **x**: 700
- **y**: 100
- **Connections**: []
- **Status** (optional): `healthy`

- **ID**: "ticket-service"
- **Label**: "Ticket Service (gRPC)"
- **Type**: `service`
- **x**: 700
- **y**: 200
- **Connections**: []

### Connections (`DiagramConnection[]`)

- **ID**: "conn-1"
- **From**: "client-1"
- **To**: "api-gateway"
- **Label** (optional): "HTTPS"
- **Protocol** (optional): "HTTP/REST"
- **Is Active** (optional): `true`

- **ID**: "conn-2"
- **From**: "api-gateway"
- **To**: "catalog-service"
- **Label** (optional): "HTTP/REST"
- **Protocol** (optional): "HTTP"
- **Is Active** (optional): `true`

- **ID**: "conn-3"
- **From**: "catalog-service"
- **To**: "postgres"
- **Label** (optional): "SQL"
- **Protocol** (optional): "PostgreSQL"
- **Is Active** (optional): `true`

- **ID**: "conn-4"
- **From**: "catalog-service"
- **To**: "redis"
- **Label** (optional): "Cache"
- **Protocol** (optional): "Redis"
- **Is Active** (optional): `true`

- **ID**: "conn-5"
- **From**: "catalog-service"
- **To**: "ticket-service"
- **Label** (optional): "gRPC"
- **Protocol** (optional): "gRPC"
- **Is Active** (optional): `true`

---

## 8. Data Flow (`DataFlowModel`)

### Request Flow (`FlowStep[]`)

- **Number**: 1
- **Title**: "Client Request"
- **Description**: Client sends authenticated HTTP request to catalog endpoint
- **Icon**: "👤"

- **Number**: 2
- **Title**: "API Validation"
- **Description**: FastAPI validates JWT, checks roles, validates request body via Pydantic
- **Icon**: "🔒"

- **Number**: 3
- **Title**: "Use Case Execution"
- **Description**: Controller calls use case which orchestrates domain operations
- **Icon**: "⚙️"

- **Number**: 4
- **Title**: "Persistence"
- **Description**: Domain entities saved/retrieved from PostgreSQL via SQLAlchemy repository
- **Icon**: "🗄️"

- **Number**: 5
- **Title**: "Caching"
- **Description**: Optionally cache results in Redis for frequently accessed data
- **Icon**: "⚡"

- **Number**: 6
- **Title**: "Response"
- **Description**: HTTP response returned with catalog data
- **Icon**: "✅"

### Event Flow (`FlowStep[]`)

- **Number**: 1
- **Title**: "Movie Created Event"
- **Description**: Domain event emitted when new movie is created
- **Icon**: "🎬"

- **Number**: 2
- **Title**: "Kafka Publishing"
- **Description**: Event published to catalog.events Kafka topic
- **Icon**: "📤"

- **Number**: 3
- **Title**: "Consumer Processing"
- **Description**: Ticket service consumes and processes the event
- **Icon**: "📥"

---

## 9. Tech Decisions (`TechDecisionsModel`)

For each decision (`TechDecisionModel`):

- **Title**: "FastAPI over Flask/Django"
- **Problem**: "Need async-capable, high-performance REST API framework"
- **Solution**: "FastAPI with native async support, automatic OpenAPI docs, Pydantic validation"
- **Alternatives**:
  - Flask (synchronous, requires async extensions)
  - Django (heavy, not async-native)
- **Outcome**: "High performance, type safety, automatic documentation"
- **Icon**: "🐍"

---

- **Title**: "gRPC Server"
- **Problem**: "Need high-performance inter-service communication for catalog queries"
- **Solution**: "Built-in gRPC server for real-time ticket service queries"
- **Alternatives**:
  - REST API (higher latency)
  - GraphQL (overhead)
- **Outcome**: "< 30ms response time for catalog queries"
- **Icon**: "🔗"

---

- **Title**: "Async SQLAlchemy"
- **Problem**: "Need non-blocking database access for high concurrency"
- **Solution**: "asyncpg driver with SQLAlchemy async session"
- **Alternatives**:
  - Synchronous SQLAlchemy (blocks threads)
  - Raw asyncpg (loses ORM benefits)
- **Outcome**: "High concurrency without thread blocking"
- **Icon**: "🗄️"

---

- **Title**: "Clean Architecture"
- **Problem**: "Need maintainable, testable code with clear separation of concerns"
- **Solution**: "Four-layer architecture with dependency injection and domain-driven design"
- **Alternatives**:
  - Layered architecture (less strict)
  - Microservices without clear boundaries
- **Outcome**: "Testable, maintainable, clear dependencies"
- **Icon**: "🏗️"
