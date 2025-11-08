from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from datetime import datetime, date

class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_name: str = Field(default = "")
    created_date: date = Field(default_factory=datetime.now)
    thumbnail_url: str = Field(default = "")
    phone_number: str = Field(default = "")
    email: str = Field(default = "")
    address: str = Field(default = "")
    account_id: UUID = Field(default_factory=uuid4)
