from typing import List, Optional

from pymongo.database import Database

from app.external.billboard.application.repositories.showtime_repository import (
    ShowtimeRepository,
)
from app.external.billboard.core.entities.showtime import Showtime
from app.external.billboard.infrastructure.repository.mongo_mappers import (
    ShowtimeDocMapper,
)


class MongoShowtimeRepository(ShowtimeRepository):
    def __init__(self, mongo_db) -> None:
        self.collection = mongo_db["showtimes"]

    async def get_by_id(
        self, showtime_id: int, raise_exception: bool = True
    ) -> Optional[Showtime]:
        doc = await self.collection.find_one({"showtime_id": showtime_id})
        if doc:
            return ShowtimeDocMapper.doc_to_domain(doc)

        if not raise_exception:
            return None

        raise ValueError("Showtime not found")

    async def get_all(self) -> List[Showtime]:
        showtimes: List[Showtime] = []
        async for doc in self.collection.find():
            showtimes.append(ShowtimeDocMapper.doc_to_domain(doc))
        return showtimes

    async def create(self, showtime: Showtime) -> None:
        showtime_doc = ShowtimeDocMapper.domain_to_doc(showtime)
        await self.collection.insert_one(showtime_doc)

    async def update(self, showtime: Showtime) -> None:
        doc_to_update = ShowtimeDocMapper.domain_to_doc(showtime)
        doc_to_update.pop("_id", None)

        result = await self.collection.update_one(
            {"showtime_id": showtime.get_id()}, {"$set": doc_to_update}
        )

        if result.matched_count == 0:
            raise ValueError("Can't Update showtime")

    async def delete(self, showtime_id: int) -> None:
        doc = await self.collection.find_one({"showtime_id": showtime_id})
        if not doc:
            raise ValueError("Can't Find showtime")

        await self.collection.delete_one({"showtime_id": showtime_id})
