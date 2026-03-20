from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from app.combos.domain.entities.combo import Combo
from app.shared.schema import ComboBase, ComboItemBase
from app.shared.pagination import PaginationMetadata
from uuid import UUID


class ComboListResponse(BaseModel):
    """Paginated list of combos."""

    items: List["ComboResponse"] = Field(..., description="List of combos")
    metadata: PaginationMetadata = Field(..., description="Pagination metadata")


class ComboResponse(ComboBase):
    """Schema for combo meal responses"""

    id: UUID = Field(
        ...,
        description="Unique identifier for the combo",
        json_schema_extra={"example": "123e4567-e89b-12d3-a456-426614174000"},
    )

    combo_items: Optional[List["ComboItemResponse"]] = Field(
        None,
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

    class Config:
        from_attributes = True
        json_schema_extra = {
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
        }

    @classmethod
    def from_domain(cls, combo: Combo, include_items: Optional[bool] = False):
        """Convert domain model to DTO"""
        items = []
        if include_items:
            items = [
                ComboItemResponse(
                    id=item.id.value,
                    product_id=item.product.id.value,
                    quantity=item.quantity,
                )
                for item in combo.items
            ]
        combo_dict = combo.to_dict()
        combo_dict.pop("items")
        combo_dict.pop("id")

        return cls(
            id=combo.id.value,
            combo_items=items if include_items else None,
            **combo_dict
        )


class ComboItemResponse(ComboItemBase):
    """Schema for combo item responses with full product details"""

    id: UUID = Field(
        ...,
        description="Unique identifier for the combo item",
        json_schema_extra={"example": "123e4567-e89b-12d3-a456-426614174001"},
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
            "description": "Complete combo item response",
            "examples": [
                {
                    "id": "123e4567-e89b-12d3-a456-426614174001",
                    "product_id": "123e4567-e89b-22d3-a456-426614174002",
                    "quantity": 2,
                }
            ],
        }


ComboListResponse.model_rebuild()
