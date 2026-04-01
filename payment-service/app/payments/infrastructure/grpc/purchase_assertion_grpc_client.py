from __future__ import annotations

from typing import Any

from app.config.app_config import settings
from app.payments.domain.interfaces import PurchaseAssertionClient


class PurchaseAssertionGrpcClient(PurchaseAssertionClient):
    """
    Placeholder gRPC adapter for sync business assertions.

    Real gRPC calls are intentionally deferred until cross-service contracts
    are finalized; this adapter returns "allowed" so local flows continue.
    """

    def __init__(self, target: str | None = None) -> None:
        self.target = target or settings.GRPC_BILLBOARD_TARGET or settings.GRPC_PAYMENT_TARGET

    async def assert_ticket_purchase(
        self, user_id: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        return await self._allowed("ticket_purchase", user_id, payload)

    async def assert_concessions_purchase(
        self, user_id: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        return await self._allowed("concessions_purchase", user_id, payload)

    async def assert_merchandise_purchase(
        self, user_id: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        return await self._allowed("merchandise_purchase", user_id, payload)

    async def assert_subscription_purchase(
        self, user_id: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        return await self._allowed("subscription_purchase", user_id, payload)

    async def assert_wallet_credit(
        self, user_id: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        return await self._allowed("wallet_credit", user_id, payload)

    async def _allowed(
        self, operation: str, user_id: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        # This shape mirrors the proto response for smooth migration later.
        return {
            "allowed": True,
            "reason": "grpc_not_implemented_yet",
            "reference_id": "",
            "normalized_payload": payload,
            "operation": operation,
            "user_id": user_id,
            "target": self.target,
        }
