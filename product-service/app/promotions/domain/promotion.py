from datetime import datetime
from decimal import Decimal
from typing import List, Optional, TYPE_CHECKING
from .valueobjects import PromotionId, PromotionType, ProductId
from app.shared.base_exceptions import DomainException

if TYPE_CHECKING:
    from .promotion_rule_factory import PromotionRule


class Promotion:
    """Domain entity representing a commercial promotion"""

    def __init__(
        self,
        name: str,
        promotion_type: PromotionType,
        rule: "PromotionRule",
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
        # Name validation
        if not self.name:
            raise DomainException("The promotion name cannot be empty")

        # Promotion type validation
        if not isinstance(self.promotion_type, PromotionType):
            raise DomainException("Invalid promotion type")

        # Applicable products validation
        if not isinstance(self.name, str) or len(self.name) < 3:
            raise DomainException("Invalid promotion name")

        # Applicable products validation
        if self.applicable_product_ids != []:
            if not isinstance(self.applicable_product_ids, list) or not all(
                isinstance(pid, ProductId) for pid in self.applicable_product_ids
            ):
                raise DomainException("Invalid product IDs in the promotion")

        # Applicable categories validation
        if self.applicable_categories_ids != []:
            if not isinstance(self.applicable_categories_ids, list) or not all(
                isinstance(cid, int) for cid in self.applicable_categories_ids
            ):
                raise DomainException("Invalid category IDs in the promotion")

        # Date range validation
        if not isinstance(self.start_date, datetime) or not isinstance(
            self.end_date, datetime
        ):
            raise DomainException("Start and end dates must be valid datetime objects")

        if isinstance(self.start_date, datetime) and isinstance(
            self.end_date, datetime
        ):
            if self.start_date >= self.end_date:
                raise DomainException("The start date must be before the end date")

        # Maximum uses validation
        if self.max_uses is not None and not isinstance(self.max_uses, int):
            raise DomainException("Maximum uses must be an integer")

        # Current uses validation
        if self.current_uses is not None and not isinstance(self.current_uses, int):
            raise DomainException("Current uses must be an integer")

        if self.current_uses < 0:
            raise DomainException("The current number of uses cannot be negative")

        if self.current_uses > (
            self.max_uses if self.max_uses is not None else float("inf")
        ):
            raise DomainException(
                "The current number of uses cannot exceed the maximum allowed"
            )

    def activate(self):
        """Activates the promotion"""
        if self.is_active:
            raise DomainException("The promotion is already active")
        self.is_active = True
        self.updated_at = datetime.now()

    def deactivate(self):
        """Deactivates the promotion"""
        if not self.is_active:
            raise DomainException("The promotion is already inactive")
        self.is_active = False
        self.updated_at = datetime.now()

    def extend_validity(self, new_end_date: datetime):
        """Extends the validity of the promotion"""
        if new_end_date <= self.end_date:
            raise DomainException("The new date must be after the current end date")
        self.end_date = new_end_date
        self.updated_at = datetime.now()

    def add_applicable_products(self, product_ids: List[ProductId]):
        """Adds a list of products to the promotion"""
        for product_id in product_ids:
            if product_id in self.applicable_product_ids:
                raise DomainException(
                    f"Product {product_id} is already in the promotion"
                )
            self.applicable_product_ids.append(product_id)
        self.updated_at = datetime.now()

    def add_applicable_product(self, product_id: ProductId):
        """Adds a product to the list of applicable products"""
        if product_id in self.applicable_product_ids:
            raise DomainException("The product is already in the promotion")
        self.applicable_product_ids.append(product_id)
        self.updated_at = datetime.now()

    def add_applicable_category(self, category_id: int):
        """Adds a category to the list of applicable categories"""
        if category_id in self.applicable_categories_ids:
            raise DomainException("The category is already in the promotion")
        self.applicable_categories_ids.append(category_id)
        self.updated_at = datetime.now()

    def apply(self, quantity: int):
        """Applies the promotion to a given quantity of products"""
        if not self.is_active:
            raise DomainException("Cannot apply an inactive promotion")
        if self.max_uses is not None and self.current_uses + quantity > self.max_uses:
            raise DomainException("Cannot apply promotion: maximum uses exceeded")
        self.current_uses += quantity
        self.updated_at = datetime.now()

    def reset_current_uses(self):
        """Resets the current uses of the promotion"""
        self.current_uses = 0
        self.updated_at = datetime.now()

    def validate_applicable_products(self, product_ids: List[ProductId]):
        """Validates that the provided product IDs are applicable to the promotion"""
        if not self.applicable_product_ids:
            raise DomainException("No applicable products defined for this promotion")

        for product_id in product_ids:
            if product_id not in self.applicable_product_ids:
                raise DomainException(
                    f"Product {product_id} is not applicable to this promotion"
                )

    def remove_applicable_products(self, product_ids: List[ProductId]):
        """Removes a list of products from the promotion"""
        for product_id in product_ids:
            if product_id not in self.applicable_product_ids:
                raise DomainException(
                    f"Product {product_id} is not applicable to this promotion"
                )
            self.applicable_product_ids.remove(product_id)
        self.updated_at = datetime.now()

    def remove_applicable_category(self, category_id: int):
        """Removes a category from the list of applicable categories"""
        if category_id not in self.applicable_categories_ids:
            raise DomainException(
                f"Category {category_id} is not applicable to this promotion"
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
            "rule": self.rule.to_dict() if self.rule else None,
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
            rule=PromotionRule.from_dict(**rule_data),
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
