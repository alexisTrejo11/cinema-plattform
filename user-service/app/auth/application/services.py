from typing import Optional
from datetime import datetime
from passlib.context import CryptContext
from app.shared.response import Result
from app.users.application.repositories import UserRepository
from app.users.domain.entities import User, Status
from app.auth.domain.exceptions import TokenExpiredException, InvalidCredentialsException
from .dtos import RefreshTokenRequest, SessionResponse
from app.token.application.service import TokenService
from app.token.domain.token import TokenType

class SessionService:
    def __init__(self, token_service: TokenService) -> None:
        self.token_service = token_service

    async def create_session(self, user: User) -> SessionResponse:
        access_token_data = {"user_id" : str(user.id), "type" : TokenType.JWT_ACCESS.value }
        refresh_token_data = {"user_id" : str(user.id), "email" : user.email, "role" : user.role, "type" : TokenType.JWT_REFRESH.value }
        
        access_token = self.token_service.create(TokenType.JWT_ACCESS, **access_token_data)
        refresh_token = self.token_service.create(TokenType.JWT_REFRESH, **refresh_token_data)
        
        time_remaining = refresh_token.expires_at - datetime.now()
        expires_in_minutes = max(0, int(time_remaining.total_seconds() / 60))
        return SessionResponse(
            access_token=access_token.code,
            refresh_token=refresh_token.code,
            expires_in_minutes = expires_in_minutes
        )

    async def refresh_session(self, request: RefreshTokenRequest, user: User) -> SessionResponse:        
        access_token_data = {"user_id" : str(user.id), "type" : TokenType.JWT_ACCESS.value }
        access_token = self.token_service.create(TokenType.JWT_ACCESS ,**access_token_data)
        
        time_remaining = access_token.expires_at - datetime.now()
        expires_in_minutes = max(0, int(time_remaining.total_seconds() / 60))
        return SessionResponse(
            access_token=request.refresh_token,
            refresh_token=access_token.code,
            expires_in_minutes=expires_in_minutes
        )
        
    def validate_refresh_token(self, user_id: int,  request: RefreshTokenRequest):
        stored_token = self.token_service.get_by_code_user_and_type(str(user_id), request.refresh_token, TokenType.JWT_REFRESH)
        if not stored_token:
            raise TokenExpiredException("Invalid Token")
        
        if stored_token.is_revoked:
            raise TokenExpiredException("Refresh token expired or revoked. Request a new one")

    def revoke_user_sessions(self, user_id: int) -> None:
        self.token_service.revoke_all_refresh_by_user(str(user_id))
        
    
    def revoke_session(self, user_id: int, token: str) -> None:
        self.token_service.revoke(str(user_id), TokenType.JWT_REFRESH, token)


class AuthValidationService:
    def __init__(self, repository: UserRepository, password_service: 'PasswordService', token_service: TokenService) -> None:
        self.repository =  repository
        self.password_service =  password_service
        self.token_service = token_service
                
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
            
        is_password_correct = self.password_service.verify_password(password, user.password)
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
    
    
    def validate_account_status_for_login(self, user: User):
        if user.status == Status.BANNED:
            raise ValueError("User account is banned")
        elif user.status == Status.PENDING:
            raise ValueError("User account is not activated. Request an activate code to activate your account")
        elif user.status == Status.INACTIVE:
            user.status = Status.ACTIVE
            return

    def validate_2FA_Access(self, user_id: int, twoFAToken):
        valid_token = self.token_service.verify_token(twoFAToken, TokenType.VERIFICATION, user_id)
        if not valid_token:
            raise ValueError("Invalid or Expired Token")
        
        


class PasswordService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)


