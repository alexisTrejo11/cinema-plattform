# Infrastructure Model

## 1. Deployment Layers (`DeploymentLayer[]`)

### Layer 1: Application Layer

- **Name**: Application Layer
- **Color**: #4CAF50
- **Components** (`DeploymentComponent[]`):
  - **Component 1**
    - **Name**: "ticket-service (FastAPI)"
    - **Icon**: "server"
    - **Description**: "Main FastAPI application handling REST API, gRPC, and Kafka consumers"
  - **Component 2**
    - **Name**: "ticket-service-grpc"
    - **Icon**: "server"
    - **Description**: "Dedicated gRPC server process for TicketService.Ping"
  - **Component 3**
    - **Name**: "nginx"
    - **Icon**: "load-balancer"
    - **Description**: "Load balancer distributing traffic across multiple service instances"

---

### Layer 2: Data Layer

- **Name**: Data Layer
- **Color**: #9C27B0
- **Components** (`DeploymentComponent[]`):
  - **Component 1**
    - **Name**: "PostgreSQL 16"
    - **Icon**: "database"
    - **Description**: "Primary transactional database for tickets and showtime seats"
  - **Component 2**
    - **Name**: "MongoDB 7"
    - **Icon**: "database"
    - **Description**: "Read-optimized replica storage for showtimes, cinemas, theaters"
  - **Component 3**
    - **Name**: "Redis 7"
    - **Icon**: "database"
    - **Description**: "Caching layer (configured but not actively used)"

---

### Layer 3: Messaging Layer

- **Name**: Messaging Layer
- **Color**: #FF9800
- **Components** (`DeploymentComponent[]`):
  - **Component 1**
    - **Name**: "Kafka"
    - **Icon**: "stream"
    - **Description**: "Event streaming for billboard and wallet events"
  - **Component 2**
    - **Name**: "DLQ Topics"
    - **Icon**: "alert-triangle"
    - **Description**: "Dead letter queues for failed event processing"

---

## 2. Docker Files (`DockerFile[]`)

### Service 1

- **Service**: "ticket-service"
- **Description**: "Main application Docker container with Python runtime, dependencies, and entrypoint script"
- **Content**:
  ```dockerfile
  FROM python:3.11-slim

  WORKDIR /app

  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt

  COPY . .

  RUN chmod +x docker/docker-entrypoint.sh

  EXPOSE 8000 50055

  ENTRYPOINT ["/app/docker/docker-entrypoint.sh"]
  ```

---

### Service 2

- **Service**: "nginx"
- **Description**: "Load balancer configuration for distributing traffic across service instances"
- **Content**:
  ```nginx
  upstream ticket_service {
      server app-1:8000;
      server app-2:8000;
      server app-3:8000;
  }

  server {
      listen 80;

      location / {
          proxy_pass http://ticket_service;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
      }
  }
  ```

---

## 3. Cloud Services (`CloudService[]`)

For each service:

- **Name**: "Local Docker Compose"
- **Purpose**: "Development and local testing environment"
- **Icon**: "docker"
- **Cost**: "N/A (local)"

---

- **Name**: "PostgreSQL"
- **Purpose**: "Managed database for ticket transactions"
- **Icon**: "database"
- **Cost**: "~$50/month (managed instance)"

---

- **Name**: "MongoDB Atlas (recommended for prod)"
- **Purpose**: "Managed MongoDB for showtime replication"
- **Icon**: "database"
- **Cost**: "~$60/month (M10 cluster)"

---

- **Name**: "Redis Cloud (recommended for prod)"
- **Purpose**: "Managed Redis for caching"
- **Icon**: "database"
- **Cost**: "~$30/month (100MB instance)"

---

- **Name**: "Confluent Cloud or MSK (recommended for prod)"
- **Purpose**: "Managed Kafka for event streaming"
- **Icon**: "stream"
- **Cost**: "~$100/month (basic cluster)"

---

## 4. Metrics (`InfrastructureMetric[]`)

For each metric:

- **Label**: "Container Instances"
- **Value**: "3"
- **Icon**: "server"
- **Description**: "Number of running ticket-service containers"

---

- **Label**: "Database Connections"
- **Value**: "10-30"
- **Icon**: "git-branch"
- **Description**: "PostgreSQL connection pool size (pool_size + max_overflow)"

---

- **Label**: "Kafka Consumer Lag"
- **Value**: "<1000"
- **Icon**: "activity"
- **Description**: "Target consumer lag for billboard events processing"

---

- **Label**: "API Response Time (p95)"
- **Value**: "<200ms"
- **Icon**: "clock"
- **Description**: "95th percentile API response time target"

---

- **Label**: "Service Uptime"
- **Value**: "99.95%"
- **Icon**: "check-circle"
- **Description**: "Target monthly uptime SLA"
