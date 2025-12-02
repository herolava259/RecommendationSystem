from abc import ABC, abstractmethod
from uuid import UUID

from pydantic import BaseModel
from typing import Dict, Any, List, Generator, Tuple, Sequence, TypeVar, Optional, Generic

from sqlmodel import SQLModel

TModel = TypeVar('TModel', bound=BaseModel)
TEntity = TypeVar('TEntity', bound=SQLModel)

class ISupportRepository(ABC, Generic[TEntity,TModel]):

    @abstractmethod
    async def exist_record(self, idx: UUID) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def find_by_id(self, idx: UUID) -> TModel:
        raise NotImplementedError()


    @abstractmethod
    async def find_by_field(self, field_name: str, value: Any) -> List[TModel]:
        raise NotImplementedError()


    @abstractmethod
    async def find_all(self) -> List[TModel]:
        raise NotImplementedError()

    @abstractmethod
    async def find_all_by_condition(self, condition: Dict[str, Any]) -> Sequence[TModel] | Generator[TModel, None, None]:
        raise NotImplementedError()

    @abstractmethod
    async def update(self, model: TModel, refresh_data = False) -> Tuple[bool, Optional[TModel]]:
        raise NotImplementedError()

    @abstractmethod
    async def partial_update(self, model: TModel, update_properties: List[str],
                             refresh_data: bool = False) -> Tuple[bool, Optional[TModel]]:
        raise NotImplementedError()

    @abstractmethod
    async def query_raw(self, query_question: str, parameters: Dict[str, Any]) -> List[TModel]:
        raise NotImplementedError()

    @abstractmethod
    async def query_raw_take_first(self, query_question: str, parameters: Dict[str, Any]) -> TModel:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, model: TModel, ) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def delete_by_id(self, idx: UUID) -> TModel:
        raise NotImplementedError()


from enum import Enum

class RestrictAccessType(str, Enum):
    ReadOnly = 1
    Writable = 2
    Readable = 3
    Constant = 3
    RequireRole = 4
    AuthWritable = 5


class RestrictActionType(str, Enum):
    NoPublic = 1
    Private = 2
    Public = 3