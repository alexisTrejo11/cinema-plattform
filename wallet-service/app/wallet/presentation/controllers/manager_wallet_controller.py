from fastapi import APIRouter, Depends

from app.shared.auth import AuthUserContext, require_staff_user
from app.wallet.presentation.dependencies import WalletUseCases, get_wallet_uc
from app.wallet.presentation.dtos.query_params import (
    WalletManagementSummaryQueryParams,
    get_wallet_management_summary_params,
)
from app.wallet.presentation.dtos.response import WalletSummaryResponse

router = APIRouter(
    prefix="/api/v2/wallets/management",
    tags=["Wallet — management"],
)


@router.get("/summary", response_model=WalletSummaryResponse)
async def get_wallet_summary_for_staff(
    params: WalletManagementSummaryQueryParams = Depends(
        get_wallet_management_summary_params
    ),
    _: AuthUserContext = Depends(require_staff_user),
    wallet_use_cases: WalletUseCases = Depends(get_wallet_uc),
) -> WalletSummaryResponse:
    result = await wallet_use_cases.get_wallet_summary(params.to_wallet_summary_query())
    return WalletSummaryResponse.from_result(result)
