import uuid
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict

from pydantic_core.core_schema import FieldValidationInfo

import re
from datetime import datetime, timedelta
from uuid import UUID
from typing import Dict



class OAuthSessionModel(BaseModel):
    id: uuid.UUID
    user_id: str
    provider: str
    token: dict
    expires_at: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class OAuthSessionResponse(BaseModel):
    id: str
    account_id: str
    user_id: str
    provider: str
    expires_at: datetime
