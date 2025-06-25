from fastapi import APIRouter

router = APIRouter(prefix="/v1/api/auth/2FA")

@router.patch("/enable-2FA")
def enable_2FA():
    pass

@router.patch("/disable-2FA")
def disable_2FA():
    pass

@router.patch("/send_verification")
def send_2FA_verfication():
    pass
