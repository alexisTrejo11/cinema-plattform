from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.application.repositories.wallet_repository import WalletRepository
from app.domain.models import Wallet
from app.infrastructure.persistence.sqlalchemy_models import WalletModel


class SQLAlchemyWalletRepository(WalletRepository):
    """SQLAlchemy async implementation of the wallet repository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, wallet_id: UUID) -> Wallet | None:
        result = await self.session.execute(
            select(WalletModel).where(WalletModel.id == wallet_id)
        )
        wallet_model = result.scalars().first()
        return Wallet.model_validate(wallet_model) if wallet_model else None

    async def get_by_user_id(self, user_id: UUID) -> list[Wallet]:
        result = await self.session.execute(
            select(WalletModel).where(WalletModel.user_id == user_id)
        )
        wallet_models = result.scalars().all()
        return [Wallet.model_validate(wallet) for wallet in wallet_models]

    async def create(self, wallet: Wallet) -> Wallet:
        wallet_model = WalletModel(**wallet.model_dump())
        self.session.add(wallet_model)
        await self.session.commit()
        await self.session.refresh(wallet_model)
        return Wallet.model_validate(wallet_model)

    async def update(self, wallet: Wallet) -> Wallet:
        result = await self.session.execute(
            select(WalletModel).where(WalletModel.id == wallet.id)
        )
        wallet_model = result.scalars().first()

        if wallet_model:
            for field, value in wallet.model_dump().items():
                setattr(wallet_model, field, value)
            await self.session.commit()
            await self.session.refresh(wallet_model)

        return Wallet.model_validate(wallet_model)

    async def delete(self, wallet_id: UUID) -> bool:
        result = await self.session.execute(
            select(WalletModel).where(WalletModel.id == wallet_id)
        )
        wallet_model = result.scalars().first()

        if wallet_model:
            await self.session.delete(wallet_model)
            await self.session.commit()
            return True
        return False
