import uuid
from typing import List, Optional, Literal

from pydantic import BaseModel, Field, field_validator, model_validator

from pydantic_core.core_schema import FieldValidationInfo

import re
from datetime import datetime, timedelta
from uuid import UUID
from typing import Dict, Literal, Any


## dtos model

#abstract model

class PeopleModel(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    name: Optional[str] = None

class RelationshipModel(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    type: Literal["one-to-one", "one-to-many", "many-to-many"] = Field(
        default="one-to-one",
    )

# detail model


#I. some stuffs oriented movie
class MovieModel(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    title: str = Field(default="Title")
    summary: str = Field(default="Summary")
    duration: int = Field(default=0)
    release_date: datetime = Field(default=datetime.now())
    imdb_score: float = Field(default=0.0)
    type: Literal["tv-series-show", "film-season-short", "block-bluster", "feature-film"] = Field()


class MovieDetailModel(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    movie_id: UUID = Field(default_factory=uuid.uuid4)
    description: str = Field(default="")
    country: str = Field(default="")
    status: Literal["unknown", "new", "released"] = Field(default="unknown")
    tagline: str = Field(default="")
    original_language: str = Field(default="")
    original_title: str = Field(default="")
    spoken_languages: Dict[str, Any] = Field(default_factory=dict)
    network: str = Field(default="")
    director: str = Field(default="")
    writer: str = Field(default="")

class MovieGalleryModel(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    movie_id: UUID = Field(default_factory=uuid.uuid4)
    number: int = Field(default=0)


class MovieMediaInfoModel(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    is_main: bool = Field(default=False)
    image_url: str = Field(default=None)
    movie_id: UUID = Field(default_factory=uuid.uuid4)
    gallery_id: UUID = Field(default_factory=uuid.uuid4)
    type: Literal["image", "short"] = Field(default="movie-gallery")

class GenreModel(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    name: str = Field(default= "Action")

class MovieMetadataModel(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    movie_id: UUID = Field(default_factory=uuid.uuid4)
    resource_url: str = Field(default=None)



class TagModel(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)


# I.1 Movie Relationship with  Tag, Genre

class MovieTagRelationshipModel(RelationshipModel):
    """Many-to-many relationship."""
    tag_id: UUID = Field(default_factory=uuid.uuid4)
    movie_id: UUID = Field(default_factory=uuid.uuid4)

class MovieGenreRelationshipModel(RelationshipModel):
    """Many-to-many relationship."""
    genre_id: UUID = Field(default_factory=uuid.uuid4)
    movie_id: UUID = Field(default_factory=uuid.uuid4)

#II. relate to humans and relationship between

class StaffModel(PeopleModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    company_id: UUID = Field(default_factory=uuid.uuid4)

class ActorModel(PeopleModel):
    name: Optional[str] = Field(default= "Action")

class MovieDirectorModel(StaffModel):
    name: Optional[str] = Field(default= "Action")
    movie_id: UUID = Field(default_factory=uuid.uuid4)


class MovieCrewModel(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    movie_id: UUID = Field(default_factory=uuid.uuid4)
    production_company_id: UUID = Field(default_factory=uuid.uuid4)

class MovieCastModel(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    movie_id: UUID = Field(default_factory=uuid.uuid4)


class MovieCharacterModel(PeopleModel):
    movie_id: UUID = Field(default_factory=uuid.uuid4)
    actor_id: UUID = Field(default_factory=uuid.uuid4)

class MovieWriterModel(PeopleModel):
	pass


#II. organization

class OrganizationModel(BaseModel):
	id: UUID = Field(default_factory=uuid.uuid4)

class ProductionCompanyModel(OrganizationModel):
    name: Optional[str] = Field(default= "Action")
    country: Optional[str] = Field(default= "US")

class StudioModel(OrganizationModel):
    name: Optional[str] = Field(default= "Action")
    country: Optional[str] = Field(default= "US")

class MovieProductionRelationshipModel(RelationshipModel):
	"""Many-to-many relationship."""
	movie_id: UUID = Field(default_factory=uuid.uuid4)
	production_company_id: UUID = Field(default_factory=uuid.uuid4)

class MovieStudioRelationshipModel(RelationshipModel):
	"""Many-to-many relationship."""
	movie_id: UUID = Field(default_factory=uuid.uuid4)
	studio_id: UUID = Field(default_factory=uuid.uuid4)


#IV. reviews, rating, voting, like/dislike, comments => movie-oriented

class MovieInteractionModel(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    created_at: datetime = Field(default_factory=datetime)
    updated_at: datetime = Field(default_factory=datetime)
    movie_id: UUID = Field(default_factory=uuid.uuid4)
    user_id: UUID = Field(default_factory=uuid.uuid4)

class MovieReviewModel(MovieInteractionModel):
    review_text: str = Field(default_factory=str)
    created_at: datetime = Field(default_factory=datetime)
    updated_at: datetime = Field(default_factory=datetime)
    rating: int = Field(default = 0)

class MovieCommentModel(MovieInteractionModel):
    content: str = Field(default_factory=str)
    created_at: datetime = Field(default_factory=datetime)
    updated_at: datetime = Field(default_factory=datetime)

class CommentVotingModel(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    comment_id: UUID = Field(default_factory=uuid.uuid4)
    user_id: UUID = Field(default_factory=uuid.uuid4)
    up_or_down_vote: bool = Field(default=True)

class MoviePreferenceModel(MovieInteractionModel):
    """preference movie of a user"""
    pass

class MovieBlogModel(MovieInteractionModel):
    """blog about movie of a user"""
    content: str = Field(default_factory=str)

# intent

class SubscriptionModel(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    movie_id: UUID = Field(default_factory=uuid.uuid4)