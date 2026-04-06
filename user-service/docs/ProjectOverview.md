# Project Overview

## 1. Problem Statement (`OverviewProblemStatement`)

- **Problem Title**: "Cinema User Management & Authentication"
- **Problem Description**:
  - Cinema platforms need a centralized user management service to handle customer registration, authentication, profile management, and authorization across all services. Legacy systems often lack secure session management, multi-factor authentication, and event-driven communication with other microservices.
- **Problem List**:
  - Secure user registration and login with strong password validation
  - Session management with access and refresh tokens
  - Two-factor authentication (2FA) with TOTP support
  - User profile management and updates
  - Role-based access control (admin, customer, employee, manager)
  - Account status management (pending, active, inactive, banned)
  - Event-driven communication with other cinema platform services
  - gRPC interface for internal service-to-service communication

---

## 2. Solution (`OverviewSolution`)

- **Solution Title**: "Comprehensive User Management Microservice"
- **Solution List** (array of `Solution`):
  - **Solution 1**
    - **Title**: "Hexagonal Architecture"
    - **Description**: Clean separation of domain logic from infrastructure using Ports and Adapters pattern with clear domain/application/infrastructure layers.
  - **Solution 2**
    - **Title**: "JWT-Based Session Management"
    - **Description**: Stateless authentication with access tokens for API authorization and refresh tokens stored in Redis for session management.
  - **Solution 3**
    - **Title**: "Two-Factor Authentication (TOTP)"
    - **Description**: Optional 2FA with TOTP (Google Authenticator compatible) for enhanced account security.
  - **Solution 4**
    - **Title**: "Event-Driven Architecture"
    - **Description**: Kafka-based domain events for user lifecycle notifications to other microservices (notification service, etc.).
  - **Solution 5**
    - **Title**: "Dual Protocol Support"
    - **Description**: REST API for client-facing operations and gRPC for high-performance inter-service communication.

---

## 3. Key Metrics (`OverviewKeyMetrics`)

- **Metrics Title**: "Service Performance Indicators"
- **Metrics List** (strings):
  - "API Response Time: < 100ms (p95)"
  - "Session Token Lookup: < 10ms (Redis)"
  - "Authentication Success Rate: > 99%"
  - "Uptime: 99.9%"

See also [ProjectMetric.md](ProjectMetric.md) for richer metrics.

---

## 4. Cover Image (`ProjectCoverImage`, optional)

- **URL**: "https://via.placeholder.com/800x400/user-service-cover"
- **Alt**: "User Service Architecture"
- **Credit** (optional): "Cinema Platform Team"

---

## 5. Links (`ProjectLinks`)

See [ProjectLinks.md](ProjectLinks.md).

- **GitHub**: "https://github.com/anomalyco/cinema-plattform"
- **Demo**: null
- **Documentation**: "https://cinema-platform.example.com/docs/user-service"
- **Docker Hub**: "https://hub.docker.com/r/cinema-platform/user-service"

---

## 6. Media Gallery Section (`MediaGallerySection`)

See [MediaGallerySection.md](MediaGallerySection.md).

- **Title**: "User Service Visuals"
- **Description**: "Screenshots and diagrams showcasing the user service authentication flows and architecture."
- **Items**: list of media items (see `ProjectMediaItem` in MediaGallerySection.md).

---

## 7. Media Items (`ProjectMediaItem[]`)

For each media item:

- **Type**: `image`
- **URL**: "https://via.placeholder.com/800x600/auth-flow"
- **Thumbnail** (optional): "https://via.placeholder.com/400x300/auth-flow-thumb"
- **Title**: "Authentication Flow"
- **Description**: "Sequence diagram showing the user authentication flow"
- **Alt** (optional): "Authentication flow diagram"
- **Category** (optional): `diagram`

---

## 8. Metrics (`ProjectMetric[]`)

For each metric see [ProjectMetric.md](ProjectMetric.md):

- **Label**: "Active Users"
- **Value**: "10,000+"
- **Description** (optional): "Registered users in the platform"
- **Icon** (optional): "users"
- **Unit** (optional): "users"
- **Trend** (optional): `up`
- **Threshold** (optional): "5000"
