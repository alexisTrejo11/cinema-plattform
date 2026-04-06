from dataclasses import dataclass

from app.employees.domain.enums import Department, EmploymentStatus
from app.shared.pagination import PaginationParams


@dataclass
class GetEmployeeByIdQuery:
    employee_id: int


@dataclass
class ListEmployeesQuery:
    pagination: PaginationParams
    department: Department | None = None
    status: EmploymentStatus | None = None
    search: str | None = None
