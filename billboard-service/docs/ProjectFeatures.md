# Project Features

## Feature List (`ProjectFeature[]`)

### Feature 1: Showtime Management

- **ID**: "showtime-management"
- **Title**: Showtime Management
- **Description**: Complete CRUD operations for showtimes with lifecycle management (draft, upcoming, completed, cancelled).
- **Icon**: "📅"
- **Category** (`FeatureCategory`): `api`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Full showtime CRUD operations
  - Draft → Launch workflow
  - Cancel and restore functionality
  - Soft delete support
  - Search and filtering
- **Tech Stack** (optional):
  - FastAPI
  - SQLAlchemy (async)
  - PostgreSQL

---

### Feature 2: Business Rule Validation

- **ID**: "business-rules"
- **Title**: Business Rule Validation
- **Description**: Domain entity enforces pricing limits, duration constraints, and scheduling rules.
- **Icon**: "📋"
- **Category** (`FeatureCategory`): `api`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Price validation ($3.00 - $50.00)
  - Duration validation (30 - 300 minutes)
  - Schedule not in past
  - Schedule within 30-day booking window
  - Seat quantity limits (1-15 per transaction)

---

### Feature 3: Seat Reservation

- **ID**: "seat-reservation"
- **Title**: Seat Reservation
- **Description**: Real-time seat status tracking with take/leave operations and transaction tracking.
- **Icon**: "💺"
- **Category** (`FeatureCategory`): `api`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Take seat with timestamp
  - Leave seat to release
  - Transaction ID tracking
  - User ID association
  - Available seat calculation

---

### Feature 4: Buffer Time Management

- **ID**: "buffer-times"
- **Title**: Buffer Time Management
- **Description**: Automatic pre-show and post-show buffer time calculation.
- **Icon**: "⏱️"
- **Category** (`FeatureCategory`): `api`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Pre-show buffer: 10min cleaning + 40min commercials = 50min
  - Post-show buffer: 30min cleaning
  - Optional post-credits scene support

---

### Feature 5: Search & Filtering

- **ID**: "search-filtering"
- **Title**: Search & Filtering
- **Description**: Advanced search and filtering capabilities for showtimes.
- **Icon**: "🔍"
- **Category** (`FeatureCategory`): `api`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Filter by status (draft, upcoming, completed, cancelled)
  - Filter by movie ID
  - Filter by theater ID
  - Filter by date range
  - Pagination support

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

---

### Feature 7: Redis Caching

- **ID**: "caching"
- **Title**: Redis Caching
- **Description**: Redis caching support for frequently accessed showtime data.
- **Icon**: "⚡"
- **Category** (`FeatureCategory`): `caching`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Cache active showtimes
  - Cache seat availability
  - Configurable TTL

---

### Feature 8: gRPC Catalog Integration

- **ID**: "grpc-catalog"
- **Title**: gRPC Catalog Integration
- **Description**: gRPC client for fetching movie and theater data from catalog service.
- **Icon**: "🔗"
- **Category** (`FeatureCategory`): `integration`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Validate movie exists
  - Validate theater exists
  - Fetch theater capacity

---

### Feature 9: Rate Limiting

- **ID**: "rate-limiting"
- **Title**: Rate Limiting
- **Description**: API rate limiting for abuse protection.
- **Icon**: "🚦"
- **Category** (`FeatureCategory`): `security`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Per-endpoint rate limits (60/min read, 10/min write)
  - SlowAPI integration

---

### Feature 10: Service Registry

- **ID**: "service-registry"
- **Title**: Service Registry
- **Description**: Optional service registry for dynamic discovery and health checks.
- **Icon**: "🔔"
- **Category** (`FeatureCategory`): `monitoring`
- **Status** (`FeatureStatus`): `experimental`
- **Highlights**:
  - Dynamic service registration
  - Health check endpoints
  - Heartbeat mechanism

---

### Feature 11: Kafka Integration

- **ID**: "kafka-integration"
- **Title**: Kafka Event Publishing
- **Description**: Publish showtime events to Kafka for inter-service communication.
- **Icon**: "📤"
- **Category** (`FeatureCategory`): `messaging`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Showtime events (created, launched, cancelled)
  - Configurable topic
  - Optional (can be disabled)

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
  - Soft-delete support
