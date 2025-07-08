from app.domain.entities.wallet import Wallet
from app.domain.value_objects import UserId, Money, Currency, WalletId, TransactionId
from app.application.interfaces import EventPublisher, WalletRepository, NotificationService
from .result import AddCreditResult, AddCreditResultBuilder
from .command import AddCreditCommand
from typing import Tuple
from asyncio import gather

class AddCreditCommandHandler:
    """Handler for adding credit to user wallets."""
    def __init__(self, wallet_repository: WalletRepository, event_publisher: EventPublisher, notification_service: NotificationService):
        self.wallet_repository = wallet_repository
        self.event_publisher = event_publisher
        self.notification_service = notification_service
    
    async def handle(self, command: AddCreditCommand) -> AddCreditResult:
        """
        Handle add credit command.
        
        Args:
            command: Add credit command
            
        Returns:
            Add credit result
            
        Raises:
            ValueError: If wallet not found or invalid parameters
            InvalidWalletOperationException: If credit operation fails
        """
        try:
            wallet = await self._get_or_create_wallet(command)
            self._validate_wallet_currency(wallet, command)
            
            amount, transaction_id = self._procces_transaction(command, wallet)
            
            saved_wallet = await self.wallet_repository.save(wallet)
            
            await self._proccess_event(saved_wallet, amount, transaction_id)

            return self._build_response(wallet, amount, transaction_id)
        except Exception as e:
            return AddCreditResult.invalid_credit_result(command.wallet_id, command.user_id, command.amount, command.currency, str(e))
    
    async def _publish_events(self, wallet: Wallet) -> None:
        """Publish all domain events from the wallet."""
        events = wallet.get_events()
        if events:
            await self.event_publisher.publish_batch(events)
            wallet.clear_events()
    
    
    async def _send_notifications(self, wallet: Wallet, amount: Money,transaction_id) -> None:
        """Send credit confirmation notifications."""
        try:
            await self.notification_service.send_payment_confirmation(
                user_id=wallet.user_id.value,
                payment_details={
                    'wallet_id': str(wallet.id),
                    'transaction_id': str(transaction_id),
                    'amount': amount.to_float(),
                    'currency': amount.currency.value,
                    'new_balance': wallet.balance.to_float(),
                    'notification_type': 'credit_added'
                }
            )
        except Exception as e:
            print(f"Failed to send credit notification: {e}")

    def _validate_wallet_currency(self, wallet: Wallet, command: AddCreditCommand):
        if wallet.currency != Currency(command.currency):
            raise ValueError(f"Wallet currency {wallet.currency} does not match credit currency {command.currency}")   
    
    async def _get_or_create_wallet(self, command: AddCreditCommand):
        user_id = UserId.from_string(str(command.user_id))
        
        if command.wallet_id:
            wallet = await self._get_wallet(str(command.user_id))
        else:
            wallet = await self._create_wallet(user_id, Currency(command.currency))

        return wallet

    async def _get_wallet(self, wallet_id_str: str) -> Wallet:
            wallet_id = WalletId.from_string(wallet_id_str)
            wallet = await self.wallet_repository.get_by_id(wallet_id)
            if not wallet:
                raise ValueError(f"Wallet {wallet_id_str} not found")
            
            return wallet
        
    async def _create_wallet(self, user_id: UserId, currency: Currency) -> Wallet:
        wallet = await self.wallet_repository.get_by_user_id(user_id)
        if not wallet:
            wallet = Wallet.create(user_id=user_id, currency=Currency(currency))
            wallet = await self.wallet_repository.save(wallet)
            
        return wallet 
    
    async def _proccess_event(self, wallet: Wallet, amount: Money, transaction_id):
        event_coroutine= self._publish_events(wallet)
        notifcation_courutine = self._send_notifications(wallet, amount, transaction_id)
        
        _, _ = await gather(event_coroutine, notifcation_courutine)
     
    def _procces_transaction(self, command: AddCreditCommand, wallet: Wallet) -> Tuple[Money, TransactionId]:
        amount = Money.from_float(command.amount, Currency(command.currency))
        transaction_id = wallet.credit(amount, command.description, command.reference_id)
        
        return amount, transaction_id

    def _build_response(self, saved_wallet: Wallet, amount: Money, transaction_id) -> AddCreditResult:
        return AddCreditResultBuilder() \
            .set_wallet_id(saved_wallet.id.value) \
            .set_transaction_id(transaction_id.value) \
            .set_user_id(saved_wallet.user_id.value) \
            .set_amount(amount.to_float()) \
            .set_currency(amount.currency.value) \
            .set_new_balance(saved_wallet.balance.to_float()) \
            .set_status("success") \
            .set_message("Credit added successfully") \
            .build()
    
    