from typing import Optional

import sqlalchemy.dialects.postgresql as pg
from sqlmodel import select, exists, update
from sqlmodel import Column, Field, Relationship, SQLModel
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
import uuid

class Team(SQLModel, table=True):
    id: int | None = Field(sa_column=Column(pg.BIGINT, primary_key=True))
    name: str = Field(index=True)
    headquarters: str

    heroes: list["Hero"] = Relationship(back_populates="team")
    abds: list["ABD"] = Relationship(back_populates="team")

class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)

    team_id: int | None = Field(default=None, foreign_key="team.id")
    team: Team | None = Relationship(back_populates="heroes")

class ABD(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    team: Optional[Team] | None = Relationship(back_populates="abds")
    team_id: int|None=Field(default=None,foreign_key="team.id")

class Account(SQLModel, table=True):
    __tablename__ = "account"
    id: uuid.UUID = Field(sa_column=Column(pg.UUID,default=uuid.uuid4,nullable=False, primary_key=True, server_default=None))
    email: str = Field(nullable=False)
    signin_name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False,), exclude=True)
    salt: str = Field(max_length=64, sa_column=Column(pg.VARCHAR, nullable=False,))
    pwd_hash: str = Field(sa_column=Column(pg.VARCHAR, nullable=False,), exclude=True)
    active: bool = Field(default=False)
    created_at: datetime =Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    private_information: Optional["AccountPrivateInformation"]=Relationship(
        back_populates="account",
        sa_relationship_kwargs={"lazy":"selectin"},
        cascade_delete=False
    )

    activation: Optional["AccountActivation"] = Relationship()

    def __repr__(self):
        return f"<Account {self.signin_name}"

class AccountActivation(SQLModel, table=True):
    __tablename__ = "activation"
    id: uuid.UUID =  Field(sa_column=Column(pg.UUID,default=uuid.uuid4,nullable=False, primary_key=True, server_default=None))
    activation_key: int=Field(max_length=1024)
    is_verified: bool=Field(default=False)
    expire_date: datetime=Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    ## relationship with Account table
    account_id: uuid.UUID = Field(default=None, foreign_key="account.id", unique=True)
    account: Account | None = Relationship(
        back_populates="activation",
    )

    def __repr__(self):
        return f"<AccountActivation {self.id}"


class AccountPrivateInformation(SQLModel, table=True):
    __tablename__ = "private_information"
    id: uuid.UUID =  Field(sa_column=Column(pg.UUID,default=uuid.uuid4,nullable=False, primary_key=True, server_default=None))
    phone: str = Field(max_length=64)
    special_name: str = Field(max_length=512)
    address: str = Field(max_length=1024)
    post_code: str = Field(max_length=64)
    user_name: str = Field(max_length=64)
    preference: str = Field(max_length=1024)
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    secret_qas: str = Field(default="")
    secret_key: str = Field(max_length=1024)

    account_id: uuid.UUID = Field(default=None, foreign_key="account.id", unique=True)
    account: Account | None = Relationship(back_populates="private_information")

    def __repr__(self):
        return f"<PrivateAccountInformation: {self.special_name}"


if __name__ == "__main__":
    #print(select(Hero,Team).join(Team,isouter=True))

    print(select(Account, AccountPrivateInformation).join(Account, isouter=True))