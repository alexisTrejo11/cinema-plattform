import uuid
from decimal import Decimal
from typing import List, Optional
from app.user.domain.value_objects import UserId
from app.wallet.domain.value_objects import Money, WalletId
from app.wallet.domain.enums import Currency, TransactionType
from .wallet_transaction import PaymentDetails, WalletTransaction
from ..validators import WalletDomainValidator as WalletValidator

class Wallet:
    def __init__(self, id: WalletId, user_id: UserId, balance: Money):
        self.id = id
        self.user_id = user_id
        self.balance = balance
        self.transactions: List[WalletTransaction] = []
        self.validator = WalletValidator(self)

    @staticmethod
    def create(user_id: UserId, initial_currency: Currency = Currency.USD) -> "Wallet":
        initial_balance = Money(Decimal("0.00"), initial_currency)
        return Wallet(WalletId(uuid.uuid4()), user_id, initial_balance)

    def buy_product(self, payment_details: PaymentDetails, amount: Money):
        self.validator.validate_credit_decrease(amount)
        self.remove_credit(amount)
        return self.create_transaction(amount, TransactionType.ADD_CREDIT, payment_details)

    def buy_credit(self, payment_details: PaymentDetails, amount: Money):
        self.add_credit(amount)
        return self.create_transaction(amount, TransactionType.BUY_PRODUCT, payment_details)

    def add_credit(self, amount: Money) -> None:
        self.validator.validate_credit_increase(amount)
        self.balance = self.balance + amount

    def remove_credit(self, amount: Money) -> None:
        self.validator.validate_credit_decrease(amount)
        self.balance = self.balance - amount

    def add_transaction(self, transaction: WalletTransaction) -> WalletTransaction:
        self.transactions.append(transaction)
        return transaction

    def create_transaction(
        self, 
        amount: Money, 
        transaction_type: TransactionType, 
        payment_details: PaymentDetails
    ) -> WalletTransaction:
        new_transaction = WalletTransaction.create(self.id, amount, transaction_type, payment_details)
        self.add_transaction(new_transaction)
        return new_transaction


