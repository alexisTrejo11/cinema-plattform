from typing import Optional
from pydantic import BaseModel
from dataclasses import dataclass

class PaginationParams:
    def __init__( self, offset: int = 0, limit: int = 10) -> None:
        self.offset = offset
        self.limit = limit

#TODO
@dataclass
class PaginationMetadata:
    has_next: bool = False
    page_number: int = 0
    page_size: int = 0
    total_elements: int = 0

