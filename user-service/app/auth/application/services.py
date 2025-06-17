from typing import Optional
from datetime import datetime
from passlib.context import CryptContext
from app.shared.response import Result
from app.users.application.repositories import UserRepository
from app.users.domain.entities import User
from app.auth.domain.exceptions import TokenExpiredException, InvalidCredentialsException
from .dtos import RefreshTokenRequest, TokenResponse
from .repositories import SessionRepository
from app.auth.infrastructure.jwt_service import JWTService #TODO: change
from app.auth.domain.entities import TokenType

class SessionService:
    def __init__(self, jwt_service: JWTService, session_repo: SessionRepository) -> None:
        self.jwt_service = jwt_service
        self.session_repo = session_repo

    async def create_session(self, user: User) -> TokenResponse:
        access_token = self.jwt_service.create_token(str(user.id), is_access_token=True)
        refresh_token = self.jwt_service.create_token(str(user.id), user.email, user.role, is_access_token=False)

        self.session_repo.create(refresh_token)
        
        time_remaining = refresh_token.expires_at - datetime.now()
        expires_in_minutes = max(0, int(time_remaining.total_seconds() / 60))
        return TokenResponse(
            access_token=access_token.code,
            refresh_token=refresh_token.code,
            expires_in_minutes = expires_in_minutes
        )

    async def refresh_session(self, request: RefreshTokenRequest, user: User) -> TokenResponse:
        self._valdiate_refresh_token(request.refresh_token)
        
        stored_token = self.session_repo.get_user_token(str(user.id), request.refresh_token, TokenType.JWT_REFRESH)
        if not stored_token or stored_token.is_revoked:
            raise TokenExpiredException("Refresh token expired or revoked")
        
        access_token = self.jwt_service.create_token(user_id=str(user.id), is_access_token=True)
        
        time_remaining = stored_token.expires_at - datetime.now()
        expires_in_minutes = max(0, int(time_remaining.total_seconds() / 60))
        return TokenResponse(
            access_token=stored_token.code,
            refresh_token=access_token.code,
            expires_in_minutes=expires_in_minutes
        )
        
    def _valdiate_refresh_token(self, refresh_token: str):
        try:
            payload = self.jwt_service.verify_token(refresh_token)
        except InvalidCredentialsException as e:
            raise TokenExpiredException("Invalid refresh token")
        
        if payload.get("type") != "refresh":
            raise InvalidCredentialsException("Invalid token type")


class PasswordService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)


class AuthValidationService:
    def __init__(self, repository: UserRepository, password_service: 'PasswordService') -> None:
        self.repository =  repository
        self.password_service =  password_service
                
    async def validate_unique_fields(self, email: Optional[str], phone: Optional[str]) -> Result:
        if email:
            existing_user = await self.repository.get_by_email(email)
            if existing_user:
                return Result.error("User with this email already exists")
        
        if phone:
            existing_username = await self.repository.get_by_phone(phone)
            if existing_username:
                return Result.error("User with this username already exists")
            
        return Result.success()
    
    async def authenticate_user(self, identifier_field: str, password: str) -> Optional[User]:
        user = await self._get_user_by_identifier_field(identifier_field)
        if not user: 
            return None
            
        is_password_correct = self.password_service.verify_password(password, user.hashed_password)
        if not is_password_correct:    
            return None
            
        return user
    
    async def _get_user_by_identifier_field(self, identifier_field: str) -> Optional[User]:
        user = await self.repository.get_by_email(identifier_field)
        if user:
            return user
        
        user = await self.repository.get_by_phone(identifier_field)
        if user:
            return user
        
        return None        
    