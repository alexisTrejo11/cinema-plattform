from typing import Optional
from datetime import date, datetime

class Movie:
    def __init__(
        self, 
        title: str, 
        minute_duration: int, 
        release_date: date,
        end_date: date, id: Optional[int] = None,
        is_active: bool = True,
        created_at: Optional[datetime] = None, 
        updated_at: Optional[datetime] = None
    ):    
        if not isinstance(title, str) or not (1 <= len(title) <= 200):
            raise ValueError("Title must be a string between 1 and 200 characters.")
        if not isinstance(minute_duration, int) or minute_duration <= 0:
            raise ValueError("Minute duration must be a positive integer.")
        if not isinstance(release_date, date):
            raise ValueError("Release date must be a valid date object.")
        if not isinstance(end_date, date):
            raise ValueError("End date must be a valid date object.")
        if release_date > end_date:
            raise ValueError("Release date cannot be after end date.")
        if id is not None and not isinstance(id, int):
            raise ValueError("ID must be an integer or None.")
        if not isinstance(is_active, bool):
            raise ValueError("Is active must be a boolean.")
        if created_at is not None and not isinstance(created_at, datetime):
            raise ValueError("Created at must be a datetime object or None.")
        if updated_at is not None and not isinstance(updated_at, datetime):
            raise ValueError("Updated at must be a datetime object or None.")

        self.__id = id
        self.__title = title
        self.__minute_duration = minute_duration
        self.__release_date = release_date
        self.__end_date = end_date
        self.__is_active = is_active
        self.__created_at = created_at if created_at is not None else datetime.now()
        self.__updated_at = updated_at

    def get_id(self) -> Optional[int]:
        return self.__id

    def get_title(self) -> str:
        return self.__title

    def get_minute_duration(self) -> int:
        return self.__minute_duration

    def get_release_date(self) -> date:
        return self.__release_date

    def get_end_date(self) -> date:
        return self.__end_date

    def get_is_active(self) -> bool:
        return self.__is_active

    def get_created_at(self) -> Optional[datetime]:
        return self.__created_at

    def get_updated_at(self) -> Optional[datetime]:
        return self.__updated_at

    def __repr__(self):
        return (f"Movie(id={self.__id}, title='{self.__title}', "
                f"duration={self.__minute_duration} min, active={self.__is_active})")