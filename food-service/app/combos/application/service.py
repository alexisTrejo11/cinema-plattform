
class ComboService:
    def __init__(self, repository: ComboRepository, product_repository: FoodProductRepository):
        self.repository = repository
        self.product_repository = product_repository
    
    def create_combo(self, combo_data: ComboCreate) -> Optional[ComboResponse]:
        # Validar que todos los productos existen
        for item in combo_data.items:
            product = self.product_repository.get_by_id(db, item.product_id)
            if not product:
                return None
        
        combo_dict = combo_data.model_dump(exclude={'items'})
        items_data = [item.model_dump() for item in combo_data.items]
        
        combo = self.repository.create(db, combo_dict, items_data)
        return ComboResponse.model_validate(combo)
    
    def get_combo(self, combo_id: int) -> Optional[ComboResponse]:
        combo = self.repository.get_by_id(db, combo_id)
        if not combo:
            return None
        return ComboResponse.model_validate(combo)
    
    def get_combos(self, skip: int = 0, limit: int = 100, available_only: bool = True) -> List[ComboResponse]:
        combos = self.repository.get_all(db, skip, limit, available_only)
        return [ComboResponse.model_validate(combo) for combo in combos]
    
    def update_combo(self, combo_id: int, update_data: ComboUpdate) -> Optional[ComboResponse]:
        update_dict = update_data.model_dump(exclude_unset=True)
        if not update_dict:
            return None
        
        combo = self.repository.update(db, combo_id, update_dict)
        if not combo:
            return None
        return ComboResponse.model_validate(combo)
    
    def delete_combo(self, combo_id: int) -> bool:
        return self.repository.delete(db, combo_id)