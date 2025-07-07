# Payment Service API

A FastAPI microservice for managing cinema payments, implementing Clean Architecture with event-driven communication.

## 🏗️ Architecture Overview

### Clean Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                      │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   FastAPI REST  │  │   WebSocket     │  │   GraphQL   │ │
│  │   Endpoints     │  │   Real-time     │  │  (Future)   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   Use Cases     │  │   Commands      │  │   Queries   │ │
│  │   - PayTicket   │  │   - ProcessPay  │  │   - GetHist │ │
│  │   - BuyFood     │  │   - AddCredit   │  │   - GetWall │ │
│  │   - AddWallet   │  │   - RefundPay   │  │   - GetTrx  │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                      Domain Layer                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │    Entities     │  │  Value Objects  │  │  Domain     │ │
│  │   - Payment     │  │   - Money       │  │  Services   │ │
│  │   - Wallet      │  │   - PaymentId   │  │   - PayServ │ │
│  │   - Transaction │  │   - WalletId    │  │   - WalServ │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────┐
│                   Infrastructure Layer                     │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │   Database      │  │   Message Queue │  │  External   │ │
│  │   PostgreSQL    │  │   RabbitMQ      │  │  Gateways   │ │
│  │   - Payments    │  │   - Events      │  │  - Stripe   │ │
│  │   - Wallets     │  │   - Commands    │  │  - PayPal   │ │
│  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Microservice Communication

```
┌─────────────┐    Events     ┌─────────────┐    Events     ┌─────────────┐
│   Ticket    │◄─────────────►│   Payment   │◄─────────────►│    User     │
│   Service   │   RabbitMQ    │   Service   │   RabbitMQ    │   Service   │
└─────────────┘               └─────────────┘               └─────────────┘
       │                             │                             │
       │                             │                             │
       ▼                             ▼                             ▼
┌─────────────┐               ┌─────────────┐               ┌─────────────┐
│   Food      │               │  Billing &  │               │   Wallet    │
│   Service   │               │ Transaction │               │   Service   │
└─────────────┘               └─────────────┘               └─────────────┘
```

## 🚀 Features

- **Payment Processing**: Handle ticket and food purchases
- **Wallet Management**: Add credits and manage user balances
- **Transaction History**: Track all payment activities
- **Refund System**: Process refunds for canceled transactions
- **Event-Driven Architecture**: RabbitMQ for microservice communication
- **Multiple Payment Gateways**: Stripe, PayPal integration
- **Real-time Updates**: WebSocket support for payment status
- **Health Check**: `/health` endpoint for service monitoring
- **Auto Documentation**: Available at `/docs` (Swagger UI) and `/redoc`

## Quick Start

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the service:
```bash
python main.py
```

The service will be available at `http://localhost:8000`

### Using Docker

1. Build and run with docker-compose:
```bash
docker-compose up --build
```

The service will be available at `http://localhost:8004`

## 📋 API Endpoints

### Core Service Endpoints
- `GET /` - Service information
- `GET /health` - Health check endpoint
- `GET /ping` - Simple ping endpoint
- `GET /docs` - Swagger UI documentation
- `GET /redoc` - ReDoc documentation

### Payment Processing

#### Ticket Payments
- `POST /api/v1/payments/tickets` - Process ticket purchase payment
- `GET /api/v1/payments/tickets/{payment_id}` - Get ticket payment details
- `POST /api/v1/payments/tickets/{payment_id}/refund` - Refund ticket payment

#### Food & Merchandise Payments
- `POST /api/v1/payments/food` - Process food/merchandise purchase
- `GET /api/v1/payments/food/{payment_id}` - Get food payment details
- `POST /api/v1/payments/food/{payment_id}/refund` - Refund food payment

#### General Payment Operations
- `GET /api/v1/payments` - List payments (with filters)
- `GET /api/v1/payments/{payment_id}` - Get payment by ID
- `POST /api/v1/payments/{payment_id}/verify` - Verify payment status
- `PUT /api/v1/payments/{payment_id}/status` - Update payment status

### Wallet Management

#### Wallet Operations
- `GET /api/v1/wallet/{user_id}` - Get user wallet balance
- `POST /api/v1/wallet/{user_id}/credit` - Add credit to wallet
- `POST /api/v1/wallet/{user_id}/debit` - Debit from wallet
- `GET /api/v1/wallet/{user_id}/transactions` - Get wallet transaction history

#### Transaction History
- `GET /api/v1/transactions` - List all transactions (admin)
- `GET /api/v1/transactions/{user_id}` - Get user transaction history
- `GET /api/v1/transactions/{transaction_id}` - Get specific transaction

