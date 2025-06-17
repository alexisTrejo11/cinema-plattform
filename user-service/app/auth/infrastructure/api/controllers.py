from fastapi import APIRouter, HTTPException, status, Depends
from app.users.domain.exceptions import *
from app.auth.domain.exceptions import *
from app.users.application.dtos import UserResponse
from app.users.domain.entities import User
from app.auth.application.dtos import SignUpRequest, LoginRequest, TokenResponse, RefreshTokenRequest
from app.auth.application.use_cases import SignUpUseCase, LoginUseCase, RefreshTokenUseCase, LogoutAllUseCase, LogoutUseCase
from .dependencies import get_logged_user, signup_use_case, login_use_case, logout_use_case, logout_all_use_case, refresh_token_use_case

router = APIRouter(prefix="/api/v1/auth")

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    request: SignUpRequest,
    use_case: SignUpUseCase = Depends(signup_use_case)
):
    result = await use_case.execute(request)
    if not result.is_success():
        raise HTTPException(status_code=400, detail=result.get_error_message())

    return result.get_data()


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    use_case: LoginUseCase = Depends(login_use_case),
):
    result = await use_case.execute(request)
    if not result.is_success():
        raise HTTPException(status_code=400, detail=result.get_error_message())
    
    return result.get_data()

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    request: RefreshTokenRequest,
    logged_user: User = Depends(get_logged_user),
    use_case: LogoutUseCase = Depends(logout_use_case),
):
    is_season_deleted = use_case.execute(request.refresh_token, logged_user.id)
    if not is_season_deleted:
        raise HTTPException(status_code=400, detail="Unable to logout. Token Not Found")
    
    return

@router.post("/logout-all", status_code=status.HTTP_204_NO_CONTENT)
async def logout_all(
    logged_user: User = Depends(get_logged_user),
    use_case: LogoutAllUseCase = Depends(logout_all_use_case),
):
    use_case.execute(logged_user.id)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    current_user: User = Depends(get_logged_user),
    use_case: RefreshTokenUseCase = Depends(refresh_token_use_case)
):
    return await use_case.execute(request, current_user)
