# Architecture Model

## 1. Layers (`ArchitectureLayer[]`)

### Layer 1: Domain Layer

- **Name**: "Domain"
- **Description**: Core business entities, value objects, enums, and repository interfaces.
- **Components**:
  - User Entity (Account, User with profile)
  - Token Value Objects
  - User Roles (ADMIN, CUSTOMER, EMPLOYEE, MANAGER)
  - User Status (PENDING, ACTIVE, INACTIVE, BANNED)
  - Gender Enum
  - Token Types (Access, Refresh, TwoFA)
- **Color**: "#4CAF50"
- **Expanded** (optional): `true`
- **Responsibilities** (optional):
  - Business rules and validations
  - Password strength validation
  - Entity state management
- **Technologies** (optional):
  - Pydantic
  - Python dataclasses

---

### Layer 2: Application Layer

- **Name**: "Application"
- **Description**: Use cases, DTOs, and services for orchestrating domain operations.
- **Components**:
  - AuthUseCases (Signup, Login, Logout, Refresh)
  - TwoFAUseCases (Enable, Disable, Login)
  - UserUseCases (List, Get, Create, Update, Delete)
  - ProfileUseCases (Get, Update)
  - SessionService
  - AuthValidationService
  - TokenProvider
- **Color**: "#2196F3"
- **Expanded** (optional): `true`
- **Responsibilities** (optional):
  - Business logic orchestration
  - DTO validation and transformation
  - Event publishing coordination
- **Technologies** (optional):
  - Python asyncio
  - Result pattern for error handling

---

### Layer 3: Infrastructure Layer

- **Name**: "Infrastructure"
- **Description**: External implementations including controllers, repositories, cache, and event publishers.
- **Components**:
  - Auth Controllers (REST API)
  - User Controllers (REST API)
  - Profile Controllers (REST API)
  - SQLAlchemy User Repository
  - Redis Token Repository
  - Kafka Event Publisher
  - JWT Auth Middleware
  - gRPC Servicer
- **Color**: "#FF9800"
- **Expanded** (optional): `true`
- **Responsibilities** (optional):
  - HTTP request handling
  - Database persistence
  - Cache operations
  - Event publishing
- **Technologies** (optional):
  - FastAPI
  - SQLAlchemy ORM
  - Redis
  - kafka-python

---

### Layer 4: Shared Layer

- **Name**: "Shared"
- **Description**: Cross-cutting concerns shared across all domains.
- **Components**:
  - Token Core (Token entity, TokenRepository interface)
  - Events (DomainEventEnvelope, builders, publishers)
  - Notifications (Notification entity, services)
  - Shared utilities (pagination, response, exceptions, logging)
- **Color**: "#9C27B0"
- **Expanded** (optional): `false`
- **Responsibilities** (optional):
  - Token management abstraction
  - Event envelope standardization
  - Common utilities
- **Technologies** (optional):
  - Redis
  - Kafka

---

## 2. Design Patterns (`DesignPattern[]`)

For each pattern:

- **Title**: "Hexagonal Architecture (Ports & Adapters)"
- **Emoji**: "🔷"
- **Description**: "Separation of core business logic from external dependencies using ports (interfaces) and adapters (implementations)."
- **Category**: "Architecture"
- **Badge**: "Core Pattern"
- **GitHub Example URL** (optional): "https://github.com/anomalyco/cinema-plattform/blob/main/user-service/app/users/domain/entities.py"

---

- **Title**: "Repository Pattern"
- **Emoji**: "📦"
- **Description**: "Abstraction layer over data persistence. Domain depends on repository interfaces; infrastructure provides implementations."
- **Category**: "Data Access"
- **Badge**: "Pattern"

---

- **Title**: "Token Provider Pattern"
- **Emoji**: "🔑"
- **Description**: "Abstract token creation and management with Redis-backed storage and configurable expiration."
- **Category**: "Security"
- **Badge**: "Pattern"

---

- **Title**: "Domain Event Pattern"
- **Emoji**: "📡"
- **Description**: "Standardized event envelope for publishing domain events to message broker."
- **Category**: "Messaging"
- **Badge**: "Pattern"

---

- **Title**: "Result Pattern"
- **Emoji**: "✅"
- **Description**: "Explicit success/failure handling in use cases with error messages."
- **Category**: "Error Handling"
- **Badge**: "Pattern"

---

## 3. Scalability Strategies (`StrategyItem[]`)

- **Title**: "Horizontal Scaling"
- **Description**: "Multiple application instances (3 by default) behind nginx load balancer. Stateless JWT auth enables easy scaling."

---

- **Title**: "Redis Session Store"
- **Description**: "Session tokens stored in Redis for fast lookup and shared state across instances."

---

- **Title**: "Database Connection Pooling"
- **Description**: "SQLAlchemy async engine with connection pooling for efficient database resource utilization."

---

## 4. Security Strategies (`StrategyItem[]`)

- **Title**: "JWT Authentication"
- **Description**: "Stateless JWT tokens with configurable secret, algorithm, audience, and issuer validation."

---

- **Title**: "Password Strength Validation"
- **Description**: "Enforces strong passwords: 8+ chars, uppercase, lowercase, digit, and special character."

---

- **Title**: "Role-Based Access Control"
- **Description**: "Admin-only operations protected by role checks. Users can only access their own resources."

---

- **Title**: "Two-Factor Authentication"
- **Description**: "Optional TOTP-based 2FA for enhanced account security."

---

- **Title**: "Rate Limiting"
- **Description**: "IP-based rate limiting (30 req/min) prevents brute force and abuse."

