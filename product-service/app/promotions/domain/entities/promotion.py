from datetime import datetime
from typing import List, Optional
from .valueobjects import PromotionId, PromotionType, ProductId
from ..exceptions.promotion_exceptions import *


class Promotion:
    """Domain entity representing a commercial promotion"""

    def __init__(
        self,
        name: str,
        promotion_type: PromotionType,
        rule: dict,
        start_date: datetime,
        end_date: datetime,
        applicable_product_ids: Optional[List[ProductId]] = [],
        applicable_categories_ids: Optional[List[int]] = [],
        description: Optional[str] = None,
        is_active: bool = True,
        id: Optional[PromotionId] = None,
        max_uses: Optional[int] = None,
        current_uses: int = 0,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        """
        Args:
            name: Descriptive name of the promotion
            promotion_type: Type of promotion
            discount_value: Discount value (percentage or fixed amount)
            applicable_product_ids: List of products to which the promotion applies
            rule: Additional rules for applying the promotion
            start_date: Start date of validity
            end_date: End date of validity
            description: Optional description
            is_active: Indicates if the promotion is active
            id: Unique identifier (None for new promotions)
            max_uses: Maximum number of allowed uses (None for unlimited)
            current_uses: Number of times the promotion has been applied
        """

        self.id = id if id else PromotionId.generate()
        self.name = name
        self.promotion_type = promotion_type
        self.applicable_product_ids: List[ProductId] = applicable_product_ids or []
        self.applicable_categories_ids: List[int] = applicable_categories_ids or []
        self.rule = rule
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.is_active = is_active
        self.max_uses = max_uses
        self.current_uses = current_uses
        self.created_at = created_at if created_at else datetime.now()
        self.updated_at = updated_at if updated_at else datetime.now()

    def validate_creation_fields(self):
        promotion_id_str = str(self.id)

        # Name validation
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
        """Activates the promotion"""
        if self.is_active:
            raise PromotionAlreadyActiveError(promotion_id=str(self.id))
        self.is_active = True
        self.updated_at = datetime.now()

    def deactivate(self):
        """Deactivates the promotion"""
        if not self.is_active:
            raise PromotionAlreadyInactiveError(promotion_id=str(self.id))
        self.is_active = False
        self.updated_at = datetime.now()

    def extend_validity(self, new_end_date: datetime):
        """Extends the validity of the promotion"""
        promotion_id_str = str(self.id)
        if new_end_date <= self.end_date:
            raise PromotionDateError(
                "The new end date must be after the current end date",
                promotion_id=promotion_id_str,
                end_date=self.end_date,
                details={"new_end_date": new_end_date.isoformat()},
            )
        self.end_date = new_end_date
        self.updated_at = datetime.now()

    def add_applicable_products(self, product_ids: List[ProductId]):
        """Adds a list of products to the promotion"""
        promotion_id_str = str(self.id)
        for product_id in product_ids:
            if product_id in self.applicable_product_ids:
                raise PromotionProductAlreadyIncludedError(
                    f"Product {product_id} is already in the promotion",
                    promotion_id=promotion_id_str,
                    product_id=str(product_id),
                )
            self.applicable_product_ids.append(product_id)
        self.updated_at = datetime.now()

    def add_applicable_product(self, product_id: ProductId):
        """Adds a product to the list of applicable products"""
        promotion_id_str = str(self.id)
        if product_id in self.applicable_product_ids:
            raise PromotionProductAlreadyIncludedError(
                "The product is already in the promotion",
                promotion_id=promotion_id_str,
                product_id=str(product_id),
            )
        self.applicable_product_ids.append(product_id)
        self.updated_at = datetime.now()

    def add_applicable_category(self, category_id: int):
        """Adds a category to the list of applicable categories"""
        promotion_id_str = str(self.id)
        if category_id in self.applicable_categories_ids:
            raise PromotionCategoryAlreadyIncludedError(
                "The category is already in the promotion",
                promotion_id=promotion_id_str,
                category_id=category_id,
            )
        self.applicable_categories_ids.append(category_id)
        self.updated_at = datetime.now()

    def apply(self, quantity: int):
        """Applies the promotion to a given quantity of products"""
        promotion_id_str = str(self.id)
        if not self.is_active:
            raise PromotionAlreadyInactiveError(
                "Cannot apply an inactive promotion", promotion_id=promotion_id_str
            )

        # Check if promotion has expired
        if datetime.now() > self.end_date:
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
        self.updated_at = datetime.now()

    def reset_current_uses(self):
        """Resets the current uses of the promotion"""
        self.current_uses = 0
        self.updated_at = datetime.now()

    def validate_applicable_products(self, product_ids: List[ProductId]):
        """Validates that the provided product IDs are applicable to the promotion"""
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
        """Removes a list of products from the promotion"""
        promotion_id_str = str(self.id)
        for product_id in product_ids:
            if product_id not in self.applicable_product_ids:
                raise PromotionProductNotFoundError(
                    f"Product {product_id} is not found in the promotion's applicable products",
                    promotion_id=promotion_id_str,
                    product_id=str(product_id),
                )
            self.applicable_product_ids.remove(product_id)
        self.updated_at = datetime.now()

    def remove_applicable_category(self, category_id: int):
        """Removes a category from the list of applicable categories"""
        promotion_id_str = str(self.id)
        if category_id not in self.applicable_categories_ids:
            raise PromotionCategoryNotFoundError(
                f"Category {category_id} is not found in the promotion's applicable categories",
                promotion_id=promotion_id_str,
                category_id=category_id,
            )
        self.applicable_categories_ids.remove(category_id)
        self.updated_at = datetime.now()

    def clear_all(self):
        """Clears the list of applicable products"""
        self.applicable_product_ids.clear()
        self.applicable_categories_ids.clear()
        self.current_uses = 0
        self.is_active = True
        self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        """Converts the promotion to a dictionary representation"""
        return {
            "id": str(self.id),
            "name": self.name,
            "type": self.promotion_type.value,
            "applicable_product_ids": [str(pid) for pid in self.applicable_product_ids],
            "rule": self.rule if self.rule else None,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "description": self.description,
            "is_active": self.is_active,
            "max_uses": self.max_uses,
            "current_uses": self.current_uses,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Promotion":
        """Creates a Promotion instance from a dictionary representation"""
        rule_data = data.get("rule", {})

        return cls(
            id=PromotionId.from_string(data["id"]),
            name=data["name"],
            promotion_type=PromotionType(data["promotion_type"]),
            applicable_product_ids=[
                ProductId.from_string(pid) for pid in data["applicable_product_ids"]
            ],
            rule=rule_data,
            start_date=datetime.fromisoformat(data["start_date"]),
            end_date=datetime.fromisoformat(data["end_date"]),
            description=data.get("description"),
            is_active=data.get("is_active", True),
            max_uses=data.get("max_uses"),
            current_uses=data.get("current_uses", 0),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )

    def __hash__(self):
        return hash(
            (
                self.id,
                self.name,
                self.promotion_type,
                tuple(self.applicable_product_ids),
                self.start_date,
                self.end_date,
                self.is_active,
            )
        )

    def __eq__(self, other):
        if not isinstance(other, Promotion):
            return False
        return (
            self.id == other.id
            and self.name == other.name
            and self.promotion_type == other.promotion_type
            and self.applicable_product_ids == other.applicable_product_ids
            and self.start_date == other.start_date
            and self.end_date == other.end_date
            and self.is_active == other.is_active
        )

    def __repr__(self):
        return (
            f"Promotion(id={self.id}, name={self.name}, type={self.promotion_type}, "
            f"applicable_product_ids={self.applicable_product_ids}, "
            f"start_date={self.start_date}, end_date={self.end_date}, is_active={self.is_active})"
        )
