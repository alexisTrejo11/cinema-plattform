from typing import Optional, List
from uuid import UUID
from app.user.domain.value_objects import UserId
from app.wallet.domain.entities import Wallet
from ..repositories.wallet_repository import WalletRepository
from ..dtos.wallet_dtos import (
    AddCreditCommand,
    PayResponse,
    CreateWalletCommand,
    WalletResponse,
)


class GetWalletByIdUseCase:
    """Use case for retrieving a wallet by its ID."""

    def __init__(self, wallet_repo: WalletRepository):
        self.wallet_repo = wallet_repo

    async def execute(self, wallet_id: UUID) -> Optional[WalletResponse]:
        """Retrieves a wallet by its ID."""
        wallet = await self.wallet_repo.get_by_id(wallet_id)
        return WalletResponse.model_validate(wallet) if wallet else None


class GetWalletsByUserIdUseCase:
    """Use case for retrieving all wallets for a given user."""

    def __init__(self, wallet_repo: WalletRepository):
        self.wallet_repo = wallet_repo

    async def execute(self, user_id: UUID) -> List[WalletResponse]:
        """Retrieves all wallets for a given user."""
        wallets = await self.wallet_repo.get_by_user_id(user_id)
        return [WalletResponse.model_validate(wallet) for wallet in wallets]


class CreateWalletUseCase:
    def __init__(self, wallet_repo: WalletRepository):
        self.wallet_repo = wallet_repo

    async def execute(self, command: CreateWalletCommand) -> WalletResponse:
        """Creates a new wallet for a user."""
        user_id = UserId(command.user_id.value)
        new_wallet = Wallet.create(user_id)

        created_wallet = await self.wallet_repo.create(new_wallet)
        return WalletResponse.model_validate(created_wallet)


class AddCreditUseCase:
    """Use case for adding credit to a wallet."""

    def __init__(self, wallet_repo: WalletRepository):
        self.wallet_repo = wallet_repo

    async def execute(self, add_credit_dto: AddCreditCommand) -> WalletResponse:
        """Adds credit to a wallet."""
        wallet = await self.wallet_repo.get_by_id(add_credit_dto.wallet_id)
        if not wallet:
            raise ValueError("Wallet not found")

        wallet.balance += add_credit_dto.amount
        updated_wallet = await self.wallet_repo.update(wallet)

        return WalletResponse.model_validate(updated_wallet)


class PayUseCase:
    """Use case for making a payment from a wallet."""

    def __init__(self, wallet_repo: WalletRepository):
        self.wallet_repo = wallet_repo

    async def execute(self, pay_dto: PayResponse) -> WalletResponse:
        """Makes a payment from a wallet."""
        wallet = await self.wallet_repo.get_by_id(pay_dto.wallet_id)
        if not wallet:
            raise ValueError("Wallet not found")

        if wallet.balance < pay_dto.amount:
            raise ValueError("Insufficient funds")

        wallet.balance -= pay_dto.amount
        updated_wallet = await self.wallet_repo.update(wallet)

        return WalletResponse.model_validate(updated_wallet)


class WalletUseCases:
    """Container for all wallet use cases - useful for dependency injection."""

    def __init__(self, wallet_repo: WalletRepository):
        self._add_credit = AddCreditUseCase(wallet_repo)
        self._pay = PayUseCase(wallet_repo)
        self._create_wallet = CreateWalletUseCase(wallet_repo)
        self._get_wallet_by_id = GetWalletByIdUseCase(wallet_repo)
        self._get_wallets_by_user_id = GetWalletsByUserIdUseCase(wallet_repo)

    async def create_wallet(self, command: CreateWalletCommand) -> WalletResponse:
        return await self._create_wallet.execute(command)

    async def get_wallet_by_id(self, wallet_id: UUID) -> Optional[WalletResponse]:
        return await self._get_wallet_by_id.execute(wallet_id)

    async def get_wallets_by_user_id(self, user_id: UUID) -> List[WalletResponse]:
        return await self._get_wallets_by_user_id.execute(user_id)

    async def add_credit(self, add_credit_dto: AddCreditCommand) -> WalletResponse:
        return await self._add_credit.execute(add_credit_dto)

    async def pay(self, pay_dto: PayResponse) -> WalletResponse:
        return await self._pay.execute(pay_dto)
