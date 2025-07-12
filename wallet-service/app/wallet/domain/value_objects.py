import uuid
from decimal import Decimal

class Money:
    def __init__(self, amount: Decimal, currency: str):
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        if not currency or len(currency) != 3:
            raise ValueError("Invalid currency")
        self.amount = amount
        self.currency = currency

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Cannot add money with different currencies")
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Cannot subtract money with different currencies")
        if self.amount < other.amount:
            raise ValueError("Resulting amount cannot be negative")
        return Money(self.amount - other.amount, self.currency)

class CustomerId:
    def __init__(self, value: uuid.UUID):
        self.value = value

