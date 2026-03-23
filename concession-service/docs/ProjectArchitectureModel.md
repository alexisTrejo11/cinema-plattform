# Architecture Model

## 1. Layers (`ArchitectureLayer[]`)

### Layer 1: Domain Layer

- **Name**: "Domain"
- **Description**: Core business logic and entities representing the concession domain model.
- **Components**:
  - Product Entity
  - Combo Entity
  - Promotion Entity
  - Product Category Entity
  - Value Objects (ProductId, ComboId, PromotionId)
  - Domain Exceptions
- **Color**: "#4CAF50"
- **Expanded** (optional): `true`
- **Responsibilities** (optional):
  - Define business rules and validations
  - Entity state management
  - Value object creation and validation
- **Technologies** (optional):
  - Pydantic (for validation)
  - Python dataclasses

---

### Layer 2: Application Layer

- **Name**: "Application"
- **Description**: Use cases and commands/queries following CQRS pattern for orchestrating domain operations.
- **Components**:
  - Product Use Cases
  - Combo Use Cases
  - Promotion Use Cases
  - Category Use Cases
  - Commands (Create, Update, Delete)
  - Queries (GetById, Search, List)
- **Color**: "#2196F3"
- **Expanded** (optional): `true`
- **Responsibilities** (optional):
  - Business logic orchestration
  - Transaction coordination
  - Query/Command separation (CQRS)
- **Technologies** (optional):
  - Python asyncio

---

### Layer 3: Infrastructure Layer

- **Name**: "Infrastructure"
- **Description**: External implementations including database repositories, API controllers, caching, and gRPC services.
- **Components**:
  - SQLAlchemy Repositories
  - FastAPI Controllers
  - Redis Cache Service
  - gRPC Servicers
  - Middleware (JWT, Logging, Rate Limit)
- **Color**: "#FF9800"
- **Expanded** (optional): `true`
- **Responsibilities** (optional):
  - Database persistence
  - HTTP/gRPC request handling
  - External service integration
- **Technologies** (optional):
  - SQLAlchemy ORM
  - FastAPI
  - Redis
  - grpcio

---

## 2. Design Patterns (`DesignPattern[]`)

For each pattern:

- **Title**: "Hexagonal Architecture (Ports & Adapters)"
- **Emoji**: "🔷"
- **Description**: "Separation of core business logic from external dependencies using ports (interfaces) and adapters (implementations). Enables testability and flexibility in technology choices."
- **Category**: "Architecture"
- **Badge**: "Core Pattern"
- **GitHub Example URL** (optional): "https://github.com/anomalyco/cinema-plattform/blob/main/concession-service/app/products/domain/entities/product.py"

---

- **Title**: "CQRS (Command Query Responsibility Segregation)"
- **Emoji**: "⚡"
- **Description**: "Separate models for read and write operations. Commands handle state changes, queries handle data retrieval with optimized data shapes."
- **Category**: "Architecture"
- **Badge**: "Pattern"
- **GitHub Example URL** (optional): "https://github.com/anomalyco/cinema-plattform/blob/main/concession-service/app/products/application/commands.py"

---

- **Title**: "Repository Pattern"
- **Emoji**: "📦"
- **Description**: "Abstraction layer over data persistence. Domain layer depends on repository interfaces; infrastructure provides implementations."
- **Category**: "Data Access"
- **Badge**: "Pattern"
- **GitHub Example URL** (optional): "https://github.com/anomalyco/cinema-plattform/blob/main/concession-service/app/products/domain/repositories.py"

---

- **Title**: "Dependency Injection"
- **Emoji**: "💉"
- **Description**: "Dependencies are injected into classes rather than created internally. FastAPI's dependency injection system manages lifecycle."
- **Category**: "Patterns"
- **Badge**: "Pattern"

---

- **Title**: "Value Objects"
- **Emoji**: "🎯"
- **Description**: "Immutable objects defined by their attributes rather than identity. Used for IDs, enums, and domain-specific values."
- **Category**: "Domain"
- **Badge**: "DDD Pattern"

---

## 3. Scalability Strategies (`StrategyItem[]`)

- **Title**: "Horizontal Scaling"
- **Description**: "Multiple application instances (3 by default) behind nginx load balancer. Stateless design allows easy horizontal scaling by adding more containers."

---

- **Title**: "Database Connection Pooling"
- **Description**: "SQLAlchemy async engine with connection pooling for efficient database resource utilization under high load."

---

- **Title**: "Redis Caching"
- **Description**: "Frequently accessed data cached in Redis to reduce database queries and improve response times."

---

## 4. Security Strategies (`StrategyItem[]`)

