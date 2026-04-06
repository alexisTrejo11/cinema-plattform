# Infrastructure Model

## 1. Deployment Layers (`DeploymentLayer[]`)

### Layer 1: Client Layer

- **Name**: "Client Layer"
- **Color**: "#607D8B"
- **Components** (`DeploymentComponent[]`):
  - **Component 1**
    - **Name**: "Web Browser / Mobile App"
    - **Icon**: "monitor"
    - **Description**: "End-user clients accessing the user service through REST API"
  - **Component 2**
    - **Name**: "Internal Microservices"
    - **Icon**: "cpu"
    - **Description**: "Other cinema platform services communicating via gRPC"

---

### Layer 2: Gateway Layer

- **Name**: "Gateway Layer"
- **Color**: "#795548"
- **Components** (`DeploymentComponent[]`):
  - **Component 1**
    - **Name**: "Nginx Load Balancer"
    - **Icon**: "server"
    - **Description**: "HTTP load balancer distributing traffic across application instances"
  - **Component 2**
    - **Name**: "CORS Proxy"
    - **Icon**: "shield"
    - **Description**: "Cross-Origin Resource Sharing configuration for web clients"

---

### Layer 3: Application Layer

- **Name**: "Application Layer"
- **Color**: "#2196F3"
- **Components** (`DeploymentComponent[]`):
  - **Component 1**
    - **Name**: "FastAPI Application Instances"
    - **Icon**: "package"
    - **Description**: "3 uvicorn workers running the user service REST API"
  - **Component 2**
    - **Name**: "gRPC Server"
    - **Icon**: "zap"
    - **Description**: "Dedicated gRPC server for inter-service communication on port 50051"

---

### Layer 4: Data Layer

- **Name**: "Data Layer"
- **Color**: "#336791"
- **Components** (`DeploymentComponent[]`):
  - **Component 1**
    - **Name**: "PostgreSQL 16"
    - **Icon**: "database"
    - **Description**: "Primary relational database for user accounts and profiles"
  - **Component 2**
    - **Name**: "Redis 7 Alpine"
    - **Icon**: "hard-drive"
    - **Description**: "Session token storage and application caching"
  - **Component 3**
    - **Name**: "Kafka Broker"
    - **Icon**: "radio"
    - **Description**: "Event streaming for domain events (optional)"

---

## 2. Docker Files (`DockerFile[]`)

### Service 1: Application Container

- **Service**: "account-service (user-service)"
- **Description**: "Multi-stage Docker build for the FastAPI application with Python 3.13"
- **Content**:
  ```dockerfile
  FROM python:3.13-slim AS builder
  
  ENV PYTHONDONTWRITEBYTECODE=1 \
      PYTHONUNBUFFERED=1 \
      PIP_DISABLE_PIP_VERSION_CHECK=1 \
      PIP_NO_CACHE_DIR=1
  
  WORKDIR /app
  
  RUN apt-get update \
      && apt-get install -y --no-install-recommends build-essential libpq-dev \
      && rm -rf /var/lib/apt/lists/*
  
  COPY requirements.txt .
  
  RUN python -m venv /opt/venv \
      && /opt/venv/bin/pip install --upgrade pip \
      && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt
  
  FROM python:3.13-slim AS runtime
  
  ENV PYTHONDONTWRITEBYTECODE=1 \
      PYTHONUNBUFFERED=1 \
      PATH="/opt/venv/bin:${PATH}"
  
  WORKDIR /app
  
  RUN apt-get update \
      && apt-get install -y --no-install-recommends libpq5 \
      && rm -rf /var/lib/apt/lists/*
  
  COPY --from=builder /opt/venv /opt/venv
  COPY . .
  
  RUN chmod +x /app/docker/docker-entrypoint.sh
  
  RUN addgroup --system app \
      && adduser --system --ingroup app app \
      && chown -R app:app /app
  
  USER app
  
  EXPOSE 8000 50051
  
  HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3)" || exit 1
  
  CMD ["/app/docker/docker-entrypoint.sh", "serve"]
  ```

---

### Service 2: Nginx Container

- **Service**: "nginx"
- **Description**: "Nginx load balancer for distributing traffic to application instances"
- **Content**:
  ```nginx
  # See docker/nginx/nginx.conf for full configuration
  upstream user_backend {
      least_conn;
      server app-1:8000;
      server app-2:8000;
      server app-3:8000;
  }
  
  server {
      listen 80;
      
      location / {
          proxy_pass http://user_backend;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      }
  }
  ```

---

## 3. Cloud Services (`CloudService[]`)

For each service:

- **Name**: "PostgreSQL 16 (Self-Hosted)"
- **Purpose**: "Primary relational database for user accounts and profiles"
- **Icon**: "database"
- **Cost**: "Infrastructure cost (self-hosted)"

---

- **Name**: "Redis 7 (Self-Hosted)"
- **Purpose**: "Session token storage and caching layer"
- **Icon**: "hard-drive"
- **Cost**: "Infrastructure cost (self-hosted)"

---

- **Name**: "Apache Kafka (Optional)"
- **Purpose**: "Domain event streaming for inter-service communication"
- **Icon**: "radio"
- **Cost**: "Infrastructure cost (self-hosted)"

---

- **Name**: "Docker Compose Orchestration"
- **Purpose**: "Container orchestration for local development and deployment"
- **Icon**: "container"
- **Cost**: "Open Source"

---

## 4. Metrics (`InfrastructureMetric[]`)

For each metric:

- **Label**: "Container Instances"
- **Value**: "7"
- **Icon**: "box"
- **Description**: "Total containers: 3 app + 1 gRPC + 1 nginx + 1 redis + 1 postgres"

---

- **Label**: "Application Workers"
- **Value**: "12"
- **Icon**: "cpu"
- **Description**: "4 workers per instance x 3 instances"

---

- **Label**: "Database Connections"
- **Value**: "20"
- **Icon**: "link"
- **Description**: "Connection pool size per application instance"

---

- **Label**: "Session Token TTL"
- **Value**: "7 days"
- **Icon**: "clock"
- **Description**: "Default refresh token expiration time"

---

- **Label**: "Access Token TTL"
- **Value**: "15 minutes"
- **Icon**: "clock"
- **Description**: "JWT access token expiration time"
