"""Test doubles for integration tests."""

from __future__ import annotations

from datetime import date, datetime

from app.wallet.domain.entities.wallet import Wallet
from app.wallet.domain.value_objects import WalletId, Money, Currency, UserId
from app.wallet.domain.enums import Currency, TransactionType, WalletStatus


def make_domain_wallet(
    *,
    wallet_id: WalletId = WalletId(0),
    user_id: UserId = UserId(0),
    balance: Money = Money(0),
    currency: Currency = Currency.USD,
    status: WalletStatus = WalletStatus.ACTIVE,
    created_at: datetime = datetime.now(),
    updated_at: datetime = datetime.now(),
) -> Wallet:
    return Wallet(
        id=wallet_id,
        user_id=user_id,
        balance=balance,
        currency=currency,
        status=status,
        created_at=created_at,
        updated_at=updated_at,
    )
