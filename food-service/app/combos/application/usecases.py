from typing import List
from .repository import ComboRepository
from .dtos import  ComboResponse, ComboCreate, ComboItemCreate
from .exceptions import ComboNotFoundError, ComboItemValidationError, ProductValidationError
from app.products.application.repositories import FoodRepository
from app.combos.domain.combo import Combo, ComboItem

class ListActiveComboUseCase:
    def __init__(self, combo_repository: ComboRepository) -> None:
        self.combo_repository = combo_repository
    
    def execute(self):
        combos = self.combo_repository.list_all(active_only=True)    
        return [ComboResponse(**combo.to_dict()) for combo in combos]


class GetComboByIdUseCase:
    def __init__(self, combo_repository: ComboRepository) -> None:
        self.combo_repository = combo_repository
    
    def execute(self, combo_id: int, include_items : bool = True):
        combo = self.combo_repository.get_by_id(combo_id, include_items)    
        if not combo:
            raise ComboNotFoundError(combo_id)

        return ComboResponse(**combo.to_dict())
    
    
class GetCombosByProductUseCase:
    def __init__(self, combo_repository: ComboRepository, product_repository: FoodRepository) -> None:
        self.combo_repository = combo_repository
        self.product_repository = product_repository
    
    def execute(self, product_id: int, include_items: bool = True) -> List[ComboResponse]:
        product = self.product_repository.get_by_id(product_id)
        if not product:
            raise ProductValidationError()

        combos = self.combo_repository.list_by_product(product_id, include_items)
        return [ComboResponse(**combo.to_dict()) for combo in combos]


class CreateComboUseCase:
    def __init__(self, combo_repository: ComboRepository, product_repository: FoodRepository) -> None:
        self.combo_repository = combo_repository
        self.product_repository = product_repository
    
    def execute(self, create_data : ComboCreate) -> ComboResponse:
        new_combo = Combo(**create_data.model_dump())
        
        items = self._generate_products(create_data)
        new_combo.items = items
        
        new_combo.validate_business_logic()
        
        combo_created = self.combo_repository.save(new_combo)
        return ComboResponse(**combo_created.to_dict()) 

    def _generate_products(self, create_data : ComboCreate) -> List[ComboItem]:
        self.validate_items(create_data.items)
        products_map = self.product_repository.get_by_id_in([item.product_id for item in create_data.items])
        
        items = []
        for item in create_data.items:
            combo_items = ComboItem(quantity= item.quantity, product=products_map[item.product_id])
            items.append(combo_items)
        
        return items
    
    
    def validate_items(self, required_items: List['ComboItemCreate']):
        if len(required_items) <= 0:
            raise ComboItemValidationError("at least one product is require to create a combo")
        elif len(required_items) == 1:
            if required_items[0].quantity <= 1:
                raise ComboItemValidationError("at least one item and two quantity are required to create a combo ")
        elif len(required_items) > 20:
                raise ComboItemValidationError("too much items")

        
class UpdateComboUseCase:
    def __init__(self, combo_repository: ComboRepository, product_repository: FoodRepository) -> None:
        self.combo_repository = combo_repository
        self.product_repository = product_repository
    
    def execute(self, combo_id: int, update_data : ComboCreate) -> ComboResponse:
        combo = self.combo_repository.get_by_id(combo_id)
        if not combo:
            raise ComboNotFoundError(combo_id)
                        
        data = update_data.model_dump(exclude_unset=True)
        for k,v in data.items():
            setattr(combo, k,v)
        
        combo.validate_business_logic()
        
        combo_updated = self.combo_repository.save(combo)
        return ComboResponse(**combo_updated.to_dict()) 


class DeleteComboUseCase:
    def __init__(self, combo_repository: ComboRepository) -> None:
        self.combo_repository = combo_repository
    
    def execute(self, combo_id: int) -> None:
        combo = self.combo_repository.get_by_id(combo_id)    
        if not combo:
            raise ComboNotFoundError(combo_id)

        self.combo_repository.soft_delete(combo_id)    
       