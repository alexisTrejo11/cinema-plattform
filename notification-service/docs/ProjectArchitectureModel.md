# Architecture Model

## 1. Layers (`ArchitectureLayer[]`)

### Layer 1 - Presentation

- **Name**: Presentation Layer
- **Description**: FastAPI HTTP API layer handling REST endpoints, authentication, rate limiting, and request logging
- **Components**:
  - notification_controller.py (API router with endpoints)
  - dependencies.py (FastAPI dependency injection)
  - middleware/ (JWT validation, logging)
- **Color**: #4A90E2
- **Expanded** (optional): `true`
- **Responsibilities** (optional):
  - HTTP request/response handling
  - JWT authentication validation
  - Rate limiting enforcement
  - Request logging and audit trails
- **Technologies** (optional):
  - FastAPI
  - SlowAPI
  - PyJWT

---

### Layer 2 - Application

- **Name**: Application Layer
- **Description**: Use cases orchestrating domain logic, command/query handlers, DTOs, and event processing
- **Components**:
  - commands/ (CreateNotificationCommand, ProcessIncomingNotificationEventCommand)
  - queries/ (GetNotificationByIdQuery, ListNotificationsQuery)
  - usecases/ (CreateNotificationUseCase, GetNotificationByIdUseCase, etc.)
  - dtos.py (NotificationResponse, NotificationListResponse)
- **Color**: #50C878
- **Expanded** (optional): `true`
- **Responsibilities** (optional):
  - Business logic orchestration
  - Command validation and processing
  - Query execution
  - Event routing and deduplication
- **Technologies** (optional):
  - Pydantic v2
  - Python dataclasses

---

### Layer 3 - Domain

- **Name**: Domain Layer
- **Description**: Core business entities, value objects, enums, and repository/service interfaces
- **Components**:
  - entities/models.py (Notification aggregate)
  - entities/content.py (NotificationContent VO)
  - entities/recipient.py (Recipient VO)
  - enums.py (NotificationType, Channel, Status)
  - repository.py (NotificationRepository ABC)
  - sending_service.py (SendingService ABC)
- **Color**: #FFD700
- **Expanded** (optional): `true`
- **Responsibilities** (optional):
  - Notification lifecycle state management
  - Validation of business rules
  - Status transitions (PENDING → SENT/FAILED)
  - Port interfaces for infrastructure
- **Technologies** (optional):
  - Pydantic v2

---

### Layer 4 - Infrastructure

- **Name**: Infrastructure Layer
- **Description**: External adapters implementing domain ports (MongoDB, Redis, Kafka, SMTP, Twilio, HTTP)
- **Components**:
  - repository/mongo_notification_repository.py
  - email/mail_service.py, html_templates.py
  - message/sms_message_services.py
  - external/user_profile_http_service.py
  - events/infrastructure/kafka_publisher.py
  - config/ (MongoDB, Kafka, Redis configurations)
- **Color**: #FF6B6B
- **Expanded** (optional): `true`
- **Responsibilities** (optional):
  - MongoDB document storage
  - SMTP email delivery
  - Twilio SMS delivery
  - Kafka event consumption/publishing
  - HTTP user directory lookup
- **Technologies** (optional):
  - Motor, pymongo
  - Jinja2
  - twilio
  - kafka-python
  - httpx

---

## 2. Design Patterns (`DesignPattern[]`)

For each pattern:

- **Title**: Hexagonal Architecture (Ports & Adapters)
- **Emoji**: 🔷
- **Description**: Clean separation between domain (core) and infrastructure (adapters) with port interfaces defining boundaries
- **Category**: Architectural
- **Badge**: DDD
- **GitHub Example URL** (optional): ""

---

- **Title**: Domain-Driven Design
- **Emoji**: 🏛️
- **Description**: Rich domain model with aggregates, value objects, and domain services following DDD principles
- **Category**: Architectural
- **Badge**: DDD
- **GitHub Example URL** (optional): ""

---

