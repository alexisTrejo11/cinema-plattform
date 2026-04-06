from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.employees.domain.exceptions import (
    EmployeeAlreadyExistsError,
    EmployeeNotFoundError,
    InvalidEmployeeOperationError,
)
from app.schedules.domain.exceptions import (
    ScheduleConflictError,
    ScheduleNotFoundError,
)
from app.vacations.domain.exceptions import (
    VacationNotFoundError,
    VacationRequestConflictError,
    VacationRequestInvalidStatusError,
)


def register(app: FastAPI) -> None:
    @app.exception_handler(EmployeeNotFoundError)
    async def employee_not_found(request: Request, exc: EmployeeNotFoundError):
        return JSONResponse(status_code=404, content={"error": "EMPLOYEE_NOT_FOUND", "message": str(exc)})

    @app.exception_handler(EmployeeAlreadyExistsError)
    async def employee_already_exists(request: Request, exc: EmployeeAlreadyExistsError):
        return JSONResponse(status_code=409, content={"error": "EMPLOYEE_ALREADY_EXISTS", "message": str(exc)})

    @app.exception_handler(InvalidEmployeeOperationError)
    async def invalid_employee_operation(request: Request, exc: InvalidEmployeeOperationError):
        return JSONResponse(status_code=422, content={"error": "INVALID_OPERATION", "message": str(exc)})

    @app.exception_handler(ScheduleNotFoundError)
    async def schedule_not_found(request: Request, exc: ScheduleNotFoundError):
        return JSONResponse(status_code=404, content={"error": "SCHEDULE_NOT_FOUND", "message": str(exc)})

    @app.exception_handler(ScheduleConflictError)
    async def schedule_conflict(request: Request, exc: ScheduleConflictError):
        return JSONResponse(status_code=409, content={"error": "SCHEDULE_CONFLICT", "message": str(exc)})

    @app.exception_handler(VacationNotFoundError)
    async def vacation_not_found(request: Request, exc: VacationNotFoundError):
        return JSONResponse(status_code=404, content={"error": "VACATION_NOT_FOUND", "message": str(exc)})

    @app.exception_handler(VacationRequestConflictError)
    async def vacation_conflict(request: Request, exc: VacationRequestConflictError):
        return JSONResponse(status_code=409, content={"error": "VACATION_CONFLICT", "message": str(exc)})

    @app.exception_handler(VacationRequestInvalidStatusError)
    async def vacation_invalid_status(request: Request, exc: VacationRequestInvalidStatusError):
        return JSONResponse(status_code=422, content={"error": "VACATION_INVALID_STATUS", "message": str(exc)})
