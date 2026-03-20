from app.shared.base_exceptions import DomainException
from datetime import datetime
from typing import Optional


class PromotionError(DomainException):
    """Base exception for all Promotion-related errors."""

    pass


class InvalidPromotionDataError(PromotionError):
    """Raised when promotion data is invalid during creation or update."""

    def __init__(
        self,
        message="Invalid promotion data.",
        field_name: Optional[str] = None,
        **kwargs
    ):
        super().__init__(message, **kwargs)
        if field_name:
            self.details["field_name"] = field_name


class PromotionAlreadyActiveError(PromotionError):
    """Raised when attempting to activate an already active promotion."""

    def __init__(
        self,
        message="The promotion is already active.",
        promotion_id: Optional[str] = None,
        **kwargs
    ):
        super().__init__(message, **kwargs)
        if promotion_id:
            self.details["promotion_id"] = promotion_id


class PromotionAlreadyInactiveError(PromotionError):
    """Raised when attempting to deactivate an already inactive promotion."""

    def __init__(
        self,
        message="The promotion is already inactive.",
        promotion_id: Optional[str] = None,
        **kwargs
    ):
        super().__init__(message, **kwargs)
        if promotion_id:
            self.details["promotion_id"] = promotion_id


class PromotionExpiredError(PromotionError):
    """Raised when attempting to apply or modify an expired promotion."""

    def __init__(
        self,
        message="The promotion has expired.",
        promotion_id: Optional[str] = None,
        end_date: Optional[datetime] = None,
        **kwargs
    ):
        super().__init__(message, **kwargs)
        if promotion_id:
            self.details["promotion_id"] = promotion_id
        if end_date:
            self.details["end_date"] = end_date.isoformat()


class PromotionNotApplicableError(PromotionError):
    """Raised when a promotion is not applicable to a given product or context."""

    def __init__(
        self,
        message="The promotion is not applicable.",
        promotion_id: Optional[str] = None,
        product_id: Optional[str] = None,
        category_id: Optional[int] = None,
        **kwargs
    ):
        super().__init__(message, **kwargs)
        if promotion_id:
            self.details["promotion_id"] = promotion_id
        if product_id:
            self.details["product_id"] = product_id
        if category_id:
            self.details["category_id"] = category_id


class PromotionMaxUsesExceededError(PromotionError):
    """Raised when the maximum number of uses for a promotion has been exceeded."""

    def __init__(
        self,
        message="Maximum uses for the promotion exceeded.",
        promotion_id: Optional[str] = None,
        max_uses: Optional[int] = None,
        current_uses: Optional[int] = None,
        **kwargs
    ):
        super().__init__(message, **kwargs)
        if promotion_id:
            self.details["promotion_id"] = promotion_id
        if max_uses is not None:
            self.details["max_uses"] = max_uses
        if current_uses is not None:
            self.details["current_uses"] = current_uses


class PromotionProductAlreadyIncludedError(PromotionError):
    """Raised when attempting to add a product that's already in the promotion's applicable products list."""

    def __init__(
        self,
        message="Product is already included in the promotion.",
        promotion_id: Optional[str] = None,
        product_id: Optional[str] = None,
        **kwargs
    ):
        super().__init__(message, **kwargs)
        if promotion_id:
            self.details["promotion_id"] = promotion_id
        if product_id:
            self.details["product_id"] = product_id


class PromotionCategoryAlreadyIncludedError(PromotionError):
    """Raised when attempting to add a category that's already in the promotion's applicable categories list."""

    def __init__(
        self,
        message="Category is already included in the promotion.",
        promotion_id: Optional[str] = None,
        category_id: Optional[int] = None,
        **kwargs
    ):
        super().__init__(message, **kwargs)
        if promotion_id:
            self.details["promotion_id"] = promotion_id
        if category_id:
            self.details["category_id"] = category_id


class PromotionProductNotFoundError(PromotionError):
    """Raised when attempting to remove a product that is not in the promotion's applicable products list."""

    def __init__(
        self,
        message="Product not found in the promotion's applicable products.",
        promotion_id: Optional[str] = None,
        product_id: Optional[str] = None,
        **kwargs
    ):
        super().__init__(message, **kwargs)
        if promotion_id:
            self.details["promotion_id"] = promotion_id
        if product_id:
            self.details["product_id"] = product_id


class PromotionCategoryNotFoundError(PromotionError):
    """Raised when attempting to remove a category that is not in the promotion's applicable categories list."""

    def __init__(
        self,
        message="Category not found in the promotion's applicable categories.",
        promotion_id: Optional[str] = None,
        category_id: Optional[int] = None,
        **kwargs
    ):
        super().__init__(message, **kwargs)
        if promotion_id:
            self.details["promotion_id"] = promotion_id
        if category_id:
            self.details["category_id"] = category_id


class PromotionDateError(PromotionError):
    """Raised when there's an issue with promotion start/end dates."""

    def __init__(
        self,
        message="Invalid promotion dates.",
        promotion_id: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        **kwargs
    ):
        super().__init__(message, **kwargs)
        if promotion_id:
            self.details["promotion_id"] = promotion_id
        if start_date:
            self.details["start_date"] = start_date.isoformat()
        if end_date:
            self.details["end_date"] = end_date.isoformat()
