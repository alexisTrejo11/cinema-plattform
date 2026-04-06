"""Map presentation request DTOs to application commands."""

from app.wallet.application.commands import AddCreditCommand, PayWithWalletCommand
from app.wallet.domain.value_objects import Charge, Money, PaymentDetails, WalletId
from app.wallet.presentation.dtos.request import UserWalletOperationRequest, WalletOperationRequest


def map_wallet_operation_to_add_credit_command(
    req: WalletOperationRequest,
) -> AddCreditCommand:
    return AddCreditCommand(
        wallet_id=WalletId(value=req.wallet_id),
        amount=Money(amount=req.amount, currency=req.currency),
        payment_details=PaymentDetails(
            payment_method=req.payment_method,
            payment_id=req.payment_id,
        ),
    )


def map_user_wallet_operation_to_add_credit_command(
    req: UserWalletOperationRequest,
    wallet_id: WalletId,
) -> AddCreditCommand:
    return AddCreditCommand(
        wallet_id=wallet_id,
        amount=Money(amount=req.amount, currency=req.currency),
        payment_details=PaymentDetails(
            payment_method=req.payment_method,
            payment_id=req.payment_id,
        ),
    )


def map_wallet_operation_to_pay_command(
    req: WalletOperationRequest,
) -> PayWithWalletCommand:
    return PayWithWalletCommand(
        wallet_id=WalletId(value=req.wallet_id),
        charge=Charge(amount=req.amount, currency=req.currency),
        payment_details=PaymentDetails(
            payment_method=req.payment_method,
            payment_id=req.payment_id,
        ),
    )


def map_user_wallet_operation_to_pay_command(
    req: UserWalletOperationRequest,
    wallet_id: WalletId,
) -> PayWithWalletCommand:
    return PayWithWalletCommand(
        wallet_id=wallet_id,
        charge=Charge(amount=req.amount, currency=req.currency),
        payment_details=PaymentDetails(
            payment_method=req.payment_method,
            payment_id=req.payment_id,
        ),
    )
