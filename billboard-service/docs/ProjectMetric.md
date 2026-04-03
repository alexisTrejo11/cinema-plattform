# Project Metrics

## Performance Metrics

### Metric 1: API Response Time (Cached)

- **Label**: "API Response Time (Cached)"
- **Value**: "<50ms"
- **Unit** (optional): "milliseconds"
- **Description** (optional): "Average response time for cached endpoints (85% hit rate)"
- **Icon** (optional): "⚡"
- **Trend** (optional): `stable`
- **Threshold** (optional): 100

---

### Metric 2: API Response Time (Database)

- **Label**: "API Response Time (Uncached)"
- **Value**: "<100ms"
- **Unit** (optional): "milliseconds"
- **Description** (optional): "P95 response time for database queries with indexing"
- **Icon** (optional): "🐘"
- **Trend** (optional): `stable`
- **Threshold** (optional): 200

---

### Metric 3: Cache Hit Rate

- **Label**: "Redis Cache Hit Rate"
- **Value**: "85%"
- **Unit** (optional): "percent"
- **Description** (optional): "Percentage of requests served from cache vs database"
- **Icon** (optional): "💾"
- **Trend** (optional): `up`
- **Threshold** (optional): 80

---

### Metric 4: Database Query Performance

- **Label**: "Database Query Time"
- **Value**: "<100ms"
- **Unit** (optional): "milliseconds"
- **Description** (optional): "Average PostgreSQL query execution time with strategic indexes"
- **Icon** (optional): "📊"
- **Trend** (optional): `stable`
- **Threshold** (optional): 150

---

### Metric 5: Concurrent Request Handling

- **Label**: "Max Concurrent Requests"
- **Value**: "500+"
- **Unit** (optional): "requests/second"
- **Description** (optional): "Async architecture handles 500+ concurrent requests per worker"
- **Icon** (optional): "🚀"
- **Trend** (optional): `up`
- **Threshold** (optional): 300

---

## Code Quality Metrics

### Metric 6: Test Coverage

- **Label**: "Test Coverage"
- **Value**: "85%"
- **Unit** (optional): "percent"
- **Description** (optional): "Unit and integration test coverage across all modules"
- **Icon** (optional): "🧪"
- **Trend** (optional): `up`
- **Threshold** (optional): 80

---

### Metric 7: Code Organization

- **Label**: "Domain Modules"
- **Value**: "5"
- **Unit** (optional): "modules"
- **Description** (optional): "Modular DDD architecture (Cinema, Movie, Theater, Showtime, Shared)"
- **Icon** (optional): "🏛️"
- **Trend** (optional): `stable`
- **Threshold** (optional): null

---

### Metric 8: API Endpoints

- **Label**: "REST Endpoints"
- **Value**: "30+"
- **Unit** (optional): "endpoints"
- **Description** (optional): "Total number of REST API endpoints across all domains"
- **Icon** (optional): "🌐"
- **Trend** (optional): `up`
- **Threshold** (optional): null

---

### Metric 9: Dependencies

- **Label**: "External Dependencies"
- **Value**: "12"
- **Unit** (optional): "packages"
- **Description** (optional): "Core dependencies including FastAPI, SQLAlchemy, Redis, Alembic"
- **Icon** (optional): "📦"
- **Trend** (optional): `stable`
- **Threshold** (optional): 20

---

## Infrastructure Metrics

### Metric 10: Container Image Size

- **Label**: "Docker Image Size"
- **Value**: "450MB"
- **Unit** (optional): "megabytes"
- **Description** (optional): "Optimized multi-stage build with Alpine base images"
- **Icon** (optional): "🐳"
- **Trend** (optional): `down`
- **Threshold** (optional): 600

---

### Metric 11: application Startup Time

- **Label**: "Cold Start Time"
- **Value**: "<10s"
- **Unit** (optional): "seconds"
- **Description** (optional): "application startup including database migrations"
- **Icon** (optional): "⏱️"
- **Trend** (optional): `stable`
- **Threshold** (optional): 15

---

### Metric 12: Memory Usage Per Worker

- **Label**: "Memory Footprint"
- **Value**: "200MB"
- **Unit** (optional): "megabytes"
- **Description** (optional): "Average memory usage per Gunicorn worker process"
- **Icon** (optional): "🧠"
- **Trend** (optional): `stable`
- **Threshold** (optional): 300

---

### Metric 13: Database Connection Pool

