from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.wallet.domain.repositories.wallet_repository import WalletRepository
from app.wallet.domain.entities.wallet import Wallet
from .sqlalchemy_models import WalletSQLModel
from sqlalchemy.orm import joinedload


# TODO: Transaction
class SqlAlchemyWalletRepository(WalletRepository):
    """SQLAlchemy async implementation of the wallet repository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(
        self, wallet_id: UUID, include_transactions: bool = True
    ) -> Optional[Wallet]:
        query = select(WalletSQLModel).where(WalletSQLModel.id == wallet_id)

        if include_transactions:
            query = query.options(joinedload(WalletSQLModel.transactions))

        result = await self.session.execute(query)
        wallet_model = result.scalars().first()

        return WalletSQLModel.to_domain_wallet(wallet_model) if wallet_model else None

    async def get_by_user_id(
        self, user_id: UUID, include_transactions: bool = True
    ) -> Wallet:
        query = select(WalletSQLModel).where(WalletSQLModel.user_id == user_id)

        if include_transactions:
            # Usamos joinedload para realizar un LEFT JOIN explícito
            query = query.options(joinedload(WalletSQLModel.transactions))

        result = await self.session.execute(query)
        wallet_model = result.scalars().one()

        return WalletSQLModel.to_domain_wallet(wallet_model)

    async def create(self, wallet: Wallet) -> Wallet:
        wallet_model = WalletSQLModel.from_domain(wallet)

        self.session.add(wallet_model)
        await self.session.commit()
        await self.session.refresh(wallet_model)

        return WalletSQLModel.to_domain_wallet(wallet_model)

    # FIX
    async def update(self, wallet: Wallet) -> Wallet:
        result = await self.session.execute(
            select(WalletSQLModel).where(WalletSQLModel.id == wallet.id)
        )
        wallet_model = result.scalars().first()

        if not wallet_model:
            raise ValueError("not found")
        for field, value in wallet.__dict__.items():
            setattr(wallet_model, field, value)

        await self.session.commit()
        await self.session.refresh(wallet_model)

        return WalletSQLModel.to_domain_wallet(wallet_model)

    async def delete(self, wallet_id: UUID) -> bool:
        result = await self.session.execute(
            select(WalletSQLModel).where(WalletSQLModel.id == wallet_id)
        )
        wallet_model = result.scalars().first()

        if wallet_model:
            await self.session.delete(wallet_model)
            await self.session.commit()
            return True
        return False
