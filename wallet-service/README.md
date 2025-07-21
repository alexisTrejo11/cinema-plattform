# Cinema Wallet Service

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [API Endpoints](#api-endpoints)
- [Domain Models](#domain-models)
- [Technology Stack](#technology-stack)
- [Environment Variables](#environment-variables)
- [Installation & Setup](#installation--setup)
- [Testing](#testing)
- [Project Structure](#project-structure)

## Overview

The Cinema Wallet Service is a microservice designed to manage digital wallet accounts for cinema customers within a larger cinema ecosystem. It provides comprehensive wallet management capabilities including balance management, transaction processing, and financial operations for users purchasing cinema tickets and concessions.

## Architecture

The service follows **Clean Architecture** principles with clear separation of concerns:

```mermaid
graph TB
    subgraph "Presentation Layer"
        A[FastAPI Controllers]
        B[DTOs]
        C[API Documentation]
    end
    
    subgraph "Application Layer"
        D[Use Cases]
        E[Commands & Queries]
        F[Application Services]
    end
    
    subgraph "Domain Layer"
        G[Wallet Entity]
        H[Transaction Entity]
        I[Value Objects]
        J[Domain Services]
    end
    
    subgraph "Infrastructure Layer"
        K[PostgreSQL Repository]
        L[RabbitMQ Producer]
        M[Event Processors]
    end
    
    A --> D
    D --> G
    D --> K
    D --> L
```

### System Architecture

```plaintext
┌─────────────────────────────────────────────────────────────────┐
│                    Cinema Wallet Service                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   Wallet API    │  │   Admin API     │  │   Health API    │  │
│  │  (Staff Only)   │  │  (Admin Only)   │  │   (Public)      │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│                     Middleware Layer                           │
│  • JWT Authentication  • Rate Limiting  • Logging             │
├─────────────────────────────────────────────────────────────────┤
│                    Application Services                        │
│  • Wallet Management  • Transaction Processing  • User Mgmt   │
├─────────────────────────────────────────────────────────────────┤
│                      Domain Models                             │
│  • Wallet Entity  • Transaction Entity  • Value Objects       │
├─────────────────────────────────────────────────────────────────┤
│                    Infrastructure                              │
│  ┌─────────────────┐           ┌─────────────────────────────┐  │
│  │   PostgreSQL    │           │         RabbitMQ            │  │
│  │                 │           │                             │  │
│  │ • Wallet Data   │           │ • User Events Consumer      │  │
│  │ • Transactions  │           │ • Wallet Events Producer    │  │
│  │ • User Cache    │           │ • Event-Driven Messaging   │  │
│  └─────────────────┘           └─────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
          │                                      │
          ▼                                      ▼
┌─────────────────┐                    ┌─────────────────────┐
│ Service Registry│                    │   Other Services    │
│   (Discovery)   │                    │  • User Service     │
└─────────────────┘                    │  • Order Service    │
                                       │  • Notification     │
                                       └─────────────────────┘
```

## Features

### 🏦 Wallet Management
- Create and manage digital wallets for users
- Multi-currency support (USD, EUR, MXN)
- Balance inquiries and transaction history
- Secure wallet operations with validation

### 💳 Transaction Processing
- Add credit to wallets
- Process payments for cinema purchases
- Transaction history with detailed metadata
- Support for different transaction types (credit, payment, refund, transfers)

### 👥 User Management (Admin)
- User lookup by ID or email
- User listing for administrative purposes
- Role-based access control

### 🔒 Security & Authentication
- JWT-based authentication
- Role-based authorization (Staff, Admin)
- Rate limiting (30 requests/minute)
- Comprehensive input validation

### 📊 Event-Driven Architecture
- Consumes user events from other services
- Publishes wallet events for downstream processing
- Asynchronous messaging via RabbitMQ

## API Endpoints

### Health & Status

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|--------------|
| `GET` | `/` | Service status | No |
| `GET` | `/health` | Health check | No |

### Wallet Operations (Staff Access)

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| `GET` | `/api/v2/wallets/{wallet_id}` | Get wallet by ID | - | `WalletResponse` |
| `GET` | `/api/v2/wallets/user/{user_id}` | Get wallet by user ID | - | `WalletResponse` |
| `POST` | `/api/v2/wallets/user/{user_id}` | Create wallet for user | - | `WalletResponse` |
| `POST` | `/api/v2/wallets/add-credit` | Add credit to wallet | `WalletOperationRequest` | `WalletBuyResponse` |
| `POST` | `/api/v2/wallets/pay` | Process payment | `WalletOperationRequest` | `WalletBuyResponse` |

#### Query Parameters for Wallet Retrieval:
- `include_transactions` (bool): Include transaction history (default: false)
- `limit` (int): Number of transactions to return (default: 10, max: 100)
- `offset` (int): Pagination offset (default: 0)

### Admin Operations (Admin Access)

| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| `GET` | `/api/v2/admin/users/{user_id}` | Get user by ID | `UserResponse` |
| `GET` | `/api/v2/admin/users/by-email/{email}` | Get user by email | `UserResponse` |
| `GET` | `/api/v2/admin/users/` | List all users | `List[UserResponse]` |

### Request/Response Examples

#### Add Credit Request
```json
{
  "wallet_id": "c1d2e3f4-a5b6-7890-1234-567890abcdef",
  "amount": 50.00,
  "currency": "USD",
  "payment_details": {
    "method": "credit_card",
    "reference": "cc_transaction_123",
    "metadata": {
      "card_last_four": "1234",
      "transaction_id": "txn_abc123"
    }
  }
}
```

#### Wallet Response
```json
{
  "message": "Wallet Successfully Retrieved",
  "data": {
    "id": "c1d2e3f4-a5b6-7890-1234-567890abcdef",
    "user_id": "2a3b4c5d-6e7f-8901-2345-67890abcdef1",
    "balance": {
      "amount": 150.50,
      "currency": "USD"
    },
    "created_at": "2024-07-15T10:30:00.123456Z",
    "updated_at": "2024-07-20T14:22:15.789012Z",
    "transactions": [
      {
        "transaction_id": "txn_789xyz",
        "amount": 25.00,
        "currency": "USD",
        "transaction_type": "buy_product",
        "timestamp": "2024-07-20T14:22:15.789012Z",
        "payment_details": {
          "method": "wallet",
          "reference": "cinema_purchase_456"
        }
      }
    ]
  },
  "error": null
}
```

## Domain Models

### Wallet Entity
- **ID**: Unique wallet identifier (UUID)
- **User ID**: Associated user identifier
- **Balance**: Current wallet balance with currency
- **Transactions**: List of associated transactions
- **Timestamps**: Creation and last update times

### Transaction Entity
- **Transaction ID**: Unique transaction identifier (UUID)
- **Wallet ID**: Associated wallet
- **Amount**: Transaction amount with currency
- **Type**: Transaction type (ADD_CREDIT, BUY_PRODUCT, REFUND, TRANSFER_IN, TRANSFER_OUT)
- **Payment Details**: Metadata about the payment method
- **Timestamp**: Transaction timestamp

### Supported Currencies
- USD (US Dollar)
- EUR (Euro)
- MXN (Mexican Peso)

## Technology Stack

### Core Framework
- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI web server implementation
- **Pydantic**: Data validation using Python type annotations

### Database & ORM
- **PostgreSQL**: Primary database for persistent storage
- **SQLAlchemy**: SQL toolkit and ORM
- **asyncpg**: Asynchronous PostgreSQL driver

### Messaging & Events
- **RabbitMQ**: Message broker for event-driven communication
- **aio_pika**: Asynchronous RabbitMQ client

### Security & Authentication
- **python-jose**: JWT token handling
- **SlowAPI**: Rate limiting middleware

### Development & Testing
- **pytest**: Testing framework
- **pytest-asyncio**: Async testing support
- **colorlog**: Enhanced logging with colors

## Environment Variables

Create a `.env` file in the project root:

```bash
# Application Configuration
API_NAME="Wallet Service"
API_HOST="0.0.0.0"
API_PORT=8000
API_VERSION="1.0"
DEBUG_MODE=false

# Service Registry
REGISTRY_ADMIN_URL="http://registry-service:8080"

# JWT Configuration
JWT_SECRET_KEY="your-super-secret-jwt-key-here"
JWT_ALGORITHM="HS256"

# Database Configuration
DATABASE_URL="postgresql+asyncpg://user:password@localhost/wallet_db"
POSTGRES_USER="wallet_user"
POSTGRES_PASSWORD="wallet_password"
POSTGRES_HOST="localhost"
POSTGRES_PORT=5432
POSTGRES_DB="wallet_db"

# RabbitMQ Configuration
RABBITMQ_URL="amqp://guest:guest@localhost:5672/"
USER_EVENTS_EXCHANGE="user.events"
CONSUMER_QUEUE_NAME="wallet.user.events"
WALLET_EXCHANGE="wallet.events"
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- RabbitMQ 3.8+

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd wallet-service
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Set up database**
   ```bash
   # Create PostgreSQL database
   createdb wallet_db
   
   # Run database migrations (if applicable)
   # alembic upgrade head
   ```

6. **Start RabbitMQ**
   ```bash
   # Using Docker
   docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
   
   # Or install locally and start service
   sudo systemctl start rabbitmq-server
   ```

7. **Run the application**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

8. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

## Testing

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/wallet/test_repository.py -v
```

### Test Structure
- `tests/users/` - User-related tests
- `tests/wallet/` - Wallet domain and use case tests
- `conftest.py` - Test configuration and fixtures

## Project Structure

```
wallet-service/
├── app/
│   ├── shared/                    # Shared utilities
│   │   ├── base_exceptions.py
│   │   ├── pagination.py
│   │   ├── response.py
│   │   └── documentation.py
│   ├── user/                      # User domain
│   │   ├── application/           # Use cases, DTOs
│   │   ├── auth/                  # Authentication logic
│   │   ├── domain/                # User entities, value objects
│   │   ├── infrastructure/        # Database models, repositories
│   │   └── presentation/          # Controllers, DTOs
│   └── wallet/                    # Wallet domain
│       ├── application/           # Use cases, commands, queries
│       ├── domain/                # Wallet entities, value objects
│       ├── infrastructure/        # Database, messaging
│       └── presentation/          # Controllers, DTOs
├── config/                        # Configuration files
│   ├── app_config.py
│   ├── postgres_config.py
│   ├── logging.py
│   ├── global_exception_handler.py
│   ├── register_server.py
│   └── queue/                     # RabbitMQ configuration
├── middleware/                    # Custom middleware
├── tests/                         # Test files
├── main.py                        # Application entry point
├── requirements.txt               # Dependencies
└── README.md                      # This file
```

---

**Note**: This service is part of a larger cinema management ecosystem and requires proper authentication tokens from the user service to access protected endpoints.
