# Project Features

## Feature List (`ProjectFeature[]`)

### Feature 1

- **ID**: notification-api
- **Title**: REST API for Notification Management
- **Description**: FastAPI-based REST API for creating, retrieving, and listing notifications with JWT authentication, rate limiting, and pagination support.
- **Icon**: api
- **Category** (`FeatureCategory`): `api`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - POST /api/v2/notifications - Create new notification
  - GET /api/v2/notifications/{id} - Get notification by ID
  - GET /api/v2/notifications - List with filters (type, channel, status, user, etc.)
  - JWT Bearer token authentication
  - SlowAPI rate limiting (60 req/min)
- **Tech Stack** (optional):
  - FastAPI
  - Pydantic v2
  - SlowAPI
  - PyJWT
- **Metrics** (optional, `FeatureMetric[]`):
  - **Label**: Response Time
  - **Value**: <100ms
  - **Trend** (optional): `stable`
  - **Icon** (optional): "zap"
- **Code Snippet** (optional, `CodeSnippet`):
  - **Language**: python
  - **Filename** (optional): notification_controller.py
  - **Code**:
    ```python
    @router.post("", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
    async def create_notification(
        command: CreateNotificationCommand,
        usecase: CreateNotificationUseCase = Depends(get_create_notification_usecase),
    ):
        return await usecase.execute(command)
    ```
- **GitHub Example URL** (optional): ""

---

### Feature 2

- **ID**: event-driven-processing
- **Title**: Kafka Event-Driven Notification Processing
- **Description**: Consumes events from Kafka topics (notification.incoming, cinema.user-service.events, wallet.events) to automatically create and deliver notifications with deduplication.
- **Icon**: bolt
- **Category** (`FeatureCategory`): `messaging`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Async Kafka consumer with configurable polling
  - Event deduplication by event_id
  - Automatic recipient resolution via user directory lookup
  - Important event detection (failed, deleted, fraud, etc.)
  - Store-only mode for certain event types
- **Tech Stack** (optional):
  - kafka-python
  - Motor (async MongoDB)
- **Code Snippet** (optional, `CodeSnippet`):
  - **Language**: python
  - **Filename** (optional): kafka_config.py
  - **Code**:
    ```python
    IMPORTANT_EVENT_KEYWORDS = ("failed", "deleted", "banned", "fraud", "chargeback", "alert")
    IMPORTANT_EVENT_TYPES = {
        "user.lifecycle.deleted",
        "user.lifecycle.banned",
        "payment.failed",
        "wallet.payment_failed",
    }
    ```
- **GitHub Example URL** (optional): ""

---

### Feature 3

- **ID**: email-delivery
- **Title**: Email Notification Delivery (SMTP)
- **Description**: Send HTML email notifications using SMTP with Jinja2 template rendering for consistent branding and personalization.
- **Icon**: mail
- **Category** (`FeatureCategory`): `messaging`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - SMTP with TLS support
  - Jinja2 HTML template rendering
  - Pre-built templates: USER_ACTIVATION, AUTH_CODE, TICKET_PURCHASE, GENERIC_INFO
  - Configurable sender name and address
- **Tech Stack** (optional):
  - Jinja2
  - aiosmtplib (async SMTP)
- **Code Snippet** (optional, `CodeSnippet`):
  - **Language**: python
  - **Filename** (optional): mail_service.py
  - **Code**:
    ```python
    async def send(self, notification: Notification) -> None:
        html_body = self._render_template(notification)
        await self._smtp_client.send_message(msg)
    ```
- **GitHub Example URL** (optional): ""

---

### Feature 4

- **ID**: sms-delivery
- **Title**: SMS Notification Delivery (Twilio)
- **Description**: Send text message notifications via Twilio API with graceful fallback when disabled.
- **Icon**: message-circle
- **Category** (`FeatureCategory`): `messaging`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Twilio REST API integration
  - Configurable Twilio phone number
  - Graceful no-op when Twilio is disabled
  - Error handling for delivery failures
- **Tech Stack** (optional):
  - twilio
- **Code Snippet** (optional, `CodeSnippet`):
  - **Language**: python
  - **Filename** (optional): sms_message_services.py
  - **Code**:
    ```python
    if not settings.TWILIO_ENABLED:
        logger.info("Twilio is disabled, skipping SMS send")
        return
    message = self._client.messages.create(body=body, from_=from_number, to=to)
    ```
- **GitHub Example URL** (optional): ""

---

### Feature 5

- **ID**: mongo-persistence
- **Title**: MongoDB Document Storage
- **Description**: Async MongoDB persistence using Motor driver for notification history with rich querying capabilities.
- **Icon**: database
- **Category** (`FeatureCategory`): `database`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Async Motor driver
  - Notification aggregate with full lifecycle tracking
  - Query by notification_id, user_id, event_id, type, channel, status
  - Pagination support (limit/offset)
- **Tech Stack** (optional):
  - Motor (async MongoDB driver)
  - Pymongo
- **Code Snippet** (optional, `CodeSnippet`):
  - **Language**: python
  - **Filename** (optional): mongo_notification_repository.py
  - **Code**:
    ```python
    async def save(self, notification: Notification) -> Notification:
        doc = notification.to_document()
        await self._collection.insert_one(doc)
        return notification
    ```
- **GitHub Example URL** (optional): ""

---

### Feature 6

- **ID**: user-directory-integration
- **Title**: User Directory Integration
- **Description**: HTTP-based user contact lookup from user-service for recipient resolution when contact info is not provided in the event payload.
- **Icon**: users
- **Category** (`FeatureCategory`): `integration`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - HTTP client to user-service
  - Configurable timeout (default 3s)
  - Fallback to payload-provided contact info
  - Graceful handling when lookup fails
