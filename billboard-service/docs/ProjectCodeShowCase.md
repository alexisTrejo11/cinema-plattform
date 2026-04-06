# Code Showcase

## Code Examples (`CodeExample[]`)

### Example 1: Showtime Entity with Business Rules

- **ID**: "showtime-entity"
- **Title**: "Showtime Entity with Business Rules"
- **Description**: "Domain entity implementing validation for price, duration, and scheduling rules"
- **Category**: "Domain"
- **Duration** (optional): ""
- **Views** (optional): 
- **Tags** (optional):
  - Domain-Driven Design
  - Business Rules
  - Validation

#### Files (`CodeFile[]`)

- **Name**: "showtime.py"
- **Path**: "app/showtime/domain/entities/showtime.py"
- **Language**: "python"
- **Content**:
  ```python
  def _validate_price(self):
      MAX_LIMIT_PRICE = Decimal("50.00")
      MIN_LIMIT_PRICE = Decimal("3.00")
      if not (MIN_LIMIT_PRICE < self.price < MAX_LIMIT_PRICE):
          raise InvalidShowtimePriceError(self.price, MIN_LIMIT_PRICE, MAX_LIMIT_PRICE)

  def _validate_schedule_date(self):
      self._validate_not_schedule_in_past()
      self._validate_schedule_date_no_too_far()

  def _validate_not_schedule_in_past(self):
      now_utc = datetime.now(timezone.utc)
      start_time_utc = self._normalize_datetime_to_utc(self.start_time)
      if start_time_utc < now_utc:
          raise ShowtimeSchedulingError("Showtime start time cannot be in the past")

  def _validate_schedule_date_no_too_far(self):
      MAX_DAYS_START_DATE_ALLOWED = 30
      now_utc = datetime.now(timezone.utc)
      future_limit_date = now_utc + timedelta(days=MAX_DAYS_START_DATE_ALLOWED)
      start_time_utc = self._normalize_datetime_to_utc(self.start_time)
      if start_time_utc > future_limit_date:
          raise ShowtimeSchedulingError(f"Showtime exceeds {MAX_DAYS_START_DATE_ALLOWED} days limit")
  ```
- **Highlighted** (optional): `true`
- **Explanation** (optional): "The Showtime entity enforces business rules: price $3-$50, duration 30-300 mins, schedule within 30 days"

---

### Example 2: Showtime Lifecycle Methods

- **ID**: "showtime-lifecycle"
- **Title**: "Showtime Lifecycle Methods"
- **Description**: "Domain methods for showtime state transitions (draft, launch, cancel, restore)"
- **Category**: "Domain"
- **Duration** (optional): ""
- **Views** (optional): 
- **Tags** (optional):
  - State Management
  - Business Logic

#### Files (`CodeFile[]`)

- **Name**: "showtime.py"
- **Path**: "app/showtime/domain/entities/showtime.py"
- **Language**: "python"
- **Content**:
  ```python
  def mark_as_launchable(self):
      if self.status != ShowtimeStatus.DRAFT:
          raise ValidationError("Showtime is not draft can't be launched")
      self.status = ShowtimeStatus.UPCOMING
      self.updated_at = datetime.now(timezone.utc)

  def cancel(self):
      if self.deleted_at is not None:
          raise ShowtimeCancellationError(self.id)
      if self.status == ShowtimeStatus.COMPLETED:
          raise ShowtimeCancellationError(self.id)
      self.status = ShowtimeStatus.CANCELLED
      self.updated_at = datetime.now(timezone.utc)

  def restore(self):
      if self.deleted_at is None:
          raise ShowtimeRestorationError(self.id)
      self.deleted_at = None
      self.updated_at = datetime.now(timezone.utc)
  ```
- **Highlighted** (optional): `true`
- **Explanation** (optional): "State machine for showtime lifecycle with validation at each transition"

---

### Example 3: ShowtimeSeat Entity

- **ID**: "showtime-seat"
- **Title**: "ShowtimeSeat Entity"
- **Description**: "Seat reservation with take/leave operations and timestamp tracking"
- **Category**: "Domain"
- **Duration** (optional): ""
- **Views** (optional): 
- **Tags** (optional):
  - Seat Reservation
  - Domain Entities

#### Files (`CodeFile[]`)

- **Name**: "showtime_seat.py"
- **Path**: "app/showtime/domain/entities/showtime_seat.py"
- **Language**: "python"
- **Content**:
  ```python
  class ShowtimeSeat(ShowtimeSeatBase):
      id: Optional[int] = Field(None)
      created_at: Optional[datetime] = None
      updated_at: Optional[datetime] = None

      def is_taken(self) -> bool:
          return self.taken_at is not None 

      def take(self):
          if self.is_taken():
              raise ValueError("Seat Already Taken")
          self.taken_at = datetime.now(timezone.utc)

      def leave(self):
          self.taken_at = None
          self.user_id = None
  ```