---

## 5. Cache Strategies (`CacheStrategy[]`)

- **Name**: "Redis Session Cache"
- **Description**: "Session tokens (refresh tokens) stored in Redis with TTL-based expiration."
- **TTL**: "Configurable (default: 7 days for refresh tokens)"
- **Coverage**: "Session management operations"

---

- **Name**: "FastAPI Cache"
- **Description**: "Application-level caching using fastapi-cache with Redis backend."
- **TTL**: "Configurable per endpoint"
- **Coverage**: "Read-heavy operations"

---

## 6. Architecture Features (`ArchitectureFeature[]`)

- **Title**: "Async/Await Throughout"
- **Emoji**: "⚡"
- **Description**: "Full async implementation using Python asyncio for high-concurrency I/O operations."

---

- **Title**: "Event-Driven Design"
- **Emoji**: "📡"
- **Description**: "Domain events published to Kafka for loose coupling with other services."

---

- **Title**: "Startup Validation"
- **Emoji**: "🔍"
- **Description**: "Fail-fast validation of database and Redis connectivity on startup."

---

- **Title**: "Graceful Degradation"
- **Emoji**: "🛡️"
- **Description**: "Service continues without Kafka when disabled; Redis optional on startup."

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
- **Label**: "Redis / Kafka"
- **Color**: "#DC382D"
- **Icon**: "hard-drive"

---

### Nodes (`DiagramNode[]`)

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
- **Connections**: ["postgres", "redis", "kafka"]
- **Status** (optional): `healthy`

---

- **ID**: "app-2"
- **Label**: "App Instance 2"
- **Type**: `service`
- **x**: 500
- **y**: 150
- **Connections**: ["postgres", "redis", "kafka"]
- **Status** (optional): `healthy`

---

- **ID**: "app-3"
- **Label**: "App Instance 3"
- **Type**: `service`
- **x**: 500
- **y**: 250
- **Connections**: ["postgres", "redis", "kafka"]
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

- **ID**: "kafka"
- **Label**: "Kafka Broker"
- **Type**: `queue`
- **x**: 700
- **y**: 400
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
- **Label** (optional): "Sessions"
- **Protocol** (optional): "Redis"
- **Is Active** (optional): `true`

---

- **ID**: "conn-5"
- **From**: "app-1"
- **To**: "kafka"
- **Label** (optional): "Events"
- **Protocol** (optional): "Kafka"
- **Is Active** (optional): `true`

---

## 8. Data Flow (`DataFlowModel`)

### Request Flow (`FlowStep[]`)

For each step:

- **Number**: 1
- **Title**: "Client Request"
- **Description**: "Client sends HTTP request with optional JWT token"
- **Icon**: "send"

---

- **Number**: 2
- **Title**: "JWT Middleware"
- **Description**: "Middleware validates JWT token and extracts user context"
- **Icon**: "lock"

---

- **Number**: 3
- **Title**: "Route to Controller"
- **Description**: "FastAPI routes to appropriate controller based on path"
- **Icon**: "route"

---

- **Number**: 4
- **Title**: "Dependency Injection"
- **Description**: "FastAPI injects use cases and validates role permissions"
- **Icon**: "box"

---

- **Number**: 5
- **Title**: "Business Logic Execution"
- **Description**: "Use case orchestrates domain operations and services"
- **Icon**: "play"

---

- **Number**: 6
- **Title**: "Data Access"
- **Description**: "Repository accesses PostgreSQL; Token repository accesses Redis"
- **Icon**: "database"

---

- **Number**: 7
- **Title**: "Event Publishing"
- **Description**: "Domain events published to Kafka (when enabled)"
- **Icon**: "radio"

---

- **Number**: 8
- **Title**: "Response"
- **Description**: "DTO returned to client with appropriate status code"
- **Icon**: "check"

---

## 9. Tech Decisions (`TechDecisionsModel`)

For each decision (`TechDecisionModel`):

- **Title**: "Redis over Database Sessions"
- **Problem**: "Need fast session lookup with horizontal scaling support"
- **Solution**: "Redis stores refresh tokens; JWT access tokens remain stateless"
- **Alternatives**:
  - "Database sessions: slower, adds load to primary DB"
  - "In-memory: doesn't scale horizontally"
- **Outcome**: "Sub-10ms session lookups with shared state across instances"
- **Icon**: "database"

---

- **Title**: "TOTP for 2FA"
- **Problem**: "Need standard-compliant 2FA that works with authenticator apps"
- **Solution**: "TOTP using pyotp with QR code generation"
- **Alternatives**:
  - "SMS 2FA: carrier-dependent, less secure"
  - "Email codes: less convenient"
- **Outcome**: "Google Authenticator compatible 2FA"
- **Icon**: "shield"

---

- **Title**: "Kafka for Domain Events"
- **Problem**: "Need reliable event delivery to other microservices"
- **Solution**: "Domain events published to Kafka topics with envelope pattern"
- **Alternatives**:
  - "Direct HTTP calls: tight coupling"
  - "No events: poll-based queries"
- **Outcome**: "Decoupled services with guaranteed event delivery"
- **Icon**: "radio"

---

- **Title**: "Fail-Fast Startup Validation"
- **Problem**: "Need to detect configuration errors early"
- **Solution**: "Validate PostgreSQL and Redis connectivity on startup"
- **Alternatives**:
  - "Lazy validation: errors surface later"
  - "No validation: silent failures"
- **Outcome**: "Clear errors at startup, not runtime"
- **Icon**: "alert-triangle"
