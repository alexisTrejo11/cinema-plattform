from app.employees.domain.entities import Employee
from app.employees.domain.exceptions import EmployeeNotFoundError
from app.employees.domain.repositories import EmployeeRepository

from ..commands import (
    PromoteEmployeeCommand,
    ReactivateEmployeeCommand,
    SuspendEmployeeCommand,
    TerminateEmployeeCommand,
)


class TerminateEmployeeUseCase:
    def __init__(self, repository: EmployeeRepository):
        self._repository = repository

    async def execute(self, command: TerminateEmployeeCommand) -> Employee:
        employee = await self._repository.get_by_id(command.employee_id)
        if not employee:
            raise EmployeeNotFoundError(command.employee_id)
        employee.terminate(command.termination_date)
        return await self._repository.update(employee)


class SuspendEmployeeUseCase:
    def __init__(self, repository: EmployeeRepository):
        self._repository = repository

    async def execute(self, command: SuspendEmployeeCommand) -> Employee:
        employee = await self._repository.get_by_id(command.employee_id)
        if not employee:
            raise EmployeeNotFoundError(command.employee_id)
        employee.suspend()
        return await self._repository.update(employee)


class ReactivateEmployeeUseCase:
    def __init__(self, repository: EmployeeRepository):
        self._repository = repository

    async def execute(self, command: ReactivateEmployeeCommand) -> Employee:
        employee = await self._repository.get_by_id(command.employee_id)
        if not employee:
            raise EmployeeNotFoundError(command.employee_id)
        employee.reactivate()
        return await self._repository.update(employee)


class PromoteEmployeeUseCase:
    def __init__(self, repository: EmployeeRepository):
        self._repository = repository

    async def execute(self, command: PromoteEmployeeCommand) -> Employee:
        employee = await self._repository.get_by_id(command.employee_id)
        if not employee:
            raise EmployeeNotFoundError(command.employee_id)
        employee.promote(command.new_position, command.new_salary, command.new_role)
        return await self._repository.update(employee)