- **Title**: Command Query Responsibility Segregation
- **Emoji**: ⚡
- **Description**: Separate command (Create, Update, Process) and query (Get, List) operations with dedicated handlers
- **Category**: Architectural
- **Badge**: CQRS
- **GitHub Example URL** (optional): ""

---

- **Title**: Event-Driven Architecture
- **Emoji**: 📡
- **Description**: Kafka-based event consumption and publishing for decoupled, reactive system design
- **Category**: Architectural
- **Badge**: EDA
- **GitHub Example URL** (optional): ""

---

- **Title**: Dependency Injection
- **Emoji**: 💉
- **Description**: FastAPI Depends for constructor injection of repositories and services into use cases
- **Category**: Creational
- **Badge**: DI
- **GitHub Example URL** (optional): ""

---

- **Title**: Repository Pattern
- **Emoji**: 📦
- **Description**: Abstract data access with NotificationRepository interface, implemented by MongoNotificationRepository
- **Category**: Data Access
- **Badge**: Repository
- **GitHub Example URL** (optional): ""

---

## 3. Scalability Strategies (`StrategyItem[]`)

- **Title**: Horizontal Scaling
- **Description**: Multiple instances of the notification service can run behind a load balancer with Kafka consumer group distribution for parallel event processing

---

- **Title**: Async Processing
- **Description**: Full async/await architecture with Motor (MongoDB), aiohttp (HTTP), and kafka-python for non-blocking I/O and high concurrency

---

- **Title**: Kafka Consumer Groups
- **Description**: Consumer group configuration allows multiple service instances to share partition processing workload

---

## 4. Security Strategies (`StrategyItem[]`)

- **Title**: JWT Authentication
- **Description**: All API endpoints (except health checks) require valid JWT Bearer tokens with configurable algorithm and optional issuer/audience validation

---

- **Title**: Rate Limiting
- **Description**: SlowAPI-based rate limiting (60 requests/minute default) prevents abuse and ensures fair resource usage

---

- **Title**: Input Validation
- **Description**: Pydantic v2 models with strict type checking and validation for all command and query DTOs

---

- **Title**: Environment-Based Secrets
- **Description**: Sensitive credentials (JWT_SECRET_KEY, SMTP_PASSWORD, TWILIO_AUTH_TOKEN) loaded from environment variables or .env file

---

## 5. Cache Strategies (`CacheStrategy[]`)

- **Name**: Redis Response Caching
- **Description**: FastAPI-Cache with Redis backend for caching frequently accessed data
- **TTL**: Configurable (default 300s for notification queries)
- **Coverage**: Read-heavy endpoints (GET by ID, list with common filters)

---

- **Name**: No Cache for Mutations
- **Description**: POST, PUT, PATCH operations bypass cache to ensure data consistency
- **TTL**: N/A
- **Coverage**: All write operations

---

## 6. Architecture Features (`ArchitectureFeature[]`)

- **Title**: Notification Lifecycle Management
- **Emoji**: 📬
- **Description**: Full state machine for notifications: PENDING → SENT/FAILED, with DELIVERED and READ tracking for confirmation

---

- **Title**: Multi-Channel Routing
- **Emoji**: 📱
- **Description**: Channel-based delivery routing to EMAIL (SMTP), SMS (Twilio), PUSH_NOTIFICATION, or IN_APP

---

- **Title**: Event Deduplication
- **Emoji**: 🔄
- **Description**: Incoming Kafka events are deduplicated by event_id to prevent duplicate notifications from reprocessing

---

- **Title**: Attention Tracking
- **Emoji**: ⚠️
- **Description**: Failed and important notifications are flagged for operational monitoring with OPEN/ACKNOWLEDGED/RESOLVED states

---

## 7. Architecture Diagram (`ArchitectureDiagramModel`)

### Legend (`LegendItem[]`)

- **Type**: client
- **Label**: Client/API Consumer
- **Color**: #4A90E2
- **Icon**: user

