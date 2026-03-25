from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.auth.application.usecases import AuthUseCasesContainer
from app.users.domain import User
from app.auth.application.dtos import LoginRequest
from .dependencies import get_auth_use_cases, get_logged_user

router = APIRouter(prefix="/api/v2/auth/2FA")


@router.patch("/enable", status_code=status.HTTP_200_OK, response_model=dict[str, str])
async def enable_2FA(
    logged_user: User = Depends(get_logged_user),
    use_cases: AuthUseCasesContainer = Depends(get_auth_use_cases),
):
    qr_code, toptp_secret = await use_cases.enable_2fa.execute(logged_user)
    return {"qr_code": qr_code, "secret": toptp_secret}


@router.patch("/disable", status_code=status.HTTP_200_OK, response_model=dict[str, str])
async def disable_2FA(
    logged_user: User = Depends(get_logged_user),
    token: str = Query(default=""),
    use_cases: AuthUseCasesContainer = Depends(get_auth_use_cases),
):
    await use_cases.disable_2fa.execute(logged_user, token)
    return {"message": "2FA Auth Successfully Disable"}


# TODO: Check
@router.patch("/access", status_code=status.HTTP_200_OK)
async def verify_2FA_access(
    request_body: LoginRequest,
    use_cases: AuthUseCasesContainer = Depends(get_auth_use_cases),
):
    result = await use_cases.two_fa_login.execute(request_body)
    if not result.is_success():
        raise HTTPException(status_code=400, detail=result.get_error_message())

    return result.get_data()
