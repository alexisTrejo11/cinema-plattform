from typing import Any
from app.shared.base_exceptions import NotFoundException, ValidationException
from http import HTTPStatus


class WalletNotFoundError(NotFoundException):
    def __init__(self, entity_id: Any):
        super().__init__("Wallet", entity_id)


class UserNotFoundError(NotFoundException):
    def __init__(self, entity_id: Any):
        super().__init__("User", entity_id)


class UserWalletConflict(ValidationException):
    def __init__(self, reason: str):
        super().__init__("User", reason)

    status_code = HTTPStatus.CONFLICT
