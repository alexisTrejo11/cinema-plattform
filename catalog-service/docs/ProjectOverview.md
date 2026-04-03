# Project Overview

## 1. Problem Statement (`OverviewProblemStatement`)

- **Problem Title**: Cinema Catalog Management
- **Problem Description**:
  - Need for centralized management of cinema, theater, and movie data across the platform
  - Support for multiple cinema locations with different amenities and features
  - Theater management with seat configurations and capacity rules
  - Movie catalog with showtimes and exhibition periods
  - Need for gRPC inter-service communication with ticket service
- **Problem List**:
  - Complex entity relationships (cinema → theaters → seats)
  - Business rule validation (theater capacity by type)
  - Soft delete and restore functionality
  - Role-based access for admin operations

---

## 2. Solution (`OverviewSolution`)

- **Solution Title**: Clean Architecture Catalog Microservice
- **Solution List** (array of `Solution`):
  - **Solution 1**
    - **Title**: Multi-Domain Architecture
    - **Description**: Separate domains for Movies, Cinemas, Theaters with clear boundaries and shared infrastructure
  - **Solution 2**
    - **Title**: Business Rule Validation
    - **Description**: Domain entities implement business rules (theater capacity validation by type, seat type management)
  - **Solution 3**
    - **Title**: gRPC Server
    - **Description**: Built-in gRPC server for real-time catalog queries from other services
  - **Solution 4**
    - **Title**: Soft Delete Pattern
    - **Description**: All entities support soft delete with restore capability for audit trail

---

## 3. Key Metrics (`OverviewKeyMetrics`)

- **Metrics Title**: Catalog Service Key Metrics
- **Metrics List** (strings):
  - API Response Time: < 150ms (p95)
  - Movie Queries: 10,000 QPS peak
  - Cinema Lookup: < 50ms with caching
  - gRPC Response Time: < 30ms

See also [ProjectMetric.md](ProjectMetric.md) for richer metrics.

---

## 4. Cover Image (`ProjectCoverImage`, optional)

- **URL**: ""
- **Alt**: "Catalog Service Architecture"
- **Credit** (optional): "Cinema Platform Team"

---

## 5. Links (`ProjectLinks`)

See [ProjectLinks.md](ProjectLinks.md).

- **GitHub**: https://github.com/anomalyco/cinema-platform/catalog-service
- **Demo**: ""
- **Documentation**: http://localhost:8000/docs
- **Docker Hub**: ""

---

## 6. Media Gallery Section (`MediaGallerySection`)

See [MediaGallerySection.md](MediaGallerySection.md).

- **Title**: "Catalog Service Screenshots"
- **Description**: "Screenshots and diagrams of the catalog service architecture and API documentation"
- **Items**: list of media items (see `ProjectMediaItem` in MediaGallerySection.md).

---

## 7. Media Items (`ProjectMediaItem[]`)

For each media item:

- **Type**: `diagram`
- **URL**: ""
- **Thumbnail** (optional): ""
- **Title**: "Domain Structure"
- **Description**: "Clean Architecture diagram showing Movies, Cinemas, Theaters domains"
- **Alt** (optional): "Domain Structure Diagram"
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
