from typing import List, Optional
from app.showtime.application.repositories.theater_repository import TheaterRepository
from pymongo.database import Database
from app.showtime.domain.entities.theater import Theater
from .mongo_mappers import TheaterMongoMapper as TheaterMapper

class MongoTheaterRepository(TheaterRepository):
    def __init__(self, mongo_db) -> None:
        self.collection = mongo_db['theaters']
    
    async def get_by_id(self, theater_id: int) -> Optional[Theater]:
        doc = await self.collection.find_one({"theater_id": theater_id})
        if not doc:
            return None
        
        return TheaterMapper.doc_to_domain(doc)

    async def get_all(self) -> List[Theater]:
        theaters = []
        async for doc in self.collection.find():
            theaters.append(TheaterMapper.doc_to_domain(doc))
        return theaters

    async def create(self, theater: Theater) -> None:
        theater_doc = TheaterMapper.domain_to_doc(theater)
        self.collection.insert_one(theater_doc)
    
    
    async def update(self, theater: Theater) -> None:
        doc_to_update = TheaterMapper.domain_to_doc(theater)
        doc_to_update.pop("_id", None)
        doc_to_update.pop("theater_id", None)

        result = self.collection.update_one(
            {"theater_id": theater.get_theater_id()},
            {"$set": doc_to_update}
        )
         
        if result.modified_count == 0:
            raise ValueError("Can't Update Theater")
    
    async def delete(self, theater_id: int) -> None:
        doc = self.collection.find_one({"theather_id":  theater_id})
        if not doc:
            raise ValueError("Can't Find Theater")
       
        self.collection.delete_one({"theater_id": theater_id})

