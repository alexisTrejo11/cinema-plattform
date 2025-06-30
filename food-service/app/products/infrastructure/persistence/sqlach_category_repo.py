from app.products.application.repositories import FoodCategoryRepository 
from app.products.domain.entities import FoodCategory 
from typing import Optional, List
from .models import FoodCategoryModel
from sqlalchemy.orm import Session

class SQLAlchemyCategoryRepository(FoodCategoryRepository):
    def __init__(self, session: Session) -> None:
        self.session = session
    
    def get_by_id(self, category_id: int) -> Optional[FoodCategory]:
        category_model = self.session.query(FoodCategoryModel).filter(
            FoodCategoryModel.id == category_id,
            FoodCategoryModel.is_active == True,
        ).first()
        
        if category_model:
            return category_model.to_domain()
        
    def list(self) -> List[FoodCategory]:
        categories = self.session.query(FoodCategoryModel).filter(FoodCategoryModel.is_active == True).all()

        return [category.to_domain() for category in categories]

    def save(self, category: FoodCategory) -> FoodCategory:
        model = FoodCategoryModel(**category.model_dump())
        if category.id == 0:
            model.id = None
            self.session.add(model)
            self.session.flush()
        else:
            self.session.merge(model)
            
        self.session.commit()
        
        if model in self.session:
            self.session.refresh(model)
        
        return model.to_domain()

    
    def delete(self, category_id: int) -> bool:
        category_model = self.session.query(FoodCategoryModel).filter(FoodCategoryModel.id == category_id).first()
        if not category_model:
            return False
        
        self.session.delete(category_model)
        self.session.commit()
        
        return True
    
    
    def exists_by_id(self, category_id: int) -> bool:
        return self.session.query(FoodCategoryModel).filter(FoodCategoryModel.id == category_id).first() is not None
    
    def exists_by_name(self, category_name: str) -> bool:
        return self.session.query(FoodCategoryModel).filter(FoodCategoryModel.name == category_name).first() is not None
      