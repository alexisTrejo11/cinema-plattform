class UserNotFoundException(Exception):
    """Exception raised when a user is not found in the repository."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
