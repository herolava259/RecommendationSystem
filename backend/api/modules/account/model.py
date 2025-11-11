

import uuid
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator

from pydantic_core.core_schema import FieldValidationInfo

import re
from datetime import datetime, timedelta
from uuid import UUID
from typing import Dict

class CreateAccountRequest(BaseModel):
    email: str
    phone: str = Field(max_length=64)
    signin_name: str = Field(max_length=64)
    password: str = Field(max_length=64)
    confirm_password: str = Field(max_length=64)
    active: bool = Field(default=False)

    model_config = {
        "json_schema_extra": {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "username": "johndoe",
                "email": "johndoe123@co.com",
                "password": "testpass123",
            }
        }
    }

class CreateAccountResponse(BaseModel):
    succeed: bool = Field(default=False)
    response_message: str = Field(max_length=64)
    navigate_home: bool = Field(default=False)
    need_verify_email: bool = Field(default=False)
    additional_msg: dict = Field(default_factory=dict)


class LoginRequest(BaseModel):
    email: str
    signin_name: str = Field(max_length=64)
    password: str = Field(max_length=1024)
    check_sum: str = Field(max_length=256)

    @field_validator("password")
    def validate_password(cls, value):
        pass
    @model_validator(mode="after")
    def validate_request(self):
        pass


class ForgetPasswordRequest(BaseModel):
    email: str
    access_token: str = Field(default="")
    personal_identifier: str = Field(default="")
    check_sum: str = Field(default="")

class ForgetPasswordResponse(BaseModel):
    succeed: bool = Field(default=False)


class ChangePasswordRequest(BaseModel):
    signin_name: str = Field(max_length=1024)
    password: str = Field(max_length=1024)
    new_password: str = Field(max_length=1024)
    confirm_password: str = Field(max_length=1024)
    check_sum: str = Field(max_length=256)

class ChangePasswordResponse(BaseModel):
    succeed: bool = Field(default=False)
    stay_logged_in: bool = Field(default=False)
    token_stale: bool = Field(default=False)
    need_confirm_email: bool = Field(default=False)
    response_message: str = Field(max_length=2048)

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class NewAccessTokenResponse(BaseModel):
    succeed: bool = Field(default=False)
    expire_time: timedelta = Field(default=timedelta(minutes=60))
    access_token: str = Field(max_length=1024)


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
    id: UUID = Field(default=uuid.uuid4)
    email: str
    image_url: str = Field(max_length=1024)
    signin_name: str = Field(max_length=64)
    is_verified: bool = Field(default=False)
    active: bool = Field(default=False)
    pwd_hash: str = Field(max_length=1024)
    personal_identifier: str = Field(max_length=2048)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    private_information: Optional[AccountPrivateInformationModel] = Field(default_factory=AccountPrivateInformationModel)


class LogoutRequest(BaseModel):
    access_token: str = Field(default = "")
class LogoutResponse(BaseModel):
    succeed: bool = Field(default = True)


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str
    expire: int
    refresh_token: str
    alg_type: str
    claim: str

class ChangePersonalAccountInformationRequest(BaseModel):
    new_address: str = Field(max_length=1024)
    new_phone_number: str = Field(max_length=64)
    new_preference: str = Field(max_length=1024)
    new_postcode: str = Field(max_length=32)
    login_model: Optional[LoginRequest] = Field(default = None)
    new_nick_name: str = Field(max_length=512)

class ChangeAccountInformationResponse(BaseModel):
    succeed: bool = Field(default = False)
    confirmed_address: str = Field(max_length=1024)
    confirmed_phone: str = Field(max_length=64)
    confirmed_postcode: str = Field(max_length=32)
    confirmed_preference: str = Field(max_length=1024)



# TODO: implement later

from enum import Enum

class AccountState(str, Enum):
    Pending = "Pending"
    Active = "Active"
    Dangling = "Dangling"
    Inactive = "Inactive"
    ScheduledDeactivate = "ScheduledDeactivate"

class ConfirmChangePasswordRequest(BaseModel):
    pass

class ConfirmChangePasswordResponse(BaseModel):
    pass