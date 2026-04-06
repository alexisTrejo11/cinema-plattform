# API Schema

- **Type**: `REST` 

---

## HTTP Endpoints (`ApiEndpoint[]`)

### Showtimes Endpoints

#### GET /api/v1/showtimes/{showtime_id}

- **ID**: "get-showtime-by-id"
- **Method**: `GET`
- **URL Path**: "/api/v1/showtimes/{showtime_id}"
- **Summary**: "Get a showtime by ID"
- **Description**: "Retrieves a single showtime with all details"
- **Tags**: `showtimes`
- **Authenticated**: `false`
- **Rate Limit**: "60/minute"

#### Parameters (`ApiParameter[]`)

- **Name**: "showtime_id"
- **In**: `path`
- **Type**: `integer`
- **Required**: `true`
- **Description**: "The ID of the showtime to retrieve"

#### Responses (`ApiResponse[]`)

- **Status**: 200
- **Description**: "Showtime found"
- **Schema**: `ShowtimeDetailResponse`
- **Example**:
  ```json
  {
    "id": 1,
    "movie_id": 100,
    "theater_id": 50,
    "start_time": "2026-04-05T18:00:00Z",
    "end_time": "2026-04-05T20:30:00Z",
    "price": 12.50,
    "currency": "USD",
    "status": "UPCOMING",
    "total_seats": 150,
    "available_seats": 120
  }
  ```

---

#### GET /api/v1/showtimes/

- **ID**: "search-showtimes"
- **Method**: `GET`
- **URL Path**: "/api/v1/showtimes/"
- **Summary**: "Search showtimes with filters"
- **Description**: "Search and filter showtimes by various criteria"
- **Tags**: `showtimes`
- **Authenticated**: `false`
- **Rate Limit**: "60/minute"

#### Parameters (`ApiParameter[]`)

- **Name**: "filters"
- **In**: `query`
- **Type**: `SearchShowtimeFilters`
- **Required**: `false`
- **Description**: "Search filters"
- **Name**: "offset"
- **In**: `query`
- **Type**: `integer`
- **Required**: `false`
- **Description**: "Pagination offset"
- **Example**: 0
- **Name**: "limit"
- **In**: `query`
- **Type**: `integer`
- **Required**: `false`
- **Description**: "Pagination limit (1-100)"
- **Example**: 10

#### Responses (`ApiResponse[]`)

- **Status**: 200
- **Description**: "List of showtimes"
- **Schema**: `PaginatedShowtimeResponse`

---

#### POST /api/v1/showtimes/

- **ID**: "draft-showtime"
- **Method**: `POST`
- **URL Path**: "/api/v1/showtimes/"
- **Summary**: "Create a new showtime (draft)"
- **Description**: "Creates a new showtime in draft status (admin/manager only)"
- **Tags**: `showtimes`
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

#### Request Body (`ApiRequestBody`)

- **Content Type**: "application/json"
- **Schema**: `ShowtimeCreate`
- **Example**:
  ```json
  {
    "movie_id": 100,
    "theater_id": 50,
    "start_time": "2026-04-05T18:00:00Z",
    "end_time": "2026-04-05T20:30:00Z",
    "price": 12.50,
    "currency": "USD"
  }
  ```

---

#### POST /api/v1/showtimes/{showtime_id}/launch

- **ID**: "launch-showtime"
- **Method**: `POST`
- **URL Path**: "/api/v1/showtimes/{showtime_id}/launch"
- **Summary**: "Launch a showtime"
- **Description**: "Changes showtime status from DRAFT to UPCOMING (admin/manager only)"
- **Tags**: `showtimes`
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

---

#### POST /api/v1/showtimes/{showtime_id}/cancel

- **ID**: "cancel-showtime"
- **Method**: `POST`
- **URL Path**: "/api/v1/showtimes/{showtime_id}/cancel"
- **Summary**: "Cancel a showtime"
- **Description**: "Cancels an upcoming showtime (admin/manager only)"
- **Tags**: `showtimes`
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

---

#### POST /api/v1/showtimes/{showtime_id}/restore

- **ID**: "restore-showtime"
- **Method**: `POST`
- **URL Path**: "/api/v1/showtimes/{showtime_id}/restore"
- **Summary**: "Restore a showtime"
- **Description**: "Restores a cancelled showtime (admin/manager only)"
- **Tags**: `showtimes`
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

---

#### PUT /api/v1/showtimes/{showtime_id}

- **ID**: "update-showtime"
- **Method**: `PUT`
- **URL Path**: "/api/v1/showtimes/{showtime_id}"
- **Summary**: "Update a showtime"
- **Description**: "Updates an existing showtime (admin/manager only)"
- **Tags**: `showtimes`
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

#### Request Body (`ApiRequestBody`)

- **Content Type**: "application/json"
- **Schema**: `ShowtimeUpdate`
- **Example**:
  ```json
  {
    "price": 15.00,
    "start_time": "2026-04-05T19:00:00Z",
    "end_time": "2026-04-05T21:30:00Z"
  }
  ```

---

#### DELETE /api/v1/showtimes/{showtime_id}

- **ID**: "delete-showtime"
- **Method**: `DELETE`
- **URL Path**: "/api/v1/showtimes/{showtime_id}"
- **Summary**: "Delete a showtime"
- **Description**: "Soft deletes a draft showtime (admin/manager only)"
- **Tags**: `showtimes`
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

---

### Service Endpoints

#### GET /health

- **ID**: "health-check"
- **Method**: `GET`
- **URL Path**: "/health"
- **Summary**: "Health check"
- **Description**: "Returns service health status"
- **Tags**: `service`
- **Authenticated**: `false`
- **Rate Limit**: "none"

#### Responses (`ApiResponse[]`)

- **Status**: 200
- **Description**: "Service is healthy"
- **Schema**: 
- **Example**:
  ```json
  {
    "status": "healthy",
    "service": "billboard-service"
  }
  ```

---

## Request/Response Schemas

### ShowtimeCreate

```json
{
  "movie_id": "integer (required)",
  "theater_id": "integer (required)",
  "start_time": "datetime (required)",
  "end_time": "datetime (required)",
  "price": "decimal (required, 3.00-50.00)",
  "currency": "string (default: USD)"
}
```

### ShowtimeUpdate

```json
{
  "movie_id": "integer (optional)",
  "theater_id": "integer (optional)",
  "start_time": "datetime (optional)",
  "end_time": "datetime (optional)",
  "price": "decimal (optional)",
  "currency": "string (optional)"
}
```

### ShowtimeDetailResponse

```json
{
  "id": "integer",
  "movie_id": "integer",
  "theater_id": "integer",
  "start_time": "datetime",
  "end_time": "datetime",
  "price": "decimal",
  "currency": "string",
  "status": "string (DRAFT|UPCOMING|COMPLETED|CANCELLED)",
  "total_seats": "integer",
  "available_seats": "integer",
  "created_at": "datetime",
  "updated_at": "datetime",
  "deleted_at": "datetime (nullable)"
}
```

### PaginatedShowtimeResponse

```json
{
  "items": ["ShowtimeDetailResponse"],
  "total": "integer",
  "offset": "integer",
  "limit": "integer"
}
```
