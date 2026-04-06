class EmployeeNotFoundError(Exception):
    """Raised when the requested employee does not exist."""

    def __init__(self, employee_id: int | str):
        self.employee_id = employee_id
        super().__init__(f"Employee not found: {employee_id}")


class EmployeeAlreadyExistsError(Exception):
    """Raised when trying to create an employee with a duplicate email."""

    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Employee already exists with email: {email}")


class InvalidEmployeeOperationError(Exception):
    """Raised when a business operation is not allowed in the current state."""

    def __init__(self, message: str):
        super().__init__(message)
