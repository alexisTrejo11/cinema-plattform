from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, Field, model_validator

from .enums import ContractType, Department, EmployeeRole, EmploymentStatus
from .exceptions import InvalidEmployeeOperationError


class Employee(BaseModel):
    """Core employee domain entity. Holds business logic for state transitions."""

    model_config = {"arbitrary_types_allowed": True}

    id: int = 0
    first_name: str
    last_name: str
    email: str
    phone: str | None = None
    position: str
    department: Department
    contract_type: ContractType = ContractType.FULL_TIME
    role: EmployeeRole = EmployeeRole.EMPLOYEE
    employment_status: EmploymentStatus = EmploymentStatus.ACTIVE
    salary: Decimal = Field(default=Decimal("0.00"), ge=0)
    hire_date: date = Field(default_factory=date.today)
    termination_date: date | None = None
    emergency_contact_name: str | None = None
    emergency_contact_phone: str | None = None
    notes: str | None = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def is_active(self) -> bool:
        return self.employment_status == EmploymentStatus.ACTIVE

    @model_validator(mode="after")
    def _validate_email(self) -> "Employee":
        if "@" not in self.email or "." not in self.email.split("@")[-1]:
            raise ValueError(f"Invalid email address: {self.email}")
        return self

    @model_validator(mode="after")
    def _validate_termination_date(self) -> "Employee":
        if self.termination_date and self.termination_date < self.hire_date:
            raise ValueError("Termination date cannot be before hire date")
        return self

    def terminate(self, termination_date: date | None = None) -> None:
        """Fire/terminate the employee."""
        if self.employment_status == EmploymentStatus.TERMINATED:
            raise InvalidEmployeeOperationError(
                f"Employee {self.id} is already terminated"
            )
        self.employment_status = EmploymentStatus.TERMINATED
        self.termination_date = termination_date or date.today()
        self.updated_at = datetime.now()

    def suspend(self) -> None:
        """Suspend the employee temporarily."""
        if self.employment_status != EmploymentStatus.ACTIVE:
            raise InvalidEmployeeOperationError(
                f"Cannot suspend employee {self.id} — current status: {self.employment_status}"
            )
        self.employment_status = EmploymentStatus.SUSPENDED
        self.updated_at = datetime.now()

    def reactivate(self) -> None:
        """Reactivate a suspended or on-leave employee."""
        if self.employment_status not in (EmploymentStatus.SUSPENDED, EmploymentStatus.ON_LEAVE):
            raise InvalidEmployeeOperationError(
                f"Cannot reactivate employee {self.id} — current status: {self.employment_status}"
            )
        self.employment_status = EmploymentStatus.ACTIVE
        self.updated_at = datetime.now()

    def set_on_leave(self) -> None:
        """Mark employee as on approved leave."""
        if self.employment_status != EmploymentStatus.ACTIVE:
            raise InvalidEmployeeOperationError(
                f"Cannot set on_leave for employee {self.id} — current status: {self.employment_status}"
            )
        self.employment_status = EmploymentStatus.ON_LEAVE
        self.updated_at = datetime.now()

    def promote(self, new_position: str, new_salary: Decimal, new_role: EmployeeRole | None = None) -> None:
        """Update position and optionally role/salary."""
        if self.employment_status == EmploymentStatus.TERMINATED:
            raise InvalidEmployeeOperationError(
                f"Cannot promote terminated employee {self.id}"
            )
        self.position = new_position
        self.salary = new_salary
        if new_role:
            self.role = new_role
        self.updated_at = datetime.now()

    @classmethod
    def create(cls, data: dict) -> "Employee":
        return cls(**data)
