from app.wallet.application.queries import SearchTransactionQuery
from app.wallet.domain.interfaces import WalletTransactionRepository as TransactioRepository
from app.wallet.presentation.dtos.response import (
    WalletTransactionResponse as TransactionResponse,
)


class SearchTransactionUseCase:
    def __init__(self, repository: TransactioRepository) -> None:
        self.repository = repository

    # TODO: Return page metadata
    async def execute(self, query: SearchTransactionQuery):
        transactions = await self.repository.search(query)

        return [TransactionResponse.from_domain(t) for t in transactions]
