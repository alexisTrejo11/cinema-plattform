# Project Features

## Feature List (`ProjectFeature[]`)

### Feature 1: Payment Processing

- **ID**: "payment-processing"
- **Title**: Payment Processing
- **Description**: Core payment processing for tickets, concessions, merchandise, subscriptions, and wallet top-ups with support for multiple payment methods.
- **Icon**: "💳"
- **Category** (`FeatureCategory`): `api`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Support for credit card, debit card, PayPal, Stripe, and wallet payments
  - Payment intent creation and confirmation flow
  - Automatic status transitions (pending → processing → completed/failed)
  - Stripe Payment Intent integration
- **Tech Stack** (optional):
  - FastAPI
  - SQLAlchemy (async)
  - Stripe SDK
  - Kafka
- **Metrics** (optional, `FeatureMetric[]`):
  - **Label**: "Success Rate"
  - **Value**: "99.5%"
  - **Trend** (optional): `up`
  - **Icon** (optional): "✓"
- **Code Snippet** (optional, `CodeSnippet`):
  - **Language**: "python"
  - **Filename** (optional): "payment.py"
  - **Code**:
    ```python
    class Payment(AggregateRoot):
        def complete(self, transaction_reference: Optional[str] = None) -> None:
            if not self.can_be_completed():
                raise PaymentAlreadyProcessedException(str(self.id), self.status.value)
            self.status = PaymentStatus.COMPLETED
            self.completed_at = datetime.now(timezone.utc)
    ```

---

### Feature 2: Refund Management

- **ID**: "refund-management"
- **Title**: Refund Management
- **Description**: Full and partial refund processing with business rule validation (30-day window, show start time checks).
- **Icon**: "↩️"
- **Category** (`FeatureCategory`): `api`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Full and partial refunds
  - 30-day refund window enforcement
  - No refunds after show starts (for ticket purchases)
  - Refund reason tracking
- **Tech Stack** (optional):
  - Python
  - Stripe Refund API
- **Metrics** (optional, `FeatureMetric[]`):
  - **Label**: "Avg Processing Time"
  - **Value**: "< 24 hours"
  - **Trend** (optional): `stable`

---

### Feature 3: Stored Payment Methods

- **ID**: "stored-payment-methods"
- **Title**: Stored Payment Methods
- **Description**: Save and manage customer payment methods (cards) with tokenization via Stripe.
- **Icon**: "🔐"
- **Category** (`FeatureCategory`): `api`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Secure card storage with Stripe tokenization
  - Default payment method selection
  - Soft-delete support
  - PCI compliance (no raw card data stored)
- **Tech Stack** (optional):
  - Stripe PaymentMethod API
  - StoredPaymentMethod entity

---

### Feature 4: Transaction History

- **ID**: "transaction-history"
- **Title**: Transaction History
- **Description**: Complete audit trail of all payment transactions with pagination and filtering.
- **Icon**: "📜"
- **Category** (`FeatureCategory`): `api`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Paginated transaction listing
  - Filter by user, status, date range
  - Balance snapshots (before/after)
  - Receipt generation
- **Tech Stack** (optional):
  - SQLAlchemy
  - PostgreSQL

---

### Feature 5: Event Publishing (Kafka)

- **ID**: "event-publishing"
- **Title**: Event Publishing (Kafka)
- **Description**: Publishes payment events to Kafka for inter-service communication.
- **Icon**: "📤"
- **Category** (`FeatureCategory`): `messaging`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Events: payment.created, payment.completed, payment.failed, payment.refunded
  - Wallet events: wallet.credited, wallet.debited
  - Transaction events: transaction.recorded, transaction.reversed
  - Payment method events: payment_method.added, payment_method.removed
- **Tech Stack** (optional):
  - kafka-python
  - KafkaProducer
- **Code Snippet** (optional, `CodeSnippet`):
  - **Language**: "python"
  - **Filename** (optional): "kafka_payment_events.py"
  - **Code**:
    ```python
    class KafkaPaymentEventsPublisher(PaymentEventsPublisher):
        async def publish(self, event_name, payload, key=None):
            message = {"event_type": event_name, "payload": payload}
            self._producer.send(topic=self._topic, key=key, value=message)
    ```

---

### Feature 6: gRPC Integration

- **ID**: "grpc-integration"
- **Title**: gRPC Integration
- **Description**: Cross-service business assertions via gRPC (placeholder for ticket/concessions verification).
- **Icon**: "🔗"
- **Category** (`FeatureCategory`): `integration`
- **Status** (`FeatureStatus`): `beta`
- **Highlights**:
  - PurchaseAssertionClient interface
  - gRPC targets configuration
  - Graceful fallback to no-op
- **Tech Stack** (optional):
  - grpcio
  - protobuf

---

### Feature 7: Role-Based Access Control

- **ID**: "rbac"
- **Title**: Role-Based Access Control
- **Description**: JWT authentication with role enforcement for customer, staff, and admin operations.
- **Icon**: "🔒"
- **Category** (`FeatureCategory`): `security`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Customer endpoints for self-service
  - Staff endpoints for operations
  - Admin endpoints for management
  - JWT token validation
- **Tech Stack** (optional):
  - PyJWT
  - FastAPI security

---

### Feature 8: Payment Method Catalog

- **ID**: "payment-method-catalog"
- **Title**: Payment Method Catalog
- **Description**: Admin-managed catalog of available payment methods with soft-delete and restore functionality.
- **Icon**: "📋"
- **Category** (`FeatureCategory`): `api`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - CRUD operations for payment methods
  - Stripe code mapping
  - Minimum amount configuration
  - Soft-delete and restore
- **Tech Stack** (optional):
  - PaymentMethod entity
  - PaymentMethodRepository

---

### Feature 9: Database Persistence

- **ID**: "database-persistence"
- **Title**: Database Persistence
- **Description**: PostgreSQL persistence with SQLAlchemy ORM and Alembic migrations.
- **Icon**: "🗄️"
- **Category** (`FeatureCategory`): `database`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Async SQLAlchemy with asyncpg
  - Alembic migrations
  - Model-to-entity mapping
  - Soft-delete support
- **Tech Stack** (optional):
  - SQLAlchemy (async)
  - PostgreSQL
  - Alembic

---

### Feature 10: Caching

- **ID**: "caching"
- **Title**: Caching
- **Description**: Redis caching support via fastapi-cache.
- **Icon**: "⚡"
- **Category** (`FeatureCategory`): `caching`
- **Status** (`FeatureStatus`): `experimental`
- **Highlights**:
  - Redis integration via REDIS_URL config
  - Optional caching layer
- **Tech Stack** (optional):
  - fastapi-cache[redis]
  - Redis

---

### Feature 11: Rate Limiting

- **ID**: "rate-limiting"
- **Title**: Rate Limiting
- **Description**: API rate limiting via SlowAPI.
- **Icon**: "🚦"
- **Category** (`FeatureCategory`): `security`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Per-endpoint rate limits
  - Configurable limits
- **Tech Stack** (optional):
  - slowapi
