import __future__
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import (
    DECIMAL,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    Text,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from config.postgres_config import Base
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.products.domain.entities.product import Product, ProductId
from app.products.domain.entities.product_category import ProductCategory
from uuid import UUID

if TYPE_CHECKING:
    from app.combos.infrastructure.persistence.models import ComboItemModel
    from app.promotions.infrastructure.persistence.model.promotion_model import PromotionModel


class ProductCategoryModel(Base):
    __tablename__ = "product_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    products = relationship("ProductModel", back_populates="category")
    promotions = relationship("PromotionModel", back_populates="category")

    def to_domain(self) -> ProductCategory:
        return ProductCategory(
            id=self.id,
            name=self.name,
            description=self.description,
            is_active=self.is_active,
        )


class ProductModel(Base):
    __tablename__ = "products"

    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True), primary_key=True, index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    image_url: Mapped[str] = mapped_column(String(500))
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    preparation_time_mins: Mapped[int] = mapped_column(Integer)
    calories: Mapped[int] = mapped_column(Integer)
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("product_categories.id"), nullable=False
    )
    created_at: Mapped[str] = mapped_column(DateTime, default=datetime.now())
    updated_at: Mapped[str] = mapped_column(
        DateTime, default=datetime.now(), onupdate=datetime.now()
    )

    category = relationship("ProductCategoryModel", back_populates="products")
    combo_items = relationship("ComboItemModel", back_populates="product")
    promotions = relationship(
        "PromotionModel", secondary="promotion_products", back_populates="products"
    )

    def to_domain(self) -> Product:
        return Product(
            id=ProductId(self.id),
            name=self.name,
            image_url=self.image_url,
            description=self.description,
            price=Decimal(f"{self.price}"),
            is_available=self.is_available,
            preparation_time_mins=self.preparation_time_mins,
            calories=self.calories,
            category_id=self.category_id,
        )
