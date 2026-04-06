"""Idempotent Kafka processing using a Mongo unique index on event_id."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import TYPE_CHECKING

from pymongo.errors import DuplicateKeyError

if TYPE_CHECKING:
    from motor.motor_asyncio import AsyncIOMotorCollection

logger = logging.getLogger(__name__)


class KafkaEventDeduplicator:
    """
    Ensures each ``event_id`` is applied at most once to local state.
    Uses insert-before-process; on failure the claim row is removed so the
    message can be retried.
    """

    def __init__(self, collection: AsyncIOMotorCollection) -> None:
        self._col = collection

    async def ensure_indexes(self) -> None:
        await self._col.create_index("event_id", unique=True)

    async def try_claim(self, event_id: str) -> bool:
        """
        Returns True if this consumer should process the event (new claim),
        False if another replica already completed it.
        """
        try:
            await self._col.insert_one(
                {
                    "event_id": event_id,
                    "claimed_at": datetime.now(timezone.utc),
                }
            )
            return True
        except DuplicateKeyError:
            return False
        except Exception:
            logger.exception("dedup insert failed for event_id=%s", event_id)
            raise

    async def release(self, event_id: str) -> None:
        """Remove claim so a failed message can be retried."""
        await self._col.delete_one({"event_id": event_id})
