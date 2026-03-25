from abc import ABC, abstractmethod

from app.shared.pagination import Page, PaginationParams

from .entities import Employee
from .enums import Department, EmploymentStatus


class EmployeeRepository(ABC):
    """Port: defines the contract for employee persistence."""

    @abstractmethod
    async def get_by_id(self, employee_id: int) -> Employee | None: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> Employee | None: ...

    @abstractmethod
    async def list(
        self,
        pagination: PaginationParams,
        department: Department | None = None,
        status: EmploymentStatus | None = None,
        search: str | None = None,
    ) -> Page[Employee]: ...

    @abstractmethod
    async def create(self, employee: Employee) -> Employee: ...

    @abstractmethod
    async def update(self, employee: Employee) -> Employee: ...

    @abstractmethod
    async def delete(self, employee_id: int) -> None: ...
