from typing import List, Optional

from app.external.billboard.application.repositories.cinema_repository import (
    CinemaRepository,
)
from app.external.billboard.core.entities import Cinema
from app.external.billboard.infrastructure.repository.mongo_mappers import (
    CinemaMongoMapper,
)


class MongoCinemaRepository(CinemaRepository):
    def __init__(self, mongo_db) -> None:
        self.collection = mongo_db["cinemas"]

    async def get_by_id(self, cinema_id: int) -> Optional[Cinema]:
        doc = await self.collection.find_one({"cinema_id": cinema_id})
        if not doc:
            return None

        return CinemaMongoMapper.doc_to_domain(doc)

    async def get_all(self) -> List[Cinema]:
        cinemas: List[Cinema] = []
        async for doc in self.collection.find():
            cinemas.append(CinemaMongoMapper.doc_to_domain(doc))
        return cinemas

    async def save(self, cinema: Cinema) -> None:
        cinema_doc = CinemaMongoMapper.domain_to_doc(cinema)
        cinema_doc.pop("_id", None)
        await self.collection.replace_one(
            {"cinema_id": cinema.cinema_id},
            cinema_doc,
            upsert=True,
        )

    async def delete(self, cinema_id: int) -> None:
        await self.collection.delete_one({"cinema_id": cinema_id})
