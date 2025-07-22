from decimal import Decimal
from typing import Any, Dict
from app.shared.base_exceptions import (
    NotFoundException,
    ApplicationException,
    ValidationException,
)


def ComboNotFoundError(combo_id: str) -> NotFoundException:
    return NotFoundException("Combo", combo_id)


def ComboItemValidationError(reason: str) -> ValidationException:
    return ValidationException("combo item", reason)


def ProductValidationError() -> ValidationException:
    return ValidationException("product", "invalid product provided")


def ComboValidationError(reason: str) -> ValidationException:
    return ValidationException("combo", reason)


def PriceRangeException(min: Decimal, max: Decimal) -> ValidationException:
    return ValidationException("price range", f"invalid price range: {min} - {max}")


def ItemRangeException(min: int, max: int) -> ValidationException:
    return ValidationException("item range", f"invalid item range: {min} - {max}")


def PriceSumException(product_total_price: Decimal) -> ValidationException:
    return ValidationException(
        "price sum",
        f"combo price exceeds sum of product prices: {product_total_price}",
    )


def DiscountPercentageException(
    discount: Decimal, details: Dict[str, Any]
) -> ValidationException:

    return ValidationException(
        "discount percentage",
        f"discount {discount} does not match price ratio",
        details=details,
    )


def QuantityRangeException(product_id: str, min: int, max: int) -> ValidationException:
    return ValidationException(
        "quantity range",
        f"invalid quantity for product {product_id}: {min} - {max}",
    )
