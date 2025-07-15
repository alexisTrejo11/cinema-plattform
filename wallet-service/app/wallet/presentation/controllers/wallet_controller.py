from uuid import UUID
from fastapi import APIRouter, Depends, Query
from app.wallet.application.command.commands import PayWithWalletCommand, AddCreditCommand, CreateWalletCommand
from ..dtos.response import WalletResponse, WalletBuyResponse
from ..dtos.request import WalletOperationRequest
from ..dependencies import get_wallet_uc, WalletUseCases
from app.wallet.domain.value_objects import PaymentDetails, Money
from app.user.domain.value_objects import UserId
from app.shared.response import ApiResponse
router = APIRouter(prefix="/api/v2/wallets")

@router.get(
    "/{wallet_id}",
    response_model=ApiResponse[WalletResponse],
    summary="Get wallet by ID",
    description="Retrieves a wallet by its ID.",
    responses={
        200: {"description": "Wallet found"},
        404: {"description": "Wallet not found"},
    },
)
async def get_wallet(
    wallet_id: UUID,
    include_transactions: bool = Query(default=False),
    wallet_use_cases: WalletUseCases = Depends(get_wallet_uc),
):
    """
    Retrieves a wallet by its ID.
    - **wallet_id**: The ID of the wallet to retrieve.
    """
    wallet_response = await wallet_use_cases.get_wallet_by_id(wallet_id, include_transactions)
    return ApiResponse.success(wallet_response, "Wallet Succesfully Retrieved")


@router.get(
    "/user/{user_id}",
    response_model=ApiResponse[WalletResponse],
    summary="Get wallet by ID",
    description="Retrieves a wallet by its ID.",
    responses={
        200: {"description": "Wallet found"},
        404: {"description": "Wallet not found"},
    },
)
async def get_user_wallet(
    user_id: UUID,
    include_transactions: bool = Query(default=False),
    wallet_use_cases: WalletUseCases = Depends(get_wallet_uc),
):
    """
    Retrieves a wallet by its ID.
    - **wallet_id**: The ID of the wallet to retrieve.
    """
    wallet_response = await wallet_use_cases.get_wallets_by_user_id(user_id, include_transactions)
    return ApiResponse.success(wallet_response, "Wallet Succesfully Retrieved")


@router.post(
    "/{id}",
    response_model=ApiResponse[WalletResponse],
    status_code=201,
    summary="Create a new wallet",
    description="Creates a new wallet for a user.",
    responses={
        201: {"description": "Wallet created successfully"},
        400: {"description": "Invalid input"},
    },
)
async def create_wallet(
    id: UUID,
    wallet_use_cases: WalletUseCases = Depends(get_wallet_uc),
):
    """
    Creates a new wallet for a user.
    - **user_id**: The ID of the user to create the wallet for.
    """
    command = CreateWalletCommand(user_id=UserId(id))
    wallet_response = await wallet_use_cases.create_wallet(command)
    return ApiResponse.success(wallet_response, "Wallet Succesfully Inited")


@router.post(
    "/add-credit",
    response_model=ApiResponse[WalletBuyResponse],
    summary="Add credit to a wallet",
    description="Adds a specified amount of credit to a wallet.",
    responses={
        200: {"description": "Credit added successfully"},
        400: {"description": "Invalid input"},
        404: {"description": "Wallet not found"},
    },
)
async def recharge_credit(
    request_dto: WalletOperationRequest,
    wallet_use_cases: WalletUseCases = Depends(get_wallet_uc),
):
    """
    Adds credit to a wallet.
    - **wallet_id**: The ID of the wallet to add credit to.
    - **amount**: The amount of credit to add.
    """
    command = AddCreditCommand(
        wallet_id=request_dto.wallet_id,
        payment_details=PaymentDetails(request_dto.payment_method, request_dto.payment_id),
        amount=Money(request_dto.amount, request_dto.currency)
    )
    operation_response = await wallet_use_cases.add_credit(command)
    return ApiResponse.success(operation_response, "Credit Recharge Successfully proccesed in wallet")

@router.post(
    "/pay",
    response_model=ApiResponse[WalletBuyResponse],
    summary="Make a payment from a wallet",
    description="Makes a payment from a wallet.",
    responses={
        200: {"description": "Payment successful"},
        400: {"description": "Invalid input or insufficient funds"},
        404: {"description": "Wallet not found"},
    },
)
async def pay(
    request_dto: WalletOperationRequest,
    wallet_use_cases: WalletUseCases = Depends(get_wallet_uc),
):
    """
    Makes a payment from a wallet.
    - **wallet_id**: The ID of the wallet to pay from.
    - **amount**: The amount to pay.
    """
    command = PayWithWalletCommand(
        wallet_id=request_dto.wallet_id,
        payment_details=PaymentDetails(request_dto.payment_method, request_dto.payment_id),
        amount=Money(request_dto.amount, request_dto.currency)
    )
    pay_response = await wallet_use_cases.pay(command)
    return ApiResponse.success(data=pay_response, message="Pay Successfully proccesed in wallet")