- **Tech Stack** (optional):
  - httpx
- **Code Snippet** (optional, `CodeSnippet`):
  - **Language**: python
  - **Filename** (optional): user_profile_http_service.py
  - **Code**:
    ```python
    async def resolve_contact(self, user_id: str) -> UserContact | None:
        response = await self._client.get(f"/api/v2/users/{user_id}/contact")
        return UserContact(**response.json())
    ```
- **GitHub Example URL** (optional): ""

---

### Feature 7

- **ID**: attention-tracking
- **Title**: Attention Tracking for Operations
- **Description**: Operational monitoring system that flags important or failed notifications requiring human follow-up.
- **Icon**: alert-triangle
- **Category** (`FeatureCategory`): `monitoring`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - is_important flag based on event type/keywords
  - AttentionStatus: NONE, OPEN, ACKNOWLEDGED, RESOLVED
  - Automatic OPEN status for failed/important notifications
  - Filter by attention_status in list API
- **Tech Stack** (optional):
  - MongoDB queries
- **Code Snippet** (optional, `CodeSnippet`):
  - **Language**: python
  - **Filename** (optional): models.py
  - **Code**:
    ```python
    def mark_attention_open(self) -> None:
        self.is_important = True
        self.attention_status = NotificationAttentionStatus.OPEN
    ```
- **GitHub Example URL** (optional): ""

---

### Feature 8

- **ID**: redis-caching
- **Title**: Redis Caching
- **Description**: FastAPI-Cache integration with Redis for improved performance on frequently accessed data.
- **Icon**: cache
- **Category** (`FeatureCategory`): `caching`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Redis backend for FastAPI-Cache
  - Configurable TTL
  - Async Redis operations
- **Tech Stack** (optional):
  - fastapi-cache
  - redis
- **Code Snippet** (optional, `CodeSnippet`):
  - **Language**: python
  - **Filename** (optional): cache_config.py
  - **Code**:
    ```python
    @cache(expire=300)
    async def get_cached_data():
        return await fetch_from_db()
    ```
- **GitHub Example URL** (optional): ""

---

### Feature 9

- **ID**: jwt-authentication
- **Title**: JWT Authentication
- **Description**: JWT Bearer token authentication for API endpoints with role-based access control support.
- **Icon**: shield
- **Category** (`FeatureCategory`): `security`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - JWT token validation with configurable algorithm
  - AuthUserContext for request state
  - require_roles dependency for RBAC
  - Optional JWT middleware for all requests
- **Tech Stack** (optional):
  - PyJWT
  - python-jose
- **Code Snippet** (optional, `CodeSnippet`):
  - **Language**: python
  - **Filename** (optional): jwt_security.py
  - **Code**:
    ```python
    def decode_jwt_token(token: str) -> dict:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    ```
- **GitHub Example URL** (optional): ""

---

### Feature 10

- **ID**: service-registry
- **Title**: Service Registry Integration
- **Description**: Registers the notification service with a central service registry and sends periodic heartbeats for health monitoring.
- **Icon**: activity
- **Category** (`FeatureCategory`): `monitoring`
- **Status** (`FeatureStatus`): `beta`
- **Highlights**:
  - Registration on startup
  - Periodic heartbeat (configurable interval)
  - Graceful shutdown deregistration
  - Toggle via REGISTRY_ENABLED flag
- **Tech Stack** (optional):
  - httpx
- **Code Snippet** (optional, `CodeSnippet`):
  - **Language**: python
  - **Filename** (optional): register_service.py
  - **Code**:
    ```python
    async def register(self) -> None:
        async with httpx.AsyncClient() as client:
            await client.post(f"{self._registry_url}/services", json=self._service_info)
    ```
- **GitHub Example URL** (optional): ""

---

### Feature 11

- **ID**: domain-driven-design
- **Title**: Domain-Driven Design Architecture
- **Description**: Clean hexagonal architecture following DDD principles with clear separation between domain, application, infrastructure, and presentation layers.
- **Icon**: layers
- **Category** (`FeatureCategory`): `architecture`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Domain layer: Entities, Value Objects, Enums, Repository interfaces
  - Application layer: Commands, Queries, Use Cases, DTOs
  - Infrastructure layer: MongoDB, Redis, Kafka, SMTP, Twilio adapters
  - Presentation layer: Controllers, Dependencies (DI)
- **Tech Stack** (optional):
  - Clean Architecture patterns
- **Code Snippet** (optional, `CodeSnippet`):
  - **Language**: python
  - **Filename** (optional): repository.py
  - **Code**:
    ```python
    class NotificationRepository(ABC):
        @abstractmethod
        async def get_by_id(self, notification_id: str) -> Notification | None: ...
        
        @abstractmethod
        async def save(self, notification: Notification) -> Notification: ...
    ```
- **GitHub Example URL** (optional): ""

---

### Feature 12

- **ID**: event-publishing
- **Title**: Kafka Event Publishing
- **Description**: Publishes domain events to Kafka for downstream services to react to notification lifecycle changes.
- **Icon**: radio
- **Category** (`FeatureCategory`): `messaging`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - KafkaEventPublisher for outgoing events
  - NoopEventPublisher for development/testing
  - Event deduplication support
  - Configurable topics
- **Tech Stack** (optional):
  - kafka-python
- **Code Snippet** (optional, `CodeSnippet`):
  - **Language**: python
  - **Filename** (optional): kafka_publisher.py
  - **Code**:
    ```python
    class KafkaEventPublisher(EventPublisher):
        async def publish(self, event: IntegrationEvent) -> None:
            await self._producer.send_and_wait(
                self._topic, event.to_kafka_message()
            )
    ```
- **GitHub Example URL** (optional): ""

