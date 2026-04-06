from app.employees.domain.entities import Employee
from app.employees.domain.exceptions import EmployeeNotFoundError
from app.employees.domain.repositories import EmployeeRepository
from app.shared.pagination import Page

from ..queries import GetEmployeeByIdQuery, ListEmployeesQuery


class GetEmployeeByIdUseCase:
    def __init__(self, repository: EmployeeRepository):
        self._repository = repository

    async def execute(self, query: GetEmployeeByIdQuery) -> Employee:
        employee = await self._repository.get_by_id(query.employee_id)
        if not employee:
            raise EmployeeNotFoundError(query.employee_id)
        return employee


class ListEmployeesUseCase:
    def __init__(self, repository: EmployeeRepository):
        self._repository = repository

    async def execute(self, query: ListEmployeesQuery) -> Page[Employee]:
        return await self._repository.list(
            pagination=query.pagination,
            department=query.department,
            status=query.status,
            search=query.search,
        )
