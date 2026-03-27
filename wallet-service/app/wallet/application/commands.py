from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.wallet.domain.value_objects import Charge, Money, PaymentDetails, UserId, WalletId


class CreateWalletCommand(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    user_id: UserId

    @classmethod
    def from_uuid(cls, user_id: UUID) -> CreateWalletCommand:
        return cls(user_id=UserId(user_id))


class AddCreditCommand(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    wallet_id: WalletId
    amount: Money
    payment_details: PaymentDetails


class PayWithWalletCommand(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    wallet_id: WalletId
    charge: Charge
    payment_details: PaymentDetails
