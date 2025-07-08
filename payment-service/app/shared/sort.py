from enum import Enum

class PaymentSortBy(str, Enum):
    """Payment history sorting options."""
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    AMOUNT = "amount"
    STATUS = "status"


class SortOrder(str, Enum):
    """Sort order options."""
    ASC = "asc"
    DESC = "desc"