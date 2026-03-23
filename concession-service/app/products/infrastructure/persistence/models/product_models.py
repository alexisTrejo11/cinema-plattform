import __future__
from uuid import UUID
from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import (
    DECIMAL,
    Integer,
    String,
    Boolean,
    DateTime,
    Text,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from app.config.db.postgres_config import Base
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.products.domain.entities.product_category import ProductCategory


class ProductCategoryModel(Base):
    __tablename__ = "product_categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(), onupdate=datetime.now()
    )
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    products = relationship("ProductModel", back_populates="category")
    promotions = relationship("PromotionModel", back_populates="category")

    promotions = relationship(
        "PromotionModel", secondary="promotion_categories", back_populates="categories"
    )

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
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now(), onupdate=datetime.now()
    )
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    category = relationship("ProductCategoryModel", back_populates="products")
    combo_items = relationship("ComboItemModel", back_populates="product")
    promotions = relationship(
        "PromotionModel", secondary="promotion_products", back_populates="products"
    )
