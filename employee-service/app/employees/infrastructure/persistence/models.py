from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, Enum as SQLEnum, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.config.db import Base
from app.employees.domain.entities import Employee
from app.employees.domain.enums import ContractType, Department, EmployeeRole, EmploymentStatus


class EmployeeModel(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    position: Mapped[str] = mapped_column(String(100), nullable=False)
    department: Mapped[Department] = mapped_column(SQLEnum(Department), nullable=False)
    contract_type: Mapped[ContractType] = mapped_column(SQLEnum(ContractType), nullable=False)
    role: Mapped[EmployeeRole] = mapped_column(SQLEnum(EmployeeRole), nullable=False, default=EmployeeRole.EMPLOYEE)
    employment_status: Mapped[EmploymentStatus] = mapped_column(
        SQLEnum(EmploymentStatus), nullable=False, default=EmploymentStatus.ACTIVE, index=True
    )
    salary: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False, default=0)
    hire_date: Mapped[date] = mapped_column(Date, nullable=False)
    termination_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    emergency_contact_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    emergency_contact_phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    def to_domain(self) -> Employee:
        return Employee(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            phone=self.phone,
            position=self.position,
            department=self.department,
            contract_type=self.contract_type,
            role=self.role,
            employment_status=self.employment_status,
            salary=self.salary,
            hire_date=self.hire_date,
            termination_date=self.termination_date,
            emergency_contact_name=self.emergency_contact_name,
            emergency_contact_phone=self.emergency_contact_phone,
            notes=self.notes,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_domain(cls, employee: Employee) -> "EmployeeModel":
        return cls(
            id=employee.id if employee.id != 0 else None,
            first_name=employee.first_name,
            last_name=employee.last_name,
            email=employee.email,
            phone=employee.phone,
            position=employee.position,
            department=employee.department,
            contract_type=employee.contract_type,
            role=employee.role,
            employment_status=employee.employment_status,
            salary=employee.salary,
            hire_date=employee.hire_date,
            termination_date=employee.termination_date,
            emergency_contact_name=employee.emergency_contact_name,
            emergency_contact_phone=employee.emergency_contact_phone,
            notes=employee.notes,
            created_at=employee.created_at,
            updated_at=employee.updated_at,
        )
