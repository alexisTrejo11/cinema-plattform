from typing import Optional
from pydantic import BaseModel
from app.promotions.domain.valueobjects import PromotionId
from app.shared.response import ErrorResponse


class PromotionCommandResult(BaseModel):
    """
    Represents the result of a promotion command operation,
    transformed into a Pydantic v2 BaseModel.
    """

    promotion_id: str = ""  # Default to empty string for consistency with class methods
    is_success: bool
    message: str = "Promotion successfully processed"

    @classmethod
    def error(
        cls, promotion_id: Optional[PromotionId] = None, message: str = "error"
    ) -> "PromotionCommandResult":
        """
        Returns a new instance with an error message.
        This is a class method to create an error result.
        """
        return cls(
            promotion_id=promotion_id.to_string() if promotion_id else "",
            is_success=False,
            message=message,
        )

    @classmethod
    def success(
        cls, promotion_id: PromotionId, message: str = "success"
    ) -> "PromotionCommandResult":
        """
        Returns a new instance with a success message.
        This is a class method to create a success result.
        """
        return cls(
            promotion_id=promotion_id.to_string(), is_success=True, message=message
        )

    def to_error_response(self) -> ErrorResponse:
        """
        Converts the command result to an ErrorResponse.
        This is useful for API responses.
        """
        return ErrorResponse(
            code="promotion_command_error",
            type="ApplicationError",
            message=self.message,
            details={"promotion_id": self.promotion_id},
        )
