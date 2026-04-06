from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.db import get_db
from app.employees.application.use_cases.container import EmployeeUseCases
from app.employees.infrastructure.persistence.sqlalchemy_employee_repo import (
    SQLAlchemyEmployeeRepository,
)


def get_employee_use_cases(session: AsyncSession = Depends(get_db)) -> EmployeeUseCases:
    repo = SQLAlchemyEmployeeRepository(session)
    return EmployeeUseCases(repo)
