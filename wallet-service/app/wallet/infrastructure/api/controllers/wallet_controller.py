from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from app.wallet.application.use_cases.wallet_use_cases import WalletUseCases
from app.wallet.application.dtos.wallet_dtos import (
    CreateWalletCommand,
    AddCreditResponse,
    PayResponse,
    PydanticUserId,
    WalletResponse,
)
from ..dependencies import get_wallet_uc

router = APIRouter(prefix="/v2/api/wallets")


@router.post(
    "/{user_id}",
    response_model=WalletResponse,
    status_code=201,
    summary="Create a new wallet",
    description="Creates a new wallet for a user.",
    responses={
        201: {"description": "Wallet created successfully"},
        400: {"description": "Invalid input"},
    },
)
async def create_wallet(
    user_id: PydanticUserId,
    wallet_use_cases: WalletUseCases = Depends(get_wallet_uc),
):
    """
    Creates a new wallet for a user.
    - **user_id**: The ID of the user to create the wallet for.
    """
    command = CreateWalletCommand(user_id=user_id)
    return await wallet_use_cases.create_wallet(command)


@router.get(
    "/{wallet_id}",
    response_model=WalletResponse,
    summary="Get wallet by ID",
    description="Retrieves a wallet by its ID.",
    responses={
        200: {"description": "Wallet found"},
        404: {"description": "Wallet not found"},
    },
)
def get_wallet(
    wallet_id: UUID, wallet_use_cases: WalletUseCases = Depends(get_wallet_uc)
):
    """
    Retrieves a wallet by its ID.
    - **wallet_id**: The ID of the wallet to retrieve.
    """
    wallet = wallet_use_cases.get_wallet_by_id(wallet_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet


@router.post(
    "/add-credit",
    response_model=WalletResponse,
    summary="Add credit to a wallet",
    description="Adds a specified amount of credit to a wallet.",
    responses={
        200: {"description": "Credit added successfully"},
        400: {"description": "Invalid input"},
        404: {"description": "Wallet not found"},
    },
)
def add_credit(
    add_credit_dto: AddCreditResponse,
    wallet_use_cases: WalletUseCases = Depends(get_wallet_uc),
):
    """
    Adds credit to a wallet.
    - **wallet_id**: The ID of the wallet to add credit to.
    - **amount**: The amount of credit to add.
    """
    try:
        return wallet_use_cases.add_credit(add_credit_dto)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/pay",
    response_model=WalletResponse,
    summary="Make a payment from a wallet",
    description="Makes a payment from a wallet.",
    responses={
        200: {"description": "Payment successful"},
        400: {"description": "Invalid input or insufficient funds"},
        404: {"description": "Wallet not found"},
    },
)
def pay(
    pay_dto: PayResponse, wallet_use_cases: WalletUseCases = Depends(get_wallet_uc)
):
    """
    Makes a payment from a wallet.
    - **wallet_id**: The ID of the wallet to pay from.
    - **amount**: The amount to pay.
    """
    try:
        return wallet_use_cases.pay(pay_dto)
    except ValueError as e:
        if "not found" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        else:
            raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
