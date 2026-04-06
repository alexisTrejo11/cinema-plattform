from app.employees.domain.entities import Employee
from app.employees.domain.exceptions import EmployeeNotFoundError
from app.employees.domain.repositories import EmployeeRepository

from ..commands import UpdateEmployeeCommand


class UpdateEmployeeUseCase:
    def __init__(self, repository: EmployeeRepository):
        self._repository = repository

    async def execute(self, command: UpdateEmployeeCommand) -> Employee:
        employee = await self._repository.get_by_id(command.employee_id)
        if not employee:
            raise EmployeeNotFoundError(command.employee_id)

        updatable_fields = (
            "first_name", "last_name", "phone", "position",
            "department", "contract_type", "salary",
            "emergency_contact_name", "emergency_contact_phone", "notes",
        )
        for field_name in updatable_fields:
            value = getattr(command, field_name, None)
            if value is not None:
                object.__setattr__(employee, field_name, value)

        from datetime import datetime
        object.__setattr__(employee, "updated_at", datetime.now())

        return await self._repository.update(employee)
