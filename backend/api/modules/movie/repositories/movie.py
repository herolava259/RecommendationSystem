from sqlmodel.ext.asyncio.session import AsyncSession


from modules.bases.supports.implementation import SupportRepository
from modules.movie.domain import Movie
from modules.movie.model import MovieModel


class MovieTable(SupportRepository[Movie, MovieModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(Movie,MovieModel,session)

