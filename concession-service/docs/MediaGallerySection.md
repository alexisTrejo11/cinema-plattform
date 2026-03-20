# Media Gallery

## Section: Project Visuals

- **Title**: "Cinema Billboard Service Media Gallery"
- **Description** (optional): "Visual documentation showcasing the API architecture, database schema, and key features of the cinema management platform"

---

## Items (`ProjectMediaItem[]`)

### Media Item 1: Architecture Diagram

- **Type**: `image`
- **URL**: "/assets/architecture-diagram.png" (placeholder)
- **Thumbnail** (optional): "/assets/thumbnails/architecture-thumb.png"
- **Title**: "Domain-Driven Design Architecture"
- **Description**: "Multi-layer DDD architecture showing API Gateway, Application Layer, Domain Layer, and Infrastructure Layer with PostgreSQL and Redis"
- **Alt** (optional): "Billboard Service DDD Architecture Diagram"
- **Category** (optional): `architecture`

---

### Media Item 2: Database Schema

- **Type**: `image`
- **URL**: "/assets/database-schema.png" (placeholder)
- **Thumbnail** (optional): "/assets/thumbnails/db-schema-thumb.png"
- **Title**: "Database Entity-Relationship Diagram"
- **Description**: "PostgreSQL schema showing relationships between Cinemas, Movies, Theaters, Seats, and Showtimes tables with foreign keys and indexes"
- **Alt** (optional): "Billboard Service Database Schema ERD"
- **Category** (optional): `diagram`

---

### Media Item 3: API Documentation Screenshot

- **Type**: `image`
- **URL**: "/assets/swagger-ui.png" (placeholder)
- **Thumbnail** (optional): "/assets/thumbnails/swagger-thumb.png"
- **Title**: "FastAPI Swagger UI"
- **Description**: "Auto-generated interactive API documentation with 30+ endpoints across Cinema, Movie, Theater, and Showtime domains"
- **Alt** (optional): "FastAPI Swagger Documentation Interface"
- **Category** (optional): `screenshot`

---

### Media Item 4: API Response Example

- **Type**: `image`
- **URL**: "/assets/api-response.png" (placeholder)
- **Thumbnail** (optional): "/assets/thumbnails/api-response-thumb.png"
- **Title**: "Paginated Cinema Response"
- **Description**: "Example JSON response showing paginated cinema list with metadata, amenities, and location data"
- **Alt** (optional): "API JSON Response Example"
- **Category** (optional): `screenshot`

---

### Media Item 5: Docker Compose Setup

- **Type**: `image`
- **URL**: "/assets/docker-compose.png" (placeholder)
- \*\*Thumbnail" (optional): "/assets/thumbnails/docker-thumb.png"
- **Title**: "Docker Compose Architecture"
- **Description**: "Multi-container setup with FastAPI app, PostgreSQL 16, and Redis 7 with health checks and volume persistence"
- **Alt** (optional): "Docker Compose Service Diagram"
- **Category** (optional): `diagram`

---

### Media Item 6: Rate Limiting Demo

- **Type**: `video`
- **URL**: "/assets/rate-limiting-demo.mp4" (placeholder)
- **Thumbnail** (optional): "/assets/thumbnails/rate-limit-thumb.png"
- **Title**: "Rate Limiting in Action"
- **Description**: "Demonstration of SlowAPI rate limiter blocking excessive requests with 429 Too Many Requests response"
- **Alt** (optional): "Rate Limiting Feature Demo Video"
- \*\*Category" (optional): `demo`

---

### Media Item 7: JWT Authentication Flow

- **Type**: `image`
- **URL**: "/assets/jwt-flow.png" (placeholder)
- \*\*Thumbnail" (optional): "/assets/thumbnails/jwt-thumb.png"
- **Title**: "JWT Authentication Flow Diagram"
- **Description**: "Step-by-step authentication flow from token receipt to user context injection and role-based authorization"
- \*\*Alt" (optional): "JWT Authentication Sequence Diagram"
- \*\*Category" (optional): `diagram`

---

### Media Item 8: Cache Performance Metrics

- **Type**: `image`
- **URL**: "/assets/cache-metrics.png" (placeholder)
- \*\*Thumbnail" (optional): "/assets/thumbnails/cache-metrics-thumb.png"
- **Title**: "Redis Cache Performance Dashboard"
- **Description**: "Real-time metrics showing 85% cache hit rate and sub-50ms response times for cached endpoints"
- \*\*Alt" (optional): "Cache Performance Metrics Dashboard"
- \*\*Category" (optional): `screenshot`

---

### Media Item 9: Showtime Lifecycle States

- **Type**: `image`
- **URL**: "/assets/showtime-states.png" (placeholder)
- \*\*Thumbnail" (optional): "/assets/thumbnails/showtime-states-thumb.png"
- **Title**: "Showtime Status State Machine"
- **Description**: "State transition diagram showing showtime lifecycle: DRAFT → UPCOMING → IN_PROGRESS → COMPLETED/CANCELLED"
- **Alt** (optional): "Showtime Status State Machine Diagram"
- \*\*Category" (optional): `diagram`

---

### Media Item 10: Health Check Dashboard

- **Type**: `image`
- **URL**: "/assets/health-dashboard.png" (placeholder)
- \*\*Thumbnail" (optional): "/assets/thumbnails/health-thumb.png"
- **Title**: "Service Health Monitoring"
- **Description**: "Docker health check dashboard showing live status of FastAPI app, PostgreSQL, and Redis services"
- \*\*Alt" (optional): "Health Check Monitoring Dashboard"
- \*\*Category" (optional): `screenshot`

---

## Notes for Media Generation

- Architecture diagrams can be created using tools like Draw.io, Excalidraw, or Mermaid
- Database schema diagrams can be generated using DBeaver, pgAdmin, or dbdiagram.io
- API screenshots should be taken from the live Swagger UI at `/docs`
- Docker diagrams can show container relationships and port mappings
- Performance metrics can be captured from monitoring tools like Grafana or custom dashboards
- State machine diagrams can be created with Mermaid, PlantUML, or similar tools
