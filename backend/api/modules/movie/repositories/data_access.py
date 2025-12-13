from typing import Set, Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from infrastructures.persistence.postgresql.db import get_session
from modules.movie.domain import MovieDetailTable
from modules.movie.repositories.movie import MovieTable


class MovieDataAccess(object):
    def __init__(self,session: Annotated[AsyncSession,Depends(get_session)]):

        self.session = session
        # data tables
        self.movie_table= MovieTable(self.session)
        self.movie_detail_table = MovieDetailTable(self.session)