from typing import Any
from app.shared.base_exceptions import NotFoundException, ValidationException


class TheaterNotFound(NotFoundException):
    def __init__(self, entity: str, entity_id: Any):
        super().__init__(entity, entity_id)
        

class SeatNotFoundError(NotFoundException):
    def __init__(self, entity: str, entity_id: Any):
        super().__init__(entity, entity_id)
                
        
class SeatInvalidIdListError(ValidationException):
    def __init__(self, field: str, reason: str):
        super().__init__(field, reason)