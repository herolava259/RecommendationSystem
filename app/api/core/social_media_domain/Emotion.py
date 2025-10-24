import uuid

from pydantic import BaseModel, Field

from uuid import UUID, uuid4

import datetime
from datetime import date
from enum import Enum

class EmotionType(int, Enum):
    Likes = 0,
    DisLikes = 1,
    Angry = 2,
    Care = 3,
    Sadness = 4,
    Boring = 5

class Emotion(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    emotion_type: EmotionType = Field(default=EmotionType.Likes)
    content: str = Field(default = "")
    created_date: date = Field(default_factory=datetime.datetime.now)
    feed_id: UUID = Field(default=uuid4)