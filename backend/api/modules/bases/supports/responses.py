from pydantic import BaseModel
from typing import TypeVar

class BaseResponse(BaseModel):
    pass

TResponse = TypeVar('TResponse', bound=BaseResponse)

class ResponseSupport:
    pass
