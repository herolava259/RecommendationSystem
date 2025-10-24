from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import date
import datetime

class Comment(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    created_date: date = Field(default_factory=datetime.datetime.now)
    updated_date: date = Field(default_factory=datetime.datetime.now)
    content: str = Field(default = "")
    feed_id: UUID = Field(default_factory=uuid4)


