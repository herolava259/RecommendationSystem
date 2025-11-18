import uuid
from datetime import date, datetime

import sqlalchemy.dialects.postgresql as pg

from sqlmodel import Column, Field, Relationship, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from api.modules.account.error import VerifyEmailError
from api.modules.account.model import AccountPrivateInformationModel, EmailVerificationModel
from api.modules.account.model import AccountModel, AccountPrivateInformationModel
from typing import List, Dict, Set, Type, Union, Optional, Any
from sqlmodel import select, exists, update, delete
import logging
from sqlalchemy.orm import contains_eager, joinedload

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
    verified_email: bool = Field(default=False)

    private_information: Optional['AccountPrivateInformation'] = Relationship(
        back_populates="account",
        sa_relationship_kwargs={"lazy": "selectin"},
        cascade_delete=False
    )

    verification: Optional["EmailVerification"] = Relationship(
        back_populates="account",
        sa_relationship_kwargs={"lazy": "selectin"},
        cascade_delete=False
    )

    def __repr__(self):
        return f"<Account {self.signin_name}"

class EmailVerification(SQLModel, table = True):
    id: uuid.UUID =  Field(sa_column=Column(pg.UUID,default=uuid.uuid4,nullable=False, primary_key=True, server_default=None))
    activation_key: int=Field(max_length=1024)
    is_verified: bool=Field(default=False)
    expire_date: datetime=Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    ## relationship with Account table
    account_id: uuid.UUID = Field(default=None, foreign_key="account.id", unique=True)
    account: Optional["Account"] = Relationship(
        back_populates="verification",
    )


class AccountPrivateInformation(SQLModel, table=True):
    __tablename__ = "account_private_information"
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



logger  = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)



