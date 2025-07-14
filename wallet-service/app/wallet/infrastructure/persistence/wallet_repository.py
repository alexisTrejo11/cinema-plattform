from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.wallet.domain.repositories.wallet_repository import WalletRepository
from app.wallet.domain.entities.wallet import Wallet
from .sqlalchemy_models import WalletSQLModel


# TODO: Transaction
class SQLAlchemyWalletRepository(WalletRepository):
    """SQLAlchemy async implementation of the wallet repository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, wallet_id: UUID) -> Wallet | None:
        result = await self.session.execute(
            select(WalletSQLModel).where(WalletSQLModel.id == wallet_id)
        )
        wallet_model = result.scalars().first()
        return WalletSQLModel.to_domain_wallet(wallet_model) if wallet_model else None

    async def get_by_user_id(self, user_id: UUID) -> list[Wallet]:
        result = await self.session.execute(
            select(WalletSQLModel).where(WalletSQLModel.user_id == user_id)
        )
        wallet_models = result.scalars().all()
        return [WalletSQLModel.to_domain_wallet(wallet) for wallet in wallet_models]

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
