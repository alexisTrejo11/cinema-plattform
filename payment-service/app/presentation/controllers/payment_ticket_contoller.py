from fastapi import APIRouter, Depends
from ..depencies import get_buy_tickets_uc
from ..depencies import DigitalTicketPayUseCase
from app.application.dto.request import PayTicketRequest

router = APIRouter(prefix="/api/v2/payments/tickets")

@router.post("/")
async def purchase(
    buy_ticket_request: PayTicketRequest,
    use_case: DigitalTicketPayUseCase = Depends(get_buy_tickets_uc),
):
    response = await use_case.execute(buy_ticket_request)
    return response

@router.post("/{payment_id}")
def details(use_case):
    use_case.execute()


@router.post("/{payment_id}/refund")
def refund(use_case):
    use_case.execute()


