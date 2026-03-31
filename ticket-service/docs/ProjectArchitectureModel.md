# Architecture Model

## 1. Layers (`ArchitectureLayer[]`)

### Layer 1: API/Infrastructure Layer

- **Name**: API/Infrastructure Layer
- **Description**: HTTP/REST controllers (FastAPI), gRPC clients, and middleware components handling incoming requests and external service communication.
- **Components**:
  - `ticket_command_controller.py` - Write operations (buy, cancel, use tickets)
  - `ticket_query_controller.py` - Read operations (search, list, get tickets)
  - `grpc/payment_gateway_client.py` - gRPC client for payment service
  - `grpc/billboard_seat_client.py` - gRPC client for billboard seat availability
  - `middleware/jwt_security.py` - JWT authentication middleware
  - `middleware/logging_middleware.py` - Request/response logging
- **Color**: `#4CAF50`
- **Expanded** (optional): `true`
- **Responsibilities** (optional):
  - Handle HTTP requests and responses
  - Rate limiting via SlowAPI
  - JWT token validation
  - gRPC service invocation
  - OpenAPI/Swagger documentation
- **Technologies** (optional):
  - FastAPI
  - SlowAPI
  - PyJWT
  - gRPC (grpcio, grpcio-tools)

---

### Layer 2: Application/Use Case Layer

- **Name**: Application/Use Case Layer
- **Description**: Business logic orchestration through use cases implementing the command and query patterns (CQRS).
- **Components**:
  - `ticket_command_use_cases.py` - DigitalBuyTicketsUseCase, UseTicketUseCase, CancelTicketCase
  - `ticket_query_use_cases.py` - GetTicketByIdUseCase, GetTicketsByUserIdUseCase, GetTicketsByShowtimeIdUseCase, GetTicketsByCriteriaUseCase
  - `ticket_summary_use_cases.py` - GetUserTicketSummaryUseCase, GetPurchaseQuoteUseCase, ListShowtimeSeatsForSaleUseCase
  - `seat_use_cases.py` - ShowtimeSeatUseCase
- **Color**: `#2196F3`
- **Expanded** (optional): `true`
- **Responsibilities** (optional):
  - Orchestrate business workflows
  - Coordinate between domain services and external ports
  - Handle payment authorization flow
  - Validate seat availability
- **Technologies** (optional):
  - Pydantic DTOs
  - Async/await patterns

---

### Layer 3: Domain Layer

- **Name**: Domain Layer
- **Description**: Core business logic, entities, value objects, and domain services with no external dependencies.
- **Components**:
  - `entities/ticket.py` - Ticket aggregate root
  - `entities/seats.py` - ShowtimeSeat entity
  - `valueobjects/enums.py` - TicketStatus, TicketType enums
  - `valueobjects/helping_classes.py` - CustomerDetails, PriceDetails, PaymentDetails
  - `services.py` - TicketService, ShowtimeSeatService
  - `ports.py` - PaymentGatewayPort, ShowtimeSeatAssertionPort interfaces
  - `interfaces.py` - TicketRepository, SeatRepository abstractions
  - `exceptions.py` - Domain-specific exceptions
- **Color**: `#FF9800`
- **Expanded** (optional): `true`
- **Responsibilities** (optional):
  - Ticket lifecycle management (reserve, purchase, cancel, use)
  - Seat availability management
  - Business rule validation
  - Price calculation
- **Technologies** (optional):
  - Pydantic models
  - Python dataclasses

---

### Layer 4: Infrastructure/Persistence Layer

- **Name**: Infrastructure/Persistence Layer
- **Description**: Data access implementations for PostgreSQL (tickets, seats) and MongoDB (showtime replica).
- **Components**:
  - `persistence/models/ticket_model.py` - SQLAlchemy TicketModel
  - `persistence/models/showtime_seat_model.py` - SQLAlchemy ShowtimeSeatModel
  - `persistence/repository/sqlalchemy_ticket_repository.py` - PostgreSQL ticket repository
  - `persistence/repository/sqlalchemy_showtime_seat_repository.py` - PostgreSQL seat repository
  - `mongo_showtime.py` - MongoDB showtime repository
  - `mongo_cinema_repo.py` - MongoDB cinema repository
  - `mongo_theater_repo.py` - MongoDB theater repository
- **Color**: `#9C27B0`
- **Expanded** (optional): `true`
- **Responsibilities** (optional):
  - SQLAlchemy ORM mapping
  - Async database operations
  - MongoDB document management
  - Data mappers between domain and persistence models
