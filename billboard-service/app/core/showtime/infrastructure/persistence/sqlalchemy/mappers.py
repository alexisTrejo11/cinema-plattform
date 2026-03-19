from datetime import datetime, timezone
from decimal import Decimal
from typing import Dict, Any
from app.core.showtime.domain.entities.showtime import Showtime
from app.core.showtime.domain.enums import *
from app.core.showtime.domain.entities.showtime_seat import ShowtimeSeat
from app.core.showtime.application.dtos import ShowtimeCreate, ShowtimeUpdate
from .models import ShowtimeModel, ShowtimeSeatModel


class ShowtimeModelMapper:
    """
    Mapper class to convert between ShowtimeEntity (domain),
    ShowtimeCreate/Update DTOs, and ShowtimeModel (persistence/ORM).
    """

    @staticmethod
    def from_domain(entity: Showtime) -> ShowtimeModel:
        """
        Converts a ShowtimeEntity domain object to a ShowtimeModel ORM object.
        Used when saving/updating data in the database.
        Note: total_seats, available_seats, and seats are domain-only properties
        and are not directly mapped to the database model.
        """
        dumped_data = entity.model_dump(
            exclude_none=True, exclude={"total_seats", "available_seats", "seats"}
        )
        return ShowtimeModel(**dumped_data)

    @staticmethod
    def to_domain(model: ShowtimeModel) -> Showtime:
        """
        Converts a ShowtimeModel ORM object to a ShowtimeEntity domain object.
        Used when retrieving data from the database for application logic.
        Note: total_seats, available_seats, and seats need to be populated by
        separate logic (e.g., in a use case) if they are derived.
        Here, they will be set to their default values (e.g., None, 0, []).
        """
        start_time_utc = model.start_time
        if start_time_utc and start_time_utc.tzinfo is None:
            start_time_utc = start_time_utc.replace(tzinfo=timezone.utc)

        end_time_utc = model.end_time
        if end_time_utc and end_time_utc.tzinfo is None:
            end_time_utc = end_time_utc.replace(tzinfo=timezone.utc)

        # For created_at and updated_at, similar defensive checks
        created_at_utc = model.created_at
        if created_at_utc and created_at_utc.tzinfo is None:
            created_at_utc = created_at_utc.replace(tzinfo=timezone.utc)

        updated_at_utc = model.updated_at
        if updated_at_utc and updated_at_utc.tzinfo is None:
            updated_at_utc = updated_at_utc.replace(tzinfo=timezone.utc)

        deleted_at_utc = model.deleted_at
        if deleted_at_utc and deleted_at_utc.tzinfo is None:
            deleted_at_utc = deleted_at_utc.replace(tzinfo=timezone.utc)

        return Showtime(
            id=model.id,
            movie_id=model.movie_id,
            cinema_id=model.cinema_id,
            theater_id=model.theater_id,
            price=Decimal(str(model.price)),
            start_time=start_time_utc,
            end_time=end_time_utc,
            type=ShowtimeType(model.type),
            status=ShowtimeStatus(model.status),
            language=ShowtimeLanguage(model.language),
            total_seats=0,
            available_seats=0,
            seats=[],
            created_at=created_at_utc,
            updated_at=updated_at_utc,
            deleted_at=deleted_at_utc,
        )

    @staticmethod
    def from_create_request(dto: ShowtimeCreate) -> ShowtimeModel:
        """
        Converts a ShowtimeCreate DTO to a ShowtimeModel ORM object for insertion.
        Sets created_at and updated_at to the current UTC time.
        """
        now_utc = datetime.now(timezone.utc)

        return ShowtimeModel(created_at=now_utc, updated_at=now_utc, **dto.model_dump())

    @staticmethod
    def from_update_dto(dto: ShowtimeUpdate) -> Dict[str, Any]:
        """
        Converts a ShowtimeUpdate DTO to a dictionary of fields to update.
        Uses exclude_unset=True for partial updates.
        This dictionary can then be applied to an existing ShowtimeModel instance.
        """
        update_data = dto.model_dump(exclude_unset=True, exclude={"id"})

        update_data["updated_at"] = datetime.now(timezone.utc)

        return update_data


class ShowtimeSeatModelMapper:
    @staticmethod
    def from_domain(entity: ShowtimeSeat) -> ShowtimeSeatModel:
        dumped_data = entity.model_dump()
        return ShowtimeSeatModel(**dumped_data)

    @staticmethod
    def to_domain(model: ShowtimeSeatModel) -> ShowtimeSeat:
        return ShowtimeSeat.model_validate(model)
