# Code Showcase

## Code Examples (`CodeExample[]`)

### Example 1: User Entity with Validation

- **ID**: "user-entity"
- **Title**: "Domain Entity with Business Validation"
- **Description**: "User entity demonstrating Pydantic validation, password strength enforcement, and account state management."
- **Category**: "Domain"
- **Tags** (optional):
  - "python"
  - "domain-driven-design"
  - "pydantic"
  - "validation"

#### Files (`CodeFile[]`)

- **Name**: "entities.py"
- **Path**: "app/users/domain/entities.py"
- **Language**: "python"
- **Content**:
  ```python
  class User(Account):
      id: int = 0
      
      def update_profile(self, **kwargs: Any) -> None:
          updatable_fields = ["email", "gender", "phone_number", "first_name", "last_name", "date_of_birth"]
          for field_name in updatable_fields:
              if field_name in kwargs:
                  setattr(self, field_name, kwargs[field_name])
          self.updated_at = datetime.now()
      
      def add_2FA_config(self, secret: str) -> None:
          self.is_2fa_enabled = True
          self.totp_secret = secret
      
      def deactivate(self) -> None:
          self.status = Status.INACTIVE
          self.updated_at = datetime.now()
      
      def ban(self) -> None:
          self.status = Status.BANNED
          self.updated_at = datetime.now()
      
      @staticmethod
      def validate_password_before_hash(password: str):
          password_regex = re.compile(
              r"(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{}|;:'\"` ,.<>/?~]).{8,}$",
              re.VERBOSE,
          )
          if not password_regex.fullmatch(password):
              raise PasswordValidationError("Password", "not strong enough")
  ```
- **Highlighted** (optional): `true`
- **Explanation** (optional): "The User entity demonstrates strong domain modeling with business rules: password validation using regex, account state management (activate, deactivate, ban), and 2FA configuration."

---

### Example 2: Login Use Case

- **ID**: "login-usecase"
- **Title**: "Login Use Case with 2FA Support"
- **Description**: "Shows the login flow with optional two-factor authentication step-up."
- **Category**: "Application"
- **Tags** (optional):
  - "python"
  - "async"
  - "authentication"

#### Files (`CodeFile[]`)

- **Name**: "login_usecase.py"
- **Path**: "app/auth/application/usecases/login_usecase.py"
- **Language**: "python"
- **Content**:
  ```python
  class LoginUseCase:
      def __init__(
          self,
          session_service: SessionService,
          validation_service: AuthValidationService,
          token_service: TokenProvider,
          event_publisher: EventPublisher,
      ):
          self.session_service = session_service
          self.token_service = token_service
          self.validation_service = validation_service
          self._event_publisher = event_publisher

      async def execute(self, request: LoginRequest) -> Result[Any]:
          user = await self.validation_service.authenticate_user(
              request.identifier_field, request.password
          )
          if not user:
              return Result.error("User not found with given credentials")

          if user.is_2fa_enabled:
              qr_code = await self._request_2fa_access(request, user)
              return Result.success({"QR": qr_code})

          session = await self._process_login(user)
          return Result.success(session)
  ```
- **Highlighted** (optional): `true`
- **Explanation** (optional): "The LoginUseCase demonstrates async authentication with optional 2FA step-up. If 2FA is enabled, it returns a QR code for verification instead of completing the login."

---

### Example 3: Redis Token Repository

- **ID**: "redis-token-repo"
- **Title**: "Redis-Based Token Repository"
- **Description**: "Shows session token storage and revocation using Redis with pipeline operations."
- **Category**: "Infrastructure"
- **Tags** (optional):
  - "python"
  - "redis"
  - "caching"

#### Files (`CodeFile[]`)

- **Name**: "redis_repository.py"
- **Path**: "app/shared/token/infrastructure/redis_repository.py"
- **Language**: "python"
- **Content**:
  ```python
  class RedisTokenRepository(TokenRepository):
      def _generate_key(self, user_id: str, token_code: str, token_type: TokenType) -> str:
          return f"session:{user_id}:{token_type.value}:{token_code}"

      def create(self, token: Token) -> None:
          key = self._generate_key(str(token.user_id), token.code, token.type)
          expires_in_seconds = int((token.expires_at - datetime.now()).total_seconds())
          self.redis_conn.set(key, json.dumps(token.__dict__, default=json_serializer))
          if expires_in_seconds > 0:
              self.redis_conn.expire(key, expires_in_seconds)

      def revoke_all_user_tokens(self, user_id: str, token_type: Optional[TokenType] = None) -> bool:
          pattern = f"session:{user_id}:{token_type.value if token_type else '*'}:*"
          # ... scan and revoke logic with Redis pipeline
  ```
- **Highlighted** (optional): `true`
- **Explanation** (optional): "The RedisTokenRepository demonstrates efficient session management with key patterns, TTL-based expiration, and pipeline operations for bulk updates."

---

### Example 4: JWT Middleware

- **ID**: "jwt-middleware"
- **Title**: "JWT Authentication Middleware"
- **Description**: "HTTP middleware that validates JWT tokens on every request and extracts user context."
- **Category**: "Infrastructure"
- **Tags** (optional):
  - "python"
  - "fastapi"
  - "middleware"
  - "jwt"

#### Files (`CodeFile[]`)

- **Name**: "auth_middleware.py"
- **Path**: "app/middleware/auth_middleware.py"
- **Language**: "python"
- **Content**:
  ```python
  async def jwt_auth_middleware(
      request: Request,
      call_next: Callable[[Request], Awaitable[Response]],
  ) -> Response:
      request.state.current_user = None
      request.state.jwt_claims = None

      auth_header = request.headers.get("Authorization", "")
      if not auth_header:
          return await call_next(request)

      if not auth_header.lower().startswith("bearer "):
          return _unauthorized("Invalid Authorization header format. Use: Bearer <token>.")

      token = auth_header[7:].strip()
      if not token:
          return _unauthorized("Bearer token is empty.")

      try:
          claims = decode_jwt_token(token)
          current_user = AuthUserContext.from_claims(claims)
          request.state.jwt_claims = claims
          request.state.current_user = current_user
      except ExpiredSignatureError:
          return _unauthorized("Token has expired.")
      except InvalidTokenError:
          return _unauthorized("Token is invalid.")

      return await call_next(request)
  ```
- **Highlighted** (optional): `true`
- **Explanation** (optional): "The JWT middleware demonstrates request interception for token validation, error handling for expired/invalid tokens, and user context attachment to the request state."

---

### Example 5: Kafka Event Publishing

- **ID**: "kafka-events"
- **Title**: "Domain Event Publishing"
- **Description**: "Shows the event builder pattern for publishing user lifecycle events to Kafka."
- **Category**: "Infrastructure"
- **Tags** (optional):
  - "python"
  - "kafka"
  - "events"

#### Files (`CodeFile[]`)

- **Name**: "builders.py"
- **Path**: "app/shared/events/builders.py"
- **Language**: "python"
- **Content**:
  ```python
  def user_signed_up(user_id: int, email: str) -> DomainEventEnvelope:
      return DomainEventEnvelope(
          event_type=EventType.USER_SIGNED_UP,
          payload={"user_id": user_id, "email": email},
      )

  def user_activated(user_id: int, email: str) -> DomainEventEnvelope:
      return DomainEventEnvelope(
          event_type=EventType.USER_ACTIVATED,
          payload={"user_id": user_id, "email": email},
      )

  def two_factor_enabled(user_id: int, email: str) -> DomainEventEnvelope:
      return DomainEventEnvelope(
          event_type=EventType.TWO_FACTOR_ENABLED,
          payload={"user_id": user_id, "email": email},
      )
  ```
- **Highlighted** (optional): `false`
- **Explanation** (optional): "The event builders demonstrate a standardized envelope pattern for domain events with typed payloads, enabling loose coupling between services."

---

### Example 6: Profile Controller

- **ID**: "profile-controller"
- **Title**: "Profile API Controller"
- **Description**: "Shows FastAPI controller for profile retrieval and updates with dependency injection."
- **Category**: "API"
- **Tags** (optional):
  - "python"
  - "fastapi"
  - "api"

#### Files (`CodeFile[]`)

- **Name**: "controllers.py"
- **Path**: "app/profile/infrastructure/controllers.py"
- **Language**: "python"
- **Content**:
  ```python
  router = APIRouter(prefix="/api/v2/profiles", tags=["User Profiles"])

  @router.get("/", response_model=ProfileResponse)
  async def get_my_profile(
      user: User = Depends(get_logged_user),
      usecase: GetProfileUseCase = Depends(get_profile_use_case),
  ) -> ProfileResponse:
      return usecase.execute(user)

  @router.patch("/", response_model=ProfileResponse)
  async def update_my_profile(
      update_data: ProfileUpdate,
      user: User = Depends(get_logged_user),
      usecase: UpdateProfileUseCase = Depends(update_profile_use_case),
  ) -> ProfileResponse:
      return await usecase.execute(user, update_data)
  ```
- **Highlighted** (optional): `false`
- **Explanation** (optional): "The profile controller demonstrates FastAPI's dependency injection for authentication, type-safe request/response models, and RESTful endpoint design."
