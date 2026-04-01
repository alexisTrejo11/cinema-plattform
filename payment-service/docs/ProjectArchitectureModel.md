# Architecture Model

## 1. Layers (`ArchitectureLayer[]`)

### Layer 1: Presentation Layer

- **Name**: Presentation Layer
- **Description**: HTTP API endpoints via FastAPI with role-based access control
- **Components**:
  - FastAPI routers (admin_payment_controller, customer_payment_controller, staff_payment_controller, payment_methods_controllers)
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
- **Description**: Use cases and command/query handlers implementing business workflows
- **Components**:
  - CustomerPaymentUseCases
  - StaffPaymentUseCases
  - AdminPaymentUseCases
  - PaymentMethodUseCases
  - Commands (ProcessPayCommand, RefundPaymentCommand, AddCreditCommand)
  - Application Services (PaymentApplicationService)
- **Color**: "#7ED321"
- **Expanded** (optional): `true`
- **Responsibilities** (optional):
  - Orchestrate domain operations
  - Transaction management
  - Business workflow implementation
  - Cross-service assertions
- **Technologies** (optional):
  - CQRS pattern
  - Command/Query separation

---

### Layer 3: Domain Layer

- **Name**: Domain Layer
- **Description**: Core business entities, value objects, domain events, and business rules
- **Components**:
  - Entities: Payment, PaymentMethod, StoredPaymentMethod, Transaction
  - Value Objects: Money, PaymentId, WalletId, TransactionId, UserId, PaymentStatus, PaymentType
  - Domain Events: PaymentCreated, PaymentCompleted, PaymentRefunded, WalletCredited
  - Domain Exceptions
  - Repository Interfaces
- **Color**: "#F5A623"
- **Expanded** (optional): `true`
- **Responsibilities** (optional):
  - Encapsulate business rules
  - Ensure domain invariants
  - Emit domain events
  - Define repository contracts
- **Technologies** (optional):
  - Pure Python (no framework dependencies)
  - Pydantic BaseModel

---

### Layer 4: Infrastructure Layer

- **Name**: Infrastructure Layer
- **Description**: External integrations - database persistence, messaging, gRPC clients, payment gateways
- **Components**:
  - SQLAlchemy Repository implementations
  - Kafka producer/consumer
  - gRPC client
  - PostgreSQL models
  - Model mappers
- **Color**: "#D0021B"
- **Expanded** (optional): `false`
- **Responsibilities** (optional):
  - Database persistence
  - Message publishing
  - External service calls
  - Protocol translation
- **Technologies** (optional):
  - SQLAlchemy (async)
  - kafka-python
  - grpcio
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

### Pattern 2: Aggregate Root

- **Title**: Aggregate Root
- **Emoji**: "🌳"
- **Description**: Payment and Transaction entities as aggregate roots, encapsulating related objects and enforcing invariants
- **Category**: "Domain"
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

### Pattern 4: Domain Events

- **Title**: Domain Events
- **Emoji**: "📣"
- **Description**: Events emitted by aggregates to record state changes for event-driven workflows
- **Category**: "Event-Driven"
- **Badge**: "Secondary"
- **GitHub Example URL** (optional): ""

---

### Pattern 5: CQRS

- **Title**: Command Query Responsibility Segregation
- **Emoji**: "⚖️"
- **Description**: Separate command handlers (process payment, refund) from query handlers (get history, get summary)
- **Category**: "Architecture"
- **Badge**: "Secondary"
- **GitHub Example URL** (optional): ""

---

## 3. Scalability Strategies (`StrategyItem[]`)

- **Title**: Horizontal Scaling
- **Description**: Deploy multiple instances of payment-service behind load balancer for horizontal scaling

---

- **Title**: Database Connection Pooling
- **Description**: Use SQLAlchemy async with connection pooling to handle concurrent requests efficiently

---

- **Title**: Kafka Partitioning
- **Description**: Use payment_id as Kafka message key for ordered processing within partitions

---

## 4. Security Strategies (`StrategyItem[]`)

- **Title**: JWT Authentication
- **Description**: All API endpoints require valid JWT token with user_id (sub) and roles claims

---

- **Title**: Role-Based Access Control
- **Description**: Admin endpoints require admin/superadmin role, staff endpoints require admin/manager/employee role

---

- **Title**: Input Validation
- **Description**: All request bodies validated via Pydantic models with strict type checking

---

- **Title**: PCI Compliance
- **Description**: No raw card data stored; use Stripe tokenization for payment methods

---

## 5. Cache Strategies (`CacheStrategy[]`)

- **Name**: Redis Cache
- **Description**: Optional Redis caching via fastapi-cache for frequently accessed data
- **TTL**: "5 minutes"
- **Coverage**: "Payment methods catalog, user payment summaries"

---

## 6. Architecture Features (`ArchitectureFeature[]`)

- **Title**: Event-Driven Communication
- **Emoji**: "📤"
- **Description**: Payment service publishes events to Kafka for inter-service coordination

---

- **Title**: gRPC Cross-Service Calls
- **Emoji**: "🔗"
- **Description**: Synchronous calls to ticket/food services for purchase assertions

