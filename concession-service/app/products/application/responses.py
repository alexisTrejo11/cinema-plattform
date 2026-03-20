from typing import List
from uuid import UUID
from pydantic import Field, BaseModel
from app.shared.schema import ProductBase, ProductCategoryBase
from app.shared.pagination import PaginationMetadata


class ProductDetails(ProductBase):
    """Response model for food products including ID"""

    id: UUID = Field(
        ...,
        description="Unique identifier of the product",
        json_schema_extra={"example": "75bb2bef-953f-47b2-8e48-6f3101515ebe"},
    )

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Margherita Pizza",
                "description": "Classic pizza",
                "price": 12.99,
                "image_url": "https://example.com/pizza.jpg",
                "is_available": True,
                "preparation_time_mins": 20,
                "calories": 800,
                "category_id": 1,
            }
        }

    @classmethod
    def from_entity(cls, product) -> "ProductDetails":
        product_dict = product.to_dict()
        product_dict.pop("id", None)
        return cls(id=product.id.value, **product_dict)


class ProductSearchResponse(BaseModel):
    product_page: List["ProductDetails"]
    metadata: PaginationMetadata


class ProductCategoryResponse(ProductCategoryBase):
    """Response model for food categories including ID"""

    id: int = Field(
        ...,
        description="Unique identifier of the category",
        json_schema_extra={"example": 1},
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Pizzas",
                "description": "Various pizza types",
                "is_active": True,
            }
        }
