from app.users.domain.entities import User
from app.users.application.repositories import UserRepository
from app.users.application.dtos import UserResponse
from .services import PasswordService
from .dtos import SignUpRequest, LoginRequest, RefreshTokenRequest, TokenResponse
from .repositories import SessionRepository
from app.shared.response import Result
from app.auth.application.services import AuthValidationService, SessionService
from app.auth.domain.entities import TokenType


class SignUpUseCase:
    def __init__(
        self,user_repository: UserRepository, 
        password_service: PasswordService,
        validation_service: AuthValidationService
    ):
        self.user_repository = user_repository
        self.password_service = password_service
        self.validation_service = validation_service
    
    async def execute(self, request: SignUpRequest) -> Result:
        validation_result = await self.validation_service.validate_unique_fields(request.email, request.phone_number)
        if not validation_result.is_success():
            return validation_result
        
        hashed_password = self.password_service.hash_password(request.password)
        new_user = User(hashed_password=hashed_password,**request.model_dump())
        
        created_user = await self.user_repository.save(new_user)
        
        user_response = UserResponse.from_domain(created_user)
        return Result.success(user_response)


class LoginUseCase:
    def __init__(self, session_service: SessionService, validation_service: AuthValidationService):
        self.session_service = session_service
        self.validation_service = validation_service
    
    async def execute(self, request: LoginRequest) -> Result:
        user = await self.validation_service.authenticate_user(request.identifier_field, request.password)
        if not user:
            return Result.error("User not found with given credentials")
        
        if not user.is_active:
            return Result.error("User account is deactivated")
        
        session = await self.session_service.create_session(user)
        return Result.success(session)


class RefreshTokenUseCase:
    def __init__(
        self,
        session_service: SessionService
    ):
        self.session_service = session_service
    
    async def execute(self, request: RefreshTokenRequest, user: User) -> TokenResponse:
        token_response = await self.session_service.refresh_session(request, user)
        return token_response


class LogoutUseCase:
    def __init__(self, session_repository: SessionRepository):
        self.session_repository = session_repository
    
    def execute(self, refresh_token: str, user_id: int) :
        return self.session_repository.revoke_user_token(str(user_id), refresh_token, TokenType.JWT_REFRESH)


class LogoutAllUseCase:
    def __init__(self, session_repository: SessionRepository):
        self.session_repository = session_repository
    
    def execute(self, user_id: int) -> bool:
        return self.session_repository.revoke_all_user_tokens(str(user_id))
