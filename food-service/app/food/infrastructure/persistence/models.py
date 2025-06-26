from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class FoodCategoryModel(Base):
    __tablename__ = "food_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    

    products = relationship("FoodProduct", back_populates="category")

class FoodProduct(Base):
    __tablename__ = "food_products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    image_url = Column(String(500))
    is_available = Column(Boolean, default=True)
    preparation_time_mins = Column(Integer)
    calories = Column(Integer)
    category_id = Column(Integer, ForeignKey("food_categories.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    category = relationship("FoodCategory", back_populates="products")
    combo_items = relationship("ComboItem", back_populates="product")