- **Type**: service
- **Label**: Notification Service
- **Color**: #50C878
- **Icon**: server

- **Type**: database
- **Label**: MongoDB
- **Color**: #FFD700
- **Icon**: database

- **Type**: queue
- **Label**: Kafka
- **Color**: #FF6B6B
- **Icon**: activity

- **Type**: gateway
- **Label**: External Providers
- **Color**: #9B59B6
- **Icon**: mail

### Nodes (`DiagramNode[]`)

For each node:

- **ID**: notification-service
- **Label**: Notification Service
- **Type**: `service`
- **x**: 400
- **y**: 200
- **Connections**: mongo, redis, kafka, smtp, twilio, user-service
- **Status** (optional): `healthy`

- **ID**: api-clients
- **Label**: API Clients
- **Type**: `client`
- **x**: 100
- **y**: 200
- **Connections**: notification-service

- **ID**: mongo
- **Label**: MongoDB
- **Type**: `database`
- **x**: 550
- **y**: 100
- **Connections**: notification-service

- **ID**: redis
- **Label**: Redis
- **Type**: `database`
- **x**: 550
- **y**: 300
- **Connections**: notification-service

- **ID**: kafka
- **Label**: Kafka
- **Type**: `queue`
- **x**: 250
- **y**: 100
- **Connections**: notification-service, user-service, wallet-service

- **ID**: smtp
- **Label**: SMTP Server
- **Type**: `gateway`
- **x**: 700
- **y**: 150
- **Connections**: notification-service

- **ID**: twilio
- **Label**: Twilio API
- **Type**: `gateway`
- **x**: 700
- **y**: 250
- **Connections**: notification-service

- **ID**: user-service
- **Label**: User Service
- **Type**: `service`
- **x**: 100
- **y**: 50
- **Connections**: kafka

- **ID**: wallet-service
- **Label**: Wallet Service
- **Type**: `service`
- **x**: 400
- **y**: 50
- **Connections**: kafka

### Connections (`DiagramConnection[]`)

- **ID**: api-to-notif
- **From**: api-clients
- **To**: notification-service
- **Label**: REST API
- **Protocol** (optional): HTTP
- **Is Active** (optional): `true`

- **ID**: notif-to-mongo
- **From**: notification-service
- **To**: mongo
- **Label**: Store/Query
- **Protocol** (optional): MongoDB Wire
- **Is Active** (optional): `true`

- **ID**: notif-to-redis
- **From**: notification-service
- **To**: redis
- **Label**: Cache
- **Protocol** (optional): Redis
- **Is Active** (optional): `true`

- **ID**: kafka-to-notif
- **From**: kafka
- **To**: notification-service
- **Label**: Consume Events
- **Protocol** (optional): Kafka
- **Is Active** (optional): `true`

- **ID**: notif-to-smtp
- **From**: notification-service
- **To**: smtp
- **Label**: Send Email
- **Protocol** (optional): SMTP
- **Is Active** (optional): `true`

- **ID**: notif-to-twilio
- **From**: notification-service
- **To**: twilio
- **Label**: Send SMS
- **Protocol** (optional): REST
- **Is Active** (optional): `true`

- **ID**: user-to-kafka
- **From**: user-service
- **To**: kafka
- **Label**: Publish Events
- **Protocol** (optional): Kafka
- **Is Active** (optional): `true`

- **ID**: wallet-to-kafka
- **From**: wallet-service
- **To**: kafka
- **Label**: Publish Events
- **Protocol** (optional): Kafka
- **Is Active** (optional): `true`

---

## 8. Data Flow (`DataFlowModel`)

### Request Flow (`FlowStep[]`)

For each step:

- **Number**: 1
- **Title**: API Request
- **Description**: Client sends POST /api/v2/notifications with JWT Bearer token
- **Icon**: arrow-right

- **Number**: 2
- **Title**: Authentication
- **Description**: JWT middleware validates token and extracts user context
- **Icon**: shield