- **Highlighted** (optional): `false`
- **Explanation** (optional): "Seat entity with timestamp-based reservation tracking"

---

### Example 4: Showtime Controller

- **ID**: "showtime-controller"
- **Title**: "Showtime Controller"
- **Description**: "FastAPI controller with dependency injection and role-based access"
- **Category**: "Presentation"
- **Duration** (optional): ""
- **Views** (optional): 
- **Tags** (optional):
  - FastAPI
  - REST API
  - Dependency Injection

#### Files (`CodeFile[]`)

- **Name**: "showtime_controller.py"
- **Path**: "app/showtime/infrastructure/api/showtime_controller.py"
- **Language**: "python"
- **Content**:
  ```python
  @router.post("/{showtime_id}/launch", response_model=ShowtimeDetailResponse)
  @limiter.limit("10/minute")
  async def launch_showtime(
      showtime_id: int,
      request: Request,
      use_case: LaunchShowtimeUseCase = Depends(
          showtime_use_cases.launch_showtime_use_case
      ),
      current_user: AuthUserContext = Depends(require_roles("admin", "manager")),
  ):
      showtime = await use_case.execute(showtime_id)
      return ShowtimeDetailResponse.model_validate(showtime)
  ```
- **Highlighted** (optional): `true`
- **Explanation** (optional): "Controller demonstrating dependency injection and RBAC"

---

### Example 5: Buffer Time Calculation

- **ID**: "buffer-times"
- **Title**: "Buffer Time Calculation"
- **Description**: "Class method for calculating pre-show and post-show buffer times"
- **Category**: "Domain"
- **Duration** (optional): ""
- **Views** (optional): 
- **Tags** (optional):
  - Business Logic
  - Time Management

#### Files (`CodeFile[]`)

- **Name**: "showtime.py"
- **Path**: "app/showtime/domain/entities/showtime.py"
- **Language**: "python"
- **Content**:
  ```python
  _EXTRA_DURATIONS: ClassVar = {
      "initial_cleaning": 10,
      "initial_commercials": 40,
      "post_credits_scene": 10,
      "post_cleaning": 30,
  }

  @classmethod
  def get_buffered_extra_times(cls, include_post_credits_scene: bool = False) -> Dict[str, timedelta]:
      pre_buffer_minutes = cls._EXTRA_DURATIONS["initial_cleaning"] + cls._EXTRA_DURATIONS["initial_commercials"]
      post_buffer_minutes = cls._EXTRA_DURATIONS["post_cleaning"]
      if include_post_credits_scene:
          post_buffer_minutes += cls._EXTRA_DURATIONS["post_credits_scene"]
      return {"pre_buffer": timedelta(minutes=pre_buffer_minutes), "post_buffer": timedelta(minutes=post_buffer_minutes)}
  ```
- **Highlighted** (optional): `false`
- **Explanation** (optional): "Buffer times: 50min pre-show (cleaning + commercials), 30min post-show"

---

### Example 6: Seat Quantity Validation

- **ID**: "seat-validation"
- **Title**: "Seat Quantity Validation"
- **Description**: "Validation for seat reservation limits"
- **Category**: "Domain"
- **Duration** (optional): ""
- **Views** (optional): 
- **Tags** (optional):
  - Business Rules
  - Validation

#### Files (`CodeFile[]`)

- **Name**: "showtime.py"
- **Path**: "app/showtime/domain/entities/showtime.py"
- **Language**: "python"
- **Content**:
  ```python
  def take_seats(self, seats_number: int):
      self._validate_seat_quantity(seats_number)
      self._validate_avaliable_seats(seats_number)
      self.available_seats -= seats_number

  def _validate_seat_quantity(self, seats_number: int):
      MIN_SEAT_ALLOWED = 1
      MAX_SEAT_ALLOWED = 15
      if not MIN_SEAT_ALLOWED <= seats_number <= MAX_SEAT_ALLOWED:
          raise ShowtimeSeatsError(f"Seat quantity must be between {MIN_SEAT_ALLOWED} to {MAX_SEAT_ALLOWED}")

  def _validate_avaliable_seats(self, seats_number: int):
      if seats_number > self.available_seats:
          raise ShowtimeSeatsError("No Seats Avaliable for requested operation")
  ```
- **Highlighted** (optional): `false`
- **Explanation** (optional): "Validate seat quantity (1-15) and availability before reservation"