- **Technologies** (optional):
  - SQLAlchemy (async)
  - asyncpg
  - Motor (async MongoDB driver)
  - Alembic migrations

---

### Layer 5: External/Integration Layer

- **Name**: External/Integration Layer
- **Description**: Integration with external services (billboard, wallet) and event-driven messaging.
- **Components**:
  - `external/billboard/` - Billboard service read model and Kafka consumer
  - `shared/events/` - Kafka event publishing and deduplication
  - `config/kafka_config.py` - Kafka producer/consumer setup
- **Color**: `#F44336`
- **Expanded** (optional): `true`
- **Responsibilities** (optional):
  - Consume billboard events for data replication
  - Event deduplication for idempotent processing
  - Kafka topic management
- **Technologies** (optional):
  - Kafka-python
  - MongoDB (Motor)

---

## 2. Design Patterns (`DesignPattern[]`)

For each pattern:

- **Title**: Hexagonal Architecture (Ports & Adapters)
- **Emoji**: ":construction:"
- **Description**: The service follows hexagonal architecture with clear separation between domain logic and infrastructure. Ports (interfaces) define inbound and outbound contracts, while adapters implement them (SQLAlchemy repositories, gRPC clients).
- **Category**: Architecture
- **Badge**: "Core Pattern"
- **GitHub Example URL** (optional): ""

---

- **Title**: CQRS (Command Query Responsibility Segregation)
- **Emoji**: ":arrows_counterclockwise:"
- **Description**: Separate command (buy, cancel, use) and query (search, list, get) endpoints with dedicated use cases. Commands modify state, queries are read-only.
- **Category**: Pattern
- **Badge**: "API Design"
- **GitHub Example URL** (optional): ""

---

- **Title**: Repository Pattern
- **Emoji**: ":card_file_box:"
- **Description**: Abstract data access through repository interfaces (TicketRepository, SeatRepository) with multiple implementations (SQLAlchemy, MongoDB).
- **Category**: Data Access
- **Badge**: "Persistence"
- **GitHub Example URL** (optional): ""

---

- **Title**: Event-Driven Architecture
- **Emoji**: ":zap:"
- **Description**: Kafka integration for consuming billboard events and replicating showtime/cinema/theater data to MongoDB for read-heavy paths.
- **Category**: Integration
- **Badge**: "Messaging"
- **GitHub Example URL** (optional): ""

---

- **Title**: Dependency Injection via FastAPI
- **Emoji**: ":syringe:"
- **Description**: Use FastAPI's dependency injection system to wire up repositories, services, and use cases with proper scoping.
- **Category**: Pattern
- **Badge**: "DI"
- **GitHub Example URL** (optional): ""

---

## 3. Scalability Strategies (`StrategyItem[]`)

- **Title**: Horizontal Pod Scaling
- **Description**: Multiple Docker containers (app-1, app-2, app-3) behind nginx load balancer, each running the FastAPI application independently with shared PostgreSQL and MongoDB.

---

- **Title**: Database Connection Pooling
- **Description**: SQLAlchemy async engine configured with pool_size=10, max_overflow=20 for efficient PostgreSQL connection management.

---

- **Title**: Kafka Consumer Groups
- **Description**: Horizontal scaling of Kafka consumers via consumer groups (ticket-service-billboard, ticket-service-wallet) with partition-based work distribution.

---

- **Title**: Redis Caching Ready
- **Description**: FastAPI-cache with Redis integration configured for future caching of frequently accessed data (showtime prices, seat availability).

---

## 4. Security Strategies (`StrategyItem[]`)

- **Title**: JWT Authentication
- **Description**: Optional JWT Bearer token validation via middleware. Supports configurable audience, issuer, and algorithm (HS256).

---

- **Title**: Rate Limiting
- **Description**: SlowAPI integration with per-route limits (10/min for purchases, 30/min for cancel/use, 60-120/min for queries). Default: 60/minute.

---

- **Title**: Input Validation
- **Description**: Pydantic models validate all request DTOs with field constraints, email validation, and range checks.

---

- **Title**: Error Handling & Logging
- **Description**: Structured logging with correlation IDs, exception handlers that hide internal details from clients while logging full stack traces.

---

## 5. Cache Strategies (`CacheStrategy[]`)

- **Name**: Redis Cache (Configured)
- **Description**: FastAPI-cache with Redis backend configured but not actively used. Ready for caching purchase quotes, seat availability.
- **TTL**: "Configurable per endpoint"
- **Coverage**: "Optional - not currently active"

