from app.food.application.repositories import FoodCategoryRepository 
from app.food.domain.entities import FoodCategory 
from typing import Optional, List
from .models import FoodCategoryModel
from sqlalchemy.orm import Session

class SQLAlchemyCategoryRepository(FoodCategoryRepository):
    def __init__(self, db: Session) -> None:
        self.db = db
        super().__init__()
    
    def get_by_id(self, category_id: int) -> Optional[FoodCategory]:
        return self.db.query(FoodCategory).filter(FoodCategoryModel.id == category_id).first()
    
    def list(self) -> List[FoodCategory]:
        query = self.db.query(FoodCategory)
        return query.all()

    def save(self, category: FoodCategory) -> FoodCategory:
        if category.id == 0:
            return self._create(model)
        else:
            model = FoodCategoryModel(**category.model_dump())            
            return self._update(model)

    def _create(self, category: FoodCategory) -> FoodCategory:
        model = FoodCategoryModel(**category.model_dump())
        model.id = None
        
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        
        return FoodCategory(id=model.id, name=model.name, description=model.description, is_active=model.is_active)


    def _update(self, category_model: FoodCategoryModel) -> FoodCategory:        
        self.db.commit()
        self.db.refresh(category_model)
        
        return FoodCategory(id=model.id, name=model.name, description=model.description, is_active=model.is_active)
    
    def delete(self, category_id: int) -> bool:
        category = self.get_by_id(category_id)
        if not category:
            return False
        
        self.db.delete(category)
        self.db.commit()
        
        return True