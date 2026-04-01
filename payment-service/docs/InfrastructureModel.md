# Infrastructure Model

## 1. Container Orchestration (`ContainerOrchestration`)

- **Type**: "Docker Compose"
- **Description**: "Container orchestration using Docker Compose for local development and single-node deployment"
- **Components** (`ContainerComponent[]`):

### Container 1: Payment Service

- **Name**: "payment-service"
- **Image**: "payment-service:latest"
- **Port**: 8000
- **Environment Variables**:
  - POSTGRES_USER
  - POSTGRES_PASSWORD
  - POSTGRES_HOST
  - POSTGRES_PORT
  - POSTGRES_DB
  - REDIS_URL
  - JWT_SECRET_KEY
  - JWT_ALGORITHM
  - KAFKA_ENABLED
  - KAFKA_BOOTSTRAP_SERVERS
- **Dependencies**: postgres, redis, kafka (optional)
- **Health Check**: "GET /health"

---

### Container 2: PostgreSQL

- **Name**: "postgres"
- **Image**: "postgres:15"
- **Port**: 5432
- **Environment Variables**:
  - POSTGRES_USER
  - POSTGRES_PASSWORD
  - POSTGRES_DB
- **Volumes**: "postgres_data:/var/lib/postgresql/data"
- **Health Check**: "pg_isready"

---

### Container 3: Redis

- **Name**: "redis"
- **Image**: "redis:7-alpine"
- **Port**: 6379
- **Volumes**: "redis_data:/data"
- **Health Check**: "redis-cli ping"

---

### Container 4: Zookeeper

- **Name**: "zookeeper"
- **Image**: "confluentinc/cp-zookeeper:7.5.0"
- **Port**: 2181
- **Environment Variables**:
  - ZOOKEEPER_CLIENT_PORT
  - ZOOKEEPER_TICK_TIME

---

### Container 5: Kafka

- **Name**: "kafka"
- **Image**: "confluentinc/cp-kafka:7.5.0"
- **Port**: 9092
- **Environment Variables**:
  - KAFKA_BROKER_ID
  - KAFKA_ZOOKEEPER_CONNECT
  - KAFKA_ADVERTISED_LISTENERS
- **Dependencies**: zookeeper
- **Health Check**: "kafka-topics --bootstrap-server localhost:9092 --list"

---

## 2. Kubernetes Configuration (`KubernetesConfig`)

- **Namespace**: "cinema-platform"
- **Replicas**: 3
- **Resources**:
  - **Requests**: Memory: "256Mi", CPU: "250m"
  - **Limits**: Memory: "512Mi", CPU: "500m"

### Deployment Spec

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: payment-service
  template:
    spec:
      containers:
        - name: payment-service
          image: cinema-api/payment-service:latest
          ports:
            - containerPort: 8000
          envFrom:
            - secretRef:
                name: payment-secrets
