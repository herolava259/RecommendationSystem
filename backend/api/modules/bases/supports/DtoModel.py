from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class DtoModel(BaseModel):
    id: UUID = Field(default_factory=uuid4,)
    deleted: bool = Field(default= False)