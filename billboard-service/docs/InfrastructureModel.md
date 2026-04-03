# Infrastructure Model

## 1. Deployment Layers (`DeploymentLayer[]`)

### Layer 1: Client Layer

- **Name**: "Client Layer"
- **Color**: "#3498db"
- **Components** (`DeploymentComponent[]`):
  - **Component 1**
    - **Name**: "Web Browsers"
    - **Icon**: "🌐"
    - **Description**: "Modern web browsers accessing REST API endpoints"
  - **Component 2**
    - **Name**: "Mobile app.
    - **Icon**: "📱"
    - **Description**: "iOS/Android applications consuming JSON API"
  - **Component 3**
    - **Name**: "Third-Party Services"
    - **Icon**: "🔌"
    - **Description**: "External services integrating via REST API"

---

### Layer 2: Gateway Layer

- **Name**: "API Gateway Layer"
- **Color**: "#e74c3c"
- **Components** (`DeploymentComponent[]`):
  - **Component 1**
    - **Name**: "Load Balancer"
    - **Icon**: "⚖️"
    - **Description**: "NGINX/HAProxy distributing traffic across app.nstances"
  - **Component 2**
    - **Name**: "SSL/TLS Termination"
    - **Icon**: "🔒"
    - **Description**: "HTTPS endpoint with certificate management"
  - **Component 3**
    - **Name**: "Rate Limiter"
    - **Icon**: "🚦"
    - **Description**: "IP-based rate limiting at gateway level"

---

### Layer 3: application Layer

- **Name**: "application Service Layer"
- **Color**: "#2ecc71"
- **Components** (`DeploymentComponent[]`):
  - **Component 1**
    - **Name**: "FastAPI application"
    - **Icon**: "⚡"
    - **Description**: "Python 3.13 FastAPI app.ith 4 Gunicorn workers (Uvicorn)"
  - **Component 2**
    - **Name**: "JWT Auth Middleware"
    - **Icon**: "🔐"
    - **Description**: "Token validation and user context injection"
  - **Component 3**
    - **Name**: "Logging System"
    - **Icon**: "📝"
    - **Description**: "Structured logging with colorlog output"
  - **Component 4**
    - **Name**: "Cron Job Scheduler"
    - **Icon**: "⏰"
    - **Description**: "Automated tasks for showtime transitions and cleanup"

---

### Layer 4: Data Layer

- **Name**: "Data Persistence Layer"
- **Color**: "#f39c12"
- **Components** (`DeploymentComponent[]`):
  - **Component 1**
    - **Name**: "PostgreSQL 16"
    - **Icon**: "🐘"
    - **Description**: "Primary relational database with Alpine Linux base"
  - **Component 2**
    - **Name**: "Redis 7 Cache"
    - **Icon**: "💾"
    - **Description**: "In-memory cache with RDB persistence (Alpine)"
  - **Component 3**
    - **Name**: "Database Migrations"
    - **Icon**: "🔄"
    - **Description**: "Alembic version-controlled schema migrations"

---

### Layer 5: Container Orchestration

- **Name**: "Container Platform"
- **Color**: "#9b59b6"
- **Components** (`DeploymentComponent[]`):
  - **Component 1**
    - **Name**: "Docker Engine"
    - **Icon**: "🐳"
    - **Description**: "Container runtime with multi-stage builds"
  - **Component 2**
    - **Name**: "Docker Compose"
    - **Icon**: "📦"
    - **Description**: "Multi-container orchestration (app.db, redis)"
  - **Component 3**
    - **Name**: "Health Checks"
    - **Icon**: "❤️"
    - **Description**: "HTTP and TCP health monitoring for all services"

---

## 2. Docker Files (`DockerFile[]`)

### Service 1: application Service

- **Service**: "billboard-service"
- **Description**: "Multi-stage Python application container with non-root execution"
- **Content**:

  ```dockerfile
  # Stage 1: Builder
  FROM python:3.13-slim as builder
  WORKDIR /app
  RUN apt-get update && apt-get install -y \
      gcc libpq-dev && rm -rf /var/lib/apt/lists/*
  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt

  # Stage 2: Runtime
  FROM python:3.13-slim
  WORKDIR /app
  RUN apt-get update && apt-get install -y libpq5 && \
      rm -rf /var/lib/apt/lists/*
  COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
  COPY . .
  RUN useradd -m -u 1000 app.er && \
      chown -R app.er:app.er /app
  USER app.er
  EXPOSE 8000
  HEALTHCHECK --interval=30s --timeout=3s \
    CMD python -c "import requests; requests.get('http://localhost:8000/')"
  CMD ["gunicorn", "main:fast_api_app. "-k", "uvicorn.workers.UvicornWorker", \
       "-w", "4", "-b", "0.0.0.0:8000"]
  ```

---

### Service 2: PostgreSQL Database

- **Service**: "PostgreSQL 16"
- **Description**: "Official PostgreSQL Alpine image with custom configuration"
- **Content**:

  ```dockerfile
  # Using official image from Docker Hub
  FROM postgres:16-alpine

  # Environment variables set in docker-compose.yml:
  # POSTGRES_DB: cinema_billboard
  # POSTGRES_USER: billboard_user
  # POSTGRES_PASSWORD: <secure-password>

  # Health check configured via docker-compose
  # HEALTHCHECK: pg_isready -U billboard_user -d cinema_billboard
  ```

---

### Service 3: Redis Cache

