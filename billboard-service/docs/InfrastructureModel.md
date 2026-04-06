# Infrastructure Model

## 1. Deployment Layers (`DeploymentLayer[]`)

### Layer 1: Application

- **Name**: "Billboard Service"
- **Color**: "#7ED321"
- **Components** (`DeploymentComponent[]`):
  - **Component 1**
    - **Name**: "FastAPI REST API"
    - **Icon**: "🌐"
    - **Description**: "HTTP endpoints for showtime management"
  - **Component 2**
    - **Name**: "JWT Auth Middleware"
    - **Icon**: "🔒"
    - **Description**: "Authentication and role-based access control"
  - **Component 3**
    - **Name**: "Rate Limiting"
    - **Icon**: "🚦"
    - **Description**: "SlowAPI for abuse protection"

---

### Layer 2: Data

- **Name**: "Data Layer"
- **Color**: "#F5A623"
- **Components** (`DeploymentComponent[]`):
  - **Component 1**
    - **Name**: "PostgreSQL"
    - **Icon**: "🗄️"
    - **Description**: "Primary database for showtimes and seats"
  - **Component 2**
    - **Name**: "Redis"
    - **Icon**: "⚡"
    - **Description**: "Caching layer for frequently accessed queries"

---

### Layer 3: Integration

- **Name**: "Integration Layer"
- **Color**: "#D0021B"
- **Components** (`DeploymentComponent[]`):
  - **Component 1**
    - **Name**: "gRPC Clients"
    - **Icon**: "🔗"
    - **Description**: "Connections to catalog and payment services"
  - **Component 2**
    - **Name**: "Kafka"
    - **Icon**: "📤"
    - **Description**: "Event publishing (optional)"

---

### Layer 4: Infrastructure

- **Name**: "Infrastructure"
- **Color**: "#4A90E2"
- **Components** (`DeploymentComponent[]`):
  - **Component 1**
    - **Name**: "Docker"
    - **Icon**: "🐳"
    - **Description**: "Containerization"
  - **Component 2**
    - **Name**: "Service Registry"
    - **Icon**: "🔔"
    - **Description**: "Optional service discovery"

---

## 2. Docker Files (`DockerFile[]`)

### Service 1

- **Service**: "billboard-service"
- **Description**: "Billboard microservice Docker configuration"
- **Content**:
  ```dockerfile
  FROM python:3.11-slim
  
  WORKDIR /app
  
  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt
  
  COPY . .
  
  EXPOSE 8000 50055
  
  CMD ["python", "main.py"]
  ```

---

## 3. Cloud Services (`CloudService[]`)

### Service 1: PostgreSQL (AWS RDS)

- **Name**: "PostgreSQL 15"
- **Purpose**: "Primary database for showtimes and seat reservations"
- **Icon**: "🗄️"
- **Cost**: "Pay per usage (~$50/month for small instance)"

---

### Service 2: ElastiCache (Redis)

- **Name**: "Redis 7"
- **Purpose**: "Caching layer for showtime queries and seat availability"
- **Icon**: "⚡"
- **Cost**: "Pay per usage (~$25/month for small instance)"

---

## 4. Metrics (`InfrastructureMetric[]`)

### Metric 1: API Response Time

- **Label**: "API Response Time (p95)"
- **Value**: "150ms"
- **Icon**: "⚡"
- **Description**: "95th percentile response time for REST API"

---

### Metric 2: Seat Reservation Time

- **Label**: "Seat Reservation Time"
- **Value**: "50ms"
- **Icon**: "💺"
- **Description**: "Average time to reserve a seat"

---

### Metric 3: Cache Hit Rate

- **Label**: "Redis Cache Hit Rate"
- **Value**: "85%"
- **Icon**: "⚡"
- **Description**: "Percentage of cache hits for showtime queries"

---

### Metric 4: Database Connections

- **Label**: "Active DB Connections"
- **Value**: "20"
- **Icon**: "🗄️"
- **Description**: "Current number of active PostgreSQL connections"

---

### Metric 5: QPS

- **Label**: "Queries Per Second"
- **Value**: "5000"
- **Icon**: "📊"
- **Description**: "Peak queries per second"

---

### Metric 6: Uptime

- **Label**: "Service Uptime"
- **Value**: "99.9%"
- **Icon**: "🟢"
- **Description**: "Monthly service availability"

---

### Metric 7: Active Showtimes

- **Label**: "Active Showtimes"
- **Value**: "500"
- **Icon**: "📅"
- **Description**: "Number of active/upcoming showtimes"

---

### Metric 8: Concurrent Reservations

- **Label**: "Concurrent Reservations"
- **Value**: "1000+"
- **Icon**: "💺"
- **Description**: "Maximum concurrent seat reservations"

---

## 5. Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| API_VERSION | No | "2.0.0" | API version |
| DEBUG_MODE | No | false | Debug mode |
| SERVICE_NAME | No | "billboard-service" | Service name |
| API_HOST | No | "0.0.0.0" | API host |
| API_PORT | No | 8000 | API port |
| POSTGRES_USER | Yes | - | PostgreSQL user |
| POSTGRES_PASSWORD | Yes | - | PostgreSQL password |
| POSTGRES_HOST | Yes | - | PostgreSQL host |
| POSTGRES_PORT | Yes | 5432 | PostgreSQL port |
| POSTGRES_DB | Yes | - | Database name |
| REDIS_URL | Yes | - | Redis connection URL |
| JWT_SECRET_KEY | Yes | - | JWT secret |
| JWT_ALGORITHM | No | "HS256" | JWT algorithm |
| GRPC_CATALOG_TARGET | No | "localhost:50056" | Catalog service gRPC |
| GRPC_PAYMENT_TARGET | No | "" | Payment service gRPC |
| KAFKA_ENABLED | No | false | Enable Kafka |
| KAFKA_BOOTSTRAP_SERVERS | No | "localhost:9092" | Kafka servers |
| REGISTRY_ENABLED | No | false | Enable service registry |
