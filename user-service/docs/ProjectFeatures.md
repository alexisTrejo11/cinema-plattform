# Project Features

## Feature List (`ProjectFeature[]`)

### Feature 1: User Registration & Authentication

- **ID**: "user-auth"
- **Title**: "User Registration & Authentication"
- **Description**: Complete user signup and login system with strong password validation, email-based identification, and JWT token generation.
- **Icon**: "user-plus"
- **Category** (`FeatureCategory`): `authentication` | `security`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Email/password authentication
  - Strong password validation (8+ chars, uppercase, lowercase, digit, special char)
  - Access token (JWT) for API authorization
  - Refresh token for session management
  - Configurable JWT audience and issuer validation
- **Tech Stack** (optional):
  - FastAPI
  - PyJWT
  - Pydantic
- **Code Snippet** (optional, `CodeSnippet`):
  - **Language**: "python"
  - **Filename** (optional): "auth_controllers.py"
  - **Code**:
    ```python
    @router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
    async def signup(request_body: SignUpRequest, use_cases: AuthUseCasesContainer = Depends(get_auth_use_cases)):
        result = await use_cases.signup.execute(request_body)
        if not result.is_success():
            raise HTTPException(status_code=400, detail=result.get_error_message())
        return result.get_data()
    ```
- **GitHub Example URL** (optional): "https://github.com/anomalyco/cinema-plattform/blob/main/user-service/app/auth/infrastructure/api/auth_controllers.py"

---

### Feature 2: Session Management

- **ID**: "session-mgmt"
- **Title**: "Session Management"
- **Description**: Redis-based session management with support for single session logout, logout-all, and automatic session refresh.
- **Icon**: "key"
- **Category** (`FeatureCategory`): `authentication` | `caching`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Single session logout (invalidate specific refresh token)
  - Logout from all sessions
  - Automatic token refresh
  - Redis-backed session storage
  - Configurable token expiration
- **Tech Stack** (optional):
  - Redis
  - JWT
  - Token Repository Pattern

---

### Feature 3: Two-Factor Authentication (2FA)

- **ID**: "two-fa"
- **Title**: "Two-Factor Authentication (2FA)"
- **Description**: TOTP-based two-factor authentication with QR code generation, enabling/disabling 2FA, and step-up authentication for sensitive operations.
- **Icon**: "shield"
- **Category** (`FeatureCategory`): `authentication` | `security`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - TOTP (Time-based One-Time Password) support
  - QR code generation for authenticator apps
  - Enable/disable 2FA per user
  - Step-up authentication for login
  - Event publishing for 2FA challenges
- **Tech Stack** (optional):
  - pyotp (TOTP generation)
  - qrcode (QR code generation)

---

### Feature 4: User Profile Management

- **ID**: "profile-mgmt"
- **Title**: "User Profile Management"
- **Description**: Users can view and update their profile information including name, phone number, and date of birth.
- **Icon**: "user"
- **Category** (`FeatureCategory`): `api` | `database`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - View own profile
  - Partial profile updates
  - Profile data validation
  - Gender, name, phone, date of birth management

---

### Feature 5: User Administration

- **ID**: "user-admin"
- **Title**: "User Administration"
- **Description**: Admin and manager capabilities to list, create, update, delete, activate, and ban users.
- **Icon**: "users-cog"
- **Category** (`FeatureCategory`): `api` | `security`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - List all users (paginated)
  - Create users
  - Update user details
  - Delete users
  - Activate users
  - Ban users
  - Role-based access (admin only)

---

### Feature 6: Account Status Management

- **ID**: "account-status"
- **Title**: "Account Status Management"
- **Description**: Lifecycle management of user accounts through various statuses (PENDING, ACTIVE, INACTIVE, BANNED) with role-based transitions.
- **Icon**: "toggle-on"
- **Category** (`FeatureCategory`): `database` | `security`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Account activation (admin or self-service)
  - Account deactivation
  - Account banning
  - Status-based login restrictions
  - Status transitions trigger events

---

### Feature 7: JWT Authentication Middleware