- **Title**: "JWT Authentication"
- **Description**: "All write operations require valid JWT tokens with configurable secret, algorithm, audience, and issuer validation."

---

- **Title**: "Role-Based Access Control"
- **Description**: "Role-based authorization ensuring only admin and manager users can perform write operations (create, update, delete)."

---

- **Title**: "Rate Limiting"
- **Description**: "Per-client rate limiting (SlowAPI) prevents abuse: 60 req/min for reads, 10 req/min for writes."

---

- **Title**: "CORS Configuration"
- **Description**: "Configured allowed origins for cross-origin requests with appropriate HTTP headers."

---

## 5. Cache Strategies (`CacheStrategy[]`)

- **Name**: "Redis Cache"
- **Description**: "Application-level caching using Redis for frequently accessed product and category data."
- **TTL**: "Configurable (default: 60 seconds)"
- **Coverage**: "Read operations for products, categories, and combos"

---

## 6. Architecture Features (`ArchitectureFeature[]`)

- **Title**: "Async/Await Throughout"
- **Emoji**: "⚡"
- **Description**: "Full async implementation using Python asyncio for high-concurrency I/O operations."

---

- **Title**: "Soft Delete Support"
- **Description**: "Products, categories, and combos support soft deletion (deleted_at timestamp) for data retention and recovery."

---

- **Title**: "Audit Logging"
- **Description**: "Logging middleware captures all requests with timing information for monitoring and debugging."

---

- **Title**: "Graceful Degradation"
- **Description**: "Service continues to operate without caching if Redis is unavailable, ensuring core functionality."

---

## 7. Architecture Diagram (`ArchitectureDiagramModel`)

### Legend (`LegendItem[]`)

- **Type**: "client"
- **Label**: "Web Client / Mobile App"
- **Color**: "#607D8B"
- **Icon**: "monitor"

---

- **Type**: "gateway"
- **Label**: "Nginx Load Balancer"
- **Color**: "#795548"
- **Icon**: "server"

---

- **Type**: "service"
- **Label**: "Application Instance"
- **Color**: "#2196F3"
- **Icon**: "cpu"

---

- **Type**: "database"
- **Label**: "PostgreSQL"
- **Color**: "#336791"
- **Icon**: "database"

---

- **Type**: "queue"
- **Label**: "Redis Cache"
- **Color**: "#DC382D"
- **Icon**: "hard-drive"

---

### Nodes (`DiagramNode[]`)

For each node:

- **ID**: "client-1"
- **Label**: "Web Client"
- **Type**: `client`
- **x**: 100
- **y**: 100
- **Connections**: ["nginx"]
- **Status** (optional): `healthy`

---

- **ID**: "nginx"
- **Label**: "Nginx LB"
- **Type**: `gateway`
- **x**: 300
- **y**: 100
- **Connections**: ["app-1", "app-2", "app-3"]
- **Status** (optional): `healthy`

---

- **ID**: "app-1"
- **Label**: "App Instance 1"
- **Type**: `service`
- **x**: 500
- **y**: 50
- **Connections**: ["postgres", "redis"]
- **Status** (optional): `healthy`

---

- **ID**: "app-2"
- **Label**: "App Instance 2"
- **Type**: `service`
- **x**: 500
- **y**: 150
- **Connections**: ["postgres", "redis"]
- **Status** (optional): `healthy`

---

- **ID**: "app-3"
- **Label**: "App Instance 3"
- **Type**: `service`
- **x**: 500
- **y**: 250
- **Connections**: ["postgres", "redis"]
- **Status** (optional): `healthy`

---

- **ID**: "app-grpc"
- **Label**: "gRPC Server"
- **Type**: `service`
- **x**: 700
- **y**: 150
- **Connections**: ["postgres"]
- **Status** (optional): `healthy`

---

- **ID**: "postgres"
- **Label**: "PostgreSQL 16"
- **Type**: `database`
- **x**: 700
- **y**: 50
- **Connections**: []
- **Status** (optional): `healthy`

---

- **ID**: "redis"
- **Label**: "Redis 7"
- **Type**: `queue`
- **x**: 700
- **y**: 300
- **Connections**: []
- **Status** (optional): `healthy`

---

### Connections (`DiagramConnection[]`)

- **ID**: "conn-1"
- **From**: "client-1"
- **To**: "nginx"
- **Label** (optional): "HTTP/REST"
- **Protocol** (optional): "HTTP/1.1"
- **Is Active** (optional): `true`

---

- **ID**: "conn-2"
- **From**: "nginx"
- **To**: "app-1"
- **Label** (optional): "Load Balanced"
- **Protocol** (optional): "HTTP/1.1"
- **Is Active** (optional): `true`

