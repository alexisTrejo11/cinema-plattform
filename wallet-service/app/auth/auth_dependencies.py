from app.user.presentation.dependencies import get_user_repository, UserRepository
from typing import List, Callable
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.user.domain.user import User, UserRole
from .jwt_service import AuthorizationException, JWTTokenService
from config.app_config import settings

security = HTTPBearer()


def get_token_service() -> JWTTokenService:
    """
    Dependency that provides an instance of TokenService,
    initialized with the secret key from your application settings.
    """
    return JWTTokenService(
        secret_key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )


# --- User Authorization Dependency ---
async def get_logged_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_repository: UserRepository = Depends(get_user_repository),
    token_service: JWTTokenService = Depends(get_token_service),
) -> User:
    try:
        payload = token_service.verify_jwt_token(credentials.credentials)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

        user = await user_repository.get_by_id(str(user_id))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )

        return user
    except AuthorizationException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or credentials",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication error: {e}",
        )


def role_required(required_roles: List[UserRole]) -> Callable[[User], User]:
    """
    Dependency factory to check if the current user has any of the specified roles.
    """

    def role_checker(logged_user: User = Depends(get_logged_user)) -> User:
        if logged_user.get_roles not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Not enough permissions. Required roles: {[r.value for r in required_roles]}",
            )
        return logged_user

    return role_checker


def get_logged_admin_user(
    logged_user: User = Depends(role_required([UserRole.ADMIN])),
) -> User:
    return logged_user


def get_logged_manager_user(
    logged_user: User = Depends(role_required([UserRole.MANAGER, UserRole.ADMIN]))
) -> User:
    return logged_user


def get_staff_user(
    logged_user: User = Depends(
        role_required([UserRole.MANAGER, UserRole.ADMIN, UserRole.EMPLOYEE])
    )
) -> User:
    return logged_user


def get_customer_user(
    logged_user: User = Depends(
        role_required([UserRole.MANAGER, UserRole.CUSTOMER, UserRole.ADMIN])
    )
) -> User:
    return logged_user
