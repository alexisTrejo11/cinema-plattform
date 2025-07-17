from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.wallet.domain.repositories.wallet_repository import WalletRepository
from app.wallet.domain.entities.wallet import Wallet, WalletId
from .sqlalchemy_models import WalletSQLModel
from app.wallet.application.exceptions import WalletNotFoundError
from app.user.domain.value_objects import UserId


class SqlAlchemyWalletRepository(WalletRepository):
    """SQLAlchemy async implementation of the wallet repository."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(
        self,
        wallet_id: WalletId,
        raise_exception: bool = False,
    ) -> Wallet:
        query = select(WalletSQLModel).where(WalletSQLModel.id == wallet_id.value)

        result = await self.session.execute(query)
        wallet_model = result.unique().scalars().one_or_none()

        if not wallet_model and raise_exception:
            raise WalletNotFoundError(wallet_id.to_string())

        return WalletSQLModel.to_domain_wallet(wallet_model) if wallet_model else None

    async def get_by_user_id(
        self,
        user_id: UserId,
        raise_exception: bool = False,
    ) -> Wallet:
        query = select(WalletSQLModel).where(WalletSQLModel.user_id == user_id.value)

        result = await self.session.execute(query)
        wallet_model = result.unique().scalars().one_or_none()

        if not wallet_model and raise_exception:
            raise WalletNotFoundError(user_id.to_string())

        return WalletSQLModel.to_domain_wallet(wallet_model) if wallet_model else None

    async def create(self, wallet: Wallet) -> Wallet:
        wallet_model = WalletSQLModel.from_domain(wallet)

        self.session.add(wallet_model)
        await self.session.commit()
        await self.session.refresh(wallet_model)

        return WalletSQLModel.to_domain_wallet(wallet_model)

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

        return WalletSQLModel.to_domain_wallet(wallet_model)

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
