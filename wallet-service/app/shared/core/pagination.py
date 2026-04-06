from dataclasses import dataclass
from typing import Generic, TypeVar

from fastapi import Query
from pydantic import BaseModel

T = TypeVar("T")

DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100


class PaginationParams(BaseModel):
    """
    Represents the parameters for a pagination request.

    Attributes:
        page (int): The page number (1-indexed).
        page_size (int): The number of items per page.

    Properties:
        offset (int): The offset of the items to return.
        limit (int): The limit of the items to return.
    """
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)")
    page_size: int = Query(default=DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE, description="Items per page")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size

class PaginationMetadata(BaseModel):
    """
    Represents the metadata for a pagination response.

    Attributes:
        total (int): The total number of items.
        page (int): The page number (1-indexed).
        page_size (int): The number of items per page.
        total_pages (int): The total number of pages.
        has_next (bool): Whether there is a next page.
        has_prev (bool): Whether there is a previous page.
    """
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool

@dataclass
class Page(Generic[T]):
    """
    Represents a page of items.

    Attributes:
        items (list[T]): The list of items.
        total (int): The total number of items.
        page (int): The page number (1-indexed).
        page_size (int): The number of items per page.

    Properties:
        total_pages (int): The total number of pages.
        has_next (bool): Whether there is a next page.
        has_prev (bool): Whether there is a previous page.
    """
    items: list[T]
    total: int
    page: int
    page_size: int

    @property
    def total_pages(self) -> int:
        if self.page_size == 0:
            return 0
        return (self.total + self.page_size - 1) // self.page_size

    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages

    @property
    def has_prev(self) -> bool:
        return self.page > 1

    def to_dict(self) -> dict:
        return {
            "items": self.items,
            "total": self.total,
            "page": self.page,
            "page_size": self.page_size,
            "total_pages": self.total_pages,
            "has_next": self.has_next,
            "has_prev": self.has_prev,
        }
