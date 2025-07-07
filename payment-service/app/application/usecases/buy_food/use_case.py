from ...commands.procces_pay import ProcessPayCommand
from datetime import datetime

class BuyProductUseCase:
    """
    Use case for orchestrating the product purchase process.
    """
    
    async def execute(self, command: ProcessPayCommand) -> None:
        """
        Executes the product purchase logic based on the provided command.

        Args:
            command (ProcessPayCommand): The command containing purchase and payment details.

        Raises:
            ProductNotFoundException: If the product does not exist.
            ProductOutOfStockException: If the product is out of stock.
            Exception: If an unexpected error occurs during payment processing.
        """

        
