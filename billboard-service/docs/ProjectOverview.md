# Project Overview

## 1. Problem Statement (`OverviewProblemStatement`)

- **Problem Title**: Showtime & Seat Management
- **Problem Description**:
  - Need for centralized showtime scheduling and management across cinemas
  - Real-time seat availability tracking and reservation
  - Integration with catalog service for movie/theater data
  - Integration with payment service for ticket purchases
  - Event-driven architecture for seat status updates
- **Problem List**:
  - Complex scheduling with buffer times (cleaning, commercials)
  - Business rule validation (price limits, duration, booking window)
  - Seat reservation with transaction support
  - Showtime lifecycle management (draft, upcoming, completed, cancelled)

---

## 2. Solution (`OverviewSolution`)

- **Solution Title**: Clean Architecture Billboard Microservice
- **Solution List** (array of `Solution`):
  - **Solution 1**
    - **Title**: Showtime Domain Model
    - **Description**: Domain entity with business rules for scheduling, price validation, and lifecycle management
  - **Solution 2**
    - **Title**: Seat Reservation System
    - **Description**: Real-time seat status tracking with take/leave operations and transaction IDs
  - **Solution 3**
    - **Title**: Catalog Service Integration
    - **Description**: gRPC client for fetching movie and theater data from catalog service
  - **Solution 4**
    - **Title**: Service Registry
    - **Description**: Optional service registry for dynamic service discovery and health checks

---

## 3. Key Metrics (`OverviewKeyMetrics`)

- **Metrics Title**: Billboard Service Key Metrics
- **Metrics List** (strings):
  - API Response Time: < 150ms (p95)
  - Seat Reservation: < 50ms
  - Showtime Queries: 5,000 QPS peak
  - Concurrent Reservations: 1,000+

See also [ProjectMetric.md](ProjectMetric.md) for richer metrics.

---

## 4. Cover Image (`ProjectCoverImage`, optional)

- **URL**: ""
- **Alt**: "Billboard Service Architecture"
- **Credit** (optional): "Cinema Platform Team"

---

## 5. Links (`ProjectLinks`)

See [ProjectLinks.md](ProjectLinks.md).

- **GitHub**: https://github.com/anomalyco/cinema-platform/billboard-service
- **Demo**: ""
- **Documentation**: http://localhost:8000/docs
- **Docker Hub**: ""

---

## 6. Media Gallery Section (`MediaGallerySection`)

See [MediaGallerySection.md](MediaGallerySection.md).

- **Title**: "Billboard Service Screenshots"
- **Description**: "Screenshots and diagrams of the billboard service architecture and API documentation"
- **Items**: list of media items (see `ProjectMediaItem` in MediaGallerySection.md).

---

## 7. Media Items (`ProjectMediaItem[]`)

For each media item:

- **Type**: `diagram`
- **URL**: ""
- **Thumbnail** (optional): ""
- **Title**: "Showtime Lifecycle"
- **Description**: "Diagram showing showtime states: draft → upcoming → completed/cancelled"
- **Alt** (optional): "Showtime Lifecycle Diagram"
- **Category** (optional): `diagram`

---

## 8. Metrics (`ProjectMetric[]`)

For each metric see [ProjectMetric.md](ProjectMetric.md):

- **Label**: "API Response Time"
- **Value**: "< 150ms"
- **Description** (optional): "95th percentile response time"
- **Icon** (optional): "⚡"
- **Unit** (optional): "ms"
- **Trend** (optional): `stable`
- **Threshold** (optional): 150
