import uuid
from datetime import datetime
from typing import List, Dict, Optional


from pydantic import BaseModel, Field, Field, field_validator, model_validator

from pydantic_core.core_schema import FieldValidationInfo

# TODO: add field validation for requests


class CreateUserSessionRequest(BaseModel):
    signin_name: str = Field(...)
    password: str = Field(...)

class CreateUserSessionResponse(BaseModel):
    session_key: str = Field(...)
    expire_in: datetime = Field(...)


class CreateUserRequest(BaseModel):

    first_name: str = Field(...)
    last_name: str = Field(...)
    account_id: uuid.UUID = Field(...)
    nick_name: str = Field(...)
    session_key: str = Field(...)

    country: str = Field(...)
    city: str = Field(...)
    province: str = Field(...)
    hometown: str = Field(...)
    street: str = Field(...)
    home_number: int = Field(...)
    hobbies: List[str] = Field(...)
    bio: Optional[str] = Field(...)


    gender: str = Field(...)

    age: int = Field(...)
    date_of_birth: datetime = Field(...)
    verified_email: str = Field(...)

    additional_info: Dict[str, str] = Field(...)


class CreateUserResponse(BaseModel):
    succeed: bool = Field(default = False)
    verify_key: str = Field(default = False)

class UserModel(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    account_id: uuid.UUID = Field(...)
    nick_name: str = Field(...)

    gender: str = Field(...)

    age: int = Field(...)
    date_of_birth: datetime = Field(...)

    additional_info: Dict[str, str] = Field(...)

    country: str = Field(...)
    city: str = Field(...)
    province: str = Field(...)
    hometown: str = Field(...)
    street: str = Field(...)
    home_number: int = Field(...)
    hobbies: List[str] = Field(...)
    bio: Optional[str] = Field(...)

    image_wrapper_url: Optional[str] = Field(...)
    image_thumb_url: Optional[str] = Field(...)


    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)

class UpdateUserRequest(BaseModel):
    first_name: Optional[str] = Field(...)
    last_name: Optional[str] = Field(...)
    nick_name: Optional[str] = Field(...)

    gender: Optional[str] = Field(...)

    age: Optional[int] = Field(...)
    date_of_birth: Optional[datetime] = Field(...)
    additional_info: Optional[Dict[str, str]] = Field(...)

    country: Optional[str] = Field(...)
    city: str | None = Field(...)
    province: str | None = Field(...)
    hometown: str|None = Field(...)
    street: str|None = Field(...)
    home_number: int|None = Field(...)
    hobbies: List[str] | None = Field(...)
    bio: Optional[str] = Field(...)

class UploadImageRequest(BaseModel):
    user_id: Optional[uuid.UUID] = Field(...)
    account_id: Optional[uuid.UUID] = Field(...)
    image_name: str = Field(...)
    data: bytes = Field(...)
    size: int = Field(...)
    format: str = Field(...)
    image_type: str = Field(...)

class UploadImageResponse(BaseModel):
    succeed: bool = Field(default = False)
    img_name: str = Field(...)



# TODO: implement later
class UserRoleModel(BaseModel):
    """Relationship between User and Role"""
    pass

class RoleModel(BaseModel):
    pass

class RoleGroupModel(BaseModel):
    role_list: List[RoleModel]
    pass

class RoleClaimModel(BaseModel):
    role_id: uuid.UUID
    claims: Dict[str, str]
    pass

class ResourceModel(BaseModel):
    pass

class CompositeAccessActionModel(BaseModel):
    pass

class RoleDefaultModel(RoleModel):
    ## default role of resource when a resource is created
    ## include owner, reader, writer
    pass


class ResourcePermissionModel(BaseModel):
    resource_id: uuid.UUID
    ## traditional access type: create, update, delete, read

    ## composite access type: include traditional access type and expire time of the permission or owner
    # evict the permission, is combination of the traditional access action

class ResourcePolicyModel(BaseModel):
    resource_id: uuid.UUID

class ResourceStaticModel(ResourceModel):
    """Include files, information is persistent"""

class ResourceDynamicModel(ResourceModel):
    """"computation resource"""



