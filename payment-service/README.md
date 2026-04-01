# 🎬 Cinema Plattform - Payment Service (Microservice)

> Enterprise-grade payment processing service for cinema platform with support for tickets, concessions, merchandise, subscriptions, and wallet management

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.1+-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-red.svg)](https://redis.io/)
[![Kafka](https://img.shields.io/badge/Kafka-Ready-blue.svg)](https://kafka.apache.org/)
[![gRPC](https://img.shields.io/badge/gRPC-Ready-blue.svg)](https://grpc.io/)
[![Stripe](https://img.shields.io/badge/Stripe-Ready-blue.svg)](https://stripe.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Overview

**Cinema Payment Service** is a comprehensive payment processing microservice for managing cinema platform transactions including ticket purchases, food/concessions, merchandise, subscriptions, and wallet credits. Built with modern async Python architecture, Clean Architecture principles, and event-driven communication via Kafka.

### 🎯 Key Features

- **💳 Payment Processing** - Support for tickets, concessions, merchandise, subscriptions, and wallet top-ups
- **💰 Refund Management** - Full and partial refunds with 30-day window enforcement
- **🔐 Stored Payment Methods** - Secure card storage with Stripe tokenization (PCI compliant)
- **📜 Transaction History** - Complete audit trail with pagination and filtering
- **👥 Role-Based Access Control** - Customer, staff, and admin endpoints with JWT authentication
- **📤 Event Publishing** - Kafka-based domain events for inter-service communication
- **🔗 gRPC Integration** - Cross-service business assertions with ticket/food services
- **⚡ Caching** - Redis caching support for frequently accessed data
- **🚦 Rate Limiting** - API rate limiting for abuse protection
- **🐳 Docker Ready** - Containerized deployment with health checks

---

## 🏗️ Architecture

Built following **Clean Architecture** principles with strict separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                         │
│  Controllers • JWT Middleware • Rate Limiting • CORS       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                          │
│      Use Cases • Commands • DTOs • Event Handlers            │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      Domain Layer                             │
│   Entities • Value Objects • Enums • Domain Events          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                 Infrastructure Layer                         │
│  SQLAlchemy • Kafka • Stripe • gRPC • PostgreSQL           │
└─────────────────────────────────────────────────────────────┘
```

### Core Domains

- **Payments** - Payment processing, status management, refund handling
- **Payment Methods** - Catalog management for checkout options
- **Stored Payment Methods** - User-saved cards with Stripe tokenization
- **Transactions** - Wallet transaction audit trail
- **Events** - Domain event publishing (Kafka)
- **Shared** - Cross-cutting concerns (pagination, exceptions, auth)

---

## 🚀 Tech Stack

| Category             | Technology                    |
| -------------------- | ----------------------------- |
| **Framework**        | FastAPI (Async REST API)      |
| **Language**         | Python 3.11+                  |
| **Database**         | PostgreSQL 15 (Alpine)        |
| **ORM**              | SQLAlchemy 2.0+ (Async)       |
| **Cache**            | Redis 7 (Optional)            |
| **Migrations**       | Alembic                       |
| **Authentication**   | JWT (PyJWT)                   |
| **Validation**       | Pydantic v2                   |
| **Rate Limiting**    | SlowAPI                       |
| **Event Streaming**  | Apache Kafka                  |
| **RPC**              | gRPC + Protocol Buffers       |
| **Payment Gateway**  | Stripe SDK                    |
| **Server**           | Uvicorn                       |
| **Containerization** | Docker + Docker Compose       |
| **Testing**          | pytest + pytest-asyncio        |

---

## 🎯 Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- PostgreSQL 15 (if running locally)
- Redis 7 (if running locally)

### 🐳 Docker Setup (Recommended)

1. **Clone the repository**

   ```bash
   git clone https://github.com/anomalyco/cinema-platform.git
   cd cinema-platform/payment-service
   ```

2. **Configure environment variables**

   ```bash
   cp .env docker/.env
   # Edit docker/.env with your configuration
   ```

3. **Start all services**

   ```bash
   docker compose -f docker/docker-compose.yml up --build -d
   ```

4. **Access the API**
   - API: http://localhost:8000
   - Swagger Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### 💻 Local Development Setup

1. **Create virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**

   ```bash
   export POSTGRES_HOST=localhost
   export POSTGRES_PORT=5432
   export POSTGRES_DB=cinema_payments
   export POSTGRES_USER=postgres
   export POSTGRES_PASSWORD=fedoraadmin
   export REDIS_URL=redis://localhost:6379
   export JWT_SECRET_KEY=your-secret-key
   export JWT_ALGORITHM=HS256
   ```

4. **Run database migrations**

   ```bash
   alembic upgrade head
   ```

5. **Start the application**

   ```bash
   python main.py
   ```

---

## 📚 API Documentation

Once the service is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Core Endpoints

#### Customer Endpoints

```bash
# Purchase tickets
POST /api/v1/payments/customers/tickets
{
  "show_id": "uuid",
  "showtime_id": "uuid",
  "seats": ["A1", "A2"],
  "total_amount": 29.99,
  "currency": "USD",
  "payment_method": "stripe"
}

# Purchase concessions
POST /api/v1/payments/customers/consessions
{
  "order_id": "uuid",
  "items": [{"item_id": "popcorn", "quantity": 1, "price": 12.99}],
  "total_amount": 22.99,
  "currency": "USD",
  "payment_method": "wallet"
}

# Get payment history
GET /api/v1/payments/customers/history?limit=20&offset=0
Authorization: Bearer <jwt_token>

# Request refund
POST /api/v1/payments/customers/payments/{payment_id}/refund
{
  "reason": "Customer refund request",
  "refund_amount": 15.00
}
```

#### Staff Endpoints

```bash
# Verify payment status
GET /api/v1/payments/staff/{payment_id}/status
Authorization: Bearer <jwt_token>

# Refund for cancelled show
POST /api/v1/payments/staff/{payment_id}/refund
{
  "reason": "Show cancelled by theater"
}

# Get show revenue summary
GET /api/v1/payments/staff/show/{show_id}/summary
```

#### Admin Endpoints

```bash
# Search payments
GET /api/v1/payments/admin/payments?user_id=uuid&status=completed
Authorization: Bearer <jwt_token>

# Override payment status
PATCH /api/v1/payments/admin/payments/{payment_id}/status
{
  "status": "completed"
}

# Get payments summary
GET /api/v1/payments/admin/summary

# Get summary by type
GET /api/v1/payments/admin/summary/by-type

# Get summary by payment method
GET /api/v1/payments/admin/summary/by-method
```

#### Payment Method Catalog

```bash
# List payment methods
GET /api/v2/payment/methods/

# Create payment method (admin)
POST /api/v2/payment/methods/
{
  "name": "Credit or debit card",
  "provider": "stripe",
  "type": "card",
  "stripe_code": "card",
  "is_active": true,
  "min_amount": 0.0
}

# Update payment method (admin)
PUT /api/v2/payment/methods/{payment_method_id}
{
  "is_active": false
}
```

### Authentication

Protected endpoints require a JWT Bearer token:

```bash
curl -H "Authorization: Bearer <your_jwt_token>" \
     http://localhost:8000/api/v1/payments/customers/history
```

**Roles:**
- `customer` - Access to customer endpoints
- `employee`, `manager`, `admin` - Access to staff endpoints
- `admin`, `superadmin` - Access to admin endpoints

---

## 📁 Project Structure

```
payment-service/
├── main.py                    # FastAPI application entry point
├── requirements.txt           # Python dependencies
├── alembic.ini               # Alembic configuration
├── .env                      # Environment variables
│
├── app/
│   ├── config/              # Application configuration
│   │   ├── app_config.py    # Pydantic settings
│   │   ├── postgres_config.py
│   │   ├── cache_config.py
│   │   ├── kafka_config.py
│   │   ├── rate_limit.py
│   │   └── logging.py
│   │
│   ├── payments/            # Payments domain
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   │   ├── payment.py
│   │   │   │   ├── payment_method.py
│   │   │   │   ├── stored_payment_method.py
│   │   │   │   └── transaction.py
│   │   │   ├── value_objects.py
│   │   │   ├── events.py
│   │   │   ├── exceptions.py
│   │   │   ├── interfaces.py
│   │   │   └── aggregate_root.py
│   │   │
│   │   ├── application/
│   │   │   ├── commands.py
│   │   │   ├── usecases/
│   │   │   │   ├── admin_usecases.py
│   │   │   │   ├── customer_usecases.py
│   │   │   │   ├── staff_usecases.py
│   │   │   │   └── payment_method_usecases.py
│   │   │   └── services/
│   │   │       ├── payment_application_service.py
│   │   │       └── payment_incoming_events_handler.py
│   │   │
│   │   ├── infrastructure/
│   │   │   ├── persistence/
│   │   │   │   ├── models.py
│   │   │   │   ├── sql_alchemy_repository.py
│   │   │   │   └── model_mapper.py
│   │   │   ├── messaging/
│   │   │   │   └── kafka_payment_events.py
│   │   │   └── grpc/
│   │   │       └── purchase_assertion_grpc_client.py
│   │   │
│   │   └── presentation/
│   │       ├── controllers/
│   │       │   ├── admin_payment_controller.py
│   │       │   ├── customer_payment_controller.py
│   │       │   ├── staff_payment_controller.py
│   │       │   └── payment_methods_controllers.py
│   │       ├── depencies.py
│   │       └── dtos.py
│   │
│   ├── shared/              # Shared utilities
│   │   ├── auth.py
│   │   ├── base_exceptions.py
│   │   ├── documentation.py
│   │   ├── events/
│   │   │   ├── base.py
│   │   │   └── infrastructure/
│   │   │       ├── kafka_publisher.py
│   │   │       └── noop_publisher.py
│   │   ├── middleware/
│   │   │   ├── jwt_security.py
│   │   │   └── logging_middleware.py
│   │   └── core/
│   │       ├── jwt_security.py
│   │       ├── pagination.py
│   │       └── response.py
│   │
│   └── grpc/                # gRPC server
│       └── server.py
│
├── alembic/                 # Database migrations
│   └── versions/           # Migration scripts
│
├── docker/                  # Docker configuration
│   └── docker-compose.yml
│
├── docs/                    # Documentation
│   ├── ProjectOverview.md
│   ├── ProjectFeatures.md
│   ├── ProjectArchitectureModel.md
│   ├── InfrastructureModel.md
│   ├── APISchema.md
│   ├── ProjectMetric.md
│   ├── ProjectCodeShowCase.md
│   ├── ProjectLinks.md
│   └── MediaGallerySection.md
│
└── agents/                  # Agent documentation
    ├── AGENTS.md
    └── CONVENTIONS.md
```

---

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest app/tests/payments/

# Run with verbose output
pytest -v

# Run unit tests only
pytest app/tests/unit/
```

---

## 🔧 Development

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Add payment metadata"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

### Code Quality

```bash
# Format code
black app/ tests/

# Lint code
ruff check app/ tests/

# Type checking
mypy app/
```

### Generate gRPC Code

```bash
# Generate Python code from .proto files
python -m grpc_tools.protoc \
    -I. \
    --python_out=. \
    --grpc_python_out=. \
    payment.proto
```

---

## 🚢 Deployment

### Docker Deployment

The service includes production-ready Docker configuration:

- **Health checks** for all services
- **Async SQLAlchemy** for high concurrency
- **Kafka integration** for domain events (optional)
- **gRPC support** for cross-service communication
- **Stripe integration** for payment processing

```bash
# Build production image
docker build -f docker/Dockerfile -t payment-service:latest .

# Run production stack
docker compose -f docker/docker-compose.yml up -d
```

### Environment Variables

Required environment variables for production:

```bash
# Database
POSTGRES_HOST=your-db-host
POSTGRES_PORT=5432
POSTGRES_DB=cinema_payments
POSTGRES_USER=payment_service
POSTGRES_PASSWORD=<secure-password>

# Redis
REDIS_URL=redis://your-redis-host:6379

# Security
JWT_SECRET_KEY=<long-random-secret>
JWT_ALGORITHM=HS256
JWT_AUDIENCE=<optional-audience>
JWT_ISSUER=<optional-issuer>

# Application
DEBUG_MODE=false
API_HOST=0.0.0.0
API_PORT=8000

# Kafka (optional)
KAFKA_ENABLED=true
KAFKA_BOOTSTRAP_SERVERS=kafka1:9092,kafka2:9092
KAFKA_TOPIC_PAYMENT_EVENTS=payment.events

# gRPC
GRPC_HOST=0.0.0.0
GRPC_PORT=50055
GRPC_BILLBOARD_TARGET=billboard-service:50051
```

---

## 📊 Performance Metrics

- **Response Time**: <200ms (p95) for API requests
- **Payment Success Rate**: 99.5%+
- **Transaction Throughput**: 1,000 TPS peak
- **Refund Processing Time**: <24 hours
- **Kafka Message Latency**: <50ms
- **Service Uptime**: 99.9%

---

## 📖 Documentation

Comprehensive documentation available in the `/docs` folder:

- **[Project Overview](docs/ProjectOverview.md)** - Problem statement, solutions, key metrics
- **[Features](docs/ProjectFeatures.md)** - Detailed feature descriptions with code examples
- **[Architecture](docs/ProjectArchitectureModel.md)** - Clean Architecture layers, patterns, strategies
- **[Infrastructure](docs/InfrastructureModel.md)** - Docker setup, Kubernetes, cloud services
- **[API Schema](docs/APISchema.md)** - Complete API endpoint documentation
- **[Code Showcase](docs/ProjectCodeShowCase.md)** - Code examples showcasing best practices
- **[Metrics](docs/ProjectMetric.md)** - Performance and business metrics
- **[Media Gallery](docs/MediaGallerySection.md)** - Screenshots and diagrams

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Follow the architecture conventions in `agents/CONVENTIONS.md`
4. Write tests for new features
5. Ensure all tests pass (`pytest`)
6. Commit your changes (`git commit -m 'Add payment feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Alexis** - _Initial work_

---

## 🙏 Acknowledgments

- FastAPI for the excellent async framework
- SQLAlchemy for the powerful ORM
- PostgreSQL for the robust database
- Redis for the blazing-fast cache
- Apache Kafka for event streaming
- gRPC for efficient inter-service communication
- Stripe for payment processing
- The Python community for amazing tools and libraries

---

## 📞 Contact & Links

- **GitHub**: [https://github.com/anomalyco/cinema-plattform](https://github.com/anomalyco/cinema-plattform)
- **Payment Service**: [payment-service/](payment-service/)
- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/anomalyco/cinema-plattform/issues)

---

<div align="center">

**Built with ❤️ using Python, FastAPI, PostgreSQL, Kafka, Stripe, and Clean Architecture**

⭐ Star this repo if you find it helpful!

</div>
