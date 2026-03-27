"""Backward-compatible re-exports (prefer `wallet_command_use_cases` / `wallet_query_use_cases`)."""

from app.wallet.application.use_cases.wallet_command_use_cases import (
    AddCreditUseCase,
    InitWalletForUserUseCase,
    PayWithWalletUseCase,
)
from app.wallet.application.use_cases.wallet_query_use_cases import (
    GetWalletByIdUseCase,
    GetWalletsByUserIdUseCase,
)

__all__ = [
    "InitWalletForUserUseCase",
    "AddCreditUseCase",
    "PayWithWalletUseCase",
    "GetWalletByIdUseCase",
    "GetWalletsByUserIdUseCase",
]
