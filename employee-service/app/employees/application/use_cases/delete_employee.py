from app.employees.domain.exceptions import EmployeeNotFoundError
from app.employees.domain.repositories import EmployeeRepository


class DeleteEmployeeUseCase:
    def __init__(self, repository: EmployeeRepository):
        self._repository = repository

    async def execute(self, employee_id: int) -> None:
        employee = await self._repository.get_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundError(employee_id)
        await self._repository.delete(employee_id)