---

- **ID**: "conn-3"
- **From**: "app-1"
- **To**: "postgres"
- **Label** (optional): "SQL"
- **Protocol** (optional): "asyncpg"
- **Is Active** (optional): `true`

---

- **ID**: "conn-4"
- **From**: "app-1"
- **To**: "redis"
- **Label** (optional): "Cache"
- **Protocol** (optional): "Redis"
- **Is Active** (optional): `true`

---

## 8. Data Flow (`DataFlowModel`)

### Request Flow (`FlowStep[]`)

For each step:

- **Number**: 1
- **Title**: "Client Request"
- **Description**: "Client sends HTTP request to nginx load balancer"
- **Icon**: "send"

---

- **Number**: 2
- **Title**: "Load Balancing"
- **Description**: "Nginx distributes request to one of the application instances"
- **Icon**: "shuffle"

---

- **Number**: 3
- **Title**: "Middleware Processing"
- **Description**: "Logging, JWT authentication, and rate limiting middleware process the request"
- **Icon**: "filter"

---

- **Number**: 4
- **Title**: "Route to Controller"
- **Description**: "FastAPI routes request to appropriate controller based on path and method"
- **Icon**: "route"

---

- **Number**: 5
- **Title**: "Use Case Execution"
- **Description**: "Controller invokes use case which orchestrates business logic"
- **Icon**: "play"

---

- **Number**: 6
- **Title**: "Repository Access"
- **Description**: "Use case interacts with repository for data persistence"
- **Icon**: "database"

---

- **Number**: 7
- **Title**: "Cache Check"
- **Description**: "Repository checks Redis cache before querying database"
- **Icon**: "hard-drive"

---

- **Number**: 8
- **Title**: "Response Serialization"
- **Description**: "Domain entity converted to DTO/response model"
- **Icon**: "package"

---

- **Number**: 9
- **Title**: "HTTP Response"
- **Description**: "FastAPI returns JSON response to client"
- **Icon**: "check"

---

### Event Flow (`FlowStep[]`)

For each step:

- **Number**: 1
- **Title**: "Service Startup"
- **Description**: "Application starts, migrations run, Redis initializes"
- **Icon**: "power"

---

- **Number**: 2
- **Title**: "Health Check"
- **Description**: "Docker healthcheck verifies service is responding"
- **Icon**: "heart"

---

## 9. Tech Decisions (`TechDecisionsModel`)

For each decision (`TechDecisionModel`):

- **Title**: "FastAPI over Flask/Django"
- **Problem**: "Need high-performance async API framework with built-in OpenAPI documentation"
- **Solution**: "FastAPI provides native async support, automatic OpenAPI/Swagger generation, and type safety with Pydantic"
- **Alternatives**:
  - "Flask: Synchronous only, manual OpenAPI docs"
  - "Django: Heavy framework, not async-native"
- **Outcome**: "Improved development velocity and runtime performance"
- **Icon**: "zap"

---

- **Title**: "SQLAlchemy Async over Traditional ORM"
- **Problem**: "Need non-blocking database operations for high concurrency"
- **Solution**: "SQLAlchemy with asyncpg driver provides fully async database access"
- **Alternatives**:
  - "Synchronous SQLAlchemy: Blocks threads"
  - "Raw asyncpg: No ORM benefits"
- **Outcome**: "High concurrency with connection pooling"
- **Icon**: "database"

---

- **Title**: "Redis for Caching"
- **Problem**: "Frequent database queries for read-heavy endpoints"
- **Solution**: "Redis caching layer with graceful degradation"
- **Alternatives**:
  - "No caching: High DB load"
  - "Memcached: Less feature-rich"
- **Outcome**: "Reduced latency and database load"
- **Icon**: "hard-drive"

---

- **Title**: "gRPC for Internal Communication"
- **Problem**: "Need efficient service-to-service communication"
- **Solution**: "gRPC with Protocol Buffers for strongly-typed, high-performance RPC"
- **Alternatives**:
  - "REST over HTTP: More verbose, less efficient"
  - "Message queues: Overkill for synchronous calls"
- **Outcome**: "Faster inter-service calls with type safety"
- **Icon**: "zap"

---

- **Title**: "JWT for Authentication"
- **Problem**: "Need stateless authentication for horizontally scaled services"
- **Solution**: "JWT tokens with configurable validation parameters"
- **Alternatives**:
  - "Session-based: Requires shared session storage"
  - "API Keys: Less flexible for user context"
- **Outcome**: "Stateless auth enables horizontal scaling"
- **Icon**: "shield"
