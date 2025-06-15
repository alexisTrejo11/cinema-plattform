from fastapi import APIRouter, HTTPException, status, Depends
from app.users.application.dtos import UserResponse
from app.users.domain.exceptions import *
from app.users.domain.entities import User
from app.auth.domain.exceptions import *
from app.auth.application.dtos import SignUpRequest, LoginRequest, TokenResponse, RefreshTokenRequest
from app.auth.application.use_cases import SignUpUseCase, LoginUseCase, RefreshTokenUseCase, LogoutAllUseCase, LogoutUseCase
from .dependencies import get_current_user, signup_use_case, login_use_case, logout_use_case, logout_all_use_case, refresh_token_use_case

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
async def logout(
    request: RefreshTokenRequest,
    use_case: LogoutUseCase = Depends(logout_use_case),
):
    await use_case.execute(request.refresh_token)


@router.post("/logout-all", status_code=status.HTTP_204_NO_CONTENT)
async def logout_all(
    current_user: User = Depends(get_current_user),
    use_case: LogoutAllUseCase = Depends(logout_all_use_case),
):
    await use_case.execute(current_user.id)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    current_user: User = Depends(get_current_user),
    use_case: RefreshTokenUseCase = Depends(refresh_token_use_case)
):
    try:
        return await use_case.execute(request, current_user)
    except (TokenExpiredException, UserNotFoundException, InvalidCredentialsException) as e:
        raise HTTPException(status_code=401, detail=str(e))
