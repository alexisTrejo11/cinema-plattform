from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field
from pydantic.types import PositiveInt, NonNegativeInt
from datetime import datetime
from typing import List, Optional
from app.promotions.domain.entities.promotion import PromotionType, Promotion
from app.shared.pagination import PaginationMetadata


class PromotionResponse(BaseModel):
    """
    Pydantic model for representing a Promotion in API responses.
    This mirrors the domain entity's structure, including system-generated fields.
    """

    id: UUID = Field(..., description="Unique identifier of the promotion")
    name: str = Field(..., description="Descriptive name of the promotion")
    promotion_type: PromotionType = Field(..., description="Type of promotion")

    rule: dict = Field(..., description="Additional rules for applying the promotion")
    start_date: datetime = Field(
        ..., description="Start date of the promotion's validity"
    )
    end_date: datetime = Field(..., description="End date of the promotion's validity")
    description: Optional[str] = Field(
        None, description="Optional description of the promotion"
    )
    is_active: bool = Field(..., description="Indicates if the promotion is active")
    max_uses: Optional[PositiveInt] = Field(
        None, description="Maximum number of allowed uses (None for unlimited)"
    )
    current_uses: NonNegativeInt = Field(
        ..., description="Current number of times the promotion has been used"
    )
    created_at: datetime = Field(
        ..., description="Timestamp when the promotion was created"
    )
    updated_at: datetime = Field(
        ..., description="Timestamp when the promotion was last updated"
    )
    applicable_product_ids: Optional[List[UUID]] = Field(
        None, description="List of products applicable to this promotion"
    )
    applicable_category_ids: Optional[List[str]] = Field(
        None, description="List of categories applicable to this promotion"
    )

    @classmethod
    def from_domain(cls, promotion: Promotion):
        """
        Convert a domain Promotion entity to a PromotionResponse model.
        Optionally include products if provided.
        """
        response = cls(
            id=promotion.id.value,
            name=promotion.name,
            promotion_type=promotion.promotion_type,
            rule=promotion.rule,
            start_date=promotion.start_date,
            end_date=promotion.end_date,
            description=promotion.description,
            is_active=promotion.is_active,
            max_uses=promotion.max_uses,
            current_uses=promotion.current_uses,
            created_at=promotion.created_at,
            updated_at=promotion.updated_at,
            applicable_product_ids=[p.value for p in promotion.applicable_product_ids],
            applicable_category_ids=[
                str(c) for c in promotion.applicable_categories_ids
            ],
        )
        return response

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Promotion 1",
                "promotion_type": "PERCENTAGE_DISCOUNT",
                "rule": {"percentage": 10},
                "start_date": "2021-01-01",
                "end_date": "2021-01-01",
                "description": "Promotion 1 description",
                "is_active": True,
                "max_uses": 100,
                "current_uses": 0,
                "created_at": "2021-01-01",
                "updated_at": "2021-01-01",
                "applicable_product_ids": ["123e4567-e89b-12d3-a456-426614174000"],
                "applicable_category_ids": ["123e4567-e89b-12d3-a456-426614174000"],
            }
        }
    )


class PromotionPaginatedResponse(BaseModel):
    """
    Pydantic model for representing a list of promotions in API responses.
    This is used when returning multiple promotions from search queries.
    """

    promotions: List[PromotionResponse] = Field(
        ..., description="List of promotions matching the search criteria"
    )

    paginationMetadata: PaginationMetadata = Field(
        ..., description="Metadata for pagination"
    )

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_domain(
        cls, promotions: List[Promotion], pagination_metadata: PaginationMetadata
    ):
        """
        Convert a list of domain Promotion entities to a PromotionPaginatedResponse model.
        """
        if not promotions:
            return cls(promotions=[], paginationMetadata=pagination_metadata)

        promotion_responses = [
            PromotionResponse.from_domain(promotion) for promotion in promotions
        ]
        return cls(
            promotions=promotion_responses,
            paginationMetadata=pagination_metadata,
        )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "promotions": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                    }
                ]
            }
        }
    )
