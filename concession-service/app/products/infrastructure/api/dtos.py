from typing import List
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from app.shared.schema import ProductBase, ProductCategoryBase
from app.shared.pagination import PaginationMetadata


class ProductResponse(ProductBase):
    """Response model for food products including ID"""

    id: UUID = Field(
        ...,
        description="Unique identifier of the product",
        json_schema_extra={"example": "75bb2bef-953f-47b2-8e48-6f3101515ebe"},
    )

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        from_attributes=True,
        json_schema_extra={
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
        },
    )

    @classmethod
    def from_entity(cls, product) -> "ProductResponse":
        product_dict = product.model_dump(exclude={"id"})
        return cls(id=product.id.value, **product_dict)


class ProductPaginatedResponse(BaseModel):
    product_page: List["ProductResponse"]
    metadata: PaginationMetadata


class ProductCategoryResponse(ProductCategoryBase):
    """Response model for food categories including ID"""

    id: int = Field(
        ...,
        description="Unique identifier of the category",
        json_schema_extra={"example": 1},
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Pizzas",
                "description": "Various pizza types",
                "is_active": True,
            }
        },
    )
