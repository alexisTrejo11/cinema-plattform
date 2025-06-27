from sqlalchemy import  Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, mapped_column, Mapped
from datetime import datetime
from app.food.domain.entities import FoodCategory, FoodProduct
from decimal import Decimal

Base = declarative_base()

class FoodCategoryModel(Base):
    __tablename__ = "food_categories"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    products = relationship("FoodProductModel", back_populates="category")

    def to_domain(self) -> FoodCategory:
        return FoodCategory(
            id=self.id, 
            name=self.name, 
            description=self.description, 
            is_active=self.is_active        
            )
        

class FoodProductModel(Base):
    __tablename__ = "food_products"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    image_url: Mapped[str] = mapped_column(String(500))
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    preparation_time_mins: Mapped[int] = mapped_column(Integer)
    calories: Mapped[int] = mapped_column(Integer)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("food_categories.id"), nullable=False)
    created_at: Mapped[str] = mapped_column(DateTime, default=datetime.now())
    updated_at: Mapped[str] = mapped_column(DateTime, default=datetime.now(), onupdate=datetime.now())
    
    category = relationship("FoodCategoryModel", back_populates="products")
    #combo_items = relationship("ComboItem", back_populates="product")

    def to_domain(self) -> FoodProduct:
        return FoodProduct(
            id=self.id,
            name=self.name,
            image_url=self.image_url,
            description=self.description,
            price=self.price,
            is_available=self.is_available,
            preparation_time_mins=self.preparation_time_mins,
            calories=self.calories,
            category_id=self.category_id,
        )