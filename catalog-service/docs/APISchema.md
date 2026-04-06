# API Schema

- **Type**: `REST` 

---

## HTTP Endpoints (`ApiEndpoint[]`)

### Movies Endpoints

#### GET /api/v1/movies/{movie_id}

- **ID**: "get-movie-by-id"
- **Method**: `GET`
- **URL Path**: "/api/v1/movies/{movie_id}"
- **Summary**: "Get a movie by its ID"
- **Description**: "Retrieves a single movie by its unique identifier"
- **Tags**: `movies`
- **Authenticated**: `false`
- **Rate Limit**: "60/minute"

#### Parameters (`ApiParameter[]`)

- **Name**: "movie_id"
- **In**: `path`
- **Type**: `integer`
- **Required**: `true`
- **Description**: "The ID of the movie to retrieve"

#### Responses (`ApiResponse[]`)

- **Status**: 200
- **Description**: "Movie found"
- **Schema**: `MovieDetailResponse`
- **Example**:
  ```json
  {
    "id": 1,
    "title": "Inception",
    "original_title": "Inception",
    "minute_duration": 148,
    "release_date": "2010-07-16",
    "projection_start_date": "2026-04-01",
    "projection_end_date": "2026-06-30",
    "synopsis": "A thief who steals corporate secrets...",
    "genre": "ACTION",
    "rating": "PG13",
    "poster_url": "https://example.com/poster.jpg"
  }
  ```

---

#### GET /api/v1/movies/active/

- **ID**: "get-active-movies"
- **Method**: `GET`
- **URL Path**: "/api/v1/movies/active/"
- **Summary**: "Get movies currently in exhibition"
- **Description**: "Returns movies that are currently showing based on projection dates"
- **Tags**: `movies`
- **Authenticated**: `false`
- **Rate Limit**: "60/minute"

#### Parameters (`ApiParameter[]`)

- **Name**: "offset"
- **In**: `query`
- **Type**: `integer`
- **Required**: `false`
- **Description**: "Number of records to skip"
- **Example**: 0
- **Name**: "limit"
- **In**: `query`
- **Type**: `integer`
- **Required**: `false`
- **Description**: "Maximum number of records to return"
- **Example**: 10

#### Responses (`ApiResponse[]`)

- **Status**: 200
- **Description**: "List of active movies"
- **Schema**: `PaginatedMovieResponse`

---

#### GET /api/v1/movies/

- **ID**: "search-movies"
- **Method**: `GET`
- **URL Path**: "/api/v1/movies/"
- **Summary**: "Search movies with filters"
- **Description**: "Search and filter movies by various criteria"
- **Tags**: `movies`
- **Authenticated**: `false`
- **Rate Limit**: "60/minute"

#### Parameters (`ApiParameter[]`)

- **Name**: "filters"
- **In**: `query`
- **Type**: `SearchMovieFilters`
- **Required**: `false`
- **Description**: "Search filters"

---

#### POST /api/v1/movies/

- **ID**: "create-movie"
- **Method**: `POST`
- **URL Path**: "/api/v1/movies/"
- **Summary**: "Create a new movie"
- **Description**: "Creates a new movie in the catalog (admin/manager only)"
- **Tags**: `movies`
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

#### Request Body (`ApiRequestBody`)

- **Content Type**: "application/json"
- **Schema**: `Movie`
- **Example**:
  ```json
  {
    "title": "New Movie",
    "minute_duration": 120,
    "release_date": "2026-01-01",
    "projection_start_date": "2026-04-01",
    "projection_end_date": "2026-06-30",
    "synopsis": "Movie synopsis...",
    "genre": "DRAMA",
    "rating": "R"
  }
  ```

---

#### PUT /api/v1/movies/{movie_id}

- **ID**: "update-movie"
- **Method**: `PUT`
- **URL Path**: "/api/v1/movies/{movie_id}"
- **Summary**: "Update a movie"
- **Description**: "Updates an existing movie (admin/manager only)"
- **Tags**: `movies`
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

---

#### DELETE /api/v1/movies/{movie_id}

- **ID**: "delete-movie"
- **Method**: `DELETE`
- **URL Path**: "/api/v1/movies/{movie_id}"
- **Summary**: "Delete a movie"
- **Description**: "Soft deletes a movie (admin/manager only)"
- **Tags**: `movies`
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

---

### Cinemas Endpoints

#### GET /api/v1/cinemas/{cinema_id}

- **ID**: "get-cinema-by-id"
- **Method**: `GET`
- **URL Path**: "/api/v1/cinemas/{cinema_id}"
- **Summary**: "Get a cinema by ID"
- **Description**: "Retrieves a single cinema with full details"
- **Tags**: `cinemas`
- **Authenticated**: `false`
- **Rate Limit**: "60/minute"

---

#### GET /api/v1/cinemas/active/

- **ID**: "get-active-cinemas"
- **Method**: `GET`
- **URL Path**: "/api/v1/cinemas/active/"
- **Summary**: "Get active cinemas"
- **Description**: "Returns all active cinemas with pagination"
- **Tags**: `cinemas`
- **Authenticated**: `false`
- **Rate Limit**: "60/minute"

---

#### GET /api/v1/cinemas/

- **ID**: "search-cinemas"
- **Method**: `GET`
- **URL Path**: "/api/v1/cinemas/"
- **Summary**: "Search cinemas"
- **Description**: "Search and filter cinemas"
- **Tags**: `cinemas`
- **Authenticated**: `false`
- **Rate Limit**: "60/minute"

---

#### POST /api/v1/cinemas/

- **ID**: "create-cinema"
- **Method**: `POST`
- **URL Path**: "/api/v1/cinemas/"
- **Summary**: "Create a cinema"
- **Description**: "Creates a new cinema (admin/manager only)"
- **Tags**: `cinemas`
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

