# Project Metric

## Metric 1: API Response Time

- **Label**: "API Response Time (p95)"
- **Value**: "< 150ms"
- **Unit** (optional): "ms"
- **Description** (optional): "95th percentile response time for showtime API endpoints"
- **Icon** (optional): "⚡"
- **Trend** (optional): `stable`
- **Threshold** (optional): 150

---

## Metric 2: Seat Reservation Time

- **Label**: "Seat Reservation Time"
- **Value**: "< 50ms"
- **Unit** (optional): "ms"
- **Description** (optional): "Average time to reserve a seat"
- **Icon** (optional): "💺"
- **Trend** (optional): `stable`
- **Threshold** (optional): 50

---

## Metric 3: Showtime Queries QPS

- **Label**: "Showtime Queries QPS"
- **Value**: "5000 QPS"
- **Unit** (optional): "QPS"
- **Description** (optional): "Peak queries per second for showtime catalog"
- **Icon** (optional): "📅"
- **Trend** (optional): `stable`
- **Threshold** (optional): 5000

---

## Metric 4: Concurrent Reservations

- **Label**: "Concurrent Reservations"
- **Value**: "1000+"
- **Unit** (optional): ""
- **Description** (optional): "Maximum concurrent seat reservations supported"
- **Icon** (optional): "💺"
- **Trend** (optional): `stable`
- **Threshold** (optional): 1000

---

## Metric 5: Active Showtimes

- **Label**: "Active Showtimes"
- **Value**: "500"
- **Unit** (optional): ""
- **Description** (optional): "Number of active/upcoming showtimes"
- **Icon** (optional): "📅"
- **Trend** (optional): `up`
- **Threshold** (optional): 100

---

## Metric 6: Database Connections

- **Label**: "DB Connection Pool Size"
- **Value**: "20"
- **Unit** (optional): ""
- **Description** (optional): "Maximum PostgreSQL connections"
- **Icon** (optional): "🗄️"
- **Trend** (optional): `stable`
- **Threshold** (optional): 25

---

## Metric 7: Cache Hit Rate

- **Label**: "Redis Cache Hit Rate"
- **Value**: "85%"
- **Unit** (optional): "%"
- **Description** (optional): "Percentage of cache hits for showtime queries"
- **Icon** (optional): "⚡"
- **Trend** (optional): `stable`
- **Threshold** (optional): 80

---

## Metric 8: Service Uptime

- **Label**: "Service Uptime"
- **Value**: "99.9%"
- **Unit** (optional): "%"
- **Description** (optional): "Monthly service availability"
- **Icon** (optional): "🟢"
- **Trend** (optional): `stable`
- **Threshold** (optional): 99.9
