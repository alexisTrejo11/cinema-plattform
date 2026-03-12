from ..domain.entities import Cinema
from .dtos import CreateCinemaRequest, UpdateCinemaRequest


class CinemaMapper:

    @staticmethod
    def from_create_request(cinema_create: CreateCinemaRequest) -> Cinema:
        return Cinema(**cinema_create.model_dump())

    @staticmethod
    def update_cinema_from_request(
        existing_cinema: Cinema, cinema_update: UpdateCinemaRequest
    ) -> Cinema:
        update_data = cinema_update.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(existing_cinema, key, value)

        return existing_cinema
