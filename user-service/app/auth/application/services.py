from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.auth.domain.exceptions import InvalidCredentialsException
from typing import Dict, Any, Optional
from app.shared.response import Result
from app.users.application.repositories import UserRepository
from app.users.domain.entities import User
from .dtos import RefreshTokenRequest, TokenResponse
from .repositories import SessionRepository
from app.auth.domain.entities import SessionToken
from app.auth.domain.exceptions import TokenExpiredException, InvalidCredentialsException

class PasswordService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)


class JWTService:
    def __init__(self, secret_key: str, algorithm: str = "HS256"):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = 30
        self.refresh_token_expire_days = 30
    
    def create_access_token(self, data: Dict[str, Any]) -> str:
        to_encode = data.copy()
        expire = datetime.now() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire, "type": "access"})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        to_encode = data.copy()
        expire = datetime.now() + timedelta(days=self.refresh_token_expire_days)
        to_encode.update({"exp": expire, "type": "refresh"})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            raise InvalidCredentialsException("Invalid token")
        
        
class AuthValidationService:
    def __init__(self, repository: UserRepository, password_service: PasswordService) -> None:
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
    
    
class SessionService:
    def __init__(self, jwt_service: JWTService, session_repo :SessionRepository) -> None:
        self.jwt_service = jwt_service
        self.session_repo = session_repo

    async def create_session(self, user: User) -> TokenResponse:
        token_data: Dict[str, Any] = {"sub": user.id, "email": user.email, "role": user.role}
        access_token = self.jwt_service.create_access_token(token_data)
        refresh_token = self.jwt_service.create_refresh_token({"sub": user.id})
        
        refresh_token_entity = SessionToken(
            user_id=user.id,
            token=refresh_token,
            expires_at=datetime.now() + timedelta(days=30)
        )
        
        await self.session_repo.create(refresh_token_entity)
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=self.jwt_service.access_token_expire_minutes * 60
        )

    async def refresh_session(self, request: RefreshTokenRequest, user: User) -> TokenResponse:
        self._valdiate_refresh_token(request.refresh_token)
        
        stored_token = await self.session_repo.get_user_token(str(user.id), request.refresh_token)
        if not stored_token or not stored_token.is_valid():
            raise TokenExpiredException("Refresh token expired or revoked")
        
        access_token = self.jwt_service.create_access_token(
            data={"sub": user.id, "email": user.email, "role": user.role}
        )
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=request.refresh_token,
            expires_in=self.jwt_service.access_token_expire_minutes * 60
        )
        
    def _valdiate_refresh_token(self, refresh_token: str):
        try:
            payload = self.jwt_service.verify_token(refresh_token)
        except InvalidCredentialsException:
            raise TokenExpiredException("Invalid refresh token")
        
        if payload.get("type") != "refresh":
            raise InvalidCredentialsException("Invalid token type")
    
