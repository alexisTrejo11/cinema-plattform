from __future__ import annotations

import grpc

from app.config.app_config import settings
from app.config.postgres_config import AsyncSessionLocal
from app.grpc.generated import catalog_pb2, catalog_pb2_grpc
from app.movies.infrastructure.persistence.sqlalchemy.repositories import (
    SQLAlchemyMovieRepository,
)
from app.cinema.infrastructure.persistence.sqlalchemy.repositories import (
    SQLAlchemyCinemaRepository,
)
from app.theater.infrastructure.persistence.sqlalchemy.repositories import (
    SQLAlchemyTheaterSeatRepository,
)


class CatalogServiceServicer(catalog_pb2_grpc.CatalogServiceServicer):
    async def IsMovieActive(
        self,
        request: catalog_pb2.IsMovieActiveRequest,
        context: grpc.aio.ServicerContext,
    ) -> catalog_pb2.IsMovieActiveResponse:
        async with AsyncSessionLocal() as session:
            repo = SQLAlchemyMovieRepository(session)
            movie = await repo.find_by_id(request.movie_id)
            return catalog_pb2.IsMovieActiveResponse(is_active=bool(movie and movie.is_active))

    async def IsCinemaActive(
        self,
        request: catalog_pb2.IsCinemaActiveRequest,
        context: grpc.aio.ServicerContext,
    ) -> catalog_pb2.IsCinemaActiveResponse:
        async with AsyncSessionLocal() as session:
            repo = SQLAlchemyCinemaRepository(session)
            cinema = await repo.find_by_id(request.cinema_id)
            return catalog_pb2.IsCinemaActiveResponse(
                is_active=bool(cinema and cinema.is_active)
            )

    async def TheaterHasSeats(
        self,
        request: catalog_pb2.TheaterHasSeatsRequest,
        context: grpc.aio.ServicerContext,
    ) -> catalog_pb2.TheaterHasSeatsResponse:
        async with AsyncSessionLocal() as session:
            repo = SQLAlchemyTheaterSeatRepository(session)
            has_seats = await repo.exists_by_theater(request.theater_id)
            return catalog_pb2.TheaterHasSeatsResponse(has_seats=bool(has_seats))

    async def ListTheaterSeats(
        self,
        request: catalog_pb2.ListTheaterSeatsRequest,
        context: grpc.aio.ServicerContext,
    ) -> catalog_pb2.ListTheaterSeatsResponse:
        async with AsyncSessionLocal() as session:
            repo = SQLAlchemyTheaterSeatRepository(session)
            seats = await repo.get_by_theater(request.theater_id)
            return catalog_pb2.ListTheaterSeatsResponse(
                seats=[
                    catalog_pb2.TheaterSeat(
                        id=seat.id or 0,
                        theater_id=seat.theater_id,
                        seat_row=seat.seat_row,
                        seat_number=seat.seat_number,
                    )
                    for seat in seats
                ]
            )


def create_catalog_grpc_server() -> grpc.aio.Server:
    server = grpc.aio.server()
    catalog_pb2_grpc.add_CatalogServiceServicer_to_server(
        CatalogServiceServicer(),
        server,
    )
    server.add_insecure_port(f"{settings.GRPC_HOST}:{settings.GRPC_PORT}")
    return server
