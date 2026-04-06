import logging
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import exists

from app.wallet.domain.interfaces import WalletRepository
from app.wallet.domain.entities.wallet import Wallet
from app.wallet.domain.value_objects import WalletId, UserId
from .sqlalchemy_models import WalletSQLModel

logger = logging.getLogger("app")


class SqlAlchemyWalletRepository(WalletRepository):
    """SQLAlchemy async implementation of the wallet repository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_by_id(
        self,
        wallet_id: WalletId,
        include_deleted: bool = False,
    ) -> Optional[Wallet]:
        query = select(WalletSQLModel).where(
            WalletSQLModel.id == wallet_id.value,
            WalletSQLModel.deleted_at is None if not include_deleted else True,
        )

        result = await self.session.execute(query)
        wallet_model = result.scalars().first()

        return wallet_model.to_domain() if wallet_model else None

    async def find_by_user_id(
        self,
        user_id: UserId,
        include_deleted: bool = False,
    ) -> Optional[Wallet]:

        logger.info(f"Finding wallet for user {user_id.value}")
        query = select(WalletSQLModel).where(
            WalletSQLModel.user_id == user_id.value,
            WalletSQLModel.deleted_at is None if include_deleted else True,
        )

        result = await self.session.execute(query)
        wallet_model = result.scalars().one_or_none()

        return wallet_model.to_domain() if wallet_model else None

    async def create(self, wallet: Wallet) -> Wallet:
        wallet_model = WalletSQLModel.from_domain(wallet)

        self.session.add(wallet_model)
        await self.session.commit()
        await self.session.refresh(wallet_model)

        return wallet_model.to_domain()

    async def update(self, wallet: Wallet) -> Wallet:
        result = await self.session.execute(
            select(WalletSQLModel).where(WalletSQLModel.id == wallet.id.value)
        )
        wallet_model = result.scalars().first()
        if not wallet_model:
            raise ValueError("Wallet not found for update")

        wallet_model.balance_amount = wallet.balance.amount
        wallet_model.balance_currency = wallet.balance.currency

        await self.session.commit()
        await self.session.refresh(wallet_model)

        return wallet_model.to_domain()

    async def delete(self, wallet_id: WalletId) -> bool:
        result = await self.session.execute(
            select(WalletSQLModel).where(WalletSQLModel.id == wallet_id.value)
        )
        wallet_model = result.scalars().first()

        if wallet_model:
            await self.session.delete(wallet_model)
            await self.session.commit()
            return True
        return False

    async def exists_by_user_id(self, user_id: UserId) -> bool:
        query = select(exists().where(WalletSQLModel.user_id == user_id.value))
        result = await self.session.execute(query)
        return result.scalar() or False
