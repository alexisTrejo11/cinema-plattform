# Project Metric

## Metric 1: API Response Time

- **Label**: "API Response Time (p95)"
- **Value**: "< 150ms"
- **Unit** (optional): "ms"
- **Description** (optional): "95th percentile response time for catalog API endpoints"
- **Icon** (optional): "⚡"
- **Trend** (optional): `stable`
- **Threshold** (optional): 150

---

## Metric 2: Movie Queries QPS

- **Label**: "Movie Queries QPS"
- **Value**: "10000 QPS"
- **Unit** (optional): "QPS"
- **Description** (optional): "Peak queries per second for movie catalog"
- **Icon** (optional): "🎬"
- **Trend** (optional): `stable`
- **Threshold** (optional): 10000

---

## Metric 3: Cinema Lookup

- **Label**: "Cinema Lookup (with cache)"
- **Value**: "< 50ms"
- **Unit** (optional): "ms"
- **Description** (optional): "Average time to lookup cinema with Redis caching"
- **Icon** (optional): "🏠"
- **Trend** (optional): `stable`
- **Threshold** (optional): 50

---

## Metric 4: gRPC Response Time

- **Label**: "gRPC Response Time"
- **Value**: "< 30ms"
- **Unit** (optional): "ms"
- **Description** (optional): "Average gRPC response time for catalog queries"
- **Icon** (optional): "🔗"
- **Trend** (optional): `stable`
- **Threshold** (optional): 30

---

## Metric 5: Active Cinemas

- **Label**: "Active Cinemas"
- **Value**: "50"
- **Unit** (optional): ""
- **Description** (optional): "Number of active cinema locations"
- **Icon** (optional): "🏠"
- **Trend** (optional): `up`
- **Threshold** (optional): 10

---

## Metric 6: Total Theaters

- **Label**: "Total Theaters"
- **Value**: "200"
- **Unit** (optional): ""
- **Description** (optional): "Total number of theaters across all cinemas"
- **Icon** (optional): "🎭"
- **Trend** (optional): `stable`
- **Threshold** (optional): 50

---

## Metric 7: Database Connections

- **Label**: "DB Connection Pool Size"
- **Value**: "20"
- **Unit** (optional): ""
- **Description** (optional): "Maximum PostgreSQL connections"
- **Icon** (optional): "🗄️"
- **Trend** (optional): `stable`
- **Threshold** (optional): 25

---

## Metric 8: Service Uptime

- **Label**: "Service Uptime"
- **Value**: "99.9%"
- **Unit** (optional): "%"
- **Description** (optional): "Monthly service availability"
- **Icon** (optional): "🟢"
- **Trend** (optional): `stable`
- **Threshold** (optional): 99.9
