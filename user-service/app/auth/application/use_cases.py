from typing import Any
from app.users.domain.entities import User, Status as UserStatus
from app.users.application.repositories import UserRepository
from app.users.application.dtos import UserResponse
from .services import PasswordService, SessionService, AuthValidationService
from .dtos import SignUpRequest, LoginRequest, RefreshTokenRequest, SessionResponse
from app.token.application.repository import TokenRepository
from app.shared.response import Result
from app.auth.domain.entities import TokenType

class SignUpUseCase:
    def __init__(self, user_repository: UserRepository, validation_service: AuthValidationService):
        self.user_repository = user_repository
        self.validation_service = validation_service
        self.password_service = PasswordService()
    
    async def execute(self, request: SignUpRequest) -> Result[UserResponse]:
        validation_result = await self.validation_service.validate_unique_fields(request.email, request.phone_number)
        if not validation_result.is_success():
            return validation_result
        
        new_user = User(**request.model_dump())
        hashed_password = self.password_service.hash_password(request.password)
        new_user.password = hashed_password
        
        created_user = await self.user_repository.save(new_user)
        
        user_response = UserResponse.from_domain(created_user)
        return Result.success(user_response)


class LoginUseCase:
    def __init__(self, session_service: SessionService, validation_service: AuthValidationService):
        self.session_service = session_service
        self.validation_service = validation_service
    
    async def execute(self, request: LoginRequest) -> Result[Any]:
        user = await self.validation_service.authenticate_user(request.identifier_field, request.password)
        if not user:
            return Result.error("User not found with given credentials")
        
        self._validate_account_status(user)
                
        if user.is_2fa_enabled:
            return await self._proccess_2fa_login(user, request)
        else:
            return await self.proccess_login(user)
            
    async def proccess_login(self, user):
        session = await self.session_service.create_session(user)
        return Result.success(session)
    
    async def _proccess_2fa_login(self, user: User, request: LoginRequest) -> Result:
        if not request.twoFACode:
            # Send Notification
            return Result.success()
        else:
            # Validate Code
            session = await self.session_service.create_session(user)
            return Result.success(session)
    
    def _validate_account_status(self, user: User):
        if user.status == UserStatus.BANNED:
            raise ValueError("User account is banned")
        elif user.status == UserStatus.PENDING:
            raise ValueError("User account is not activated. Request an activate code to activate your account")
        elif user.status == UserStatus.INACTIVE:
            user.status = UserStatus.ACTIVE
            return

        
class RefreshTokenUseCase:
    def __init__(self, session_service: SessionService):
        self.session_service = session_service
    
    async def execute(self, request: RefreshTokenRequest, user: User) -> SessionResponse:
        token_response = await self.session_service.refresh_session(request, user)
        return token_response


class LogoutUseCase:
    def __init__(self, session_repository: TokenRepository):
        self.session_repository = session_repository
    
    def execute(self, refresh_token: str, user_id: int) :
        return self.session_repository.revoke_user_token(str(user_id), refresh_token, TokenType.JWT_REFRESH)


class LogoutAllUseCase:
    def __init__(self, session_repository: SessionService):
        self.session_repository = session_repository
    
    def execute(self, user_id: int) -> None:
        return self.session_repository.revoke_user_sessions(user_id)

    
    