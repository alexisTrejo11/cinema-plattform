from typing import Optional
from pydantic import BaseModel
from app.promotions.domain.entities.value_objects import PromotionId


class PromotionCommandResult(BaseModel):
    """Result of a promotion command operation."""

    promotion_id: str = ""
    is_success: bool
    message: str = "Promotion successfully processed"

    @classmethod
    def error(
        cls, promotion_id: Optional[PromotionId] = None, message: str = "error"
    ) -> "PromotionCommandResult":
        return cls(
            promotion_id=promotion_id.to_string() if promotion_id else "",
            is_success=False,
            message=message,
        )

    @classmethod
    def success(
        cls, promotion_id: PromotionId, message: str = "success"
    ) -> "PromotionCommandResult":
        return cls(
            promotion_id=promotion_id.to_string(), is_success=True, message=message
        )
