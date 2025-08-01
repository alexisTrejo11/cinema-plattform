import math
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
        default=None,
        description="Field to sort by",
        json_schema_extra={"example": "name"},
    )
    sort_order: Optional[SortOrder] = Field(
        default=SortOrder.ASC,
        description="Sort order, either 'asc' or 'desc'",
        json_schema_extra={"example": "asc"},
    )

    @classmethod
    def paginate_stmt(cls, stmt, page_params):
        if page_params.page is not None and page_params.page >= 0:
            stmt = stmt.offset((page_params.page - 1) * page_params.page_size)
        if page_params.page_size is not None and page_params.page_size > 0:
            stmt = stmt.limit(page_params.page_size)
        return stmt


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

    @classmethod
    def get_search_pagination_metadata(
        cls, page_data: PaginationQuery, total_items: int
    ) -> "PaginationMetadata":
        items_per_page = (
            page_data.page_size
            if page_data.page_size and page_data.page_size > 0
            else total_items
        )
        current_page = (
            (page_data.page * items_per_page) + 1
            if page_data.page and items_per_page
            else 1
        )
        total_pages = (
            math.ceil(total_items / items_per_page) if items_per_page > 0 else 1
        )

        return PaginationMetadata(
            total_items=total_items,
            total_pages=total_pages,
            current_page=current_page,
            items_per_page=items_per_page,
        )