class AccountTable(object):

    async def insert_new_account(self, model: AccountModel, session: AsyncSession) -> Optional[AccountModel]:
        if self.account_exists(model.id, session):
            raise ValueError("Account already exists")

        account_data_dict = model.model_dump()

        new_account = Account(**account_data_dict)

        session.add(new_account)

        await session.commit()

        await session.refresh(new_account)

        model_data = new_account.model_dump()

        return AccountModel(**{key:model_data[key] for key in AccountModel.model_fields.keys()})

    async def insert_activation(self,model: EmailVerificationModel,session: AsyncSession) -> Optional[EmailVerificationModel]:
        new_record = self._dto_to_record(EmailVerificationModel, model)

        session.add(new_record)

        await session.commit()
        await session.refresh(new_record)
        model_data = new_record.model_dump()

        return self._record_to_dto(EmailVerificationModel, model_data)

    async def upsert_private_information(self, model: AccountPrivateInformationModel, session: AsyncSession) \
            -> AccountPrivateInformationModel|None:

        existing_record: AccountPrivateInformation = await self.get_private_information_by_id(model.id, session)

        if existing_record is None:

            new_record = self._dto_to_record(AccountPrivateInformation, model)
            session.add(new_record)
            await session.commit()

            await session.refresh(new_record)
            return self._record_to_dto(AccountPrivateInformationModel, new_record)

        upsert_data=model.model_dump()
        self._update_record(upsert_data, existing_record)
        await session.commit()
        await session.refresh(existing_record)

        return self._record_to_dto(AccountPrivateInformationModel, existing_record)

    async def verify_email(self, account_id: uuid.UUID, activation_key: int, email: str, session: AsyncSession) -> bool:

        query = select(Account).options(joinedload(Account.verification)).where((Account.id==account_id)&(Account.email==email))

        result = await session.exec(query)

        record: Account = result.first()

        if record is None:
            raise VerifyEmailError("Account and respected email do not match")

        if record.verification.activation_key != activation_key:
            raise VerifyEmailError("Invalid activation key")

        if record.verification.expire_date > datetime.now():
            raise VerifyEmailError("Activation expired")

        activation_id = record.verification.id
        try:
            update_account_query = update(Account).where(Account.id == account_id).values(verified_email = True)
            result =  await session.exec(update_account_query)
            if result.rowcount != 1:
                await session.rollback()
                return False
            update_activation_query = update(EmailVerification).where(EmailVerification.account_id==activation_id).values(is_verified = True)
            result = await session.exec(update_activation_query)
            if result.rowcount != 1:
                await session.rollback()
                return False
            await session.commit()
            #await session.refresh(record)
        except Exception as ex:
            await session.rollback()
            raise ex

        return True


    async def deactivate_account(self, account_id: uuid.UUID, session: AsyncSession) -> bool:
        update_command = update(Account).where(Account.id == account_id).values(active = False)
        result = await session.exec(update_command)

        return result.rowcount == 1


    async def activate_account(self, account_id: uuid.UUID, session: AsyncSession) -> bool:
        update_command=update(Account).where(Account.id==account_id).values(active=True)
        result=await session.exec(update_command)
        return result.rowcount==1

    async def exist_account_with_signin_name(self, signin_name: str, session: AsyncSession) -> bool:
        query = exists(Account).where(Account.signin_name==signin_name)

        result = await session.exec(query)

        return result.scalar()


    async def client_update_private_information(self, model: AccountPrivateInformationModel, session: AsyncSession) -> Optional[AccountPrivateInformation]:
        pass

    async def verify_identity_by_secret_qas(self, answers: Dict[str, str], session: AsyncSession) -> bool:
        pass

    async def change_secret_key(self, signin_name: str, pwd_hash: str, client_secret_segment: str, session: AsyncSession) -> bool:
        pass
    
    async def account_exists(self, idx: uuid.UUID, session: AsyncSession) -> bool:
        """
        :param idx:
        :param session:
        :return:
        """
        statement = exists(Account).where(Account.id == idx)
        result = await session.exec(statement)
        return result.scalar()
    
    async def private_information_exists(self, idx: uuid.UUID, session: AsyncSession) -> bool:
        statement = exists(AccountPrivateInformation).where(AccountPrivateInformation.id == idx)
        result = await session.exec(statement)
        return result.scalar()
    
    async def get_private_information_by_id(self, idx: uuid.UUID, session: AsyncSession, return_dto = True) \
            -> Union[AccountPrivateInformationModel, AccountPrivateInformation, None]:

        private_information_query = select(AccountPrivateInformation).where(AccountPrivateInformation.id == idx)
        result = await session.exec(private_information_query)
        record: AccountPrivateInformation | None = result.first()

        if record is None:
            return None

        if return_dto:
            return self._record_to_dto(AccountPrivateInformationModel, record)

        return record

    async def get_account_by_id(self, idx: uuid.UUID, session: AsyncSession,return_dto = False) -> Union[Account, AccountModel, None]:
        record : Account = await session.get_one(Account, idx)
        if record is None:
            return None
        if return_dto:
            return self._record_to_dto(AccountModel, record)
        return record

    async def get_account_by_name(self, name: str, session: AsyncSession) -> Optional[AccountModel]:
        query = select(Account).where(Account.name==name)
        result = await session.exec(query)
        record = result.first()

        if record is None:
            return None

        return self._record_to_dto(AccountModel, record)


    async def get_activation_by_id(self, idx: uuid.UUID, session: AsyncSession) -> Optional[EmailVerification]:
        record: Optional[EmailVerification] = await session.get_one(Account, idx)
        return record

    async def get_account_domain_by_id(self, idx: uuid.UUID, session: AsyncSession) -> Optional[Account]:
        account_query = select(Account).options(joinedload(Account.verification),
                                                        joinedload(Account.private_information)
                                                )\
                                       .where(Account.id == idx)

        result = await session.exec(account_query)

        return result.first()

    def _record_to_dto(self,dto_type: Type[AccountModel|EmailVerificationModel|AccountPrivateInformationModel],
                       record: Account|EmailVerification|AccountPrivateInformation) \
            -> AccountModel|EmailVerificationModel|AccountPrivateInformationModel:
        field_data = record.model_dump()

        return dto_type(**field_data)

    def _dto_to_record(self,record_type: Type[Account|EmailVerification|AccountPrivateInformation],
                       dto_data: AccountModel|EmailVerificationModel|AccountPrivateInformationModel) \
        -> Account|EmailVerification|AccountPrivateInformation:
        field_data = dto_data.model_dump()
        return record_type(**{field_name:field_data[field_name] for field_name in type(dto_data).model_fields().keys()})

    def _update_record(self,data_dict: Dict[str, Any],record: Account|EmailVerification|AccountPrivateInformation) -> None:
        for k,v in data_dict.items():
            setattr(record, k, v)


    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.account_readonly_fields: Set[str] = {"id"}
        self.account_private_fields: Set[str] = set()
        self.private_information_readonly_fields: Set[str] = {"id"}
        self.private_information_private_fields: Set[str] = set()



AccountDataAccess = AccountTable()

# if __name__ == "__main__":
#     pass
    # print(select(Account).join(AccountPrivateInformation))
    # print(select(Account, AccountPrivateInformation, AccountActivation)
    # .join(AccountPrivateInformation).join(AccountActivation).where(Account.signin_name == "aaa"))
    #print(select(Account).join(AccountActivation).where(AccountActivation.activation_key == 123))
    #print(select(Account).join(AccountActivation, isouter=True).where(AccountActivation.activation_key == 123))
    #print(select(Account).join(Account.activation).where(Account.active == True))
    #print(select(Account).join(Account.activation).join(Account.private_information))
    # print(select(Account)\
    # .options(contains_eager(Account.private_information), contains_eager(Account.activation)))

    #print(select(Account).options(joinedload(Account.private_information), joinedload(Account.activation)))

    #print(update(Account).where(Account.email == "aaa").values(active = True))


