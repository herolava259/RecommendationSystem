from datetime import datetime

from pydantic import BaseModel, Field
from uuid import UUID, uuid4
import datetime
from datetime import date

from typing import List

class Feed(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    create_date: date = Field(default_factory=datetime.now)
    content: str = Field(default = "")
    creator_id: UUID = Field(default_factory=uuid4)
    image_urls: List[str] = Field(default_factory=list)
