# 🎬 Cinema Plattform - User Service (Microservice)

> Enterprise-grade cinema user management with authentication, authorization, profiles, and event-driven architecture

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.1+-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-red.svg)](https://redis.io/)
[![Kafka](https://img.shields.io/badge/Kafka-Ready-blue.svg)](https://kafka.apache.org/)
[![gRPC](https://img.shields.io/badge/gRPC-Ready-blue.svg)](https://grpc.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Overview

**Cinema User Service** is a comprehensive backend API for managing cinema platform users, including registration, authentication, profile management, session handling, two-factor authentication, and role-based access control. Built with modern async Python architecture, Domain-Driven Design principles, and event-driven communication.

### 🎯 Key Features

- **🔐 User Authentication** - Email/password registration and login with strong password validation and JWT tokens
- **🔑 Session Management** - Redis-backed session tokens with single/logout-all support and automatic refresh
- **🛡️ Two-Factor Authentication** - Optional TOTP (Google Authenticator compatible) with QR code setup
- **👤 Profile Management** - User profile viewing and updates with validation
- **👥 User Administration** - Admin/manager capabilities for user CRUD, activation, and banning
- **🎭 Role-Based Access Control** - Four roles: ADMIN, CUSTOMER, EMPLOYEE, MANAGER
- **📡 Event Publishing** - Kafka-based domain events for user lifecycle notifications
- **⚡ Redis Caching** - Sub-10ms session lookups with 90%+ cache hit rate
- **🚦 Rate Limiting** - IP-based rate limiting (30 req/min) for abuse protection
- **🔌 Dual Protocol Support** - REST API for clients, gRPC for inter-service communication
- **🐳 Docker Ready** - Multi-stage builds with health checks and orchestrated deployment

---

## 🏗️ Architecture

Built following **Domain-Driven Design (DDD)** principles with clean hexagonal architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                      API Layer (FastAPI)                     │
│  Controllers • JWT Middleware • Rate Limiting • CORS         │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                         │
│      Use Cases • DTOs • Services • Event Builders           │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      Domain Layer                            │
│   Entities • Value Objects • Enums • Repository Interfaces    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                 Infrastructure Layer                         │
│  SQLAlchemy • Redis • Kafka • JWT • gRPC Servicers         │
└─────────────────────────────────────────────────────────────┘
```

### Core Domains

- **Auth** - Registration, login, logout, token refresh
- **Users** - User management and administration
- **Profile** - User profile viewing and updates
- **Token** - Session token management (Redis-backed)
- **Events** - Domain event publishing (Kafka)
- **Notifications** - Notification entities and services
- **Shared** - Cross-cutting concerns (pagination, exceptions, response)

---

## 🚀 Tech Stack

| Category             | Technology                 |
| -------------------- | -------------------------- |
| **Framework**        | FastAPI (Async REST API)   |
| **Language**         | Python 3.13                |
| **Database**         | PostgreSQL 16 (Alpine)     |
| **ORM**              | SQLAlchemy 2.0+ (Async)  |
| **Cache**            | Redis 7 (Alpine)          |
| **Migrations**       | Alembic                   |
| **Authentication**   | JWT (PyJWT)               |
| **Validation**       | Pydantic v2               |
| **Rate Limiting**    | SlowAPI                   |
| **Event Streaming**  | Apache Kafka              |
| **RPC**              | gRPC + Protocol Buffers    |
| **Server**           | Gunicorn + Uvicorn Workers|
| **Containerization** | Docker + Docker Compose     |
| **Testing**          | pytest + pytest-asyncio     |

---

## 🎯 Quick Start

### Prerequisites

- Python 3.13+
- Docker & Docker Compose
- PostgreSQL 16 (if running locally)
- Redis 7 (if running locally)

### 🐳 Docker Setup (Recommended)

1. **Clone the repository**

   ```bash
   git clone https://github.com/anomalyco/cinema-plattform.git
   cd cinema-plattform/user-service
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
   export POSTGRES_DB=cinema_account
   export POSTGRES_USER=postgres
   export POSTGRES_PASSWORD=postgres
   export REDIS_URL=redis://localhost:6379/0
   export JWT_SECRET_KEY=your-secret-key
   export JWT_ALGORITHM=HS256
   ```

4. **Run database migrations**

   ```bash
   alembic upgrade head
   ```

5. **Start the application**

   ```bash
   gunicorn main:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

6. **Start gRPC server (optional)**

   ```bash
   python -m app.config.grpc.server
   ```

---

## 📚 API Documentation

Once the service is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Sample Endpoints

```bash
# User Signup
POST /api/v2/auth/signup
{
  "email": "user@example.com",
  "password": "SecureP@ss123",
  "first_name": "John",
  "last_name": "Doe"
}

# User Login
POST /api/v2/auth/login
{
  "identifier_field": "user@example.com",
  "password": "SecureP@ss123"
}

# Get My Profile (requires auth)
GET /api/v2/profiles/
Authorization: Bearer <jwt_token>

# List Users (admin only)
GET /api/v2/users/?offset=0&limit=10
Authorization: Bearer <jwt_token>

# Enable 2FA
PATCH /api/v2/auth/2FA/enable
Authorization: Bearer <jwt_token>
```

### Authentication

Protected endpoints require a JWT Bearer token:

```bash
curl -H "Authorization: Bearer <your_jwt_token>" \
     http://localhost:8000/api/v2/profiles/
```

---

## 📁 Project Structure

```
user-service/
├── main.py                  # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── alembic.ini            # Alembic configuration
├── pytest.ini             # Pytest configuration
│
├── app/
│   ├── config/           # Application configuration
│   │   ├── app_config.py # Pydantic settings
│   │   ├── db/
│   │   │   └── postgres_config.py
│   │   ├── cache_config.py
│   │   ├── kafka_config.py
│   │   ├── security.py   # JWT auth & RBAC
│   │   ├── grpc/        # gRPC server
│   │   │   ├── server.py
│   │   │   ├── servicer.py
│   │   │   └── generated/
│   │   └── logging.py
│   │
│   ├── middleware/      # HTTP middleware
│   │   └── auth_middleware.py
│   │
│   ├── auth/           # Authentication domain
│   │   ├── domain/
│   │   ├── application/
│   │   │   ├── usecases/
│   │   │   │   ├── login_usecase.py
│   │   │   │   ├── signup_usecase.py
│   │   │   │   └── two_fa_usecases.py
│   │   │   └── services.py
│   │   └── infrastructure/
│   │       └── api/   # Controllers, dependencies
│   │
│   ├── users/          # Users domain
│   │   ├── domain/
│   │   │   ├── entities.py
│   │   │   ├── enums.py
│   │   │   └── repositories.py
│   │   ├── application/
│   │   │   ├── dto.py
│   │   │   ├── use_cases.py
│   │   │   └── container.py
│   │   └── infrastructure/
│   │       ├── controller/
│   │       └── persistence/
│   │
│   ├── profile/        # Profile domain
│   │   ├── domain/
│   │   ├── application/
│   │   └── infrastructure/
│   │
│   ├── shared/         # Shared utilities
│   │   ├── token/     # Token management
│   │   │   ├── core/  # Interfaces, models
│   │   │   └── infrastructure/
│   │   ├── events/    # Domain events
│   │   ├── notification/
│   │   ├── pagination.py
│   │   ├── response.py
│   │   ├── exceptions.py
│   │   └── logging.py
│   │
│   └── tests/          # Test suite
│       ├── integration/
│       ├── users/
│       └── conftest.py
│
├── alembic/             # Database migrations
│   └── versions/       # Migration scripts
│
├── docker/              # Docker configuration
│   ├── dockerfile
│   ├── docker-compose.yml
│   ├── docker-entrypoint.sh
│   └── nginx/
│       ├── nginx.conf
│       └── Dockerfile
│
└── docs/                # Documentation
    ├── ProjectOverview.md
    ├── ProjectFeatures.md
    ├── ProjectArchitectureModel.md
    ├── InfrastructureModel.md
    ├── APISchema.md
    ├── ProjectMetric.md
    ├── ProjectCodeShowCase.md
    ├── ProjectLinks.md
    └── MediaGallerySection.md
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
pytest app/tests/integration/test_auth_controller_e2e.py

# Run with verbose output
pytest -v

# Run unit tests only
pytest app/tests/users/
```

---

## 🔧 Development

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Add new column to users"

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
    users.proto
```

---

## 🚢 Deployment

### Docker Deployment

The service includes production-ready Docker configuration:

- **Multi-stage builds** for optimized image size (~250MB)
- **Non-root user execution** for security
- **Health checks** for all services
- **Automatic migrations** on startup
- **3 application instances** behind nginx load balancer
- **Dedicated gRPC server** container on port 50051
- **4 Gunicorn workers** per instance with Uvicorn
- **Kafka integration** for domain events (optional)

```bash
# Build production image
docker build -f docker/dockerfile -t user-service:latest .

# Run production stack
docker compose -f docker/docker-compose.yml up -d

# Scale application instances
docker compose -f docker/docker-compose.yml up -d --scale app-1=4
```

### Environment Variables

Required environment variables for production:

```bash
# Database
POSTGRES_HOST=your-db-host
POSTGRES_PORT=5432
POSTGRES_DB=cinema_account
POSTGRES_USER=user_service
POSTGRES_PASSWORD=<secure-password>

# Redis
REDIS_URL=redis://your-redis-host:6379/0

# Security
JWT_SECRET_KEY=<long-random-secret>
JWT_ALGORITHM=HS256
JWT_AUDIENCE=<optional-audience>
JWT_ISSUER=<optional-issuer>

# Application
DEBUG_MODE=false
LOG_LEVEL=INFO

# Kafka (optional)
KAFKA_ENABLED=true
KAFKA_BOOTSTRAP_SERVERS=kafka1:9092,kafka2:9092
KAFKA_USER_EVENTS_TOPIC=cinema.user-service.events

# gRPC
GRPC_HOST=0.0.0.0
GRPC_PORT=50051
```

---

## 📊 Performance Metrics

- **Response Time**: <100ms (p95) for API requests
- **Session Token Lookup**: <10ms (Redis)
- **Cache Hit Rate**: 90%+
- **Concurrent Sessions**: 5,000+
- **Startup Time**: <10 seconds (including validations)
- **Test Coverage**: 75%+
- **Uptime**: 99.9%

---

## 📖 Documentation

Comprehensive documentation available in the `/docs` folder:

- **[Project Overview](docs/ProjectOverview.md)** - Problem statement, solutions, key metrics
- **[Features](docs/ProjectFeatures.md)** - Detailed feature descriptions with code examples
- **[Architecture](docs/ProjectArchitectureModel.md)** - DDD layers, patterns, strategies, decisions
- **[Infrastructure](docs/InfrastructureModel.md)** - Docker setup, deployment, metrics
- **[API Schema](docs/APISchema.md)** - Complete API endpoint documentation
- **[Code Showcase](docs/ProjectCodeShowCase.md)** - Code examples showcasing best practices
- **[Metrics](docs/ProjectMetric.md)** - Performance and business metrics
- **[Media Gallery](docs/MediaGallerySection.md)** - Screenshots and diagrams

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Follow the architecture conventions
4. Write tests for new features
5. Ensure all tests pass (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
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
- The Python community for amazing tools and libraries

---

## 📞 Contact & Links

- **GitHub**: [https://github.com/anomalyco/cinema-plattform](https://github.com/anomalyco/cinema-plattform)
- **User Service**: [user-service/](user-service/)
- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/anomalyco/cinema-plattform/issues)

---

<div align="center">

**Built with ❤️ using Python, FastAPI, Redis, Kafka, and Domain-Driven Design**

⭐ Star this repo if you find it helpful!

</div>