```

---

## 3. Cloud Services (`CloudService[]`)

### Service 1: PostgreSQL (AWS RDS)

- **Provider**: "AWS"
- **Service**: "RDS PostgreSQL 15"
- **Instance**: "db.t3.medium"
- **Storage**: "100GB gp3"
- **Multi-AZ**: true
- **Backup Retention**: 7 days

---

### Service 2: ElastiCache (Redis)

- **Provider**: "AWS"
- **Service**: "ElastiCache Redis 7"
- **Node Type**: "cache.t3.micro"
- **Cluster Mode**: Disabled
- **Replicas**: 2

---

### Service 3: Amazon MSK (Kafka)

- **Provider**: "AWS"
- **Service**: "Amazon MSK"
- **Kafka Version**: "3.5.1"
- **Brokers**: 3
- **Storage**: 100GB per broker

---

## 4. Database Schema (`DatabaseSchema`)

### Table: payments

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR(36) | PRIMARY KEY | Payment UUID |
| user_id | VARCHAR(36) | NOT NULL | User UUID |
| amount | DECIMAL(10,2) | NOT NULL | Payment amount |
| currency | VARCHAR(3) | NOT NULL | Currency code |
| refunded_amount | DECIMAL(10,2) | DEFAULT 0 | Amount refunded |
| payment_method | VARCHAR(50) | NOT NULL | Payment method |
| payment_type | VARCHAR(50) | NOT NULL | Payment type |
| status | VARCHAR(20) | NOT NULL | Payment status |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update |
| completed_at | TIMESTAMP | NULL | Completion time |
| expires_at | TIMESTAMP | NULL | Expiry time |
| stripe_payment_intent_id | VARCHAR(255) | NULL | Stripe PI ID |
| metadata | JSONB | NULL | Additional data |
| failure_reason | TEXT | NULL | Failure reason |
| refund_reasons | JSONB | NULL | Refund reasons |

---

### Table: payment_methods

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR(36) | PRIMARY KEY | Method UUID |
| name | VARCHAR(255) | NOT NULL | Display name |
| provider | VARCHAR(255) | NOT NULL | Payment provider |
| type | VARCHAR(255) | NOT NULL | Method type |
| stripe_code | VARCHAR(255) | NOT NULL | Stripe code |
| is_active | BOOLEAN | DEFAULT TRUE | Active status |
| min_amount | DECIMAL(10,2) | NOT NULL | Min amount |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update |
| deleted_at | TIMESTAMP | NULL | Soft delete |

---

### Table: stored_payment_methods

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR(36) | PRIMARY KEY | Stored method UUID |
| user_id | VARCHAR(36) | NOT NULL, INDEX | User UUID |
| payment_method_id | VARCHAR(255) | NOT NULL | Stripe PM ID |
| provider_token | VARCHAR(255) | NOT NULL | Token |
| card | JSONB | NULL | Card data |
| is_default | BOOLEAN | DEFAULT FALSE | Default flag |
| created_at | TIMESTAMP | DEFAULT NOW() | Creation time |
| updated_at | TIMESTAMP | DEFAULT NOW() | Last update |
| deleted_at | TIMESTAMP | NULL | Soft delete |

---

## 5. Environment Variables (`EnvironmentVariable[]`)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| API_VERSION | No | "2.0.0" | API version |
| DEBUG_MODE | No | false | Debug mode |
| SERVICE_NAME | No | "payment-service" | Service name |
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
| JWT_AUDIENCE | No | null | JWT audience |
| JWT_ISSUER | No | null | JWT issuer |
| GRPC_HOST | No | "0.0.0.0" | gRPC host |
| GRPC_PORT | No | 50055 | gRPC port |
| KAFKA_ENABLED | No | false | Enable Kafka |
| KAFKA_BOOTSTRAP_SERVERS | No | "localhost:9092" | Kafka servers |
| KAFKA_CLIENT_ID | No | "ticket-service" | Kafka client ID |
| KAFKA_TOPIC_PAYMENT_EVENTS | No | "payment.events" | Payment events topic |
| KAFKA_CONSUMER_ENABLED | No | false | Enable Kafka consumer |
| REGISTRY_ENABLED | No | false | Enable service registry |

---

## 6. Infrastructure Metrics (`InfrastructureMetric[]`)

### Metric 1: Pod Count

- **Label**: "Pod Count"
- **Value**: 3
- **Unit**: "pods"
- **Description**: "Number of payment-service pods"
- **Icon**: "📦"
- **Trend**: `stable`

---

### Metric 2: CPU Usage

- **Label**: "CPU Usage"
- **Value**: "45%"
- **Unit**: "%"
- **Description**: "Average CPU usage across pods"
- **Icon**: "⚙️"
- **Trend**: `stable`

---

### Metric 3: Memory Usage

- **Label**: "Memory Usage"
- **Value**: "128Mi"
- **Unit**: "Mi"
- **Description**: "Average memory usage per pod"
- **Icon**: "💾"
- **Trend**: `stable`

---

### Metric 4: Database Connections

- **Label**: "DB Connections"
- **Value**: 15
- **Unit**: "connections"
- **Description**: "Active PostgreSQL connections"
- **Icon**: "🗄️"
- **Trend**: `stable`

---

### Metric 5: Kafka Lag

- **Label**: "Kafka Consumer Lag"
- **Value**: "< 100"
- **Unit**: "messages"
- **Description**: "Consumer lag for payment events"
- **Icon**: "📤"
- **Trend**: `stable`

---

### Metric 6: API Request Rate

- **Label**: "API Request Rate"
- **Value**: "500 RPS"
- **Unit**: "RPS"
- **Description**: "Requests per second"
- **Icon**: "📊"
- **Trend**: `up`

---

### Metric 7: Error Rate

- **Label**: "Error Rate"
- **Value**: "0.1%"
- **Unit**: "%"
- **Description**: "Percentage of 5xx errors"
- **Icon**: "❌"
- **Trend**: `down`

---

### Metric 8: P95 Latency

- **Label**: "P95 Latency"
- **Value**: "150ms"
- **Unit**: "ms"
- **Description**: "95th percentile response time"
- **Icon**: "⚡"
- **Trend**: `stable`
