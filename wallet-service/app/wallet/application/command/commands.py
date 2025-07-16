from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.wallet.domain.value_objects import Money, PaymentDetails, Charge
from app.user.domain.value_objects import UserId

class PayWithWalletCommand(BaseModel):
    """DTO for making a payment from a wallet."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    wallet_id: UUID
    payment_details: PaymentDetails
    charge: Charge


class AddCreditCommand(BaseModel):
    """DTO for adding credit to a wallet."""
    model_config = ConfigDict(arbitrary_types_allowed=True)

    wallet_id: UUID
    payment_details: PaymentDetails
    amount: Money


class CreateWalletCommand(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    user_id: UserId