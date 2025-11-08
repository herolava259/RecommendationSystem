from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class Customer(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    Name: str = Field(default_factory=str)
    Email: str = Field(default_factory=str)
    Address: str = Field(default_factory=str)
    PhoneNumber: str = Field(default_factory=str, min_length=10, max_length=11)