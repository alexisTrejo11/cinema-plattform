from typing import Optional
import logging
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status

from app.shared.response import ApiResponse
from app.user.auth.auth_dependencies import get_staff_user, User
from ..docs.walley_docs import *
from app.wallet.application.command.commands import (
    PayWithWalletCommand,
    AddCreditCommand,
    CreateWalletCommand,
)
from app.wallet.application.query.queries import (
    GetWalletByIdQuery,
    GetWalletByUserIdQuery,
)

from ..dtos.response import WalletResponse, WalletBuyResponse
from ..dtos.request import WalletOperationRequest
from ..dependencies import get_wallet_uc, WalletUseCases
from app.shared.documentation import (
    common_wallet_error_responses as common_error_responses,
)

logger = logging.getLogger("app")
router = APIRouter(prefix="/api/v2/wallets", tags=["Wallets"])


@router.get(
    "/{wallet_id}",
    response_model=ApiResponse[WalletResponse],
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
    user: User = Depends(get_staff_user),
    wallet_use_cases: WalletUseCases = Depends(get_wallet_uc),
):
    """
    Retrieves a wallet by its ID.
    """
    try:
        logger.info(
            f"GET get wallet request | Wallet ID:{wallet_id} | Client:{user.get_id().value if user else None}"
        )
        query = GetWalletByIdQuery.from_request(
            wallet_id, include_transactions, limit, offset
        )

        wallet_response = await wallet_use_cases.get_wallet_by_id(query)
        logger.info(
            f"GET get wallet success | Wallet ID:{wallet_id} | User ID:{user.get_id().value}"
        )

        return ApiResponse.success(wallet_response, "Wallet Successfully Retrieved")
    except Exception as e:
        logger.error(f"GET get wallet failed | Wallet ID:{wallet_id} | Error: {str(e)}")
        raise


@router.get(
    "/user/{user_id}",
    response_model=ApiResponse[WalletResponse],
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
    user: User = Depends(get_staff_user),
    wallet_use_cases: WalletUseCases = Depends(get_wallet_uc),
):
    """
    Retrieves a wallet by its associated user ID.
    """
    try:
        logger.info(
            f"GET get user wallet request | User ID:{user_id} | Client:{user.get_id().value if user else None}"
        )

        query = GetWalletByUserIdQuery.from_request(
            user_id, include_transactions, limit, offset
        )
        wallet_response = await wallet_use_cases.get_wallets_by_user_id(query)

        logger.info(
            f"GET get user wallet success | User ID:{user_id} | Wallet ID:{str(wallet_response.id)}"
        )
        return ApiResponse.success(wallet_response, "Wallet Successfully Retrieved")
    except Exception as e:
        logger.error(
            f"GET get user wallet failed | User ID:{user_id} | Error: {str(e)}"
        )
        raise


@router.post(
    "/user/{user_id}",
    response_model=ApiResponse[WalletResponse],
    summary="Create a New Wallet for a User",
    description="""
    Creates a new wallet for a specified user ID.

    This endpoint requires authentication as an employee.
    A user can typically only have one wallet. If a wallet already exists for the user,
    a 400 Bad Request error will be returned.
    """,
    status_code=status.HTTP_201_CREATED,
    responses={
        **common_error_responses,
        status.HTTP_201_CREATED: {
            "description": "Wallet created successfully.",
            "content": {
                "application/json": {
                    "examples": {
                        "success": {
                            "summary": "Successful Wallet Creation",
                            "value": {
                                "message": "Wallet Successfully Inited",
                                "data": {
                                    "id": "c1d2e3f4-a5b6-7890-1234-567890abcdef",
                                    "user_id": "2a3b4c5d-6e7f-8901-2345-67890abcdef1",
                                    "balance": {
                                        "amount": 0.00,
                                        "currency": "USD",
                                    },  # Assuming initial balance is 0
                                    "transactions": [],
                                },
                                "error": None,
                            },
                        }
                    }
                }
            },
        },
    },
)
async def create_wallet(
    user_id: UUID,
    wallet_use_cases: WalletUseCases = Depends(get_wallet_uc),
    user: User = Depends(get_staff_user),
):
    """
    Creates a new wallet for a user.
    """
    command = CreateWalletCommand.from_uuid(user_id)
    wallet_response = await wallet_use_cases.create_wallet(command)

    return ApiResponse.success(wallet_response, "Wallet Successfully Inited")


@router.post(
    "/add-credit",
    response_model=ApiResponse[WalletBuyResponse],
    status_code=status.HTTP_200_OK,
    summary=addCreditDoc["summary"],
    description=addCreditDoc["description"],
    responses=addCreditDoc["responses"],
)
async def recharge_credit(
    request_dto: WalletOperationRequest,
    wallet_use_cases: WalletUseCases = Depends(get_wallet_uc),
    user: User = Depends(get_staff_user),
):
    """
    Adds credit to a wallet based on the provided operation details.
    """
    try:
        logger.info(
            f"POST add credit to wallet request | Wallet ID:{request_dto.wallet_id} |Client:{user.get_id().value if user else None}"
        )
        command = AddCreditCommand.from_request(request_dto)

        operation_response = await wallet_use_cases.add_credit(command)

        logger.info(
            f"POST add credit to wallet success | Wallet ID:{request_dto.wallet_id} | New Balance: {operation_response.balance} | Transaction ID: {operation_response.transaction.transaction_id}"
        )

        return ApiResponse.success(
            operation_response, "Credit Recharge Successfully processed in wallet"
        )
    except Exception as e:
        logger.error(
            f"POST add credit to wallet failed | Wallet ID:{request_dto.wallet_id} | Error: {str(e)}"
        )
        raise


@router.post(
    "/pay",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[WalletBuyResponse],
    summary=payCartDoc["summary"],
    description=payCartDoc["description"],
    responses=payCartDoc["responses"],
)
async def pay(
    request_dto: WalletOperationRequest,
    wallet_use_cases: WalletUseCases = Depends(get_wallet_uc),
    user: User = Depends(get_staff_user),
):
    """
    Makes a payment from a wallet.
    """
    try:
        logger.info(
            f"POST pay from wallet request | Wallet ID:{request_dto.wallet_id} | Client:{user.get_id().value if user else None}"
        )
        command = PayWithWalletCommand.from_request(request_dto)

        pay_response = await wallet_use_cases.pay(command)

        logger.info(
            f"POST pay from wallet success | Wallet ID:{request_dto.wallet_id} | New Balance: {pay_response.balance} | Transaction ID: {pay_response.transaction.transaction_id}"
        )
        return ApiResponse.success(pay_response, "Pay Successfully processed in wallet")
    except Exception as e:
        logger.error(
            f"POST pay from wallet failed | Wallet ID:{request_dto.wallet_id} | Error: {str(e)}"
        )
        raise
