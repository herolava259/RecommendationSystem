

import uuid
from typing import List, Optional, Mapping, Sequence, Set

from pydantic import BaseModel, Field, field_validator, model_validator

from pydantic_core.core_schema import FieldValidationInfo
import json
from datetime import datetime, timedelta
from uuid import UUID
from typing import Dict
from modules.account.utils import AccountHelper



from functools import partial


class AccountPrivateInformationModel(BaseModel):
    id: UUID = Field(default=uuid.uuid4)
    account_id: UUID = Field(default=uuid.uuid4)
    phone: str = Field(max_length=64)
    special_name: str = Field(max_length=512)
    address: str = Field(max_length=1024)
    post_code: str = Field(max_length=64)
    user_name: str = Field(max_length=64)
    preference: str = Field(max_length=1024)
    updated_at: datetime = Field(default_factory=datetime.now)
    secret_qas: Dict[str, str] = Field(default_factory=dict)
    secret_key: str = Field(max_length=1024)

class AccountModel(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    email: str = Field(max_length=64, default="abc@email.com")
    image_url: str | None = Field(max_length=1024, default=None)
    signin_name: str = Field(max_length=64)

    active: bool = Field(default=False)
    salt: str = Field(max_length=64)
    pwd_hash: str = Field(max_length=1024)
    personal_identifier: str = Field(max_length=256, default=partial(AccountHelper.create_random_token, length=256))
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    email_verified: bool=Field(default=False)

    # foreign models, depend on AccountModel,
    private_information: Optional[AccountPrivateInformationModel] = Field(default = None)
    email_verification: Optional["EmailVerificationModel"] = Field(default = None)
    claim_principal: Optional["AccountClaimPrincipalModel"]=Field(default=None)


class EmailVerificationModel(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    account_id: UUID = Field(default=uuid.uuid4)
    activation_key: int=Field(max_length=1024)
    expire_date: datetime =  Field(default_factory=datetime.now)
    is_verified: bool=Field(default=False)

    @classmethod
    def create_new(cls, account_model: AccountModel) -> "EmailVerificationModel":
        return EmailVerificationModel(account_id=account_model.id,
                                      activation_key = AccountHelper.random_number(8),
                                      expire_date = datetime.now() + timedelta(weeks=2),
                                      is_verified= False)

class AccountClaimModel(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    key: str = Field(default = "")
    value: str = Field(default = "")


class AccountClaimPrincipalModel(BaseModel):
    def __init__(self,account_id: UUID,system_claims_lookup: str| dict | None = None, custom_claims: str | dict | None = None):
        self.account_id = account_id
        if system_claims_lookup is None:
            system_claims_lookup = dict()
        elif isinstance(system_claims_lookup, str):
            system_claims_lookup = json.loads(system_claims_lookup)

        if custom_claims is None:
            custom_claims = dict()
        elif isinstance(custom_claims, str):
            custom_claims = json.loads(custom_claims)

        self.system_claims = system_claims_lookup
        self.custom_claims = custom_claims

    account_id: UUID = Field(default=uuid.uuid4)
    system_claims: Mapping[str, Sequence[str]] = Field(default_factory=dict)
    custom_claims: Mapping[str, Sequence[str]] = Field(default_factory=dict)

    def get_claim_of_account(self) -> dict:

        claims = {**self.custom_claims, **self.system_claims}

        return claims

    @classmethod
    def no_claim(cls) -> "AccountClaimPrincipalModel":
        return cls(account_id=uuid.UUID(int=0))

    @classmethod
    def create_new(cls, account_model: AccountModel, custom_claims: dict | None = None) -> "AccountClaimPrincipalModel":
        if custom_claims is None:
            custom_claims = {"user_name": account_model.signin_name,
                             "email": account_model.email,}
        else:
            custom_claims.update(**{"user_name": account_model.signin_name,
                             "email": account_model.email,})
        return AccountClaimPrincipalModel(account_id=account_model.id, system_claims_lookup=None, custom_claims=custom_claims)

    @property
    def all_claim(self) -> Dict[str, Set[str]]:

        claim_mapping: Dict[str, Set[str]] = dict()

        for k in (set(self.custom_claims.keys()) | set(self.system_claims.keys())):
            if claim_mapping.get(k, None) is None:
                claim_mapping[k] = set()
            if k in self.custom_claims:
                claim_mapping[k] |= self.custom_claims[k]
            if k in self.system_claims:
                claim_mapping[k] |= self.system_claims[k]
        return claim_mapping


    def query_by_key(self, key: str) -> Set[str]:

        claims: List[str] = []
        if key in self.custom_claims.keys():
            claims.extend(self.custom_claims[key])
        if key in self.system_claims.keys():
            claims.extend(self.system_claims[key])
        return set(claims)

# TODO: implement later

from enum import Enum

class AccountClaimGroupModel(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    claims: List[AccountClaimModel] = Field(default_factory=list)

class AccountState(str, Enum):
    Pending = "Pending"
    Active = "Active"
    Dangling = "Dangling"
    Inactive = "Inactive"
    ScheduledDeactivate = "ScheduledDeactivate"

