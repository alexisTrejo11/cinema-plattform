from abc import ABC, abstractmethod
from typing import List, Optional
from app.combos.domain.combo import Combo

class ComboRepository(ABC): 
    @abstractmethod
    def get_by_id(self, combo_id: int, include_items=True) -> Optional[Combo]:
        pass
    
    
    @abstractmethod
    def list_by_product(self, product_id: int, include_items=True) -> List[Combo]:
        pass
    
    
    @abstractmethod
    def list_all(self, active_only=True) -> List[Combo]:
        pass
    
    
    @abstractmethod
    def save(self, combo: Combo) -> Combo:
        pass
    
    
    @abstractmethod
    def soft_delete(self, combo_id: int) -> None:
        pass