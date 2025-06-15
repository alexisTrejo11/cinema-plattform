from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from config.postgres_config import get_db

from app.users.infrastructure.persistence.sql_alchemy_user_repo import SQLAlchemyUserRepository
from app.users.infrastructure.persistence.redis_session_repo import RedisSessionRepository
from app.users.application.repositories import UserRepository
from app.auth.application.repositories import SessionRepository
from app.auth.application.use_cases import SignUpUseCase, LoginUseCase, LogoutAllUseCase, LogoutUseCase, RefreshTokenUseCase
from app.users.domain.entities import User
from app.auth.application.services import JWTService, PasswordService, AuthValidationService, SessionService
from app.auth.domain.exceptions import InvalidCredentialsException
from config.redis_config import get_redis_client, redis

security = HTTPBearer()

def get_user_repository(session: AsyncSession = Depends(get_db)) -> UserRepository:
    return SQLAlchemyUserRepository(session)

def get_refresh_token_repository(redisConn: redis.Redis = Depends(get_redis_client)) -> SessionRepository:
    return RedisSessionRepository(redisConn)

def get_password_service() -> PasswordService:
    return PasswordService()

def get_jwt_service() -> JWTService:
    return JWTService(secret_key="your-secret-key-here")

def signup_use_case(session: AsyncSession = Depends(get_db)) -> SignUpUseCase:
    repo = SQLAlchemyUserRepository(session)
    pw_service = PasswordService()
    validation_service = AuthValidationService(repo,pw_service)
    
    return SignUpUseCase(repo, pw_service, validation_service)

def login_use_case(session: AsyncSession = Depends(get_db), redisConn: redis.Redis = Depends(get_redis_client)) -> LoginUseCase:
    user_repo = SQLAlchemyUserRepository(session)
    session_repo = RedisSessionRepository(redisConn)
    
    pw_service = PasswordService()
    validation_service = AuthValidationService(user_repo, pw_service) 
    jwt_service = JWTService(secret_key="your-secret-key-here")
    
    session_service = SessionService(jwt_service, session_repo)
    
    return LoginUseCase(session_service, validation_service)

def logout_use_case(redisConn: redis.Redis = Depends(get_redis_client)) -> LogoutUseCase:
    session_repo= RedisSessionRepository(redisConn)
    return LogoutUseCase(session_repo)

def logout_all_use_case( redisConn: redis.Redis = Depends(get_redis_client)) -> LogoutAllUseCase:
    session_repo= RedisSessionRepository(redisConn)
    return LogoutAllUseCase(session_repo)

def refresh_token_use_case( redisConn: redis.Redis = Depends(get_redis_client)) -> RefreshTokenUseCase:
    session_repo = RedisSessionRepository(redisConn)
    
    jwt_service = JWTService(secret_key="your-secret-key-here")
    session_service = SessionService(jwt_service, session_repo)
    
    return RefreshTokenUseCase(session_service)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_repository: UserRepository = Depends(get_user_repository),
    jwt_service: JWTService = Depends(get_jwt_service)
) -> User:
    try:
        payload = jwt_service.verify_token(credentials.credentials)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user = await user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user
    except InvalidCredentialsException:
        raise HTTPException(status_code=401, detail="Invalid token")