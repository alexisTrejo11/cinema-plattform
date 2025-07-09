class UserException(Exception):
    """Base exception for user-related errors."""

    pass


class UserNotFoundException(UserException):
    """
    Exception raised when a requested user is not found.
    """

    def __init__(self, identifier: str, identifier_type: str = "ID"):
        self.identifier = identifier
        self.identifier_type = identifier_type
        super().__init__(f"User with {identifier_type} '{identifier}' not found.")


class UserAlreadyExistsException(UserException):
    """
    Exception raised when an attempt is made to create a user
    with an identifier (e.g., email, phone) that already exists.
    """

    def __init__(self, identifier: str, identifier_type: str = "identifier"):
        self.identifier = identifier
        self.identifier_type = identifier_type
        super().__init__(f"User with {identifier_type} '{identifier}' already exists.")


class UserDeletionFailedException(UserException):
    """
    Exception raised when a user deletion operation fails.
    """

    def __init__(self, user_id: str, reason: str = "unknown"):
        self.user_id = user_id
        self.reason = reason
        super().__init__(f"Failed to delete user '{user_id}': {reason}")


class UserUpdateFailedException(UserException):
    """
    Exception raised when a user update operation fails (e.g., no matching user found).
    """

    def __init__(self, user_id: str, reason: str = "unknown"):
        self.user_id = user_id
        self.reason = reason
        super().__init__(f"Failed to update user '{user_id}': {reason}")


class InvalidUserRoleException(UserException):
    """
    Exception raised when an invalid user role is provided.
    """

    def __init__(self, role: str):
        self.role = role
        super().__init__(f"Invalid user role: '{role}'.")


# You might also want a generic database exception if you catch low-level DB errors
# and want to re-raise them as domain-agnostic infrastructure exceptions,
# or map them to more specific domain exceptions.
class RepositoryException(Exception):
    """Base exception for repository-level errors (infrastructure concerns)."""

    pass


class DataIntegrityError(RepositoryException):
    """Raised when data integrity constraints are violated (e.g., unique key violation)."""

    def __init__(self, message: str = "Data integrity violation"):
        super().__init__(message)
