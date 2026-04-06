---
projectId: notification-service
name: Notification Service
shortName: notification-service
status: "active"
docsVersion: "1.0.0"
lastUpdated: "2026-04-06"
owner: "Alexis"
repositoryUrl: "https://github.com/anomalyco/cinema-plattform"
tags: ["microservice", "notifications", "fastapi", "mongodb", "kafka", "ddD", "hexagonal-architecture"]
---

# Project Documentation

## 1. Code Showcase

- **File**: [ProjectCodeShowCase.md](ProjectCodeShowCase.md)
- **Description**: Code examples that highlight key implementation details and patterns including the Notification aggregate, event processing, multi-channel delivery, and MongoDB repository.

## 2. Overview

- **File**: [ProjectOverview.md](ProjectOverview.md)
- **Description**: Business context, problem statement, solution overview, and key metrics for the notification service.

## 3. Infrastructure

- **File**: [InfrastructureModel.md](InfrastructureModel.md)
- **Description**: Deployments, Docker configuration, cloud services (MongoDB Atlas, Redis Cloud, Kafka, Twilio, SMTP), and infrastructure metrics.

## 4. Architecture

- **File**: [ProjectArchitectureModel.md](ProjectArchitectureModel.md)
- **Description**: DDD layers (Presentation, Application, Domain, Infrastructure), design patterns (Hexagonal, DDD, CQRS, EDA), scalability and security strategies, architecture diagrams, and tech decisions.

## 5. Features

- **File**: [ProjectFeatures.md](ProjectFeatures.md)
- **Description**: 12 detailed feature descriptions covering REST API, Kafka event processing, email delivery, SMS delivery, MongoDB persistence, user directory integration, attention tracking, Redis caching, JWT authentication, service registry, DDD architecture, and event publishing.

## 6. APIs

- **File**: [APISchema.md](APISchema.md)
- **Description**: Complete HTTP API endpoint documentation with request/response schemas, parameters, authentication requirements, and code examples.

## 7. Metrics

- **File**: [ProjectMetric.md](ProjectMetric.md)
- **Description**: Performance and business metrics including API response time, notification success rate, cache hit rate, Kafka consumer lag, and uptime.

## 8. Links

- **File**: [ProjectLinks.md](ProjectLinks.md)
- **Description**: GitHub repository links and references to other services in the Cinema Platform ecosystem.

## 9. Media Gallery

- **File**: [MediaGallerySection.md](MediaGallerySection.md)
- **Description**: Architecture diagrams, flow charts, and visual representations of the notification service.

---

## Service Information

| Property | Value |
|----------|-------|
| **Service Name** | notification-service |
| **Framework** | FastAPI |
| **Language** | Python 3.13 |
| **Database** | MongoDB |
| **Cache** | Redis |
| **Message Broker** | Apache Kafka |
| **Channels** | Email (SMTP), SMS (Twilio), Push, In-App |
| **Architecture** | DDD (Hexagonal) |
| **Status** | Active |
| **Documentation Version** | 1.0.0 |
| **Last Updated** | 2026-04-06 |
| **Owner** | Alexis |

---

## Related Services

| Service | Description |
|---------|-------------|
| user-service | User management and authentication |
| wallet-service | Payment and wallet operations |
| catalog-service | Movie and showtime catalog |
| concession-service | Food and beverage orders |
| billboard-service | Cinema billboard/show schedule |

---

## Quick Links

- [README.md](../README.md) - Main service README
- [app/notification/domain/](app/notification/domain/) - Domain layer source
- [app/notification/application/](app/notification/application/) - Application layer source
- [app/notification/infrastructure/](app/notification/infrastructure/) - Infrastructure layer source
- [app/notification/presentation/](app/notification/presentation/) - Presentation layer source
