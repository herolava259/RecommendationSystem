from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructures.persistence.postgresql.db import get_session
from modules.bases.supports.abstraction import TEntity, TModel, ISupportRepository
from typing import Type, Generic, Annotated, TypeVar, Literal
from abc import ABC, abstractmethod
from modules.bases.supports.implementation import SupportRepository

import uuid


class UseCase(ABC):
    pass

class Endpoint(ABC):
    verb: Literal["GET", "POST", "PUT", "PATCH", "DELETE"]

    pass

TUseCase = TypeVar("TUseCase", bound=UseCase)
TEndpoint = TypeVar("TEndpoint", bound=Endpoint)
class ClientSide(ABC):
    pass

class ServerSide(ABC):
    pass

class UseCaseBuilder(ABC):
    @abstractmethod
    def build(self) -> TUseCase:
        pass


class CRUDRouter(ABC,Generic[TEntity, TModel],APIRouter):

    def __init__(self,entity_type: Type[TEntity], dto_type: Type[TModel],entity_name: str,prefix_path: str| None = None, **kwargs):

        super().__init__(**kwargs)

        self.entity_name = entity_name

        self.prefix_path = prefix_path or "crud"

        self.entity_type: Type[TEntity] = entity_type
        self.dto_type: Type[TModel] = dto_type

        self.setup_crud_endpoints()


    def setup_crud_endpoints(self):

        @self.get(path= f"/{self.entity_name}/{self.prefix_path}/get_by_id")
        async def get_by_id(idx: Annotated[uuid.UUID, Query()], session:Annotated[AsyncSession, Depends(get_session)]):
            repo: ISupportRepository[TEntity, TModel] = SupportRepository(self.entity_type, self.dto_type, session)

            return await repo.find_by_id(idx)

        # base operations

        # update


        # delete

        # create


        # slightly advanced








