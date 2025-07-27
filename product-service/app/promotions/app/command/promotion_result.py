from dataclasses import dataclass
from app.shared.response import ErrorResponse


@dataclass
class PromotionCommandResult:
    promotion_id: str
    is_success: bool
    message: str = "Promotion successfully processed"

    @classmethod
    def error(
        cls, promotion_id: str = "", message: str = "error"
    ) -> "PromotionCommandResult":
        """Returns a new instance with an error message."""
        return cls(promotion_id=promotion_id, is_success=False, message=message)

    @classmethod
    def success(
        cls, promotion_id: str = "", message: str = "success"
    ) -> "PromotionCommandResult":
        """Returns a new instance with a success message."""
        return cls(promotion_id=promotion_id, is_success=True, message=message)

    @classmethod
    def error_details(cls, message: str = "error") -> "ErrorResponse":
        return ErrorResponse(
            code="PROMOTION_CREATION_ERROR",
            type="PromotionError",
            message=cls.message,
            details={},
        )