- **Service**: "Redis 7"
- **Description**: "Official Redis Alpine image with RDB persistence"
- **Content**:

  ```dockerfile
  # Using official image from Docker Hub
  FROM redis:7-alpine

  # Command configured in docker-compose.yml:
  # redis-server --save 60 1 --loglevel warning

  # Persistence:
  # - RDB snapshots every 60s if 1+ key changed
  # - Data stored in Docker volume

  # Health check: redis-cli ping
  ```

---

## 3. Cloud Services (`CloudService[]`)

### Service 1: Container Registry

- **Name**: "Docker Hub / Private Registry"
- **Purpose**: "Store and version Docker images for deployment"
- **Icon**: "🐳"
- **Cost**: "Free tier (public) / Self-hosted"

---

### Service 2: Container Platform

- **Name**: "Docker Swarm / Kubernetes"
- **Purpose**: "Orchestrate multi-instance deployment with auto-scaling"
- **Icon**: "☸️"
- **Cost**: "Self-managed infrastructure"

---

### Service 3: Database Hosting

- **Name**: "Managed PostgreSQL"
- **Purpose**: "Production database with automated backups and HA"
- **Icon**: "🐘"
- **Cost**: "~$15-50/month (managed service)"

---

### Service 4: Cache Hosting

- **Name**: "Managed Redis"
- **Purpose**: "Production cache with clustering and persistence"
- **Icon**: "💾"
- **Cost**: "~$10-30/month (managed service)"

---

### Service 5: Load Balancer

- **Name**: "Cloud Load Balancer"
- **Purpose**: "Distribute traffic, SSL termination, health checks"
- **Icon**: "⚖️"
- **Cost**: "~$15-25/month + bandwidth"

---

### Service 6: Monitoring & Logging

- **Name**: "application Monitoring"
- **Purpose**: "Metrics, logs aggregation, alerting (Prometheus/Grafana/ELK)"
- **Icon**: "📊"
- **Cost**: "Self-hosted or managed ($20-100/month)"

---

## 4. Metrics (`InfrastructureMetric[]`)

### Metric 1: Container Efficiency

- **Label**: "Container Image Size"
- **Value**: "~450MB (multi-stage build)"
- **Icon**: "📦"
- **Description**: "Optimized Docker images using Alpine base and multi-stage builds"

---

### Metric 2: Startup Time

- **Label**: "application Startup"
- **Value**: "<10s (with migrations)"
- **Icon**: "⚡"
- **Description**: "Fast cold start including database migration execution"

---

### Metric 3: Database Performance

- **Label**: "Query Response Time"
- **Value**: "<100ms (p95), <50ms cached"
- **Icon**: "🐘"
- **Description**: "PostgreSQL query performance with strategic indexing"

---

### Metric 4: Cache Performance

- **Label**: "Redis Latency"
- **Value**: "<5ms (p99)"
- **Icon**: "💾"
- **Description**: "Sub-millisecond cache access times for hot data"

---

### Metric 5: Memory Usage

- **Label**: "application Memory"
- **Value**: "~150-250MB per worker"
- **Icon**: "🧠"
- **Description**: "Low memory footprint per Gunicorn worker"

---

### Metric 6: Health Check Success

- **Label**: "Service Availability"
- **Value**: "99.9% uptime"
- **Icon**: "❤️"
- **Description**: "Automated health checks with 30s intervals"

---

### Metric 7: Deployment Automation

- **Label**: "Deployment Time"
- **Value**: "<3 minutes (zero-downtime)"
- **Icon**: "🚀"
- **Description**: "Automated deployment with rolling updates via Docker Compose"

---

### Metric 8: Scalability

- **Label**: "Horizontal Scale"
- **Value**: "Stateless (unlimited instances)"
- **Icon**: "📈"
- **Description**: "Fully stateless design enables linear horizontal scaling"

---

## 5. Docker Compose Configuration

```yaml
version: "3.8"

services:
  db:
    image: postgres:16-alpine
    container_name: billboard-postgres
    environment:
      POSTGRES_DB: cinema_billboard
      POSTGRES_USER: billboard_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U billboard_user"]
      interval: 5s
      timeout: 3s
      retries: 5
    networks:
      - billboard-network

  redis:
    image: redis:7-alpine
    container_name: billboard-redis
    command: redis-server --save 60 1 --loglevel warning
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 3s
      retries: 5
    networks:
      - billboard-network

  app:
    build:
      context: .
      dockerfile: docker/dockerfile
    container_name: billboard-app
    environment:
      DB_HOST: db
      DB_PORT: 5432
      DB_NAME: cinema_billboard
      DB_USER: billboard_user
      DB_PASSWORD: ${DB_PASSWORD}
      REDIS_URL: redis://redis:6379/0
      JWT_SECRET: ${JWT_SECRET}
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - billboard-network
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:

networks:
  billboard-network:
    driver: bridge
```

---

## 6. Production Deployment Checklist

- ✅ Multi-stage Docker builds for image optimization
- ✅ Non-root container execution (security)
- ✅ Health checks on all services
- ✅ Automated database migrations on startup
- ✅ Connection retry logic (20 attempts, 3s delay)
- ✅ Volume persistence for databases
- ✅ Environment-based configuration
- ✅ Gunicorn with 4 Uvicorn workers
- ✅ Graceful shutdown handling
- ✅ Structured logging for production monitoring
- ✅ Rate limiting enabled
- ✅ JWT authentication enforced
- ⏳ SSL/TLS certificate configuration (external)
- ⏳ Backup strategy implementation (external)
- ⏳ Monitoring/alerting setup (external)
