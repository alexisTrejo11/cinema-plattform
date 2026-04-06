from fastapi import APIRouter, Depends, status

from app.shared.auth import AuthUserContext, get_current_user
from app.wallet.application.queries import (
    GetWalletByUserIdQuery,
    WalletSummaryQuery,
)
from app.wallet.domain.value_objects import UserId
from app.wallet.presentation.dependencies import WalletUseCases, get_wallet_uc
from app.wallet.presentation.dtos.query_params import (
    WalletPagedQueryParams,
    WalletTransactionListQueryParams,
)
from app.wallet.presentation.dtos.request import UserWalletOperationRequest
from app.wallet.presentation.mappers import (
    map_user_wallet_operation_to_add_credit_command,
    map_user_wallet_operation_to_pay_command,
)
from app.wallet.presentation.dtos.response import (
    BuyCreditDetails,
    WalletBuyDetails,
    WalletResponse,
    WalletSummaryResponse,
    WalletTransactionResponse,
)

router = APIRouter(prefix="/api/v2/wallets/users", tags=["Wallet — customer"])


@router.get("/summary", response_model=WalletSummaryResponse)
async def get_my_wallet_summary(
    user: AuthUserContext = Depends(get_current_user),
    wallet_use_cases: WalletUseCases = Depends(get_wallet_uc),
) -> WalletSummaryResponse:
    q = WalletSummaryQuery(userId=UserId(value=user.id))
    result = await wallet_use_cases.get_wallet_summary(q)
    return WalletSummaryResponse.from_result(result)


@router.get("/", response_model=WalletResponse)
async def get_my_wallet(
    user: AuthUserContext = Depends(get_current_user),
    params: WalletPagedQueryParams = Depends(),
    wallet_use_cases: WalletUseCases = Depends(get_wallet_uc),
) -> WalletResponse:
    query = params.to_get_wallet_by_user_id_query(user.id)
    wallet = await wallet_use_cases.get_wallets_by_user_id(query)
    return WalletResponse.from_domain(wallet)


@router.get("/transactions", response_model=list[WalletTransactionResponse])
async def get_my_wallet_transactions(
    user: AuthUserContext = Depends(get_current_user),
    list_params: WalletTransactionListQueryParams = Depends(),
    wallet_use_cases: WalletUseCases = Depends(get_wallet_uc),
) -> list[WalletTransactionResponse]:
    wq = GetWalletByUserIdQuery(
        userId=UserId(value=user.id),
        include_transactions=False,
    )
    wallet = await wallet_use_cases.get_wallets_by_user_id(wq)
    tq = list_params.to_transaction_by_wallet_query(wallet.id)
    txs = await wallet_use_cases.list_wallet_transactions(tq)
    return [WalletTransactionResponse.from_domain(t) for t in txs]


@router.post(
    "/transactions/add-credit",
    response_model=BuyCreditDetails,
    status_code=status.HTTP_200_OK,
)
async def add_credit(
    body: UserWalletOperationRequest,
    user: AuthUserContext = Depends(get_current_user),
    wallet_use_cases: WalletUseCases = Depends(get_wallet_uc),
) -> BuyCreditDetails:
    wq = GetWalletByUserIdQuery(
        userId=UserId(value=user.id),
        include_transactions=False,
    )
    wallet = await wallet_use_cases.get_wallets_by_user_id(wq)
    command = map_user_wallet_operation_to_add_credit_command(body, wallet.id)
    outcome = await wallet_use_cases.add_credit(command)
    return BuyCreditDetails.from_domain(outcome.wallet, outcome.transaction)


@router.post(
    "/transactions/pay",
    response_model=WalletBuyDetails,
    status_code=status.HTTP_200_OK,
)
async def pay(
    body: UserWalletOperationRequest,
    user: AuthUserContext = Depends(get_current_user),
    wallet_use_cases: WalletUseCases = Depends(get_wallet_uc),
) -> WalletBuyDetails:
    wq = GetWalletByUserIdQuery(
        userId=UserId(value=user.id),
        include_transactions=False,
    )
    wallet = await wallet_use_cases.get_wallets_by_user_id(wq)
    command = map_user_wallet_operation_to_pay_command(body, wallet.id)
    outcome = await wallet_use_cases.pay(command)
    return WalletBuyDetails.generate(outcome.wallet, outcome.transaction)
