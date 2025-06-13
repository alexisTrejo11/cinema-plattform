from datetime import datetime
import uuid
from app.users.domain.entities import User
from app.users.application.repositories import UserRepository
from app.users.application.dtos import UserResponse
from app.users.domain.exceptions import UserAlreadyExistsException, UserNotFoundException

from app.auth.domain.exceptions import TokenExpiredException, InvalidCredentialsException
from app.auth.domain.entities import SessionToken
from .services import PasswordService, JWTService
from .dtos import SignUpRequest, LoginRequest, RefreshTokenRequest, TokenResponse
from .repositories import SessionTokenRepository

class SignUpUseCase:
    def __init__(self,user_repository: UserRepository,password_service: PasswordService):
        self.user_repository = user_repository
        self.password_service = password_service
    
    async def execute(self, request: SignUpRequest) -> UserResponse:
        existing_user = await self.user_repository.get_by_email(request.email)
        if existing_user:
            raise UserAlreadyExistsException("User with this email already exists")
        
        existing_username = await self.user_repository.get_by_username(request.username)
        if existing_username:
            raise UserAlreadyExistsException("User with this username already exists")
        
        hashed_password = self.password_service.hash_password(request.password)
        user = User(
            user_id=str(uuid.uuid4()),
            email=request.email,
            username=request.username,
            hashed_password=hashed_password
        )
        
        created_user = await self.user_repository.create(user)
        
        return UserResponse(
            user_id=created_user.user_id,
            email=created_user.email,
            username=created_user.username,
            role=created_user.role,
            is_active=created_user.is_active,
            created_at=created_user.created_at
        )

class LoginUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        refresh_token_repository: SessionTokenRepository,
        password_service: PasswordService,
        jwt_service: JWTService
    ):
        self.user_repository = user_repository
        self.refresh_token_repository = refresh_token_repository
        self.password_service = password_service
        self.jwt_service = jwt_service
    
    async def execute(self, request: LoginRequest) -> TokenResponse:
        user = await self.user_repository.get_by_email(request.email)
        if not user or not self.password_service.verify_password(request.password, user.hashed_password):
            raise InvalidCredentialsException("Invalid email or password")
        
        if not user.is_active:
            raise InvalidCredentialsException("User account is deactivated")
        
        token_data = {"sub": user.user_id, "email": user.email, "role": user.role}
        access_token = self.jwt_service.create_access_token(token_data)
        refresh_token = self.jwt_service.create_refresh_token({"sub": user.user_id})
        
        refresh_token_entity = SessionToken(
            token_id=str(uuid.uuid4()),
            user_id=user.user_id,
            token=refresh_token,
            expires_at=datetime.utcnow() + timedelta(days=30)
        )
        await self.refresh_token_repository.create(refresh_token_entity)
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=self.jwt_service.access_token_expire_minutes * 60
        )

class RefreshTokenUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        refresh_token_repository: SessionTokenRepository,
        jwt_service: JWTService
    ):
        self.user_repository = user_repository
        self.refresh_token_repository = refresh_token_repository
        self.jwt_service = jwt_service
    
    async def execute(self, request: RefreshTokenRequest) -> TokenResponse:
        try:
            payload = self.jwt_service.verify_token(request.refresh_token)
        except InvalidCredentialsException:
            raise TokenExpiredException("Invalid refresh token")
        
        if payload.get("type") != "refresh":
            raise InvalidCredentialsException("Invalid token type")
        
        stored_token = await self.refresh_token_repository.get_by_token(request.refresh_token)
        if not stored_token or not stored_token.is_valid():
            raise TokenExpiredException("Refresh token expired or revoked")
        
        user = await self.user_repository.get_by_id(stored_token.user_id)
        if not user or not user.is_active:
            raise UserNotFoundException("User not found or inactive")
        
        token_data = {"sub": user.user_id, "email": user.email, "role": user.role}
        access_token = self.jwt_service.create_access_token(token_data)
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=request.refresh_token,
            expires_in=self.jwt_service.access_token_expire_minutes * 60
        )


class LogoutUseCase:
    def __init__(self, refresh_token_repository: SessionTokenRepository):
        self.refresh_token_repository = refresh_token_repository
    
    async def execute(self, refresh_token: str) -> bool:
        return await self.refresh_token_repository.revoke_token(refresh_token)


class LogoutAllUseCase:
    def __init__(self, refresh_token_repository: SessionTokenRepository):
        self.refresh_token_repository = refresh_token_repository
    
    async def execute(self, user_id: str) -> bool:
        return await self.refresh_token_repository.revoke_all_user_tokens(user_id)
