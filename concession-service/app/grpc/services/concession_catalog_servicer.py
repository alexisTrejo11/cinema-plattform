import json
from typing import Iterable

import grpc
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.combos.domain.entities.value_objects import ComboId
from app.combos.infrastructure.persistence.sqlalchemy_combo_repo import (
    SQLAlchemyComboRepository,
)
from app.grpc.generated import concession_pb2, concession_pb2_grpc
from app.products.domain.entities.value_objects import ProductId
from app.products.infrastructure.persistence.repositories.sqlalchemy_product_repo import (
    SQLAlchemyProductRepository,
)
from app.promotions.domain.entities.value_objects import PromotionId
from app.promotions.infrastructure.persistence.repository.sql_alchemy_promotion_repository import (
    SQLAlchemyPromotionRepository,
)


class ConcessionCatalogGrpcServicer(
    concession_pb2_grpc.ConcessionCatalogServiceServicer
):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

    async def GetProductById(self, request, context):
        product_id = await self._parse_id(
            raw_id=request.id,
            parser=ProductId.from_string,
            entity_name="product",
            context=context,
        )
        async with self._session_factory() as session:
            repo = SQLAlchemyProductRepository(session)
            product = await repo.find_by_id(product_id)
            if product is None:
                product = await repo.find_deleted_by_id(product_id)
            return self._build_product_reply(product)

    async def GetProductsByIds(self, request, context):
        ids = await self._parse_ids(
            raw_ids=request.ids,
            parser=ProductId.from_string,
            entity_name="product",
            context=context,
        )
        if not ids:
            return concession_pb2.ProductListReply(items=[])

        async with self._session_factory() as session:
            repo = SQLAlchemyProductRepository(session)
            active_products = await repo.find_by_id_in(ids)
            items = []
            for product_id in ids:
                product = active_products.get(product_id)
                if product is None:
                    product = await repo.find_deleted_by_id(product_id)
                items.append(self._build_product_reply(product))
            return concession_pb2.ProductListReply(items=items)

    async def GetComboById(self, request, context):
        combo_id = await self._parse_id(
            raw_id=request.id,
            parser=ComboId.from_string,
            entity_name="combo",
            context=context,
        )
        async with self._session_factory() as session:
            repo = SQLAlchemyComboRepository(session)
            combo = await repo.find_by_id(combo_id, include_items=True)
            if combo is None:
                combo = await repo.find_deleted_by_id(combo_id)
            return self._build_combo_reply(combo)

    async def GetCombosByIds(self, request, context):
        ids = await self._parse_ids(
            raw_ids=request.ids,
            parser=ComboId.from_string,
            entity_name="combo",
            context=context,
        )
        if not ids:
            return concession_pb2.ComboListReply(items=[])

        async with self._session_factory() as session:
            repo = SQLAlchemyComboRepository(session)
            items = []
            for combo_id in ids:
                combo = await repo.find_by_id(combo_id, include_items=True)
                if combo is None:
                    combo = await repo.find_deleted_by_id(combo_id)
                items.append(self._build_combo_reply(combo))
            return concession_pb2.ComboListReply(items=items)

    async def GetPromotionById(self, request, context):
        promotion_id = await self._parse_id(
            raw_id=request.id,
            parser=PromotionId.from_string,
            entity_name="promotion",
            context=context,
        )
        async with self._session_factory() as session:
            repo = SQLAlchemyPromotionRepository(session)
            promotion = await repo.get_by_id(promotion_id, is_active=True)
            if promotion is None:
                promotion = await repo.get_by_id(promotion_id, is_active=False)
            return self._build_promotion_reply(promotion)

    async def GetPromotionsByIds(self, request, context):
        ids = await self._parse_ids(
            raw_ids=request.ids,
            parser=PromotionId.from_string,
            entity_name="promotion",
            context=context,
        )
        if not ids:
            return concession_pb2.PromotionListReply(items=[])

        async with self._session_factory() as session:
            repo = SQLAlchemyPromotionRepository(session)
            items = []
            for promotion_id in ids:
                promotion = await repo.get_by_id(promotion_id, is_active=True)
                if promotion is None:
                    promotion = await repo.get_by_id(promotion_id, is_active=False)
                items.append(self._build_promotion_reply(promotion))
            return concession_pb2.PromotionListReply(items=items)

    @staticmethod
    def _build_product_reply(product):
        if product is None:
            return concession_pb2.ProductReply(exists=False)

        return concession_pb2.ProductReply(
            exists=True,
            data=concession_pb2.ProductData(
                id=product.id.to_string(),
                category_id=product.category_id,
                description=product.description or "",
                image_url=product.image_url or "",
                is_available=product.is_available,
                preparation_time_mins=(
                    "" if product.preparation_time_mins is None else str(product.preparation_time_mins)
                ),
                calories="" if product.calories is None else str(product.calories),
                created_at=product.created_at.isoformat(),
                updated_at=product.updated_at.isoformat(),
                deleted_at="" if product.deleted_at is None else product.deleted_at.isoformat(),
                name=product.name,
                price=float(product.price),
            ),
        )

    @staticmethod
    def _build_combo_reply(combo):
        if combo is None:
            return concession_pb2.ComboReply(exists=False)

        return concession_pb2.ComboReply(
            exists=True,
            data=concession_pb2.ComboData(
                id=combo.id.to_string(),
                name=combo.name,
                price=float(combo.price),
                is_available=combo.is_available,
                description=combo.description or "",
                discount_percentage=float(combo.discount_percentage),
                image_url=combo.image_url or "",
                created_at=combo.created_at.isoformat(),
                updated_at=combo.updated_at.isoformat(),
                deleted_at="" if combo.deleted_at is None else combo.deleted_at.isoformat(),
                items=[
                    concession_pb2.ComboItemData(
                        id=item.id.to_string(),
                        product_id=item.product.id.to_string(),
                        product_name=item.product.name,
                        product_price=float(item.product.price),
                        product_is_available=item.product.is_available,
                        quantity=item.quantity,
                    )
                    for item in combo.items
                ],
            ),
        )

    @staticmethod
    def _build_promotion_reply(promotion):
        if promotion is None:
            return concession_pb2.PromotionReply(exists=False)

        return concession_pb2.PromotionReply(
            exists=True,
            data=concession_pb2.PromotionData(
                id=promotion.id.to_string(),
                name=promotion.name,
                description=promotion.description or "",
                is_active=promotion.is_active,
                promotion_type=promotion.promotion_type.value,
                rule_json=json.dumps(promotion.rule or {}, default=str),
                start_date=promotion.start_date.isoformat(),
                end_date=promotion.end_date.isoformat(),
                created_at=promotion.created_at.isoformat(),
                updated_at=promotion.updated_at.isoformat(),
                max_uses="" if promotion.max_uses is None else str(promotion.max_uses),
                current_uses=promotion.current_uses,
                applicable_product_ids=[
                    product_id.to_string() for product_id in promotion.applicable_product_ids
                ],
                applicable_categories_ids=promotion.applicable_categories_ids,
            ),
        )

    @staticmethod
    async def _abort_invalid_id(context, entity_name: str, raw_id: str):
        await context.abort(
            grpc.StatusCode.INVALID_ARGUMENT,
            f"Invalid {entity_name} id '{raw_id}'. Expected UUID string.",
        )

    async def _parse_id(self, raw_id: str, parser, entity_name: str, context):
        try:
            return parser(raw_id)
        except Exception:
            await self._abort_invalid_id(context, entity_name, raw_id)

    async def _parse_ids(self, raw_ids: Iterable[str], parser, entity_name: str, context):
        parsed_ids = []
        for raw_id in raw_ids:
            parsed_ids.append(await self._parse_id(raw_id, parser, entity_name, context))
        return parsed_ids