- **ID**: "jwt-middleware"
- **Title**: "JWT Authentication Middleware"
- **Description**: HTTP middleware that validates JWT tokens on every request, extracts user context, and attaches it to the request state.
- **Icon**: "lock"
- **Category** (`FeatureCategory`): `authentication` | `security`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Token validation on every request
  - Token expiration handling
  - Invalid token rejection
  - User context extraction
  - Request state attachment

---

### Feature 8: Role-Based Access Control

- **ID**: "rbac"
- **Title**: "Role-Based Access Control"
- **Description**: Authorization system supporting multiple roles (ADMIN, CUSTOMER, EMPLOYEE, MANAGER) with permission checks on protected endpoints.
- **Icon**: "user-shield"
- **Category** (`FeatureCategory`): `security`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - 4 roles: ADMIN, CUSTOMER, EMPLOYEE, MANAGER
  - Role-based endpoint protection
  - Admin-only operations
  - Role hierarchy awareness

---

### Feature 9: Rate Limiting

- **ID**: "rate-limiting"
- **Title**: "API Rate Limiting"
- **Description**: IP-based rate limiting using SlowAPI to protect the service from abuse.
- **Icon**: "clock"
- **Category** (`FeatureCategory`): `security` | `performance`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - 30 requests/minute default limit
  - Per-client rate limiting
  - Configurable limits
  - SlowAPI integration

---

### Feature 10: Redis Caching

- **ID**: "redis-cache"
- **Title**: "Redis Caching"
- **Description**: High-performance Redis caching for session tokens and application data with startup validation.
- **Icon**: "database"
- **Category** (`FeatureCategory`): `caching` | `performance`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Session token storage
  - Cache service wrapper
  - Startup validation (ping + read/write check)
  - Graceful degradation when disabled
  - FastAPI-Cache integration
- **Tech Stack** (optional):
  - Redis 7
  - fastapi-cache

---

### Feature 11: Event Publishing (Kafka)

- **ID**: "kafka-events"
- **Title**: "Event Publishing with Kafka"
- **Description**: Domain event publishing to Kafka for user lifecycle events, enabling other services to react to user changes.
- **Icon**: "radio"
- **Category** (`FeatureCategory`): `messaging` | `integration`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - User signup events
  - User activation/banning events
  - 2FA enable/disable events
  - Notification request events
  - No-op fallback when disabled
- **Tech Stack** (optional):
  - kafka-python
  - Domain Event Envelope pattern

---

### Feature 12: gRPC Service Interface

- **ID**: "grpc-service"
- **Title**: "gRPC Service Interface"
- **Description**: High-performance gRPC interface for internal service-to-service communication.
- **Icon**: "zap"
- **Category** (`FeatureCategory`): `api` | `integration`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - UsersService with multiple RPC methods
  - User lookup by ID
  - Batch user retrieval
  - Dedicated gRPC server container
  - Protocol Buffers definition
- **Tech Stack** (optional):
  - grpcio
  - Protocol Buffers

---

### Feature 13: Docker Containerization

- **ID**: "docker"
- **Title**: "Docker Containerization"
- **Description**: Production-ready Docker setup with multi-container orchestration including load balancing and health checks.
- **Icon**: "container"
- **Category** (`FeatureCategory`): `infrastructure` | `performance`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Multi-stage Docker build
  - 3 application instances with nginx load balancing
  - Separate gRPC server container
  - PostgreSQL 16 Alpine database
  - Redis 7 Alpine cache
  - Automatic migrations on startup
  - Health checks configured

---

### Feature 14: Comprehensive Testing

- **ID**: "testing"
- **Title**: "Unit & Integration Testing"
- **Description**: pytest-based testing suite with async support, integration tests, and JWT helpers.
- **Icon**: "check-circle"
- **Category** (`FeatureCategory`): `testing`
- **Status** (`FeatureStatus`): `stable`
- **Highlights**:
  - Unit tests for repositories
  - Integration tests for controllers
  - JWT token helpers for testing
  - Stub implementations
  - Test fixtures and conftest setup
- **Tech Stack** (optional):
  - pytest
  - pytest-asyncio
  - pytest-mock