- **Number**: 3
- **Title**: Command Validation
- **Description**: CreateNotificationCommand is validated with Pydantic
- **Icon**: check

- **Number**: 4
- **Title**: Use Case Execution
- **Description**: CreateNotificationUseCase orchestrates domain logic
- **Icon**: play

- **Number**: 5
- **Title**: Repository Save
- **Description**: Notification saved to MongoDB with PENDING status
- **Icon**: database

- **Number**: 6
- **Title**: Send Notification
- **Description**: SendingService routes to EmailService or SmsMessageService
- **Icon**: send

- **Number**: 7
- **Title**: Status Update
- **Description**: Notification status updated to SENT or FAILED
- **Icon**: check-circle

- **Number**: 8
- **Title**: Response
- **Description**: NotificationResponse returned to client
- **Icon**: arrow-left

### Event Flow (`FlowStep[]`)

For each step:

- **Number**: 1
- **Title**: Event Published
- **Description**: Another service (user, wallet) publishes event to Kafka
- **Icon**: radio

- **Number**: 2
- **Title**: Event Consumed
- **Description**: Kafka consumer receives event from configured topics
- **Icon**: inbox

- **Number**: 3
- **Title**: Deduplication Check
- **Description**: Event ID checked against MongoDB to skip duplicates
- **Icon**: copy

- **Number**: 4
- **Title**: Recipient Resolution
- **Description**: UserProfileService resolves contact info if not in payload
- **Icon**: users

- **Number**: 5
- **Title**: Event Routing
- **Description**: Event type mapped to notification type, channel, importance
- **Icon**: git-branch

- **Number**: 6
- **Title**: Notification Created
- **Description**: Notification entity created with routing decision
- **Icon**: bell

- **Number**: 7
- **Title**: Delivery Attempt
- **Description**: SendingService delivers via configured channel
- **Icon**: send

- **Number**: 8
- **Title**: Status Tracking
- **Description**: Final status (SENT/FAILED) persisted with attention flag if needed
- **Icon**: flag

---

## 9. Tech Decisions (`TechDecisionsModel`)

For each decision (`TechDecisionModel`):

- **Title**: MongoDB over PostgreSQL for Notifications
- **Problem**: Notifications are document-oriented with varying schemas and require flexible querying by multiple fields
- **Solution**: MongoDB with Motor async driver for high-performance document storage
- **Alternatives**:
  - PostgreSQL with JSONB columns
  - Elasticsearch for search-heavy workloads
- **Outcome**: Chosen for schema flexibility and async performance
- **Icon**: database

---

- **Title**: Kafka for Event Streaming
- **Problem**: Need to consume events from multiple services (user, wallet) without tight coupling
- **Solution**: Kafka consumer with configurable topics and consumer group
- **Alternatives**:
  - RabbitMQ for point-to-point
  - Direct HTTP webhooks
- **Outcome**: Chosen for durability, replay capability, and multi-consumer support
- **Icon**: activity

---

- **Title**: Twilio for SMS Delivery
- **Problem**: Need reliable SMS delivery with global coverage
- **Solution**: Twilio REST API with graceful fallback when disabled
- **Alternatives**:
  - AWS SNS
  - Nexmo/Vonage
- **Outcome**: Chosen for reliability and Python SDK support
- **Icon**: message-circle

---

- **Title**: SMTP for Email Delivery
- **Problem**: Need to send HTML emails with templates
- **Solution**: Direct SMTP connection with Jinja2 template rendering
- **Alternatives**:
  - SendGrid API
  - AWS SES
- **Outcome**: Chosen for simplicity and full template control
- **Icon**: mail

---

- **Title**: DDD Architecture
- **Problem**: Need clear separation between business logic and infrastructure
- **Solution**: Hexagonal architecture with domain, application, infrastructure, presentation layers
- **Alternatives**:
  - Simple layered architecture
  - Microservices without clear boundaries
- **Outcome**: Chosen for maintainability and testability
- **Icon**: layers
