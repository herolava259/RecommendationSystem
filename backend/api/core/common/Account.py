from pydantic import BaseModel, Field


class Account(BaseModel):
    user_name: str = Field(default="abc", min_length= 12, max_length=256)
    password_hash: str = Field(default="abc", min_length=16, max_length=1024)



