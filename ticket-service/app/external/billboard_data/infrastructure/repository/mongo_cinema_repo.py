from typing import List, Optional
from app.external.billboard_data.domain.entities.cinema import Cinema
from .mongo_mappers import CinemaMongoMapper

class MongoCinemaRepository:
    def __init__(self, mongo_db) -> None:
            self.collection = mongo_db['cinemas']
    
    async def get_by_id(self, theater_id: int) -> Optional[Cinema]:
        doc = await self.collection.find_one({"cinema_id": theater_id})
        if not doc:
            return None
        
        return CinemaMongoMapper.doc_to_domain(doc)

    async def get_all(self) -> List[Cinema]:
        cinemas = []
        async for doc in self.collection.find():
            cinemas.append(CinemaMongoMapper.doc_to_domain(doc))
        return cinemas

    async def create(self, cinema: Cinema) -> None:
        cinema_doc = CinemaMongoMapper.domain_to_doc(cinema)
        self.collection.insert_one(cinema_doc)
    
    
    async def update(self, cinema: Cinema) -> None:
        doc_to_update = CinemaMongoMapper.domain_to_doc(cinema)
        doc_to_update.pop("_id", None)
        doc_to_update.pop("cinema_id", None)

        result = self.collection.update_one(
            {"cinema_id": cinema.cinema_id},
            {"$set": doc_to_update}
        )
         
        if result.modified_count == 0:
            raise ValueError("Can't Update Theater")
    
    async def delete(self, theater_id: int) -> None:
        doc = self.collection.find_one({"theather_id":  theater_id})
        if not doc:
            raise ValueError("Can't Find Theater")
       
        self.collection.delete_one({"theater_id": theater_id})   

