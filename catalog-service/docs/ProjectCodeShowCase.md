# Code Showcase

## Code Examples (`CodeExample[]`)

### Example 1: Movie Entity

- **ID**: "movie-entity"
- **Title**: "Movie Entity"
- **Description**: "Domain entity representing a movie with exhibition date validation"
- **Category**: "Domain"
- **Duration** (optional): ""
- **Views** (optional): 
- **Tags** (optional):
  - Domain-Driven Design
  - Validation

#### Files (`CodeFile[]`)

- **Name**: "entities.py"
- **Path**: "app/movies/domain/entities.py"
- **Language**: "python"
- **Content**:
  ```python
  class Movie(BaseModel):
      id: Optional[int] = None
      title: str = Field(..., max_length=200)
      minute_duration: PositiveInt = Field(..., description="Duration in minutes")
      release_date: date
      projection_start_date: date
      projection_end_date: date
      synopsis: str
      genre: MovieGenre
      rating: MovieRating
      
      @property
      def is_active(self) -> bool:
          return self.deleted_at is None

      def is_showing(self, on_date: Optional[date] = None) -> bool:
          if on_date is None:
              on_date = date.today()
          return self.projection_start_date <= on_date <= self.projection_end_date
  ```
- **Highlighted** (optional): `true`
- **Explanation** (optional): "The Movie entity includes exhibition date logic with is_showing() method"

---

### Example 2: Theater Entity with Business Rules

- **ID**: "theater-entity"
- **Title**: "Theater Entity with Business Rules"
- **Description**: "Domain entity implementing capacity validation by theater type"
- **Category**: "Domain"
- **Duration** (optional): ""
- **Views** (optional): 
- **Tags** (optional):
  - Business Rules
  - Domain Validation

#### Files (`CodeFile[]`)

- **Name**: "theater.py"
- **Path**: "app/theater/domain/theater.py"
- **Language**: "python"
- **Content**:
  ```python
  class Theater(BaseModel):
      id: Optional[int] = None
      cinema_id: int
      name: str = Field(..., max_length=50)
      capacity: PositiveInt
      theater_type: TheaterType
      is_active: bool = True
      maintenance_mode: bool = False

      CAPACITY_RULES: ClassVar = {
          TheaterType.IMAX: {"min": 150, "max": 300},
          TheaterType.TWO_D: {"min": 50, "max": 200},
          TheaterType.THREE_D: {"min": 100, "max": 200},
          TheaterType.FOUR_DX: {"min": 20, "max": 100},
          TheaterType.VIP: {"min": 10, "max": 50}
      }

      def validate_capacity(self):
          rules = self.CAPACITY_RULES.get(self.theater_type, {})
          if not (rules['min'] <= self.capacity <= rules['max']):
              raise InvalidCapacityError(
                  f"Capacity {self.capacity} is invalid for {self.theater_type}"
              )

      def enter_maintenance(self):
          self.maintenance_mode = True
          self.deactivate()
  ```
- **Highlighted** (optional): `true`
- **Explanation** (optional): "The Theater entity enforces capacity rules based on theater type (IMAX 150-300, VIP 10-50, etc.)"

---

### Example 3: Movie Controller

- **ID**: "movie-controller"
- **Title**: "Movie Controller"
- **Description**: "FastAPI controller with dependency injection and rate limiting"
- **Category**: "Presentation"
- **Duration** (optional): ""
- **Views** (optional): 
- **Tags** (optional):
  - FastAPI
  - REST API
  - Dependency Injection

#### Files (`CodeFile[]`)

- **Name**: "movie_controllers.py"
- **Path**: "app/movies/infrastructure/api/movie_controllers.py"
- **Language**: "python"
- **Content**:
  ```python
  @router.get("/active/", response_model=PaginatedMovieResponse)
  @limiter.limit("60/minute")
  async def get_movies_in_exhibition(
      use_case: Annotated[
          GetMoviesInExhitionUseCase, Depends(movie_use_cases.get_active_movies_use_case)
      ],
      request: Request,
      offset: Annotated[int, Query(ge=0)] = 0,
      limit: Annotated[int, Query(ge=1, le=100)] = 10,
  ):
      params = PaginationParams(offset=offset, limit=limit)
      page: Page[Movie] = await use_case.execute(params)
      return PaginatedMovieResponse.from_page(page)
  ```
