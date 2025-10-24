from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime, date

class Review(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    product_id: UUID = Field(default_factory=uuid4)
    rating: int = Field(default=1,gt=1,lt=5)
    content: str = Field(default="")
    review_date: date = Field(default=date.today())


