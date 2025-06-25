from fastapi import APIRouter, Depends, HTTPException, status, Query
from .dependencies import disable_2FA_use_case, enable_2FA_use_case, two_fa_login_use_case
from .dependencies import Disable2FaUseCase, Enable2FAUseCase, TwoFALoginUseCase
from .dependencies import get_logged_user
from app.users.domain.entities import User
from app.shared.response import ApiResponse
from app.auth.application.dtos import LoginRequest

router = APIRouter(prefix="/api/v1/auth/2FA")

@router.patch("/enable", status_code=status.HTTP_200_OK, response_model=ApiResponse[tuple])
async def enable_2FA(
    logged_user: User = Depends(get_logged_user),
    usecase: Enable2FAUseCase = Depends(enable_2FA_use_case)
):
    qr_code, toptp_secret = await usecase.execute(logged_user)
    return ApiResponse.success(data=(qr_code, toptp_secret), message="2FA Auth Successfully Enabled")


@router.patch("/disable", status_code=status.HTTP_200_OK, response_model=ApiResponse)
async def disable_2FA(
    logged_user: User = Depends(get_logged_user),
    token: str = Query(default=""),
    usecase: Disable2FaUseCase = Depends(disable_2FA_use_case)
):
    await usecase.execute(logged_user, token)
    return ApiResponse.success(message="2FA Auth Successfully Disable")


# TODO: Check
@router.patch("/access", status_code=status.HTTP_200_OK, response_model=ApiResponse)
async def verify_2FA_access(
    request_body: LoginRequest,
    usecase: TwoFALoginUseCase = Depends(two_fa_login_use_case),
):
    result = await usecase.execute(request_body)
    if not result.is_success():
            raise HTTPException(status_code=400, detail=result.get_error_message())
        
    return ApiResponse.success(result.get_data(), "Login successfully proccesed.")