from sqlmodel import SQLModel, Field, Column
from uuid import UUID, uuid4
import sqlalchemy.dialects.postgresql as pg
from typing import Any

class EntityBase(SQLModel, table=False):
    id: UUID | Any = Field(sa_column=Column(pg.UUID,default=uuid4,nullable=False, primary_key=True, server_default=None))
    deleted: bool = Field(default=False, nullable=False)