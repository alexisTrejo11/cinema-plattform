from fastapi import Depends
from app.application.usecases.pay_ticket.use_case import DigitalTicketPayUseCase




def get_buy_tickets_uc() -> DigitalTicketPayUseCase:
    return DigitalTicketPayUseCase()