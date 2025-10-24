from uuid import UUID, uuid4
from pydantic import BaseModel,Field
from uuid import UUID, uuid4

class Feedback(BaseModel):
    rating: int = Field(default=1, ge= 1, lt=5)
    content: str = Field(default="", min_length=1, max_length=16384)
    id: UUID = Field(default_factory=uuid4)
    customer_id: UUID = Field(default_factory=uuid4, )