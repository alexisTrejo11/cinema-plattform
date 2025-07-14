from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from app.wallet.application.dtos.wallet_dtos import (
    CreateWalletCommand,
    AddCreditCommand,
    PayWithWalletCommand,
    WalletResponse,
)
from ..dependencies import get_wallet_uc, WalletUseCases

router = APIRouter(prefix="/api/v2/wallets")


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
async def get_wallet(
    wallet_id: UUID,
    include_transactions: bool = Query(default=False),
    wallet_use_cases: WalletUseCases = Depends(get_wallet_uc),
):
    """
    Retrieves a wallet by its ID.
    - **wallet_id**: The ID of the wallet to retrieve.
    """
    wallet = await wallet_use_cases.get_wallet_by_id(wallet_id, include_transactions)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet


@router.get(
    "/user/{user_id}",
    response_model=WalletResponse,
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
    wallet = await wallet_use_cases.get_wallets_by_user_id(
        user_id, include_transactions
    )
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet


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
    user_id: UUID,
    wallet_use_cases: WalletUseCases = Depends(get_wallet_uc),
):
    """
    Creates a new wallet for a user.
    - **user_id**: The ID of the user to create the wallet for.
    """
    command = CreateWalletCommand(user_id=user_id)
    return await wallet_use_cases.create_wallet(command)


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
async def add_credit(
    add_credit_dto: AddCreditCommand,
    wallet_use_cases: WalletUseCases = Depends(get_wallet_uc),
):
    """
    Adds credit to a wallet.
    - **wallet_id**: The ID of the wallet to add credit to.
    - **amount**: The amount of credit to add.
    """
    try:
        return await wallet_use_cases.add_credit(add_credit_dto)
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
async def pay(
    pay_dto: PayWithWalletCommand,
    wallet_use_cases: WalletUseCases = Depends(get_wallet_uc),
):
    """
    Makes a payment from a wallet.
    - **wallet_id**: The ID of the wallet to pay from.
    - **amount**: The amount to pay.
    """
    try:
        return await wallet_use_cases.pay(pay_dto)
    except ValueError as e:
        if "not found" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        else:
            raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
