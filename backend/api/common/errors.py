from typing import Any, Callable, Coroutine

from fastapi import Request
from fastapi.responses import JSONResponse

from fastapi import FastAPI, status

from sqlalchemy.exc import SQLAlchemyError

from common.base import ApplicationException


# error from role, resource management

def create_exception_handler(
        status_code: int, initial_detail: Any
) -> Callable[[Request, ApplicationException], Coroutine[Any, Any, JSONResponse]] | Any:
    async def exception_handler(request: Request, exc: ApplicationException) -> JSONResponse:
        return JSONResponse(content=initial_detail, status_code=status_code)
    return exception_handler

def register_all_errors(app: FastAPI):

    app.add_exception_handler(
        exc_class_or_status_code=ApplicationException,
        handler=create_exception_handler(
            status_code=status.HTTP_404_NOT_FOUND,
            initial_detail={"message": "Bad Request", "error_code": "400"},
        )
    )

    # register error for account module


    # register error for movie module

    # register errors for user module

    # register errors for role module


