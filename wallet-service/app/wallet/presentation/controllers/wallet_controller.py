from typing import Optional
import logging
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status

from app.shared.auth import get_current_user, AuthUserContext
from ..docs.walley_docs import *
from app.wallet.application.commands import (
    PayWithWalletCommand,
    AddCreditCommand,
    CreateWalletCommand,
)
from app.wallet.application.queries import (
    GetWalletByIdQuery,
    GetWalletByUserIdQuery,
)

from ..dtos.response import WalletResponse, WalletBuyResponse
from ..dtos.request import WalletOperationRequest
from ..dependencies import get_wallet_uc, WalletUseCases
from app.shared.documentation import (
    common_wallet_error_responses as common_error_responses,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v2/wallets", tags=["Wallets"])


@router.get(
    "/{wallet_id}",
    response_model=WalletResponse,
    summary=walleyByIdDoc["summary"],
    description=walleyByIdDoc["description"],
    status_code=status.HTTP_200_OK,
    responses=walleyByIdDoc["responses"],
)
async def get_wallet(
    wallet_id: UUID,
    include_transactions: bool = Query(
        default=False,
        description="If true, includes the latest transactions for the wallet. Default is false.",
    ),
    offset: Optional[int] = Query(
        default=0,
        ge=0,
        description="Offset for paginating transactions, used with `include_transactions=true`.",
    ),
    limit: Optional[int] = Query(
        default=10,
        gt=0,
        le=100,
        description="Limit for the number of transactions to return, used with `include_transactions=true`.",
    ),
    user: AuthUserContext = Depends(get_current_user),
    wallet_use_cases: WalletUseCases = Depends(get_wallet_uc),
):
    """
    Retrieves a wallet by its ID.
    """
    query = GetWalletByIdQuery.from_request(
        wallet_id, include_transactions, limit, offset
    )

    wallet_response = await wallet_use_cases.get_wallet_by_id(query)

    return wallet_response


@router.get(
    "/user/{user_id}",
    response_model=[WalletResponse],
    summary=walleyByUserIdDoc["summary"],
    description=walleyByUserIdDoc["description"],
    status_code=status.HTTP_200_OK,
    responses=walleyByUserIdDoc["responses"],
)
async def get_user_wallet(
    user_id: UUID,
    include_transactions: bool = Query(
        default=False,
        description="If true, includes the latest transactions for the wallet. Default is false.",
    ),
    offset: Optional[int] = Query(
        default=0,
        ge=0,
        description="Offset for paginating transactions, used with `include_transactions=true`.",
    ),
    limit: Optional[int] = Query(
        default=10,
        gt=0,
        le=100,
        description="Limit for the number of transactions to return, used with `include_transactions=true`.",
    ),
    user: AuthUserContext = Depends(get_current_user),
    wallet_use_cases: WalletUseCases = Depends(get_wallet_uc),
):
    """
    Retrieves a wallet by its associated user ID.
    """
    query = GetWalletByUserIdQuery.from_request(
        user_id, include_transactions, limit, offset
    )
    return await wallet_use_cases.get_wallets_by_user_id(query)


@router.post(
    "/user/{user_id}",
    response_model=[WalletResponse],
    summary="Create a New Wallet for a User",
    description="""
    Creates a new wallet for a specified user ID.

    This endpoint requires authentication as an employee.
    A user can typically only have one wallet. If a wallet already exists for the user,
    a 400 Bad Request error will be returned.
    """,
    status_code=status.HTTP_201_CREATED,
    responses=common_error_responses,
)
async def create_wallet(
    user_id: UUID,
    wallet_use_cases: WalletUseCases = Depends(get_wallet_uc),
    user: AuthUserContext = Depends(get_current_user),
):
    """
    Creates a new wallet for a user.
    """
    command = CreateWalletCommand.from_uuid(user_id)
    return await wallet_use_cases.create_wallet(command)


@router.post(
    "/add-credit",
    response_model=[WalletBuyResponse],
    status_code=status.HTTP_200_OK,
    summary=addCreditDoc["summary"],
    description=addCreditDoc["description"],
    responses=addCreditDoc["responses"],
)
async def recharge_credit(
    request_dto: WalletOperationRequest,
    wallet_use_cases: WalletUseCases = Depends(get_wallet_uc),
    user: AuthUserContext = Depends(get_current_user),
):
    """
    Adds credit to a wallet based on the provided operation details.
    """

    command = AddCreditCommand.from_request(request_dto)
    operation_response = await wallet_use_cases.add_credit(command)

    return operation_response


@router.post(
    "/pay",
    status_code=status.HTTP_200_OK,
    response_model=[WalletBuyResponse],
    summary=payCartDoc["summary"],
    description=payCartDoc["description"],
    responses=payCartDoc["responses"],
)
async def pay(
    request_dto: WalletOperationRequest,
    wallet_use_cases: WalletUseCases = Depends(get_wallet_uc),
    user: AuthUserContext = Depends(get_current_user),
):
    """
    Makes a payment from a wallet.
    """
    command = PayWithWalletCommand.from_request(request_dto)
    pay_response = await wallet_use_cases.pay(command)
    return pay_response