---

- **Title**: Soft Delete Pattern
- **Description**: Payment methods use soft-delete (deleted_at timestamp) to preserve audit trail

---

## 7. Architecture Diagram (`ArchitectureDiagramModel`)

### Legend (`LegendItem[]`)

- **Type**: "client"
- **Label**: "Client Application"
- **Color**: "#4A90E2"
- **Icon**: "👤"

- **Type**: "service"
- **Label**: "Payment Service"
- **Color**: "#7ED321"
- **Icon**: "⚙️"

- **Type**: "database"
- **Label**: "PostgreSQL"
- **Color**: "#F5A623"
- **Icon**: "🗄️"

- **Type**: "queue"
- **Label**: "Kafka"
- **Color**: "#D0021B"
- **Icon**: "📤"

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
- **Connections**: ["payment-service"]
- **Status** (optional): `healthy`

- **ID**: "payment-service"
- **Label**: "Payment Service"
- **Type**: `service`
- **x**: 500
- **y**: 100
- **Connections**: ["postgres", "kafka", "stripe", "ticket-service"]
- **Status** (optional): `healthy`
- **Traffic**: "1000 TPS"

- **ID**: "postgres"
- **Label**: "PostgreSQL"
- **Type**: `database`
- **x**: 500
- **y**: 300
- **Connections**: []
- **Status** (optional): `healthy`

- **ID**: "kafka"
- **Label**: "Kafka"
- **Type**: `queue`
- **x**: 700
- **y**: 100
- **Connections**: ["ticket-service", "user-service"]
- **Status** (optional): `healthy`

- **ID**: "stripe"
- **Label**: "Stripe API"
- **Type**: `service`
- **x**: 700
- **y**: 200
- **Connections**: []

- **ID**: "ticket-service"
- **Label**: "Ticket Service (gRPC)"
- **Type**: `service`
- **x**: 900
- **y**: 100
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
- **To**: "payment-service"
- **Label** (optional): "HTTP/REST"
- **Protocol** (optional): "HTTP"
- **Is Active** (optional): `true`

- **ID**: "conn-3"
- **From**: "payment-service"
- **To**: "postgres"
- **Label** (optional): "SQL"
- **Protocol** (optional): "PostgreSQL"
- **Is Active** (optional): `true`

- **ID**: "conn-4"
- **From**: "payment-service"
- **To**: "kafka"
- **Label** (optional): "Events"
- **Protocol** (optional): "Kafka"
- **Is Active** (optional): `true`

- **ID**: "conn-5"
- **From**: "payment-service"
- **To**: "stripe"
- **Label** (optional): "Payment"
- **Protocol** (optional): "REST"
- **Is Active** (optional): `true`

- **ID**: "conn-6"
- **From**: "payment-service"
- **To**: "ticket-service"
- **Label** (optional): "Assertions"
- **Protocol** (optional): "gRPC"
- **Is Active** (optional): `false`

- **ID**: "conn-7"
- **From**: "kafka"
- **To**: "ticket-service"
- **Label** (optional): "Events"
- **Protocol** (optional): "Kafka"
- **Is Active** (optional): `true`

---

## 8. Data Flow (`DataFlowModel`)

### Request Flow (`FlowStep[]`)

- **Number**: 1
- **Title**: "Client Request"
- **Description**: Client sends authenticated HTTP request with JWT token to payment endpoint
- **Icon**: "👤"

- **Number**: 2
- **Title**: "API Validation"
- **Description**: FastAPI validates JWT, checks roles, validates request body via Pydantic
- **Icon**: "🔒"

- **Number**: 3
- **Title**: "Use Case Execution"
- **Description**: Controller calls use case which orchestrates domain operations and emits events
- **Icon**: "⚙️"

- **Number**: 4
- **Title**: "Persistence"
- **Description**: Domain entities saved to PostgreSQL via SQLAlchemy repository
- **Icon**: "🗄️"

- **Number**: 5
- **Title**: "Event Publishing"
- **Description**: Payment events published to Kafka for inter-service notification
- **Icon**: "📤"

- **Number**: 6
- **Title**: "Response"
- **Description**: HTTP response returned with payment data and status
- **Icon**: "✅"

### Event Flow (`FlowStep[]`)

- **Number**: 1
- **Title**: "Payment Created Event"
- **Description**: PaymentCreated event emitted when new payment intent is created
- **Icon**: "💰"

- **Number**: 2
- **Title**: "Kafka Publishing"
- **Description**: Event published to payment.events Kafka topic
- **Icon**: "📤"

- **Number**: 3
- **Title**: "Consumer Processing"
- **Description**: Ticket/User services consume and process the event
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

- **Title**: "Kafka over RabbitMQ"
- **Problem**: "Need durable, scalable event streaming for inter-service communication"
- **Solution**: "Kafka provides durability, replay capability, and better scalability"
- **Alternatives**:
  - RabbitMQ (simpler, less scalable)
  - AWS SQS (vendor lock-in)
- **Outcome**: "Event replay, ordered processing, high throughput"
- **Icon**: "📤"

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
