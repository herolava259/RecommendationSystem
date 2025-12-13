from abc import ABC
from uuid import UUID, uuid4

from datetime import datetime, timedelta

from sqlmodel import Column, Field, Relationship, SQLModel, ForeignKey
import sqlalchemy.dialects.postgresql as pg
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlmodel import select, exists, update, delete

# import type
from typing import Optional, Literal, Set, Dict, Any

from sqlmodel import ARRAY, VARCHAR, JSON, Text, String, Enum, Double

import logging

from modules.bases.supports.EntityBase import EntityBase
from modules.bases.supports.implementation import SupportRepository
from modules.movie.model import (
    MovieModel,
    MovieDetailsModel,
    MovieGalleryModel, RelationshipType, MovieStatus,

)

####
# general entities
####

class Person(SQLModel,ABC, table= False):
    id: UUID = Field(sa_column = Column(pg.UUID, primary_key = True, default = uuid4, nullable= False, unique = True, server_default = None))
    name: Optional[str] = Field(sa_column= Column(pg.VARCHAR, nullable=True))

class RelationshipBase(SQLModel,ABC, table=False):
    type: RelationshipType = Field(sa_column= Column(pg.ENUM, default = RelationshipType.OneOne))


###
# Domain entities
###
class Movie(EntityBase, table=True):

    __tablename__ = 'movie'
    # id: UUID = Field(sa_column=Column(pg.UUID, primary_key=True, default=uuid4, nullable=False, server_default=None))
    title: str = Field(nullable=False, default="movie-title")
    summary: str = Field(nullable=False, default="movie-summary")
    duration: int = Field(nullable=True, default=120)
    release_date: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    imdb_score: Optional[float] = Field(nullable=False, default=None)

    type: Literal["tv-series-show", "film-season-short", "block-bluster", "feature-film"] = Field(nullable=False, default="film-season-short")


    def __repr__(self):
        return f"<Movie {self.title}"
    # define constraints: foreign key, index, unique, auto-increment,...


class MovieDetails(EntityBase, table=True):

    __tablename__ = "movie_details"

    #id: UUID = Field(sa_column=Column(pg.UUID, primary_key=True, default=uuid4, nullable=False, server_default=None))
    description: str = Field(nullable=False, default="movie-description")
    country: str = Field(nullable=False, default="movie-country")
    status: MovieStatus = Field(sa_column=Column(pg.ENUM,name="movie_status_enum", default = MovieStatus.Unknown, nullable=False))
    tagline: str = Field(nullable=False, default="movie-tagline")
    original_language: str = Field(nullable=False, default="movie-original-language")
    original_title: str = Field(nullable=False, default="original-title")
    spoken_languages: Dict[str, Any] = Field(sa_column=Column(pg.JSONB, nullable=False, server_default="{}")) # use gin index when create alembic migration
    network: str = Field(nullable=False, default="movie-network")
    director: Dict[str, Any] = Field(sa_column=Column(pg.JSONB, nullable=False, server_default="{'name': 'director-name', 'id': '00000000-0000-0000-0000-000000000000'}"))
    writer: Dict[str, Any] = Field(sa_column=Column(pg.JSONB, nullable=False, server_default="{'name': 'writer-name', 'id': '00000000-0000-0000-0000-000000000000'}"))

    # foreign key
    movie_id: UUID = Field(sa_column=Column(pg.UUID, ForeignKey("movie.id")))


    def __repr__(self):
        return f"Movie-Details {self.description}"

class MovieGallery(SQLModel, table=True):
    __tablename__ = "movie_gallery"




#####
## database access
####

class MovieTable(SupportRepository[Movie, MovieModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(Movie,MovieModel,session)

class MovieDetailTable(SupportRepository[MovieDetails, MovieDetailsModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(MovieDetails, MovieDetailsModel, session)