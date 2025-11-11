import uuid
from datetime import date, datetime

from typing import List, Optional

import sqlalchemy.dialects.postgresql as pg

from sqlmodel import Column, Field, Relationship, SQLModel


class Account(SQLModel, table=True):
    __tablename__ = "account"
    id: uuid.UUID = Field(sa_column=Column(pg.UUID,nullable=True, primary_key=True, dafault=uuid.uuid4))
    email: str = Field(nullable=False)
    signin_name: str = Field(nullable=False)
    salt: str = Field(max_length=64)
    pwd_hash: str = Field(sa_column=Column(pg.VARCHAR, nullable=False,), exclude=True)
    active: bool = Field(default=False)
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(default=None)
    updated_at: datetime = Field(default=None)

    private_information: Optional['AccountPrivateInformation'] = Relationship(
        back_populates="account",
        sa_relationship_kwargs={"lazy": "selectin"},
        cascade_delete=False
    )

    def __repr__(self):
        return f"<Account {self.signin_name}"


class AccountPrivateInformation(SQLModel, table=True):
    __tablename__ = "account_private_information"
    id: uuid.UUID = Field(default=uuid.uuid4)
    phone: str = Field(max_length=64)
    special_name: str = Field(max_length=512)
    address: str = Field(max_length=1024)
    post_code: str = Field(max_length=64)
    user_name: str = Field(max_length=64)
    preference: str = Field(max_length=1024)
    updated_at: datetime = Field(nullable=False)
    secret_qas: str = Field(default="")
    secret_key: str = Field(max_length=1024)

    account_id: uuid.UUID = Field(default=None, foreign_key="account.id")
    account: Optional[Account] = Relationship(back_populates="private_information")

    def __repr__(self):
        return f"<PrivateAccountInformation: {self.special_name}"

from .model import AccountModel, AccountPrivateInformationModel
from typing import List, Dict

class AccountTable(object):
    def insert_new_account(self, model: AccountModel) -> Optional[AccountModel]:
        pass
    def upsert_private_information(self, model: AccountPrivateInformationModel) -> Optional[AccountPrivateInformation]:
        pass
    def verify_email(self, account_id: uuid.UUID, secret_key: uuid.UUID, email: str) -> str:
        pass
    def deactivate_account(self, account_id: uuid.UUID) -> bool:
        pass

    def enable_account(self, account_id: uuid.UUID) -> bool:
        pass
    def activate_account(self, account_id: uuid.UUID) -> bool:
        pass

    def disable_account(self, account_id: uuid.UUID) -> bool:
        pass

    def validate_signin_process(self, signin_name: str, pwd_hash: str, get_private_info: bool = False) -> Optional[AccountModel]:
        pass

    def client_update_private_information(self, model: AccountPrivateInformation) -> Optional[AccountPrivateInformation]:
        pass

    def verify_identity_by_secret_qas(self, answers: Dict[str, str]) -> bool:
        pass

    def change_secret_key(self, signin_name: str, pwd_hash: str, client_secret_segment: str) -> bool:
        pass



AccountRepository = AccountTable()


