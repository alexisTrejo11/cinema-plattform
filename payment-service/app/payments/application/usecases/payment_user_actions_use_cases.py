from ..commands.credit.command import AddCreditCommand
from ..commands.credit.result import AddCreditResult
from ..commands.credit.handler import AddCreditCommandHandler
from ..commands.procces_pay.procces_pay import ProcessPayCommand


class AddCreditToWalletUseCase:
    def __init__(self, add_credit_handler: AddCreditCommandHandler) -> None:
        self.add_credit_handler = add_credit_handler

    async def execute(self, credit_command: AddCreditCommand) -> AddCreditResult:
        result = await self.add_credit_handler.handle(credit_command)
        return result


class BuyProductUseCase:
    async def execute(self, command: ProcessPayCommand) -> None:
        pass


class BuyTicketUseCase:
    def __init__(
        self,
        payment_repository: PaymentRepository,
        wallet_repository: WalletRepository,
        event_publisher: EventPublisher,
        payment_gateway: PaymentGateway,
        notification_service: NotificationService,
    ):
        self.payment_repository = payment_repository
        self.wallet_repository = wallet_repository
        self.event_publisher = event_publisher
        self.payment_gateway = payment_gateway
        self.notification_service = notification_service

        self.payment_handler = ProcessPaymentCommandHandler(
            payment_repository=payment_repository,
            wallet_repository=wallet_repository,
            event_publisher=event_publisher,
            payment_gateway=payment_gateway,
            notification_service=notification_service,
        )

    async def execute(self, request: PayTicketRequest) -> PayTicketResponse:
        """
        Execute the ticket payment workflow.

        Args:
            request: Ticket payment request

        Returns:
            Ticket payment response
        """
        validation_result = await self._validate_ticket_payment(request)
        if not validation_result.is_valid:
            return PayTicketResponse(
                success=False,
                message=validation_result.error_message,
                error_code="VALIDATION_FAILED",
            )

        payment_command = ProcessPayCommand(
            product_id=UUID(int=0),
            user_id=request.user_id,
            amount=request.amount,
            payment_method=request.payment_method,
            payment_type="ticket_purchase",
            wallet_id=request.wallet_id,
            correlation_id=None,
            currency=request.currency,
            metadata=None,
        )

        payment_result = await self.payment_handler.handle(payment_command)

        if payment_result.status != "completed":
            return PayTicketResponse(
                success=False,
                message=payment_result.message,
                error_code="PAYMENT_FAILED",
            )

        await self._handle_post_payment_actions(request, payment_result)

        return PayTicketResponse(
            success=True,
            payment_id=payment_result.payment_id,
            amount_paid=request.amount,
            transaction_reference=payment_result.transaction_reference,
            confirmation_code=None,
            message="Ticket payment processed successfully",
        )

    async def _validate_ticket_payment(
        self, request: PayTicketRequest
    ) -> "ValidationResult":
        if request.amount <= 0:
            return ValidationResult(False, "Invalid payment amount")

        if request.payment_method == "wallet":
            user_id = UserId.from_string(str(request.user_id))
            wallet = await self.wallet_repository.get_by_user_id(user_id)
            if wallet:
                required_amount = Money.from_float(
                    request.amount, Currency(request.currency)
                )
                if not wallet.can_debit(required_amount):
                    return ValidationResult(False, "Insufficient wallet balance")
            else:
                return ValidationResult(False, "User wallet not found")

        return ValidationResult(True, "Validation passed")

    async def _handle_post_payment_actions(
        self, request: PayTicketRequest, payment_result: ProcessPaymentResult
    ) -> None:
        # 1. Send Succes to ticket
        print(f"Post-payment actions for payment {payment_result.payment_id}")


class ValidationResult:
    def __init__(self, is_valid: bool, error_message: str = ""):
        self.is_valid = is_valid
        self.error_message = error_message
