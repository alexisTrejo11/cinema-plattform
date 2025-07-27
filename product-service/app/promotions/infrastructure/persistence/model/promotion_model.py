from datetime import datetime
from decimal import Decimal
from typing import Dict, TYPE_CHECKING
from uuid import UUID
from sqlalchemy import (
    JSON,
    String,
    DateTime,
    Boolean,
    ForeignKey,
    DECIMAL,
    Integer,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from config.postgres_config import Base
from app.promotions.domain.promotion import (
    Promotion,
    PromotionId,
    ProductId,
    PromotionRule,
    PromotionType,
)
from dataclasses import asdict

if TYPE_CHECKING:
    from app.products.infrastructure.persistence.db.sql.models import (
        ProductModel,
        ProductCategoryModel,
    )


class PromotionModel(Base):
    __tablename__ = "promotions"

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True), primary_key=True, index=True
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    promotion_type: Mapped[str] = mapped_column(String(50), nullable=False)
    discount_value: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    rule: Mapped[Dict] = mapped_column(JSON, nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    max_uses: Mapped[int] = mapped_column(Integer, nullable=True)
    current_uses: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(), onupdate=datetime.now()
    )

    products = relationship(
        "ProductModel", secondary="promotion_products", back_populates="promotions", lazy="joined"
    )

    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("product_categories.id"), nullable=True
    )
    category = relationship("ProductCategoryModel", back_populates="promotions")

    def to_domain(self) -> Promotion:
        """Converts the model to a domain entity"""
        # Convert rule dict back to domain objects
        rule_dict = self.rule.copy()
        
        # Convert float back to Decimal
        if rule_dict.get('min_purchase_amount'):
            rule_dict['min_purchase_amount'] = Decimal(str(rule_dict['min_purchase_amount']))
        
        # Convert string UUIDs back to ProductId objects
        if rule_dict.get('required_products'):
            rule_dict['required_products'] = [ProductId.from_string(pid) for pid in rule_dict['required_products']]
        
        return Promotion(
            id=PromotionId(self.id),
            name=self.name,
            description=self.description,
            promotion_type=PromotionType(int(self.promotion_type)),
            discount_value=self.discount_value,
            applicable_product_ids=[ProductId(product.id) for product in self.products],
            rule=PromotionRule(**rule_dict),
            start_date=self.start_date,
            end_date=self.end_date,
            is_active=self.is_active,
            max_uses=self.max_uses,
            current_uses=self.current_uses,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_domain(cls, promotion: Promotion) -> "PromotionModel":
        """Creates a model instance from a domain entity"""
        # Convert PromotionRule to JSON-serializable dict
        rule_dict = asdict(promotion.rule)
        
        # Convert Decimal to float for JSON serialization
        if rule_dict.get('min_purchase_amount'):
            rule_dict['min_purchase_amount'] = float(rule_dict['min_purchase_amount'])
        
        # Convert ProductId objects to strings
        if rule_dict.get('required_products'):
            rule_dict['required_products'] = [str(pid.value) for pid in promotion.rule.required_products]
        
        return cls(
            id=promotion.id.value,
            name=promotion.name,
            description=promotion.description,
            promotion_type=str(promotion.promotion_type.value),
            discount_value=promotion.discount_value,
            rule=rule_dict,
            start_date=promotion.start_date,
            end_date=promotion.end_date,
            is_active=promotion.is_active,
            max_uses=promotion.max_uses,
            current_uses=promotion.current_uses,
        )


class PromotionProductModel(Base):
    __tablename__ = "promotion_products"

    promotion_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True), ForeignKey("promotions.id"), primary_key=True
    )
    product_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True), ForeignKey("products.id"), primary_key=True
    )

    min_quantity: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
