import __future__
from datetime import datetime
from decimal import Decimal
from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import ForeignKey, Numeric, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY
from app.products.infrastructure.persistence.models import Base

if TYPE_CHECKING:
    from app.products.infrastructure.persistence.models import  FoodProductModel


class ComboModel(Base):
    __tablename__ = "combos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    discount_percentage: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=Decimal('0'))
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(nullable=True, default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(nullable=True, default=datetime.now(), onupdate=datetime.now())
    
    # Relationships
    items: Mapped[List["ComboItemModel"]] = relationship(
        back_populates="combo", 
        cascade="all, delete-orphan"
    )

class ComboItemModel(Base):
    __tablename__ = "combo_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    combo_id: Mapped[int] = mapped_column(ForeignKey("combos.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(ForeignKey("food_products.id"))
    quantity: Mapped[int] = mapped_column(default=1)
    
    # Relationships
    combo: Mapped["ComboModel"] = relationship(back_populates="items")
    product: Mapped["FoodProductModel"] = relationship(back_populates="combo_items")
