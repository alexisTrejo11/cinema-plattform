from datetime import datetime, timezone
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from .value_objects import PromotionId, PromotionType, ProductId
from ..exceptions.promotion_exceptions import *


def _utc_now() -> datetime:
    """Always use timezone-aware UTC for domain timestamps and comparisons."""
    return datetime.now(timezone.utc)


class Promotion(BaseModel):
    """Domain entity representing a commercial promotion."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    promotion_type: PromotionType
    rule: dict = Field(default_factory=dict)
    start_date: datetime
    end_date: datetime
    applicable_product_ids: List[ProductId] = Field(default_factory=list)
    applicable_categories_ids: List[int] = Field(default_factory=list)
    description: Optional[str] = None
    is_active: bool = True
    id: PromotionId = Field(default_factory=PromotionId.generate)
    max_uses: Optional[int] = None
    current_uses: int = 0
    created_at: datetime = Field(default_factory=_utc_now)
    updated_at: datetime = Field(default_factory=_utc_now)

    def validate_creation_fields(self):
        promotion_id_str = str(self.id)

        if not self.name:
            raise InvalidPromotionDataError(
                "The promotion name cannot be empty",
                field_name="name",
                promotion_id=promotion_id_str,
            )
        if not isinstance(self.name, str) or len(self.name) < 3:
            raise InvalidPromotionDataError(
                "Invalid promotion name",
                field_name="name",
                promotion_id=promotion_id_str,
            )

        if not isinstance(self.promotion_type, PromotionType):
            raise InvalidPromotionDataError(
                "Invalid promotion type",
                field_name="promotion_type",
                promotion_id=promotion_id_str,
            )

        if self.applicable_product_ids:
            if not isinstance(self.applicable_product_ids, list) or not all(
                isinstance(pid, ProductId) for pid in self.applicable_product_ids
            ):
                raise InvalidPromotionDataError(
                    "Invalid product IDs in the promotion",
                    field_name="applicable_product_ids",
                    promotion_id=promotion_id_str,
                )

        if self.applicable_categories_ids:
            if not isinstance(self.applicable_categories_ids, list) or not all(
                isinstance(cid, int) for cid in self.applicable_categories_ids
            ):
                raise InvalidPromotionDataError(
                    "Invalid category IDs in the promotion",
                    field_name="applicable_categories_ids",
                    promotion_id=promotion_id_str,
                )

        if not isinstance(self.start_date, datetime) or not isinstance(
            self.end_date, datetime
        ):
            raise PromotionDateError(
                "Start and end dates must be valid datetime objects",
                promotion_id=promotion_id_str,
            )

        if self.start_date.tzinfo is None or self.end_date.tzinfo is None:
            raise PromotionDateError(
                "Start and end dates must be timezone-aware (use UTC, e.g. datetime.now(timezone.utc)).",
                promotion_id=promotion_id_str,
                start_date=self.start_date,
                end_date=self.end_date,
            )

        if self.start_date >= self.end_date:
            raise PromotionDateError(
                "The start date must be before the end date",
                promotion_id=promotion_id_str,
                start_date=self.start_date,
                end_date=self.end_date,
            )

        if self.max_uses is not None and not isinstance(self.max_uses, int):
            raise InvalidPromotionDataError(
                "Maximum uses must be an integer",
                field_name="max_uses",
                promotion_id=promotion_id_str,
            )

        if not isinstance(self.current_uses, int):
            raise InvalidPromotionDataError(
                "Current uses must be an integer",
                field_name="current_uses",
                promotion_id=promotion_id_str,
            )

        if self.current_uses < 0:
            raise InvalidPromotionDataError(
                "The current number of uses cannot be negative",
                field_name="current_uses",
                promotion_id=promotion_id_str,
            )

        if self.max_uses is not None and self.current_uses > self.max_uses:
            raise InvalidPromotionDataError(
                "The current number of uses cannot exceed the maximum allowed",
                field_name="current_uses",
                promotion_id=promotion_id_str,
                details={"max_uses": self.max_uses, "current_uses": self.current_uses},
            )

    def activate(self):
        if self.is_active:
            raise PromotionAlreadyActiveError(promotion_id=str(self.id))
        self.is_active = True
        self.updated_at = _utc_now()

    def deactivate(self):
        if not self.is_active:
            raise PromotionAlreadyInactiveError(promotion_id=str(self.id))
        self.is_active = False
        self.updated_at = _utc_now()

    def extend_validity(self, new_end_date: datetime):
        promotion_id_str = str(self.id)
        if new_end_date.tzinfo is None:
            raise PromotionDateError(
                "The new end date must be timezone-aware (use UTC).",
                promotion_id=promotion_id_str,
                end_date=self.end_date,
                details={"new_end_date": new_end_date.isoformat()},
            )
        if new_end_date <= self.end_date:
            raise PromotionDateError(
                "The new end date must be after the current end date",
                promotion_id=promotion_id_str,
                end_date=self.end_date,
                details={"new_end_date": new_end_date.isoformat()},
            )
        self.end_date = new_end_date
        self.updated_at = _utc_now()

    def add_applicable_products(self, product_ids: List[ProductId]):
        promotion_id_str = str(self.id)
        for product_id in product_ids:
            if product_id in self.applicable_product_ids:
                raise PromotionProductAlreadyIncludedError(
                    f"Product {product_id} is already in the promotion",
                    promotion_id=promotion_id_str,
                    product_id=str(product_id),
                )
            self.applicable_product_ids.append(product_id)
        self.updated_at = _utc_now()

    def add_applicable_product(self, product_id: ProductId):
        promotion_id_str = str(self.id)
        if product_id in self.applicable_product_ids:
            raise PromotionProductAlreadyIncludedError(
                "The product is already in the promotion",
                promotion_id=promotion_id_str,
                product_id=str(product_id),
            )
        self.applicable_product_ids.append(product_id)
        self.updated_at = _utc_now()

    def add_applicable_category(self, category_id: int):
        promotion_id_str = str(self.id)
        if category_id in self.applicable_categories_ids:
            raise PromotionCategoryAlreadyIncludedError(
                "The category is already in the promotion",
                promotion_id=promotion_id_str,
                category_id=category_id,
            )
        self.applicable_categories_ids.append(category_id)
        self.updated_at = _utc_now()

    def apply(self, quantity: int):
        promotion_id_str = str(self.id)
        if not self.is_active:
            raise PromotionAlreadyInactiveError(
                "Cannot apply an inactive promotion", promotion_id=promotion_id_str
            )

        if _utc_now() > self.end_date:
            raise PromotionExpiredError(
                "Cannot apply promotion: promotion has expired",
                promotion_id=promotion_id_str,
                end_date=self.end_date,
            )

        if self.max_uses is not None and self.current_uses + quantity > self.max_uses:
            raise PromotionMaxUsesExceededError(
                "Cannot apply promotion: maximum uses exceeded",
                promotion_id=promotion_id_str,
                max_uses=self.max_uses,
                current_uses=self.current_uses,
            )
        self.current_uses += quantity
        self.updated_at = _utc_now()

    def reset_current_uses(self):
        self.current_uses = 0
        self.updated_at = _utc_now()

    def validate_applicable_products(self, product_ids: List[ProductId]):
        promotion_id_str = str(self.id)
        if not self.applicable_product_ids:
            raise PromotionNotApplicableError(
                "No specific applicable products defined for this promotion to validate against.",
                promotion_id=promotion_id_str,
            )

        for product_id in product_ids:
            if product_id not in self.applicable_product_ids:
                raise PromotionNotApplicableError(
                    f"Product {product_id} is not applicable to this promotion",
                    promotion_id=promotion_id_str,
                    product_id=str(product_id),
                )

    def remove_applicable_products(self, product_ids: List[ProductId]):
        promotion_id_str = str(self.id)
        for product_id in product_ids:
            if product_id not in self.applicable_product_ids:
                raise PromotionProductNotFoundError(
                    f"Product {product_id} is not found in the promotion's applicable products",
                    promotion_id=promotion_id_str,
                    product_id=str(product_id),
                )
            self.applicable_product_ids.remove(product_id)
        self.updated_at = _utc_now()

    def remove_applicable_category(self, category_id: int):
        promotion_id_str = str(self.id)
        if category_id not in self.applicable_categories_ids:
            raise PromotionCategoryNotFoundError(
                f"Category {category_id} is not found in the promotion's applicable categories",
                promotion_id=promotion_id_str,
                category_id=category_id,
            )
        self.applicable_categories_ids.remove(category_id)
        self.updated_at = _utc_now()

    def clear_all(self):
        self.applicable_product_ids.clear()
        self.applicable_categories_ids.clear()
        self.current_uses = 0
        self.is_active = True
        self.updated_at = _utc_now()
