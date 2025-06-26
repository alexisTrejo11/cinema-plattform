from app.food.application.repositories import FoodCategoryRepository, FoodRepository
from app.food.domain.entities import FoodProduct
from typing import Optional, List
from sqlalchemy.orm import Session

class SqlAlchFoodRepository(FoodRepository):
    def __init__(self, session: Session) -> None:
        self.session = session
    
    
    def get_by_id(self, category_id: int) -> Optional[FoodProduct]:
        pass
    

    def search(self, skip: int = 0, limit: int = 100, active_only: bool = True) -> List[FoodProduct]:
        pass
    

    def save(self, category: FoodProduct) -> FoodProduct:
        pass
    


    def delete(self, category_id: int) -> bool:
        pass
    