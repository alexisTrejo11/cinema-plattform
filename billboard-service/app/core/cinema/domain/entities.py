from pydantic import Field
from .base import CinemaBase
from typing import Optional

class Cinema(CinemaBase):
    """Domain model representing a cinema with all required fields"""
    id: Optional[int] = Field(None, description="Unique identifier for the cinema")