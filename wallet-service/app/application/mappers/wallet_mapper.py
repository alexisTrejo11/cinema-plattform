from app.domain.models import Wallet
from app.application.dtos.wallet_dtos import WalletResponse


def wallet_to_dto(wallet: Wallet) -> WalletResponse:
    """Maps a Wallet domain object to a WalletResponse."""
    return WalletResponse.model_validate(wallet)