- **Highlighted** (optional): `true`
- **Explanation** (optional): "Controller demonstrates dependency injection for use cases with pagination"

---

### Example 4: Cinema Base Model

- **ID**: "cinema-base-model"
- **Title**: "Cinema Base Model"
- **Description**: "Pydantic model with value objects for complex cinema data"
- **Category**: "Domain"
- **Duration** (optional): ""
- **Views** (optional): 
- **Tags** (optional):
  - Value Objects
  - Pydantic

#### Files (`CodeFile[]`)

- **Name**: "base.py"
- **Path**: "app/cinema/domain/base.py"
- **Language**: "python"
- **Content**:
  ```python
  class CinemaBase(BaseModel):
      image: str = Field(..., description="Cinema image URL")
      name: str = Field(..., max_length=255, min_length=3)
      tax_number: str = Field(..., max_length=255, min_length=5)
      is_active: bool = Field(False)
      description: str = Field("")
      screens: int = Field(..., ge=0)
      type: CinemaType
      status: CinemaStatus
      amenities: CinemaAmenities
      region: LocationRegion
      location: Location = Field(..., description="Geographical coordinates")
      contact_info: ContactInfo
      social_media: SocialMedia
      features: List[CinemaFeatures]
  ```
- **Highlighted** (optional): `false`
- **Explanation** (optional): "Cinema model with rich value objects for location, contact, amenities"

---

### Example 5: Theater Seat Model

- **ID**: "seat-model"
- **Title**: "Theater Seat Model"
- **Description**: "Seat entity with type classification and status"
- **Category**: "Domain"
- **Duration** (optional): ""
- **Views** (optional): 
- **Tags** (optional):
  - Domain
  - Entities

#### Files (`CodeFile[]`)

- **Name**: "seat.py"
- **Path**: "app/theater/domain/seat.py"
- **Language**: "python"
- **Content**:
  ```python
  class TheaterSeatBase(BaseModel):
      theater_id: int = Field(..., description="Theater ID")
      seat_row: str = Field(..., max_length=5, description="Row identifier (e.g., 'A')")
      seat_number: int = Field(..., gt=0, description="Seat number within row")
      seat_type: SeatType = Field(SeatType.STANDARD)
      is_active: bool = Field(True)

  class TheaterSeat(TheaterSeatBase):
      id: Optional[int] = Field(None, description="Seat ID")
      created_at: Optional[datetime] = None
      updated_at: Optional[datetime] = None
  ```
- **Highlighted** (optional): `false`
- **Explanation** (optional): "Seat model with row/seat number and type (STANDARD, VIP, ACCESSIBLE)"

---

### Example 6: Seat Controller

- **ID**: "seat-controller"
- **Title**: "Seat Controller with Logging"
- **Description**: "Controller demonstrating comprehensive logging for seat operations"
- **Category**: "Presentation"
- **Duration** (optional): ""
- **Views** (optional): 
- **Tags** (optional):
  - FastAPI
  - Logging

#### Files (`CodeFile[]`)

- **Name**: "theather_seat_controllers.py"
- **Path**: "app/theater/infrastructure/api/theather_seat_controllers.py"
- **Language**: "python"
- **Content**:
  ```python
  @router.get("/by_theater/{theater_id}", response_model=List[TheaterSeat])
  @limiter.limit("60/minute")
  async def get_seats_by_theater(
      request: Request,
      theater_id: int,
      use_case: GetSeatsByTheaterUseCase = Depends(get_seats_by_theater_use_case),
  ) -> List[TheaterSeat]:
      logger.info(f"GET seats by theater started | theater_id:{theater_id}")
      try:
          seats = await use_case.execute(theater_id)
          logger.info(f"GET seats by theater success | count:{len(seats)}")
          return seats
      except Exception as e:
          logger.error(f"GET seats by theater failed | error:{str(e)}")
          raise
  ```
- **Highlighted** (optional): `false`
- **Explanation** (optional): "Controller with comprehensive logging for debugging and audit"
