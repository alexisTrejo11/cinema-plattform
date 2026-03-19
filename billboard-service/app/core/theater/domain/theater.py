from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, ClassVar
from pydantic import PositiveInt
from .exceptions import InvalidCapacityError, TheaterMaintenanceError
from .enums import TheaterType

class Theater(BaseModel):
    """
    Represents a Theater entity within a Cinema.
    """
    id: Optional[int] = None
    cinema_id: int
    name: str = Field(..., max_length=50)
    capacity: PositiveInt
    theater_type: TheaterType
    is_active: bool = True
    maintenance_mode: bool = False

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    CAPACITY_RULES: ClassVar = {
        TheaterType.IMAX: {"min": 150, "max": 300},
        TheaterType.TWO_D: {"min": 50, "max": 200},
        TheaterType.THREE_D: {"min": 100, "max": 200},
        TheaterType.FOUR_DX: {"min": 20, "max": 100},
        TheaterType.VIP: {"min": 10, "max": 50}
    }

    def validate_buissness_rules(self):
        self.validate_capacity()

    def validate_capacity(self):
        theater_type = self.theater_type
        capacity = self.capacity

        rules = self.CAPACITY_RULES.get(theater_type, {})
        if not rules:
            return
            
        if not (rules['min'] <= capacity <= rules['max']):
            raise InvalidCapacityError(
                f"Capacity {capacity} is invalid for {theater_type}. "
                f"Allowed range: {rules['min']}-{rules['max']}"
            )

    def update(self, new_data: "Theater"):
        """Update theater properties"""
        self.name = new_data.name
        self.capacity = new_data.capacity
        self.theater_type = new_data.theater_type
        self.maintenance_mode = new_data.maintenance_mode
        
        if new_data.is_active:
            self.activate()

    def activate(self):
        """Activate the theater if not in maintenance"""
        if self.maintenance_mode:
            raise TheaterMaintenanceError(
                "Cannot activate theater while in maintenance mode"
            )
        self.is_active = True

    def deactivate(self):
        """Deactivate the theater"""
        self.is_active = False

    def enter_maintenance(self):
        """Put theater in maintenance mode (automatically deactivates)"""
        self.maintenance_mode = True
        self.deactivate()

    def exit_maintenance(self):
        """Take theater out of maintenance mode"""
        self.maintenance_mode = False