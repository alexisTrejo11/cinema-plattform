from app.promotions.application.command.promotion_command import (
    PromotionCreateCommand,
    ExtendPromotionCommand,
)
from app.promotions.infrastructure.api.controller.dto.request import (
    PromotionCreateRequest,
    ExtendPromotionRequest,
)
from app.promotions.domain.valueobjects import ProductId, PromotionId
from app.shared.schema import PydanticUUID


class RequestMapper:
    @staticmethod
    def create_request_to_command(
        request: PromotionCreateRequest,
    ) -> PromotionCreateCommand:
        return PromotionCreateCommand(
            name=request.name,
            description=request.description,
            start_date=request.start_date,
            promotion_type=request.promotion_type,
            rule=request.rule,
            is_active=request.is_active,
            max_uses=request.max_uses,
            end_date=request.end_date,
            applicable_product_ids=(
                [ProductId(pid) for pid in request.applicable_product_ids]
                if request.applicable_product_ids
                else []
            ),
            applicable_category_id=(
                request.applicable_category_id
                if request.applicable_category_id
                else None
            ),
        )

    @staticmethod
    def extend_request_to_command(
        request: ExtendPromotionRequest,
    ) -> ExtendPromotionCommand:
        return ExtendPromotionCommand(
            id=PydanticUUID(id=request.id),
            available_until=request.available_until,
        )