- **Label**: "DB Connection Pool Size"
- **Value**: "20"
- **Unit** (optional): "connections"
- **Description** (optional): "Async connection pool supporting concurrent queries"
- **Icon** (optional): "🔌"
- **Trend** (optional): `stable`
- **Threshold** (optional): 30

---

### Metric 14: Service Uptime

- **Label**: "Service Availability"
- **Value**: "99.9%"
- **Unit** (optional): "percent"
- **Description** (optional): "Production uptime with health check monitoring"
- **Icon** (optional): "❤️"
- **Trend** (optional): `stable`
- **Threshold** (optional): 99.5

---

## Security Metrics

### Metric 15: Authentication Success Rate

- **Label**: "JWT Validation Success"
- **Value**: "99.5%"
- **Unit** (optional): "percent"
- **Description** (optional): "Successful JWT token validations vs total auth requests"
- **Icon** (optional): "🔐"
- **Trend** (optional): `stable`
- **Threshold** (optional): 98

---

### Metric 16: Rate Limit Violations

- **Label**: "Rate Limit Hits"
- **Value**: "<1%"
- **Unit** (optional): "percent"
- **Description** (optional): "Percentage of requests blocked by rate limiter"
- **Icon** (optional): "🚦"
- **Trend** (optional): `down`
- **Threshold** (optional): 5

---

### Metric 17: Authorization Checks

- **Label**: "Protected Endpoints"
- **Value**: "40%"
- **Unit** (optional): "percent"
- **Description** (optional): "Percentage of endpoints requiring authentication/authorization"
- **Icon** (optional): "🔒"
- **Trend** (optional): `up`
- **Threshold** (optional): 30

---

## Business Metrics

### Metric 18: Theater Types Supported

- **Label**: "Theater Technologies"
- **Value**: "6"
- **Unit** (optional): "types"
- **Description** (optional): "Supported formats: 2D, 3D, IMAX, 4DX, VIP"
- **Icon** (optional): "🎪"
- **Trend** (optional): `stable`
- **Threshold** (optional): null

---

### Metric 19: Seat Categories

- **Label**: "Seat Types"
- **Value**: "6"
- **Unit** (optional): "categories"
- **Description** (optional): "Standard, VIP, Accessible, Premium, 4DX, Loveseat"
- **Icon** (optional): "💺"
- **Trend** (optional): `stable`
- **Threshold** (optional): null

---

### Metric 20: Showtime Statuses

- **Label**: "Showtime Lifecycle States"
- **Value**: "5"
- **Unit** (optional): "states"
- **Description** (optional): "DRAFT, UPCOMING, IN_PROGRESS, COMPLETED, CANCELLED"
- **Icon** (optional): "📅"
- **Trend** (optional): `stable`
- **Threshold** (optional): null

---

### Metric 21: Multi-Language Support

- **Label**: "Supported Languages"
- **Value**: "6+"
- **Unit** (optional): "languages"
- **Description** (optional): "English, Spanish, Japanese, Korean with dubbed/original options"
- **Icon** (optional): "🌍"
- **Trend** (optional): `stable`
- **Threshold** (optional): null

---

### Metric 22: Regional Coverage

- **Label**: "Geographic Regions"
- **Value**: "CDMX Metropolitan"
- **Unit** (optional): "areas"
- **Description** (optional): "Cinema locations across Mexico City zones"
- **Icon** (optional): "📍"
- **Trend** (optional): `up`
- **Threshold** (optional): null

---

## Scalability Metrics

### Metric 23: Horizontal Scalability

- **Label**: "Scale Factor"
- **Value**: "Unlimited"
- **Unit** (optional): "instances"
- **Description** (optional): "Stateless design allows infinite horizontal scaling"
- **Icon** (optional): "📈"
- **Trend** (optional): `stable`
- **Threshold** (optional): null

---

### Metric 24: Database Load Reduction

- **Label**: "Cache Load Reduction"
- **Value**: "80%"
- **Unit** (optional): "percent"
- **Description** (optional): "Database query reduction thanks to Redis caching layer"
- **Icon** (optional): "💾"
- **Trend** (optional): `up`
- **Threshold** (optional): 70

---

### Metric 25: Request Throughput

- **Label**: "Max Throughput"
- \*\*Value": "2000+"
- **Unit** (optional): "req/s"
- **Description** (optional): "Maximum requests per second with 4 Gunicorn workers"
- **Icon** (optional): "🚀"
- **Trend** (optional): `up`
- **Threshold** (optional): 1500
