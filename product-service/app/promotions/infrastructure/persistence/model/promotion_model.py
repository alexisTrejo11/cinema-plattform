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
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from config.postgres_config import Base
from app.promotions.domain.promotion_rule_factory import PromotionRule

if TYPE_CHECKING:
    from app.products.infrastructure.persistence.models.product_models import (
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
    rule: Mapped[Dict] = mapped_column(JSON, nullable=False)
    start_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    end_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    max_uses: Mapped[int] = mapped_column(Integer, nullable=True)
    current_uses: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now()
    )

    products = relationship(
        "ProductModel",
        secondary="promotion_products",
        back_populates="promotions",
        lazy="joined",
    )

    categories = relationship(
        "ProductCategoryModel",
        secondary="promotion_categories",
        back_populates="promotions",
        lazy="joined",
    )


class PromotionProductModel(Base):
    __tablename__ = "promotion_products"

    promotion_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True), ForeignKey("promotions.id"), primary_key=True
    )
    product_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True), ForeignKey("products.id"), primary_key=True
    )


class PromotionCategoryModel(Base):
    __tablename__ = "promotion_categories"

    promotion_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True), ForeignKey("promotions.id"), primary_key=True
    )
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("product_categories.id"), primary_key=True
    )
