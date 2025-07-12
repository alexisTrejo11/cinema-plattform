from uuid import UUID
from app.application.repositories.wallet_repository import WalletRepository
from app.application.dtos.wallet_dtos import (
    AddCreditResponse,
    PayResponse,
    CreateWalletResponse,
    WalletResponse,
)
from app.domain.models import Wallet
from app.application.mappers.wallet_mapper import wallet_to_dto


class WalletUseCases:
    """Provides use cases for wallet operations."""

    def __init__(self, wallet_repo: WalletRepository):
        self.wallet_repo = wallet_repo

    async def create_wallet(
        self, create_wallet_dto: CreateWalletResponse
    ) -> WalletResponse:
        """Creates a new wallet for a user."""
        new_wallet = Wallet(user_id=create_wallet_dto.user_id, balance=0.00)
        created_wallet = await self.wallet_repo.create(new_wallet)
        return wallet_to_dto(created_wallet)

    async def add_credit(self, add_credit_dto: AddCreditResponse) -> WalletResponse:
        """Adds credit to a wallet."""
        wallet = await self.wallet_repo.get_by_id(add_credit_dto.wallet_id)
        if not wallet:
            raise ValueError("Wallet not found")

        wallet.balance += add_credit_dto.amount
        updated_wallet = await self.wallet_repo.update(wallet)

        return wallet_to_dto(updated_wallet)

    async def pay(self, pay_dto: PayResponse) -> WalletResponse:
        """Makes a payment from a wallet."""
        wallet = await self.wallet_repo.get_by_id(pay_dto.wallet_id)
        if not wallet:
            raise ValueError("Wallet not found")

        if wallet.balance < pay_dto.amount:
            raise ValueError("Insufficient funds")

        wallet.balance -= pay_dto.amount
        updated_wallet = await self.wallet_repo.update(wallet)

        return wallet_to_dto(updated_wallet)

    async def get_wallet_by_id(self, wallet_id: UUID) -> WalletResponse | None:
        """Retrieves a wallet by its ID."""
        wallet = await self.wallet_repo.get_by_id(wallet_id)
        return wallet_to_dto(wallet) if wallet else None

    async def get_wallets_by_user_id(self, user_id: UUID) -> list[WalletResponse]:
        """Retrieves all wallets for a given user."""
        wallets = await self.wallet_repo.get_by_user_id(user_id)
        return [wallet_to_dto(wallet) for wallet in wallets]
