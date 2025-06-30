from app.utils.exceptions import DomainException
from decimal import Decimal
from abc import ABC
from typing import Any, Optional, Dict

class PriceRangeException(DomainException):
    """Exception for invalid price ranges."""
    def __init__(self, min_price: Decimal, max_price: Decimal):
        message = f"Price must be between {min_price} and {max_price}"
        super().__init__(message)

class ItemRangeException(DomainException):
    """Exception for invalid item ranges."""
    def __init__(self, min_items: int, max_items: int):
        message = f"Number of items must be between {min_items} and {max_items}"
        super().__init__(message)

class PriceSumException(DomainException):
    """Exception when combo price exceeds sum of product prices."""
    def __init__(self, product_total_price: Decimal):
        message = f"The price can't be higher than the product price sum = {product_total_price}"
        super().__init__(message)

class DiscountPercentageException(DomainException):
    """Exception for invalid discount percentages."""
    def __init__(self, expected_percentage: Decimal, details: Optional[Dict[str, Any]] = {}):
        message = f"Invalid Percentage Provided for that request of products must be {expected_percentage}"
    
        super().__init__(message= message, details= details)

class QuantityRangeException(DomainException):
    """Exception for invalid quantity ranges."""
    def __init__(self, product_id: int, min_quantity: int, max_quantity: int):
        message = f"Item for product {product_id} exceeds the allowed range for quantity that must be between {min_quantity} and {max_quantity}"
        super().__init__(message)