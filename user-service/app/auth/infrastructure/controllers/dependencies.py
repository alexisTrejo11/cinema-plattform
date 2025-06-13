

def get_user_repository() -> UserRepository:
    return InMemoryUserRepository()

def get_refresh_token_repository() -> RefreshTokenRepository:
    return InMemoryRefreshTokenRepository()

def get_password_service() -> PasswordService:
    return PasswordService()

def get_jwt_service() -> JWTService:
    # In production, use environment variables
    return JWTService(secret_key="your-secret-key-here")


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