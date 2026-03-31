"""
Outbound adapter: billboard / showtime service over gRPC for seat availability.

Implements :class:`~app.ticket.domain.ports.ShowtimeSeatAssertionPort`.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Optional

import grpc

import app.grpc  # noqa: F401 — bootstrap generated import path
from app.config.app_config import settings
from app.ticket.domain.exceptions import SeatUnavailableError
from app.ticket.domain.ports import ShowtimeSeatAssertionPort
from billboard.v1 import billboard_pb2, billboard_pb2_grpc

_log = logging.getLogger(__name__)

_client: Optional["GrpcBillboardSeatAssertionClient"] = None


class GrpcBillboardSeatAssertionClient(ShowtimeSeatAssertionPort):
    """gRPC client for ``cinema.billboard.v1.SeatAvailabilityService``."""

    def __init__(self, target: str, timeout: float) -> None:
        self._channel = grpc.insecure_channel(target)
        self._stub = billboard_pb2_grpc.SeatAvailabilityServiceStub(self._channel)
        self._timeout = timeout

    async def assert_seats_available_for_purchase(
        self, showtime_id: int, showtime_seat_ids: list[int]
    ) -> None:
        proto = billboard_pb2.AssertSeatsRequest(
            showtime_id=showtime_id,
            showtime_seat_ids=showtime_seat_ids,
        )
        loop = asyncio.get_running_loop()
        try:
            resp = await loop.run_in_executor(
                None,
                lambda: self._stub.AssertSeatsAvailable(proto, timeout=self._timeout),
            )
        except grpc.RpcError as exc:
            _log.warning("billboard AssertSeatsAvailable failed: %s", exc)
            raise SeatUnavailableError(
                showtime_seat_ids[0] if showtime_seat_ids else 0,
                f"gRPC {exc.code().name}: {exc.details() or 'billboard unavailable'}",
            ) from exc

        if not resp.ok:
            raise SeatUnavailableError(
                showtime_seat_ids[0] if showtime_seat_ids else 0,
                resp.message or "seats not available at source",
            )


def get_shared_billboard_seat_client() -> Optional[GrpcBillboardSeatAssertionClient]:
    """Singleton client when ``GRPC_BILLBOARD_TARGET`` is set; otherwise ``None``."""
    global _client
    target = settings.GRPC_BILLBOARD_TARGET.strip()
    if not target:
        return None
    if _client is None:
        _client = GrpcBillboardSeatAssertionClient(target, settings.GRPC_TIMEOUT_SECONDS)
        _log.info("gRPC billboard seat client target=%s", target)
    return _client
