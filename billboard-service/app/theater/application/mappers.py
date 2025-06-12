from app.theater.domain.seat import TheaterSeat
from .dtos import TheaterSeatCreate, TheaterSeatUpdate
from datetime import datetime, timezone

class TheaterSeatMapper:
    @staticmethod
    def from_create_dto(dto: TheaterSeatCreate) -> TheaterSeat:
        now_utc = datetime.now(timezone.utc)
        return TheaterSeat(
            created_at=now_utc,
            updated_at=now_utc,
            **dto.model_dump()
        )

    @staticmethod
    def from_update_dto(update_data: TheaterSeatUpdate, existing_seat : TheaterSeat) -> TheaterSeat:
        update_data_dict = update_data.model_dump(exclude_unset=True)
        
        for key, value in update_data_dict.items():
            if key not in ['id', 'created_at']:
                setattr(existing_seat, key, value)

        return existing_seat
