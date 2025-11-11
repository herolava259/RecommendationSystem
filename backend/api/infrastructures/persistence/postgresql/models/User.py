from sqlmodel import Field, SQLModel, create_engine
from uuid import UUID, uuid4


class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(nullable=False, min_length=8, max_length=512, default="")
    phone_number: str = Field(nullable=False, min_length=8, max_length=512, default="")
    address: str = Field(nullable=False, min_length=8, max_length=512, default="")
    thumbnail_url = Field(nullable=False, default="")


class Customer(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4)
    Name: str = Field(default_factory=str)
    Email: str = Field(default_factory=str)
    Address: str = Field(default_factory=str)
    PhoneNumber: str = Field(default_factory=str, min_length=10, max_length=11)