### Refunds
- `POST /api/v1/refunds` - Create refund request
- `GET /api/v1/refunds/{refund_id}` - Get refund status
- `PUT /api/v1/refunds/{refund_id}/approve` - Approve refund (admin)
- `PUT /api/v1/refunds/{refund_id}/reject` - Reject refund (admin)

### Payment Methods
- `GET /api/v1/payment-methods` - List available payment methods
- `POST /api/v1/payment-methods/{user_id}` - Add payment method
- `DELETE /api/v1/payment-methods/{method_id}` - Remove payment method

### WebSocket Endpoints
- `WS /ws/payments/{user_id}` - Real-time payment status updates
- `WS /ws/wallet/{user_id}` - Real-time wallet balance updates

### Example API Usage

#### Process Ticket Payment
```json
POST /api/v1/payments/tickets
{
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "ticket_ids": ["ticket_001", "ticket_002"],
  "amount": 29.98,
  "currency": "USD",
  "payment_method": "stripe",
  "payment_token": "tok_1234567890",
  "metadata": {
    "showtime_id": "show_001",
    "seats": ["A1", "A2"]
  }
}
```

#### Add Wallet Credit
```json
POST /api/v1/wallet/123e4567-e89b-12d3-a456-426614174000/credit
{
  "amount": 50.00,
  "currency": "USD",
  "payment_method": "stripe",
  "payment_token": "tok_1234567890",
  "description": "Wallet top-up"
}
```

#### Process Food Purchase
```json
POST /api/v1/payments/food
{
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "items": [
    {
      "item_id": "popcorn_large",
      "name": "Large Thematic Popcorn Container",
      "quantity": 1,
      "price": 12.99
    },
    {
      "item_id": "coffee_medium",
      "name": "Medium Coffee",
      "quantity": 2,
      "price": 4.99
    }
  ],
  "total_amount": 22.97,
  "currency": "USD",
  "payment_method": "wallet",
  "pickup_location": "Concession Stand A"
}
```

## 🗎 Event-Driven Architecture

### Published Events

The Payment Service publishes the following events to RabbitMQ:

#### Payment Events
- `payment.created` - When a new payment is initiated
- `payment.completed` - When payment processing is successful
- `payment.failed` - When payment processing fails
- `payment.refunded` - When a refund is processed
- `payment.verified` - When payment verification is complete

#### Wallet Events
- `wallet.credited` - When wallet balance is increased
- `wallet.debited` - When wallet balance is decreased
- `wallet.insufficient_funds` - When wallet has insufficient balance

#### Transaction Events
- `transaction.created` - When a new transaction is recorded
- `transaction.updated` - When transaction status changes

### Consumed Events

The Payment Service listens to these events from other services:

#### From Ticket Service
- `ticket.reserved` - To initiate ticket payment
- `ticket.cancelled` - To process refunds

#### From Food Service
- `order.created` - To process food/merchandise payments
- `order.cancelled` - To process refunds

#### From User Service
- `user.created` - To initialize user wallet
- `user.deleted` - To handle wallet cleanup

### Event Schema Examples

#### Payment Completed Event
```json
{
  "event_type": "payment.completed",
  "event_id": "evt_123e4567-e89b-12d3-a456-426614174000",
  "timestamp": "2024-01-20T10:30:00Z",
  "data": {
    "payment_id": "pay_123e4567-e89b-12d3-a456-426614174000",
    "user_id": "usr_123e4567-e89b-12d3-a456-426614174000",
    "amount": 29.98,
    "currency": "USD",
    "payment_method": "stripe",
    "transaction_id": "txn_1234567890",
    "type": "ticket_purchase",
    "metadata": {
      "ticket_ids": ["ticket_001", "ticket_002"],
      "showtime_id": "show_001"
    }
  }
}
```

#### Wallet Credited Event
```json
{
  "event_type": "wallet.credited",
  "event_id": "evt_234e5678-e89b-12d3-a456-426614174001",
  "timestamp": "2024-01-20T10:35:00Z",
  "data": {
    "wallet_id": "wal_123e4567-e89b-12d3-a456-426614174000",
    "user_id": "usr_123e4567-e89b-12d3-a456-426614174000",
    "amount": 50.00,
    "currency": "USD",
    "previous_balance": 25.50,
    "new_balance": 75.50,
    "transaction_id": "txn_1234567891",
    "description": "Wallet top-up"
  }
}
```

## 🛠️ Development Setup

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- RabbitMQ 3.12+
- Docker & Docker Compose (optional)

### Environment Configuration

Create a `.env` file:

