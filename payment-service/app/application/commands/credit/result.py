from typing import Optional
from pydantic import BaseModel
from uuid import UUID

class AddCreditResult(BaseModel):
    """Result of adding credit to wallet."""
    wallet_id: UUID
    transaction_id: UUID
    user_id: UUID
    amount: float
    currency: str
    new_balance: float
    status: str
    message: str

    @staticmethod
    def invalid_credit_result(wallet_id: Optional[UUID], user_id: UUID, amount: float, 
                            currency: str, message: str):
        return AddCreditResult(
            wallet_id=wallet_id or UUID(int=0),
            transaction_id=UUID(int=0),
            user_id=user_id,
            amount=amount,
            currency=currency,
            new_balance=0.0,
            status="failed",
            message=f"Credit addition failed: {message}"
        )


class AddCreditResultBuilder:
    def __init__(self):
        self._wallet_id = UUID(int=0)
        self._transaction_id = UUID(int=0)
        self._user_id = UUID(int=0)
        self._amount = 0.0
        self._currency = "USD"
        self._new_balance = 0.0
        self._status = "pending"
        self._message = ""

    def set_wallet_id(self, wallet_id: UUID) -> 'AddCreditResultBuilder':
        self._wallet_id = wallet_id
        return self

    def set_transaction_id(self, transaction_id: UUID) -> 'AddCreditResultBuilder':
        self._transaction_id = transaction_id
        return self

    def set_user_id(self, user_id: UUID) -> 'AddCreditResultBuilder':
        self._user_id = user_id
        return self

    def set_amount(self, amount: float) -> 'AddCreditResultBuilder':
        self._amount = amount
        return self

    def set_currency(self, currency: str) -> 'AddCreditResultBuilder':
        self._currency = currency
        return self

    def set_new_balance(self, new_balance: float) -> 'AddCreditResultBuilder':
        self._new_balance = new_balance
        return self

    def set_status(self, status: str) -> 'AddCreditResultBuilder':
        self._status = status
        return self

    def set_message(self, message: str) -> 'AddCreditResultBuilder':
        self._message = message
        return self

    def build(self) -> AddCreditResult:
        return AddCreditResult(
            wallet_id=self._wallet_id,
            transaction_id=self._transaction_id,
            user_id=self._user_id,
            amount=self._amount,
            currency=self._currency,
            new_balance=self._new_balance,
            status=self._status,
            message=self._message
        )

    @classmethod
    def success_builder(cls, wallet_id: UUID, transaction_id: UUID, user_id: UUID,
                       amount: float, currency: str, new_balance: float) -> 'AddCreditResultBuilder':
        return cls() \
            .set_wallet_id(wallet_id) \
            .set_transaction_id(transaction_id) \
            .set_user_id(user_id) \
            .set_amount(amount) \
            .set_currency(currency) \
            .set_new_balance(new_balance) \
            .set_status("success") \
            .set_message("Credit added successfully")

    @classmethod
    def from_invalid_result(cls, invalid_result: AddCreditResult) -> 'AddCreditResultBuilder':
        return cls() \
            .set_wallet_id(invalid_result.wallet_id) \
            .set_transaction_id(invalid_result.transaction_id) \
            .set_user_id(invalid_result.user_id) \
            .set_amount(invalid_result.amount) \
            .set_currency(invalid_result.currency) \
            .set_new_balance(invalid_result.new_balance) \
            .set_status(invalid_result.status) \
            .set_message(invalid_result.message)