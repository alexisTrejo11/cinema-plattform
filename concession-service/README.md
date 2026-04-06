# 🎬 Cinema Plattform - Concession Service (Microservice)

> Enterprise-grade cinema concession management with products, combos, promotions, and real-time availability tracking

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.1+-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-red.svg)](https://redis.io/)
[![gRPC](https://img.shields.io/badge/gRPC-Ready-blue.svg)](https://grpc.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Overview

**Cinema Concession Service** is a comprehensive backend API for managing cinema concession operations, including food products, combo meals, promotional campaigns, and product categories. Built with modern async Python architecture, Domain-Driven Design principles, and supporting both REST and gRPC protocols.

### 🎯 Key Features

- **🍿 Product Catalog Management** - Complete CRUD operations for cinema concession products (snacks, beverages, food) with pricing, availability, preparation time, and nutritional info
- **🎁 Combo Meal System** - Create and manage bundle deals with multiple products and configurable discount percentages
- **🏷️ Promotional Campaigns** - Time-based promotions linked to specific products or categories with usage tracking
- **📁 Category Organization** - Hierarchical product categorization with active/inactive status management
- **🔐 JWT Authentication** - Secure token-based authentication with role-based access control (admin/manager)
- **⚡ Redis Caching** - Sub-100ms response times with 85%+ cache hit rate
- **🚦 Rate Limiting** - IP-based rate limiting (60 req/min reads, 10 req/min writes)
- **🔍 Advanced Search** - Multi-criterion search with filters, pagination, and sorting
- **🔌 Dual Protocol Support** - REST API for clients, gRPC for inter-service communication
- **🐳 Docker Ready** - Multi-stage builds with health checks and orchestrated deployment

---

## 🏗️ Architecture

Built following **Domain-Driven Design (DDD)** principles with clean hexagonal architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                      API Layer (FastAPI)                     │
│  Controllers • JWT Middleware • Rate Limiting • Logging      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                         │
│         Use Cases • Commands/Queries • DTOs • Mappers       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      Domain Layer                            │
│   Entities • Value Objects • Repository Interfaces • Rules   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                 Infrastructure Layer                         │
│    SQLAlchemy • PostgreSQL • Redis • gRPC Servicers         │
└─────────────────────────────────────────────────────────────┘
```

### Core Domains

- **Products** - Food product catalog with pricing, availability, and nutritional info
- **Categories** - Product categorization and organization
- **Combos** - Bundle meal management with discount pricing
- **Promotions** - Time-based campaigns with product/category linking
- **Shared** - Cross-cutting concerns (pagination, exceptions, caching, auth)

---

## 🚀 Tech Stack

| Category             | Technology                 |
| -------------------- | -------------------------- |
| **Framework**        | FastAPI (Async REST API)   |
| **Language**         | Python 3.13                |
| **Database**         | PostgreSQL 16 (Alpine)     |
| **ORM**              | SQLAlchemy 2.0+ (Async)    |
| **Cache**            | Redis 7 (Alpine)           |
| **Migrations**       | Alembic                    |
| **Authentication**   | JWT (PyJWT)                |
| **Validation**       | Pydantic v2                |
| **Rate Limiting**    | SlowAPI                    |
| **RPC**              | gRPC + Protocol Buffers    |
| **Server**           | Gunicorn + Uvicorn Workers |
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
   cd cinema-plattform/concession-service
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
   export POSTGRES_DB=cinema_concession
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
   python -m app.grpc.server
   ```

---

## 📚 API Documentation

Once the service is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Sample Endpoints

```bash
# Get all products (paginated with filters)
GET /api/v2/products/?page=1&page_size=10&category_id=1&min_price=5.00

# Get product by ID
GET /api/v2/products/{product_id}

# Search products
GET /api/v2/products/?name_like=popcorn&available_only=true

# Get all categories
GET /api/v2/categories/

# Get active combos
GET /api/v2/combos/?page=1&page_size=20

# Get combo by ID
GET /api/v2/combos/{combo_id}

# Get active promotions
GET /api/v2/promotions/active/

# Create product (requires admin/manager role)
POST /api/v2/products/
Authorization: Bearer <jwt_token>
```

### Authentication

Protected endpoints require a JWT Bearer token:

```bash
curl -H "Authorization: Bearer <your_jwt_token>" \
     -X POST http://localhost:8000/api/v2/products/ \
     -H "Content-Type: application/json" \
     -d '{"name":"Large Popcorn","price":8.99,"category_id":1}'
```

---

## 📁 Project Structure

```
concession-service/
├── main.py                  # FastAPI application entry point
├── requirements.txt         # Python dependencies
├── alembic.ini             # Alembic configuration
├── pytest.ini              # Pytest configuration
├── concession.proto        # gRPC protocol definitions
│
├── app/
│   ├── config/             # Application configuration
│   │   ├── app_config.py   # Pydantic settings
│   │   ├── db/
│   │   │   └── postgres_config.py
│   │   ├── cache_config.py
│   │   ├── security.py     # JWT auth & RBAC
│   │   └── rate_limit.py
│   │
│   ├── products/          # Products domain (DDD)
│   │   ├── domain/
│   │   │   ├── entities/  # Product, ProductCategory
│   │   │   ├── repositories.py
│   │   │   └── exceptions.py
│   │   ├── application/
│   │   │   ├── commands.py
│   │   │   ├── queries.py
│   │   │   └── use_cases/
│   │   └── infrastructure/
│   │       ├── api/       # Controllers, DTOs
│   │       └── persistence/  # SQLAlchemy repos
│   │
│   ├── combos/            # Combos domain (DDD)
│   │   ├── domain/
│   │   ├── application/
│   │   └── infrastructure/
│   │
│   ├── promotions/        # Promotions domain (DDD)
│   │   ├── domain/
│   │   ├── application/
│   │   └── infrastructure/
│   │
│   ├── grpc/             # gRPC service implementation
│   │   ├── server.py
│   │   ├── clients/
│   │   ├── services/
│   │   └── generated/     # Protobuf generated code
│   │
│   ├── middleware/       # HTTP middleware
│   │   ├── jwt_auth_middleware.py
│   │   └── logging_middleware.py
│   │
│   ├── shared/           # Shared utilities
│   │   ├── pagination.py
│   │   ├── response.py
│   │   ├── base_exceptions.py
│   │   └── docs/
│   │
│   └── tests/            # Test suite
│       ├── api/
│       ├── repository/
│       └── conftest.py
│
├── alembic/              # Database migrations
│   ├── env.py
│   └── versions/         # Migration scripts
│
├── docker/               # Docker configuration
│   ├── dockerfile
│   ├── docker-compose.yml
│   ├── docker-entrypoint.sh
│   └── nginx/
│       ├── nginx.conf
│       └── Dockerfile
│
└── docs/                 # Documentation
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
pytest app/tests/api/test_product_controller_e2e.py

# Run with verbose output
pytest -v

# Run repository tests
pytest app/tests/repository/
```

---

## 🔧 Development

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Add new column to products"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history

# Show current migration
alembic current
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
    concession.proto
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

```bash
# Build production image
docker build -f docker/dockerfile -t concession-service:latest .

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
POSTGRES_DB=cinema_concession
POSTGRES_USER=concession_user
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

# gRPC
GRPC_HOST=0.0.0.0
GRPC_PORT=50051
```

---

## 📊 Performance Metrics

- **Response Time**: <100ms (p95) for API requests
- **Cache Hit Rate**: 85%+
- **Database Query Time**: <50ms (p95)
- **Concurrent Requests**: 500+ per worker
- **Startup Time**: <10 seconds (including migrations)
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
- gRPC for efficient inter-service communication
- The Python community for amazing tools and libraries

---

## 📞 Contact & Links

- **GitHub**: [https://github.com/anomalyco/cinema-plattform](https://github.com/anomalyco/cinema-plattform)
- **Concession Service**: [concession-service/](concession-service/)
- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/anomalyco/cinema-plattform/issues)

---

<div align="center">

**Built with ❤️ using Python, FastAPI, gRPC, and Domain-Driven Design**

⭐ Star this repo if you find it helpful!

</div>
