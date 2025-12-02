from pydantic import BaseModel
from typing import TypeVar, Any
class BaseRequest(BaseModel):
    pass

TRequest = TypeVar('TRequest', bound=BaseRequest)

class RequestSupport:
    pass
