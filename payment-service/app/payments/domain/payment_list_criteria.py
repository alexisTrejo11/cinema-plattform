"""Criteria for listing/filtering payments (repository + application boundary)."""

from pydantic import BaseModel, ConfigDict


class PaymentListCriteria(BaseModel):
    """Filters and pagination for payment queries; extend as new filters are needed."""

    model_config = ConfigDict(frozen=True)

    user_id: str | None = None
    status: str | None = None
    limit: int = 50
    offset: int = 0

    @classmethod
    def paginate(cls, *, limit: int = 50, offset: int = 0) -> "PaymentListCriteria":
        """List without user/status filters (common for summaries)."""
        return cls(limit=limit, offset=offset)
