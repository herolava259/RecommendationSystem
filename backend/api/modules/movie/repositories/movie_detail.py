from sqlmodel.ext.asyncio.session import AsyncSession

from modules.bases.supports.implementation import SupportRepository
from modules.movie.domain import MovieDetails
from modules.movie.model import MovieDetailsModel


class MovieDetailTable(SupportRepository[MovieDetails, MovieDetailsModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(MovieDetails, MovieDetailsModel, session)