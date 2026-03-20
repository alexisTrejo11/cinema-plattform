from pydantic import BaseModel, Field
from typing import List, Any, Generic, TypeVar
from typing import Optional
from math import ceil


T = TypeVar("T")


class PaginationParams(BaseModel):
    offset: int = Field(default=0, ge=0)
    limit: int = Field(default=10, ge=1, le=100)
    sort_by: Optional[str] = None
    sort_order: Optional[str] = None

    @property
    def page(self) -> int:
        """Convert offset to 1-indexed page number."""
        return (self.offset // self.limit) + 1


class Page(BaseModel, Generic[T]):
    """
    Generic paginated response wrapper.

    Contains items and complete pagination metadata.
    """

    items: List[T] = Field(..., description="List of items for the current page.")
    total: int = Field(..., ge=0, description="Total number of items across all pages.")
    page: int = Field(..., ge=1, description="Current page number (1-indexed).")
    page_size: int = Field(..., ge=1, description="Number of items per page.")
    total_pages: int = Field(..., ge=0, description="Total number of pages.")
    has_next: bool = Field(..., description="Whether there is a next page.")
    has_previous: bool = Field(..., description="Whether there is a previous page.")

    @classmethod
    def create(cls, items: List[T], total: int, params: PaginationParams) -> "Page[T]":
        """
        Factory method to create a Page from items, total count, and pagination params.

        Args:
            items: List of items for the current page
            total: Total number of items across all pages
            params: Pagination parameters (offset, limit, etc.)

        Returns:
            Page[T] instance with calculated pagination metadata
        """
        page = params.page
        page_size = params.limit
        total_pages = ceil(total / page_size) if page_size > 0 else 0

        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_previous=page > 1,
        )


class PaginationResponse(BaseModel):
    data: List[Any] = Field(
        ...,
        description="List of items returned for the current page.",
    )
    page_size: int = Field(
        ...,
        ge=1,
        description="Maximum number of items returned per page.",
        examples=[10],
    )
    total_items: int = Field(
        ...,
        ge=0,
        description="Total number of items available across all pages.",
        examples=[42],
    )
    total_pages: int = Field(
        ...,
        ge=0,
        description="Total number of pages available for the given query.",
        examples=[5],
    )
    current_page: int = Field(
        ...,
        ge=1,
        description="Current page number (1-indexed).",
        examples=[2],
    )
    next_page: int = Field(
        ...,
        ge=1,
        description="Next page number if it exists; otherwise equals current page.",
        examples=[3],
    )
    previous_page: int = Field(
        ...,
        ge=1,
        description="Previous page number if it exists; otherwise equals current page.",
        examples=[1],
    )
    has_next: bool = Field(
        ...,
        description="Whether there is a next page available.",
    )
    has_previous: bool = Field(
        ...,
        description="Whether there is a previous page available.",
    )
