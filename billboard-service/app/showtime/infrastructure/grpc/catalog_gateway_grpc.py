from __future__ import annotations

import grpc

from app.config.app_config import settings
from app.showtime.application.ports import CatalogGateway, CatalogTheaterSeat
from .generated import catalog_pb2, catalog_pb2_grpc


class GrpcCatalogGateway(CatalogGateway):
    def __init__(self, target: str | None = None):
        self.target = target or settings.GRPC_CATALOG_TARGET
        if not self.target:
            raise ValueError("GRPC_CATALOG_TARGET is required for GrpcCatalogGateway")

    async def is_movie_active(self, movie_id: int) -> bool:
        response = await self._call_is_movie_active(movie_id)
        return bool(response.is_active)

    async def is_cinema_active(self, cinema_id: int) -> bool:
        response = await self._call_is_cinema_active(cinema_id)
        return bool(response.is_active)

    async def theater_has_seats(self, theater_id: int) -> bool:
        response = await self._call_theater_has_seats(theater_id)
        return bool(response.has_seats)

    async def list_theater_seats(self, theater_id: int) -> list[CatalogTheaterSeat]:
        response = await self._call_list_theater_seats(theater_id)
        return [
            CatalogTheaterSeat(
                id=int(seat.id),
                theater_id=int(seat.theater_id),
                seat_row=str(seat.seat_row),
                seat_number=int(seat.seat_number),
            )
            for seat in response.seats
        ]

    async def _call_is_movie_active(
        self, movie_id: int
    ) -> catalog_pb2.IsMovieActiveResponse:
        async with grpc.aio.insecure_channel(self.target) as channel:
            stub = catalog_pb2_grpc.CatalogServiceStub(channel)
            return await stub.IsMovieActive(
                catalog_pb2.IsMovieActiveRequest(movie_id=movie_id),
                timeout=settings.GRPC_TIMEOUT_SECONDS,
            )

    async def _call_is_cinema_active(
        self, cinema_id: int
    ) -> catalog_pb2.IsCinemaActiveResponse:
        async with grpc.aio.insecure_channel(self.target) as channel:
            stub = catalog_pb2_grpc.CatalogServiceStub(channel)
            return await stub.IsCinemaActive(
                catalog_pb2.IsCinemaActiveRequest(cinema_id=cinema_id),
                timeout=settings.GRPC_TIMEOUT_SECONDS,
            )

    async def _call_theater_has_seats(
        self, theater_id: int
    ) -> catalog_pb2.TheaterHasSeatsResponse:
        async with grpc.aio.insecure_channel(self.target) as channel:
            stub = catalog_pb2_grpc.CatalogServiceStub(channel)
            return await stub.TheaterHasSeats(
                catalog_pb2.TheaterHasSeatsRequest(theater_id=theater_id),
                timeout=settings.GRPC_TIMEOUT_SECONDS,
            )

    async def _call_list_theater_seats(
        self, theater_id: int
    ) -> catalog_pb2.ListTheaterSeatsResponse:
        async with grpc.aio.insecure_channel(self.target) as channel:
            stub = catalog_pb2_grpc.CatalogServiceStub(channel)
            return await stub.ListTheaterSeats(
                catalog_pb2.ListTheaterSeatsRequest(theater_id=theater_id),
                timeout=settings.GRPC_TIMEOUT_SECONDS,
            )
