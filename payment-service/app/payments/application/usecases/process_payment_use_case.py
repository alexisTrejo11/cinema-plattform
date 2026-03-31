class ProcessPaymentCommandHandler:
    """Handler for processing payment commands."""

    def __init__(
        self,
        payment_repository: PaymentRepository,
        wallet_repository: WalletRepository,
        event_publisher: EventPublisher,
        payment_gateway: PaymentGateway,
    ):
        self.payment_repository = payment_repository
        self.wallet_repository = wallet_repository
        self.event_publisher = event_publisher
        self.payment_gateway = payment_gateway

    async def handle(self, command: ProcessPayCommand) -> ProcessPaymentResult:
        """
        Handle payment processing command.

        Args:
            command: Payment processing command

        Returns:
            Payment processing result

        Raises:
            InvalidPaymentAmountException: If payment amount is invalid
            InsufficientFundsException: If wallet has insufficient funds
            PaymentAlreadyProcessedException: If payment is already processed
        """
        payment = None
        try:
            user_id = UserId.from_string(str(command.user_id))
            amount = Money.from_float(command.amount, Currency(command.currency))
            payment_method = PaymentMethod(command.payment_method)
            payment_type = PaymentType(command.payment_type)

            payment_metadata = None
            if command.metadata:
                payment_metadata = self._create_payment_metadata(command.metadata)

            payment = Payment.create(
                user_id, amount, payment_method, payment_type, payment_metadata
            )
            payment.start_processing()

            result = await self._handle_payment_method(payment_method, payment, command)

            saved_payment = await self.payment_repository.save(payment)

            await self._procces_event(payment, result)

            return ProcessPaymentResult(
                payment_id=saved_payment.id.value,
                status=saved_payment.status.value,
                message="Payment processed successfully",
                transaction_reference=result.get("transaction_id"),
            )
        except Exception as e:
            failure_result = await self._proccess_payment_failure(payment, str(e))
            return failure_result

    async def _process_wallet_payment(
        self, payment: Payment, wallet_id: Optional[UUID]
    ) -> Dict[str, Any]:
        """Process payment using wallet funds."""
        wallet = (
            await self._get_wallet_by_id(wallet_id)
            if wallet_id
            else await self._get_user_wallet(payment.user_id)
        )

        if not wallet.can_debit(payment.amount):
            raise InsufficientFundsException(
                wallet.get_available_balance().to_float(), payment.amount.to_float()
            )

        transaction_id = wallet.debit(
            payment.amount, f"Payment for {payment.payment_type.value}", str(payment.id)
        )

        await self.wallet_repository.save(wallet)
        payment.complete(transaction_reference=str(transaction_id))

        await self._publish_wallet_events(wallet)
        return {
            "transaction_id": str(transaction_id),
            "wallet_id": str(wallet.id),
            "method": "wallet",
        }

    async def _process_external_payment(
        self, payment: Payment, command: ProcessPayCommand
    ) -> Dict[str, Any]:
        """Process payment using external gateway."""
        gateway_metadata = {
            "payment_id": str(payment.id),
            "user_id": str(payment.user_id),
            "payment_type": payment.payment_type.value,
            "correlation_id": (
                str(command.correlation_id) if command.correlation_id else None
            ),
        }

        if command.metadata:
            gateway_metadata.update(command.metadata)

        gateway_result = await self.payment_gateway.process_payment(
            amount=payment.amount.to_float(),
            currency=payment.amount.currency.value,
            payment_method=payment.payment_method.value,
            metadata=gateway_metadata,
        )

        await self._process_gateway_result(gateway_result, payment)
        return gateway_result

    async def _send_notifications(
        self, payment: Payment, processing_result: Dict[str, Any]
    ) -> None:
        """Send appropriate notifications based on payment status."""
        try:
            if payment.status.value == "completed":
                await self.notification_service.send_payment_confirmation(
                    user_id=payment.user_id.value,
                    payment_details={
                        "payment_id": str(payment.id),
                        "amount": payment.amount.to_float(),
                        "currency": payment.amount.currency.value,
                        "payment_type": payment.payment_type.value,
                        "transaction_reference": processing_result.get(
                            "transaction_id"
                        ),
                    },
                )
            elif payment.status.value in ["failed", "cancelled"]:
                await self.notification_service.send_payment_failure(
                    user_id=payment.user_id.value,
                    failure_details={
                        "payment_id": str(payment.id),
                        "amount": payment.amount.to_float(),
                        "currency": payment.amount.currency.value,
                        "failure_reason": payment.failure_reason,
                        "error_details": processing_result.get("error"),
                    },
                )
        except Exception as e:
            print(f"Failed to send notification: {e}")

    async def _procces_event(self, payment: Payment, result: Dict[str, Any]):
        await self._publish_payment_events(payment)
        await self._send_notifications(payment, result)

    def _create_payment_metadata(self, metadata: Dict[str, Any]):
        return PaymentMetadata(
            ticket_ids=metadata.get("ticket_ids"),
            showtime_id=metadata.get("showtime_id"),
            seat_numbers=metadata.get("seat_numbers"),
            food_items=metadata.get("food_items"),
            pickup_location=metadata.get("pickup_location"),
            special_instructions=metadata.get("special_instructions"),
        )

    async def _handle_payment_method(self, payment_method, payment, command):
        if payment_method == PaymentMethod.WALLET:
            result = await self._process_wallet_payment(payment, command.wallet_id)
        else:
            result = await self._process_external_payment(payment, command)

        return result

    async def _proccess_payment_failure(
        self, payment: Optional[Payment], message: str
    ) -> ProcessPaymentResult:
        if payment is not None:
            payment.fail(str(message), error_code=type(message).__name__)
            await self.payment_repository.save(payment)
            await self._publish_payment_events(payment)
            await self._send_notifications(payment, {"error": str(message)})

        return ProcessPaymentResult(
            payment_id=payment.id.value if payment is not None else UUID(int=0),
            status="failed",
            message=f"Payment failed: {str(message)}",
        )

    async def _get_user_wallet(self, user_id) -> Wallet:
        wallet = await self.wallet_repository.get_by_user_id(user_id)
        if not wallet:
            raise ValueError("User does not have a wallet")

        return wallet

    async def _get_wallet_by_id(self, wallet_id: UUID) -> Wallet:
        wallet = await self.wallet_repository.get_by_id(
            WalletId.from_string(str(wallet_id))
        )

        if not wallet:
            raise ValueError("Wallet not found")

        return wallet

    async def _publish_wallet_events(self, wallet: Wallet):
        wallet_events = wallet.get_events()

        for event in wallet_events:
            await self.event_publisher.publish(event)

        wallet.clear_events()

    async def _publish_payment_events(self, payment: Payment) -> None:
        """Publish all domain events from the payment."""
        events = payment.get_events()
        if events:
            await self.event_publisher.publish_batch(events)
            payment.clear_events()

    async def _process_gateway_result(self, gateway_result, payment):
        if gateway_result.get("status") == "success":
            payment.complete(transaction_reference=gateway_result.get("transaction_id"))
        else:
            payment.fail(
                reason=gateway_result.get("error", "Unknown gateway error"),
                error_code=gateway_result.get("error_code"),
            )
