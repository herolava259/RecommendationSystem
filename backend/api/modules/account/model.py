

import uuid
from typing import List,Optional,Mapping,Sequence, Self

from pydantic import BaseModel, Field, field_validator, model_validator

from pydantic_core.core_schema import FieldValidationInfo
import json
import re
from datetime import datetime, timedelta
from uuid import UUID
from typing import Dict

from api.modules.account.domain import EmailVerification


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
    personal_identifier: str = Field(max_length=2048)
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

class AccountClaimModel(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    key: str = Field(default = "")
    value: str = Field(default = "")


class AccountClaimPrincipalModel(BaseModel):
    def __init__(self,account_id: UUID,system_claims_lookup: str, custom_claims: str):
        self.account_id = account_id
        self.system_claims = json.loads(system_claims_lookup)
        self.custom_claims = json.loads(custom_claims)

    account_id: UUID = Field(default=uuid.uuid4)
    system_claims: Mapping[str, Sequence[str]] = Field(default_factory=dict)
    custom_claims: Mapping[str, Sequence[str]] = Field(default_factory=dict)

    def get_claim_of_account(self) -> dict:

        claims = {**self.custom_claims, **self.system_claims}

        return claims

    @staticmethod
    def no_claim(cls) -> Self:
        return cls(account_id=uuid.UUID(int=0))


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

