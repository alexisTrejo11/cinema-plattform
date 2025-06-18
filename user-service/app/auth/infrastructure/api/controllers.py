from fastapi import APIRouter, HTTPException, status, Depends, Request
from app.users.domain.exceptions import *
from app.auth.domain.exceptions import *
from app.users.domain.entities import User
from app.users.application.dtos import UserResponse
from app.auth.application.dtos import SignUpRequest, LoginRequest, TokenResponse, RefreshTokenRequest
from app.auth.application.use_cases import SignUpUseCase, LoginUseCase, RefreshTokenUseCase, LogoutAllUseCase, LogoutUseCase
from .dependencies import get_logged_user, signup_use_case, login_use_case, logout_use_case, logout_all_use_case, refresh_token_use_case
import logging

logger = logging.getLogger("app")
router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    request_body: SignUpRequest,
    request: Request,
    use_case: SignUpUseCase = Depends(signup_use_case)
):
    logger.info(f"POST signup started | email:{request_body.email} | client:{request.client.host if request.client else None}")
    try:
        result = await use_case.execute(request_body)
        if not result.is_success():
            logger.warning(f"POST signup failed | email:{request_body.email} | reason:{result.get_error_message()}")
            raise HTTPException(status_code=400, detail=result.get_error_message())
        
        logger.info(f"POST signup success | user_id:{result.get_data().id} | email:{request_body.email}")
        return result.get_data()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"POST signup failed | email:{request_body.email} | error:{str(e)}")
        raise


@router.post("/login", response_model=TokenResponse)
async def login(
    request_body: LoginRequest,
    request: Request,
    use_case: LoginUseCase = Depends(login_use_case),
):
    logger.info(f"POST login started | identifier_field:{request_body.identifier_field} | client:{request.client.host if request.client else None}")
    try:
        result = await use_case.execute(request_body)
        if not result.is_success():
            logger.warning(f"POST login failed | identifier_field:{request_body.identifier_field} | reason:{result.get_error_message()}")
            raise HTTPException(status_code=400, detail=result.get_error_message())
        
        logger.info(f"POST login success | identifier_field:{request_body.identifier_field}")
        return result.get_data()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"POST login failed | identifier_field:{request_body.identifier_field} | error:{str(e)}")
        raise

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    request_body: RefreshTokenRequest,
    request: Request,
    logged_user: User = Depends(get_logged_user),
    use_case: LogoutUseCase = Depends(logout_use_case),
):
    logger.info(f"POST logout started | user_id:{logged_user.id} | client:{request.client.host if request.client else None}")
    try:
        is_season_deleted = use_case.execute(request_body.refresh_token, logged_user.id)
        if not is_season_deleted:
            logger.warning(f"POST logout failed | user_id:{logged_user.id} | reason: Unable to logout. Token Not Found")
            raise HTTPException(status_code=400, detail="Unable to logout. Token Not Found")
        
        logger.info(f"POST logout success | user_id:{logged_user.id}")
        return
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"POST logout failed | user_id:{logged_user.id} | error:{str(e)}")
        raise

@router.post("/logout-all", status_code=status.HTTP_204_NO_CONTENT)
async def logout_all(
    request: Request,
    logged_user: User = Depends(get_logged_user),
    use_case: LogoutAllUseCase = Depends(logout_all_use_case),
):
    logger.info(f"POST logout-all started | user_id:{logged_user.id} | client:{request.client.host if request.client else None}")
    try:
        use_case.execute(logged_user.id)
        logger.info(f"POST logout-all success | user_id:{logged_user.id}")
    except Exception as e:
        logger.error(f"POST logout-all failed | user_id:{logged_user.id} | error:{str(e)}")
        raise


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request_body: RefreshTokenRequest,
    request: Request,
    current_user: User = Depends(get_logged_user),
    use_case: RefreshTokenUseCase = Depends(refresh_token_use_case)
):
    logger.info(f"POST refresh started | user_id:{current_user.id} | client:{request.client.host if request.client else None}")
    try:
        token_response = await use_case.execute(request_body, current_user)
        logger.info(f"POST refresh success | user_id:{current_user.id}")
        return token_response
    except Exception as e:
        logger.error(f"POST refresh failed | user_id:{current_user.id} | error:{str(e)}")
        raise