---

## 6. Architecture Features (`ArchitectureFeature[]`)

- **Title**: Multi-Database Strategy
- **Emoji**: ":floppy_disk:"
- **Description**: PostgreSQL for transactional ticket data (writes), MongoDB for replicated showtime/cinema data (reads). Each optimized for its access pattern.

---

- **Title**: gRPC for External Calls
- **Emoji**: ":telephone_receiver:"
- **Description**: Outbound gRPC clients for payment authorization and billboard seat assertions with timeout and error handling.

---

- **Title**: QR Code Generation
- **Description**: Built-in QR code generation for ticket validation at venue entry points.

---

- **Title**: Service Registry Ready
- **Description**: Optional microservice registry integration for service discovery and health heartbeats.

---

## 7. Architecture Diagram (`ArchitectureDiagramModel`)

### Legend (`LegendItem[]`)

- **Type**: "external_service"
- **Label**: "External Services (Billboard, Payment)"
- **Color**: "#F44336"
- **Icon**: "cloud"

- **Type**: "database"
- **Label**: "Databases"
- **Color**: "#9C27B0"
- **Icon**: "database"

- **Type**: "queue"
- **Label**: "Kafka"
- **Color**: "#FF9800"
- **Icon**: "stream"

- **Type**: "service"
- **Label**: "FastAPI Service"
- **Color**: "#4CAF50"
- **Icon**: "server"

### Nodes (`DiagramNode[]`)

For each node:

- **ID**: "client"
- **Label**: "Client App"
- **Type**: `client`
- **x**: 100
- **y**: 200
- **Connections** (optional): ["nginx"]
- **Status** (optional): `healthy`

---

- **ID**: "nginx"
- **Label**: "nginx Load Balancer"
- **Type**: `gateway`
- **x**: 250
- **y**: 200
- **Connections** (optional): ["app1", "app2", "app3"]
- **Status** (optional): `healthy`

---

- **ID**: "app1"
- **Label**: "ticket-service-1"
- **Type**: `service`
- **x**: 400
- **y**: 150
- **Connections** (optional): ["postgres", "mongo", "redis", "kafka"]
- **Status** (optional): `healthy`

---

- **ID**: "app2"
- **Label**: "ticket-service-2"
- **Type**: `service`
- **x**: 400
- **y**: 200
- **Connections** (optional): ["postgres", "mongo", "redis", "kafka"]
- **Status** (optional): `healthy`

---

- **ID**: "app3"
- **Label**: "ticket-service-3"
- **Type**: `service`
- **x**: 400
- **y**: 250
- **Connections** (optional): ["postgres", "mongo", "redis", "kafka"]
- **Status** (optional): `healthy`

---

- **ID**: "postgres"
- **Label**: "PostgreSQL"
- **Type**: `database`
- **x**: 600
- **y**: 150
- **Connections** (optional): []
- **Status** (optional): `healthy`

---

- **ID**: "mongo"
- **Label**: "MongoDB"
- **Type**: `database`
- **x**: 600
- **y**: 250
- **Connections** (optional): []
- **Status** (optional): `healthy`

---

- **ID**: "redis"
- **Label**: "Redis"
- **Type**: `database`
- **x**: 600
- **y**: 200
- **Connections** (optional): []
- **Status** (optional): `healthy`

---

- **ID**: "kafka"
- **Label**: "Kafka"
- **Type**: `queue`
- **x**: 600
- **y**: 350
- **Connections** (optional): ["billboard_svc", "wallet_svc"]
- **Status** (optional): `healthy`

---

- **ID**: "billboard_svc"
- **Label**: "Billboard Service"
- **Type**: `service`
- **x**: 750
- **y**: 350
- **Connections** (optional): []
- **Status** (optional): `healthy`

---

- **ID**: "payment_svc"
- **Label**: "Payment Service"
- **Type**: `service`
- **x**: 600
- **y**: 50
- **Connections** (optional): []
- **Status** (optional): `healthy`

### Connections (`DiagramConnection[]`)

- **ID**: "c1"
- **From**: "client"
- **To**: "nginx"
- **Label** (optional): "HTTP/REST"
- **Protocol** (optional): "HTTP"
- **Is Active** (optional): `true`

---

- **ID**: "c2"
- **From**: "nginx"
- **To**: "app1"
- **Label** (optional): "HTTP"
- **Protocol** (optional): "HTTP"
- **Is Active** (optional): `true`

