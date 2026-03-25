from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, EmailStr, Field

from app.employees.domain.entities import Employee
from app.employees.domain.enums import ContractType, Department, EmployeeRole, EmploymentStatus


class EmployeeCreateRequest(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: str | None = Field(default=None, max_length=20)
    position: str = Field(..., min_length=1, max_length=100)
    department: Department
    contract_type: ContractType = ContractType.FULL_TIME
    role: EmployeeRole = EmployeeRole.EMPLOYEE
    salary: Decimal = Field(..., ge=0, decimal_places=2)
    hire_date: date | None = None
    emergency_contact_name: str | None = Field(default=None, max_length=100)
    emergency_contact_phone: str | None = Field(default=None, max_length=20)
    notes: str | None = Field(default=None, max_length=1000)


class EmployeeUpdateRequest(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    phone: str | None = Field(default=None, max_length=20)
    position: str | None = Field(default=None, min_length=1, max_length=100)
    department: Department | None = None
    contract_type: ContractType | None = None
    salary: Decimal | None = Field(default=None, ge=0, decimal_places=2)
    emergency_contact_name: str | None = Field(default=None, max_length=100)
    emergency_contact_phone: str | None = Field(default=None, max_length=20)
    notes: str | None = Field(default=None, max_length=1000)


class PromoteEmployeeRequest(BaseModel):
    new_position: str = Field(..., min_length=1, max_length=100)
    new_salary: Decimal = Field(..., ge=0, decimal_places=2)
    new_role: EmployeeRole | None = None


class TerminateEmployeeRequest(BaseModel):
    termination_date: date | None = None


class EmployeeResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    full_name: str
    email: str
    phone: str | None
    position: str
    department: Department
    contract_type: ContractType
    role: EmployeeRole
    employment_status: EmploymentStatus
    salary: Decimal
    hire_date: date
    termination_date: date | None
    emergency_contact_name: str | None
    emergency_contact_phone: str | None
    notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

    @classmethod
    def from_domain(cls, employee: Employee) -> "EmployeeResponse":
        return cls(
            id=employee.id,
            first_name=employee.first_name,
            last_name=employee.last_name,
            full_name=employee.full_name,
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
