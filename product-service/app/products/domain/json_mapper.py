from uuid import UUID
from typing import Dict, Any
from datetime import datetime
from decimal import Decimal
from .entities.product import Product, ProductId


class ProductJsonMapper:

    @staticmethod
    def to_dict(product: "Product") -> Dict[str, Any]:
        """Converts the FoodProduct instance to a dictionary."""
        return {
            "id": product.id.value,
            "name": product.name,
            "description": product.description,
            "price": str(product.price),
            "image_url": product.image_url,
            "is_available": product.is_available,
            "preparation_time_mins": product.preparation_time_mins,
            "calories": product.calories,
            "category_id": product.category_id,
            "created_at": product.created_at,
            "updated_at": product.updated_at,
        }

    @staticmethod
    def to_json(product: "Product") -> Dict[str, Any]:
        """Converts the FoodProduct instance to a JSON-serializable dictionary."""
        return ProductJsonMapper.to_dict(product)

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> "Product":
        """Creates a FoodProduct instance from a dictionary."""
        product_id = data.get("id", ProductId.generate())
        if isinstance(product_id, str):
            product_id = ProductId.from_string(product_id)
        elif not isinstance(product_id, ProductId):
            product_id = ProductId(product_id)
        elif isinstance(product_id, UUID):
            product_id = ProductId(product_id)

        price = data.get("price", Decimal("0.00"))
        if isinstance(price, str):
            price = Decimal(price)
        elif isinstance(price, float):
            price = Decimal(str(price))
        elif not isinstance(price, Decimal):
            price = Decimal(price)

        created_at = data.get("created_at", datetime.now())
        updated_at = data.get("updated_at", datetime.now())
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        if isinstance(updated_at, str):
            updated_at = datetime.fromisoformat(updated_at)

        return Product(
            id=product_id,
            name=data["name"],
            description=data.get("description"),
            price=price,
            image_url=data.get("image_url"),
            is_available=data["is_available"],
            preparation_time_mins=data.get("preparation_time_mins"),
            calories=data.get("calories"),
            category_id=data["category_id"],
            created_at=created_at,
            updated_at=updated_at,
        )
