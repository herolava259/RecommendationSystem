from pydantic import BaseModel, Field


class Account(BaseModel):
    user_name: str = Field()

