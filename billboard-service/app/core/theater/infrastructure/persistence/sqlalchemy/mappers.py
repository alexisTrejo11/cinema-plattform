from app.core.theater.domain.theater import Theater
from app.core.theater.domain.seat import TheaterSeat
from .models import TheaterModel, TheaterSeatModel


class TheaterModelMapper:
    @staticmethod
    def from_domain(theater_entity: Theater) -> TheaterModel:
        return TheaterModel(
            id=theater_entity.id if theater_entity.id else None,
            cinema_id=theater_entity.cinema_id,
            name=theater_entity.name,
            capacity=theater_entity.capacity,
            theater_type=theater_entity.theater_type,
            is_active=theater_entity.is_active,
            maintenance_mode=theater_entity.maintenance_mode,
        )

    @staticmethod
    def to_domain(theater_model: TheaterModel) -> Theater:
        return Theater(
            id=theater_model.id,
            cinema_id=theater_model.cinema_id,
            name=theater_model.name,
            capacity=theater_model.capacity,
            theater_type=theater_model.theater_type,
            is_active=theater_model.is_active,
            maintenance_mode=theater_model.maintenance_mode,
        )


class TheaterSeatModelMapper:
    """
    Mapper class to convert between TheaterSeat (domain)
    and TheaterSeatModel (persistence/ORM).
    """

    @staticmethod
    def from_domain(entity: TheaterSeat) -> TheaterSeatModel:
        """
        Converts a TheaterSeat domain object to a TheaterSeatModel ORM object.
        Used when saving/updating data in the database.
        """
        return TheaterSeatModel(
            id=entity.id if hasattr(entity, "id") else None,
            theater_id=entity.theater_id,
            seat_row=entity.seat_row,
            seat_number=entity.seat_number,
            seat_type=entity.seat_type,
            is_active=entity.is_active,
            created_at=entity.created_at if hasattr(entity, "created_at") else None,
            updated_at=entity.updated_at if hasattr(entity, "updated_at") else None,
        )

    @staticmethod
    def to_domain(model: TheaterSeatModel) -> TheaterSeat:
        """
        Converts a TheaterSeatModel ORM object to a TheaterSeat domain object.
        Used when retrieving data from the database for application logic.
        """
        return TheaterSeat(
            id=model.id,
            theater_id=model.theater_id,
            seat_row=model.seat_row,
            seat_number=model.seat_number,
            seat_type=model.seat_type,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