---

- **ID**: "c3"
- **From**: "app1"
- **To**: "postgres"
- **Label** (optional): "Tickets/Seats"
- **Protocol** (optional): "SQL"
- **Is Active** (optional): `true`

---

- **ID**: "c4"
- **From**: "app1"
- **To**: "mongo"
- **Label** (optional): "Showtime Data"
- **Protocol** (optional): "MongoDB"
- **Is Active** (optional): `true`

---

- **ID**: "c5"
- **From**: "app1"
- **To**: "kafka"
- **Label** (optional): "Event Consume"
- **Protocol** (optional): "Kafka"
- **Is Active** (optional): `true`

---

- **ID**: "c6"
- **From**: "billboard_svc"
- **To**: "kafka"
- **Label** (optional): "Billboard Events"
- **Protocol** (optional): "Kafka"
- **Is Active** (optional): `true`

---

## 8. Data Flow (`DataFlowModel`)

### Request Flow (`FlowStep[]`)

For each step:

- **Number**: 1
- **Title**: "HTTP Request"
- **Description**: "Client sends REST request to FastAPI endpoint via nginx load balancer"
- **Icon**: "globe"

---

- **Number**: 2
- **Title**: "Middleware Processing"
- **Description**: "JWT validation, rate limiting, logging middleware execute"
- **Icon**: "filter"

---

- **Number**: 3
- **Title**: "Use Case Execution"
- **Description**: "Controller delegates to use case which orchestrates domain services"
- **Icon**: "play"

---

- **Number**: 4
- **Title**: "Domain Logic"
- **Description**: "Domain services apply business rules, validate constraints"
- **Icon**: "check"

---

- **Number**: 5
- **Title**: "Data Persistence"
- **Description**: "Repository implementations persist/retrieve data from PostgreSQL or MongoDB"
- **Icon**: "database"

---

- **Number**: 6
- **Title**: "Response Generation"
- **Description**: "DTOs serialized to JSON response with appropriate HTTP status"
- **Icon**: "send"

### Event Flow (`FlowStep[]`)

For each step:

- **Number**: 1
- **Title**: "Billboard Event Published"
- **Description**: "Billboard service publishes cinema/theater/showtime events to Kafka"
- **Icon**: "broadcast"

---

- **Number**: 2
- **Title**: "Event Consumption"
- **Description**: "ticket-service Kafka consumer polls for billboard.events"
- **Icon**: "download"

---

- **Number**: 3
- **Title**: "Deduplication Check"
- **Description**: "Event ID checked against MongoDB deduplication collection"
- **Icon**: "copy"

---

- **Number**: 4
- **Title**: "Event Processing"
- **Description**: "BillboardReplicationService applies event to MongoDB collections"
- **Icon**: "database"

---

- **Number**: 5
- **Title**: "Offset Commit"
- **Description**: "Kafka consumer commits offset after successful processing"
- **Icon**: "check"

---

## 9. Tech Decisions (`TechDecisionsModel`)

For each decision (`TechDecisionModel`):

- **Title**: FastAPI over Flask/Django
- **Problem**: "Need async-first web framework with native OpenAPI support and type safety"
- **Solution**: "FastAPI with Pydantic for request/response validation, automatic OpenAPI docs"
- **Alternatives**:
  - Flask - synchronous, manual validation
  - Django - heavyweight, not async-native
- **Outcome**: "Fast API chosen for performance and developer experience"
- **Icon**: "star"

---

- **Title**: PostgreSQL + MongoDB dual database
- **Problem**: "Need transactional writes for tickets but flexible read model for showtime data"
- **Solution**: "PostgreSQL for tickets/seats (ACID), MongoDB for replicated showtime/cinema (schema flexibility)"
- **Alternatives**:
  - Single PostgreSQL - less flexible for evolving showtime schema
  - Single MongoDB - weaker consistency for ticket transactions
- **Outcome**: "Best of both worlds with each database optimized for its workload"
- **Icon**: "database"

---

- **Title**: Kafka for event replication
- **Problem**: "Need eventual consistency for showtime data from billboard service"
- **Solution**: "Kafka consumer replicates billboard.events to MongoDB with deduplication"
- **Alternatives**:
  - Direct HTTP polling - higher latency, tighter coupling
  - GraphQL subscriptions - less mature for this use case
- **Outcome**: "Decoupled, scalable event-driven data replication"
- **Icon**: "stream"
