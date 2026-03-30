"""
Applies Kafka billboard-domain events to the local Mongo read model (ports).

See docs/event-catalog.md for event_type and payload shapes.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Mapping

from app.external.billboard.application.repositories.cinema_repository import (
    CinemaRepository,
)
from app.external.billboard.application.repositories.showtime_repository import (
    ShowtimeRepository,
)
from app.external.billboard.application.repositories.theater_repository import (
    TheaterRepository,
)
from app.external.billboard.core.entities.cinema import Cinema
from app.external.billboard.core.entities.showtime import Showtime
from app.external.billboard.core.entities.theater import Theater
from app.shared.events.infrastructure.kafka_deduplication import KafkaEventDeduplicator

logger = logging.getLogger(__name__)


class BillboardReplicationService:
    """Consumes billboard ``event_type`` envelopes and updates Mongo via repositories."""

    def __init__(
        self,
        cinema_repo: CinemaRepository,
        theater_repo: TheaterRepository,
        showtime_repo: ShowtimeRepository,
        dedup: KafkaEventDeduplicator,
    ) -> None:
        self._cinema = cinema_repo
        self._theater = theater_repo
        self._showtime = showtime_repo
        self._dedup = dedup

    async def apply_envelope(self, envelope: Mapping[str, Any]) -> None:
        event_id = envelope.get("event_id")
        if not event_id or not isinstance(event_id, str):
            raise ValueError("envelope missing event_id")

        if not await self._dedup.try_claim(event_id):
            logger.debug("skip duplicate event_id=%s", event_id)
            return

        try:
            event_type = envelope.get("event_type")
            if not event_type:
                raise ValueError("envelope missing event_type")
            payload = envelope.get("payload") or {}
            if not isinstance(payload, dict):
                raise ValueError("payload must be an object")

            await self._dispatch(str(event_type), payload)
        except Exception:
            await self._dedup.release(event_id)
            raise

    async def _dispatch(self, event_type: str, payload: Dict[str, Any]) -> None:
        if event_type == "cinema.upserted":
            await self._cinema_upserted(payload)
        elif event_type == "cinema.deactivated":
            await self._cinema_deactivated(payload)
        elif event_type == "theater.upserted":
            await self._theater_upserted(payload)
        elif event_type == "theater.deleted":
            await self._theater_deleted(payload)
        elif event_type == "showtime.upserted":
            await self._showtime_upserted(payload)
        elif event_type == "showtime.cancelled":
            await self._showtime_cancelled(payload)
        elif event_type == "movie.metadata.updated":
            logger.info("movie.metadata.updated ignored (optional projection)")
        else:
            logger.warning("unknown billboard event_type=%s", event_type)

    async def _cinema_upserted(self, payload: Dict[str, Any]) -> None:
        cinema = Cinema.model_validate(payload)
        await self._cinema.save(cinema)

    async def _cinema_deactivated(self, payload: Dict[str, Any]) -> None:
        cinema_id = int(payload["cinema_id"])
        cinema = await self._cinema.get_by_id(cinema_id)
        if cinema is None:
            logger.warning("cinema.deactivated: cinema_id=%s not in replica", cinema_id)
            return
        cinema.deactivate()
        await self._cinema.save(cinema)

    async def _theater_upserted(self, payload: Dict[str, Any]) -> None:
        theater = Theater.model_validate(payload)
        await self._theater.save(theater)

    async def _theater_deleted(self, payload: Dict[str, Any]) -> None:
        theater_id = int(payload["theater_id"])
        await self._theater.delete(theater_id)

    async def _showtime_upserted(self, payload: Dict[str, Any]) -> None:
        normalized = _normalize_showtime_payload(payload)
        showtime = Showtime.model_validate(normalized)
        existing = await self._showtime.get_by_id(showtime_id=showtime.id, raise_exception=False)
        if existing is None:
            await self._showtime.create(showtime)
        else:
            await self._showtime.update(showtime)

    async def _showtime_cancelled(self, payload: Dict[str, Any]) -> None:
        showtime_id = int(payload["showtime_id"])
        await self._showtime.delete(showtime_id)


def _normalize_showtime_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    data = dict(payload)
    if "showtime_id" in data and "id" not in data:
        data["id"] = data.pop("showtime_id")
    return data
