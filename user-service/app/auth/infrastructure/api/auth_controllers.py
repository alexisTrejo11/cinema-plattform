from fastapi import APIRouter, HTTPException, status, Depends, Request
from app.shared.response import ApiResponse, ErrorResponse
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

common_auth_error_responses = {
    400: {"model": ApiResponse[ErrorResponse], "description": "Bad Request - Invalid input or business rule violation."},
    401: {"model": ApiResponse[ErrorResponse], "description": "Unauthorized - Authentication required or failed (e.g., invalid credentials, missing token)."},
    403: {"model": ApiResponse[ErrorResponse], "description": "Forbidden - User does not have the necessary permissions."},
    500: {"model": ApiResponse[ErrorResponse], "description": "Internal Server Error - An unexpected server error occurred."}
}

@router.post(
    "/signup",
    response_model=ApiResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Allows a new user to sign up by providing their details. Returns the created user's information.",
    responses={
        201: {"model": ApiResponse[UserResponse], "description": "User successfully registered."},
        400: {"model": ApiResponse[ErrorResponse], "description": "Bad Request - Invalid signup data or user with provided email already exists."},
        409: {"model": ApiResponse[ErrorResponse], "description": "Conflict - User with the provided email already exists."},
        **common_auth_error_responses
    }
)
async def signup(
    request_body: SignUpRequest,
    request: Request,
    use_case: SignUpUseCase = Depends(signup_use_case)
):
    """
    Registers a new user.
    """
    logger.info(f"POST signup started | email:{request_body.email} | client:{request.client.host if request.client else None}")
    try:
        result = await use_case.execute(request_body)
        if not result.is_success():
            logger.warning(f"POST signup failed | email:{request_body.email} | reason:{result.get_error_message()}")
            raise HTTPException(status_code=400, detail=result.get_error_message())
        
        user = result.get_data()
        logger.info(f"POST signup success | user_id:{user.id} | email:{request_body.email}")
        return ApiResponse.success(user, "User successfully registered.")
    except Exception as e:
        logger.error(f"POST signup failed | email:{request_body.email} | error:{str(e)}")
        raise

@router.post(
    "/login",
    response_model=ApiResponse[TokenResponse],
    status_code=status.HTTP_200_OK,
    summary="Authenticate user and get tokens",
    description="Authenticates a user with their credentials and returns access and refresh tokens.",
    responses={
        200: {"model": ApiResponse[TokenResponse], "description": "Successfully authenticated and tokens issued."},
        400: {"model": ApiResponse[ErrorResponse], "description": "Bad Request - Invalid credentials provided."},
        401: {"model": ApiResponse[ErrorResponse], "description": "Unauthorized - Invalid identifier or password."},
        **common_auth_error_responses
    }
)
async def login(
    request_body: LoginRequest,
    request: Request,
    use_case: LoginUseCase = Depends(login_use_case),
):
    """
    Authenticates user and returns tokens.
    """
    logger.info(f"POST login started | identifier_field:{request_body.identifier_field} | client:{request.client.host if request.client else None}")
    try:
        result = await use_case.execute(request_body)
        if not result.is_success():
            logger.warning(f"POST login failed | identifier_field:{request_body.identifier_field} | reason:{result.get_error_message()}")
            raise HTTPException(status_code=400, detail=result.get_error_message())
        
        token_response = result.get_data()
        logger.info(f"POST login success | identifier_field:{request_body.identifier_field}")
        return ApiResponse.success(token_response, "Login successful.")
    except Exception as e:
        logger.error(f"POST login failed | identifier_field:{request_body.identifier_field} | error:{str(e)}")
        raise

@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[None],
    summary="Log out a user from a specific session",
    description="Invalidates a specific refresh token, effectively logging out the user from that session.",
    responses={
        200: {"model": ApiResponse[None], "description": "Successfully logged out from the session."},
        400: {"model": ApiResponse[ErrorResponse], "description": "Bad Request - Invalid refresh token or session not found."},
        401: {"model": ApiResponse[ErrorResponse], "description": "Unauthorized - Missing or invalid access token."},
        **common_auth_error_responses
    }
)
def logout(
    request_body: RefreshTokenRequest,
    request: Request,
    logged_user: User = Depends(get_logged_user),
    use_case: LogoutUseCase = Depends(logout_use_case),
):
    """
    Logs out a user from a specific session.
    """
    logger.info(f"POST logout started | user_id:{logged_user.id} | client:{request.client.host if request.client else None}")
    try:
        is_session_deleted = use_case.execute(request_body.refresh_token, logged_user.id)
        if not is_session_deleted:
            logger.warning(f"POST logout failed | user_id:{logged_user.id} | reason: Unable to logout. Token Not Found")
            raise HTTPException(status_code=400, detail="Unable to logout. Token Not Found")
        
        logger.info(f"POST logout success | user_id:{logged_user.id}")
        return ApiResponse.success(None, "Logged out from session successfully.")
    except Exception as e:
        logger.error(f"POST logout failed | user_id:{logged_user.id} | error:{str(e)}")
        raise

@router.post(
    "/logout-all",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[None],
    summary="Log out user from all sessions",
    description="Invalidates all refresh tokens for the current user, logging them out from all active sessions.",
    responses={
        200: {"model": ApiResponse[None], "description": "Successfully logged out from all sessions."},
        401: {"model": ApiResponse[ErrorResponse], "description": "Unauthorized - Missing or invalid access token."},
        **common_auth_error_responses
    }
)
async def logout_all(
    request: Request,
    logged_user: User = Depends(get_logged_user),
    use_case: LogoutAllUseCase = Depends(logout_all_use_case),
):
    """
    Logs out user from all sessions.
    """
    logger.info(f"POST logout-all started | user_id:{logged_user.id} | client:{request.client.host if request.client else None}")
    try:
        use_case.execute(logged_user.id)
        logger.info(f"POST logout-all success | user_id:{logged_user.id}")
        return ApiResponse.success(None, "Logged out from all sessions successfully.")
    except Exception as e:
        logger.error(f"POST logout-all failed | user_id:{logged_user.id} | error:{str(e)}")
        raise

@router.post(
    "/refresh",
    response_model=ApiResponse[TokenResponse],
    status_code=status.HTTP_200_OK,
    summary="Refresh access token",
    description="Exchanges a valid refresh token for a new access token and refresh token pair.",
    responses={
        200: {"model": ApiResponse[TokenResponse], "description": "Successfully refreshed tokens."},
        400: {"model": ApiResponse[ErrorResponse], "description": "Bad Request - Invalid or expired refresh token."},
        401: {"model": ApiResponse[ErrorResponse], "description": "Unauthorized - Missing or invalid access token."},
        **common_auth_error_responses
    }
)
async def refresh_token(
    request_body: RefreshTokenRequest,
    request: Request,
    current_user: User = Depends(get_logged_user),
    use_case: RefreshTokenUseCase = Depends(refresh_token_use_case)
):
    """
    Refreshes access token.
    """
    logger.info(f"POST refresh started | user_id:{current_user.id} | client:{request.client.host if request.client else None}")
    try:
        token_response = await use_case.execute(request_body, current_user)
        logger.info(f"POST refresh success | user_id:{current_user.id}")
        return ApiResponse.success(token_response, "Tokens refreshed successfully.")
    except Exception as e:
        logger.error(f"POST refresh failed | user_id:{current_user.id} | error:{str(e)}")
        raise