# 🎬 Cinema Platform - Microservices Ecosystem

> Enterprise-grade cinema management platform built with microservices architecture, featuring modern Python async frameworks, event-driven communication, and domain-driven design

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.1+-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)](https://www.postgresql.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Ready-green.svg)](https://www.mongodb.com/)
[![Redis](https://img.shields.io/badge/Redis-7-red.svg)](https://redis.io/)
[![Kafka](https://img.shields.io/badge/Kafka-Ready-blue.svg)](https://kafka.apache.org/)
[![RabbitMQ](https://img.shields.io/badge/RabbitMQ-Ready-orange.svg)](https://www.rabbitmq.com/)
[![gRPC](https://img.shields.io/badge/gRPC-Ready-blue.svg)](https://grpc.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Overview

**Cinema Platform** is a comprehensive microservices ecosystem for managing all aspects of cinema operations. Built with modern Python async architecture, Clean Architecture principles, and event-driven communication patterns.

The platform consists of independently deployable services that communicate via REST APIs, gRPC, and message brokers (Kafka/RabbitMQ). Each service follows Domain-Driven Design (DDD) principles with clear separation of concerns.

### 🎯 Key Principles

- **Microservices Architecture** - Independently deployable, scalable services
- **Domain-Driven Design** - Clean separation of domain logic from infrastructure
- **Event-Driven Communication** - Asynchronous messaging via Kafka and RabbitMQ
- **Dual Protocol Support** - REST for clients, gRPC for inter-service communication
- **Async First** - Full async/await for high concurrency and performance
- **Infrastructure as Code** - Docker Compose for local development and deployment

---

## 🏗️ Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                              API Gateway / Load Balancer                       │
│                           (nginx, Cloudflare, etc.)                          │
└──────────────────────────────────────────────────────────────────────────────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          │                           │                           │
          ▼                           ▼                           ▼
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│   Client Apps   │      │  External APIs  │      │  Admin Portal   │
│  (Web, Mobile)  │      │   (Partners)    │      │   (Internal)    │
└─────────────────┘      └─────────────────┘      └─────────────────┘
                                      │
                                      ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                           Service Communication Layer                         │
│                                                                                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │    REST     │  │    gRPC     │  │    Kafka    │  │  RabbitMQ   │         │
│  │  (External) │  │ (Internal)  │  │  (Events)   │  │  (Events)   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘         │
└──────────────────────────────────────────────────────────────────────────────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          │                           │                           │
          ▼                           ▼                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Core Services                                    │
│                                                                              │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐          │
│  │   User     │  │   Wallet   │  │    Order   │  │ Notification│          │
│  │  Service   │  │  Service   │  │  Service   │  │   Service   │          │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘          │
│                                                                              │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐          │
│  │  Catalog   │  │  Billboard │  │ Concession │  │  Employee  │          │
│  │  Service   │  │  Service   │  │  Service   │  │  Service   │          │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘          │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          │                           │                           │
          ▼                           ▼                           ▼
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│   PostgreSQL    │      │    MongoDB      │      │     Redis       │
│  (User, Order)  │      │  (Notification) │      │    (Cache)      │
└─────────────────┘      └─────────────────┘      └─────────────────┘
```

---

## 📦 Services

| Service | Description | Port | Database | Protocols |
|---------|-------------|------|----------|-----------|
| **[user-service](user-service/)** | User authentication, profiles, sessions, 2FA | 8000 | PostgreSQL | REST, gRPC |
| **[wallet-service](wallet-service/)** | Digital wallet, transactions, multi-currency | 8001 | PostgreSQL | REST |
| **[catalog-service](catalog-service/)** | Movies, cinemas, theaters, seats | 8002 | PostgreSQL | REST, gRPC |
| **[billboard-service](billboard-service/)** | Showtimes, seat reservations | 8003 | PostgreSQL | REST, gRPC |
| **[concession-service](concession-service/)** | Products, combos, promotions | 8004 | PostgreSQL | REST, gRPC |
| **[notification-service](notification-service/)** | Email, SMS, push notifications | 8005 | MongoDB | REST |
| **[employee-service](employee-service/)** | Employee management | 8006 | PostgreSQL | REST |
| **admin-service** | Spring Boot Admin dashboard | 8080 | - | HTTP |
| **kafka-infra** | Centralized Kafka cluster | - | - | Kafka |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+ / 3.13+
- Docker & Docker Compose
- PostgreSQL 15+ (if running locally)
- Redis 7
- MongoDB 6+ (for notification-service)
- Kafka 3+ (or kafka-infra)

### 🐳 Docker Setup (Recommended)

1. **Clone the repository**

   ```bash
   git clone https://github.com/anomalyco/cinema-plattform.git
   cd cinema-plattform
   ```

2. **Start Kafka Infrastructure**

   ```bash
   cd kafka-infra
   docker compose up -d
   cd ..
   ```

3. **Start Core Services**

   ```bash
   cd user-service && docker compose up -d
   cd ../wallet-service && docker compose up -d
   cd ../catalog-service && docker compose up -d
   # Continue for other services...
   ```

4. **Access Service APIs**

   - User Service: http://localhost:8000/docs
   - Wallet Service: http://localhost:8001/docs
   - Catalog Service: http://localhost:8002/docs
   - Billboard Service: http://localhost:8003/docs
   - Concession Service: http://localhost:8004/docs
   - Notification Service: http://localhost:8005/docs
   - Admin Dashboard: http://localhost:8080

### 💻 Local Development Setup

1. **Create virtual environment per service**

   ```bash
   cd <service-name>
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run database migrations**

   ```bash
   alembic upgrade head
   ```

4. **Start the service**

   ```bash
   uvicorn main:app --reload
   # Or with Gunicorn for production:
   gunicorn main:app --worker-class uvicorn.workers.UvicornWorker
   ```

---

## 🛠️ Tech Stack

### Core Technologies

| Category | Technology | Usage |
|----------|------------|-------|
| **Framework** | FastAPI | Async REST API framework |
| **Language** | Python 3.11+ / 3.13 | Primary development language |
| **ORM** | SQLAlchemy 2.0+ (Async) | Database access |
| **Validation** | Pydantic v2 | Data validation and serialization |
| **Server** | Uvicorn / Gunicorn | ASGI server |

### Databases

| Database | Service | Usage |
|----------|---------|-------|
| **PostgreSQL 16** | user, wallet, catalog, billboard, concession, employee | Primary data storage |
| **MongoDB** | notification-service | Document storage for notifications |
| **Redis 7** | All services | Caching, sessions, rate limiting |

### Message Brokers

| Broker | Usage |
|--------|-------|
| **Apache Kafka** | Event streaming, domain events |
| **RabbitMQ** | wallet-service message queue |

### Communication Protocols

| Protocol | Usage |
|----------|-------|
| **REST** | Client-facing APIs |
| **gRPC** | Inter-service communication |
| **Kafka** | Event publishing/consuming |
| **RabbitMQ** | Async messaging |

### Infrastructure

| Category | Technology |
|----------|------------|
| **Containerization** | Docker, Docker Compose |
| **Migrations** | Alembic |
| **Authentication** | JWT (PyJWT) |
| **Rate Limiting** | SlowAPI |
| **Monitoring** | Spring Boot Admin |

---

## 🏛️ Architecture Patterns

### Domain-Driven Design (DDD)

Each service follows DDD principles with clear layer separation:

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                         │
│              Controllers • Middleware • DTOs                  │
└─────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                          │
│         Use Cases • Commands/Queries • DTOs • Mappers       │
└─────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────┐
│                      Domain Layer                            │
│     Entities • Value Objects • Enums • Repository Interfaces  │
└─────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────┐
│                 Infrastructure Layer                          │
│      SQLAlchemy • Redis • Kafka • SMTP • gRPC Clients       │
└─────────────────────────────────────────────────────────────┘
```

### Event-Driven Architecture

Services communicate asynchronously via events:

```
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│ User Service │      │  Kafka      │      │Notification  │
│  (Publishes) │ ───► │  Broker     │ ───► │  Service     │
└──────────────┘      └──────────────┘      └──────────────┘
       │                                              │
       │                                              ▼
       │                                     ┌──────────────┐
       │                                     │   Email/SMS  │
       └────────────────────────────────────►│   Gateway    │
                                             └──────────────┘
```

### Hexagonal Architecture (Ports & Adapters)

Domain logic is isolated from external dependencies through port interfaces:

- **Driving Ports**: REST controllers, gRPC servicers
- **Driven Ports**: Repository interfaces, external service interfaces
- **Adapters**: Database implementations, HTTP clients, message publishers

---

## 📊 Service Details

### User Service

**Purpose**: Central authentication and user management

**Features**:
- User registration and login with JWT
- Session management (Redis-backed)
- Two-Factor Authentication (TOTP)
- Profile management
- Role-based access control (ADMIN, CUSTOMER, EMPLOYEE, MANAGER)
- Domain event publishing (Kafka)

**Tech Stack**: FastAPI, PostgreSQL, Redis, Kafka, gRPC

---

### Wallet Service

**Purpose**: Digital wallet and transaction management

**Features**:
- Multi-currency support (USD, EUR, MXN)
- Add credit and payment processing
- Transaction history
- RabbitMQ event integration

**Tech Stack**: FastAPI, PostgreSQL, RabbitMQ

---

### Catalog Service

**Purpose**: Cinema catalog management

**Features**:
- Movie catalog with showtimes
- Cinema and theater management
- Seat configuration
- Advanced search and filtering
- gRPC catalog gateway

**Tech Stack**: FastAPI, PostgreSQL, Redis, Kafka, gRPC

---

### Billboard Service

**Purpose**: Showtime scheduling and seat reservations

**Features**:
- Showtime lifecycle (draft → upcoming → active)
- Real-time seat reservation
- Business rule validation (pricing, duration, buffers)
- gRPC integration with catalog service

**Tech Stack**: FastAPI, PostgreSQL, Redis, Kafka, gRPC

---

### Concession Service

**Purpose**: Food and beverage product management

**Features**:
- Product catalog (snacks, beverages, food)
- Combo meal bundles with discounts
- Promotional campaigns
- Category organization
- Nutritional information

**Tech Stack**: FastAPI, PostgreSQL, Redis, gRPC

---

### Notification Service

**Purpose**: Multi-channel notification delivery

**Features**:
- Email delivery (SMTP + Jinja2 templates)
- SMS delivery (Twilio)
- Kafka event-driven notifications
- Deduplication and attention tracking
- MongoDB document storage

**Tech Stack**: FastAPI, MongoDB, Redis, Kafka

---

### Employee Service

**Purpose**: Employee management

**Features**:
- Employee CRUD operations
- Role assignment
- Schedule management

**Tech Stack**: FastAPI, PostgreSQL

---

## 📂 Project Structure

```
cinema-plattform/
├── user-service/              # User authentication & profiles
│   ├── app/
│   │   ├── auth/            # Authentication domain
│   │   ├── users/          # Users domain
│   │   ├── profile/        # Profile domain
│   │   └── shared/         # Shared utilities
│   ├── alembic/            # Database migrations
│   ├── docker/              # Docker configuration
│   └── docs/                # Service documentation
│
├── wallet-service/           # Digital wallet management
│   ├── app/
│   │   ├── wallet/         # Wallet domain
│   │   └── shared/         # Shared utilities
│   └── docs/                # Service documentation
│
├── catalog-service/          # Movies, cinemas, theaters
│   ├── app/
│   │   ├── movies/         # Movies domain
│   │   ├── cinema/         # Cinema domain
│   │   ├── theater/        # Theater domain
│   │   └── shared/         # Shared utilities
│   └── docs/                # Service documentation
│
├── billboard-service/        # Showtimes & reservations
│   ├── app/
│   │   ├── showtime/       # Showtime domain
│   │   └── shared/         # Shared utilities
│   └── docs/                # Service documentation
│
├── concession-service/       # Food & beverage products
│   ├── app/
│   │   ├── products/       # Products domain
│   │   ├── combos/          # Combos domain
│   │   ├── promotions/      # Promotions domain
│   │   └── shared/         # Shared utilities
│   └── docs/                # Service documentation
│
├── notification-service/     # Multi-channel notifications
│   ├── app/
│   │   ├── notification/   # Notification domain
│   │   └── shared/         # Shared utilities
│   └── docs/                # Service documentation
│
├── employee-service/         # Employee management
│   ├── app/
│   └── docs/                # Service documentation
│
├── admin-service/           # Spring Boot Admin dashboard
│
└── kafka-infra/              # Centralized Kafka cluster
    └── docker-compose.yml
```

---

## 🔧 Development

### Code Quality Tools

```bash
# Format code
black app/ tests/

# Lint code
ruff check app/ tests/

# Type checking
mypy app/

# Run tests
pytest
pytest --cov=app --cov-report=html
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Add new column"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

### gRPC Code Generation

```bash
# Generate Python code from .proto files
python -m grpc_tools.protoc \
    -I. \
    --python_out=. \
    --grpc_python_out=. \
    your_service.proto
```

---

## 📊 Performance Metrics

| Metric | Target |
|--------|--------|
| API Response Time (p95) | <150ms |
| gRPC Response Time | <30ms |
| Cache Hit Rate | 85%+ |
| Database Query Time | <50ms |
| Service Uptime | 99.9% |
| Concurrent Users | 5,000+ |

---

## 🔒 Security

- **JWT Authentication** - All protected endpoints require valid tokens
- **Role-Based Access Control** - ADMIN, CUSTOMER, EMPLOYEE, MANAGER roles
- **Rate Limiting** - SlowAPI for abuse protection (30-60 req/min)
- **Input Validation** - Pydantic v2 for request validation
- **Environment Secrets** - All credentials via environment variables
- **Non-root Docker** - Containers run as non-root user

---

## 📖 Documentation

Each service has comprehensive documentation in its `/docs` folder:

- **[Project Overview](docs/ProjectOverview.md)** - Problem statement and solutions
- **[Features](docs/ProjectFeatures.md)** - Detailed feature descriptions
- **[Architecture](docs/ProjectArchitectureModel.md)** - Layers, patterns, strategies
- **[Infrastructure](docs/InfrastructureModel.md)** - Docker setup and deployment
- **[API Schema](docs/APISchema.md)** - Complete API documentation
- **[Code Showcase](docs/ProjectCodeShowCase.md)** - Code examples
- **[Metrics](docs/ProjectMetric.md)** - Performance metrics
- **[Media Gallery](docs/MediaGallerySection.md)** - Diagrams and screenshots

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Follow the architecture conventions (DDD, Clean Architecture)
4. Write tests for new features
5. Ensure all tests pass (`pytest`)
6. Run linting and type checks
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Alexis** - _Initial work_

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Excellent async framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - Powerful ORM
- [PostgreSQL](https://www.postgresql.org/) - Robust relational database
- [MongoDB](https://www.mongodb.com/) - Flexible document database
- [Redis](https://redis.io/) - Blazing-fast cache
- [Apache Kafka](https://kafka.apache.org/) - Event streaming platform
- [gRPC](https://grpc.io/) - Efficient inter-service communication
- [Docker](https://www.docker.com/) - Container platform
- [The Python Community](https://www.python.org/) - Amazing tools and libraries

---

## 📞 Contact & Links

- **GitHub**: [https://github.com/anomalyco/cinema-plattform](https://github.com/anomalyco/cinema-plattform)
- **Issues**: [GitHub Issues](https://github.com/anomalyco/cinema-plattform/issues)

### Service-Specific Links

| Service | Documentation | API Docs |
|---------|--------------|----------|
| User Service | [user-service/docs/](user-service/docs/) | http://localhost:8000/docs |
| Wallet Service | [wallet-service/docs/](wallet-service/docs/) | http://localhost:8001/docs |
| Catalog Service | [catalog-service/docs/](catalog-service/docs/) | http://localhost:8002/docs |
| Billboard Service | [billboard-service/docs/](billboard-service/docs/) | http://localhost:8003/docs |
| Concession Service | [concession-service/docs/](concession-service/docs/) | http://localhost:8004/docs |
| Notification Service | [notification-service/docs/](notification-service/docs/) | http://localhost:8005/docs |
| Admin Dashboard | - | http://localhost:8080 |

---

## 🗺️ Roadmap

- [ ] Order Service - Complete purchase flow
- [ ] Payment Gateway Integration - Stripe/PayPal
- [ ] Mobile Apps - iOS and Android clients
- [ ] Real-time Notifications - WebSocket support
- [ ] Analytics Dashboard - Business intelligence
- [ ] Multi-tenancy - Support for multiple cinema chains
- [ ] GraphQL API - Alternative to REST

---

<div align="center">

**Built with ❤️ using Python, FastAPI, PostgreSQL, MongoDB, Redis, Kafka, and Domain-Driven Design**

⭐ Star this repo if you find it helpful!

</div>
