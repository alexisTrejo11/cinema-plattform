from typing import Optional

from pymongo.database import Database

from app.external.billboard.application.repositories.theater_repository import (
    TheaterRepository,
)
from app.external.billboard.core.entities.theater import Theater
from app.external.billboard.infrastructure.repository.mongo_mappers import (
    TheaterMongoMapper,
)


class MongoTheaterRepository(TheaterRepository):
    def __init__(self, mongo_db: Database) -> None:
        self.collection = mongo_db["theaters"]

    async def get_by_id(self, theater_id: int) -> Optional[Theater]:
        doc = await self.collection.find_one({"theater_id": theater_id})
        if not doc:
            return None
        return TheaterMongoMapper.doc_to_domain(doc)

    async def save(self, theater: Theater) -> None:
        doc = TheaterMongoMapper.domain_to_doc(theater)
        doc.pop("_id", None)
        await self.collection.replace_one(
            {"theater_id": theater.theater_id},
            doc,
            upsert=True,
        )

    async def delete(self, theater_id: int) -> None:
        await self.collection.delete_one({"theater_id": theater_id})
