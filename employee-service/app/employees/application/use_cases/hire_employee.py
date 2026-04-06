from app.employees.domain.entities import Employee
from app.employees.domain.exceptions import EmployeeAlreadyExistsError
from app.employees.domain.repositories import EmployeeRepository

from ..commands import HireEmployeeCommand


class HireEmployeeUseCase:
    def __init__(self, repository: EmployeeRepository):
        self._repository = repository

    async def execute(self, command: HireEmployeeCommand) -> Employee:
        existing = await self._repository.get_by_email(command.email)
        if existing:
            raise EmployeeAlreadyExistsError(command.email)

        employee = Employee.create({
            "first_name": command.first_name,
            "last_name": command.last_name,
            "email": command.email,
            "phone": command.phone,
            "position": command.position,
            "department": command.department,
            "contract_type": command.contract_type,
            "role": command.role,
            "salary": command.salary,
            "hire_date": command.hire_date,
            "emergency_contact_name": command.emergency_contact_name,
            "emergency_contact_phone": command.emergency_contact_phone,
            "notes": command.notes,
        })
        return await self._repository.create(employee)
