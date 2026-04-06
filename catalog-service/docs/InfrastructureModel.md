# Infrastructure Model

## 1. Deployment Layers (`DeploymentLayer[]`)

### Layer 1: Application

- **Name**: "Catalog Service"
- **Color**: "#7ED321"
- **Components** (`DeploymentComponent[]`):
  - **Component 1**
    - **Name**: "FastAPI REST API"
    - **Icon**: "🌐"
    - **Description**: "HTTP endpoints for movies, cinemas, theaters, seats"
  - **Component 2**
    - **Name**: "gRPC Server"
    - **Icon**: "🔗"
    - **Description**: "High-performance gRPC for inter-service queries"
  - **Component 3**
    - **Name**: "JWT Auth Middleware"
    - **Icon**: "🔒"
    - **Description**: "Authentication and role-based access control"

---

### Layer 2: Data

- **Name**: "Data Layer"
- **Color**: "#F5A623"
- **Components** (`DeploymentComponent[]`):
  - **Component 1**
    - **Name**: "PostgreSQL"
    - **Icon**: "🗄️"
    - **Description**: "Primary database for catalog data"
  - **Component 2**
    - **Name**: "Redis"
    - **Icon**: "⚡"
    - **Description**: "Caching layer for frequently accessed queries"

---

### Layer 3: Infrastructure

- **Name**: "Infrastructure"
- **Color**: "#D0021B"
- **Components** (`DeploymentComponent[]`):
  - **Component 1**
    - **Name**: "Docker"
    - **Icon**: "🐳"
    - **Description**: "Containerization"
  - **Component 2**
    - **Name**: "Kafka"
    - **Icon**: "📤"
    - **Description**: "Event streaming (optional)"

---

## 2. Docker Files (`DockerFile[]`)

### Service 1

- **Service**: "catalog-service"
- **Description**: "Catalog microservice Docker configuration"
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
- **Purpose**: "Primary database for movies, cinemas, theaters, seats"
- **Icon**: "🗄️"
- **Cost**: "Pay per usage (~$50/month for small instance)"

---

### Service 2: ElastiCache (Redis)

- **Name**: "Redis 7"
- **Purpose**: "Caching layer for catalog queries"
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

### Metric 2: gRPC Response Time

- **Label**: "gRPC Response Time"
- **Value**: "30ms"
- **Icon**: "🔗"
- **Description**: "Average gRPC response time for catalog queries"

---

### Metric 3: Cache Hit Rate

- **Label**: "Redis Cache Hit Rate"
- **Value**: "85%"
- **Icon**: "⚡"
- **Description**: "Percentage of cache hits for catalog queries"

---

### Metric 4: Database Connections

- **Label**: "Active DB Connections"
- **Value**: "20"
- **Icon**: "🗄️"
- **Description**: "Current number of active PostgreSQL connections"

---

### Metric 5: QPS

- **Label**: "Queries Per Second"
- **Value**: "10000"
- **Icon**: "📊"
- **Description**: "Peak queries per second"

---

### Metric 6: Uptime

- **Label**: "Service Uptime"
- **Value**: "99.9%"
- **Icon**: "🟢"
- **Description**: "Monthly service availability"

---

### Metric 7: Movies Count

- **Label**: "Total Movies"
- **Value**: "500"
- **Icon**: "🎬"
- **Description**: "Number of movies in catalog"

---

### Metric 8: Cinemas Count

- **Label**: "Total Cinemas"
- **Value**: "50"
- **Icon**: "🏠"
- **Description**: "Number of cinema locations"

---

## 5. Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| API_VERSION | No | "2.0.0" | API version |
| DEBUG_MODE | No | false | Debug mode |
| SERVICE_NAME | No | "catalog-service" | Service name |
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
| GRPC_HOST | No | "0.0.0.0" | gRPC host |
| GRPC_PORT | No | 50055 | gRPC port |
| KAFKA_ENABLED | No | false | Enable Kafka |
| KAFKA_BOOTSTRAP_SERVERS | No | "localhost:9092" | Kafka servers |
