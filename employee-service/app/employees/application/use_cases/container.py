from app.employees.domain.entities import Employee
from app.employees.domain.repositories import EmployeeRepository
from app.shared.pagination import Page

from ..commands import (
    HireEmployeeCommand,
    PromoteEmployeeCommand,
    ReactivateEmployeeCommand,
    SuspendEmployeeCommand,
    TerminateEmployeeCommand,
    UpdateEmployeeCommand,
)
from ..queries import GetEmployeeByIdQuery, ListEmployeesQuery
from .delete_employee import DeleteEmployeeUseCase
from .employee_actions import (
    PromoteEmployeeUseCase,
    ReactivateEmployeeUseCase,
    SuspendEmployeeUseCase,
    TerminateEmployeeUseCase,
)
from .hire_employee import HireEmployeeUseCase
from .query_employees import GetEmployeeByIdUseCase, ListEmployeesUseCase
from .update_employee import UpdateEmployeeUseCase


class EmployeeUseCases:
    """Aggregates all employee use cases — acts as a facade."""

    def __init__(self, repository: EmployeeRepository):
        self._hire = HireEmployeeUseCase(repository)
        self._update = UpdateEmployeeUseCase(repository)
        self._delete = DeleteEmployeeUseCase(repository)
        self._get = GetEmployeeByIdUseCase(repository)
        self._list = ListEmployeesUseCase(repository)
        self._terminate = TerminateEmployeeUseCase(repository)
        self._suspend = SuspendEmployeeUseCase(repository)
        self._reactivate = ReactivateEmployeeUseCase(repository)
        self._promote = PromoteEmployeeUseCase(repository)

    async def hire(self, command: HireEmployeeCommand) -> Employee:
        return await self._hire.execute(command)

    async def update(self, command: UpdateEmployeeCommand) -> Employee:
        return await self._update.execute(command)

    async def delete(self, employee_id: int) -> None:
        return await self._delete.execute(employee_id)

    async def get_by_id(self, query: GetEmployeeByIdQuery) -> Employee:
        return await self._get.execute(query)

    async def list_all(self, query: ListEmployeesQuery) -> Page[Employee]:
        return await self._list.execute(query)

    async def terminate(self, command: TerminateEmployeeCommand) -> Employee:
        return await self._terminate.execute(command)

    async def suspend(self, command: SuspendEmployeeCommand) -> Employee:
        return await self._suspend.execute(command)

    async def reactivate(self, command: ReactivateEmployeeCommand) -> Employee:
        return await self._reactivate.execute(command)

    async def promote(self, command: PromoteEmployeeCommand) -> Employee:
        return await self._promote.execute(command)
