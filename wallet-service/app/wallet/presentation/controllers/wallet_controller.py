from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.shared.auth import get_current_user, AuthUserContext
from ..docs.walley_docs import *
from app.wallet.application.commands import CreateWalletCommand
from ..dtos.response import BuyCreditDetails, WalletResponse, WalletBuyDetails
from ..dtos.request import WalletOperationRequest
from ..dtos.query_params import WalletPagedQueryParams
from ..dependencies import get_wallet_uc, WalletUseCases
from ..mappers import (
    map_wallet_operation_to_add_credit_command,
    map_wallet_operation_to_pay_command,
)
from app.shared.documentation import (
    common_wallet_error_responses as common_error_responses,
)

router = APIRouter(prefix="/api/v2/wallets", tags=["Wallets Staff Management"])


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
    params: WalletPagedQueryParams = Depends(),
    user: AuthUserContext = Depends(get_current_user),
    wallet_use_cases: WalletUseCases = Depends(get_wallet_uc),
):
    """
    Retrieves a wallet by its ID.
    """
    query = params.to_get_wallet_by_id_query(wallet_id)

    wallet = await wallet_use_cases.get_wallet_by_id(query)
    return WalletResponse.from_domain(wallet)


@router.get(
    "/user/{user_id}",
    response_model=WalletResponse,
    summary=walleyByUserIdDoc["summary"],
    description=walleyByUserIdDoc["description"],
    status_code=status.HTTP_200_OK,
    responses=walleyByUserIdDoc["responses"],
)
async def get_user_wallet(
    user_id: UUID,
    params: WalletPagedQueryParams = Depends(),
    wallet_use_cases: WalletUseCases = Depends(get_wallet_uc),
    user: AuthUserContext = Depends(get_current_user),
):
    """
    Retrieves a wallet by its associated user ID.
    """
    query = params.to_get_wallet_by_user_id_query(user_id)
    wallet = await wallet_use_cases.get_wallets_by_user_id(query)
    return WalletResponse.from_domain(wallet)


@router.post(
    "/user/{user_id}",
    response_model=WalletResponse,
    summary="Create a New Wallet for a User manually. This proccess is doing by a queue worker",
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
    wallet = await wallet_use_cases.create_wallet(command)
    return WalletResponse.from_domain(wallet)


@router.post(
    "/add-credit",
    response_model=BuyCreditDetails,
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
    Acts an orchestrator for the payment process.
    """

    command = map_wallet_operation_to_add_credit_command(request_dto)
    outcome = await wallet_use_cases.add_credit(command)
    return BuyCreditDetails.from_domain(outcome.wallet, outcome.transaction)


@router.post(
    "/pay",
    status_code=status.HTTP_200_OK,
    response_model=WalletBuyDetails,
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
    command = map_wallet_operation_to_pay_command(request_dto)
    outcome = await wallet_use_cases.pay(command)
    return WalletBuyDetails.generate(outcome.wallet, outcome.transaction)
