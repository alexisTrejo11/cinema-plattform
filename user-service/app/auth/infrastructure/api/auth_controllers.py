from fastapi import APIRouter, HTTPException, status, Depends
from app.users.domain import User
from app.users.application.dtos import UserResponse
from app.auth.application.dtos import (
    SignUpRequest,
    LoginRequest,
    RefreshTokenRequest,
    SessionResponse,
)
from app.auth.application.usecases import AuthUseCasesContainer
from .dependencies import get_logged_user, get_auth_use_cases

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Allows a new user to sign up by providing their details. Returns the created user's information.",
)
async def signup(
    request_body: SignUpRequest,
    use_cases: AuthUseCasesContainer = Depends(get_auth_use_cases),
):
    """
    Registers a new user.
    """
    result = await use_cases.signup.execute(request_body)
    if not result.is_success():
        raise HTTPException(status_code=400, detail=result.get_error_message())

    return result.get_data()


@router.post(
    "/login",
    response_model=SessionResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate user and get tokens",
    description="Authenticates a user with their credentials and returns access and refresh tokens.",
)
async def login(
    request_body: LoginRequest,
    use_cases: AuthUseCasesContainer = Depends(get_auth_use_cases),
):
    """
    Authenticates user and returns tokens.
    """
    result = await use_cases.login.execute(request_body)
    if not result.is_success():
        raise HTTPException(status_code=400, detail=result.get_error_message())

    return result.get_data()


@router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, str],
    summary="Log out a user from a specific session",
    description="Invalidates a specific refresh token, effectively logging out the user from that session.",
)
def logout(
    request_body: RefreshTokenRequest,
    logged_user: User = Depends(get_logged_user),
    use_cases: AuthUseCasesContainer = Depends(get_auth_use_cases),
):
    """
    Logs out a user from a specific session.
    """
    is_session_deleted = use_cases.logout.execute(
        request_body.refresh_token, logged_user.id
    )
    if not is_session_deleted:
        raise HTTPException(status_code=400, detail="Unable to logout. Token Not Found")

    return {"message": "Logged out from session successfully."}


@router.post(
    "/logout-all",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, str],
    summary="Log out user from all sessions",
    description="Invalidates all refresh tokens for the current user, logging them out from all active sessions.",
)
async def logout_all(
    logged_user: User = Depends(get_logged_user),
    use_cases: AuthUseCasesContainer = Depends(get_auth_use_cases),
):
    """
    Logs out user from all sessions.
    """
    use_cases.logout_all.execute(logged_user.id)
    return {"message": "Logged out from all sessions successfully."}


@router.post(
    "/refresh",
    response_model=SessionResponse,
    status_code=status.HTTP_200_OK,
    summary="Refresh access token",
    description="Exchanges a valid refresh token for a new access token and refresh token pair.",
)
async def refresh_session_token(
    request_body: RefreshTokenRequest,
    current_user: User = Depends(get_logged_user),
    use_cases: AuthUseCasesContainer = Depends(get_auth_use_cases),
):
    """
    Refreshes access token.
    """
    return await use_cases.refresh_token.execute(request_body, current_user)


@router.post("/send-token", response_model=User)
def resend_verification_token(user: User):
    return user


async def activate_account(
    user_id: int, use_case, logged_user: User = Depends(get_logged_user)
):
    """
    Activate a user by their ID.
    """
    await use_case.execute(user_id)
    return {"message": f"User with ID {user_id} banned successfully."}
