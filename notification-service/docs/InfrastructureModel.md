# Infrastructure Model

## 1. Deployment Layers (`DeploymentLayer[]`)

### Layer 1 - API Gateway

- **Name**: API Gateway Layer
- **Color**: #4A90E2
- **Components** (`DeploymentComponent[]`):
  - **Component 1**
    - **Name**: Load Balancer
    - **Icon**: server
    - **Description**: Distributes traffic across multiple notification service instances
  - **Component 2**
    - **Name**: SSL Termination
    - **Icon**: shield
    - **Description**: Handles HTTPS certificates and encryption
  - **Component 3**
    - **Name**: Rate Limiter
    - **Icon**: gauge
    - **Description**: SlowAPI rate limiting (60 req/min per IP)

---

### Layer 2 - Application

- **Name**: Application Layer
- **Color**: #50C878
- **Components** (`DeploymentComponent[]`):
  - **Component 1**
    - **Name**: Notification Service
    - **Icon**: server
    - **Description**: FastAPI application running on Uvicorn with async handlers
  - **Component 2**
    - **Name**: Kafka Consumer
    - **Icon**: activity
    - **Description**: Background consumer process for incoming events
  - **Component 3**
    - **Name**: Service Registry Client
    - **Icon**: radio
    - **Description**: Heartbeat client for service discovery

---

### Layer 3 - Data

- **Name**: Data Layer
- **Color**: #FFD700
- **Components** (`DeploymentComponent[]`):
  - **Component 1**
    - **Name**: MongoDB
    - **Icon**: database
    - **Description**: Primary document store for notification history
  - **Component 2**
    - **Name**: Redis
    - **Icon**: cache
    - **Description**: Response caching and session storage
  - **Component 3**
    - **Name**: Kafka Cluster
    - **Icon**: activity
    - **Description**: Event streaming platform for incoming and outgoing events

---

### Layer 4 - External Services

- **Name**: External Services Layer
- **Color**: #9B59B6
- **Components** (`DeploymentComponent[]`):
  - **Component 1**
    - **Name**: SMTP Server
    - **Icon**: mail
    - **Description**: Email delivery via SMTP (Postfix, SendGrid, etc.)
  - **Component 2**
    - **Name**: Twilio API
    - **Icon**: message-circle
    - **Description**: SMS delivery via Twilio REST API
  - **Component 3**
    - **Name**: User Service
    - **Icon**: users
    - **Description**: HTTP client for user directory lookup

---

## 2. Docker Files (`DockerFile[]`)

### Service 1

- **Service**: Notification Service
- **Description**: Multi-stage Docker build for the notification service
- **Content**:
  ```dockerfile
  # Build stage
  FROM python:3.13-slim AS builder
  
  WORKDIR /app
  RUN pip install --no-cache-dir --user -r requirements.txt
  
  # Runtime stage
  FROM python:3.13-slim
  
  WORKDIR /app
  
  COPY --from=builder /root/.local /root/.local
  COPY --from=builder /app /app
  
  ENV PATH=/root/.local:$PATH
  
  EXPOSE 8000
  
  CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
  ```

---

## 3. Cloud Services (`CloudService[]`)

For each service:

- **Name**: MongoDB Atlas (or self-hosted)
- **Purpose**: Document storage for notification history
- **Icon**: database
- **Cost**: Variable (Atlas starter free tier available)

---

- **Name**: Redis Cloud (or self-hosted)
- **Purpose**: Caching layer for improved performance
- **Icon**: cache
- **Cost**: Variable (free tier available)

---

- **Name**: Confluent Cloud (or self-managed Kafka)
- **Purpose**: Event streaming for event-driven notifications
- **Icon**: activity
- **Cost**: Variable (Confluent Cloud free tier available)

---

- **Name**: Twilio
- **Purpose**: SMS notification delivery
- **Icon**: message-circle
- **Cost**: Pay-per-use (~$0.0075 per SMS in US)

---

- **Name**: SMTP Provider (SendGrid, Mailgun, Postmark)
- **Purpose**: Email delivery
- **Icon**: mail
- **Cost**: Variable (free tiers available)

---

## 4. Metrics (`InfrastructureMetric[]`)

For each metric:

- **Label**: CPU Usage
- **Value**: <70%
- **Icon**: cpu
- **Description**: Average CPU utilization across service instances

---

- **Label**: Memory Usage
- **Value**: <512MB
- **Icon**: memory
- **Description**: RAM consumption per container

---

- **Label**: Request Latency (p95)
- **Value**: <100ms
- **Icon**: zap
- **Description**: API response time at 95th percentile

---

- **Label**: MongoDB Query Time
- **Value**: <50ms
- **Icon**: database
- **Description**: Average MongoDB query execution time

---

- **Label**: Kafka Consumer Lag
- **Value**: <1000
- **Icon**: activity
- **Description**: Number of unprocessed messages behind the latest offset

---

- **Label**: Cache Hit Rate
- **Value**: >80%
- **Icon**: cache
- **Description**: Percentage of requests served from Redis cache

---

- **Label**: Notification Success Rate
- **Value**: >95%
- **Icon**: bell
- **Description**: Percentage of notifications successfully delivered

---

- **Label**: Uptime
- **Value**: 99.9%
- **Icon**: activity
- **Description**: Service availability SLA
