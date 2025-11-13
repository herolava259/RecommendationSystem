from typing import Any, Callable

from fastapi import Request
from fastapi.responses import JSONResponse

from fastapi import FastAPI, status

from sqlalchemy.exc import SQLAlchemyError


class ApplicationException(Exception):
    pass

# error from role, resource management




def create_exception_handler(
        status_code: int, initial_detail: Any
) -> Callable[[Request, ApplicationException], JSONResponse]:
    async def exception_handler(request: ApplicationException, exc: ApplicationException) -> JSONResponse:
        return JSONResponse(content=initial_detail, status_code=status_code)
    return exception_handler