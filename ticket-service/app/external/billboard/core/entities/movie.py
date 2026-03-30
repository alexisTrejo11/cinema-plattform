from datetime import date, datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Movie(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    id: Optional[int] = Field(default=None, gt=0)
    title: str = Field(min_length=1, max_length=200)
    minute_duration: int = Field(gt=0)
    release_date: date
    end_date: date
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    @model_validator(mode='after')
    def validate_date_range(self) -> 'Movie':
        if self.release_date > self.end_date:
            raise ValueError('Release date cannot be after end date.')
        return self

    def get_id(self) -> Optional[int]:
        return self.id

    def get_title(self) -> str:
        return self.title

    def get_minute_duration(self) -> int:
        return self.minute_duration

    def get_release_date(self) -> date:
        return self.release_date

    def get_end_date(self) -> date:
        return self.end_date

    def get_is_active(self) -> bool:
        return self.is_active

    def get_created_at(self) -> Optional[datetime]:
        return self.created_at

    def get_updated_at(self) -> Optional[datetime]:
        return self.updated_at

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()
