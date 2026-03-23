from typing import Iterable, Optional

import grpc

from app.grpc.generated import concession_pb2, concession_pb2_grpc


class ConcessionCatalogGrpcClient:
    """Async gRPC client for cross-service catalog queries."""

    def __init__(self, target: str) -> None:
        self._target = target
        self._channel: Optional[grpc.aio.Channel] = None
        self._stub: Optional[concession_pb2_grpc.ConcessionCatalogServiceStub] = None

    async def connect(self) -> None:
        if self._channel is None:
            self._channel = grpc.aio.insecure_channel(self._target)
            self._stub = concession_pb2_grpc.ConcessionCatalogServiceStub(self._channel)

    async def close(self) -> None:
        if self._channel is not None:
            await self._channel.close()
            self._channel = None
            self._stub = None

    async def get_product_by_id(self, entity_id: str):
        return await self._get_stub().GetProductById(
            concession_pb2.EntityByIdRequest(id=entity_id)
        )

    async def get_products_by_ids(self, entity_ids: Iterable[str]):
        return await self._get_stub().GetProductsByIds(
            concession_pb2.EntityByIdsRequest(ids=list(entity_ids))
        )

    async def get_combo_by_id(self, entity_id: str):
        return await self._get_stub().GetComboById(
            concession_pb2.EntityByIdRequest(id=entity_id)
        )

    async def get_combos_by_ids(self, entity_ids: Iterable[str]):
        return await self._get_stub().GetCombosByIds(
            concession_pb2.EntityByIdsRequest(ids=list(entity_ids))
        )

    async def get_promotion_by_id(self, entity_id: str):
        return await self._get_stub().GetPromotionById(
            concession_pb2.EntityByIdRequest(id=entity_id)
        )

    async def get_promotions_by_ids(self, entity_ids: Iterable[str]):
        return await self._get_stub().GetPromotionsByIds(
            concession_pb2.EntityByIdsRequest(ids=list(entity_ids))
        )

    async def _get_stub(self) -> concession_pb2_grpc.ConcessionCatalogServiceStub:
        if self._stub is None:
            await self.connect()
        if self._stub is None:
            raise RuntimeError("gRPC client stub is not initialized.")
        return self._stub

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()
