from ...commands.credit.command import AddCreditCommand
from ...commands.credit.result import AddCreditResult
from ...commands.credit.handler import AddCreditCommandHandler

class AddCreditToWalletUseCase:
    def __init__(self, add_credit_handler: AddCreditCommandHandler) -> None:
        self.add_credit_handler = add_credit_handler
    
    async def execute(self, credit_command: AddCreditCommand) -> AddCreditResult:
        result = await self.add_credit_handler.handle(credit_command)
        return result
    
    