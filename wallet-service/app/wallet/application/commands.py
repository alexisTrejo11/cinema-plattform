from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.wallet.domain.enums import Currency
from app.wallet.domain.value_objects import Charge, Money, PaymentDetails, UserId, WalletId
from app.wallet.presentation.dtos.request import WalletOperationRequest


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

    @classmethod
    def from_request(cls, req: WalletOperationRequest) -> AddCreditCommand:
        return cls(
            wallet_id=WalletId(value=req.wallet_id),
            amount=Money(amount=req.amount, currency=req.currency),
            payment_details=PaymentDetails(
                payment_method=req.payment_method,
                payment_id=req.payment_id,
            ),
        )


class PayWithWalletCommand(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    wallet_id: WalletId
    charge: Charge
    payment_details: PaymentDetails

    @classmethod
    def from_request(cls, req: WalletOperationRequest) -> PayWithWalletCommand:
        return cls(
            wallet_id=WalletId(value=req.wallet_id),
            charge=Charge(amount=req.amount, currency=req.currency),
            payment_details=PaymentDetails(
                payment_method=req.payment_method,
                payment_id=req.payment_id,
            ),
        )
