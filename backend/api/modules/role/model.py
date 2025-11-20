import uuid
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict

from pydantic_core.core_schema import FieldValidationInfo

import re
from datetime import datetime, timedelta
from uuid import UUID
from typing import Dict