---

#### PUT /api/v1/cinemas/{cinema_id}

- **ID**: "update-cinema"
- **Method**: `PUT`
- **URL Path**: "/api/v1/cinemas/{cinema_id}"
- **Summary**: "Update a cinema"
- **Description**: "Updates an existing cinema (admin/manager only)"
- **Tags**: `cinemas`
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

---

#### POST /api/v1/cinemas/{cinema_id}/restore

- **ID**: "restore-cinema"
- **Method**: `POST`
- **URL Path**: "/api/v1/cinemas/{cinema_id}/restore"
- **Summary**: "Restore a cinema"
- **Description**: "Restores a soft-deleted cinema (admin/manager only)"
- **Tags**: `cinemas`
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

---

#### DELETE /api/v1/cinemas/{cinema_id}

- **ID**: "delete-cinema"
- **Method**: `DELETE`
- **URL Path**: "/api/v1/cinemas/{cinema_id}"
- **Summary**: "Delete a cinema"
- **Description**: "Soft deletes a cinema (admin/manager only)"
- **Tags**: `cinemas`
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

---

### Theaters Endpoints

#### GET /api/v1/theaters/{theater_id}

- **ID**: "get-theater-by-id"
- **Method**: `GET`
- **URL Path**: "/api/v1/theaters/{theater_id}"
- **Summary**: "Get a theater by ID"
- **Description**: "Retrieves a single theater with details"
- **Tags**: `theaters`
- **Authenticated**: `false`
- **Rate Limit**: "60/minute"

---

#### GET /api/v1/theaters/

- **ID**: "search-theaters"
- **Method**: `GET`
- **URL Path**: "/api/v1/theaters/"
- **Summary**: "Search theaters"
- **Description**: "Search and filter theaters"
- **Tags**: `theaters`
- **Authenticated**: `false`
- **Rate Limit**: "60/minute"

---

#### GET /api/v1/theaters/cinema/{cinema_id}

- **ID**: "get-theaters-by-cinema"
- **Method**: `GET`
- **URL Path**: "/api/v1/theaters/cinema/{cinema_id}"
- **Summary**: "Get theaters by cinema"
- **Description**: "Returns all theaters in a specific cinema"
- **Tags**: `theaters`
- **Authenticated**: `false`
- **Rate Limit**: "60/minute"

---

#### POST /api/v1/theaters/

- **ID**: "create-theater"
- **Method**: `POST`
- **URL Path**: "/api/v1/theaters/"
- **Summary**: "Create a theater"
- **Description**: "Creates a new theater (admin/manager only)"
- **Tags**: `theaters`
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

---

#### PUT /api/v1/theaters/{theater_id}

- **ID**: "update-theater"
- **Method**: `PUT`
- **URL Path**: "/api/v1/theaters/{theater_id}"
- **Summary**: "Update a theater"
- **Description**: "Updates an existing theater (admin/manager only)"
- **Tags**: `theaters`
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

---

#### DELETE /api/v1/theaters/{theater_id}

- **ID**: "delete-theater"
- **Method**: `DELETE`
- **URL Path**: "/api/v1/theaters/{theater_id}"
- **Summary**: "Delete a theater"
- **Description**: "Soft deletes a theater (admin/manager only)"
- **Tags**: `theaters`
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

---

#### POST /api/v1/theaters/{theater_id}/restore

- **ID**: "restore-theater"
- **Method**: `POST`
- **URL Path**: "/api/v1/theaters/{theater_id}/restore"
- **Summary**: "Restore a theater"
- **Description**: "Restores a soft-deleted theater (admin/manager only)"
- **Tags**: `theaters`
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

---

### Seats Endpoints

#### GET /api/v1/theaters/seats/{seat_id}

- **ID**: "get-seat-by-id"
- **Method**: `GET`
- **URL Path**: "/api/v1/theaters/seats/{seat_id}"
- **Summary**: "Get a seat by ID"
- **Description**: "Retrieves a single seat"
- **Tags**: `seats`
- **Authenticated**: `false`
- **Rate Limit**: "60/minute"

---

#### GET /api/v1/theaters/seats/by_theater/{theater_id}

- **ID**: "get-seats-by-theater"
- **Method**: `GET`
- **URL Path**: "/api/v1/theaters/seats/by_theater/{theater_id}"
- **Summary**: "Get all seats for a theater"
- **Description**: "Returns all seats in a specific theater"
- **Tags**: `seats`
- **Authenticated**: `false`
- **Rate Limit**: "60/minute"

---

#### POST /api/v1/theaters/seats/

- **ID**: "create-seat"
- **Method**: `POST`
- **URL Path**: "/api/v1/theaters/seats/"
- **Summary**: "Create a seat"
- **Description**: "Creates a new seat (admin/manager only)"
- **Tags**: `seats`
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

---

#### PUT /api/v1/theaters/seats/{seat_id}

- **ID**: "update-seat"
- **Method**: `PUT`
- **URL Path**: "/api/v1/theaters/seats/{seat_id}"
- **Summary**: "Update a seat"
- **Description**: "Updates an existing seat (admin/manager only)"
- **Tags**: `seats`
- **Authenticated**: `true`
- **Rate Limit**: "10/minute"

---

#### DELETE /api/v1/theaters/seats/{seat_id}

- **ID**: "delete-seat"
- **Method**: `DELETE`
- **URL Path**: "/api/v1/theaters/seats/{seat_id}"
- **Summary**: "Delete a seat"
- **Description**: "Deletes a seat (admin/manager only)"
- **Tags**: `seats`
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
    "service": "catalog-service"
  }
  ```
