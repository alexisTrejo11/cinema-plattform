from app.shared.schema import ComboBase, ComboItemBase
from app.shared.pagination import PaginationMetadata, Page
from typing import List
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.combos.domain.entities.combo import Combo
from uuid import UUID


class ComboItemCreateRequest(ComboItemBase):
    """Schema for creating combo items"""

    pass


class ComboCreateRequest(ComboBase):
    """Schema for creating a new combo meal"""

    items: List["ComboItemCreateRequest"] = Field(
        ...,
        description="List of items included in the combo (1-10 items)",
        json_schema_extra={"example": [{"product_id": "prod_123", "quantity": 2}]},
    )


class PaginationQuery:
    """Schema for pagination query parameters"""

    page: int = Field(1, ge=1, description="Page number for pagination")
    size: int = Field(10, ge=1, le=100, description="Number of items per page")


class ComboPaginatedResponse(BaseModel):
    """Paginated list of combos."""

    items: List["ComboSummaryResponse"] = Field(..., description="List of combos")
    metadata: PaginationMetadata = Field(..., description="Pagination metadata")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "description": "Paginated list of combos",
            "examples": [
                {
                    "items": [
                        {
                            "id": "123e4567-e89b-12d3-a456-426614174000",
                            "name": "Family Bundle",
                            "description": "A bundle of family-sized items",
                            "price": 49.99,
                            "discount_percentage": 10.0,
                            "image_url": "https://example.com/image.jpg",
                            "is_available": True,
                            "created_at": "2023-01-01T12:00:00Z",
                            "updated_at": "2023-01-01T12:00:00Z",
                        }
                    ],
                }
            ],
        },
    )

    @classmethod
    def from_domain(cls, combo_page: Page[Combo]):
        return cls(
            items=[
                ComboSummaryResponse.from_domain(combo) for combo in combo_page.items
            ],
            metadata=combo_page.metadata,
        )


class ComboSummaryResponse(ComboBase):
    """Schema for combo meal summary responses"""

    id: UUID = Field(
        ...,
        description="Unique identifier for the combo",
        json_schema_extra={"example": "123e4567-e89b-12d3-a456-426614174000"},
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when the combo was created",
        json_schema_extra={"example": "2023-01-01T12:00:00Z"},
    )
    updated_at: datetime = Field(
        ...,
        description="Timestamp when the combo was last updated",
        json_schema_extra={"example": "2023-01-01T12:00:00Z"},
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "description": "Complete combo response with items",
            "examples": [
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "name": "Family Bundle",
                    "price": 49.99,
                    "discount_percentage": 10.0,
                    "image_url": "https://example.com/image.jpg",
                    "is_available": True,
                    "created_at": "2023-01-01T12:00:00Z",
                    "updated_at": "2023-01-01T12:00:00Z",
                }
            ],
        },
    )

    @classmethod
    def from_domain(cls, combo: Combo):
        return cls(
            id=combo.id.value,
            **combo.model_dump(exclude={"id"}),
        )


class ComboDetailResponse(ComboBase):
    """Schema for combo meal responses"""

    id: UUID = Field(
        ...,
        description="Unique identifier for the combo",
        json_schema_extra={"example": "123e4567-e89b-12d3-a456-426614174000"},
    )

    items: List["ComboItemResponse"] = Field(
        default_factory=list,
        description="Detailed information about items in the combo",
        json_schema_extra={
            "example": [
                {"product_id": "44f699451-3666-46bc-bcce-6d410c763744", "quantity": 2}
            ]
        },
    )

    created_at: datetime = Field(
        ...,
        description="Timestamp when the combo was created",
        json_schema_extra={"example": "2023-01-01T12:00:00Z"},
    )

    updated_at: datetime = Field(
        ...,
        description="Timestamp when the combo was last updated",
        json_schema_extra={"example": "2023-01-01T12:00:00Z"},
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "description": "Complete combo response with items",
            "examples": [
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "name": "Family Bundle",
                    "price": 49.99,
                    "items": [
                        {
                            "product_id": "4f699451-3666-46bc-bcce-6d410c763744",
                            "quantity": 2,
                        }
                    ],
                    "created_at": "2023-01-01T12:00:00Z",
                    "updated_at": "2023-01-01T12:00:00Z",
                }
            ],
        },
    )

    @classmethod
    def from_domain(cls, combo: Combo):
        """Convert domain model to DTO"""
        items = []
        if combo.items:
            items = [
                ComboItemResponse(
                    id=item.id.value,
                    product_id=item.product.id.value,
                    quantity=item.quantity,
                    name=item.product.name,
                    description=item.product.description or "",
                )
                for item in combo.items
            ]
        return cls(
            id=combo.id.value,
            name=combo.name,
            description=combo.description,
            price=combo.price,
            discount_percentage=combo.discount_percentage,
            image_url=combo.image_url,
            is_available=combo.is_available,
            created_at=combo.created_at,
            updated_at=combo.updated_at,
            items=items,
        )


class ComboItemResponse(ComboItemBase):
    """Schema for combo item responses with full product details"""

    id: UUID = Field(
        ...,
        description="Unique identifier for the combo item",
        json_schema_extra={"example": "123e4567-e89b-12d3-a456-426614174001"},
    )

    name: str = Field(
        ...,
        description="Name of the product",
        json_schema_extra={"example": "Product Name"},
    )

    description: str = Field(
        ...,
        description="Description of the product",
        json_schema_extra={"example": "Product Description"},
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "description": "Complete combo item response",
            "examples": [
                {
                    "id": "123e4567-e89b-12d3-a456-426614174001",
                    "product_id": "123e4567-e89b-22d3-a456-426614174002",
                    "quantity": 2,
                }
            ],
        },
    )
