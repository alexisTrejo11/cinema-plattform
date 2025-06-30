from app.utils.exceptions import NotFoundException, ApplicationException, ValidationException


def ComboNotFoundError(combo_id: int) -> NotFoundException:
    return NotFoundException("Combo", combo_id)


def ComboItemValidationError(reason: str) -> ValidationException:
    return ValidationException("combo item", reason)

def ProductValidationError() -> ValidationException:
    return ValidationException("product", "invalid prodcut provided")