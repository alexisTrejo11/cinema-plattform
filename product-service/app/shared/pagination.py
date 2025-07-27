from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


class PaginationQuery(BaseModel):
    page: int = Field(
        default=1,
        ge=1,
        description="Page number for pagination, starting from 1",
        json_schema_extra={"example": 1},
    )
    page_size: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Number of items per page (max 100)",
        json_schema_extra={"example": 10},
    )
    sort_by: Optional[str] = Field(
        None,
        description="Field to sort by",
        json_schema_extra={"example": "name"},
    )
    sort_order: Optional[SortOrder] = Field(
        SortOrder.ASC,
        description="Sort order, either 'asc' or 'desc'",
        json_schema_extra={"example": "asc"},
    )


class PaginationMetadata(BaseModel):
    total_items: int = Field(
        ...,
        description="Total number of items available",
        json_schema_extra={"example": 100},
    )
    total_pages: int = Field(
        default=1,
        description="Total number of pages based on the limit",
        json_schema_extra={"example": 10},
    )
    current_page: int = Field(
        default=1,
        description="Current page number",
        json_schema_extra={"example": 1},
    )
    items_per_page: int = Field(
        ...,
        description="Number of items per page",
        json_schema_extra={"example": 10},
    )
