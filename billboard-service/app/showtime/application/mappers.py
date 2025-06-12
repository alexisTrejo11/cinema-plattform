from datetime import datetime, timezone
from ..domain.entities.showtime import Showtime
from .dtos import ShowtimeCreate, ShowtimeUpdate

class ShowtimeMappers:
    """
    Mapper class to convert between Showtime DTOs (Create/Update)
    and the Showtime domain entity.
    """

    @staticmethod
    def from_create_dto(create_data: ShowtimeCreate) -> Showtime:
        """
        Converts a ShowtimeCreate DTO into a full Showtime domain entity
        for a new showtime.
        """
        now_utc = datetime.now(timezone.utc)
        
        return Showtime(
            created_at=now_utc,
            updated_at=now_utc,
            total_seats=None, 
            available_seats=0,
            seats=[],
            **create_data.model_dump()
        )

    @staticmethod
    def update_with_dto(update_data: ShowtimeUpdate, existing_entity: Showtime) -> Showtime:
        updated_data = update_data.model_dump(exclude_unset=True, exclude={'id'})
        for key, value in updated_data.items():
            setattr(existing_entity, key, value)

        existing_entity.updated_at = datetime.now(timezone.utc)
        return existing_entity