```env
# Application
DEBUG=True
API_VERSION=1.0.0
APP_PORT=8000
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/payment_db
DATABASE_TEST_URL=postgresql://user:password@localhost:5432/payment_test_db

# Message Queue
RABBITMQ_URL=amqp://guest:guest@localhost:5672/
RABBITMQ_EXCHANGE=cinema_events

# Payment Gateways
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_CLIENT_SECRET=your-paypal-client-secret
PAYPAL_MODE=sandbox  # or live

# External Services
TICKET_SERVICE_URL=http://localhost:8001
FOOD_SERVICE_URL=http://localhost:8002
USER_SERVICE_URL=http://localhost:8003
```

### Database Migration

```bash
# Install Alembic for migrations
pip install alembic

# Initialize migrations (first time only)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial tables"

# Run migrations
alembic upgrade head
```

### Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov httpx

# Run tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_payments.py
```

## 📚 Technology Stack

### Core Technologies
- **FastAPI** - Modern Python web framework for building APIs
- **Python 3.11+** - Programming language
- **PostgreSQL** - Primary database for payment and wallet data
- **RabbitMQ** - Message broker for event-driven communication
- **SQLAlchemy** - ORM for database operations
- **Alembic** - Database migration tool
- **Pydantic** - Data validation and serialization

### Payment Integrations
- **Stripe** - Credit card processing
- **PayPal** - Alternative payment method
- **Wallet System** - Internal credit system

### Development Tools
- **pytest** - Testing framework
- **Black** - Code formatting
- **isort** - Import sorting
- **mypy** - Type checking
- **pre-commit** - Git hooks for code quality

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Redis** - Caching (optional)
- **Prometheus** - Metrics collection
- **Grafana** - Monitoring dashboards

## 🚀 Deployment

### Docker Production Setup

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  payment-service:
    build: .
    ports:
      - "8004:8000"
    environment:
      - DEBUG=False
      - DATABASE_URL=postgresql://user:pass@db:5432/payment_prod
      - RABBITMQ_URL=amqp://user:pass@rabbitmq:5672/
    depends_on:
      - db
      - rabbitmq
    restart: unless-stopped

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: payment_prod
      POSTGRES_USER: user
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  rabbitmq:
    image: rabbitmq:3.12-management
    environment:
      RABBITMQ_DEFAULT_USER: user
      RABBITMQ_DEFAULT_PASS: secure_password
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    restart: unless-stopped

volumes:
  postgres_data:
  rabbitmq_data:
```

### Kubernetes Deployment

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: payment-service
  template:
    metadata:
      labels:
        app: payment-service
    spec:
      containers:
      - name: payment-service
        image: cinema-api/payment-service:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: payment-secrets
              key: database-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

### CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy Payment Service

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          docker build -t payment-service .
          docker push ${{ secrets.REGISTRY_URL }}/payment-service:latest
```

## 🛡️ Security

### Authentication & Authorization
- JWT token-based authentication
- Role-based access control (RBAC)
- API key authentication for service-to-service calls

### Payment Security
- PCI DSS compliance considerations
- No storage of sensitive payment data
- Payment tokenization through gateways
- HTTPS enforcement
- Request rate limiting

### Data Protection
- Encryption at rest and in transit
- Audit logging for all transactions
- Input validation and sanitization
- SQL injection prevention

## 📊 Monitoring & Observability

### Metrics
- Payment success/failure rates
- Transaction volumes
- API response times
- Database connection pool status
- RabbitMQ queue lengths

### Logging
- Structured JSON logging
- Correlation IDs for tracing
- Payment audit trails
- Error tracking and alerting

### Health Checks
- `/health` - Overall service health
- `/health/db` - Database connectivity
- `/health/queue` - Message queue status
- `/health/payment-gateways` - External service status

## Testing the Service

```bash
# Health check
curl http://localhost:8000/health

# Ping
curl http://localhost:8000/ping

# Service info
curl http://localhost:8000/

# Test payment endpoint
curl -X POST http://localhost:8000/api/v1/payments/tickets \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "ticket_ids": ["ticket_001"],
    "amount": 15.99,
    "currency": "USD",
    "payment_method": "stripe",
    "payment_token": "tok_test_1234567890"
  }'
```

## 📝 License

This project is part of the Cinema API microservices architecture.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow Clean Architecture principles
- Write comprehensive tests
- Use type hints throughout the codebase
- Follow PEP 8 style guidelines
- Document API changes in the README
- Ensure all tests pass before submitting PR

## 📞 Support

For questions or support regarding the Payment Service:

- Check the [API Documentation](http://localhost:8000/docs)
- Review the [Architecture Documentation](#architecture-overview)
- Create an issue in the repository
- Contact the development team
