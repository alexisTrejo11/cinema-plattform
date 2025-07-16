from typing import Optional
import logging
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status


from app.shared.response import ApiResponse
from app.user.domain.value_objects import UserId
from app.auth.auth_dependencies import get_staff_user, User

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

router = APIRouter(prefix="/api/v2/wallets", tags=["Wallets"])

logger = logging.getLogger("app")


@router.get(
    "/{wallet_id}",
    response_model=ApiResponse[WalletResponse],
    summary="Retrieve Wallet by ID",
    description="""
    Retrieves detailed information for a specific wallet using its unique identifier.

    This endpoint requires authentication as an employee.
    It can optionally include a list of recent transactions associated with the wallet.
    """,
    status_code=status.HTTP_200_OK,
    responses={
        **common_error_responses,
        status.HTTP_200_OK: {
            "description": "Wallet successfully retrieved.",
            "content": {
                "application/json": {
                    "examples": {
                        "success": {
                            "summary": "Successful Wallet Retrieval",
                            "value": {
                                "message": "Wallet Successfully Retrieved",
                                "data": {
                                    "id": "b1c2d3e4-f5a6-7890-1234-567890abcdef",
                                    "user_id": "1a2b3c4d-5e6f-7890-1234-567890abcdef",
                                    "balance": {"amount": 1250.75, "currency": "USD"},
                                    "transactions": [
                                        {
                                            "transaction_id": "a0b1c2d3-e4f5-6789-0123-456789abcdef",
                                            "wallet_id": "b1c2d3e4-f5a6-7890-1234-567890abcdef",
                                            "amount": {
                                                "amount": 50.00,
                                                "currency": "USD",
                                            },
                                            "transaction_type": "CREDIT",
                                            "payment_details": {
                                                "payment_method": "card",
                                                "payment_id": "d1e2f3a4-b5c6-7890-1234-567890abcdef",
                                            },
                                            "timestamp": "2024-07-15T19:00:00.123456Z",
                                        }
                                    ],
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
    summary="Retrieve Wallet by User ID",
    description="""
    Retrieves detailed information for a specific wallet associated with a user ID.

    This endpoint requires authentication as an employee.
    It can optionally include a list of recent transactions for the wallet.
    """,
    status_code=status.HTTP_200_OK,
    responses={
        **common_error_responses,
        status.HTTP_200_OK: {
            "description": "Wallet successfully retrieved.",
            "content": {
                "application/json": {
                    "examples": {
                        "success": {
                            "summary": "Successful Wallet Retrieval by User ID",
                            "value": {
                                "message": "Wallet Successfully Retrieved",
                                "data": {
                                    "id": "b1c2d3e4-f5a6-7890-1234-567890abcdef",
                                    "user_id": "1a2b3c4d-5e6f-7890-1234-567890abcdef",
                                    "balance": {"amount": 1250.75, "currency": "USD"},
                                    "transactions": [],  # Example with no transactions
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
    summary="Add Credit to a Wallet",
    description="""
    Adds a specified amount of credit to a wallet. This operation typically represents
    a top-up or a deposit into the user's wallet.

    This endpoint requires authentication as an employee.
    The `WalletOperationRequest` includes the target wallet ID, amount, currency,
    and details of the payment used for the credit addition.
    """,
    status_code=status.HTTP_200_OK,
    responses={
        **common_error_responses,
        status.HTTP_200_OK: {
            "description": "Credit successfully added to the wallet.",
            "content": {
                "application/json": {
                    "examples": {
                        "success": {
                            "summary": "Successful Credit Addition",
                            "value": {
                                "message": "Credit Recharge Successfully processed in wallet",
                                "data": {
                                    "id": "b1c2d3e4-f5a6-7890-1234-567890abcdef",
                                    "user_id": "1a2b3c4d-5e6f-7890-1234-567890abcdef",
                                    "balance": 1300.75,  # Example new balance
                                    "transaction": {
                                        "transaction_id": "g1h2i3j4-k5l6-7890-1234-567890abcdef",
                                        "wallet_id": "b1c2d3e4-f5a6-7890-1234-567890abcdef",
                                        "amount": {"amount": 50.00, "currency": "USD"},
                                        "transaction_type": "CREDIT",
                                        "payment_details": {
                                            "payment_method": "card",
                                            "payment_id": "x1y2z3a4-b5c6-7890-1234-567890abcdef",
                                        },
                                        "timestamp": "2024-07-15T19:30:00.123456Z",
                                    },
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
    response_model=ApiResponse[
        WalletBuyResponse
    ],  # Assuming WalletBuyResponse is suitable for payment output
    summary="Make a Payment from a Wallet",
    description="""
    Initiates a payment from a specified wallet, debiting the given amount.

    This endpoint requires authentication as an employee.
    The `WalletOperationRequest` includes the wallet ID, amount, currency,
    and details of the payment being made.
    """,
    status_code=status.HTTP_200_OK,
    responses={
        **common_error_responses,
        status.HTTP_200_OK: {
            "description": "Payment successfully processed from the wallet.",
            "content": {
                "application/json": {
                    "examples": {
                        "success": {
                            "summary": "Successful Payment",
                            "value": {
                                "message": "Pay Successfully processed in wallet",
                                "data": {
                                    "id": "b1c2d3e4-f5a6-7890-1234-567890abcdef",
                                    "user_id": "1a2b3c4d-5e6f-7890-1234-567890abcdef",
                                    "balance": 1200.00,  # Example new balance after payment
                                    "transaction": {
                                        "transaction_id": "h1i2j3k4-l5m6-7890-0123-456789abcdef",
                                        "wallet_id": "b1c2d3e4-f5a6-7890-1234-567890abcdef",
                                        "amount": {"amount": 100.75, "currency": "USD"},
                                        "transaction_type": "DEBIT",
                                        "payment_details": {
                                            "payment_method": "merchant_purchase",
                                            "payment_id": "y1z2a3b4-c5d6-7890-1234-567890abcdef",
                                        },
                                        "timestamp": "2024-07-15T19:45:00.123456Z",
                                    },
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
