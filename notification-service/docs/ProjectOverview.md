# Project Overview

## 1. Problem Statement (`OverviewProblemStatement`)

- **Problem Title**: Fragmented Notification System
- **Problem Description**:
  - Each microservice in the Cinema Platform independently manages its own notification delivery
  - No centralized way to track notification status across channels
  - Duplicate notifications when the same event triggers multiple services
  - No consistency in email templates or branding
  - Difficulty in monitoring and debugging notification failures
- **Problem List**:
  - Inconsistent user notification experience across services
  - No unified notification history for users
  - Scattered SMTP/Twilio credentials across multiple services
  - No deduplication mechanism for event-driven notifications
  - Poor operational visibility into notification delivery status

---

## 2. Solution (`OverviewSolution`)

- **Solution Title**: Centralized Notification Service
- **Solution List** (array of `Solution`):
  - **Solution 1**
    - **Title**: Event-Driven Notification Processing
    - **Description**: Kafka consumer that subscribes to events from other microservices (user-service, wallet-service, etc.) and automatically creates and delivers appropriate notifications with deduplication.
  - **Solution 2**
    - **Title**: Multi-Channel Delivery
    - **Description**: Unified API supporting Email (SMTP), SMS (Twilio), Push Notifications, and In-App notifications through a single interface.
  - **Solution 3**
    - **Title**: MongoDB Document Storage
    - **Description**: Async MongoDB persistence for notification history with rich querying capabilities by user, type, status, and channel.
  - **Solution 4**
    - **Title**: Attention Tracking
    - **Description**: Operational monitoring system that flags important/failed notifications requiring human follow-up.

---

## 3. Key Metrics (`OverviewKeyMetrics`)

- **Metrics Title**: Notification Service KPIs
- **Metrics List** (strings):
  - Multi-channel support: EMAIL, SMS, PUSH_NOTIFICATION, IN_APP
  - Event types: 8 predefined notification types
  - Kafka topic consumers: 3 topics (incoming, user events, wallet events)
  - API response time: <100ms (p95)
  - Deduplication: Event-based idempotency

See also [ProjectMetric.md](ProjectMetric.md) for richer metrics.

---

## 4. Cover Image (`ProjectCoverImage`, optional)

- **URL**: ""
- **Alt**: ""
- **Credit** (optional): ""

---

## 5. Links (`ProjectLinks`)

See [ProjectLinks.md](ProjectLinks.md).

- **GitHub**: https://github.com/anomalyco/cinema-plattform
- **Demo**: 
- **Documentation**: notification-service/docs/
- **Docker Hub**: 

---

## 6. Media Gallery Section (`MediaGallerySection`)

See [MediaGallerySection.md](MediaGallerySection.md).

- **Title**: Notification Service Architecture
- **Description**: Overview of the notification service architecture and data flow
- **Items**: list of media items (see `ProjectMediaItem` in MediaGallerySection.md).

---

## 7. Media Items (`ProjectMediaItem[]`)

For each media item:

- **Type**: `image` | `video`
- **URL**: ""
- **Thumbnail** (optional): ""
- **Title**: ""
- **Description**: ""
- **Alt** (optional): ""
- **Category** (optional): `screenshot` | `diagram` | `demo` | `architecture`

---

## 8. Metrics (`ProjectMetric[]`)

For each metric see [ProjectMetric.md](ProjectMetric.md):

- **Label**: "Notifications Processed"
- **Value**: "Real-time"
- **Description** (optional): "Count of notifications processed via API or Kafka"
- **Icon** (optional): "bell"
- **Unit** (optional): "count"
- **Trend** (optional): `stable`
- **Threshold** (optional): 
