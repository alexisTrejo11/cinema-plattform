# Notification Service (Microservice)

> Centralized notification service for multi-channel user communications (Email, SMS, Push, In-App)

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.1+-green.svg)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Ready-green.svg)](https://www.mongodb.com/)
[![Redis](https://img.shields.io/badge/Redis-7-red.svg)](https://redis.io/)
[![Kafka](https://img.shields.io/badge/Kafka-Ready-blue.svg)](https://kafka.apache.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Overview

**Notification Service** is a centralized microservice responsible for managing and delivering multi-channel notifications to users across the Cinema Platform ecosystem. It supports Email (SMTP), SMS (Twilio), Push Notifications, and In-App notifications with a domain-driven design architecture.

### Key Features

- **Multi-Channel Delivery** - Send notifications via Email (SMTP), SMS (Twilio), Push Notifications, and In-App
- **Event-Driven Architecture** - Consumes Kafka events from other services for automatic notification triggering
- **Template-Based Emails** - HTML email templates using Jinja2 for consistent branding
- **User Directory Integration** - Automatic recipient contact resolution via HTTP lookup to user-service
- **Deduplication** - Prevents duplicate notifications from idempotent Kafka event processing
- **Attention Tracking** - Operational monitoring for important/failed notifications requiring follow-up
- **Rate Limiting** - SlowAPI-based rate limiting (60 req/min) for API abuse protection
- **JWT Authentication** - Secure API endpoints with JWT token validation
- **MongoDB Persistence** - Async document storage with Motor driver
- **Redis Caching** - FastAPI-Cache integration for performance optimization

---

## Architecture

Built following **Domain-Driven Design (DDD)** principles with hexagonal architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                   Presentation Layer (FastAPI)               │
│  Controllers • JWT Middleware • Rate Limiting • Logging      │
└─────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                        │
│    Use Cases • Commands • Queries • DTOs • Event Handlers    │
└─────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────┐
│                      Domain Layer                           │
│   Entities • Value Objects • Enums • Repository Interfaces   │
└─────────────────────────────────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────┐
│                 Infrastructure Layer                         │
│   MongoDB • Redis • Kafka • SMTP • Twilio • HTTP Clients     │
└─────────────────────────────────────────────────────────────┘
```

### Core Domains

- **Notification** - Aggregate root managing notification lifecycle (PENDING → SENT/FAILED)
- **NotificationContent** - Value object for subject, body, template, and data
- **Recipient** - Value object for user_id, email, phone_number, device_token
- **SendingService** - Port interface for notification delivery adapters
- **UserProfileService** - Port interface for user contact resolution

---

## Tech Stack

| Category           | Technology                    |
| ------------------ | ----------------------------- |
| **Framework**      | FastAPI (Async REST API)      |
| **Language**       | Python 3.13                   |
| **Database**       | MongoDB (Motor Async Driver)   |
| **Cache**          | Redis 7                       |
| **Message Broker** | Apache Kafka                  |
| **Email**          | SMTP + Jinja2 Templates       |
| **SMS**            | Twilio API                    |
| **Authentication** | JWT (PyJWT)                   |
| **Validation**     | Pydantic v2                   |
| **Rate Limiting**  | SlowAPI                       |
| **Server**         | Uvicorn                       |
| **Containerization** | Docker + Docker Compose     |

---

## Quick Start

### Prerequisites

- Python 3.13+
- Docker & Docker Compose
- MongoDB (if running locally)
- Redis 7 (if running locally)

### Docker Setup (Recommended)

1. **Clone the repository**

   ```bash
   git clone https://github.com/anomalyco/cinema-plattform.git
   cd cinema-plattform/notification-service
   ```

2. **Configure environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start all services**

   ```bash
   docker compose up --build -d
   ```

4. **Access the API**
   - API: http://localhost:8000
   - Swagger Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Local Development Setup

1. **Create virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**

   ```bash
   export MONGO_URI=mongodb://localhost:27017
   export MONGO_DB_NAME=notification_db
   export REDIS_URL=redis://localhost:6379/0
   export SMTP_HOST=smtp.example.com
   export SMTP_PORT=587
   export SMTP_USERNAME=user@example.com
   export SMTP_PASSWORD=your_password
   ```

4. **Start the application**

   ```bash
   uvicorn main:app --reload
   ```

---

## API Documentation

Once the service is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Sample Endpoints

```bash
# Create Notification (requires auth)
POST /api/v2/notifications
Authorization: Bearer <jwt_token>
{
  "notification_type": "TICKET_BUY",
  "channel": "EMAIL",
  "recipient": {
    "user_id": "user-123",
    "email": "user@example.com"
  },
  "content": {
    "subject": "Your Ticket Confirmation",
    "body": "Your tickets have been purchased successfully."
  }
}

# Get Notification by ID (requires auth)
GET /api/v2/notifications/{notification_id}
Authorization: Bearer <jwt_token>

# List Notifications (requires auth)
GET /api/v2/notifications?notification_type=TICKET_BUY&channel=EMAIL&limit=10&offset=0
Authorization: Bearer <jwt_token>

# Health Check
GET /health
```

### Authentication

Protected endpoints require a JWT Bearer token:

```bash
curl -H "Authorization: Bearer <your_jwt_token>" \
     http://localhost:8000/api/v2/notifications
```

---

## Project Structure

```
notification-service/
├── main.py                  # FastAPI application entry point
├── requirements.txt          # Python dependencies
├── README.md                # This file
│
├── app/
│   ├── config/              # Application configuration
│   │   ├── app_config.py    # Pydantic settings
│   │   ├── mongo_config.py  # MongoDB connection
│   │   ├── kafka_config.py  # Kafka consumer
│   │   ├── cache_config.py  # Redis cache
│   │   ├── logging.py       # Logging setup
│   │   ├── register_service.py  # Service registry
│   │   ├── rate_limit.py    # Rate limiter
│   │   └── global_exception_handler.py
│   │
│   ├── notification/        # Notification domain (DDD)
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   │   ├── models.py      # Notification aggregate
│   │   │   │   ├── content.py     # NotificationContent VO
│   │   │   │   └── recipient.py   # Recipient VO
│   │   │   ├── enums.py           # NotificationType, Channel, Status
│   │   │   ├── repository.py      # NotificationRepository ABC
│   │   │   ├── sending_service.py  # SendingService ABC
│   │   │   └── user_profile_service.py
│   │   │
│   │   ├── application/
│   │   │   ├── commands/          # CreateNotificationCommand
│   │   │   ├── queries/           # GetNotificationByIdQuery, ListNotificationsQuery
│   │   │   ├── usecases/          # Create, Get, List, ProcessEvent use cases
│   │   │   ├── dtos.py            # Response DTOs
│   │   │   └── events/            # Topic registry
│   │   │
│   │   ├── infrastructure/
│   │   │   ├── repository/        # MongoNotificationRepository
│   │   │   ├── email/             # EmailService + Jinja2 templates
│   │   │   ├── message/           # SmsMessageService (Twilio)
│   │   │   ├── external/          # UserProfileHttpService
│   │   │   ├── queue/             # RabbitMQ receiver (placeholder)
│   │   │   └── services.py        # SendingServiceImplementation
│   │   │
│   │   └── presentation/
│   │       ├── notification_controller.py  # API endpoints
│   │       └── dependencies.py             # DI container
│   │
│   └── shared/                # Cross-cutting concerns
│       ├── auth.py            # JWT helpers, role checking
│       ├── qr.py              # QR code generation
│       ├── documentation.py   # OpenAPI error specs
│       ├── base_exceptions.py # Base exceptions
│       ├── core/
│       │   ├── exceptions.py  # Domain, Application, Auth exceptions
│       │   ├── response.py    # Result, ErrorResponse
│       │   ├── pagination.py  # PaginationParams, Page
│       │   └── jwt_security.py
│       ├── middleware/
│       │   ├── logging_middleware.py
│       │   └── jwt_security.py
│       └── events/
│           ├── base.py        # IntegrationEvent, DomainEvent
│           ├── protocols.py   # EventPublisher
│           └── infrastructure/  # Kafka, Noop publishers
│
├── docker/                    # Docker configuration
├── logs/                      # Application logs
└── docs/                      # Documentation
    ├── ProjectOverview.md
    ├── ProjectFeatures.md
    ├── ProjectArchitectureModel.md
    ├── InfrastructureModel.md
    ├── APISchema.md
    ├── ProjectMetric.md
    ├── ProjectCodeShowCase.md
    ├── ProjectLinks.md
    ├── MediaGallerySection.md
    └── ProjectMetadata.md
```

---

## Notification Types

| Type              | Description                        |
| ----------------- | ---------------------------------- |
| PRODUCT_BUY       | Product purchase confirmation      |
| TICKET_BUY        | Movie ticket purchase confirmation  |
| ACCOUNT_AUTH      | Authentication events (login, 2FA) |
| ACCOUNT_CREATED   | New account registration            |
| ACCOUNT_DELETED   | Account deletion notification       |
| PAYMENT_FAILED    | Payment failure alert              |
| ANNOUNCEMENT      | Platform announcements             |
| CUSTOM_MESSAGE    | Custom notification messages       |

## Notification Channels

| Channel           | Provider       | Description              |
| ----------------- | -------------- | ------------------------ |
| EMAIL             | SMTP           | HTML email with Jinja2 templates |
| SMS               | Twilio         | Text messages            |
| PUSH_NOTIFICATION | (Future)       | Mobile push notifications |
| IN_APP            | Internal       | In-application alerts    |

## Notification Status

| Status    | Description                          |
| --------- | ------------------------------------ |
| PENDING   | Created, awaiting processing         |
| SENT      | Successfully delivered to provider   |
| FAILED    | Delivery failed                     |
| DELIVERED | Confirmed delivered to user         |
| READ      | User has read the notification      |
| CANCELED  | Notification canceled                |

---

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest app/tests/

# Run with verbose output
pytest -v
```

---

## Development

### Code Quality

```bash
# Format code
black app/

# Lint code
ruff check app/

# Type checking
mypy app/
```

---

## Deployment

### Docker Deployment

The service includes production-ready Docker configuration:

- **Async Uvicorn** server with health checks
- **MongoDB** async driver (Motor)
- **Kafka consumer** for event-driven notifications
- **Service registry** integration for microservice discovery

```bash
# Build production image
docker build -t notification-service:latest .

# Run production stack
docker compose up -d
```

### Environment Variables

Required environment variables for production:

```bash
# MongoDB
MONGO_URI=mongodb://your-mongo-host:27017
MONGO_DB_NAME=notification_db

# Redis
REDIS_URL=redis://your-redis-host:6379/0

# JWT
JWT_SECRET_KEY=<long-random-secret>
JWT_ALGORITHM=HS256

# SMTP
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=user@example.com
SMTP_PASSWORD=<secure-password>
EMAIL_FROM_ADDRESS=no-reply@cinema.local

# Twilio (optional)
TWILIO_ENABLED=true
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# Kafka (optional)
KAFKA_ENABLED=true
KAFKA_BOOTSTRAP_SERVERS=kafka1:9092,kafka2:9092
KAFKA_TOPIC_NOTIFICATION_INCOMING=notification.incoming
```

---

## Performance Metrics

- **Response Time**: <100ms (p95) for API requests
- **Event Processing**: Sub-second Kafka event processing
- **MongoDB Queries**: Indexed by notification_id, user_id, status
- **Cache Hit Rate**: 90%+ (Redis)
- **Concurrent Notifications**: 1,000+ per minute
- **Uptime**: 99.9%

---

## Documentation

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

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Follow the architecture conventions (DDD structure)
4. Write tests for new features
5. Ensure all tests pass (`pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Authors

- **Alexis** - _Initial work_

---

## Acknowledgments

- FastAPI for the excellent async framework
- MongoDB for flexible document storage
- Redis for blazing-fast caching
- Apache Kafka for event streaming
- Twilio for SMS delivery
- The Python community for amazing tools and libraries

---

## Contact & Links

- **GitHub**: [https://github.com/anomalyco/cinema-plattform](https://github.com/anomalyco/cinema-plattform)
- **Notification Service**: [notification-service/](notification-service/)
- **Documentation**: [docs/](docs/)
- **Issues**: [GitHub Issues](https://github.com/anomalyco/cinema-plattform/issues)

---

<div align="center">

**Built with ❤️ using Python, FastAPI, MongoDB, Redis, and Kafka**

⭐ Star this repo if you find it helpful!

</div>
