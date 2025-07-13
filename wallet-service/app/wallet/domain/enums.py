from enum import Enum


class Currency(Enum):
    MXN = "MXN"
    USD = "USD"
    EUR = "EUR"


class TransactionType(Enum):
    ADD_CREDIT = "add_credit"
    BUY_PRODUCT = "buy_product"
    REFUND = "refund"
    TRANSFER_IN = "transfer_in"
    TRANSFER_OUT = "transfer_out"
