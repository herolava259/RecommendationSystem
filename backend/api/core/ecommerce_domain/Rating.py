from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from enum import Enum


class NumOfStar(int, Enum):
    One = 1,
    Two = 2,
    Three = 3,
    Four = 4
    Five = 5

class SentimentType(int, Enum):
    Like = 1,
    Dislike = 2,
    Care = 3,
    Angry = 4,
    Boring = 5,
    Sadness = 6,

class SatisfiedLevel(int, Enum):
    VeryUnsatisfied = 1,
    PrettyUnsatisfied = 2,
    Unsatisfied = 3,
    Neutral = 4,
    PrettySatisfied = 5,
    VerySatisfied = 6,


class StarRating(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    star: NumOfStar = Field(default_factory=NumOfStar)
    user_id: UUID = Field(default_factory=uuid4)

class SentimentResponse(BaseModel):
    sentiment: SentimentType = Field(default_factory=SentimentType)
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID = Field(default_factory=uuid4)

class SatisfiedResponse(BaseModel):
    level: SatisfiedLevel = Field(default_factory=SatisfiedLevel)
    id: UUID = Field(default_factory=uuid4)
    user_id: UUID = Field(default_factory=uuid4)
