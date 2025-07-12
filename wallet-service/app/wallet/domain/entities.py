import uuid
from decimal import Decimal
from .value_objects import Money, CustomerId
from .exceptions import InsufficientFundsError, InvalidTransactionAmountError

class Wallet:
    def __init__(self, id: uuid.UUID, customer_id: CustomerId, balance: Money):
        self.id = id
        self.customer_id = customer_id
        self.balance = balance

    def credit(self, amount: Money):
        if amount.amount <= 0:
            raise InvalidTransactionAmountError("Credit amount must be positive")
        self.balance += amount

    def debit(self, amount: Money):
        if amount.amount <= 0:
            raise InvalidTransactionAmountError("Debit amount must be positive")
        if self.balance.amount < amount.amount:
            raise InsufficientFundsError("Insufficient funds for this transaction")
        self.balance -= amount

    @staticmethod
    def create(customer_id: CustomerId) -> "Wallet":
        return Wallet(uuid.uuid4(), customer_id, Money(Decimal("0.00"), "USD"))

