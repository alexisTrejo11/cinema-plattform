from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal

from app.employees.domain.enums import ContractType, Department, EmployeeRole


@dataclass
class HireEmployeeCommand:
    first_name: str
    last_name: str
    email: str
    position: str
    department: Department
    salary: Decimal
    contract_type: ContractType = ContractType.FULL_TIME
    role: EmployeeRole = EmployeeRole.EMPLOYEE
    phone: str | None = None
    hire_date: date = field(default_factory=date.today)
    emergency_contact_name: str | None = None
    emergency_contact_phone: str | None = None
    notes: str | None = None


@dataclass
class UpdateEmployeeCommand:
    employee_id: int
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    position: str | None = None
    department: Department | None = None
    contract_type: ContractType | None = None
    salary: Decimal | None = None
    emergency_contact_name: str | None = None
    emergency_contact_phone: str | None = None
    notes: str | None = None


@dataclass
class TerminateEmployeeCommand:
    employee_id: int
    termination_date: date | None = None


@dataclass
class SuspendEmployeeCommand:
    employee_id: int


@dataclass
class ReactivateEmployeeCommand:
    employee_id: int


@dataclass
class PromoteEmployeeCommand:
    employee_id: int
    new_position: str
    new_salary: Decimal
    new_role: EmployeeRole | None = None
