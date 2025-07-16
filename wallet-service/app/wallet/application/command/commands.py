from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.wallet.domain.value_objects import Money, PaymentDetails, Charge, WalletId
from app.user.domain.value_objects import UserId
from app.wallet.presentation.dtos.request import WalletOperationRequest


class PayWithWalletCommand(BaseModel):
    """DTO for making a payment from a wallet."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    wallet_id: WalletId
    payment_details: PaymentDetails
    charge: Charge

    @staticmethod
    def from_request(request: WalletOperationRequest):
        return PayWithWalletCommand(
            wallet_id=WalletId(request.wallet_id),
            payment_details=PaymentDetails(request.payment_method, request.payment_id),
            charge=Charge(request.amount, request.currency),
        )


class AddCreditCommand(BaseModel):
    """DTO for adding credit to a wallet."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    wallet_id: WalletId
    payment_details: PaymentDetails
    amount: Money

    @staticmethod
    def from_request(request: WalletOperationRequest):
        return AddCreditCommand(
            wallet_id=WalletId(request.wallet_id),
            payment_details=PaymentDetails(request.payment_method, request.payment_id),
            amount=Money(request.amount, request.currency),
        )


class CreateWalletCommand(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    user_id: UserId

    @staticmethod
    def from_uuid(uuid: UUID):
        return CreateWalletCommand(
            user_id=UserId(uuid),
        )
