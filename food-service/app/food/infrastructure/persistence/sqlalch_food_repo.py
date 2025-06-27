from app.food.application.repositories import FoodCategoryRepository, FoodRepository
from app.food.domain.entities import FoodProduct
from typing import Optional, List
from sqlalchemy.orm import Session
from .models import FoodProductModel
from app.food.application.dtos import SearchFoodParams


class SqlAlchFoodRepository(FoodRepository):
    def __init__(self, session: Session) -> None:
        self.session = session
    
    
    def get_by_id(self, product_id: int) -> Optional[FoodProduct]:
        model = self.session.query(FoodProductModel).filter(
            FoodProductModel.id == product_id,
            FoodProductModel.is_available == True,
        ).first()

        return model.to_domain() if model else None

    def search(self, food_params: SearchFoodParams) -> List[FoodProduct]:

        query = self.session.query(FoodProductModel)
        
        if food_params.min_price is not None:
            query = query.filter(FoodProductModel.price >= food_params.min_price)

        if food_params.max_price is not None:
            query = query.filter(FoodProductModel.price <= food_params.max_price)

        if food_params.name:
            query = query.filter(FoodProductModel.name.ilike(f"%{food_params.name}%"))

        if food_params.category is not None:
            query = query.filter(FoodProductModel.category_id == food_params.category)

        if food_params.active_only:
            query = query.filter(FoodProductModel.is_available == True)

        query = query.order_by(FoodProductModel.name)

        if food_params.offset is not None and food_params.offset >= 0:
            query = query.offset(food_params.offset)

        if food_params.limit is not None and food_params.limit > 0:
            query = query.limit(food_params.limit)

        product_models = query.all()

        return [model.to_domain() for model in product_models]


    def save(self, product: FoodProduct) -> FoodProduct:
        model = FoodProductModel(**product.model_dump())
        if product.id == 0:
            model.id = None # type: ignore
            self.session.add(model)
            self.session.flush()
        else:
            self.session.merge(model)
            
        self.session.commit()
        
        if model in self.session:
            self.session.refresh(model)
        
        return model.to_domain()
    

    def delete(self, product_id: int) -> None:
        model = self.session.query(FoodProductModel).filter(FoodProductModel.id == product_id).first()
        if not model:
            return
        
        self.session.delete(model)
        self.session.commit()
  