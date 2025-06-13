from fastapi import FastAPI, HTTPException, status, Depends
from app.users.application.dtos import UserResponse
from app.auth.application.dtos import SignUpRequest, LoginRequest, TokenResponse, RefreshTokenRequest
from app.auth.application.use_cases import SignUpUseCase, LoginUseCase, RefreshTokenUseCase, LogoutAllUseCase, LogoutUseCase
from app.auth.domain.exceptions import *
from app.users.domain.exceptions import *
from app.users.domain.entities import User
from app.auth.infrastructure.controllers.dependencies import get_current_user

app = FastAPI()

@app.post("/auth/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    request: SignUpRequest,
    use_case: SignUpUseCase
):
    try:
        return await use_case.execute(request)
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/auth/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    use_case: LoginUseCase,
):
    try:
        return await use_case.execute(request)
    except InvalidCredentialsException as e:
        raise HTTPException(status_code=401, detail=str(e))


@app.post("/auth/refresh", response_model=TokenResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    use_case: RefreshTokenUseCase
):
    try:
        return await use_case.execute(request)
    except (TokenExpiredException, UserNotFoundException, InvalidCredentialsException) as e:
        raise HTTPException(status_code=401, detail=str(e))


@app.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    request: RefreshTokenRequest,
    use_case: LogoutUseCase,
):
    await use_case.execute(request.refresh_token)


@app.post("/auth/logout-all", status_code=status.HTTP_204_NO_CONTENT)
async def logout_all(
    current_user: User = Depends(get_current_user),
    use_case: LogoutAllUseCase,
):
    await use_case.execute(current_user.user_id)

