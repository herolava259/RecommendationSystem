import uuid
from typing import List,Optional,Mapping,Sequence

from pydantic import BaseModel, Field, field_validator, model_validator

from pydantic_core.core_schema import FieldValidationInfo
import json
import re
from datetime import datetime, timedelta
from uuid import UUID
from typing import Dict

from api.modules.account.model import AccountModel


class CreateAccountRequest(BaseModel):
    email: str
    phone: str = Field(max_length=64)
    signin_name: str = Field(max_length=64)
    password: str = Field(max_length=64)

    model_config = {
        "json_schema_extra": {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "signin_name": "johndoe",
                "email": "johndoe123@co.com",
                "password": "testpass123",
            }
        }
    }

    def to_account_model(self) -> AccountModel:

        account_data = self.model_dump()
        return AccountModel(**account_data)

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

    @field_validator("signin_name")
    @classmethod
    def validate_signin_name(cls, value: str) -> str:
        return value

    @model_validator(mode="after")
    def validate_request(self):
        return self

class AccessTokenResponse(BaseModel):
    access_token: str
    user_data: dict
    token_type: str
    expire: int
    refresh_token: dict
    alg_type: str
    claim: dict

class LoginResponse(BaseModel):
    succeed: bool
    response_message: str
    access_token: AccessTokenResponse | dict | None = Field(default = None)

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
    current_access_token: dict = Field(default_factory=dict)

class NewAccessTokenResponse(BaseModel):
    succeed: bool = Field(default=False)
    new_access_token: dict = Field(max_length=1024)

class EmailVerificationRequest(BaseModel):
    activation_key: int = Field(default=0)
    email: str = Field(max_length=2048)
    signin_name: str = Field(max_length=64)
    location_key: str = Field(default="")

class EmailConfirmationResponse(BaseModel):
    succeed: bool = Field(default=False)

class LogoutRequest(BaseModel):
    access_token: str = Field(default = "")
class LogoutResponse(BaseModel):
    succeed: bool = Field(default = True)

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

class ConfirmChangePasswordRequest(BaseModel):
    pass

class ConfirmChangePasswordResponse(BaseModel):
    pass