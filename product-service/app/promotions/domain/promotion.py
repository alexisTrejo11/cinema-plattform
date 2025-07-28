from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from .valueobjects import PromotionId, PromotionType, PromotionRule, ProductId
from app.shared.base_exceptions import DomainException
from .service.validation_service import (
    PromotionValidationService as ValidationService,
)


class Promotion:
    """Domain entity representing a commercial promotion"""

    def __init__(
        self,
        name: str,
        promotion_type: PromotionType,
        discount_value: Decimal,
        applicable_product_ids: List[ProductId],
        rule: PromotionRule,
        start_date: datetime,
        end_date: datetime,
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
        self.discount_value = discount_value
        self.applicable_product_ids = applicable_product_ids
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
        ValidationService.validate_fields(
            name=self.name,
            discount_value=self.discount_value,
            rule=self.rule,
            start_date=self.start_date,
            end_date=self.end_date,
            max_uses=self.max_uses,
            current_uses=self.current_uses,
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

    def to_dict(self) -> dict:
        """Converts the promotion to a dictionary representation"""
        return {
            "id": str(self.id),
            "name": self.name,
            "promotion_type": self.promotion_type.value,
            "discount_value": str(self.discount_value),
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
        return cls(
            id=PromotionId.from_string(data["id"]),
            name=data["name"],
            promotion_type=PromotionType(data["promotion_type"]),
            discount_value=Decimal(data["discount_value"]),
            applicable_product_ids=[
                ProductId.from_string(pid) for pid in data["applicable_product_ids"]
            ],
            rule=PromotionRule.from_dict(data["rule"]),
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
                self.discount_value,
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
            and self.discount_value == other.discount_value
            and self.applicable_product_ids == other.applicable_product_ids
            and self.start_date == other.start_date
            and self.end_date == other.end_date
            and self.is_active == other.is_active
        )

    def __repr__(self):
        return (
            f"Promotion(id={self.id}, name={self.name}, promotion_type={self.promotion_type}, "
            f"discount_value={self.discount_value}, applicable_product_ids={self.applicable_product_ids}, "
            f"start_date={self.start_date}, end_date={self.end_date}, is_active={self.is_active})"
        )
