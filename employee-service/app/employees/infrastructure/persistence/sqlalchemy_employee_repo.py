from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.employees.domain.entities import Employee
from app.employees.domain.enums import Department, EmploymentStatus
from app.employees.domain.repositories import EmployeeRepository
from app.shared.pagination import Page, PaginationParams

from .models import EmployeeModel


class SQLAlchemyEmployeeRepository(EmployeeRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, employee_id: int) -> Employee | None:
        result = await self._session.get(EmployeeModel, employee_id)
        return result.to_domain() if result else None

    async def get_by_email(self, email: str) -> Employee | None:
        stmt = select(EmployeeModel).where(EmployeeModel.email == email)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        return model.to_domain() if model else None

    async def list(
        self,
        pagination: PaginationParams,
        department: Department | None = None,
        status: EmploymentStatus | None = None,
        search: str | None = None,
    ) -> Page[Employee]:
        stmt = select(EmployeeModel)

        if department:
            stmt = stmt.where(EmployeeModel.department == department)
        if status:
            stmt = stmt.where(EmployeeModel.employment_status == status)
        if search:
            pattern = f"%{search}%"
            stmt = stmt.where(
                or_(
                    EmployeeModel.first_name.ilike(pattern),
                    EmployeeModel.last_name.ilike(pattern),
                    EmployeeModel.email.ilike(pattern),
                    EmployeeModel.position.ilike(pattern),
                )
            )

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self._session.execute(count_stmt)
        total = total_result.scalar_one()

        stmt = stmt.offset(pagination.offset).limit(pagination.limit).order_by(EmployeeModel.id)
        rows = await self._session.execute(stmt)
        items = [model.to_domain() for model in rows.scalars().all()]

        return Page(items=items, total=total, page=pagination.page, page_size=pagination.page_size)

    async def create(self, employee: Employee) -> Employee:
        model = EmployeeModel.from_domain(employee)
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return model.to_domain()

    async def update(self, employee: Employee) -> Employee:
        model = await self._session.get(EmployeeModel, employee.id)
        if not model:
            return employee

        model.first_name = employee.first_name
        model.last_name = employee.last_name
        model.email = employee.email
        model.phone = employee.phone
        model.position = employee.position
        model.department = employee.department
        model.contract_type = employee.contract_type
        model.role = employee.role
        model.employment_status = employee.employment_status
        model.salary = employee.salary
        model.hire_date = employee.hire_date
        model.termination_date = employee.termination_date
        model.emergency_contact_name = employee.emergency_contact_name
        model.emergency_contact_phone = employee.emergency_contact_phone
        model.notes = employee.notes
        model.updated_at = employee.updated_at

        await self._session.commit()
        await self._session.refresh(model)
        return model.to_domain()

    async def delete(self, employee_id: int) -> None:
        model = await self._session.get(EmployeeModel, employee_id)
        if model:
            await self._session.delete(model)
            await self._session.commit()
